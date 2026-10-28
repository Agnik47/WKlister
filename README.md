# Wish Karo – Multi-Platform Listing Tool

The listing team fills in **one master sheet**. The tool turns it into upload files for
**Meesho, Flipkart, Myntra and Amazon**. Each output is the marketplace's **own template**,
filled in, with its dropdowns, hidden sheets and formatting left as they were.

```
Wishkaro_Master_Listing.xlsx  ──►  python generate.py  ──►  Meesho_*.xlsx
   (filled by listing team)                                Flipkart_*.xls
                                                           Myntra_*.xlsx
                                                           Amazon_*.xlsm
                                                           Listing_Report_*.xlsx
```

## Website (recommended way to use it)

On ONE office PC (Windows):
1. Install Python 3.10+ (tick "Add python.exe to PATH") and LibreOffice (free, for the Flipkart file).
2. Double-click `start_website.bat`. First run installs everything (about 1 minute), then the browser opens.
3. Keep the black window open. It prints two links:
   - `http://localhost:5050` on that PC
   - `http://<PC-IP>:5050` for anyone on the same office Wi-Fi

The listing person opens the link, drops the filled master sheet, clicks **Generate**, and gets a zip
with the 4 platform files + report. Nothing is stored; files are deleted after 2 hours. No database, no cost.

**Auto-fixes before generating** (each one is listed under "Auto-fixed for you"):
double spaces, stray spaces in codes/links, prices typed as "Rs. 749", sizes typed as "6 - 7 years",
dropdown values in wrong capitals, the same product typed on several rows, secondary colour same as primary,
shoulder copied from length, impossible Meesho kids weight, "Wishkaro" in Meesho text (Meesho brand is Silver Kraft).

## Daily use (without the website)

1. Listing person fills `Wishkaro_Master_Listing.xlsx`:
   - **Products**: one row per colour.
   - **Sizes**: one row per size.
   - **Settings**: filled once.
2. Run the generator. You can either:
   - drag the filled file onto `generate_listings.bat` (Windows), or
   - run `python generate.py "path\to\filled_master.xlsx"`.
3. Open `Listing_Report_*.xlsx`. Fix every **ERROR** in the master and run again. Look at each **CHECK**.
4. Upload each file to its seller panel.

A run takes about 10 seconds, so it costs no AI tokens.

## One-time setup

- Python 3.10+ → `pip install -r requirements.txt`
- LibreOffice (free) is needed **only** for Flipkart's old `.xls` format. On Windows it's found automatically in `C:\Program Files\LibreOffice`.

## How the IDs work

- **SKU = `StyleCode_Size`** (e.g. `bxa245pkblu_3-6_Months`). This is the same pattern already used in Shopify and on all four marketplaces, so one SKU works everywhere.
- ASIN, Flipkart listing ID, Myntra styleId and the Meesho catalog ID are **assigned by the platforms after upload**. Nothing needs to match beforehand.
- **Parent Code** (e.g. `bxa245`) groups the colours of one design:
  - Amazon parent row
  - Meesho Group ID
  - Flipkart Group ID

## Files

| File | What it is |
|---|---|
| `app.py` | The website server: serves the page from `frontend/dist`, `/generate`, `/download`, `/api/info` |
| `start_website.bat` | Starts the website (rebuilds the page first on a PC with Node.js) |
| `dev.bat` | Developer mode: page and server rebuild/restart on every save |
| `publish.bat` | Sends your changes to GitHub; the laptop updates itself on its next start |
| `make_release.bat` | Makes a zip for the laptop (fallback when GitHub is not used) |
| `frontend/` | The web page source (Vite, plain JavaScript). See "Changing the website" below |
| `generate.py` | Main program: reads master → fills 4 templates → writes report |
| `vocab.py` | Master dropdown values and how each maps to each platform's spelling. **Edit this to add a colour, fabric, etc.** |
| `master_spec.py` | Master sheet columns and default settings |
| `build_master.py` | Rebuilds the blank master sheet (run after editing vocab/spec) |
| `writers.py` | Writes into the original templates without breaking them |
| `refresh_templates.py` | Run after downloading a newer template from a marketplace |
| `templates/` | The 4 original marketplace templates (Kids Dresses category) |
| `config/allowed_values.json` | Every dropdown list read out of those templates |

## Adding an option (example: a new fabric)

1. Add one line to `FABRICS` in `vocab.py`, with the platform spellings taken from the templates.
2. Run `python vocab.py`. It confirms every value exists in each platform's dropdown.
3. Run `python build_master.py` to refresh the master sheet's dropdowns.

## Looking after the tool

There are two copies:

| | Your PC (developer) | Office laptop (listing person) |
|---|---|---|
| Needs | Python, Node.js, LibreOffice | Python, LibreOffice. **No** Node.js |
| Start it with | `dev.bat` while you change things, or `start_website.bat` | `start_website.bat` |
| Address | http://localhost:5050 | http://localhost:5050 |

### While you change code (your PC)

Double-click **`dev.bat`**. It opens two windows; keep both open.
- Save a file in `frontend/src` → the page rebuilds in about 2 seconds. Refresh the browser.
- Save a `.py` file → the server restarts by itself.

`start_website.bat` also rebuilds the page every time it starts on a PC that has Node.js, so the page is never out of date.

### Sending a new version to the office laptop (GitHub, the normal way)

1. On your PC, double-click **`publish.bat`** and type a few words about what you changed.
   It builds the page, saves the change and sends it to GitHub.
2. That's all. The laptop downloads it the next time `start_website.bat` is opened there.
   No internet on the laptop? It simply starts the version it already has.

