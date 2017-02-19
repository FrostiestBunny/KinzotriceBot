import os
import re
import pickle

files = []

for path, name, filename in os.walk("logs"):
    for f in filename:
        files.append(os.path.join(path, f))

result = []
for f in files:
    with open(f, mode="r", encoding="utf-8") as fo:
        pattern = re.compile(r"(\[\d{4}-\d{2}-\d{2}(\s\d{2}:\d{2}:\d{2})\])?\s*.*\(.*\):\s*.*", re.I)
        for line in fo:
            match = re.match(pattern, line)
            if match.group(2):
                line = line.replace(match.group(2), "")
            result.append(line)

result = set(result)
result = list(result)

with open("logs.pickle", "wb") as f:
    pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
