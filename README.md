# TekMG – fixed pages

Static copies of the Tek Media Group pages with speed and bug fixes:

- `aboutUs.aspx.html`
- `Camcorder-Camera-And-Deck-Repair.aspx.html`
- `contact.html` / `contact.aspx.html`
- `css` (self-hosted Google Fonts, now with `font-display: swap`)

## Missing: site assets

The pages reference the site's existing files, which are not in this repo yet:
`assets/` (Bootstrap, layout CSS, scripts, images, logo), `Sony/Sony-Camcorder/Images/`,
`s/` (font files) and `favicon.ico`. Copy those folders from the live server into the
repo root and the pages will render fully styled.

## Deploy on Render

New > Blueprint > pick this repo. Render reads `render.yaml` (static site, no build).
Every push to `main` redeploys.
