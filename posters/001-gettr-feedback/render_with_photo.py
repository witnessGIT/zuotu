from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import textwrap

W, H = 1080, 1440
root = Path(__file__).resolve().parent
src = root / 'assets' / 'guo-selected-default_1.286.1.jpg'
out = root / 'poster-photo-test.png'

def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def fit_cover(im, box):
    return ImageOps.fit(im, box, method=Image.Resampling.LANCZOS, centering=(0.52, 0.50))

def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

bg = Image.new('RGB', (W, H), '#0b0d10')
photo = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
# Photo occupies right side and extends behind copy as a real photographic background.
crop = fit_cover(photo, (760, H))
bg.paste(crop, (320, 0))

# Strong editorial overlays keep Chinese text crisp while retaining the subject.
ov = Image.new('RGBA', (W, H), (0,0,0,0))
od = ImageDraw.Draw(ov)
for x in range(W):
    if x < 610:
        a = int(238 - 40 * (x / 610))
    else:
        a = int(max(25, 198 - (x-610) * 0.40))
    od.line((x,0,x,H), fill=(7,9,12,max(0,min(245,a))))
od.rectangle((0, 0, W, 210), fill=(0,0,0,48))
od.rectangle((0, H-220, W, H), fill=(0,0,0,120))
bg = Image.alpha_composite(bg.convert('RGBA'), ov)
d = ImageDraw.Draw(bg)

RED = '#e33a2e'
CREAM = '#f4f0e7'
MUTED = '#c9c7c1'
WHITE = '#ffffff'

# top label
d.rectangle((72, 70, 238, 77), fill=RED)
d.text((72, 96), 'GETTR · 战友作品反馈', font=font(27, True), fill=CREAM)

d.text((72, 176), '郭先生来电', font=font(42, True), fill=WHITE)
d.text((72, 240), '“非常非常', font=font(92, True), fill=WHITE)
d.text((72, 342), '震撼”', font=font(112, True), fill=RED)

lead = '郭先生今天打来电话，对昨天的 GETTR 活动节目表示非常非常震撼，并对多档节目与作品给出反馈。'
# wrap by approximate CJK character count
lines = textwrap.wrap(lead, width=21)
y = 500
for line in lines:
    d.text((76, y), line, font=font(30), fill=CREAM)
    y += 49

rounded_rect(d, (72, 690, 665, 805), 18, fill=(227,58,46,230))
d.text((102, 714), '“战友们做得都', font=font(34, True), fill=WHITE)
d.text((102, 758), '非常非常好”', font=font(42, True), fill=WHITE)

items = [
    'Hpay《为自由而生》', '盘古先生的节目', '避风港第 639 期节目',
    'Q-May 音乐《女猫王的故事》', '台湾农场 8 月 15 日大街访', 'Rica 8 月 28 日节目',
    '意大利农场 8 月 31 日节目', '上海农场 8 月 29 日「经济孤岛」',
    '纽约磐石农场第 112 期', '华盛顿自由农场第 118 期', '英国伦敦阳光农场第 152 期'
]
y = 855
for i, item in enumerate(items, 1):
    num = f'{i:02d}'
    d.text((76, y), num, font=font(22, True), fill=RED)
    d.text((124, y-1), item, font=font(24, True if i in (1,4) else False), fill=WHITE)
    d.line((76, y+37, 650, y+37), fill=(255,255,255,42), width=1)
    y += 47

d.text((72, 1370), 'GETTR · FEEDBACK  /  TEST 001', font=font(18, True), fill=MUTED)
d.text((740, 1370), 'PHOTO: MEGA LIBRARY', font=font(17, True), fill=MUTED)

bg.convert('RGB').save(out, 'PNG', optimize=True)
print(out)
