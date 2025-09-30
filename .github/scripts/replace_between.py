import sys, io

path, start, end, new = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
text = io.open(path, "r", encoding="utf-8").read()
s = text.find(start)
e = text.find(end)
if s == -1 or e == -1 or e < s:
    print("Marker not found.")
    sys.exit(1)

before = text[:s + len(start)]
after  = text[e:]
mid = "\n" + new.strip() + "\n"
io.open(path, "w", encoding="utf-8").write(before + mid + after)
print("Replaced between markers.")