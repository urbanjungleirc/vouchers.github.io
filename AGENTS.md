# vouchers.github.io — UJ eVoucher Public Page

Public-facing voucher page hosted on GitHub Pages.

## Live URL

GitHub Pages default URL (no custom domain configured).

## Structure

```
index.html              — main voucher page
index_old.html          — archived previous version
config.js               — configuration (URLs, settings)
default_voucher_bg.png  — default voucher background image
```

## Related

The private backend for the voucher system lives in `working-private-files/vouchers/`:
- GAS project (`gas/`) handles PDF generation and email
- Python scripts for maintenance and fixes
- `src/` contains the source frontend files before they are published here

## Deploy

```bash
git add .
git commit -m "description"
git push   # GitHub Pages publishes automatically
```

## GitHub

Repo: `github.com/urbanjungleirc/vouchers.github.io` (private)
Branch: `main`

## Notes

- Source files (pre-publish) are in `working-private-files/vouchers/src/`
- Edit source there, then copy/build output into this repo for deployment
