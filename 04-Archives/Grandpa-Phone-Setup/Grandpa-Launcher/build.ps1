# ============================================================================
#  build.ps1 - compiles the Home launcher APK with aapt2 + javac + d8.
#  No Gradle, no AndroidX, no Play services: pure framework app.
#
#  Usage:
#    .\build.ps1                # build dist\Home.apk
#    .\build.ps1 -Install       # build + adb install -r
#    .\build.ps1 -Install -SetRole   # also set as default home
# ============================================================================

param(
  [switch]$Install,
  [switch]$SetRole
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Join-Path $env:LOCALAPPDATA 'Android'
$sdk = Join-Path $root 'sdk'

$jdkDir = Get-ChildItem (Join-Path $root 'jdk17') -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $jdkDir) {
  throw 'no JDK under %LOCALAPPDATA%\Android\jdk17; run setup first'
}
$env:JAVA_HOME = $jdkDir.FullName
$env:Path = "$($jdkDir.FullName)\bin;$env:Path"

$jar = Join-Path $sdk 'platforms\android-34\android.jar'
$bt = Join-Path $sdk 'build-tools\34.0.0'
if (-not (Test-Path $jar)) {
  throw 'platform android-34 missing (run sdkmanager)'
}
if (-not (Test-Path (Join-Path $bt 'aapt2.exe'))) {
  throw 'build-tools 34.0.0 missing (run sdkmanager)'
}

$build = Join-Path $scriptDir 'build'
if (Test-Path $build) {
  Remove-Item $build -Recurse -Force
}
New-Item -ItemType Directory -Force -Path "$build\gen", "$build\classes", "$build\dex" | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $scriptDir 'dist') | Out-Null

Write-Host 'aapt2 compile'
& (Join-Path $bt 'aapt2.exe') compile --dir "$scriptDir\src\res" -o "$build\res.zip"
if ($LASTEXITCODE) { throw 'aapt2 compile failed' }

Write-Host 'aapt2 link'
& (Join-Path $bt 'aapt2.exe') link -o "$build\base.apk" -I $jar `
  --manifest "$scriptDir\src\AndroidManifest.xml" `
  -A "$scriptDir\src\assets" `
  --java "$build\gen" `
  --min-sdk-version 29 --target-sdk-version 34 `
  --version-code 1 --version-name '1.0' `
  "$build\res.zip"
if ($LASTEXITCODE) { throw 'aapt2 link failed' }

Write-Host 'javac'
$srcs = @(Get-ChildItem "$scriptDir\src\java" -Recurse -Filter *.java | ForEach-Object { $_.FullName })
$srcs += "$build\gen\com\grannyhome\launcher\R.java"
& (Join-Path $jdkDir.FullName 'bin\javac.exe') -encoding UTF-8 -source 8 -target 8 `
  -bootclasspath $jar -classpath $jar -d "$build\classes" @srcs
if ($LASTEXITCODE) { throw 'javac failed' }

Write-Host 'd8'
$cls = @(Get-ChildItem "$build\classes" -Recurse -Filter *.class | ForEach-Object { $_.FullName })
& (Join-Path $bt 'd8.bat') --release --min-api 29 --lib $jar --output "$build\dex" $cls
if ($LASTEXITCODE) { throw 'd8 failed' }

Write-Host 'packaging dex into apk'
& (Join-Path $jdkDir.FullName 'bin\jar.exe') -uf "$build\base.apk" -C "$build\dex" classes.dex
if ($LASTEXITCODE) { throw 'jar update failed' }

& (Join-Path $bt 'zipalign.exe') -f 4 "$build\base.apk" "$build\aligned.apk"
if ($LASTEXITCODE) { throw 'zipalign failed' }

$ksPath = Join-Path $scriptDir 'keys\granny.keystore'
New-Item -ItemType Directory -Force -Path (Split-Path $ksPath) | Out-Null
if (-not (Test-Path $ksPath)) {
  Write-Host 'creating signing key'
  & (Join-Path $jdkDir.FullName 'bin\keytool.exe') -genkeypair -keystore $ksPath -alias granny `
    -keyalg RSA -keysize 2048 -validity 36500 `
    -storepass REDACTED -keypass REDACTED `
    -dname 'CN=Home,OU=Granny,O=Chandra,C=IN'
  if ($LASTEXITCODE) { throw 'keytool failed' }
}

Write-Host 'apksigner'
& (Join-Path $bt 'apksigner.bat') sign --ks $ksPath --ks-key-alias granny `
  --ks-pass pass:REDACTED --key-pass pass:REDACTED `
  --out "$scriptDir\dist\Home.apk" "$build\aligned.apk"
if ($LASTEXITCODE) { throw 'apksigner failed' }

Write-Host ("APK ready: " + (Join-Path $scriptDir 'dist\Home.apk'))

if ($Install) {
  Write-Host 'adb install -r'
  adb install -r "$scriptDir\dist\Home.apk"
  if ($LASTEXITCODE) { throw 'adb install failed' }
}
if ($SetRole) {
  Write-Host 'setting default home role'
  adb shell cmd role add-role-holder android.app.role.HOME com.grannyhome.launcher
  adb shell cmd role holders android.app.role.HOME
}
