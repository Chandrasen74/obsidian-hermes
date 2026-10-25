---
name: Multiroom Audio (Snapcast)
tags: ["#status/archived", "#type/project", "#domain/audio"]
---

# Multiroom Audio with Snapcast

Self-hosted, synchronised multi-room audio on the home LAN. One server holds the
library and streams it; every client device plays in sync. Built October 2026,
archived as a working configuration record.

## What it does

- Plays a 51-track FLAC library (Kishore, Lata, Rafi, Asha classics from a YouTube
  Music playlist) on any number of devices at once, in sync.
- One web page controls both the music (play/pause/next/track pick) and the
  speakers (per-device volume, mute, sync offset).
- Runs fully on demand. Nothing starts at boot, nothing plays until asked.

## Architecture

```
        MPD (library + control)          snapserver
  /var/lib/mpd/music (51 FLAC)  -->  pipe /var/lib/mpd/snapfifo
                                             |
                                    TCP 1704 (audio stream)
                                             |
        +------------------+-----------------+------------------+
        |                  |                                    |
  Windows PC          Android phone                       Browser
  snapclient.exe      Snapdroid APK                      Snapweb / merged remote
  (latency 100)       (latency 0)                        (latency 160)

  Control plane: TCP 1705 JSON-RPC (newline-delimited, raw TCP)
  Web: :1804 Snapweb, :8080 custom merged remote
```

## Roles and addresses

| Item | Value |
|---|---|
| Windows PC LAN IP | 192.168.1.6 (DHCP, router 192.168.1.1) |
| PC Ethernet MAC | BC-EC-A0-30-B9-32 |
| WSL distro | Ubuntu 26.04, systemd enabled |
| WSL IP | 172.22.152.227, stable across shutdown/start cycles |
| Stream port | 1704 |
| Control port | 1705 |
| Snapweb | 1804 |
| Merged remote | 8080 |
| MPD | 6600 (localhost only) |

LAN reachability works through `netsh interface portproxy` entries mapping
0.0.0.0:PORT to 172.22.152.227:PORT, plus firewall rules named
`Snapcast TCP <port>` (1704, 1705, 1804, 8080, inbound allow, all profiles).
The portproxy entries are static config, not processes.

## Current operating model

Nothing auto-starts. Removed on 2026-10-25:

- Scheduled tasks `Snapcast Keepalive` and `Snapcast Refresh` (the 2-minute one
  caused a console window flash every cycle)
- Startup shortcut `Snapcast Client.lnk` and desktop `Play Music.lnk`
- systemd autostart for `snapserver`, `mpd`, `mpd-remote`, `mpd.socket`
  (all still installed, just `disabled`)
- The `sleep infinity` keep-alive inside WSL

Start and stop are manual scripts, run on request:

```
C:\snapcast\start-snapcast.cmd   # boots WSL, starts 3 services, runs mpc stop
C:\snapcast\stop-snapcast.cmd    # stops services, wsl --shutdown
```

`start-snapcast.cmd` calls `start-snapcast.sh` inside WSL. It always ends with
`mpc stop`, so the stream is silent until play is pressed.

## Using it

- Control page: `http://192.168.1.6:8080` (playlist + speakers)
- Advanced: `http://192.168.1.6:1804`
- Sound on this PC: `C:\snapcast\client-dist\Play Music.bat`
  (`snapclient.exe tcp://192.168.1.6:1704 --latency 100`)
- Phone: Snapdroid app, server `192.168.1.6`; APK also hosted at
  `http://192.168.1.6:1804/downloads/Snapcast.apk`
- Windows client zip: `http://192.168.1.6:1804/downloads/snapclient-win.zip`

## Adding music

```
wsl -d Ubuntu -u root -- yt2snap dl <YouTube-or-YT-Music-URL>
wsl -d Ubuntu -u root -- mpc update
```

Downloads land in `/var/lib/mpd/music`. `yt2snap` is a small yt-dlp wrapper kept
at `/usr/local/bin/yt2snap`, archived here as `scripts/yt2snap`.

## Sync and latency

Snapserver stores per-client latency, volume and name, keyed by client ID, and
restores them on reconnect.

| Client | Latency | Why |
|---|---|---|
| Windows PC (`snapclient.exe`) | 100 ms | FxSound DSP + WASAPI output delay |
| Browser (Snapweb) | 160 ms | browser audio path |
| Android (Snapdroid) | 0 ms | native fast path |

The 160 ms number was the point where offsets became inaudible by ear, not a
shared setting. A new device starts at 0 and can be nudged from the 8080 page.

## Files

This archive:
- `configs/snapserver.conf`, `configs/mpd.conf`
- `configs/mpd-remote.service` is under `scripts/`
- `scripts/mpd-remote.py` (source of the merged remote)
- `scripts/yt2snap`
- `scripts/start-snapcast.cmd`, `scripts/stop-snapcast.cmd`,
  `scripts/start-snapcast.sh`, `scripts/restore-portproxy.ps1`
