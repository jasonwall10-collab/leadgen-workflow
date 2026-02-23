# Performance + Core Web Vitals (WP-focused)

Core metrics (field data targets):
- **LCP** <= 2.5s
- **INP** <= 200ms
- **CLS** <= 0.1

Common WordPress wins:

## LCP (largest element loads late)
- Serve properly-sized images + WebP (already used on Charge Wise).
- Preload hero image and key fonts.
- Minimize render-blocking CSS; generate critical CSS.
- Reduce heavy sliders/video backgrounds above the fold.

## INP (site feels sluggish)
- Reduce JS (page builder widgets, analytics tags, chat widgets).
- Defer non-critical scripts.
- Limit third-party scripts.

## CLS (layout jumps)
- Set width/height for images and embeds.
- Avoid injecting banners above content after load.

Tooling suggestions (when access is available):
- PageSpeed Insights / Lighthouse
- Search Console Core Web Vitals report

Source: https://web.dev/vitals/
