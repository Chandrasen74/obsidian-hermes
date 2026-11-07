import os, json, csv
from datetime import datetime
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # user's own photos; some are >100 MP

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

PHOTO  = r"C:\Users\Kanchan Verma\OneDrive\Desktop\photography"
INDEX  = os.path.join(PHOTO, "photo-index.json")
THUMBS = os.path.join(PHOTO, "thumbs")
CONV   = os.path.join(PHOTO, "converted")
DESCS  = os.path.join(PHOTO, "descriptions.json")
LOG    = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline\undo-log-photography.csv"

idx = json.load(open(INDEX, encoding="utf-8"))
items = idx["items"]

# merge descriptions if present
if os.path.exists(DESCS):
    descs = json.load(open(DESCS, encoding="utf-8"))
    for it in items:
        d = descs.get(it["file"])
        if d:
            it["desc"] = d.get("desc")
            it["tags"] = d.get("tags", [])
            it["ocr"] = d.get("ocr", "")

os.makedirs(THUMBS, exist_ok=True)

def thumb_name(rel):
    return rel.replace("/", "__") + ".jpg"

print("Generating thumbnails...", flush=True)
made = 0
for it in items:
    t = os.path.join(THUMBS, thumb_name(it["file"]))
    if it["ext"] in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic"):
        if not os.path.exists(t):
            src = os.path.join(PHOTO, it["file"].replace("/", os.sep))
            try:
                img = Image.open(src)
                img = ImageOps.exif_transpose(img) if hasattr(ImageOps, "exif_transpose") else img
                img.thumbnail((400, 400), Image.LANCZOS)
                img.convert("RGB").save(t, "JPEG", quality=82)
                made += 1
            except Exception:
                pass
        it["thumb"] = "thumbs/" + thumb_name(it["file"])
    else:
        # video: poster thumbnails are made by transcode_videos.py; use when present
        it["thumb"] = ("thumbs/" + thumb_name(it["file"])
                       if os.path.exists(t) and os.path.getsize(t) > 0 else None)

print(f"thumbnails made now: {made}", flush=True)

# display copies for HEIC (browsers can't render HEIC; originals stay untouched)
os.makedirs(CONV, exist_ok=True)
converted = 0
for it in items:
    if it["ext"] == ".heic":
        c = os.path.join(CONV, thumb_name(it["file"]))
        if not os.path.exists(c):
            src = os.path.join(PHOTO, it["file"].replace("/", os.sep))
            try:
                img = Image.open(src)
                img = ImageOps.exif_transpose(img) if hasattr(ImageOps, "exif_transpose") else img
                img.thumbnail((2560, 2560), Image.LANCZOS)
                img.convert("RGB").save(c, "JPEG", quality=88)
                converted += 1
            except Exception:
                pass
        if os.path.exists(c) and os.path.getsize(c) > 0:
            it["disp"] = "converted/" + thumb_name(it["file"])
    it.setdefault("disp", it["file"])
print(f"HEIC display copies made now: {converted}", flush=True)

# orphan sweep: thumbs whose source file is no longer in the index
valid = {thumb_name(it["file"]) for it in items}
for folder in (THUMBS, CONV):
    orphans = [f for f in os.listdir(folder) if f.endswith(".jpg") and f not in valid]
    for f in orphans:
        try:
            os.remove(os.path.join(folder, f))
        except OSError:
            pass
    if orphans:
        with open(LOG, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), "THUMB-SWEEP",
                                    os.path.join(folder, "*"), f"{len(orphans)} orphan files removed",
                                    "derived cache only; source files no longer in index"])
    print(f"orphans removed in {os.path.basename(folder)}: {len(orphans)}", flush=True)

# ---- similarity groups: connected components over near-dup (same dhash, different bytes) ----
itemmap = {it["file"]: it for it in items}
parent = {it["file"]: it["file"] for it in items}

def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a

for it in items:
    for o in (it.get("near_of") or []):
        if o in parent:
            ra, rb = find(it["file"]), find(o)
            if ra != rb:
                parent[ra] = rb

clusters = {}
for k in parent:
    clusters.setdefault(find(k), []).append(k)

