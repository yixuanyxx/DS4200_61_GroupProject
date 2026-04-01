# Unboxing the Retail Pulse

DS4200 (**Information Presentation and Data Visualisation**), Group 61.

## Live site (GitHub Pages)

After you turn Pages on (steps below), your project site URL is:

`https://<your-github-username>.github.io/DS4200_61_GroupProject/`

Replace `<your-github-username>` with the account that owns this repo (example: `yixuanyxx`).

### Make this `index.html` show up on that URL

1. Commit and push everything on `main` (including `index.html`, `css/`, `js/`).
2. On GitHub: open the repo **Settings** → **Pages** (left sidebar).
3. Under **Build and deployment** → **Source**, choose **Deploy from a branch**.
4. Branch: **main**, folder: **/ (root)** → **Save**.
5. Wait one or two minutes. Refresh the Pages section; it will show the site URL when ready.
6. Open that URL in a browser. You should see this project page (same as opening `index.html` locally).

GitHub serves `index.html` from the repo root as the homepage for project sites. The empty `.nojekyll` file tells GitHub not to use Jekyll, which avoids weird build issues for a plain HTML site.

## What is in this repo

| File / folder | What it is |
|---------------|------------|
| `index.html` | Main webpage (text + placeholders for charts) |
| `css/style.css` | Basic styling |
| `js/main.js` | Small script; more JS added when D3 is hooked up |
| `Sample - Superstore.csv` | Dataset |

## Who did what

| Person | Main tasks |
|--------|------------|
| Yuansi | Data cleaning, Altair charts |
| Yixuan | Writing for the site, references, summary, design notes |
| Ryan | D3, interactions, putting charts on the page, GitHub Pages |

## Still to do

1. Replace the gray placeholder boxes in `index.html` with the real charts.
2. Make sure there are at least three different interaction types on the site (hover, filter, brush, etc.).
3. Submit the separate design writeup for class if your instructor wants a Word/txt file with the published URL.
