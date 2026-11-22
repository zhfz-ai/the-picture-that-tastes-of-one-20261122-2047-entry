import os, struct, zlib, math, random
W=1024; H=1024
buf=bytearray(W*H*3)

def set_px(x,y,r,g,b):
    if 0<=x<W and 0<=y<H:
        i=(y*W+x)*3; buf[i]=r; buf[i+1]=g; buf[i+2]=b

def blend(x,y,r,g,b,a):
    if 0<=x<W and 0<=y<H:
        i=(y*W+x)*3
        buf[i]=int(buf[i]*(1-a)+r*a); buf[i+1]=int(buf[i+1]*(1-a)+g*a); buf[i+2]=int(buf[i+2]*(1-a)+b*a)

def hspan(y,x0,x1,r,g,b):
    if y<0 or y>=H: return
    x0=max(0,x0); x1=min(W-1,x1)
    i=(y*W+x0)*3
    for x in range(x0,x1+1):
        buf[i]=r; buf[i+1]=g; buf[i+2]=b; i+=3

def rect(x0,y0,x1,y1,r,g,b):
    for y in range(y0,y1+1): hspan(y,x0,x1,r,g,b)

def ellipse(cx,cy,rx,ry,r,g,b):
    for y in range(cy-ry,cy+ry+1):
        if y<0 or y>=H: continue
        dy=(y-cy)/ry
        if abs(dy)>1: continue
        dx=int(rx*math.sqrt(1-dy*dy))
        hspan(y,cx-dx,cx+dx,r,g,b)

def stamp(cx,cy,rad,r,g,b):
    ellipse(cx,cy,rad,rad,r,g,b)

def thick_line(pts,rad,r,g,b):
    for i in range(len(pts)-1):
        x0,y0=pts[i]; x1,y1=pts[i+1]
        steps=max(abs(x1-x0),abs(y1-y0),1)
        for s in range(steps+1):
            t=s/steps
            stamp(int(x0+(x1-x0)*t),int(y0+(y1-y0)*t),rad,r,g,b)

def bezier(p0,p1,p2,p3,n=40):
    pts=[]
    for i in range(n+1):
        t=i/n; u=1-t
        x=int(u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0])
        y=int(u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
        pts.append((x,y))
    return pts

def rounded_rect(x0,y0,x1,y1,rad,r,g,b):
    rect(x0+rad,y0,x1-rad,y1,r,g,b)
    rect(x0,y0+rad,x1,y1-rad,r,g,b)
    ellipse(x0+rad,y0+rad,rad,rad,r,g,b); ellipse(x1-rad,y0+rad,rad,rad,r,g,b)
    ellipse(x0+rad,y1-rad,rad,rad,r,g,b); ellipse(x1-rad,y1-rad,rad,rad,r,g,b)

# background radial warm gradient + vignette
cx,cy=W//2,H//2
for y in range(H):
    for x in range(W):
        d=math.sqrt((x-cx)**2+(y-cy)**2)/720.0
        d=min(d,1.0)
        r=int(72*(1-d)+14*d); g=int(44*(1-d)+9*d); b=int(26*(1-d)+6*d)
        set_px(x,y,r,g,b)

rng=random.Random(20261122)
# table speckle crumbs later; first breads
# left bread: crust + inner
rounded_rect(70,330,430,700,70,150,92,38)
rounded_rect(95,355,405,675,55,198,138,62)
rounded_rect(115,375,390,655,45,225,168,84)
# right bread
rounded_rect(594,330,954,700,70,150,92,38)
rounded_rect(619,355,929,675,55,198,138,62)
rounded_rect(634,375,909,655,45,225,168,84)
# toast texture: irregular speckles (seeded)
for _ in range(420):
    side=rng.choice([(115,390),(634,909)])
    x=rng.randint(side[0]+15,side[1]-15); y=rng.randint(390,640)
    s=rng.randint(2,7)
    c=rng.choice([(205,148,66),(215,160,76),(192,132,54),(232,182,98)])
    rect(x,y,x+s,y+max(1,s//2),c[0],c[1],c[2])

# cheese base slabs on inner faces
rect(400,400,435,630,245,205,105)
rect(589,400,624,630,245,205,105)

# strands: horizontal sagging curves
strand_specs=[]
for i in range(17):
    y0=408+i*13+rng.randint(-3,3)
    sag=rng.randint(8,48)
    strand_specs.append((y0,sag))
for idx,(y0,sag) in enumerate(strand_specs):
    pts=bezier((425,y0),(500,y0+sag),(525,y0+sag),(600,y0))
    rad=7 if idx%3 else 10
    thick_line(pts,rad,246,206,96)
    thick_line(pts,max(3,rad-3),251,224,128)
    hpts=[(x,y-4) for (x,y) in pts]
    thick_line(hpts,2,255,246,196)
# glossy sheen blobs on cheese slabs
for (gx,gy) in [(418,450),(418,560),(606,460),(606,570)]:
    ellipse(gx,gy,10,26,255,240,175)

# cheese drips
for (dx,dy,ln) in [(420,500,60),(605,480,55),(415,580,45),(610,590,50)]:
    thick_line([(dx,dy),(dx+ (6 if dx<512 else -6),dy+ln)],8,248,214,110)
    stamp(dx+(6 if dx<512 else -6),dy+ln,10,248,214,110)

# steam wisps (blend)
for sx in [430,512,590]:
    pts=bezier((sx,390),(sx-35,300),(sx+35,220),(sx-15,130))
    for (x,y) in pts:
        for rr in range(7,0,-1):
            for a in range(0,360,30):
                xx=x+int(rr*math.cos(math.radians(a))); yy=y+int(rr*math.sin(math.radians(a)))
                blend(xx,yy,255,255,255,0.10)

# crumbs
for _ in range(260):
    x=rng.randint(60,964); y=rng.randint(690,950)
    s=rng.randint(1,4)
    c=rng.choice([(180,125,55),(160,105,45),(200,145,70)])
    rect(x,y,x+s,y+s,c[0],c[1],c[2])

# vignette corners darken
for y in range(H):
    for x in range(W):
        d=math.sqrt((x-cx)**2+(y-cy)**2)/760.0
        if d>0.75:
            f=max(0.45,1-(d-0.75)*1.1)
            i=(y*W+x)*3
            buf[i]=int(buf[i]*f); buf[i+1]=int(buf[i+1]*f); buf[i+2]=int(buf[i+2]*f)

def chunk(t,data):
    c=struct.pack(">I",len(data))+t+data
    return c+struct.pack(">I",zlib.crc32(t+data)&0xffffffff)

raw=bytearray()
for y in range(H):
    raw.append(0)
    raw.extend(buf[y*W*3:(y+1)*W*3])
png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(bytes(raw),6))+chunk(b"IEND",b"")
os.makedirs("/output",exist_ok=True)
with open("/output/entry.png","wb") as f: f.write(png)
try: os.chmod("/output/entry.png",0o644)
except Exception: pass
try: os.chmod("/output",0o755)
except Exception: pass
print(len(png))
