import math, json
from PIL import Image

im=Image.open('/home/user/ref/tile_f000.png').convert('RGB'); W,H=im.size; px=im.load()
X0,Y0,X1,Y1 = 38,33,1142,655
sx=1920/(1142-10); sy=1080/(666-33)
def iswhite(p): return p[0]>185 and p[1]>185 and p[2]>185 and max(p)-min(p)<40

arc=[];rgt=[]
for y in range(455,Y1):
    for x in range(X0,X1):
        if not iswhite(px[x,y]): continue
        if x>850 and y>580: continue    # label box
        if x<110 and y<470: continue    # pole
        if 95<x<345 and 230<y<430: continue  # net
        if 505<x<590 and 410<y<600: continue # man
        if 125<x<175 and 425<y<475: continue # ball
        if x>1050: rgt.append((x,y))
        else: arc.append((x,y))
print("arc pts",len(arc),"rgt pts",len(rgt))

def fit_ell(p):
    n=len(p); M=[[0.0]*4 for _ in range(4)]; v=[0.0]*4
    for x,y in p:
        rr=[x,y*y,y,1.0]; b=-(x*x)
        for i in range(4):
            for j in range(4): M[i][j]+=rr[i]*rr[j]
            v[i]+=rr[i]*b
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
    rx=math.sqrt(rhs); ry=math.sqrt(rhs/C)
    return cx,cy,rx,ry

cx,cy,rx,ry=fit_ell(arc)
resid=sum(abs(math.hypot((x-cx)/rx,(y-cy)/ry)-1) for x,y in arc)/len(arc)
print("ARC ellipse: cx=%.1f cy=%.1f rx=%.1f ry=%.1f resid=%.3f"%(cx,cy,rx,ry,resid))
angles=sorted(set(round(math.atan2((y-cy)/ry,(x-cx)/rx),2) for x,y in arc))
print("angle range: %.3f..%.3f  gaps>0.15:"%(angles[0],angles[-1]),[(a,b) for a,b in zip(angles,angles[1:]) if b-a>0.15])
# sample fitted ellipse into clean polyline (stitches the man/label gaps)
import numpy as np
def th_of(x,y): return math.atan2((y-cy)/ry,(x-cx)/rx)
th=[th_of(x,y) for x,y in arc]
t0,t1=min(th),max(th)
print("theta span %.3f %.3f"%(t0,t1))
N=int((t1-t0)*120)+2
poly=[(cx+rx*math.cos(a),cy+ry*math.sin(a)) for a in [t0+(t1-t0)*i/(N-1) for i in range(N)]]
# to 1080p screen then world (anchor camera cx=745,cy=560 -> world = screen-215, +20)
W_=[(round((x-10)*sx-215),round((y-33)*sy+20)) for x,y in poly]
print("world n=%d first %s last %s"%(len(W_),W_[0],W_[-1]))
json.dump(W_,open('/home/user/ref/arc_world.json','w'))
SC=[(round((x-10)*sx),round((y-33)*sy)) for x,y in poly]
print("screen first/last:",SC[0],SC[-1])

if rgt:
    xs=[p[0] for p in rgt];ys=[p[1] for p in rgt]
    print("rgt bbox x %.0f..%.0f y %.0f..%.0f n=%d"%(min(xs),max(xs),min(ys),max(ys),len(rgt)))
    cx2,cy2,rx2,ry2=fit_ell(rgt)
    resid=sum(abs(math.hypot((x-cx2)/rx2,(y-cy2)/ry2)-1) for x,y in rgt)/len(rgt)
    print("RGT ellipse: cx=%.1f cy=%.1f rx=%.1f ry=%.1f resid=%.3f"%(cx2,cy2,rx2,ry2,resid))
    print("RGT world: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%((cx2-10)*sx-215,(cy2-33)*sy+20,rx2*sx,ry2*sy))
