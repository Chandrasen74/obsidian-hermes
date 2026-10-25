import math, json
from PIL import Image

im=Image.open('/home/user/ref/tile_f000.png').convert('RGB'); W,H=im.size; px=im.load()
X0,Y0,X1,Y1 = 10,33,1142,666
sx=1920/(X1-X0); sy=1080/(Y1-Y0)
def iswhite(p): return p[0]>185 and p[1]>185 and p[2]>185 and max(p)-min(p)<40

arc=[]
for y in range(470,Y1-4):
    for x in range(X0+2,905):
        if not iswhite(px[x,y]): continue
        if x<355 and y<480: continue             # hoop stand/net zone
        if x>850 and y>583: continue             # label box
        if 505<x<585 and 415<y<600: continue     # man + ball bodies
        arc.append((x,y))
arc=list(set(arc))
print("filtered arc pts:",len(arc))

def chain(pool,maxgap):
    best=None
    S=sorted(pool,key=lambda p:p[0])
    for start in S[:6]:
        used=set([start]);cur=start;ch=[start]
        while True:
            nxt=None;bd=1e18
            cx,cy=cur
            for p in pool:
                if p in used: continue
                d=(p[0]-cx)**2+(p[1]-cy)**2
                if d<bd: bd=d;nxt=p
            if nxt is None or bd>maxgap*maxgap: break
            ch.append(nxt);used.add(nxt);cur=nxt
        if best is None or len(ch)>len(best): best=ch
    return best

c=chain(arc,45)
print("best chain len",len(c),"start",c[0],"end",c[-1])
# monotonic smoothness check
d=[round(math.hypot(c[i+1][0]-c[i][0],c[i+1][1]-c[i][1]),1) for i in range(len(c)-1)]
print("step max/mean: %.1f %.1f"%(max(d),sum(d)/len(d)))

dec=c[::4]
if c[-1]!=dec[-1]: dec.append(c[-1])
def to_world(p):
    sxp=(p[0]-X0)*sx; syp=(p[1]-Y0)*sy
    return (round(sxp-215),round(syp+20))
world=[to_world(p) for p in dec]
print("n=",len(world),"first",world[0],"last",world[-1])
with open('/home/user/ref/arc_world.json','w') as f: json.dump(world,f)
print(json.dumps(world))
