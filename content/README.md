# Adding/editing projects

Each project is a markdown file in here, under `content/frc/`,
`content/3d-prints/`, or `content/misc/`. To add a new project:

1. Create `content/<category>/<slug>.md`. `<slug>` becomes the filename of
   the generated page, e.g. `content/3d-prints/phone-stand.md` ->
   `projects/phone-stand.html`.
2. Fill in the frontmatter and description - see `build.py`'s top comment
   for the full field list (title, category, order, subgroup, progression,
   image, custom).
3. If you used an image, put the file in `/images`.
4. From the repo root, run:
   ```
   python3 build.py
   ```
   This regenerates the three hub pages (frc.html, 3d-prints.html,
   misc.html) and any non-"custom" project page.
5. Commit and push.

To edit an existing simple project, just edit its `.md` file and re-run
`build.py`. For a project marked `custom: true` in its frontmatter, the
`.md` file's title/image still drive its card on the hub page, but you
edit `projects/<slug>.html` directly for its actual content - build.py
won't touch that file.

The homepage (`index.html`) is still hand-written, not generated - it's
short and rarely changes.
