#!/usr/bin/env python3
"""
build.py - regenerates the FRC / 3D prints / Misc hub pages, and any
"simple" project detail page, from the markdown files in content/.

HOW TO ADD A NEW PROJECT:
  1. Create a new file in content/<category>/<slug>.md, where <category>
     is one of: frc, 3d-prints, misc, and <slug> matches the filename you
     want for the page (e.g. content/3d-prints/phone-stand.md -> projects/phone-stand.html).
  2. Add frontmatter between the --- lines at the top:
       title: "Phone stand"       (required)
       category: 3d-prints        (required - must match the folder)
       order: 7                   (optional - controls sort position on the hub page, lower = earlier)
       subgroup: "Other"          (optional - FRC-only grouping header, e.g. "5667 bots")
       progression: true          (optional - FRC-only, puts the card in the arrow-linked
                                    "Bot progression" row instead of the normal grid)
       image: phone-stand.png     (optional - filename inside /images, used as the card
                                    thumbnail and the detail page's header image)
       custom: true               (optional - see "CUSTOM PAGES" below)
       featured: true             (optional - pulls this project OUT of its category hub
                                    page grid entirely, because it's instead hand-linked
                                    near the top of index.html. The detail page itself is
                                    still generated normally and still back-links to its
                                    category hub. See the "EDIT: featured project links"
                                    block in index.html to add/remove/reorder these.)
  3. Below the second --- line, write the project description as plain text
     or simple markdown (**bold**, [links](url), blank-line-separated paragraphs).
  4. Put the actual image file in /images if you used one.
  5. Run:  python3 build.py
     This regenerates frc.html, 3d-prints.html, misc.html, and (for any
     non-custom entry) projects/<slug>.html.
  6. Commit + push the changed files (content/, the hub .html files,
     projects/<slug>.html, and images/ if you added one).

CUSTOM PAGES:
  Some project pages have one-off features this script doesn't know how to
  generate - image galleries, before/after sliders, embedded slideshows,
  extra sections, etc. Those are marked `custom: true` in their .md file.
  For a custom page: this script still uses the .md file's title/image to
  render that project's CARD on the hub page, but it leaves the actual
  projects/<slug>.html file alone - edit that HTML file by hand for changes
  to its content, gallery, etc. Set `custom: true` on a new project too if
  you're hand-building something fancier than title + description + one image.
"""
import os
import re
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
PROJECTS = os.path.join(ROOT, "projects")

HUB_TITLES = {
    "frc": ("FRC", "Things made for the FIRST Robotics Competition community or my team."),
    "3d-prints": ("3D prints", "Small prints and gifts for myself, family, and friends."),
    "misc": ("Miscellaneous", "Side projects unrelated to everything else."),
}

BACK_LABEL = {
    "frc": "Back to FRC",
    "3d-prints": "Back to 3D prints",
    "misc": "Back to Miscellaneous",
}


def parse_md(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: missing frontmatter")
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"')
        if val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        elif re.match(r"^-?\d+$", val):
            val = int(val)
        fm[key] = val
    return fm, body.strip()


def load_all():
    entries = {"frc": [], "3d-prints": [], "misc": []}
    for cat in entries:
        cat_dir = os.path.join(CONTENT, cat)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".md"):
                continue
            slug = fname[:-3]
            fm, body = parse_md(os.path.join(cat_dir, fname))
            fm["slug"] = slug
            fm["body"] = body
            entries[cat].append(fm)
        entries[cat].sort(key=lambda e: e.get("order", 999))
    return entries


def card_html(e):
    slug = e["slug"]
    title = e["title"]
    img = e.get("image")
    if img:
        img_tag = (
            f'<img src="images/{img}" alt="{title}" loading="lazy" '
            "onerror=\"this.style.display='none'; "
            "this.nextElementSibling.style.display='flex';\">"
        )
    else:
        img_tag = ""
    return (
        f'<a class="card" href="projects/{slug}.html"><div class="thumb">{img_tag}'
        f'<span class="thumb-fallback">{title}</span></div><h4>{title}</h4></a>'
    )


