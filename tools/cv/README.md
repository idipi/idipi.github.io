# CV

The CV is generated from Python source and published with the Astro site as
`/cv.pdf`.

## Files

- `cv_data.py` - all resume text (edit this to update content)
- `build_cv.py` - layout engine (fonts, sizes, colors, spacing). Don't need to
  touch this unless you're changing the design.
- `requirements.txt` - pinned `reportlab` version

## Local build

From the repository root:

```
npm run setup:cv
npm run build:cv
```

This writes `public/cv.pdf`, which Astro copies to `dist/cv.pdf` during
`npm run build`.

For production-grade typography, install Liberation Sans locally:

```
sudo apt install fonts-liberation
```

On macOS, use any package source that installs `LiberationSans-Regular.ttf`,
`LiberationSans-Bold.ttf`, and `LiberationSans-Italic.ttf` into one of the
standard font directories. Without Liberation Sans, the script falls back to
Helvetica so local builds still work.

## GitHub Actions

The main CI workflow builds the CV first and uploads it as an artifact. The
site build depends on that job, downloads `cv.pdf` into `public/`, and only then
builds the static Astro site for GitHub Pages.

## Fidelity note

This was reconstructed from the original PDF (`cv.pdf`, ReportLab-generated,
LinkedIn link removed) by extracting its content stream: fonts (Liberation
Sans), exact point sizes, RGB colors, margins (51.35pt), and paragraph
justification settings. It uses the same rendering engine (ReportLab) and the
same fonts, so headings, colors, and overall proportions match closely.

It is **not a byte-for-byte replica**. Two things prevented that:

1. The original's bullet/dash/apostrophe characters were remapped to custom
   single-byte codes during font subsetting - the actual glyphs turned out to
   be ordinary "•", "–", "'" (confirmed by cross-checking glyph widths against
   the embedded font's `/Widths` array), but a few line-wrap points differ by
   a word here and there as a result.
2. Vertical spacing between blocks (bullet-to-bullet, section-to-section) is
   set to clean, consistent values here, rather than reproducing the original
   file's slightly irregular gaps line-by-line.

Side-by-side the two are effectively indistinguishable at normal reading
size. If you need exact pixel parity with the original file specifically,
keep using that PDF as-is (with the LinkedIn line already stripped) - this
pipeline is for going forward, when you next need to edit and regenerate it.
