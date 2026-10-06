# Publish to GitHub Pages (Step 6)

Local preview (already works):

```bash
cd "/Users/yuenyue/Desktop/Life_Server/Knowledge/Academic/FIT3179/Ass 22"
python3 -m http.server 8765
```

Open http://127.0.0.1:8765/

---

## A. Create the GitHub repo and push

This folder is **not** a git repo yet. From Terminal:

```bash
cd "/Users/yuenyue/Desktop/Life_Server/Knowledge/Academic/FIT3179/Ass 22"

git init
git add index.html css js specs data AI_ACKNOWLEDGEMENT.txt ASSIGNMENT_WRITEUP.md PLAN.md Topic.rtf .gitignore .nojekyll scripts
git status   # confirm data/_raw, .venv, PDFs, Course Note are NOT staged

git commit -m "$(cat <<'EOF'
Publish FIT3179 DV2 volunteering visualisation for GitHub Pages.

EOF
)"
```

Create a **public** GitHub repository (required for free GitHub Pages), then:

```bash
# Replace YOUR_GITHUB_USERNAME and REPO_NAME
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/REPO_NAME.git
git push -u origin main
```

Or with GitHub CLI (if logged in):

```bash
gh repo create REPO_NAME --public --source=. --remote=origin --push
```

**Do not** force-push. **Do not** commit secrets.

---

## B. Turn on GitHub Pages

1. On GitHub: **Settings → Pages**
2. **Build and deployment → Source:** Deploy from a branch
3. **Branch:** `main` · **Folder:** `/ (root)`
4. Save. Wait 1–2 minutes.

Your live URL will be one of:

- `https://YOUR_GITHUB_USERNAME.github.io/REPO_NAME/`
- or `https://YOUR_GITHUB_USERNAME.github.io/` if the repo is named `YOUR_GITHUB_USERNAME.github.io`

5. Open the URL in an **incognito** window. Confirm all 12 charts load (they need `http(s)`, not `file://`).

---

## C. After the URL works — tell me / update Moodle docs

1. Paste the live URL into `ASSIGNMENT_WRITEUP.md` **Part A** (replace the TODO).
2. Take a **full-page screenshot** of the live site for **Part D** (browser full-page capture, or scroll-stitch).
3. Upload your **existing sketch** PDF to the same repo (e.g. `sketch/sketch.pdf`) and put that raw/GitHub URL in Moodle Part C — do not invent a new sketch.

Optional: message me the live URL and I can fill Part A in `ASSIGNMENT_WRITEUP.md` for you.

---

## D. What to paste into Moodle

| Moodle item | What to paste |
| --- | --- |
| Part A — Visualisation URL | Live GitHub Pages URL (test in incognito) |
| Part C — Sketch URL | URL to **your** existing sketch PDF on GitHub |
| Part C — Sketch screenshot | Clear screenshot of your sketch |
| Part D — Full-size screenshot | Full-page screenshot of the **live** visualisation |
| Part B — Domain description | Contents of `ASSIGNMENT_WRITEUP.md` Part B (or upload/paste as required) |
| Name / Student ID / Studio | Fill the table at the top of `ASSIGNMENT_WRITEUP.md` |

Also replace `[Your name]` in `index.html` footer before submit.
