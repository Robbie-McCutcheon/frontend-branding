FrontEndWorkshop — Branding sample

This workspace contains a small professional branding page (a single static HTML page) used for the FrontEndWorkshop assignment.

What I changed in this assignment

- Restructured `index.html` into semantic sections (header, main, footer).
- Added a modern, responsive `style.css` for a clean brand presentation.
- Added `generate_pdf.py` — a tiny dependency-free Python script that writes a simple `branding_page.pdf` snapshot.

Publish to GitHub

1. Create a new repository on GitHub (via the website) named e.g. `frontend-branding`.
2. From this project root run:

```bash
git init
git add .
git commit -m "Branding page for FrontEndWorkshop"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

3. After pushing, edit `index.html` and replace the GitHub placeholder URLs (the `View on GitHub` link and the `Repository` text in Contact) with your real repository URL.

Generate the PDF snapshot
Run the included script to produce `branding_page.pdf` in the project root:

```bash
python3 generate_pdf.py
# -> branding_page.pdf
```

Notes and how to improve

- The generated PDF is a simple text snapshot intended to give you an immediate PDF file without external dependencies. For pixel-perfect (CSS-rendered) PDFs, use a headless browser (Puppeteer) or `wkhtmltopdf`.
- After publishing to GitHub, you can also enable GitHub Pages in the repository settings to publish the static site and link that URL on the page.
