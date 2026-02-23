---
name: elementor
description: "Elementor page builder workflows for WordPress. Use when: (1) building or editing pages with Elementor (containers/widgets), (2) troubleshooting Elementor issues (editor not loading, styling not applying, responsive bugs), (3) improving Elementor performance (reduce DOM, optimize CSS/JS, fonts/icons), (4) managing templates (Theme Builder headers/footers, popups, global widgets), (5) compatibility debugging with themes/plugins, (6) migrating/duplicating Elementor pages/templates safely. NOT for: non-WordPress sites, pure SEO strategy (use seo), server provisioning (use hosting tools), or general WordPress tasks unrelated to Elementor (use wordpress)."
---

# Elementor Skill

Elementor-specific guidance: build, debug, and optimize Elementor sites without breaking production.

## Quick start (triage questions)

1) What versions?
- WordPress version
- Elementor + (optional) Elementor Pro versions
- Theme name/version (and child theme?)

2) Where is the problem?
- Elementor editor (backend) vs frontend
- One page/template vs site-wide
- Desktop vs tablet vs mobile

3) Any recent changes?
- Plugin/theme updates
- New caching/minification
- CDN/Cloudflare changes

## Canonical workflow

### 1) Collect the minimum facts
- Does the site use **Containers (Flexbox)** or legacy **Sections/Columns**?
- Is **Theme Builder** in play (header/footer/single templates)?
- Is the problem reproducible with all caching disabled?

### 2) Reproduce safely
- Test logged-out (incognito) and logged-in.
- Test with cache bypass:
  - Clear plugin cache + server cache + CDN cache
  - Disable minify/combine/defer temporarily (especially for `elementor-frontend` scripts)

### 3) Fix, then lock in
- Apply the smallest change that fixes it.
- Re-enable caches one by one.
- Document the setting/plugin responsible.

## Troubleshooting playbook

### Editor won’t load / stuck on loading
Likely causes:
- JS error from another plugin/theme
- Memory limit too low
- Caching/minification breaking editor assets

Steps:
- Check browser console for JS errors.
- Temporarily disable:
  - JS combine/minify/defer
  - Optimization plugins affecting JS (Autoptimize, WP Rocket settings, etc.)
- Switch to a default theme briefly (staging) to isolate theme conflicts.
- Raise PHP memory limit if constrained.

### Styles not applying / changes not showing
- Clear Elementor-generated CSS:
  - Elementor → Tools → Regenerate CSS & Data
- Clear all caches (plugin/server/CDN) and test logged-out.
- Check if “CSS Print Method” and “Improved Asset Loading” settings are causing mismatch.
- Ensure critical CSS tooling isn’t freezing old styles.

### Responsive issues (tablet/mobile)
- Confirm breakpoints and whether custom breakpoints are enabled.
- Look for:
  - Fixed pixel widths
  - Negative margins
  - Absolute positioning
  - Overflow hidden on parent containers
- Prefer container + gap/flex settings over manual spacing hacks.

### Theme Builder conflicts (header/footer not showing)
- Verify display conditions for templates.
- Check for competing header/footer systems (theme header builder, another plugin).
- Ensure only one active template targets the same conditions.

### Performance problems (slow pages, poor INP/LCP)
Common Elementor pain points:
- DOM bloat (too many nested containers/widgets)
- Too many widgets above the fold
- Heavy sliders, popups, motion effects
- Third-party scripts (chat, analytics, heatmaps)

Actions:
- Reduce nesting; use containers intelligently.
- Limit motion effects and entrance animations.
- Prefer system fonts or self-hosted fonts with proper `font-display`.
- Disable unused icon libraries if possible.
- Audit plugins that add frontend assets everywhere.

## Safe migration / duplication

- Prefer Elementor template export/import for templates.
- When moving a page between sites:
  - Ensure matching theme + plugin stack (or expect styling differences)
  - Rebuild global styles and fonts
- After migration: regenerate CSS & data and clear caches.

## Guardrails

- Recommend staging for theme builder edits and large redesigns.
- Don’t “fix” by disabling security plugins or editing core plugin files.
- Avoid piling on multiple optimization plugins with overlapping JS/CSS pipelines.

## Helpful references (external)

- Elementor docs: https://elementor.com/help/
- Elementor developer docs: https://developers.elementor.com/
