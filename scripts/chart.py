import json
from PIL import Image, ImageDraw, ImageFont

d = json.load(open("scan.json", encoding="utf-8"))
files = [f for f in d["files"] if f["type"] == "file"]
groups = [
    ("Java \u6e90\u7801  (.java)", lambda e: e == ".java"),
    ("\u6784\u5efa/\u914d\u7f6e  (.xml .vm .properties)", lambda e: e in (".xml", ".vm", ".properties", ".policy", ".jacoco", ".html", "")),
    ("\u6587\u6863  (.md .txt)", lambda e: e in (".md", ".txt")),
    ("\u56fe\u50cf/\u8bbe\u8ba1\u7a3f  (.png .xcf)", lambda e: e in (".png", ".xcf")),
    ("\u4e8c\u8fdb\u5236/\u6570\u636e  (.class .json .cgi)", lambda e: e in (".class", ".json", ".cgi")),
]
rows = []
for name, pred in groups:
    tot = det = 0
    for f in files:
        if pred((f.get("extension") or "").lower()):
            tot += 1
            if f.get("detected_license_expression"):
                det += 1
    rows.append((name, tot, det, 100.0 * det / tot if tot else 0.0))

W, H = 1280, 620
img = Image.new("RGB", (W, H), "white")
dr = ImageDraw.Draw(img)
fp = "C:/Windows/Fonts/msyh.ttc"
f_lab = ImageFont.truetype(fp, 23)
f_val = ImageFont.truetype(fp, 23)
f_ax = ImageFont.truetype(fp, 18)
left, right, top, bottom = 430, 150, 30, 66
plot_w = W - left - right
axis_y = H - bottom

dr.line([(left, axis_y), (W - right + 20, axis_y)], fill=(120, 120, 120), width=2)
for pct in (0, 25, 50, 75, 100):
    x = left + plot_w * pct / 100.0
    dr.line([(x, axis_y), (x, axis_y + 7)], fill=(120, 120, 120), width=2)
    w = dr.textlength("%d%%" % pct, font=f_ax)
    dr.text((x - w / 2, axis_y + 12), "%d%%" % pct, font=f_ax, fill=(90, 90, 90))

n = len(rows)
slot = (axis_y - top) / n
for i, (name, tot, det, pct) in enumerate(rows):
    cy = top + slot * (i + 0.5)
    bh = slot * 0.46
    x1 = left + plot_w * pct / 100.0
    color = (47, 111, 184) if pct >= 90 else (222, 132, 62)
    if pct > 0:
        dr.rounded_rectangle([left, cy - bh / 2, max(x1, left + 3), cy + bh / 2], radius=3, fill=color)
    else:
        dr.rectangle([left, cy - 2, left + 3, cy + 2], fill=color)
    w = dr.textlength(name, font=f_lab)
    dr.text((left - 16 - w, cy - 14), name, font=f_lab, fill=(40, 40, 40))
    txt = "%.1f%%  (%d/%d)" % (pct, det, tot)
    tw = dr.textlength(txt, font=f_val)
    if pct >= 35:
        dr.text((x1 - 12 - tw, cy - 14), txt, font=f_val, fill="white")
    else:
        dr.text((x1 + 14, cy - 14), txt, font=f_val, fill=(40, 40, 40))
img.save("fig1_detection_rate.png", dpi=(200, 200))
print("ok", rows)
