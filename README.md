# Arnan Srivastava - Maker's portfolio

Static site. No build step, no dependencies.

## Files
- `index.html` - all content, three sections (FRC, 3D prints, Miscellaneous)
- `style.css` - gradient background, frame, card and panel styling
- `images/` - drop project photos here; see `images/README.txt` for exact filenames expected

## Replacing placeholder content
Every description currently reading `[Replace: ...]` is a placeholder. Open `index.html` in any text editor, find the text, and replace it directly - each is inside a `<p class="desc">` tag tied to one project card.

## Adding images
Each card has an `<img>` pointed at a specific filename in `images/`. If the file isn't there, the card falls back to a text label automatically - nothing breaks. Add files using the exact names listed in `images/README.txt` and they appear with no HTML edits needed. Recommended: square or 4:3 images, at least 800px wide, under 500KB each (resize/compress before adding - GitHub Pages has no size limit itself, but large images slow the page).

## Deploying to GitHub Pages
1. Create a new repository on GitHub (public, or private if you have GitHub Pro).
2. Push these three items (`index.html`, `style.css`, `images/`) to the repository root - do not nest them in a subfolder unless you configure Pages for that path.
3. In the repository, go to Settings → Pages.
4. Under "Build and deployment", set Source to "Deploy from a branch", branch to `main` (or `master`), folder to `/ (root)`.
5. Save. GitHub gives a URL in the form `https://<username>.github.io/<repo-name>/` within a minute or two.
6. Optional: add a custom domain in the same Settings → Pages panel once the site is live.

Command-line push, if starting from this folder:
```
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```
