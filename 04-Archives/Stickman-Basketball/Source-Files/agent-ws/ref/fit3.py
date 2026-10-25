import math, json
from PIL import Image

im=Image.open('/home/user/ref/tile_f000.png').convert('RGB'); W,H=im.size; px=im.load()
X0,Y0,X1,Y1 = 10,33,1142,666
sx=1920/(X1-X0); sy=1080/(Y1-Y0)
def to_screen(p): # tile px -> 1920x1080 screen coords
    return ((p[0]-X0)*sx,(p[1]-Y0)*sy)

def iswhite(p): return p[0]>185 and p[1]>185 and p[2]>185 and max(p)-min(p)<40

arc=[]
for y in range(480,Y1-6):
    for x in range(X0+4,900):
        if not iswhite(px[x,y]): continue
        if x>850 and y>585: continue             # label box
        if 505<x<585 and 415<y<600: continue     # man + ball bodies
        arc.append((x,y))
print("arc pts:",len(arc))

# --- greedy nearest-neighbor chaining from the leftmost point ---
S=sorted(arc,key=lambda p:p[0])
start=S[0]
chain=[start]; used=set([start]); cur=start
pool=arc
while True:
    nxt=None;bd=1e9
    cx,cy=cur
    for p in pool:
        if p in used: continue
        d=(p[0]-cx)**2+(p[1]-cy)**2
        if d<bd: bd=d;nxt=p
    if nxt is None or bd>30*30: break
    chain.append(nxt);used.add(nxt);cur=nxt
print("chain len:",len(chain)," end:",chain[-1])

# decimate, then convert to 1080p screen, then to world (anchor: camera cx=745,cy=560)
dec=chain[::max(1,len(chain)//90)]
if chain[-1]!=dec[-1]: dec.append(chain[-1])
def to_world(p):
    sxp,syp=to_screen(p)
    return (round(sxp-215),round(syp+20))    # world = screen - cx + 960, screen + cy - 540  (cx=745,cy=560)
world=[to_world(p) for p in dec]
print("ARC world polyline (first/last):",world[0],world[-1],"n=",len(world))
with open('arc_world.json','w') as f: json.dump(world,f)

# --- right circle: keep only safe pixels above the label ---
rg=[]
for y in range(480,585):
    for x in range(1080,X1):
        if iswhite(px[x,y]): rg.append((x,y))
print("right-circle pts:",len(rg))
if rg:
    xs=[p[0] for p in rg];ys=[p[1] for p in rg]
    print("rgt bbox: x %d..%d  y %d..%d"%(min(xs),max(xs),min(ys),max(ys)))
    # axis ellipse LSQ (compact patch -> should fit)
    n=len(rg); M=[[0.0]*4 for _ in range(4)]; v=[0.0]*4
    for x,y in rg:
        rr=[x,y*y,y,1.0]; b=-(x*x)
        for i in range(4):
            for j in range(4): M[i][j]+=rr[i]*rr[j]
            v[i]+=rr[i]*b
    # simple 4x4 gauss
    for i in range(4):
        piv=M[i][i]
        for j in range(i,4): M[i][j]/=piv
        v[i]/=piv
        for k in range(4):
            if k==i: continue
            f=M[k][i]
            for j in range(i,4): M[k][j]-=f*M[i][j]
            v[k]-=f*v[i]
    A,C,D,E=v; cx=-A/2; cy=-D/(2*C); rhs=cx*cx+C*cy*cy-E
    if C>0 and rhs>0:
        rx=math.sqrt(rhs); ry=math.sqrt(rhs/C)
        resid=sum(abs(math.hypot((x-cx)/rx,(y-cy)/ry)-1) for x,y in rg)/len(rg)
        print("RGT ellipse tile: cx=%.1f cy=%.1f rx=%.1f ry=%.1f resid=%.3f"%(cx,cy,rx,ry,resid))
        sc=to_screen((cx,cy))
        print("RGT 1080p screen: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%(sc[0],sc[1],rx*sx,ry*sy))
        print("RGT world(anchor cx745 cy560): cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%(sc[0]-215,sc[1]+20,rx*sx,ry*sy))
    else:
        print("RGT ellipse fit degenerate; C=%.3g rhs=%.3g"%(C,rhs))
