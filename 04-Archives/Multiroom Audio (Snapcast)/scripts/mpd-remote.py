#!/usr/bin/env python3
"""Combined MPD + Snapcast web remote for the Snapcast setup. Serves on 0.0.0.0:8080."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
import socket
import subprocess

SNAP_HOST = '127.0.0.1'
SNAP_PORT = 1705

PAGE = r"""<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#111111">
<title>Snapcast Remote</title>
<style>
  * { box-sizing:border-box; }
  body { background:#111; color:#eee; font-family:system-ui,sans-serif; margin:0; padding:16px; text-align:center; }
  h1 { font-size:18px; color:#888; font-weight:600; letter-spacing:1px; margin:8px 0 18px; }
  .sect { text-align:left; max-width:520px; margin:26px auto 8px; font-size:11px; letter-spacing:2px; color:#666; font-weight:600; }
  #now { font-size:20px; margin:6px 0 4px; min-height:28px; }
  #sub { color:#999; margin-bottom:6px; min-height:20px; font-size:14px; }
  #bar { max-width:520px; height:4px; background:#222; border-radius:2px; margin:10px auto 4px; overflow:hidden; }
  #barfill { height:100%; width:0; background:#3d6ea8; transition:width .5s linear; }
  .row { display:flex; justify-content:center; gap:14px; margin:12px 0; }
  button.big { font-size:30px; width:76px; height:76px; border-radius:50%; border:none; background:#2a2a2a; color:#fff; }
  button.big:active { background:#3d6ea8; }
  #clients { max-width:520px; margin:0 auto; text-align:left; }
  .cli { padding:12px 14px; border-bottom:1px solid #262626; }
  .clitop { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
  .dot { width:8px; height:8px; border-radius:50%; background:#444; flex:none; }
  .dot.on { background:#4caf50; }
  .cname { flex:1; font-size:15px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .cli.off .cname { color:#777; }
  .sync { font-size:11px; color:#777; display:flex; align-items:center; gap:4px; }
  .sync input { width:44px; background:#1b1b1b; border:1px solid #333; color:#bbb; border-radius:4px; padding:2px 4px; font-size:11px; text-align:center; }
  .clirow { display:flex; align-items:center; gap:10px; }
  .mute { background:none; border:none; color:#eee; font-size:18px; width:30px; padding:0; flex:none; }
  .mute.off { color:#666; }
  .vol { flex:1; -webkit-appearance:none; appearance:none; height:4px; background:#333; border-radius:2px; outline:none; }
  .vol::-webkit-slider-thumb { -webkit-appearance:none; width:16px; height:16px; border-radius:50%; background:#3d6ea8; }
  .vol::-moz-range-thumb { width:16px; height:16px; border:none; border-radius:50%; background:#3d6ea8; }
  .pct { width:38px; text-align:right; font-size:13px; color:#999; flex:none; }
  #list { list-style:none; padding:0; margin:0 auto 80px; max-width:520px; text-align:left; }
  #list li { padding:12px 14px; border-bottom:1px solid #262626; font-size:15px; cursor:pointer; }
  #list li.cur { background:#1d3a57; }
  #list li:active { background:#3d6ea8; }
  #foot { color:#555; font-size:12px; margin:10px 0 40px; }
  #foot a { color:#5a8fc7; text-decoration:none; }
</style></head><body>
<h1>SNAPCAST REMOTE</h1>
<div id="now">loading...</div>
<div id="sub"></div>
<div id="bar"><div id="barfill"></div></div>
<div class="row">
  <button class="big" onclick="cmd('prev')" title="previous">&#9198;</button>
  <button class="big" id="pp" onclick="cmd('toggle')">&#9654;</button>
  <button class="big" onclick="cmd('next')" title="next">&#9197;</button>
</div>

<div class="sect">SPEAKERS</div>
<div id="clients"><div style="padding:0 14px;color:#666;font-size:13px">no clients seen yet</div></div>

<div class="sect">PLAYLIST</div>
<ul id="list"></ul>
<div id="foot"><a id="web" href="#">advanced (Snapweb)</a></div>

<script>
const nodes = {};
let current = {};

function secs(t){ const p=t.split(':').map(Number); if(p.some(isNaN)) return 0;
  return p.length===3 ? p[0]*3600+p[1]*60+p[2] : p.length===2 ? p[0]*60+p[1] : p[0]; }

function mkClient(c){
  const root = document.createElement('div');
  root.className = 'cli';
  const top = document.createElement('div'); top.className='clitop';
  const dot = document.createElement('span'); dot.className='dot';
  const name = document.createElement('span'); name.className='cname';
  const sync = document.createElement('span'); sync.className='sync';
  sync.append('sync ');
  const lat = document.createElement('input');
  lat.type='number'; lat.min=0; lat.max=500; lat.step=5;
  lat.onchange = () => fetch('/api/latency?id='+encodeURIComponent(c.id)+'&ms='+encodeURIComponent(lat.value));
  sync.append(lat, ' ms');
  top.append(dot, name, sync);
  const row = document.createElement('div'); row.className='clirow';
  const mute = document.createElement('button'); mute.className='mute';
  mute.textContent='\u{1F509}';
  const vol = document.createElement('input');
  vol.type='range'; vol.min=0; vol.max=100; vol.step=1; vol.className='vol';
  const pct = document.createElement('span'); pct.className='pct';
  let volTimer = null;
  vol.oninput = () => { pct.textContent = vol.value + '%'; clearTimeout(volTimer); volTimer = setTimeout(()=>sendVol(c.id, Number(vol.value), current[c.id] ? current[c.id].muted : false), 120); };
  vol.onchange = () => { clearTimeout(volTimer); sendVol(c.id, Number(vol.value), current[c.id] ? current[c.id].muted : false); };
  mute.onclick = () => {
    const st = current[c.id]; if(!st) return;
    sendVol(c.id, st.percent, !st.muted);
  };
  row.append(mute, vol, pct);
  root.append(top, row);
  return {root, dot, name, lat, vol, pct, mute};
}

function sendVol(id, percent, muted){
  fetch('/api/vol?id='+encodeURIComponent(id)+'&percent='+percent+'&muted='+(muted?1:0));
}

function renderClients(list){
  list = list.filter(c => c.connected || c.name !== 'Snapweb client');
  const box = document.getElementById('clients');
  let ph = document.getElementById('noclient');
  if(list.length === 0){
    if(!ph){
      ph = document.createElement('div');
      ph.id = 'noclient';
      ph.style.cssText = 'padding:0 14px;color:#666;font-size:13px';
      ph.textContent = 'no clients seen yet';
      box.appendChild(ph);
    }
  } else if(ph){ ph.remove(); }
  const seen = new Set();
  list.forEach(c => {
    seen.add(c.id);
    current[c.id] = c;
    if(!nodes[c.id]){ nodes[c.id] = mkClient(c); box.appendChild(nodes[c.id].root); }
    const n = nodes[c.id], h = n.root;
    h.classList.toggle('off', !c.connected);
    n.dot.classList.toggle('on', c.connected);
    n.name.textContent = c.name + (c.connected ? '' : ' (offline)');
    if(document.activeElement !== n.vol){ n.vol.value = c.percent; }
    n.pct.textContent = c.percent + '%';
    n.mute.textContent = c.muted ? '\u{1F507}' : '\u{1F509}';
    n.mute.classList.toggle('off', c.muted);
    if(document.activeElement !== n.lat){ n.lat.value = c.latency; }
  });
  Object.keys(nodes).forEach(id => {
    if(!seen.has(id)){ nodes[id].root.remove(); delete nodes[id]; delete current[id]; }
  });
}

async function refresh(){
  try{
    const s = await (await fetch('/api/state')).json();
    document.getElementById('now').textContent = s.song || 'nothing playing';
    document.getElementById('sub').textContent = s.state + (s.elapsed ? '   ' + s.elapsed + ' / ' + s.total : '');
    document.getElementById('pp').innerHTML = s.state==='play' ? '&#9646;&#9646;' : '&#9654;';
    const e = secs(s.elapsed||''), t = secs(s.total||'');
    document.getElementById('barfill').style.width = (s.state==='play' && t>0 ? Math.min(100, e/t*100) : (s.state==='pause' ? Math.min(100, e/t*100) : 0)) + '%';
    renderClients(s.clients || []);
    const ul = document.getElementById('list');
    if(s.playlist.length !== ul.children.length){
      ul.innerHTML='';
      s.playlist.forEach(t=>{
        const li=document.createElement('li');
        li.textContent = t.index + '. ' + t.title.replace(/\.[a-z0-9]+$/i,'');
        li.onclick=()=>fetch('/api/play?n='+t.index).then(refresh);
        ul.appendChild(li);
      });
    }
    Array.from(ul.children).forEach((li,i)=>li.classList.toggle('cur', (i+1)===s.index));
  }catch(e){ document.getElementById('now').textContent = 'server unreachable'; }
}
async function cmd(c){ await fetch('/api/'+c); refresh(); }
document.getElementById('web').href = 'http://'+location.hostname+':1804/';
refresh(); setInterval(refresh, 3000);
</script>
</body></html>
"""


def mpc(*args):
    return subprocess.check_output(['mpc'] + list(args), text=True).strip()


def snap_rpc(method, params=None, timeout=2.0):
    msg = {'id': 1, 'jsonrpc': '2.0', 'method': method}
    if params is not None:
        msg['params'] = params
    s = socket.create_connection((SNAP_HOST, SNAP_PORT), timeout=timeout)
    try:
        s.sendall((json.dumps(msg) + '\n').encode())
        buf = b''
        while b'\n' not in buf:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
        line = buf.split(b'\n')[0].strip()
        if not line:
            raise RuntimeError('empty reply from snapserver')
        return json.loads(line)
    finally:
        s.close()


def snap_clients():
    out = []
    try:
        server = snap_rpc('Server.GetStatus')['result']['server']
    except Exception:
        return out
    for g in server.get('groups', []):
        for c in g.get('clients', []):
            cfg = c.get('config') or {}
            vol = cfg.get('volume') or {}
            out.append({
                'id': c.get('id', ''),
                'name': (c.get('host') or {}).get('name') or c.get('id', '')[:8],
                'connected': bool(c.get('connected')),
                'percent': vol.get('percent', 100),
                'muted': bool(vol.get('muted')),
                'latency': cfg.get('latency', 0),
                'stream': g.get('stream_id', ''),
            })
    out.sort(key=lambda c: (not c['connected'], c['name'].lower()))
    return out


def state():
    out = mpc('status').splitlines()
    st = {'song': out[0] if out else '', 'state': 'stop', 'elapsed': '', 'total': '', 'index': None, 'playlist': [], 'clients': snap_clients()}
    if len(out) > 1:
        marker = out[1]
        st['state'] = 'pause' if marker.startswith('[paused') else 'play'
        parts = marker.split()
        try:
            st['index'] = int(parts[1].split('/')[0].lstrip('#'))
        except Exception:
            pass
        try:
            times = parts[2].split('/')
            st['elapsed'] = times[0]
            st['total'] = times[1] if len(times) > 1 else ''
        except Exception:
            pass
    for i, title in enumerate(mpc('playlist').splitlines(), 1):
        st['playlist'].append({'index': i, 'title': title})
    return st


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == '/':
            self.reply(200, PAGE.encode(), 'text/html; charset=utf-8')
            return
        try:
            if u.path == '/api/state':
                self.reply(200, json.dumps(state()).encode(), 'application/json')
                return
            if u.path == '/api/next':
                mpc('next')
            elif u.path == '/api/prev':
                mpc('prev')
            elif u.path == '/api/toggle':
                mpc('toggle')
            elif u.path == '/api/play':
                n = q.get('n', [None])[0]
                if n:
                    mpc('play', n)
            elif u.path == '/api/vol':
                cid = q.get('id', [None])[0]
                if not cid:
                    raise ValueError('missing id')
                pct = max(0, min(100, int(q.get('percent', ['100'])[0])))
                muted = q.get('muted', ['0'])[0] in ('1', 'true', 'True')
                r = snap_rpc('Client.SetVolume', {'id': cid, 'volume': {'percent': pct, 'muted': muted}})
                if 'error' in r:
                    raise RuntimeError(str(r['error']))
            elif u.path == '/api/latency':
                cid = q.get('id', [None])[0]
                if not cid:
                    raise ValueError('missing id')
                ms = max(0, min(1000, int(q.get('ms', ['0'])[0])))
                r = snap_rpc('Client.SetLatency', {'id': cid, 'latency': ms})
                if 'error' in r:
                    raise RuntimeError(str(r['error']))
            elif u.path == '/api/muteall':
                for c in snap_clients():
                    snap_rpc('Client.SetVolume', {'id': c['id'], 'volume': {'percent': c['percent'], 'muted': True}})
            else:
                self.reply(404, b'not found', 'text/plain')
                return
            self.reply(200, b'ok', 'application/json')
        except Exception as e:
            self.reply(500, str(e).encode(), 'text/plain')


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
