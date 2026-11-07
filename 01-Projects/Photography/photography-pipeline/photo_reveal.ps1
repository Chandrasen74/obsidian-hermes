param([string]$u)
# photo-view: handler: reveals a file in Explorer, photography-library only
$root = 'C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\Photography\photography-library'
$p = $u
# Strip scheme (handles photo-view:, photo-view://, photo-view:///)
if ($p -match '^photo-view:(/*)(.*)$') { $p = $Matches[2] }
# Handle file:/// prefix that may remain
if ($p -match '^file:(/*)(.*)$') { $p = $Matches[2] }
try { $p = [Uri]::UnescapeDataString($p) } catch {}
$p = ($p -replace '/', '\').Trim('"').Trim()
# Normalize drive letter form like \C:\... or C:\...
if ($p -match '^\\([A-Za-z]:.*)$') { $p = $Matches[1] }
$rootNorm = $root.TrimEnd('\') + '\'
if (($p.StartsWith($rootNorm, [System.StringComparison]::OrdinalIgnoreCase) -or $p.Equals($root.TrimEnd('\'), [System.StringComparison]::OrdinalIgnoreCase)) -and (Test-Path -LiteralPath $p)) {
  Start-Process -FilePath explorer.exe -ArgumentList ("/select,`"" + $p + "`"")
} else {
  # Fallback: copy path to clipboard so user can navigate manually
  try { Set-Clipboard -Value $p } catch {}
}