def build_hub(cat, entries):
    title, note = HUB_TITLES[cat]
    entries = [e for e in entries if not e.get("featured")]
    progression = [e for e in entries if e.get("progression")]
    rest = [e for e in entries if not e.get("progression")]

    body_parts = []
    if progression:
        body_parts.append('<h3 class="subgroup">Bot progression</h3>')
        body_parts.append('<div class="progression-row">')
        for i, e in enumerate(progression):
            body_parts.append(card_html(e))
            if i != len(progression) - 1:
                body_parts.append('<div class="arrow">&rarr;</div>')
        body_parts.append("</div>")

    # group "rest" by subgroup, preserving first-seen order
    groups = []
    seen = {}
    for e in rest:
        sg = e.get("subgroup")
        if sg not in seen:
            seen[sg] = []
            groups.append((sg, seen[sg]))
        seen[sg].append(e)

    for sg, items in groups:
        if sg:
            body_parts.append(f'<h3 class="subgroup">{sg}</h3>')
        body_parts.append('<div class="card-grid">')
        for e in items:
            body_parts.append(card_html(e))
        body_parts.append("</div>")

    cards_html = "\n    ".join(body_parts)

    return f"""<!DOCTYPE html>
<!-- GENERATED by build.py from content/{cat}/*.md - do not hand-edit the
     card grid below; edit the .md files and re-run build.py instead.
     Hand-editing is fine above/below the GENERATED markers if you add any. -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Arnan Srivastava</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=7">
</head>
<body>
<img class="hub-bg" src="images/bg-milkyway.jpg" alt="">
<div class="site-frame">
  <div class="hub-frame">
    <a class="hub-back" href="index.html">&larr; Back</a>
    <h2>{title}</h2>
    <p class="category-note">{note}</p>

    {cards_html}

    <footer>
      &copy; <span id="year"></span> Arnan Srivastava
      <p class="hub-credit">Credit &amp; Copyright: Rogelio Bernal Andreo (Deep Sky Colors)</p>
    </footer>
  </div>
</div>
<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
</body>
</html>
"""


def build_detail(cat, e):
    slug = e["slug"]
    title = e["title"]
    img = e.get("image")
    desc_html = markdown.markdown(e["body"])
    # tag paragraphs/headings with our CSS classes
    desc_html = desc_html.replace("<p>", '<p class="desc detail-desc">')
    desc_html = desc_html.replace("<h2>", '<h2 class="detail-subhead">')

    if img:
        gallery_html = (
            f'<h2 class="detail-subhead">Gallery</h2>\n'
            f'  <div class="gallery" id="{slug.replace("-", "_")}-gallery">\n'
            f'    <img src="../images/{img}" alt="{title}">\n'
            "  </div>"
        )
    else:
        gallery_html = ""

    # EDIT: a `featured: true` project is hand-linked from index.html instead
    # of living on its category hub page's grid (see build_hub), so its
    # back-link should return there too, not to a hub page it's no longer
    # listed on.
    if e.get("featured"):
        back_href = "../index.html"
        back_label = "&larr; Back"
    else:
        back_href = f"../{cat}.html"
        back_label = f"&larr; {BACK_LABEL[cat]}"

    return f"""<!DOCTYPE html>
<!-- GENERATED by build.py from content/{cat}/{slug}.md - do not hand-edit;
     edit that .md file and re-run build.py instead. If you need something
     this template can't do (multi-image gallery, extra sections, etc.), add
     `custom: true` to the .md frontmatter and hand-write this file instead -
     build.py will then leave it alone. Note: the project's image sits in the
     gallery near the bottom of the page, not as a header at the top. -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Arnan Srivastava</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css?v=7">
</head>
<body>
<img class="detail-bg" src="../images/bg-eclipse.jpg" alt="">
<div class="site-frame detail-frame">
  <a class="back-link" href="{back_href}">{back_label}</a>
  <h1>{title}</h1>
  {desc_html}
  {gallery_html}
  <p class="detail-credit">Credit &amp; Copyright: Reinhold Wittich</p>
</div>
</body>
</html>
"""


def main():
    entries = load_all()

    for cat, items in entries.items():
        hub_path = os.path.join(ROOT, f"{cat}.html")
        with open(hub_path, "w", encoding="utf-8") as f:
            f.write(build_hub(cat, items))
        print(f"wrote {cat}.html  ({len(items)} cards)")

        for e in items:
            if e.get("custom"):
                continue
            out_path = os.path.join(PROJECTS, f"{e['slug']}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(build_detail(cat, e))
            print(f"  wrote projects/{e['slug']}.html")


if __name__ == "__main__":
    main()
