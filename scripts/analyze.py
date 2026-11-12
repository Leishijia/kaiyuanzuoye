import json, collections, os, sys

p = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Lei\WorkBuddy\2026-10-29-13-31-13\scan\scan.json"
d = json.load(open(p, encoding="utf-8"))
files = d.get("files", [])
print("scancode header:", json.dumps({k: d[k] for k in ("scancode_version", "scancode_notice") if k in d}, ensure_ascii=False)[:300])

total = len(files)
print("total entries:", total)

lic_expr = collections.Counter()
lic_keys = collections.Counter()
no_lic = []
no_lic_by_ext = collections.Counter()
score_buckets = collections.Counter()
multi = []
copy_holders = collections.Counter()
has_copy = 0
by_top = collections.Counter()
detected = 0
unknown_or_other = []

for f in files:
    path = f.get("path", "")
    rel = path.split("commons-lang3-3.21.0-src", 1)[-1].lstrip("/\\")
    top = rel.split("/")[0].split("\\")[0] if rel else ""
    by_top[top] += 1
    ex = os.path.splitext(path)[1].lower() or "(none)"
    dets = f.get("license_detections") or []
    if not dets:
        no_lic.append(rel)
        no_lic_by_ext[ex] += 1
    else:
        detected += 1
        if len(dets) > 1:
            multi.append(rel)
        for det in dets:
            expr = det.get("license_expression")
            lic_expr[expr] += 1
            for m in det.get("matches", []):
                score_buckets[int(m.get("score", 0))] += 1
    for l in (f.get("licenses") or []):
        lic_keys[l.get("key")] += 1
    cs = f.get("copyrights") or []
    if cs:
        has_copy += 1
        for c in cs:
            copy_holders[(c.get("copyright") or "").strip()] += 1

print("\n-- files with >=1 license detection:", detected)
print("-- files with NO license detection:", total - detected)
print("\n-- license_expression counter (top 15):")
for k, v in lic_expr.most_common(15):
    print(f"   {v:5d}  {k}")
print("\n-- license keys (top 15):")
for k, v in lic_keys.most_common(15):
    print(f"   {v:5d}  {k}")
print("\n-- match score distribution:")
for k in sorted(score_buckets):
    print(f"   score {k:3d}: {score_buckets[k]}")
print("\n-- no-license files by extension:", dict(no_lic_by_ext.most_common(12)))
print("\n-- no-license sample (first 25):")
for r in no_lic[:25]:
    print("   ", r)
print("\n-- files with multiple detections:", len(multi))
for r in multi[:15]:
    print("   ", r)
print("\n-- files with copyrights:", has_copy)
print("-- distinct copyright strings:", len(copy_holders))
for k, v in copy_holders.most_common(8):
    print(f"   {v:5d}  {k[:90]}")
print("\n-- top-level dirs:", dict(by_top.most_common(8)))
pkgs = []
for f in files:
    for pk in (f.get("package_data") or []):
        pkgs.append((pk.get("type"), pk.get("name"), pk.get("version"), pk.get("primary_language"), pk.get("purl")))
print("\n-- packages detected:", len(pkgs))
for x in pkgs[:5]:
    print("   ", x)
