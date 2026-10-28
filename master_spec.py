"""
Column layout of the master sheet. build_master.py draws the sheet from this,
generate.py reads it back by header text -- so headers here are the contract.
Each column: (key, header, required, dropdown_list_name, width, help_text, default)
"""
import vocab

LISTS = {
    "sizes": vocab.SIZES,
    "colours": list(vocab.COLOURS),
    "fabrics": list(vocab.FABRICS),
    "shapes": list(vocab.SHAPES),
    "lengths": list(vocab.LENGTHS),
    "necks": list(vocab.NECKS),
    "sleeve_lengths": list(vocab.SLEEVE_LENGTHS),
    "sleeve_styles": list(vocab.SLEEVE_STYLES),
    "patterns": list(vocab.PATTERNS),
    "occasions": list(vocab.OCCASIONS),
    "surface": list(vocab.SURFACE_STYLING),
    "closures": list(vocab.CLOSURES),
    "care": list(vocab.WASH_CARE),
    "yes_no": vocab.YES_NO,
    "knit_woven": vocab.KNIT_WOVEN,
    "transparency": vocab.TRANSPARENCY,
    "add_ons": list(vocab.ADD_ONS),
    "themes": vocab.MYNTRA_THEMES,
    "gst": vocab.GST,
    "kids_weight": sorted(set(vocab.MEESHO_KIDS_WEIGHT.values()),
                          key=lambda s: float(s.split("-")[0])),
}

C = lambda key, header, req=False, lst=None, width=16, help="", default=None: \
    dict(key=key, header=header, req=req, list=lst, width=width, help=help, default=default)

PRICE_COLS = [
    C("meesho_price", "Meesho Price", width=11, help="Selling price"),
    C("meesho_mrp", "Meesho MRP", width=11),
    C("flipkart_price", "Flipkart Price", width=11),
    C("flipkart_mrp", "Flipkart MRP", width=11),
    C("myntra_price", "Myntra Price", width=11),
    C("myntra_mrp", "Myntra MRP", width=11),
    C("amazon_price", "Amazon Price", width=11),
    C("amazon_mrp", "Amazon MRP", width=11),
]