- `logs/snapcast-build.log` (MSBuild output from the Windows client build)

Live working install (do not move, paths are absolute):
- `C:\snapcast\bin\Release\snapclient.exe` plus DLLs, built from source v0.35.0
- `C:\snapcast\client-dist\` player launcher and `settings.json`
- `C:\snapcast\mpd-remote.py` (deployed to `/root/mpd-remote.py` in WSL)
- `C:\snapcast\snapclient-win.zip`, `Snapcast.apk`, `samsungsnapclient.wgt`
- `C:\snapcast\` also contains the upstream snapcast git clone used to build

WSL:
- `/etc/snapserver.conf`: `[stream]` with
  `source = pipe:///var/lib/mpd/snapfifo?name=music&mode=read`, bind 0.0.0.0,
  port 1704; `[http]` 1804 with snapweb doc root. The FLAC/48 kHz/16-bit
  settings you see in `Server.GetStatus` are snapserver defaults, not written
  in this file.
- `/etc/mpd.conf`: `music_directory /var/lib/mpd/music`, FIFO output
  `path "/var/lib/mpd/snapfifo"` format `48000:16:2`
- `/root/mpd-remote.py`: live merged remote, unit `mpd-remote.service`
- `/var/lib/mpd/music/`: the 51 FLACs
- `/usr/share/snapserver/snapweb/downloads/`: hosted APK, wgt, client zip

## Merged remote (port 8080)

Single-file Python stdlib HTTP server, `ThreadingHTTPServer`, no dependencies.

- `GET /` page: now playing, progress, prev/play/next, speaker rows, playlist
- `GET /api/state`: MPD status plus snapserver clients via `Server.GetStatus`
- `GET /api/next|prev|toggle|play?n=`: transport via `mpc`
- `GET /api/vol?id=&percent=&muted=`: `Client.SetVolume`
- `GET /api/latency?id=&ms=`: `Client.SetLatency`
- `GET /api/muteall`

Snapserver control protocol gotcha: port 1705 is raw newline-delimited JSON-RPC,
not WebSocket. Send one JSON object plus `\n`, read a line back. WebSocket
clients get a JSON parse error because the `GET` handshake is parsed as JSON.

UI detail: the volume slider posts debounced on `input` and does not trigger a
full refresh, so the 3-second poll cannot fight the drag.

## Gotchas learned the hard way

- PowerShell piped into WSL mangles scripts (truncated `snapserver` to
  `snapserve`). Reliable pattern: base64 the script, decode inside WSL, or write
  a file and run it after `sed -i 's/\r$//'`.
- snapserver sources must live under `[stream]`; misplaced keys silently fall
  back to the stock `default` pipe.
- `file://` sources reject directories in snapserver 0.34 ("Not a regular file"),
  which is why MPD feeds a FIFO instead.
- The FIFO must sit in an mpd-writable directory; `/run` fails with permission
  denied. MPD deletes its FIFO on stop.
- snapclient on Windows resolved the hostname to an IPv6 link-local address and
  sat in SYN_SENT. Use the IPv4 literal in the launcher.
- WSL shut down when idle, taking the server with it. The old fix was a
  `sleep infinity` keep-alive; it is now intentionally gone, since the server
  only runs on demand.
- WSL mirrored networking was tried on 2026-10-25 to remove portproxy. The host
  could not reach its own mirrored ports and phone behaviour was unverifiable,
  so NAT plus portproxy was restored and is the supported setup.
- Deleting scheduled tasks needs elevation. A silent `-ErrorAction SilentlyContinue`
  made an early removal look successful when the tasks were still registered.
  Always verify with `Get-ScheduledTask`.
- WSL IP stayed 172.22.152.227 across repeated `wsl --shutdown` and start cycles,
  so the portproxy targets keep working. If it ever changes, re-run
  `restore-portproxy.ps1` elevated and update the IP inside it.

## Build notes (Windows client)

Built from the snapcast source tree in `C:\snapcast` with CMake and vcpkg on
Windows, release configuration, producing `bin\Release\snapclient.exe` v0.35.0.
Server side is the distro package, v0.34.0.

## Timeline

- 2026-10-18 evening: multinode mixer experiment started, then abandoned in
  favour of snapcast; vcpkg clone at 21:52
- 2026-10-18 night to 2026-10-19 midday: deps, client build, WSL server,
  50-track download, MPD FIFO wiring, sync tuning, phone and web clients
- 2026-10-19 to 2026-10-20: merged remote on 8080, volume/mute/sync controls,
  IP move from .3 to .6, watchdog added
- 2026-10-25: watchdog and all autostart removed, on-demand scripts created,
  this archive written
