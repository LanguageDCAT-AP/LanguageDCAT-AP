from bs4 import BeautifulSoup

# ---- Load files ----
with open("OriginalTable.txt", "r", encoding="utf-8") as f:
    original_html = f.read()

with open("FinalTable.txt", "r", encoding="utf-8") as f:
    final_html = f.read()

orig_soup = BeautifulSoup(original_html, "html.parser")
final_soup = BeautifulSoup(final_html, "html.parser")

# ---- Extract rows from OriginalTable ----
original_rows = orig_soup.find_all("tr")

final_tbody = final_soup.find("tbody")
final_tbody.clear()  # remove placeholder rows

for row in original_rows:
    tds = row.find_all("td")
    if len(tds) < 6:
        continue

    # Property
    prop_link = tds[1].find("a")
    prop_name = prop_link.text.strip()
    prop_href = prop_link["href"]

    # Range
    range_link = tds[2].find("a")
    range_name = range_link.text.strip()
    range_href = range_link["href"]

    # Cardinality
    cardinality = tds[3].text.strip()

    # Definition
    definition = tds[4].text.strip()

    # Usage
    usage = tds[5].text.strip()

    # ---- Build new FinalTable row ----
    new_tr = final_soup.new_tag("tr", id=row.get("id"))

    new_tr.append(BeautifulSoup(
        f'<td><a href="{prop_href}" target="_blank">{prop_name}</a></td>',
        "html.parser"
    ))

    new_tr.append(BeautifulSoup(
        f'<td><a href="{range_href}" target="_blank">{range_name}</a></td>',
        "html.parser"
    ))

    new_tr.append(BeautifulSoup(f"<td>{cardinality}</td>", "html.parser"))
    new_tr.append(BeautifulSoup(f"<td>{definition}</td>", "html.parser"))
    new_tr.append(BeautifulSoup(f"<td>{usage}</td>", "html.parser"))

    # Controlled vocabulary (empty)
    new_tr.append(BeautifulSoup("<td></td>", "html.parser"))

    # Ref and Reuse (empty as requested)
    new_tr.append(BeautifulSoup("<td></td>", "html.parser"))
    new_tr.append(BeautifulSoup("<td></td>", "html.parser"))

    final_tbody.append(new_tr)

# ---- Write output ----
with open("FinalTable_mapped.txt", "w", encoding="utf-8") as f:
    f.write(str(final_soup))

print("✔ FinalTable_mapped.txt generated successfully")
