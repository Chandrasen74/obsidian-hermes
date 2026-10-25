import math, sys
from PIL import Image

im = Image.open('/home/user/ref/tile_f000.png').convert('RGB')
W,H = im.size
px = im.load()
print("tile size", W, H)

def iswhite(p):
    return p[0]>195 and p[1]>195 and p[2]>195 and (max(p)-min(p))<30

line_px=[]
for y in range(500, H-20):
    for x in range(20, W-20):
        if not iswhite(px[x,y]): continue
        if x > 0.70*W and y > 0.88*H: continue        # label box
        if 0.42*W<x<0.55*W and 0.55*H<y<0.95*H: continue  # man/ball zone
        line_px.append((x,y))
print("white line px:", len(line_px))

arc    = [(x,y) for x,y in line_px if x < 0.72*W and y < 0.995*H]
rightc = [(x,y) for x,y in line_px if x >=0.72*W and not (x > 0.70*W and y > 0.88*H)]
print("arc px:",len(arc)," circle px:",len(rightc))

def fit_circle(pts):
    # least squares: x^2+y^2 + D x + E y + F = 0
    A=[[0.0]*3 for _ in range(3)]; b=[0.0]*3
    for x,y in pts:
        r=[x,y,1.0]; rhs=-(x*x+y*y)
        for i in range(3):
            for j in range(3): A[i][j]+=r[i]*r[j]
            b[i]+=r[i]*rhs
    # gaussian elim
    for i in range(3):
        piv=A[i][i]
        for j in range(i,3): A[i][j]/=piv
        b[i]/=piv
        for k in range(3):
            if k==i: continue
            f=A[k][i]
            for j in range(i,3): A[k][j]-=f*A[i][j]
            b[k]-=f*b[i]
    D,E,F=b; cx=-D/2; cy=-E/2; r=math.sqrt(cx*cx+cy*cy-F)
    return cx,cy,r

if arc:
    cx,cy,r=fit_circle(arc)
    print("ARC fit(tile px): center=(%.1f,%.1f) r=%.1f"%(cx,cy,r))
    tot=sum(abs(math.hypot(x-cx,y-cy)-r) for x,y in arc)/len(arc)
    print("ARC mean residual: %.2f px"%tot)
    ang=sorted(math.atan2(y-cy,x-cx) for x,y in arc)
    print("ARC angle span: %.3f .. %.3f rad"%(ang[0],ang[-1]))
    sx=1920.0/W; sy=1080.0/H
    print("ARC @1080p screen: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%(cx*sx,cy*sy,r*sx,r*sy))
if rightc:
    cx,cy,r=fit_circle(rightc)
    print("CIRC fit(tile px): center=(%.1f,%.1f) r=%.1f"%(cx,cy,r))
    tot=sum(abs(math.hypot(x-cx,y-cx)-r) for x,y in rightc)/len(rightc); print("CIRC resid %.2f"%tot)
    ang=sorted(math.atan2(y-cy,x-cx) for x,y in rightc)
    print("CIRC angle span: %.3f .. %.3f"%(ang[0],ang[-1]))
    sx=1920.0/W; sy=1080.0/H
    print("CIRC @1080p screen: cx=%.0f cy=%.0f rx=%.0f ry=%.0f"%(cx*sx,cy*sy,r*sx,r*sy))

# ---- measure other reference anchors ----
def bbox(pred):
    xs=[];ys=[]
    for y in range(0,H):
        for x in range(0,W):
            if pred(px[x,y]): xs.append(x);ys.append(y)
    if not xs: return None
    return min(xs),min(ys),max(xs),max(ys),len(xs)

sky_g=None
for y in range(H):
    p=px[int(W*0.75),y]
    if p[1]>110 and p[0]<60: sky_g=y;break
print("grass top row @ x=0.75W:", sky_g)
court_y=None
for y in range(H-1,-1,-1):
    p=px[int(W*0.75),y]
    if p[2]>180 and p[1]>130: court_y=y;break
print("court last blue row (bottom):", court_y)
g2=None
for y in range(H):
    p=px[int(W*0.5),y]
    if p[1]>110 and p[0]<60: g2=y;break
print("grass top @ x=0.5W:", g2)

rim=bbox(lambda p: abs(p[0]-38)<45 and abs(p[1]-52)<45 and abs(p[2]-122)<70)
print("rim(navy) bbox:",rim)
man=bbox(lambda p: p[0]>225 and p[1]>195 and p[2]<90)
print("man(yellow) bbox:",man)
ball=bbox(lambda p: p[0]>215 and 110<p[1]<210 and p[2]<95)
print("ball(orange) bbox:",ball)
# grass bottom = court edge: scan col x=0.62W for green->blue
for y in range(H-1):
    p1=px[int(W*0.62),y]; p2=px[int(W*0.62),y+1]
    if p1[1]>110 and p1[0]<80 and p2[2]>170 and p2[1]>110:
        print("grass->court edge y:", y); break
