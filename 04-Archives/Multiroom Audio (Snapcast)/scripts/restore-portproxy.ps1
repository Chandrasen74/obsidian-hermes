# Recreates the portproxy rules for the stable WSL IP. Requires elevation (one time).
$ErrorActionPreference = 'SilentlyContinue'
$wslIp = '172.22.152.227'
foreach ($p in 1704,1705,1804,8080) {
    netsh interface portproxy delete v4tov4 listenport=$p listenaddress=0.0.0.0 | Out-Null
    netsh interface portproxy add v4tov4 listenport=$p listenaddress=0.0.0.0 connectport=$p connectaddress=$wslIp | Out-Null
}
"PORT_PROXY_READY"
netsh interface portproxy show v4tov4
