param([string]$u)
# photo-view:// handler: reveals a file in Explorer, photography folder only
$root = 'C:\Users\Kanchan Verma\OneDrive\Desktop\photography'
$p = $u
if ($p -like 'photo-view:*') { $p = $p.Substring(11) }
try { $p = [Uri]::UnescapeDataString($p) } catch {}
$p = ($p -replace '/', '\').Trim('"').Trim()
if ($p.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $p)) {
  Start-Process -FilePath explorer.exe -ArgumentList ("/select,`"" + $p + "`"")
}
