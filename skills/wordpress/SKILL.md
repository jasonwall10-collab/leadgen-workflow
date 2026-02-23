---
name: wordpress
description: "WordPress site management, optimization, debugging, and development. Use when: (1) auditing or improving a WordPress site's performance, security, or design, (2) troubleshooting WordPress issues (white screen, plugin conflicts, slow loading, errors), (3) managing WooCommerce stores, (4) optimizing Core Web Vitals for WordPress, (5) reviewing/recommending themes or plugins, (6) WordPress REST API or WP-CLI tasks, (7) migration or backup planning, (8) block editor / Gutenberg / FSE (Full Site Editing) questions. NOT for: non-WordPress CMS platforms, hosting infrastructure setup (use hosting-specific tools), or pure SEO work without WordPress context (use the seo skill)."
---

# WordPress Skill

Practical WordPress guidance — performance, debugging, development, and WooCommerce.

## Current landscape (as of early 2026)

- **WordPress 6.8** (April 2025): refined Style Book, expanded Query Loop controls (sticky posts, sorting), new Query Total block, Cover block resolution controls, Details block name attributes, Gallery lightbox, set Image blocks as featured images, Navigation block improvements, Discord in Social Icons
- **WordPress 6.7** (Nov 2024): PHP 8.0–8.3 support, performance + security improvements
- **Block editor / FSE** is the primary editing paradigm; classic editor is legacy
- **PHP 8.x** is recommended; PHP 7.x is end-of-life

## Elementor (page builder) notes

Elementor is common on client sites and changes the performance + debugging approach.

Use the **elementor** skill when the issue is specifically about Elementor’s editor, widgets, Theme Builder templates (headers/footers/singles), or Elementor-driven performance problems.

Quick Elementor-specific checklist:
- Clear caches (plugin/server/CDN) and test logged-out.
- Elementor → Tools → **Regenerate CSS & Data** after major styling/template changes.
- If the editor won’t load: check browser console for JS errors and temporarily disable JS minify/defer/combine.
- Watch for DOM bloat, heavy sliders/motion effects, and third-party scripts that hurt INP/LCP.

## Audit workflow

### 1) Gather site info
- WordPress version, PHP version, active theme + child theme
- Plugin list (active + inactive)
- Hosting type (shared/VPS/managed/Coolify)
- Caching setup (plugin-based, server-level, CDN)
- Ask for wp-admin access or WP-CLI access if deeper analysis needed

### 2) Performance (Core Web Vitals focus)
See `references/performance.md` for detailed checklist.

Quick wins:
- **LCP**: proper image sizing, WebP/AVIF, lazy load below fold only, preload hero image
- **INP**: defer non-critical JS, reduce DOM size, minimize third-party scripts
- **CLS**: set explicit image/video dimensions, avoid injecting content above fold

WordPress-specific:
- Use a caching plugin (WP Super Cache, W3 Total Cache, LiteSpeed Cache, WP Rocket)
- Enable object caching (Redis/Memcached) if hosting supports it
- Minimize active plugins (audit unused ones)
- Use a lightweight/well-coded theme (GeneratePress, Astra, Kadence, Twenty Twenty-Five)
- Consider a CDN (Cloudflare, BunnyCDN)

### 3) Security
- Keep WordPress core, themes, and plugins updated
- Use strong admin passwords + 2FA
- Disable XML-RPC if not needed
- Limit login attempts (plugin or server-level)
- File permissions: directories 755, files 644, wp-config.php 440
- Security headers (CSP, X-Frame-Options, HSTS)
- Regular backups (UpdraftPlus, BlogVault, or server-level)
- Consider Wordfence or Sucuri for WAF + malware scanning

### 4) Common issues
See `references/troubleshooting.md` for expanded diagnostics.

- **White screen (WSOD)**: enable WP_DEBUG in wp-config.php, check error logs, disable plugins via FTP
- **Slow admin panel**: check for heavy admin-ajax calls, disable heartbeat API frequency, audit plugins
- **Plugin conflicts**: deactivate all, reactivate one by one, check browser console
- **Database bloat**: clean post revisions, transients, spam comments (WP-Optimize)
- **Mixed content**: update URLs after HTTPS migration (Better Search Replace plugin)

### 5) WooCommerce specifics
- Product/category structure for SEO
- Cart/checkout optimization (minimize steps, guest checkout)
- Payment gateway setup
- Order/inventory management
- Shipping zones + methods
- Performance: use HPOS (High-Performance Order Storage), limit dashboard widgets

### 6) Deliverables
- Prioritized issue list with effort estimates (S/M/L)
- Recommended plugin changes (add/remove/replace)
- Performance before/after targets
- Backup + rollback plan for any changes

## WP-CLI quick reference

```bash
wp core version
wp plugin list --status=active
wp theme list
wp db optimize
wp cache flush
wp rewrite flush
wp search-replace 'http://old.com' 'https://new.com' --dry-run
wp user list --role=administrator
wp option get siteurl
wp cron event list
```

## Guardrails

- Always recommend staging/backup before making changes
- Don't suggest nulled/pirated themes or plugins
- Prefer WordPress.org repository plugins (vetted) over random third-party
- For code changes, use a child theme — never edit parent theme files
- Test changes on staging before production
