Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile('C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\deliverables\stills\layup-make-4.4s.png')
[System.Windows.Forms.Clipboard]::SetImage($img)
Start-Sleep -Milliseconds 400
[Console]::Out.Write('clipboard image: ' + [System.Windows.Forms.Clipboard]::ContainsImage())
