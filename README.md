# Bracket Maker — public site

Static pages required by App Store Connect: the privacy policy, the terms of use (EULA) and a
support page. No build step, no dependencies — Vercel serves the files as they are.

```
index.html     home page + support contact (App Store "Support URL")
privacy.html   generated from ../bracket-maker/docs/legal/privacy-policy.md
terms.html     generated from ../bracket-maker/docs/legal/terms-of-use.md
style.css      light and dark themes, matching the app
icon.svg       app mark, used as favicon and on the home page
vercel.json    clean URLs: /privacy and /terms work without the .html suffix
build.py       regenerates privacy.html and terms.html from the Markdown sources
```

## Before publishing

Replace the placeholders in **both** the Markdown sources (in the app repository, under
`docs/legal/`) and in `index.html`:

| Placeholder | What to put there |
| --- | --- |
| `[DATE]` | publication date, e.g. `20 September 2026` |
| `[DEVELOPER LEGAL NAME]` | the name you publish the app under |
| `[POSTAL ADDRESS]` | postal address (city and country are enough) |
| `[CONTACT EMAIL]` | support email address |
| `[COUNTRY]` | country whose law governs the terms |

Then regenerate the pages:

```bash
python3 build.py
```

## Local preview

Open `index.html` in a browser — the pages use relative paths, so they work from the file system
as well as from a server. `cleanUrls` in `vercel.json` makes the published `/privacy` and `/terms`
addresses work too; `privacy.html` keeps working and redirects to them.

## Deploy to Vercel

1. Create a GitHub repository and push this folder.
2. On vercel.com: **Add New… → Project → Import** this repository.
3. Framework preset **Other**, root directory `./`, no build command.
4. **Deploy.** Name the Vercel project `bracket-maker` so the URLs read well.

The URLs for App Store Connect:

- Privacy Policy URL — `https://bracket-maker.vercel.app/privacy`
- Terms of Use (EULA) — `https://bracket-maker.vercel.app/terms`
- Support URL — `https://bracket-maker.vercel.app/`

Put the first two into the app's `.env` as well, so the paywall links to them:

```
EXPO_PUBLIC_PRIVACY_URL=https://bracket-maker.vercel.app/privacy
EXPO_PUBLIC_TERMS_URL=https://bracket-maker.vercel.app/terms
```