gid = 0
grouped = 0
for members in clusters.values():
    if len(members) < 2:
        continue
    gid += 1
    cams = [m for m in members if itemmap[m]["kind"] == "camera"]
    for m in members:
        itemmap[m]["grp"] = gid
        grouped += 1
        if len(cams) == 1:
            itemmap[m]["role"] = "raw" if m == cams[0] else "edit"
print(f"similarity groups: {gid} covering {grouped} items", flush=True)

# ---- build gallery html ----
data = []
for it in items:
    data.append({
        "f": it["file"], "t": it["thumb"], "k": it["kind"], "e": it["ext"],
        "disp": it.get("disp") or it["file"],
        "d": (it["date"] or "")[:10], "dt": it["date"] or "", "mt": it.get("mtime") or "",
        "c": it["camera"] or "",
        "w": it["w"], "h": it["h"], "s": it["size"],
        "desc": it.get("desc"), "tags": it.get("tags") or [], "ocr": it.get("ocr") or "",
        "dup": it.get("dup_of"), "near": it.get("near_of") or [],
        "exif": it.get("exif"), "dur": it.get("dur"),
        "grp": it.get("grp"), "role": it.get("role"),
    })

json_data = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

page = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Photography Gallery</title>
<style>
:root{--bg:#0e0f13;--card:#181a20;--line:#262932;--txt:#e8e9ee;--dim:#9aa0ad;--acc:#7ab8ff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:15px/1.5 'Segoe UI',system-ui,sans-serif}
header{padding:18px 24px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
header h1{font-size:20px;font-weight:600}
header .sub{color:var(--dim);font-size:13px}
.srow{display:flex;gap:8px;margin-top:10px;max-width:820px}
#q{flex:1;background:var(--card);border:1px solid var(--line);border-radius:8px;color:var(--txt);padding:9px 14px;font-size:14px;outline:none}
#q:focus{border-color:var(--acc)}
#q::placeholder{color:var(--dim)}
#sort{background:var(--card);border:1px solid var(--line);border-radius:8px;color:var(--txt);padding:9px 10px;font-size:13px;outline:none;cursor:pointer}
.chips{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.chip{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:5px 14px;cursor:pointer;font-size:13px;color:var(--dim)}
.chip.on{color:var(--txt);border-color:var(--acc)}
.strip{display:flex;gap:10px;overflow-x:auto;padding:16px 24px;scroll-behavior:smooth}
.strip::-webkit-scrollbar{height:8px}
.strip::-webkit-scrollbar-thumb{background:#333745;border-radius:4px}
.strip img,.strip .vidtile{height:130px;border-radius:8px;cursor:pointer;flex:0 0 auto;border:1px solid var(--line)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;padding:8px 24px 40px}
.mhead{grid-column:1/-1;padding:16px 0 2px;font-size:14px;color:var(--acc);border-top:1px solid var(--line)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;cursor:pointer;position:relative}
.card img{width:100%;height:150px;object-fit:cover;display:block}
.card .vidtile{width:100%;height:150px;display:flex;align-items:center;justify-content:center;background:#000;color:var(--dim);font-size:34px}
.card .cap{padding:7px 10px;font-size:12px;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .badge{position:absolute;top:6px;left:6px;background:rgba(0,0,0,.65);border-radius:4px;font-size:10px;padding:2px 6px;color:#ffd479}
.card .badge.sim{color:#7dd3a0}
.card .badge.favb{left:auto;right:6px;color:#ffd479;font-size:12px}
.card .play{position:absolute;top:6px;right:6px;background:rgba(0,0,0,.65);border-radius:4px;font-size:11px;padding:2px 7px;color:#7ab8ff}
.card .dur{position:absolute;top:126px;right:6px;background:rgba(0,0,0,.7);border-radius:4px;font-size:10px;padding:1px 5px;color:#fff}
.lb{position:fixed;inset:0;background:rgba(5,6,9,.94);display:none;z-index:10;flex-direction:column}
.lb.open{display:flex}
.lb .top{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;border-bottom:1px solid var(--line)}
.lb .top .name{font-size:14px;color:var(--txt)}
.lb .top .x{cursor:pointer;font-size:22px;color:var(--dim);padding:0 8px}
.lb .mid{flex:1;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}
.lb .mid img,.lb .mid video{max-width:92%;max-height:88%;border-radius:6px;background:#000}
#lbimg{cursor:zoom-in;transition:transform .15s}
.lb .nav{position:absolute;top:50%;transform:translateY(-50%);font-size:40px;color:var(--dim);cursor:pointer;padding:20px;user-select:none;z-index:2}
.lb .nav:hover{color:#fff}
.lb .prev{left:8px}.lb .next{right:8px}
.lb .fb{display:none;color:var(--dim);font-size:14px;text-align:center;line-height:2}
.lb .fb a{color:var(--acc)}
#cmp{display:none;position:relative;width:min(92vw,1100px);height:78vh;background:#000;border-radius:6px;touch-action:none;cursor:ew-resize;overflow:hidden}
#cmp img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;pointer-events:none;user-select:none}
#cmpB{clip-path:inset(0 0 0 var(--x,50%))}
#cmpBar{position:absolute;top:0;bottom:0;left:var(--x,50%);width:2px;background:#7ab8ff;pointer-events:none}
#cmpBar::after{content:'\21C4';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:#7ab8ff;color:#0e0f13;border-radius:50%;width:34px;height:34px;line-height:34px;text-align:center;font-size:15px}
.clab{position:absolute;bottom:10px;background:rgba(0,0,0,.7);padding:2px 10px;border-radius:10px;font-size:12px;color:var(--txt);pointer-events:none}
#clabA{left:10px}#clabB{right:10px}
.lb .info{padding:12px 22px;border-top:1px solid var(--line);background:var(--card);max-height:34vh;overflow:auto}
.acts{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.acts button,.acts select{background:#232733;border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:5px 11px;cursor:pointer;font-size:12.5px}
.acts button:hover{border-color:var(--acc)}
.lb .info .desc{font-size:15px;margin-bottom:6px}
.lb .info .tags span{display:inline-block;background:#232733;border-radius:12px;padding:2px 10px;font-size:12px;margin:0 6px 6px 0;color:var(--acc);cursor:pointer}
.lb .info .meta{color:var(--dim);font-size:12.5px;line-height:1.7}
#toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#232733;border:1px solid var(--line);border-radius:8px;padding:8px 16px;font-size:13px;opacity:0;transition:opacity .25s;pointer-events:none;z-index:50}
#toast.show{opacity:1}
h2.sec{padding:18px 24px 4px;font-size:16px;color:var(--acc)}
</style></head><body>
<header><h1>Photography Gallery</h1><div class="sub"><span id="count"></span><span id="stats"></span></div>
<div class="srow"><input id="q" type="search" placeholder="Search filename, description, tags, date, camera..." autocomplete="off">
<select id="sort"><option value="new">Newest first</option><option value="old">Oldest first</option><option value="name">By name</option></select></div>
<div class="chips" id="chips"></div>
<div class="chips" id="yrs"></div></header>
<h2 class="sec">Filmstrip</h2>
<div class="strip" id="strip"></div>
<h2 class="sec">All photos</h2>
<div class="grid" id="grid"></div>
<div class="lb" id="lb">
 <div class="top"><div class="name" id="lbname"></div><div class="x" onclick="closeLb()">&times;</div></div>
 <div class="mid"><div class="nav prev" onclick="step(-1)">&#8249;</div><img id="lbimg" alt=""><video id="lbvid" controls></video>
  <div id="cmp"><img id="cmpA" alt=""><img id="cmpB" alt=""><div id="cmpBar"></div><div class="clab" id="clabA"></div><div class="clab" id="clabB"></div></div>
  <div class="fb" id="lbfb">Video preview not available.<br><a id="lblink" href="#">Open the original file</a></div>
 <div class="nav next" onclick="step(1)">&#8250;</div></div>
 <div class="info">
  <div class="acts">
   <button id="btnCmp" onclick="cycleCmp()" style="display:none">Compare</button>
   <button id="btnSwap" onclick="swapCmp()" style="display:none">Swap sides</button>
   <button onclick="showInFolder()">Show in folder</button>
   <button onclick="copyPath()">Copy path</button>
   <button id="btnPh" onclick="openPhotos()">Open in Photos</button>
   <button id="btnFav" onclick="toggleFav()"></button>
   <button id="btnSlide" onclick="toggleSlide()">Slideshow</button>
   <select id="slideSec"><option value="3">3s</option><option value="5" selected>5s</option><option value="10">10s</option></select>
   <button onclick="goFs()">Fullscreen</button>
  </div>
  <div class="desc" id="lbdesc"></div><div class="tags" id="lbtags"></div><div class="meta" id="lbmeta"></div>
 </div>
</div>
<div id="toast"></div>
<script>
const DATA = __DATA__;
const ROOT = 'C:\\Users\\Kanchan Verma\\OneDrive\\Desktop\\photography\\';
const VEXT = ['.avi','.mp4','.mov','.mts'];
const MN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const fmtKB = s => s>1048576 ? (s/1048576).toFixed(1)+' MB' : (s/1024).toFixed(0)+' KB';
const fmtDur = s => { if(s===null||s===undefined) return ''; const m=Math.floor(s/60), r=Math.floor(s%60); return m+':'+String(r).padStart(2,'0'); };
const isVid = x => VEXT.includes(x.e);
const disp  = x => x.disp || x.f;   // HEIC items display via converted JPG; x.f stays the original
const playPath = x => x.e==='.mp4' ? x.f : (x.e==='.avi'||x.e==='.mov'||x.e==='.mts' ? 'playback/'+x.f.replace(/\//g,'__')+'.mp4' : null);
const winPath = x => ROOT + x.f.split('/').join('\\');
DATA.forEach(x=>{ x._s = (x.f+' '+(x.desc||'')+' '+(x.d||'')+' '+(x.dt||'')+' '+(x.c||'')+' '+x.k+' '+(x.tags||[]).join(' ')+' '+(x.ocr||'')).toLowerCase(); });
const grpSize = {}; DATA.forEach(x=>{ if(x.grp) grpSize[x.grp]=(grpSize[x.grp]||0)+1; });

let favs = new Set();
try { favs = new Set(JSON.parse(localStorage.getItem('photog_favs')||'[]')); } catch(e) {}
let favsOnly = false;
let kind='all', year='all', q='', sort='new', view=DATA.slice(), cur=0, curIt=null;
let partners=[], cmpIdx=0, cmpOpen=false;
let slideT=null, zoomed=false, panX=0, panY=0, imgDrag=null, imgMoved=false;

const countEl=document.getElementById('count');
(function(){ const tot=DATA.reduce((a,x)=>a+(x.s||0),0)/1048576;
  const ds=DATA.map(x=>x.d).filter(Boolean).sort();
  document.getElementById('stats').textContent = ' | '+(ds[0]||'')+' to '+(ds[ds.length-1]||'')+' | '+tot.toFixed(0)+' MB'; })();

function apply(){
  const words=q.toLowerCase().split(/\s+/).filter(Boolean);
  const key=x=>x.dt||x.mt||'';
  let list=DATA.filter(x=>
    (favsOnly ? favs.has(x.f) : true) &&
    (kind==='all' || (kind==='videos'?isVid(x):x.k===kind)) &&
    (year==='all' || (x.d||'').slice(0,4)===year) &&
    words.every(w=>x._s.includes(w)));
  if(sort==='new') list.sort((a,b)=>key(b).localeCompare(key(a)));
  else if(sort==='old') list.sort((a,b)=>key(a).localeCompare(key(b)));
  else list.sort((a,b)=>a.f.localeCompare(b.f));
  view=list;
  countEl.textContent=view.length+' of '+DATA.length+' items';
  render();
}
function buildChips(){
  const el=document.getElementById('chips'); el.innerHTML='';
  const kinds={}; DATA.forEach(x=>{ kinds[x.k]=(kinds[x.k]||0)+1; });
  const defs=[['all',DATA.length],['videos',DATA.filter(isVid).length],['favorites',favs.size]];
  Object.keys(kinds).sort().forEach(k=>defs.push([k,kinds[k]]));
  const active=favsOnly?'favorites':kind;
  defs.forEach(d=>{ const lab=d[0], n=d[1];
    const c=document.createElement('div'); c.className='chip'+(lab===active?' on':'');
    c.textContent=lab+' '+n;
    c.onclick=()=>{ if(lab==='favorites'){ favsOnly=!favsOnly; } else { favsOnly=false; kind=lab; }
      buildChips(); apply(); };
    el.appendChild(c); });
}
function buildYears(){
  const yrs=[...new Set(DATA.map(x=>(x.d||'').slice(0,4)).filter(Boolean))].sort().reverse();
  const el=document.getElementById('yrs'); el.innerHTML='';
  ['all'].concat(yrs).forEach(y=>{ const c=document.createElement('div'); c.className='chip'+(y===year?' on':'');
    c.textContent=y; c.onclick=()=>{ year=y; buildYears(); apply(); }; el.appendChild(c); });
}
function tileEl(it, idx, small){
  const el=document.createElement('div'); el.className=small?'':'card';
  if(it.t){ const im=document.createElement('img'); im.src=it.t; im.loading='lazy'; im.decoding='async'; im.onclick=()=>openLb(idx); el.appendChild(im); }
  else { const v=document.createElement('div'); v.className='vidtile'; v.textContent='\25B6'; v.onclick=()=>openLb(idx); el.appendChild(v); }
  if(!small){
    const c=document.createElement('div'); c.className='cap'; c.textContent=(it.d||'')+' '+(it.desc||it.f.split('/').pop()); el.appendChild(c);
    if(it.dup){ const b=document.createElement('div'); b.className='badge'; b.textContent='dup'; el.appendChild(b); }
    else if(it.grp&&grpSize[it.grp]>1){ const b=document.createElement('div'); b.className='badge sim'; b.textContent='similar'; el.appendChild(b); }
    if(favs.has(it.f)){ const s=document.createElement('div'); s.className='badge favb'; s.textContent='\u2605'; el.appendChild(s); }
    if(isVid(it)){
      const p=document.createElement('div'); p.className='play'; p.textContent='\25B6'; el.appendChild(p);
      if(it.dur){ const d=document.createElement('div'); d.className='dur'; d.textContent=fmtDur(it.dur); el.appendChild(d); }
    }
  }
  return el;
}
function render(){
  const strip=document.getElementById('strip'); strip.innerHTML='';
  const grid=document.getElementById('grid'); grid.innerHTML='';
  let i=0, lastM=null;
  function chunk(){
    const end=Math.min(i+120, view.length);
    for(; i<end; i++){
      const it=view[i];
      if(sort!=='name'){
        const m=(it.d||'').slice(0,7);
        if(m && m!==lastM){ lastM=m;
          const h=document.createElement('div'); h.className='mhead';
          h.textContent=MN[parseInt(m.slice(5,7),10)-1]+' '+m.slice(0,4);
          grid.appendChild(h); }
      }
      strip.appendChild(tileEl(it,i,true));
      grid.appendChild(tileEl(it,i,false));
    }
    if(i<view.length) requestAnimationFrame(chunk);
  }
  chunk();
}
function openLb(i){ cur=i; show(); document.getElementById('lb').classList.add('open'); }
function stopVid(){ const v=document.getElementById('lbvid'); try{v.pause();}catch(e){} v.removeAttribute('src'); v.load(); }
function closeCmp(quiet){
  const c=document.getElementById('cmp');
  if(c.style.display==='block'){
    c.style.display='none'; cmpOpen=false;
    document.getElementById('btnSwap').style.display='none';
    if(!quiet && curIt && !isVid(curIt)) document.getElementById('lbimg').style.display='block';
  }
}
function closeLb(){
  if(slideT){ clearInterval(slideT); slideT=null; document.getElementById('btnSlide').textContent='Slideshow'; }
  stopVid(); closeCmp(true);
  document.getElementById('lb').classList.remove('open');
}
function step(n){ cur=(cur+n+view.length)%view.length; show(); }
function show(){
  stopVid(); closeCmp(true);
  const it=view[cur]; curIt=it;
  const nm=document.getElementById('lbname'); nm.textContent=it.f.split('/').pop(); nm.title=it.f;
  const img=document.getElementById('lbimg'), vid=document.getElementById('lbvid'), fb=document.getElementById('lbfb');
  fb.style.display='none';
  zoomed=false; panX=panY=0; updImg();
  if(isVid(it)){
    img.style.display='none';
    const p=playPath(it);
    if(p){ vid.style.display='block'; if(it.t) vid.poster=it.t; vid.src=p; vid.play().catch(()=>{}); }
    else { vid.style.display='none'; document.getElementById('lblink').href=it.f; fb.style.display='block'; }
  } else {
    vid.style.display='none';
    img.style.display='block'; img.src=disp(it);
  }
  document.getElementById('lbdesc').textContent=it.desc||'';
  document.getElementById('lbtags').innerHTML=(it.tags||[]).map(t=>'<span data-t="'+String(t).replace(/"/g,'')+'">'+t+'</span>').join('');
  let m=[];
  if(it.dt) m.push('Taken: '+it.dt);
  if(it.exif){ const e=it.exif, parts=[];
    if(e.iso) parts.push('ISO '+e.iso);
    if(e.f) parts.push('f/'+e.f);
    if(e.sh) parts.push(e.sh);
    if(e.fl) parts.push(e.fl);
    if(parts.length) m.push('EXIF: '+parts.join(' | ')); }
  if(it.c) m.push('Camera: '+it.c);
  if(it.ocr) m.push('Text in image: '+it.ocr.replace(/\n/g,' | ').slice(0,140));
  if(it.w) m.push('Size: '+it.w+' x '+it.h);
  if(isVid(it)&&it.dur) m.push('Length: '+fmtDur(it.dur));
  m.push('File: '+fmtKB(it.s));
  m.push('Type: '+it.k);
  if(isVid(it)) m.push('Playback: '+(playPath(it) ? (it.e==='.mp4'?'native':'optimized copy') : 'unavailable'));
  if(it.dup) m.push('Exact duplicate of: '+it.dup);
  if(it.near&&it.near.length) m.push('Similar to: '+it.near.join(', '));
  document.getElementById('lbmeta').innerHTML=m.map(x=>x+'<br>').join('');
  document.getElementById('btnCmp').style.display=(it.grp&&grpSize[it.grp]>1)?'':'none';
  document.getElementById('btnPh').style.display=isVid(it)?'none':'';
  document.getElementById('btnFav').textContent=favs.has(it.f)?'\u2605 Favorited':'\u2606 Favorite';
  partners = it.grp ? DATA.filter(x=>x.grp===it.grp && x.f!==it.f && !x.dup) : [];
  cmpIdx=0;
  preload();
}
function preload(){
  [1,-1].forEach(n=>{ const it=view[(cur+n+view.length)%view.length];
    if(it && !isVid(it)){ const im=new Image(); im.src=disp(it); } });
}
function cycleCmp(){
  if(!partners.length) return;
  const a=view[cur], b=partners[cmpIdx % partners.length]; cmpIdx++;
  document.getElementById('cmpA').src=disp(a);
  document.getElementById('cmpB').src=disp(b);
  document.getElementById('clabA').textContent=a.role||a.f.split('/').pop();
  document.getElementById('clabB').textContent=b.role||b.f.split('/').pop();
  const c=document.getElementById('cmp');
  c.style.setProperty('--x','50%');
  c.style.display='block'; cmpOpen=true;
  document.getElementById('lbimg').style.display='none';
  document.getElementById('lbvid').style.display='none';
  document.getElementById('btnSwap').style.display='';
}
function swapCmp(){
  const iA=document.getElementById('cmpA'), iB=document.getElementById('cmpB');
  const t=iA.src; iA.src=iB.src; iB.src=t;
  const lA=document.getElementById('clabA'), lB=document.getElementById('clabB');
  const tl=lA.textContent; lA.textContent=lB.textContent; lB.textContent=tl;
}
const cmpEl=document.getElementById('cmp');
let cmpDrag=false;
function cmpSet(cx){ const r=cmpEl.getBoundingClientRect();
  let p=(cx-r.left)/r.width*100; p=Math.max(0,Math.min(100,p));
  cmpEl.style.setProperty('--x',p+'%'); }
cmpEl.addEventListener('pointerdown',e=>{ cmpDrag=true; cmpEl.setPointerCapture(e.pointerId); cmpSet(e.clientX); });
cmpEl.addEventListener('pointermove',e=>{ if(cmpDrag) cmpSet(e.clientX); });
cmpEl.addEventListener('pointerup',()=>{ cmpDrag=false; });
function nudgeCmp(d){ const r=cmpEl.getBoundingClientRect();
  let cur=parseFloat(getComputedStyle(cmpEl).getPropertyValue('--x'))||50;
  cmpSet(r.left + r.width*(cur+d)/100); }
function showInFolder(){ location.href='photo-view:'+encodeURIComponent(winPath(view[cur])); }
function openPhotos(){ location.href='ms-photos:viewer?filename='+encodeURIComponent(winPath(view[cur])); }
let toastT=null;
function flash(msg){ const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  clearTimeout(toastT); toastT=setTimeout(()=>t.classList.remove('show'),1800); }
function fallbackCopy(p,done){ const ta=document.createElement('textarea'); ta.value=p; document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); done(); }catch(e){ flash('Copy failed'); } ta.remove(); }
function copyPath(){
  const p=winPath(view[cur]); const done=()=>flash('Path copied');
  if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(p).then(done).catch(()=>fallbackCopy(p,done)); }
  else fallbackCopy(p,done);
}
function toggleFav(){
  const f=view[cur].f;
  if(favs.has(f)){ favs.delete(f); flash('Removed from favorites'); }
  else { favs.add(f); flash('Added to favorites'); }
  try{ localStorage.setItem('photog_favs', JSON.stringify([...favs])); }catch(e){}
  document.getElementById('btnFav').textContent=favs.has(f)?'\u2605 Favorited':'\u2606 Favorite';
  buildChips(); render();
}
function toggleSlide(){
  const b=document.getElementById('btnSlide');
  if(slideT){ clearInterval(slideT); slideT=null; b.textContent='Slideshow'; }
  else { const sec=parseInt(document.getElementById('slideSec').value,10)||5;
    slideT=setInterval(()=>step(1), sec*1000); b.textContent='Stop show'; }
}
function goFs(){ const lb=document.getElementById('lb');
  if(document.fullscreenElement){ document.exitFullscreen(); }
  else if(lb.requestFullscreen){ lb.requestFullscreen().catch(()=>{}); } }
const lbimg=document.getElementById('lbimg');
function updImg(){ lbimg.style.transform=zoomed?('scale(2) translate('+panX+'px,'+panY+'px)'):''; }
lbimg.addEventListener('click',()=>{ if(imgMoved){ imgMoved=false; return; }
  zoomed=!zoomed; panX=panY=0; updImg(); lbimg.style.cursor=zoomed?'zoom-out':'zoom-in'; });
lbimg.addEventListener('pointerdown',e=>{ if(zoomed){ imgDrag={x:e.clientX,y:e.clientY,px:panX,py:panY}; lbimg.setPointerCapture(e.pointerId); } });
lbimg.addEventListener('pointermove',e=>{ if(imgDrag){ const dx=e.clientX-imgDrag.x, dy=e.clientY-imgDrag.y;
  if(Math.abs(dx)>4||Math.abs(dy)>4) imgMoved=true;
  panX=imgDrag.px+dx; panY=imgDrag.py+dy; updImg(); } });
lbimg.addEventListener('pointerup',()=>{ imgDrag=null; });
const qEl=document.getElementById('q');
let qT=null;
qEl.addEventListener('input',()=>{ clearTimeout(qT); qT=setTimeout(()=>{ q=qEl.value; apply(); },120); });
document.getElementById('sort').onchange=function(){ sort=this.value; apply(); };
document.getElementById('lbtags').addEventListener('click',e=>{
  const t=e.target.getAttribute&&e.target.getAttribute('data-t');
  if(t){ q=t; qEl.value=t; closeLb(); apply(); } });
document.addEventListener('keydown',e=>{
  const lb=document.getElementById('lb');
  if(!lb.classList.contains('open')) return;
  if(cmpOpen){
    if(e.key==='ArrowLeft'){ nudgeCmp(-3); e.preventDefault(); }
    else if(e.key==='ArrowRight'){ nudgeCmp(3); e.preventDefault(); }
    else if(e.key==='Escape'||e.key==='c'||e.key==='C'){ closeCmp(); e.preventDefault(); }
    return;
  }
  if(e.key==='Escape') closeLb();
  else if(e.key==='ArrowRight') step(1);
  else if(e.key==='ArrowLeft') step(-1);
  else if(e.key===' '){ toggleSlide(); e.preventDefault(); }
});
buildChips(); buildYears(); apply();
</script></body></html>"""

out = os.path.join(PHOTO, "gallery.html")
open(out, "w", encoding="utf-8").write(page.replace("__DATA__", json_data))
print(f"gallery.html written with {len(data)} items", flush=True)
print("GALLERY DONE", flush=True)