PRODUCT_GROUPS = [
    ("PRODUCT", [
        C("style_code", "Style Code", True, width=19, help="One per colour. e.g. bxa245pkblu"),
        C("parent_code", "Parent Code", True, width=13, help="Same for all colours of one design. e.g. bxa245"),
        C("title", "Product Title", True, width=40, help="Name customers see"),
        C("short_name", "Myntra Short Name", width=26, help="Max 40 letters. Blank = title shortened"),
        C("list_view", "Myntra List View Name", width=26, help="Blank = title"),
    ]),
    ("CONTENT", [
        C("description", "Description", True, width=50, help="3-4 lines about the dress"),
        C("bullet1", "Bullet Point 1", width=30, help="Amazon bullets + Flipkart key features"),
        C("bullet2", "Bullet Point 2", width=30),
        C("bullet3", "Bullet Point 3", width=30),
        C("bullet4", "Bullet Point 4", width=30),
        C("bullet5", "Bullet Point 5", width=30),
        C("keywords", "Search Keywords", width=40, help="Comma separated"),
    ]),
    ("COLOUR", [
        C("brand_colour", "Colour Name", True, width=15, help="Exact shade, e.g. Peacock Blue"),
        C("primary_colour", "Primary Colour", True, "colours", 15, "Pick closest basic colour"),
        C("secondary_colour", "Secondary Colour", False, "colours", 15),
    ]),
    ("DRESS DETAILS", [
        C("fabric", "Fabric", True, "fabrics", 14),
        C("fabric_details", "Fabric Composition", width=22, help="e.g. 100% Polyester. Blank = Fabric"),
        C("shape", "Dress Shape", True, "shapes", 15),
        C("length", "Length", True, "lengths", 13),
        C("neck", "Neck", True, "necks", 15),
        C("sleeve_length", "Sleeve Length", True, "sleeve_lengths", 18),
        C("sleeve_style", "Sleeve Style", False, "sleeve_styles", 16, "Blank = auto"),
        C("pattern", "Pattern / Print", True, "patterns", 15),
        C("occasion", "Occasion", True, "occasions", 15),
        C("surface", "Surface Styling", False, "surface", 16, "Blank = None", "None"),
        C("closure", "Closure", True, "closures", 14),
        C("care", "Wash Care", True, "care", 13),
        C("lining", "Has Lining", False, "yes_no", 10, "", "No"),
        C("knit", "Knit or Woven", False, "knit_woven", 13, "", "Woven"),
        C("transparency", "Transparency", False, "transparency", 12, "", "Opaque"),
        C("add_on", "Add-On", False, "add_ons", 13, "", "No Add Ons"),
        C("character", "Character", width=13, help="e.g. Barbie. Blank = none"),
        C("theme", "Myntra Theme", False, "themes", 13, "", "NA"),
    ]),
    ("TAX", [
        C("hsn", "HSN Code", True, width=11, help="8 digits", default="62041200"),
        C("gst", "GST %", True, "gst", 8, default="5"),
    ]),
    ("PRICES (Rs) - leave a platform blank to skip it", PRICE_COLS),
    ("IMAGES (links)", [
        C("img_front", "Image 1 Front", True, width=28),
        C("img_back", "Image 2 Back", width=28),
        C("img_side", "Image 3 Side", width=28),
        C("img_detail", "Image 4 Close-up", width=28),
        C("img_look", "Image 5 Model/Look", width=28),
        C("img6", "Image 6", width=22),
        C("img7", "Image 7", width=22),
        C("img8", "Image 8", width=22),
        C("meesho_img1", "Meesho Image 1", width=24, help="From Meesho image uploader. Blank = Image 1"),
        C("meesho_img2", "Meesho Image 2", width=24),
        C("meesho_img3", "Meesho Image 3", width=24),
        C("meesho_img4", "Meesho Image 4", width=24),
    ]),
]

SIZE_GROUPS = [
    ("SIZE", [
        C("style_code", "Style Code", True, "style_codes", 16, "Must match Products sheet"),
        C("size", "Size", True, "sizes", 14),
        C("sku", "SKU", width=26, help="Blank = auto (StyleCode_Size)"),
        C("stock", "Stock", width=8, help="Blank = Settings default"),
    ]),
    ("MEASUREMENTS (inches) - Myntra & Meesho", [
        C("chest", "Chest (in)", True, width=10),
        C("front_length", "Front Length (in)", True, width=12),
        C("bust", "Bust (in)", width=10, help="Blank = Chest"),
        C("waist", "Waist (in)", width=10),
        C("hips", "Hips (in)", width=10),
        C("shoulder", "Across Shoulder (in)", width=12),
        C("kids_weight", "Meesho Kids Weight", False, "kids_weight", 12, "Blank = auto from size"),
    ]),
    ("PACKAGE", [
        C("pkg_l", "Pack Length (cm)", True, width=11),
        C("pkg_w", "Pack Width (cm)", True, width=11),
        C("pkg_h", "Pack Height (cm)", True, width=11),
        C("weight_g", "Weight (g)", True, width=10),
    ]),
    ("PRICE OVERRIDE for this size only (optional)", [dict(c, help="") for c in PRICE_COLS]),
]

# Settings sheet ------------------------------------------------------------
CHANNELS = ["Meesho", "Flipkart", "Myntra", "Amazon"]
MYNTRA_ADDR = ("Kotemoda Lifestyle Pvt Ltd.\nSurvey No. 94/3, Koralur, Soukya Road, "
               "Hosakote Taluk,\nBangalore-560067")
