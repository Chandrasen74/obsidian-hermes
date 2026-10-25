import math
from PIL import Image

im=Image.open('/home/user/ref/tile_f000.png').convert('RGB'); W,H=im.size; px=im.load()
X0,Y0,X1,Y1 = 10,33,1142,666          # content bounds (inside the beige border)
print("content",X0,Y0,X1,Y1, "scale x%.4f y%.4f to 1080p"%(1920/(X1-X0),1080/(Y1-Y0)))

def iswhite(p): return p[0]>185 and p[1]>185 and p[2]>185 and max(p)-min(p)<40

pts=[]
for y in range(Y0+80,Y1-6):            # court area only
    for x in range(X0+4,X1-4):
        if not iswhite(px[x,y]): continue
        if x>855 and y>588: continue   # label box
        if 505<x<585 and 420<y<600: continue   # man + ball zone
        pts.append((x,y))
left =[p for p in pts if p[0]<900]
right=[p for p in pts if p[0]>=900]
print("arc pts",len(left)," right pts",len(right))

def fit_ellipse_axis(p):
    # x^2 + A x + C y^2 + D y + E = 0  (axis-aligned ellipse)
    n=len(p); M=[[0.0]*4 for _ in range(4)]; v=[0.0]*4
    for x,y in p:
        r=[x,y*y,y,1.0]; b=-(x*x)
        for i in range(4):
            M[i][0]+=r[i]*x; M[i][1]+=r[i]*y*y; M[i][2]+=r[i]*y; M[i][3]+=r[i]*1
            v[i]+=r[i]*b
    for i in range(4):
        piv=M[i][i]
        for j in range(i,4): M[i][j]/=piv
        v[i]/=piv
        for k in range(4):
            if k==i: continue
            f=M[k][i]
            for j in range(i,4): M[k][j]-=f*M[i][j]
            v[k]-=f*v[i]
    A,C,D,E=v; cx=-A/2; cy=-D/(2*C); rx=math.sqrt(max(cx*cx,0))  # will recompute properly
    # x^2+A x + C y^2 + D y + E=0 -> (x-cx)^2 + C(y-cy)^2 = cx^2 + C cy^2 - E
    rhs=cx*cx+C*cy*cy-E
    rx=math.sqrt(rhs); ry=math.sqrt(rhs/C)
    return cx,cy,rx,ry

if left:
    cx,cy,rx,ry=fit_ellipse_axis(left)
    resid=sum(abs(math.hypot((x-cx)/rx,(y-cy)/ry)-1) for x,y in left)/len(left)
    print("ARC ellipse tile: cx=%.1f cy=%.1f rx=%.1f ry=%.1f resid=%.3f"%(cx,cy,rx,ry,resid))
    ang=sorted(math.atan2((y-cy)/ry,(x-cx)/rx) for x,y in left)
    print("ARC angles: %.3f .. %.3f"%(ang[0],ang[-1]))
    sx=1920/(X1-X0); sy=1080/(Y1-Y0)
    C=(cx-X0)*sx,(cy-Y0)*sy,rx*sx,ry*sy
    print("ARC 1080p screen: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%C)
if right:
    cx,cy,rx,ry=fit_ellipse_axis(right)
    resid=sum(abs(math.hypot((x-cx)/rx,(y-cy)/ry)-1) for x,y in right)/len(right)
    print("RGTC ellipse tile: cx=%.1f cy=%.1f rx=%.1f ry=%.1f resid=%.3f"%(cx,cy,rx,ry,resid))
    ang=sorted(math.atan2((y-cy)/ry,(x-cx)/rx) for x,y in right)
    print("RGTC angles: %.3f .. %.3f"%(ang[0],ang[-1]))
    sx=1920/(X1-X0); sy=1080/(Y1-Y0)
    print("RGTC 1080p screen: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%((cx-X0)*sx,(cy-Y0)*sy,rx*sx,ry*sy))

# extra anchors: pole extent, rim, bands
dpx=[px[x,y] for y in range(Y0,Y1) for x in range(30,260)]
# vertical gray pole: light-gray pixels column-wise
polXs={}
for y in range(120,560):
    for x in range(30,260):
        p=px[x,y]
        if abs(p[0]-205)<35 and abs(p[1]-210)<35 and abs(p[2]-215)<35:
            polXs.setdefault(x,0);polXs[x]+=1
            break
print("pole cols (x:count) sample:", sorted(polXs.items())[:1], sorted(polXs.items())[-1:] if polXs else None)
# rim: navy
rxs=[]; rys=[]
for y in range(230,330):
    for x in range(60,330):
        p=px[x,y]
        if abs(p[0]-38)<30 and abs(p[1]-52)<30 and abs(p[2]-122)<40: rxs.append(x);rys.append(y)
if rxs: print("rim tile bbox: x %d..%d y %d..%d"%(min(rxs),max(rxs),min(rys),max(rys)))
sx=1920/(X1-X0); sy=1080/(Y1-Y0)
print("rim 1080p screen: x %.0f..%.0f y %.0f..%.0f center (%.0f,%.0f)"%((min(rxs)-X0)*sx,(max(rxs)-X0)*sx,(min(rys)-Y0)*sy,(max(rys)-Y0)*sy,(min(rxs)+max(rxs)-2*X0)*sx/2,(min(rys)+max(rys)-2*Y0)*sy/2))
# man feet/ball bottoms
mani=[]; [mani.append((x,y)) for y in range(400,620) for x in range(500,600) if px[x,y][0]>225 and px[x,y][1]>190 and px[x,y][2]<90]
balli=[]; [balli.append((x,y)) for y in range(400,620) for x in range(100,220) if px[x,y][0]>215 and 100<px[x,y][1]<215 and px[x,y][2]<95]
if mani: print("man feet bottom y tile=%d -> screen %.0f ; man x range %d..%d -> screen %.0f..%.0f"%(max(y for x,y in mani),(max(y for x,y in mani)-Y0)*sy,min(x for x,y in mani),max(x for x,y in mani),(min(x for x,y in mani)-X0)*sx,(max(x for x,y in mani)-X0)*sx))
if balli: print("ball bottom y tile=%d -> screen %.0f ; ball center screen x=%.0f"%(max(y for x,y in balli),(max(y for x,y in balli)-Y0)*sy,((min(x for x,y in balli)+max(x for x,y in balli))/2-X0)*sx))
