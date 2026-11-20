# TekMG (tekmg.com)

Python/Flask version of tekmg.com, hosted on Render.

- `app.py` - routes
- `pages/` - page files
- `public/` - css, assets, images, favicon (served from the site root)
- Build: `pip install -r requirements.txt` / Start: `gunicorn app:app`

Still to copy from the old GoDaddy site into `public/`: `assets/`, `Sony/Sony-Camcorder/Images/`, `s/` (fonts), `favicon.ico`, `sitemap.xml`.