FK_ADDR = "Kotemoda Lifestyle Pvt Ltd, Survey No.94/3, Soukya Road, Hoskote Taluq, Bangalore-67"
CHANNEL_SETTINGS = [
    # label, [meesho, flipkart, myntra, amazon]
    ("Brand", ["Silver Kraft", "Wishkaro", "Wish Karo", "WISHKARO"]),
    ("Manufacturer Details", ["SS Lifestyle-Bangalore-560067", FK_ADDR, MYNTRA_ADDR, "Kotemoda Lifestyle Pvt Ltd."]),
    ("Packer Details", ["SS Lifestyle-Bangalore-560067", FK_ADDR, MYNTRA_ADDR, "Kotemoda Lifestyle Pvt Ltd."]),
    ("Importer Details", ["SS Lifestyle-Bangalore-560067", FK_ADDR, MYNTRA_ADDR, "Kotemoda Lifestyle Pvt Ltd."]),
    ("Country of Origin", ["India", "India", "India", "India"]),
    ("Default Stock", [1, 0, "", 1]),
    ("Max Rows per File", [87, 500, 300, 1000]),
]
GENERAL_SETTINGS = [
    ("Amazon Browse Node", "1967972031, 1953222031, 22951822031, 6648218031",
     "Up to 5 node numbers, comma separated (Girls dresses, Baby girls dresses, Fashion novelty, Fashion)"),
    ("Amazon Model Name", "", "Blank = product title"),
    ("Amazon Product ID Type", "GTIN Exempt", "GTIN Exempt / EAN / UPC"),
    ("Amazon Fulfilment", "Fulfillment by Merchant (Default)", "Or AMAZON_IN for FBA"),
    ("Amazon Handling Time (days)", 1, ""),
    ("Amazon Min Price Gap (Rs)", 10, "Lowest allowed price = Amazon price minus this. Blank = leave empty"),
    ("Amazon Max Price Gap (Rs)", 100, "Highest allowed price = highest Amazon price of the design plus this (never above MRP). Blank = leave empty"),
    ("Amazon Special Features", "Breathable, Not See-Through, Lightweight", "Comma separated, up to 5. 'Lined' is added when Has Lining = Yes"),
    ("Amazon Occasions", "Wedding, Birthday, Diwali", "Comma separated, up to 5 (Amazon's list only)"),
    ("Amazon Holidays", "Thanksgiving, Diwali, Christmas", "Comma separated, up to 3"),
    ("Amazon Life Events", "Anniversary, Birthday, Wedding", "Comma separated, up to 3"),
    ("Amazon Seasons", "All, Winter", "All / Spring / Summer / Autumn / Winter, comma separated"),
    ("Amazon Sale Start Date", "", "Blank = no sale dates (YYYY-MM-DD)"),
    ("Amazon Sale End Date", "", "Blank = 2 years from start"),
    ("Amazon Package Padding (cm)", 1, "Amazon package L/W = item size + this"),
    ("Flipkart Listing Status", "Active", ""),
    ("Flipkart Fulfilment By", "Seller", ""),
    ("Flipkart Procurement Type", "express", ""),
    ("Flipkart Procurement SLA (days)", 1, ""),
    ("Flipkart Shipping Provider", "Flipkart", ""),
    ("Flipkart Delivery Charge (Rs)", 0, "Local, zonal and national"),
    ("Flipkart Tax Code", "GST_APPAREL", ""),
    ("Myntra Fashion Type", "Fashion", ""),
    ("Myntra Year", "2026", ""),
    ("Myntra Season", "Fall", "Spring / Summer / Fall / Winter"),
    ("Myntra Package Contains", "1 Frock", ""),
    ("Meesho Returns Price Gap (Rs)", 20, "Wrong/Defective price = Meesho price minus this. Blank = leave empty"),
]
# Used when an older master sheet has no row for a setting.
GENERAL_DEFAULTS = {label: value for label, value, _ in GENERAL_SETTINGS}
