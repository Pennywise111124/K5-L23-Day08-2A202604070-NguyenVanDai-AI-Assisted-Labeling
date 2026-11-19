import sys, json, collections
sys.path.insert(0, "scripts")
from pathlib import Path
import review_stats as rs
tax = rs.load_taxonomy()
pre = rs.load_coco(Path("submission/prelabel/pre_traps.coco.json"))
fin = rs.load_coco(Path("submission/labels/batch_reviewed.json"))
key = json.loads(Path("submission/prelabel/traps_key.json").read_text(encoding="utf-8-sig"))["traps"]
tb = collections.defaultdict(list)
for t in key:
    for f in ("orig_box", "fake_box", "box", "bad_box"):
        if t.get(f):
            b = t[f]; tb[t["image"]].append((b[0], b[1], b[0]+b[2], b[1]+b[3]))
near = lambda o, n: any(rs.box_iou(o.box, x) >= 0.3 for x in tb.get(n, []))
kept, dele = [], []
for n in sorted(fin.images):
    P, _ = rs.split_ignore(tax, pre.objects[n]); F, _ = rs.split_ignore(tax, fin.objects[n])
    if tb.get(n):
        P = [o for o in P if not near(o, n)]; F = [o for o in F if not near(o, n)]
    pairs, up, _ = rs.match_objects(P, F, fin.images[n], 0.5, False, same_class=True)
    kept += [(round(a.score, 2), n) for a, b, v in pairs if a.cls == "three_wheeler"]
    dele += [(round(o.score, 2), n) for o in up if o.cls == "three_wheeler"]
print("giữ", len(kept), "| xoá", len(dele))
for t in (0.15, 0.25, 0.5):
    print(t, "giữ đúng", sum(s >= t for s, _ in kept), "| box thừa còn", sum(s >= t for s, _ in dele))
print("xoá với điểm >= 0.5:", sorted(d for d in dele if d[0] >= 0.5))