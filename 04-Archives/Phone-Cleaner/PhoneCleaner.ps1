# ============================================================================
#  Phone Cleaner for Moto G35 (grandfather-proof)
#  - Lists user-installed apps + system preloads in a checkbox UI
#  - Junk auto-ticked, important apps protected (grayed, unremovable)
#  - Reversible removal (user-0 uninstall) + Restore tab backed by a log file
#  Needs: adb (auto-found), one phone connected with USB debugging allowed.
# ============================================================================

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {

Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase
Add-Type -AssemblyName System.Xaml

# ---------------------------------------------------------------- adb locate
$script:adb = $null
$adbCandidates = @(
  (Get-Command adb -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { $_.Source }),
  "$env:LOCALAPPDATA\Android\platform-tools\adb.exe",
  "$env:ProgramFiles\Android\platform-tools\adb.exe",
  "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe",
  "C:\Android\platform-tools\adb.exe"
)
foreach ($c in $adbCandidates) { if ($c -and (Test-Path $c)) { $script:adb = $c; break } }

# ---------------------------------------------------------------- app labels
$script:labels = @{
 'com.whatsapp'='WhatsApp'; 'com.truecaller'='Truecaller'; 'com.kotak.neo'='Kotak Neo'
 'com.flipkart.android'='Flipkart'; 'in.amazon.mShop.android.shopping'='Amazon Shopping'
 'app.blinkit.onboarding'='Blinkit'; 'com.bigbasket.mobileapp'='BigBasket'
 'app.mycountrydelight.in.countrydelight'='Country Delight'; 'com.paypal.android.p2pmobile'='PayPal'
 'com.google.android.apps.nbu.paisa.user'='Google Pay'; 'com.google.android.apps.walletnfcrel'='Google Wallet'
 'com.acko.android'='Acko Insurance'
 'com.google.android.safetycore'='Google Safety Core'; 'com.google.android.verifier'='Google App Verifier'
 'com.google.android.contactkeys'='Google Contact Keys'
 'com.openai.chatgpt'='ChatGPT'; 'com.anthropic.claude'='Claude'; 'com.google.android.apps.bard'='Gemini'
 'com.facebook.katana'='Facebook'; 'com.facebook.orca'='Facebook Messenger'; 'com.facebook.stella'='Meta App'
 'com.pinterest'='Pinterest'; 'com.fitbit.FitbitMobile'='Fitbit'; 'com.apple.android.music'='Apple Music'
 'com.booking'='Booking.com'; 'com.cleartrip.android'='Cleartrip'; 'in.redbus.android'='redBus'
 'com.nnacres.app'='99Acres'; 'com.nobroker.app'='NoBroker'; 'com.liscious'='Licious'
 'com.amazon.mp3'='Amazon Music'; 'com.amazon.avod.thirdpartyclient'='Amazon Prime Video'
 'in.startv.hotstar'='JioHotstar'; 'com.sonyliv'='SonyLIV'
 'com.google.android.apps.chromecast.app'='Google Home'; 'com.google.android.apps.books'='Google Play Books'
 'in.AajTak.headlines'='Aaj Tak'; 'com.org.AmarUjala.news'='Amar Ujala'; 'com.hindustan.hindinews'='Hindustan News'
 'com.ak.ta.dainikbhaskar.activity'='Dainik Bhaskar'; 'com.jagran.english.twa'='Dainik Jagran English'
 'com.toi.reader.activities'='Times of India'; 'com.july.ndtv'='NDTV'; 'com.kagi.news'='Kagi News'
 'bible.offline.kingjames.holy.kjv.bible.daily.verse'='Bible App'; 'com.daily.dharma'='Daily Dharma'
 'islamic.habit.tracker.app'='Islamic Habit Tracker'; 'com.moovetechhk.athan'='Athan Prayers'
 'english.hindi.translator.translate.translation'='English-Hindi Translator'
 'com.radiofmapp.radioindia'='Radio India'; 'com.streema.simpleradio'='Simple Radio'
 'fmradio.radiostation.livefm.musicradio'='FM Radio'; 'com.liveradio.fmradio.radiotuner.radiostation.amradio'='Live FM Radio'
 'com.appmind.radios.in'='Radios In'; 'com.appgeneration.itunerfree'='Radio FM Tuner'
 'com.last.fm.live.radio.stations'='LastFM Live Radio'; 'com.muso.musicplayer'='Muso Music Player'
 'mymusic.offlinemusicplayer.mp3player.playmusic'='Offline MP3 Player'; 'com.rocks.music.videoplayer'='Music Video Player'
 'in.mysoundbox.app'='MySoundBox'; 'com.korrisoft.voice.recorder'='Voice Recorder'
 'com.starmakerinteractive.starmaker'='StarMaker'; 'com.sgiggle.production.lite'='Tango Lite'
 'com.headfone.www.headfone'='Headfone'
 'com.app.uengage.bikanervala'='Bikanervala'; 'com.biryaniblues.app'='Biryani Blues'
 'com.prideofcows.customer'='Pride of Cows'; 'com.apnirasoi.customer.android'='Apni Rasoi'
 'com.mds.medanta'='Medanta'; 'com.digi.dost'='Digi Dost'; 'in.platinumrx'='PlatinumRx'
 'com.aranoah.healthkart.plus'='1mg'; 'com.gsm.customer'='GSM Customer'
 'com.weclear.junk.cache'='WeClear Junk Cleaner'; 'com.clean.mix.junk'='Mix Junk Cleaner'
 'com.anante.funny.app.fastcleaner'='Fast Cleaner'; 'com.againstvirus.flux'='AntiVirus Flux'
 'com.adoclean.aa'='ADO Clean'; 'com.thebes.phonecleaner'='Phone Cleaner (Thebes)'
 'com.aicleaner.clean.cleanstorage.ai'='AI Storage Cleaner'; 'com.phcleanpro.cleaner'='Phone Cleaner Pro'
 'com.phone.cleaner.junk.llx'='Phone Cleaner LLX'; 'com.cleanmaster.memorycleaner'='Clean Master'
 'com.filebox.junkclean.filemanager'='FileBox Junk Clean'; 'com.flare.cleaner.storage'='Flare Cleaner'
 'com.mate.cleaner.cache.files.lab.tool'='Cache Cleaner Lab'; 'com.coarcnr.quickcln'='Quick Clean'
 'com.storage.cleaner.markcon'='Storage Cleaner Markcon'; 'com.phone.cleanhub'='CleanHub'
 'com.clean.ai.junk.keepclean'='KeepClean'
 'com.skytek.animals.ringtone'='Animal Ringtone'; 'com.romantic.love.stickers.whatsapp.wasticker'='WA Love Stickers'
 'com.gcl.animalringtone.aiwallpapers.airingtones.aimaker'='AI Ringtone/Wallpapers'
 'com.hsrapps.shubhwallpaperlive'='Shubh Live Wallpaper'; 'com.digital.analog.antique.clockwally'='Clock Wallpaper'
 'com.bestringtonesapps.birdcallssoundsandringtones'='Bird Calls Ringtones'
 'com.spinwheel.quendravikslotszoon'='Slots Casino'; 'com.Version1'='Version1 (suspicious)'
 'com.ubowskihataxnrl.wifianalyzer'='WiFi Analyzer'; 'com.nexttech009.quickwifiguard'='Quick WiFi Guard'
 'com.atefekasem.wifimanager'='WiFi Manager'; 'com.instabridge.free.internet'='Instabridge WiFi'
 'com.ertunga.wifihotspot'='WiFi Hotspot'; 'com.wifi.speed.test.signal.map'='WiFi Speed Test'
 'com.wifimanager.onehub'='WiFi Manager OneHub'
 'com.videodownloader.home.mp4.vidmasti.downloader8'='VidMasti Downloader'; 'sovixa.video.downloader'='Sovixa Downloader'
 'com.private.downloader.play.video'='Private Video Downloader'; 'com.allmedia.video.saver.eiakab.app'='Video Saver'
 'com.hub.browser.video.downloader.saver.vitmate'='VitMate Browser'; 'com.all.video.hd.privacy.player'='Video Player All'
 'oops.simplecompass'='Simple Compass'; 'com.compass.digital.direction.directionfinder'='Compass DirectionFinder'
 'com.compass.digital.direction.directionfinder.pro'='Compass DirectionFinder Pro'; 'pl.netigen.compass'='Netigen Compass'
 'tools.compass.bubblelevel'='Bubble Level'
 'com.recover.file.photo.quick'='Quick Photo Recovery'; 'com.filerecover.pro'='File Recover Pro'
 'com.files.photo.recovery.restore.pro'='Photo Recovery Restore Pro'; 'com.datarecoverypro.photo.recoverplus'='Photo Recover Plus'
 'com.reco.pho.vid'='Photo/Vid Recovery'
 'com.nexora.labs.findmyphone.v1'='Find My Phone (Nexora)'; 'com.nexora.labs.bpcare'='Nexora bpCare'
 'com.binaryscript.payalert'='PayAlert'; 'com.gfpls.personalloan'='Personal Loan'
 'com.allbankbalance.accountenquiry.passbookloan'='AllBank Balance (scam)'
 'com.step.pedometer.counter.walking.tracker'='Step Counter'; 'stepcounter.pedometer.stepstracker'='Pedometer Steps'
 'com.healthtracker.bloodsugar.bloodpressure.monitor.diabetes.report'='BP/Diabetes Tracker'
 'com.healthlab.heartrate.bloodpressuretracker'='Heart Rate/BP Tracker'; 'com.nieruo.healthapp'='Health App'
 'com.contacts.dialer.caller.dialpad.android'='Caller Dialpad (fake dialer)'; 'com.contacts.nest.app'='Contacts Nest (fake dialer)'
 'callid.name.announcer'='CallID Name Announcer'; 'com.contacts.phone.allcontacts.viewcontacts'='AllContacts Viewer (fake dialer)'
 'com.contactsfree.idailerapp'='ContactsFree iDialer (fake)'; 'com.dialer.contacts.phonebook'='Dialer Phonebook (fake)'
 'com.Phone_Call_Dialer'='Phone Call Dialer (fake)'; 'com.cov.re.phone'='CovRe Phone (fake)'
 'pdfscanner.scan.pdf.scanner.free'='PDF Scanner'; 'com.t9t.alldocreader'='All Doc Reader'
 'lpdf.yreader.fmanager'='LPDF File Manager'; 'com.alldocumentfilehub.tools'='All Document Hub'
 'com.aura.scan.pdf.editor.reader.office'='PDF Editor Office'; 'com.excel.spreadsheet.reader'='Excel Reader'
 'com.getmyspeakeasy.app'='SpeakEasy'; 'com.shuru.nearme'='NearMe Shuru'; 'com.newreading.goodreels'='GoodReels'
 'com.master.learn.ai'='Learn AI'; 'com.cleonan.cpho'='CPHO'; 'app.v1bl3y'='v1bl3y (suspicious)'
 'com.szzisodeb.kzoneir'='KZone'; 'com.trevel'='Trevel (suspicious)'; 'com.app.alright'='App Alright'
 'com.hyper.office.useful'='Hyper Office'; 'com.kemnakersipkk.deviceexplorer'='Device Explorer'
 'com.duoluomao.clock.simplealarm'='Simple Alarm Clock'; 'com.atmapk.storageaid'='StorageAid'
 'com.stepora.clean.fix'='Clean Fix'; 'com.alfacln.jkclnr'='JK Cleaner'; 'com.cp.clean'='CP Clean'
 'com.cw.clean'='CW Clean'; 'com.blower.speaker.water.cleaner'='Speaker Water Clean'
 'com.dubox.drive'='DuBox Drive'; 'com.netshort.abroad'='VPN Abroad'; 'com.billu.care'='Billu Care'
 'com.potradeweb.aitrading'='AI Trading'; 'com.alertbox.app'='AlertBox'
 'com.freshterramobile'='FreshTerra'; 'com.clipwhite.onebrowsing'='One Browsing (adware)'
 'com.priva.private.web.browser.incognito'='Private Browser (adware)'; 'com.safeweb.browser'='SafeWeb Browser (adware)'
 'com.ask.browser.ai'='Ask AI Browser (adware)'; 'com.browser.safeclean'='SafeClean Browser (adware)'
 'story.tv.drama.reels'='Drama Reels TV'; 'in.reelsaga.android'='ReelSaga'; 'com.storymatrix.drama'='Drama Story'
 'com.weather.Weather'='Weather'; 'com.gpsmapcamera.geotagginglocationonphoto'='GPS Map Camera'
 'com.tatadigital.qmin'='Tata Digital'
 'org.chromium.webapk.a72c742f7e513b73f_v2'='Web App (PWA)'
 'com.ubon'=''; 'com.ubonx'=''; 'com.bestiantes'=''; 'com.ubonq'=''; 'potsdala'=''
}

# ------------------------------------------------------- categories & safety
# Hard-protected: still listed, but checkbox disabled (can never be removed).
$script:protectedPkgs = @('com.whatsapp','com.truecaller','com.grannyhome.launcher',
 'in.amazon.mShop.android.shopping','com.flipkart.android','app.blinkit.onboarding',
 'com.bigbasket.mobileapp','app.mycountrydelight.in.countrydelight',
 'com.paypal.android.p2pmobile','com.google.android.apps.nbu.paisa.user',
 'com.google.android.apps.walletnfcrel','com.Version1','com.csam.icici.bank.imobile',
 'com.google.android.safetycore','com.google.android.verifier','com.google.android.contactkeys')

# Junk detection: pattern hits on package name.
$script:junkPatterns = @(
 'clean|junk|booster|optimiz|antivirus|againstvirus',
 'rington|wallpaper',
 'wifianalyzer|wifimanager|wifiguard|wifihotspot|wifispeed|wifi\.speed|instabridge',
 'downloader|vidmasti|video\.saver|videosaver|tubemate',
 'recover|recovery',
 'compass|bubblelevel',
 'loan|payalert|trading|slots|casino|spinwheel',
 'pedometer|stepcounter|heartrate|bloodpressure|diabetes|healthtracker|healthapp|bpcare|findmyphone',
 'dialpad|idialer|phonecall_dialer|Phone_Call_Dialer|announcer|phonebook|viewcontacts|contacts\.nest|contacts\.dialer|contactsfree|dialer\.contacts|\.cov\.re\.phone',
 'drama|reels|reelsaga|goodreels|video\.hd\.privacy',
 'webapk'
)
# Manually flagged junk (exact package names).
$script:junkManual = @(
 'com.weclear.junk.cache','com.clean.mix.junk','com.anante.funny.app.fastcleaner',
 'com.againstvirus.flux','com.adoclean.aa','com.thebes.phonecleaner',
 'com.aicleaner.clean.cleanstorage.ai','com.phcleanpro.cleaner','com.phone.cleaner.junk.llx',
 'com.cleanmaster.memorycleaner','com.filebox.junkclean.filemanager','com.flare.cleaner.storage',
 'com.mate.cleaner.cache.files.lab.tool','com.coarcnr.quickcln','com.storage.cleaner.markcon',
 'com.phone.cleanhub','com.clean.ai.junk.keepclean','com.atmapk.storageaid','com.stepora.clean.fix',
 'com.alfacln.jkclnr','com.cp.clean','com.cw.clean','com.blower.speaker.water.cleaner',
 'com.Version1','app.v1bl3y','com.trevel','com.szzisodeb.kzoneir','com.cleonan.cpho',
 'com.master.learn.ai','com.newreading.goodreels','com.getmyspeakeasy.app','com.shuru.nearme',
 'com.hyper.office.useful','com.kemnakersipkk.deviceexplorer','com.duoluomao.clock.simplealarm',
 'com.romantic.love.stickers.whatsapp.wasticker','com.hsrapps.shubhwallpaperlive',
 'com.digital.analog.antique.clockwally','com.billu.care','com.dubox.drive',
 'com.netshort.abroad','com.clipwhite.onebrowsing','com.priva.private.web.browser.incognito',
 'com.safeweb.browser','com.ask.browser.ai','com.browser.safeclean',
 'com.excel.spreadsheet.reader','com.t9t.alldocreader','lpdf.yreader.fmanager',
 'com.alldocumentfilehub.tools','com.aura.scan.pdf.editor.reader.office','pdfscanner.scan.pdf.scanner.free',
 'com.ironsource.appcloud.oobe','com.gsm.customer','com.kotak.neo','com.acko.android'
)
# Never treat as junk (religious/daily-use apps that match junk patterns).
$script:notJunk = @('com.moovetechhk.athan',
 'bible.offline.kingjames.holy.kjv.bible.daily.verse',
 'com.daily.dharma','islamic.habit.tracker.app')

# Extra pre-ticks per user request (radio + Hindi news are removable).
$script:tickManual = @(
 'com.radiofmapp.radioindia','com.streema.simpleradio','fmradio.radiostation.livefm.musicradio',
 'com.liveradio.fmradio.radiotuner.radiostation.amradio','com.appmind.radios.in',
 'com.appgeneration.itunerfree','com.last.fm.live.radio.stations',
 'in.AajTak.headlines','com.org.AmarUjala.news','com.hindustan.hindinews',
 'com.ak.ta.dainikbhaskar.activity','com.jagran.english.twa'
)

# System-list junk (curated matches, shown pre-ticked in tab 2).
$script:systemJunkPatterns = @(
 '^com\.facebook\.(appmanager|services|system)',
 '^com\.amazon\.(appmanager|marketingtool|meridian)',
 '^com\.netflix\.',
 '^com\.motorola\.(fmradio|motocitizens)',
 '^co\.sitic\.pp', '^com\.payjoy\.access',
 '^com\.inmobi\.(installer|weather)', '^com\.indus\.appstore',
 '^com\.glance\.', '^com\.taboola\.ody',
 '^com\.handmark\.expressweather',
 '^com\.altice\.android\.myapps', '^com\.telcel\.contenedor',
 '^com\.sfr\.android\.sfrjeux', '^com\.orange\.update',
 '^com\.ironsource\.appcloud'
)

# Advanced system view: keep essentials/vendor cores out of the checklist.
$script:systemHiddenPatterns = @(
 '^android$','^android\.','^com\.android\.','^com\.google\.','^com\.motorola\.','^com\.mediatek\.'
,'^com\.qualcomm\.','^com\.dts\.','^com\.unisoc','^com\.sprd\.','^com\.spreadtrum'
,'^com\.ontim','^com\.dolby','^com\.lenovo','^de\.telekom','\.overlay','^com\.dti\.'
,'^com\.aura\.oobe','^com\.orange\.aura'
)

$script:catColors = @{ Junk='#e53935'; Other='#7f8c8d'; Protected='#2e7d32'; System='#6d4c41'; Restore='#2e7d32' }
$script:rowColors = @{ Junk='#fff3f3'; Other='#ffffff'; Protected='#eef4ee'; System='#fffaf1'; Restore='#e8f5e9' }

# ------------------------------------------------------------------ logging
$script:logFile = Join-Path $scriptDir 'removed-apps.json'

function Load-LogHistory {
  if (Test-Path $script:logFile) {
    try { return @(Get-Content $script:logFile -Raw -Encoding UTF8 | ConvertFrom-Json) } catch { return @() }
  }
  return @()
}
function Save-LogHistory($items) {
  # OneDrive can hold a read lock on the file; retry a few times.
  for ($t = 0; $t -lt 4; $t++) {
    try {
      $items | ConvertTo-Json -Depth 3 | Set-Content -Path $script:logFile -Encoding UTF8 -Force
      return
    } catch { Start-Sleep -Milliseconds 250 }
  }
  try {
    $fb = Join-Path $env:TEMP 'removed-apps.json'
    $items | ConvertTo-Json -Depth 3 | Set-Content -Path $fb -Encoding UTF8 -Force
  } catch { }
}

# -------------------------------------------------------------- device state
function Get-DeviceState {
  if (-not $script:adb) { return 'noadb' }
  $lines = & $script:adb devices | Select-Object -Skip 1 | Where-Object { $_ -match '\S' }
  $serials = @()
  $unauth = 0
  foreach ($l in $lines) {
    $parts = ($l -split '\s+') | Where-Object { $_ }
    if ($parts.Count -lt 2) { continue }
    if ($parts[1] -eq 'device') { $serials += $parts[0] }
    elseif ($parts[1] -eq 'unauthorized') { $unauth++ }
  }
  if ($serials.Count -gt 0) { return 'device' }
  if ($unauth -gt 0) { return 'unauthorized' }
  return 'none'
}

function Get-DeviceModel {
  try { return ((& $script:adb shell getprop ro.product.model) | Out-String).Trim() } catch { return 'Android device' }
}

# ---------------------------------------------------------------- UI helpers
$script:brushConv = New-Object System.Windows.Media.BrushConverter
function New-Brush([string]$hex) { return $script:brushConv.ConvertFromString($hex) }
$script:devGood = New-Brush '#2e7d32'
$script:devBad  = New-Brush '#e06c75'
$script:warnCol = New-Brush '#e65100'

function Update-Status([string]$msg, $color = $null) {
  if (-not $color) { $color = $script:statusBrush } else { $script:statusBrush = $color }
  $script:statusTB.Text = $msg
  $script:statusTB.Foreground = $color
}
function Pulse([string]$msg) {
  if ($script:statusTB) { $script:statusTB.Text = $msg }
  [System.Windows.Threading.Dispatcher]::CurrentDispatcher.Invoke([action]{}, [System.Windows.Threading.DispatcherPriority]::Background) | Out-Null
}

function Assert-DeviceReady {
  $st = Get-DeviceState
  if ($st -eq 'noadb') {
    Update-Status 'adb not found. Install Android platform-tools first.' $script:devBad; return $false
  }
  if ($st -eq 'none') {
    Update-Status 'no phone detected. plug in USB with USB debugging on.' $script:devBad; return $false
  }
  if ($st -eq 'unauthorized') {
    Update-Status 'unauthorized. unlock the phone and tap Allow on the USB debugging prompt.' $script:devBad; return $false
  }
  Update-Status ("device ready: " + (Get-DeviceModel)) $script:devGood
  return $true
}

# ---------------------------------------------------------- package fetching
function Get-ShellList([string]$cmd) {
  (& $script:adb shell $cmd) | ForEach-Object { ($_ -replace '^package:','').Trim() } | Where-Object { $_ }
}
function Get-UserPackages    { Get-ShellList 'pm list packages -3'  ; }
function Get-SystemPackages  { Get-ShellList 'pm list packages -s'  ; }
function Get-AllPackages {
  $all = Get-ShellList 'pm list packages'
  return ,$all
}
function Get-Installers {
  $map = @{}
  (& $script:adb shell 'pm list packages -3 -i') | ForEach-Object {
    $l = $_.Trim()
    if ($l -match '^package:(\S+)\s+installer=(\S+)') { $map[$Matches[1]] = $Matches[2] }
  }
  return $map
}

function Get-PackageName([string]$pkg) {
  if ($script:labels.ContainsKey($pkg) -and $script:labels[$pkg]) { return $script:labels[$pkg] }
  return $pkg
}
function Is-SystemJunk([string]$pkg) {
  foreach ($p in $script:systemJunkPatterns) { if ($pkg -match $p) { return $true } }
  return $false
}
function Get-Category([string]$pkg) {
  if ($script:protectedPkgs -contains $pkg) { return 'Protected' }
  if ($script:notJunk -contains $pkg) { return 'Other' }
  if ($script:junkManual -contains $pkg) { return 'Junk' }
  foreach ($p in $script:junkPatterns) { if ($pkg -match $p) { return 'Junk' } }
  return 'Other'
}

function Build-Model([string]$pkg, [string]$group) {
  $cat = 'Other'
  $rank = 2
  $ticked = $false
  if ($group -eq 'User') {
    $cat = Get-Category $pkg
    if ($script:tickManual -contains $pkg) { $ticked = $true }
    if ($cat -eq 'Protected') { $rank = 0 }
    elseif ($cat -eq 'Junk')   { $rank = 1; $ticked = $true }
  } else {
    $cat = 'System'
    if (Is-SystemJunk $pkg) { $rank = 1; $ticked = $true } else { $rank = 2 }
  }
  $isProt = ($script:protectedPkgs -contains $pkg)
  if ($isProt) { $ticked = $false }
  $name = Get-PackageName $pkg
  return [pscustomobject]@{
    Pkg      = $pkg
    Name     = $name
    Name2    = "$name   ($pkg)"
    Cat      = $cat
    Group    = $group
    Del      = $ticked
    CanDel   = (-not $isProt)
    RowBg    = $script:rowColors[$cat]
    CatColor = $script:catColors[$cat]
    Rank     = $rank
  }
}

# ------------------------------------------------------------------- UI XAML
[xml]$script:xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Moto Phone Cleaner"
        Height="840" Width="1040"
        WindowStartupLocation="CenterScreen"
        Background="#f5f2ee"
        FontFamily="Segoe UI">
  <Grid Margin="14">
    <Grid.RowDefinitions>
      <RowDefinition Height="Auto"/>
      <RowDefinition Height="Auto"/>
      <RowDefinition Height="*"/>
      <RowDefinition Height="Auto"/>
    </Grid.RowDefinitions>

    <Border Grid.Row="0" Background="#ffffff" CornerRadius="8" Padding="12" Margin="0,0,0,8" BorderBrush="#e6e2dc" BorderThickness="1">
      <DockPanel LastChildFill="False">
        <Ellipse x:Name="dot" Width="12" Height="12" Fill="#e06c75" VerticalAlignment="Center" Margin="0,0,10,0"/>
        <TextBlock x:Name="devStatus" Text="checking device..." VerticalAlignment="Center" FontSize="14.5" Foreground="#2c2c2c"/>
        <Button x:Name="btnRefresh" Content="Refresh from phone" Width="180" Height="36"
                DockPanel.Dock="Right" Background="#ffffff" BorderBrush="#c9c4bd" BorderThickness="1"/>
      </DockPanel>
    </Border>

    <TextBlock Grid.Row="1" Text="Junk is pre-ticked. Review the list, untick anything doubtful, then Uninstall. Everything removed can be restored from tab 3."
               FontSize="12.5" Foreground="#777" Margin="4,0,0,6"/>

    <TabControl Grid.Row="2" Background="Transparent" BorderThickness="0">

      <TabItem Header="1 | User apps">
        <Grid Margin="10">
          <Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition Height="*"/></Grid.RowDefinitions>
          <DockPanel LastChildFill="False">
            <Button x:Name="btnSelJunk" Content="Tick all junk" Width="140" Height="34"/>
            <Button x:Name="btnClearUser" Content="Clear ticks" Width="110" Height="34" Margin="6,0,0,0"/>
            <TextBox x:Name="userFilter" Width="240" Height="34" Margin="20,0,0,0"
                     VerticalContentAlignment="Center" FontSize="13"/>
            <Button x:Name="btnUninstallUser" Content="Uninstall (0)" Width="180" Height="40"
                    DockPanel.Dock="Right" Background="#e53935" Foreground="White" FontWeight="Bold"/>
          </DockPanel>
          <ScrollViewer Grid.Row="1" Margin="0,8,0,0" VerticalScrollBarVisibility="Auto">
            <ItemsControl x:Name="userList"/>
          </ScrollViewer>
        </Grid>
      </TabItem>

      <TabItem Header="2 | System preloads">
        <Grid Margin="10">
          <Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition Height="Auto"/><RowDefinition Height="*"/></Grid.RowDefinitions>
          <DockPanel LastChildFill="False">
            <Button x:Name="btnSysAll" Content="Tick all shown" Width="140" Height="34"/>
            <Button x:Name="btnClearSys" Content="Clear ticks" Width="110" Height="34" Margin="6,0,0,0"/>
            <CheckBox x:Name="sysAdvanced" Content="advanced: show full android system list (risky)"
                      Margin="26,0,0,0" VerticalAlignment="Center" FontSize="12.5"/>
            <Button x:Name="btnUninstallSys" Content="Uninstall (0)" Width="180" Height="40"
                    DockPanel.Dock="Right" Background="#e53935" Foreground="White" FontWeight="Bold"/>
          </DockPanel>
          <TextBlock Grid.Row="1" x:Name="sysNote" Margin="2,6,0,0" FontSize="12" TextWrapping="Wrap"
                     Foreground="#666" Text="Loading..."/>
          <ScrollViewer Grid.Row="2" Margin="0,8,0,0" VerticalScrollBarVisibility="Auto">
            <ItemsControl x:Name="sysList"/>
          </ScrollViewer>
        </Grid>
      </TabItem>

      <TabItem Header="3 | Restore">
        <Grid Margin="10">
          <Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition Height="Auto"/><RowDefinition Height="*"/></Grid.RowDefinitions>
          <DockPanel LastChildFill="False">
            <Button x:Name="btnRestRefresh" Content="Refresh list" Width="140" Height="34"/>
            <Button x:Name="btnReinstall" Content="Reinstall selected" Width="190" Height="40"
                    DockPanel.Dock="Right" Background="#2e7d32" Foreground="White" FontWeight="Bold"/>
          </DockPanel>
          <TextBlock Grid.Row="1" x:Name="restNote" Margin="2,6,0,0" FontSize="12" TextWrapping="Wrap"
                     Foreground="#666" Text="Loading..."/>
          <ScrollViewer Grid.Row="2" Margin="0,8,0,0" VerticalScrollBarVisibility="Auto">
            <ItemsControl x:Name="restList"/>
          </ScrollViewer>
        </Grid>
      </TabItem>
    </TabControl>

    <Border Grid.Row="3" Background="#ffffff" CornerRadius="8" Padding="10" Margin="0,8,0,0"
            BorderBrush="#e6e2dc" BorderThickness="1">
      <TextBlock x:Name="statusTB" Text="" FontSize="13"/>
    </Border>
  </Grid>
</Window>
"@

function Build-RowTemplate {
  $xml = @"
<DataTemplate xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
  <Border Background="{Binding RowBg}" CornerRadius="4" Margin="0,1" Padding="8,5">
    <DockPanel LastChildFill="False">
      <CheckBox DockPanel.Dock="Left" VerticalAlignment="Center"
                IsChecked="{Binding Del, Mode=TwoWay}" IsEnabled="{Binding CanDel}"/>
      <TextBlock DockPanel.Dock="Left" Text="{Binding Name2}" FontSize="13.5" Margin="10,0,0,0"/>
      <TextBlock DockPanel.Dock="Right" HorizontalAlignment="Right"
                 Text="{Binding Cat}" FontSize="11.5" Foreground="{Binding CatColor}"/>
    </DockPanel>
  </Border>
</DataTemplate>
"@
  $rdr = New-Object System.Xml.XmlNodeReader ([xml]$xml)
  return [Windows.Markup.XamlReader]::Load($rdr)
}

$reader = New-Object System.Xml.XmlNodeReader $script:xaml
$window = [Windows.Markup.XamlReader]::Load($reader)

$dot              = $window.FindName('dot')
$devStatus        = $window.FindName('devStatus')
$btnRefresh       = $window.FindName('btnRefresh')
$userList         = $window.FindName('userList')
$userFilter       = $window.FindName('userFilter')
$btnSelJunk       = $window.FindName('btnSelJunk')
$btnClearUser     = $window.FindName('btnClearUser')
$btnUninstallUser = $window.FindName('btnUninstallUser')
$sysList          = $window.FindName('sysList')
$btnSysAll        = $window.FindName('btnSysAll')
$btnClearSys      = $window.FindName('btnClearSys')
$sysAdvanced      = $window.FindName('sysAdvanced')
$sysNote          = $window.FindName('sysNote')
$btnUninstallSys  = $window.FindName('btnUninstallSys')
$restList         = $window.FindName('restList')
$restNote         = $window.FindName('restNote')
$btnRestRefresh   = $window.FindName('btnRestRefresh')
$btnReinstall     = $window.FindName('btnReinstall')
$script:statusTB  = $window.FindName('statusTB')

$template = Build-RowTemplate
$userList.ItemTemplate = $template
$sysList.ItemTemplate  = $template
$restList.ItemTemplate = $template

$script:userModels   = New-Object System.Collections.Generic.List[object]
$script:systemModels = New-Object System.Collections.Generic.List[object]
$script:restModels   = New-Object System.Collections.Generic.List[object]

# ---------------------------------------------------------- view refresh fns
function Update-FilteredLists {
  $f = $userFilter.Text.Trim()
  $matched = New-Object System.Collections.Generic.List[object]
  if ($f) {
    $pat = [regex]::Escape($f)
    foreach ($m in $script:userModels) { if ($m.Name2 -match $pat) { $matched.Add($m) } }
  } else {
    foreach ($m in $script:userModels) { $matched.Add($m) }
  }
  $userList.ItemsSource = $matched
}

function Update-Counts {
  $n = @($script:userModels | Where-Object { $_.Del -and $_.CanDel }).Count
  $btnUninstallUser.Content = "Uninstall ($n)"
  $m = @($script:systemModels | Where-Object { $_.Del -and $_.CanDel }).Count
  $btnUninstallSys.Content = "Uninstall ($m)"
}

function Update-DevBanner {
  $st = Get-DeviceState
  switch ($st) {
    'noadb'        { $devStatus.Text = 'adb not found (install Android platform-tools).'; $dot.Fill = $script:devBad }
    'none'         { $devStatus.Text = 'no phone connected. plug in USB and keep USB debugging on.'; $dot.Fill = $script:devBad }
    'unauthorized' { $devStatus.Text = 'unauthorized. unlock the phone and tap Allow on the USB prompt.'; $dot.Fill = $script:devBad }
    default        { $devStatus.Text = 'connected: ' + (Get-DeviceModel); $dot.Fill = $script:devGood }
  }
}

function Refresh-UserTab {
  if (-not (Assert-DeviceReady)) { return }
  # keep the user's manual tick/untick decisions across refreshes
  $prevTicks = @{}
  foreach ($pm in $script:userModels) { $prevTicks[$pm.Pkg] = $pm.Del }
  Pulse 'reading all installed apps from the phone...'
  $list = New-Object System.Collections.Generic.List[object]
  foreach ($pkg in (Get-UserPackages)) {
    $bm = Build-Model $pkg 'User'
    if ($prevTicks.ContainsKey($pkg) -and ($script:protectedPkgs -notcontains $pkg)) {
      $bm.Del = $prevTicks[$pkg]
    }
    $list.Add($bm)
  }
  $script:userModels = New-Object System.Collections.Generic.List[object]
  foreach ($m in ($list | Sort-Object Rank, Name)) { $script:userModels.Add($m) }
  Update-FilteredLists
  Update-Counts
  Update-DevBanner
  Update-Status ("user apps: " + $script:userModels.Count + " loaded. Your earlier ticks were kept.") $script:devGood
}

function Refresh-SystemTab {
  if (-not (Assert-DeviceReady)) { return }
  Pulse 'reading system preloads...'
  $list = New-Object System.Collections.Generic.List[object]
  foreach ($pkg in (Get-SystemPackages)) {
    if (Is-SystemJunk $pkg) { $list.Add((Build-Model $pkg 'System')); continue }
    if ($sysAdvanced.IsChecked) {
      $hidden = $false
      foreach ($h in $script:systemHiddenPatterns) { if ($pkg -match $h) { $hidden = $true; break } }
      if (-not $hidden) { $list.Add((Build-Model $pkg 'System')) }
    }
  }
  $script:systemModels = New-Object System.Collections.Generic.List[object]
  foreach ($m in ($list | Sort-Object Rank, Name)) { $script:systemModels.Add($m) }
  $sysList.ItemsSource = $script:systemModels
  Update-Counts
  $nCurated = @($script:systemModels | Where-Object { $_.Rank -eq 1 }).Count
  if (-not $sysAdvanced.IsChecked) {
    $sysNote.Text = "found $nCurated known junk preloads (pre-ticked). Turn on ANDROID advanced view for more: core android/google/motorola components are hidden. All removals here are reversible via Restore tab."
  } else {
    $sysNote.Text = "FULL system view. Everything below is vendor/android preinstalled. Untick anything doubtful. Removal keeps app data and is reversible."
  }
}

function Refresh-RestoreTab {
  if (-not (Assert-DeviceReady)) { return }
  Pulse 'checking removal history...'
  $script:restModels = New-Object System.Collections.Generic.List[object]
  $hist = Load-LogHistory
  $installedSet = @{}
  foreach ($p in (Get-AllPackages)) { $installedSet[$p] = $true }
  # newest first, one row per package
  $rows = @()
  $seen = @{}
  for ($i = $hist.Count - 1; $i -ge 0; $i--) {
    $h = $hist[$i]
    if (-not $h.pkg -or $seen.ContainsKey($h.pkg)) { continue }
    $seen[$h.pkg] = $true
    $rows += $h
  }
  foreach ($h in $rows) {
    $name = Get-PackageName $h.pkg
    $isInstalled = $installedSet.ContainsKey($h.pkg)
    $cat = if ($isInstalled) { 'Protected' } else { 'Restore' }
    $script:restModels.Add([pscustomobject]@{
      Pkg = $h.pkg
      Name = $name
      Name2 = "$name   ($h.pkg)"
      Cat = "$(if($isInstalled){'restored already'}else{'removed ' + $h.time})"
      Cat2 = if ($isInstalled) { 'restored already' } else { 'removed ' + $h.time }
      Del = $false
      CanDel = (-not $isInstalled)
      RowBg = $script:rowColors[$cat]
      CatColor = $script:catColors[$cat]
      Rank = 0
    })
  }
  $restList.ItemsSource = $script:restModels
  $n = $script:restModels.Count
  if ($n -eq 0) { $restNote.Text = "No removal history yet. Everything you uninstall appears here so it can be brought back." }
  else { $restNote.Text = "$n package(s) in history. Tick what to reinstall. If reinstall fails for a user app, it needs a one-time reinstall from Play Store." }
}

# ---------------------------------------------------------------- operation
function Add-LogEntry($model, $installer) {
  $hist = @(Load-LogHistory)
  $hist += [pscustomobject]@{
    pkg = $model.Pkg; name = $model.Name; cat = $model.Cat; group = $model.Group
    time = (Get-Date -Format 'yyyy-MM-dd HH:mm'); installer = "$installer"
  }
  Save-LogHistory $hist
}

function Uninstall-Package([string]$pkg, [bool]$isSystem) {
  # -k keeps data/cache where possible (extra reversibility), fallback plain.
  $cmd = "pm uninstall -k --user 0 $pkg"
  $out = ""
  try { $out = ((& $script:adb shell $cmd) | Out-String) } catch { }
  if ($out -notmatch 'Success') {
    $cmd = "pm uninstall --user 0 $pkg"
    try { $out = ((& $script:adb shell $cmd) | Out-String) } catch { }
  }
  return ($out -match 'Success')
}

function Uninstall-Kind([string]$kind) {
  if (-not (Assert-DeviceReady)) { return }
  if ($kind -eq 'User') { $models = $script:userModels } else { $models = $script:systemModels }
  $sel = @($models | Where-Object { $_.Del -and $_.CanDel })
  if ($sel.Count -eq 0) {
    Update-Status 'nothing is ticked.' $script:warnCol; return
  }
  $r = [Windows.MessageBox]::Show(
    "Remove $($sel.Count) app(s) from $("the phone")?`n`nRemoval is reversible: history stays in tab 3 (Restore).`nProceed?",
    'Confirm uninstall', [Windows.MessageBoxButton]::YesNo, [Windows.MessageBoxImage]::Warning)
  if ($r -ne [Windows.MessageBoxResult]::Yes) { return }

  $installers = Get-Installers
  $ok = 0
  $fail = @()
  $i = 0
  foreach ($m in $sel) {
    $i++
    Pulse ("removing " + $i + "/" + $sel.Count + ": " + $m.Name + " ...")
    if (Uninstall-Package $m.Pkg ($kind -eq 'System')) {
      $ok++
      $ins = ""
      if ($installers.ContainsKey($m.Pkg)) { $ins = $installers[$m.Pkg] }
      Add-LogEntry $m $ins
    } else {
      $fail += $m.Name
    }
  }
  $msg = "removed $ok of $($sel.Count)."
  if ($fail.Count -gt 0) { $msg += " failed: $($fail -join ', ')." }
  $col = if ($fail.Count -gt 0) { $script:warnCol } else { $script:devGood }
  Update-Status $msg $col
  if ($kind -eq 'User') { Refresh-UserTab } else { Refresh-SystemTab }
  Refresh-RestoreTab
}

function Reinstall-Selected {
  if (-not (Assert-DeviceReady)) { return }
  $sel = @($script:restModels | Where-Object { $_.Del -and $_.CanDel })
  if ($sel.Count -eq 0) { Update-Status 'nothing ticked to reinstall.' $script:warnCol; return }
  $ok = 0; $fail = @()
  $i = 0
  foreach ($m in $sel) {
    $i++
    Pulse ("reinstalling " + $i + "/" + $sel.Count + ": " + $m.Name + " ...")
    $out = ""
    try { $out = ((& $script:adb shell "cmd package install-existing $($m.Pkg)") | Out-String) } catch { }
    if ($out -notmatch 'Success') {
      try { $out = ((& $script:adb shell "pm install-existing --user 0 $($m.Pkg)") | Out-String) } catch { }
    }
    if ($out -match 'Success') { $ok++ } else { $fail += $m.Name }
  }
  $msg = "reinstalled $ok of $($sel.Count)."
  if ($fail.Count -gt 0) { $msg += " could not be restored here (reinstall from Play Store): $($fail -join ', ')." }
  Update-Status $msg $(if ($fail.Count -gt 0) { $script:warnCol } else { $script:devGood })
  Refresh-RestoreTab
}

# ------------------------------------------------------------------ wiring
$btnRefresh.Add_Click({
  Update-DevBanner
  if (Get-DeviceState -eq 'device') {
    Refresh-UserTab
    Refresh-SystemTab
    Refresh-RestoreTab
  } else {
    Assert-DeviceReady
  }
})
$btnSelJunk.Add_Click({
  foreach ($m in $script:userModels) {
    if ($m.Cat -eq 'Junk' -and $m.CanDel) { $m.Del = $true }
  }
  Update-FilteredLists
  Update-Counts
})
$btnClearUser.Add_Click({
  foreach ($m in $script:userModels) { if ($m.CanDel) { $m.Del = $false } }
  Update-FilteredLists
  Update-Counts
})
$btnUninstallUser.Add_Click({ Uninstall-Kind 'User' })
$btnSysAll.Add_Click({
  foreach ($m in $script:systemModels) { if ($m.CanDel) { $m.Del = $true } }
  Update-Counts
})
$btnClearSys.Add_Click({
  foreach ($m in $script:systemModels) { if ($m.CanDel) { $m.Del = $false } }
  Update-Counts
})
$btnUninstallSys.Add_Click({ Uninstall-Kind 'System' })
$sysAdvanced.Add_Click({
  Refresh-SystemTab
})
$btnRestRefresh.Add_Click({ Refresh-RestoreTab })
$btnReinstall.Add_Click({ Reinstall-Selected })
$userFilter.Add_TextChanged({ Update-FilteredLists })

$timer = New-Object System.Windows.Threading.DispatcherTimer
$timer.Interval = [TimeSpan]::FromMilliseconds(350)
$timer.Add_Tick({ Update-Counts })
$timer.Start()

# ------------------------------------------------------------------ startup
Update-DevBanner
if (Get-DeviceState -eq 'device') {
  Refresh-UserTab
  Refresh-SystemTab
  Refresh-RestoreTab
} else {
  Update-Status 'waiting for phone. plug in via USB (USB debugging on) and press Refresh.' $script:warnCol
}
[void]$window.ShowDialog()

} catch {
  $errPath = Join-Path $env:TEMP 'phonecleaner.err.txt'
  $_ | Out-File -FilePath $errPath -Append -Encoding UTF8
  try {
    [Windows.MessageBox]::Show("Error: $($_.Exception.Message)`n`nDetails saved to: $errPath",
      'Phone Cleaner', [Windows.MessageBoxButton]::OK, [Windows.MessageBoxImage]::Error) | Out-Null
  } catch { }
}
