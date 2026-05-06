import json
import pandas as pd

# Load JSON-LD file
with open("languagedcat-ap.jsonld", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten JSON to just keys (recursively)
def extract_keys(d, prefix=""):
    keys = []
    if isinstance(d, dict):
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(k)
            keys.extend(extract_keys(v, prefix=full_key))
    elif isinstance(d, list):
        for item in d:
            keys.extend(extract_keys(item, prefix=prefix))
    return keys

all_keys = extract_keys(data)

# Separate keys with and without dot
without_dot = [k for k in all_keys if '.' not in k]
with_dot = [k for k in all_keys if '.' in k]

# Create mapping: for each base, find related dotted keys
mapping = []
for base in without_dot:
    related = [w for w in with_dot if w.startswith(base + ".")]
    if related:
        for r in related:
            mapping.append([base, r])
    else:
        mapping.append([base, ""])  # keep empty if no dotted version

# Convert to DataFrame
df = pd.DataFrame(mapping, columns=["Base", "Extended"])

# Save to Excel
df.to_excel("output.xlsx", index=False)

print("Done! Excel file 'output.xlsx' created.")