The first time, `publish.bat` asks for the address of your private GitHub repository
(create an empty one at github.com/new) and a GitHub sign-in window opens once.

To undo a bad version: on your PC run `git revert HEAD`, then `publish.bat` again.

### Without GitHub (zip, as a fallback)

1. On your PC, double-click **`make_release.bat`**. It builds the page and makes
   `releases\Wishkaro_Listing_Tool_<date>.zip` (about 3.5 MB, only what the laptop needs).
2. Copy the zip to the office laptop (pen drive, WhatsApp to self, Google Drive).
3. On the laptop: close the black "Wish Karo Listing Tool" window.
4. Right-click the zip → **Extract All** → pick the tool folder (always the same one, e.g. `C:\WishkaroListingTool`) → tick **replace files**.
5. Double-click `start_website.bat`. If `requirements.txt` changed, it installs the new parts by itself.

Keep the last two zips in `releases\`. If a new version has a problem, extract the previous zip the same way to go back.

Nothing on the laptop is lost when you update: the listing person's work lives in their master sheets, which are outside the tool folder, and generated files are temporary.

### Things to check now and then

- **A marketplace changes its template:** download the new one, replace the file in `templates\` on your PC, run `python refresh_templates.py`, fix anything it reports, then send a new release.
- **New colour, fabric, etc.:** edit `vocab.py`, run `python vocab.py`, then `python build_master.py`, then send a new release (it includes the new blank master sheet).
- **"Not connected" on the page:** the black window was closed. Start `start_website.bat` again.
- **Flipkart file missing:** LibreOffice is not installed on that PC.

### Changing the page by hand (command line)

```
cd frontend
npm install          (once)
npm run watch        -> rebuilds frontend/dist on every save (what dev.bat uses)
npm run dev          -> http://localhost:5173 with live reload; keep python app.py running on port 5050
npm run build        -> one-off build into frontend/dist
```

```
frontend/
  index.html            page shell
  src/main.js           puts the page together
  src/api/client.js     calls to app.py
  src/state/            app state, actions (generate, open a run), browser storage
  src/components/       header/, sidebar/ (upload, checklist, recent runs), output/ (results, files, issues)
  src/lib/              small helpers (DOM, formatting, grouping issues)
  src/data/platforms.js what each marketplace file is
  src/styles/           colours, fonts, buttons, layout
```

The page never changes how files are generated; that is all in the Python files.

## When a marketplace changes its template

1. Download the new template and replace the file in `templates/`, keeping the same name.
2. Run `python refresh_templates.py`. It re-reads all dropdowns and reports any mapping that broke.

## Built-in rules (taken from your existing files)

**Sizes**
- Master size: `3-6 Months`.
- Flipkart: `3 - 6 Months`.
- Myntra: `3-6M` / `1-2Y`.
- Amazon: size range `3 Months` → `6 Months` (`1-2 Years` = `12 Months` → `24 Months`).

**Baby vs girls**
- Sizes up to 1-2 Years are "Baby": Amazon age range Baby / department Baby Girls, Flipkart Ideal For Baby Girls.
- Larger sizes use Kid / Girls.

**Amazon** (Amazon's newer template: labels in row 4, column keys in row 5, Amazon's example in row 6, data from row 7)
- Columns are matched by the row-5 key, so Amazon can move columns around without breaking the tool.
- One Parent row per design (title = the words all its colours share), then one Child row per size.
- Package length and width = item size + 1 cm. You can change this in Settings.
- Lowest / highest allowed price = Amazon price − 10 / highest price of the design + 100 (never above MRP). Settings.
- Browse nodes, special features, occasions, holidays, life events and seasons come from Settings. Only values in Amazon's own dropdown are used; anything else is reported and skipped.
- The old flat-file template is kept in `templates/old/`.

**Myntra**
- `styleGroupId`: one number per colour + MRP, as Myntra's instructions require.
- `vendorArticleName`: cut to 40 characters.

**Meesho**
- HSN: Meesho's dropdown has no 8-digit `62041200`, so the tool uses the closest allowed code (`6204`).
- Wrong/Defective returns price = Meesho price minus ₹20. You can change this in Settings.
- Meesho allows Group 01–30 per file. The tool splits files automatically and never splits a design across files.

**Row limits per file** (change in Settings)
- Meesho 87, Myntra 300. These match each template's dropdown range.

## Tested against your hand-made files

Real products were taken from the existing Meesho, Flipkart, Myntra and Amazon files, rebuilt as master rows, and generated again:

| Platform | Filled cells identical to the hand-made file |
|---|---|
| Flipkart | 1200 / 1200 (100%) |
| Amazon | 812 / 836 (97%) |
| Meesho | 496 / 512 (97%) |
| Myntra | 378 / 399 (95%) |

Every difference is deliberate:
- Dates.
- Group numbering.
- Fields the tool now fills that were left blank.
- Two mistakes in the hand-made files:
  - Amazon `standard_price` 799 vs `sale_price` 899 on the same SKU.
  - Myntra light-green rows marked as Burgundy.

## Known limits

- **Category:** Kids Dresses/Frocks only. That is what the 4 templates are for. Adding a category means adding its template plus a vocab section.
- **Flipkart:** the "Fast Validate" button's progress pop-up is lost when LibreOffice saves the `.xls`. The macro code and all data are kept. Test the first upload.
- **Meesho images:** Meesho rejects non-Meesho image links. Use the **Meesho Image** columns with links from Meesho's image uploader.
- **Unmapped options:** if a platform has no equivalent for an option (e.g. Meesho has no Velvet), that cell is left blank and the report says so.
