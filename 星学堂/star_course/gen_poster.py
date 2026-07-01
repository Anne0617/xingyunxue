
import os, random
from PIL import Image, ImageDraw, ImageFont

# Ensure we're in the right directory
os.chdir(r'D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂\\star_course')

W, H = 1080, 1920
img = Image.new('RGB', (W, H), (12, 12, 46))
draw = ImageDraw.Draw(img)

font_dir = 'C:/Windows/Fonts'
tf = ImageFont.truetype(os.path.join(font_dir, 'msyhbd.ttc'), 72)
bf = ImageFont.truetype(os.path.join(font_dir, 'msyhbd.ttc'), 56)
nf = ImageFont.truetype(os.path.join(font_dir, 'msyhbd.ttc'), 36)
mf = ImageFont.truetype(os.path.join(font_dir, 'msyh.ttc'), 30)
sf = ImageFont.truetype(os.path.join(font_dir, 'msyhl.ttc'), 24)
xf = ImageFont.truetype(os.path.join(font_dir, 'msyhl.ttc'), 20)

G = (245, 158, 11)
WHT = (255, 255, 255)
D = (100, 100, 130)
GL = (60, 40, 20)

random.seed(42)
for _ in range(150):
    x, y, r = random.randint(0,W-1), random.randint(0,H-1), random.randint(1,3)
    a = random.randint(40, 180)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(255,255,255,a))

def dt(x, y, t, f, c, a='lt'):
    bb = draw.textbbox((0,0), t, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    if a == 'c': draw.text((x-tw//2, y), t, fill=c, font=f)
    elif a == 'r': draw.text((x-tw, y), t, fill=c, font=f)
    else: draw.text((x, y), t, fill=c, font=f)

dt(W//2, 110, '星河智善生活集团 x 人力行政中心', sf, (180,150,90), 'c')
dt(W//2, 200, '2026\u5e74\u7b2c\u4e8c\u671f', tf, G, 'c')
dt(W//2, 290, '\u65b0\u5458\u5de5\u5165\u804c\u57f9\u8bad', nf, WHT, 'c')
dt(W//2, 350, '\u51dd\u661f\u6cb3\u4e4b\u529b \u00b7 \u542f\u667a\u5584\u65b0\u7a0b', sf, D, 'c')

# Meeting banner
for y in range(410, 530):
    for x in range(60, W-60):
        draw.point((x,y), fill=(40,30,15))

dt(W//2, 445, '\u57f9\u8bad\u65b9\u5f0f\uff1a\u817e\u8baf\u4f1a\u8bae', mf, (150,130,100), 'c')
dt(W//2, 495, '576-553-473', tf, G, 'c')

dt(60, 580, '\u57f9\u8bad\u8bae\u7a0b', nf, G, 'lt')

sl = [
    ('14:10-15:00', '\u516c\u53f8\u53d1\u5c55\u5386\u7a0b\u53ca\u4f01\u4e1a\u6587\u5316', '\u9093\u6c38\u6e56'),
    ('15:10-15:50', '\u5b89\u5168\u4fe1\u606f\u4e0e\u529e\u516c\u63d0\u6548', '\u53f2\u4e1c'),
    ('15:50-16:30', '\u54c1\u724c\u5ba3\u4f20\u3001\u793e\u533a\u6587\u5316\u3001\u8206\u60c5\u5904\u7f6e\u5b9e\u64cd\u57f9\u8bad', '\u5f20\u82b1\u4eae'),
    ('16:40-17:30', '\u5ec9\u6d01\u4ece\u4e1a\u53ca\u7ea2\u9ec4\u7ebf\u6807\u51c6', '\u8c22\u5764\uff08\u63a7\u80a1\uff09'),
    ('17:30-18:00', '\u8bad\u540e\u7edf\u4e00\u95ed\u5377\u8003\u8bd5', '\u95ef\u5173\u7cfb\u7edf\u5b8c\u6210'),
]

for i, (tm, tt, lec) in enumerate(sl):
    y = 640 + i * 150
    for cy in range(y, y+130):
        for cx in range(60, W-60):
            b = (cx < 62 or cx > W-62 or cy < y+2 or cy > y+128)
            if b: draw.point((cx,cy), fill=GL)
            else: draw.point((cx,cy), fill=(25,20,50))
    dt(80, y+15, f'\u7b2c{i+1}\u8bfe', sf, (80,200,140), 'lt')
    dt(W-80, y+15, tm, sf, D, 'r')
    dt(80, y+55, tt, mf, WHT, 'lt')
    dt(80, y+95, f'\u8bb2\u5e08\uff1a{lec}', sf, D, 'lt')

fy = 640 + 5*150 + 60
dt(W//2, fy, '\u95ef\u5173\u6d41\u7a0b\uff1a\u7b7e\u5230 \u2192 \u542c\u8bfe \u2192 \u8bc4\u4f30 \u2192 \u8003\u8bd5 \u2192 \u8bc1\u4e66', sf, (180,150,90), 'c')

dt(W//2, H-120, '\u661f\u6cb3\u667a\u5584\u751f\u6d3b\u96c6\u56e2 \u00b7 \u4eba\u529b\u884c\u653f\u4e2d\u5fc3', xf, D, 'c')
dt(W//2, H-80, '2026\u5e746\u6708', xf, (60,60,80), 'c')

img.save('poster.png', 'PNG')
print('Saved: poster.png -', os.path.getsize('poster.png')//1024, 'KB')
