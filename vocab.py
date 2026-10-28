"""
Master vocabulary for the Wish Karo listing tool (Kids Dresses / Frocks).

Each attribute has ONE master value list (what the listing person picks from a
dropdown in the master sheet). Every master value is mapped to the exact
spelling each marketplace accepts.

Rules:
- None  -> that marketplace has no matching option. The generator leaves the
           cell blank and flags it in the report so someone can pick manually.
- Mapped values are checked against config/allowed_values.json
  (run `python vocab.py` to verify after editing this file).

To add a new option: add one line to the right dict, run `python vocab.py`,
then `python build_master.py` to refresh the master sheet dropdowns.
"""

# ---------------------------------------------------------------- SIZES ----
# Master size spelling = the one already used in Shopify / Meesho / SKUs.
SIZES = [
    "0-3 Months", "3-6 Months", "6-9 Months", "9-12 Months", "12-18 Months",
    "18-24 Months", "1-2 Years", "2-3 Years", "3-4 Years", "4-5 Years",
    "5-6 Years", "6-7 Years", "7-8 Years", "8-9 Years", "9-10 Years",
    "10-11 Years", "11-12 Years", "12-13 Years", "13-14 Years", "14-15 Years",
    "15-16 Years",
]

# Sizes up to and including this one are "Baby" (Amazon age range / Flipkart
# Ideal For / Amazon department). Matches how the existing files were filled.
LAST_BABY_SIZE = "1-2 Years"


def _parse(size):
    lo, rest = size.split("-")
    hi, unit = rest.split(" ")
    return lo, hi, unit  # e.g. ("3", "6", "Months")


def size_for(channel, size):
    lo, hi, unit = _parse(size)
    if channel == "meesho":
        return size
    if channel == "flipkart":
        return f"{lo} - {hi} {unit}"
    if channel == "myntra":
        return f"{lo}-{hi}{'M' if unit == 'Months' else 'Y'}"
    raise ValueError(channel)


def amazon_key(attribute):
    """Amazon template column key without the marketplace/language parts, e.g.
    'item_name[marketplace_id=A21TJRUUN4KGV][language_tag=en_IN]#1.value' -> 'item_name#1.value'."""
    import re
    return re.sub(r"\[[^\]]*\]", "", str(attribute))


def amazon_size_range(size):
    """Amazon wants from/to values like '3 Months' / '6 Months', '2 Years'."""
    lo, hi, unit = _parse(size)
    if unit == "Months":
        return f"{lo} Months", f"{hi} Months"
    if size == "1-2 Years":           # Amazon has no '1 Years'; files used 12-24 Months
        return "12 Months", "24 Months"
    return f"{lo} Years", f"{hi} Years"


def is_baby(size):
    return SIZES.index(size) <= SIZES.index(LAST_BABY_SIZE)


def sku_for(style_code, size):
    return f"{style_code}_{size.replace(' ', '_')}"


# Default Meesho "Kids Weight (In Kgs)" per size (editable in master Settings).
MEESHO_KIDS_WEIGHT = {
    "0-3 Months": "3-5", "3-6 Months": "5-8", "6-9 Months": "5-8",
    "9-12 Months": "8-10", "12-18 Months": "8-10", "18-24 Months": "10-12",
    "1-2 Years": "10-12", "2-3 Years": "12-14", "3-4 Years": "14-15",
    "4-5 Years": "15-16", "5-6 Years": "17-19", "6-7 Years": "19-21",
    "7-8 Years": "21-23", "8-9 Years": "23-25", "9-10 Years": "26-28",
    "10-11 Years": "28-32", "11-12 Years": "32-35", "12-13 Years": "35-40",
    "13-14 Years": "35-40", "14-15 Years": "35-40", "15-16 Years": "35-40",
}

# --------------------------------------------------------------- COLOURS ---
COLOURS = {
    #  master        meesho          flipkart        myntra            amazon (Color Map)
    "Black":        dict(meesho="Black",      flipkart="Black",       myntra="Black",          amazon="Black"),
    "White":        dict(meesho="White",      flipkart="White",       myntra="White",          amazon="White"),
    "Off White":    dict(meesho="Cream",      flipkart="White",       myntra="Off White",      amazon="Off White"),
    "Cream":        dict(meesho="Cream",      flipkart="Beige",       myntra="Cream",          amazon="Off White"),
    "Beige":        dict(meesho="Beige",      flipkart="Beige",       myntra="Beige",          amazon="Beige"),
    "Red":          dict(meesho="Red",        flipkart="Red",         myntra="Red",            amazon="Red"),
    "Maroon":       dict(meesho="Maroon",     flipkart="Maroon",      myntra="Maroon",         amazon="Red"),
    "Burgundy":     dict(meesho="Maroon",     flipkart="Maroon",      myntra="Burgundy",       amazon="Red"),
    "Pink":         dict(meesho="Pink",       flipkart="Pink",        myntra="Pink",           amazon="Pink"),
    "Peach":        dict(meesho="Peach",      flipkart="Pink",        myntra="Peach",          amazon="Pink"),
    "Coral":        dict(meesho="Coral",      flipkart="Orange",      myntra="Coral",          amazon="Orange"),
    "Orange":       dict(meesho="Orange",     flipkart="Orange",      myntra="Orange",         amazon="Orange"),
    "Mustard":      dict(meesho="Mustard",    flipkart="Yellow",      myntra="Mustard",        amazon="Yellow"),
    "Yellow":       dict(meesho="Yellow",     flipkart="Yellow",      myntra="Yellow",         amazon="Yellow"),
    "Gold":         dict(meesho="Gold",       flipkart="Gold",        myntra="Gold",           amazon="Gold"),
    "Green":        dict(meesho="Green",      flipkart="Green",       myntra="Green",          amazon="Green"),
    "Dark Green":   dict(meesho="Green",      flipkart="Dark Green",  myntra="Green",          amazon="Green"),
    "Light Green":  dict(meesho="Mint Green", flipkart="Light Green", myntra="Lime Green",     amazon="Green"),
    "Mint Green":   dict(meesho="Mint Green", flipkart="Light Green", myntra="Sea Green",      amazon="Green"),
    "Olive":        dict(meesho="Olive",      flipkart="Green",       myntra="Olive",          amazon="Green"),
    "Teal":         dict(meesho="Teal",       flipkart="Blue",        myntra="Teal",           amazon="Turquoise"),
    "Blue":         dict(meesho="Blue",       flipkart="Blue",        myntra="Blue",           amazon="Blue"),
    "Navy Blue":    dict(meesho="Navy Blue",  flipkart="Dark Blue",   myntra="Navy Blue",      amazon="Blue"),
    "Light Blue":   dict(meesho="Blue",       flipkart="Light Blue",  myntra="Blue",           amazon="Blue"),
    "Turquoise":    dict(meesho="Aqua Blue",  flipkart="Light Blue",  myntra="Turquoise Blue", amazon="Turquoise"),
    "Purple":       dict(meesho="Purple",     flipkart="Purple",      myntra="Purple",         amazon="Purple"),
    "Lavender":     dict(meesho="Lavendar",   flipkart="Purple",      myntra="Lavender",       amazon="Purple"),
    "Magenta":      dict(meesho="Pink",       flipkart="Pink",        myntra="Magenta",        amazon="Pink"),
    "Brown":        dict(meesho="Brown",      flipkart="Brown",       myntra="Brown",          amazon="Brown"),
    "Grey":         dict(meesho="Grey",       flipkart="Grey",        myntra="Grey",           amazon="Grey"),
    "Silver":       dict(meesho="Silver",     flipkart="Silver",      myntra="Silver",         amazon="Silver"),
    "Multicolor":   dict(meesho="Multicolor", flipkart="Multicolor",  myntra="Multi",          amazon="Multicolor"),
}

# ---------------------------------------------------------------- FABRIC ---
# myntra = "Fabric" (base fibre), myntra_type = "Fabric Type" (weave/finish)
# amazon = "Material" dropdown (fibre only). Amazon's free-text "Fabric Type" gets the real fabric name.
FABRICS = {
    "Cotton":        dict(meesho="Cotton",        flipkart="Pure Cotton",   myntra="Cotton",        myntra_type="Cotton",   amazon="Cotton"),
    "Cotton Blend":  dict(meesho="Cotton Blend",  flipkart="Cotton Blend",  myntra="Cotton",        myntra_type="Cotton",   amazon="Cotton Blend"),
    "Cotton Lycra":  dict(meesho="Cotton Blend",  flipkart="Cotton Lycra",  myntra="Cotton",        myntra_type="Knitted",  amazon="Cotton Blend"),
    "Hosiery":       dict(meesho="Cotton",        flipkart="Hosiery",       myntra="Cotton",        myntra_type="Knitted",  amazon="Cotton"),
    "Cotton Linen":  dict(meesho="Cotton Linen",  flipkart="Cotton Linen",  myntra="Linen Blend",   myntra_type="Linen",    amazon="Linen Blend"),
    "Linen":         dict(meesho="Linen",         flipkart="Linen",         myntra="Linen",         myntra_type="Linen",    amazon="Linen"),
    "Satin":         dict(meesho="Satin",         flipkart="Satin",         myntra="Satin",         myntra_type="Satin",    amazon="Polyester"),
    "Georgette":     dict(meesho="Georgette",     flipkart="Georgette",     myntra="Georgette",     myntra_type="Georgette", amazon="Polyester"),
    "Net":           dict(meesho="Net",           flipkart="Net",           myntra="Polyester",     myntra_type="Net",      amazon="Nylon"),
    "Chiffon":       dict(meesho="Chiffon",       flipkart="Chiffon",       myntra="Chiffon",       myntra_type="Chiffon",  amazon="Polyester"),
    "Crepe":         dict(meesho="Crepe",         flipkart="Crepe",         myntra="Crepe",         myntra_type="Crepe",    amazon="Polyester"),
    "Lace":          dict(meesho="Lace",          flipkart="Lace",          myntra="Polyester",     myntra_type="Lace",     amazon="Polyester"),
    "Silk":          dict(meesho="Silk",          flipkart="Silk",          myntra="Silk",          myntra_type="NA",       amazon="Silk"),
    "Silk Blend":    dict(meesho="Silk Blend",    flipkart="Silk Blend",    myntra="Silk",          myntra_type="NA",       amazon="Silk Blend"),
    "Rayon":         dict(meesho="Rayon",         flipkart="Rayon Blend",   myntra="Viscose Rayon", myntra_type="NA",       amazon="Rayon"),
    "Viscose Rayon": dict(meesho="Viscose Rayon", flipkart="Viscose Rayon", myntra="Viscose Rayon", myntra_type="NA",       amazon="Rayon"),
    "Polyester":     dict(meesho="Polyester",     flipkart="Polyester",     myntra="Polyester",     myntra_type="NA",       amazon="Polyester"),
    "Velvet":        dict(meesho=None,            flipkart="Velvet",        myntra="Polyester",     myntra_type="Velvet",   amazon="Polyester"),
    "Jacquard":      dict(meesho="Jacquard",      flipkart=None,            myntra="Jacquard",      myntra_type="Jacquard", amazon="Polyester Blend"),
    "Denim":         dict(meesho="Denim",         flipkart="Denim",         myntra="Denim",         myntra_type="Denim",    amazon="Cotton"),
    "Modal":         dict(meesho="Modal",         flipkart="Modal",         myntra="Modal",         myntra_type="NA",       amazon="Rayon Blend"),
}

# ----------------------------------------------------------------- SHAPE ---
# amazon = "Style", amazon_silhouette = "Apparel Silhouette"
SHAPES = {
    "Fit and Flare":    dict(meesho="Fit And Flare",   flipkart="Fit and Flare Dress", myntra="Fit and Flare", amazon="Fit And Flare", amazon_silhouette="Fit & Flare"),
    "A-Line":           dict(meesho="A-Line",          flipkart="A- Line Dress",       myntra="A-Line",        amazon="A-Line",        amazon_silhouette="A-line"),
    "Gown / Princess":  dict(meesho="Princess/ Angel", flipkart="Gown Dress",          myntra="Gown",          amazon="Fit And Flare", amazon_silhouette="Princess"),
    "Shift":            dict(meesho="Shift",           flipkart="Shift Dress",         myntra="Shift",         amazon="Shift",         amazon_silhouette="Shift"),
    "Shirt Dress":      dict(meesho="Shirt",           flipkart="Shirt Dress",         myntra="Shirt",         amazon="Shirt",         amazon_silhouette="Shift"),
    "Wrap":             dict(meesho="Wrap",            flipkart=None,                  myntra="Wrap",          amazon="Wrap",          amazon_silhouette="Wrap"),
    "Kaftan":           dict(meesho="Kaftan",          flipkart="Tunic",               myntra="Kaftan",        amazon="Kaftan",        amazon_silhouette="Shift"),
    "Peplum":           dict(meesho="Peplum",          flipkart="Peplum",              myntra="Peplum",        amazon="Peplum",        amazon_silhouette="Peplum"),
    "Pinafore":         dict(meesho="Pinafore",        flipkart="Pinafore",            myntra="Pinafore",      amazon="Pinafore",      amazon_silhouette="Jumper"),
    "Blouson":          dict(meesho="Blouson",         flipkart="Blouson",             myntra="Blouson",       amazon="Swing",         amazon_silhouette="Blouson"),
    "Balloon":          dict(meesho="Balloon",         flipkart="Bubble Dress",        myntra="Balloon",       amazon="Pouf",          amazon_silhouette="Swing"),
    "Bodycon":          dict(meesho=None,              flipkart="Bodycon Dress",       myntra="Bodycon",       amazon="Bodycon",       amazon_silhouette="Bodycon"),
    "Empire":           dict(meesho=None,              flipkart="Empire Waist Dress",  myntra="Empire",        amazon="Empire Waist",  amazon_silhouette="A-line"),
    "High-Low":         dict(meesho="High-Low",        flipkart="High Low Dress",      myntra="Fit and Flare", amazon="Asymmetrical",  amazon_silhouette="Fit & Flare"),
}

# ---------------------------------------------------------------- LENGTH ---
LENGTHS = {
    "Above Knee":  dict(meesho="Above Knee",  flipkart="Above Knee",       myntra="Above Knee",  amazon="Above the Knee"),
    "Knee Length": dict(meesho="Knee Length", flipkart="Midi/Knee Length", myntra="Knee Length", amazon="Knee-Length"),
    "Below Knee":  dict(meesho="Calf Length", flipkart="Below Knee",       myntra="Midi",        amazon="Below the Knee"),
    "Calf Length": dict(meesho="Calf Length", flipkart="Calf Length",      myntra="Midi",        amazon="Calf Length"),
    "Maxi":        dict(meesho="Maxi",        flipkart="Maxi/Full Length", myntra="Maxi",        amazon="Maxi"),
}

# ------------------------------------------------------------------ NECK ---
# amazon = "Neck Style", amazon_collar = "Collar Style" (only for collars)
NECKS = {
    "Round Neck":       dict(meesho="Round Neck",       flipkart="Round",            myntra="Round Neck",       amazon="Crew Neck"),
    "V-Neck":           dict(meesho="V-Neck",           flipkart="V-Neck",           myntra="V-Neck",           amazon="V-Neck"),
    "Square Neck":      dict(meesho="Square Neck",      flipkart="Square Neck",      myntra="Square Neck",      amazon="Square Neck"),
    "Boat Neck":        dict(meesho="Boat Neck",        flipkart="Boat Neck",        myntra="Boat Neck",        amazon="Boat Neck"),
    "Peter Pan Collar": dict(meesho="Peter Pan Collar", flipkart="Peter Pan Collar", myntra="Peter Pan Collar", amazon="Collared Neck", amazon_collar="Peter Pan Collar"),
    "Shirt Collar":     dict(meesho="Shirt Collar",     flipkart="Collar Neck",      myntra="Shirt Collar",     amazon="Collared Neck", amazon_collar="Point Collar"),
    "Mandarin Collar":  dict(meesho="Mandarin Collar",  flipkart="Mandarin Collar",  myntra="Mandarin Collar",  amazon="Collared Neck", amazon_collar="Mandarin"),
    "Halter Neck":      dict(meesho="Halter Neck",      flipkart="Halter Neck",      myntra="Halter Neck",      amazon="Halter Neck"),
    "Off-Shoulder":     dict(meesho="Off-Shoulder",     flipkart="Off-Shoulder",     myntra="Off-Shoulder",     amazon="Off Shoulder Neck"),
    "One Shoulder":     dict(meesho="One Shoulder",     flipkart="One Shoulder",     myntra="One Shoulder",     amazon="One Shoulder Neck"),
    "Sweetheart Neck":  dict(meesho="Stylised",         flipkart="Sweet Heart Neck", myntra="Sweetheart Neck",  amazon="Sweetheart Neck"),
    "High Neck":        dict(meesho="High Neck",        flipkart="High Neck",        myntra="High Neck",        amazon="High Neck"),
    "Keyhole Neck":     dict(meesho="Keyhole Neck",     flipkart="Keyhole Neck",     myntra="Keyhole Neck",     amazon="Keyhole Neck"),
    "Cowl Neck":        dict(meesho="Stylised",         flipkart="Cowl Neck",        myntra="Cowl Neck",        amazon="Cowl Neck"),
    "Scoop Neck":       dict(meesho="Round Neck",       flipkart="Scoop Neck",       myntra="Scoop Neck",       amazon="Scoop Neck"),
    "Shoulder Straps":  dict(meesho="Shoulder Straps",  flipkart="Square Neck",      myntra="Shoulder Straps",  amazon="Square Neck"),
}

# --------------------------------------------------------- SLEEVE LENGTH ---
SLEEVE_LENGTHS = {
    "Sleeveless":            dict(meesho="Sleeveless",            flipkart="Sleeveless",   myntra="Sleeveless",            amazon="Sleeveless"),
    "Short Sleeves":         dict(meesho="Short Sleeves",         flipkart="Short Sleeve", myntra="Short Sleeves",         amazon="Short Sleeve"),
    "Three-Quarter Sleeves": dict(meesho="Three-Quarter Sleeves", flipkart="3/4 Sleeve",   myntra="Three-Quarter Sleeves", amazon="3/4 Sleeve"),
    "Long Sleeves":          dict(meesho="Long Sleeves",          flipkart="Full Sleeve",  myntra="Long Sleeves",          amazon="Long Sleeve"),
    "Shoulder Straps":       dict(meesho="Shoulder Straps",       flipkart="Noodle strap", myntra="Sleeveless",            amazon="Sleeveless"),
}

# ---------------------------------------------------------- SLEEVE STYLE ---
# Optional. Blank = "No Sleeves" for sleeveless, "Regular Sleeves" otherwise.
# amazon = "Sleeve Type"; Amazon has no plain/regular sleeve option, so those stay blank.
SLEEVE_STYLES = {
    "Regular Sleeves":       dict(flipkart="Regular Sleeves",      myntra="Regular Sleeves"),
    "No Sleeves":            dict(flipkart="No Sleeves",           myntra="No Sleeves"),
    "Puff Sleeves":          dict(flipkart="Puff Sleeve",          myntra="Puff Sleeves",          amazon="Puff Sleeve"),
    "Flutter Sleeves":       dict(flipkart="Flutter Sleeves",      myntra="Flutter Sleeves",       amazon="Flutter Sleeve"),
    "Flared Sleeves":        dict(flipkart="Flared Sleeve",        myntra="Flared Sleeves",        amazon="Bell Sleeve"),
    "Cap Sleeves":           dict(flipkart="Cap Sleeve",           myntra="Cap Sleeves",           amazon="Cap Sleeve"),
    "Bell Sleeves":          dict(flipkart="Bell Sleeves",         myntra="Bell Sleeves",          amazon="Bell Sleeve"),
    "Ruffled Sleeves":       dict(flipkart="Ruffled Sleeves",      myntra="Flutter Sleeves",       amazon="Ruffle Sleeve"),
    "Butterfly Sleeves":     dict(flipkart="Butterfly Sleeve",     myntra="Flutter Sleeves",       amazon="Butterfly Sleeve"),
    "Cold Shoulder Sleeves": dict(flipkart="Cold Shoulder Sleeve", myntra="Cold-Shoulder Sleeves", amazon="Cold Shoulder Sleeve"),
    "Shoulder Straps":       dict(flipkart="Shoulder Straps",      myntra="Shoulder Straps"),
}

# --------------------------------------------------------------- PATTERN ---
# flipkart_print = "Pattern/Print Type", myntra_print = "Print or Pattern Type",
# myntra_trend = "Main Trend"
PATTERNS = {
    "Solid":          dict(meesho="Solid",        flipkart="Solid",          myntra="Solid",         amazon="Solid",          flipkart_print="Solid",          myntra_print="Solid",              myntra_trend="New Basics"),
    "Printed":        dict(meesho="Printed",      flipkart="Printed",        myntra="Printed",       amazon=None,             flipkart_print="Graphic",        myntra_print="Graphic",            myntra_trend="Graphic Print Others"),
    "Floral Print":   dict(meesho="Printed",      flipkart="Floral Print",   myntra="Printed",       amazon="Floral",         flipkart_print="Floral",         myntra_print="Floral",             myntra_trend="Floral"),
    "Embroidered":    dict(meesho="Embroidered",  flipkart="Embroidered",    myntra="Embroidered",   amazon="Solid",          flipkart_print="Embroidered",    myntra_print="Self Design",        myntra_trend="Shadow Work"),
    "Embellished":    dict(meesho="Embellished",  flipkart="Embellished",    myntra="Embellished",   amazon="Solid",          flipkart_print="Embellished",    myntra_print="Embellished",        myntra_trend="Bling & Sparkly"),
    "Sequinned":      dict(meesho="Embellished",  flipkart="Embellished",    myntra="Embellished",   amazon="Solid",          flipkart_print="Sequined",       myntra_print="Embellished",        myntra_trend="Bling & Sparkly"),
    "Checked":        dict(meesho="Checked",      flipkart="Checkered",      myntra="Checked",       amazon="Checkered",      flipkart_print="Checkered",      myntra_print="Checked",            myntra_trend="Summer Checks"),
    "Striped":        dict(meesho="Striped",      flipkart="Striped",        myntra="Striped",       amazon="Striped",        flipkart_print="Striped",        myntra_print="Striped",            myntra_trend="Variegated Stripes"),
    "Polka Dots":     dict(meesho="Printed",      flipkart="Polka Print",    myntra="Printed",       amazon="Polka Dots",     flipkart_print="Polka",          myntra_print="Polka Dots",         myntra_trend="Polka Dots"),
    "Geometric":      dict(meesho="Printed",      flipkart="Geometric Print", myntra="Printed",      amazon="Geometric",      flipkart_print="Geometric",      myntra_print="Geometric",          myntra_trend="Geometric"),
    "Chevron":        dict(meesho="Printed",      flipkart="Chevron",        myntra="Printed",       amazon="Chevron",        flipkart_print="Chevron/Zig Zag", myntra_print="Chevron",          myntra_trend="Geometric"),
    "Cartoon Print":  dict(meesho="Printed",      flipkart="Graphic Print",  myntra="Printed",       amazon=None,             flipkart_print="Conversational", myntra_print="Cartoon Characters", myntra_trend="Conversational"),
    "Ethnic Motifs":  dict(meesho="Printed",      flipkart="Printed",        myntra="Printed",       amazon="Paisley",        flipkart_print="Ethnic Motifs",  myntra_print="Ethnic Motifs",      myntra_trend="Ethnic Print"),
    "Self Design":    dict(meesho="Self-Design",  flipkart="Self Design",    myntra="Self Design",   amazon="Solid",          flipkart_print="Self Design",    myntra_print="Self Design",        myntra_trend="New Basics"),
    "Colourblocked":  dict(meesho="Colorblocked", flipkart="Color Block",    myntra="Colourblocked", amazon="Solid",          flipkart_print="Colorblock",     myntra_print="Colourblocked",      myntra_trend="Colourblocked"),
    "Lace":           dict(meesho="Lace",         flipkart="Lace",           myntra="Self Design",   amazon="Solid",          flipkart_print="Self Design",    myntra_print="Self Design",        myntra_trend="Lace Frills Bows and Ruffles"),
    "Applique":       dict(meesho="Applique",     flipkart="Applique",       myntra="Embellished",   amazon="Solid",          flipkart_print="Applique",       myntra_print="Embellished",        myntra_trend="Placement"),
}

# -------------------------------------------------------------- OCCASION ---
# flipkart_suitable = "Suitable For", myntra_usage = "Usage"
# amazon = "Lifestyle", amazon_type = "Item Type Name", amazon_formality = "Formality Level"
OCCASIONS = {
    "Casual":           dict(meesho="Casual", flipkart="Casual",          flipkart_suitable="Western Wear", myntra="Casual", myntra_usage="Casual", amazon="Casual",
                             amazon_type="Casual Dress", amazon_formality="Casual"),
    "Party":            dict(meesho="Party",  flipkart="Party",           flipkart_suitable="Western Wear", myntra="Party",  myntra_usage="Party",  amazon="Party",
                             amazon_type="Special Occasion Dress", amazon_formality="Semi Formal"),
    "Festive / Ethnic": dict(meesho="Party",  flipkart="Festive/Wedding", flipkart_suitable="Ethnic Wear",  myntra="Party",  myntra_usage="Ethnic", amazon="Party",
                             amazon_type="Special Occasion Dress", amazon_formality="Semi Formal"),
}

# ------------------------------------------------------- SURFACE STYLING ---
SURFACE_STYLING = {
    "None":                dict(meesho="Not Applicable",      flipkart="None",                 myntra="NA"),
    "Tie-Ups":             dict(meesho="Tie-Ups",             flipkart="Tie-Ups",              myntra="Tie-Ups"),
    "Bow":                 dict(meesho="Bow",                 flipkart="Bow",                  myntra="Bow"),
    "Applique":            dict(meesho="Applique",            flipkart="Applique",             myntra="Applique"),
    "Ruffles":             dict(meesho="Ruffles",             flipkart="Ruffled",              myntra="Ruffles"),
    "Layered":             dict(meesho="Layered",             flipkart="Ruffled",              myntra="Layered"),
    "Embellished":         dict(meesho="Embellished",         flipkart="None",                 myntra="Embellished"),
    "Sequinned":           dict(meesho="Embellished",         flipkart="None",                 myntra="Sequined"),
    "Pleated or Gathered": dict(meesho="Pleated Or Gathered", flipkart="None",                 myntra="Gathered or Pleated"),
    "Lace":                dict(meesho="Lace Inserts",        flipkart="Laces",                myntra="Lace Inserts"),
    "Cut-Outs":            dict(meesho="Cut Out",             flipkart="Cut-Outs",             myntra="Cut-Outs"),
    "Smocked":             dict(meesho="Smocking Or Shirred", flipkart="None",                 myntra="Smocked"),
    "Fringed":             dict(meesho="Fringed",             flipkart="Fringed",              myntra="Fringed"),
    "Floral Detail":       dict(meesho="Rosette",             flipkart="Floral Design",        myntra="Applique"),
}

# --------------------------------------------------------------- CLOSURE ---
# amazon = "Closure Type", amazon_back = "Back Style"
CLOSURES = {
    "Zip":            dict(flipkart="Zipper",   myntra="Zip",           amazon="Zipper",       amazon_back="Zipper Back"),
    "Concealed Zip":  dict(flipkart="Zipper",   myntra="Concealed Zip", amazon="Zipper",       amazon_back="Zipper Back"),
    "Button":         dict(flipkart="Button",   myntra="Button",        amazon="Button",       amazon_back="Closed Back"),
    "Hook":           dict(flipkart="Hook",     myntra="Hook and Eye",  amazon="Hook and Eye", amazon_back="Closed Back"),
    "Tie-Up":         dict(flipkart="Tie-Up",   myntra="NA",            amazon="Drawstring",   amazon_back="Tie Back"),
    "Pull-On (none)": dict(flipkart="Pullover", myntra="NA",            amazon="Pull On",      amazon_back="Closed Back"),
}

# ------------------------------------------------------------ WASH CARE ----
WASH_CARE = {
    "Hand Wash":    dict(flipkart="Hand wash",            myntra="Hand Wash",    amazon="Hand Wash Only"),
    "Machine Wash": dict(flipkart="Regular Machine Wash", myntra="Machine Wash", amazon="Machine Wash"),
    "Dry Clean":    dict(flipkart="Dry clean only",       myntra="Dry Clean",    amazon="Dry Clean Only"),
}

# ----------------------------------------------------- SIMPLE LISTS -------
YES_NO = ["Yes", "No"]
KNIT_WOVEN = ["Woven", "Knitted", "Knitted and Woven"]
TRANSPARENCY = ["Opaque", "Semi Sheer", "Sheer"]
GST = ["5", "12"]

# Meesho Add On -> (Myntra Add-Ons, Flipkart Belt Included)
ADD_ONS = {
    "No Add Ons": dict(meesho="No Add Ons", myntra="NA",                flipkart_belt="No"),
    "Belt":       dict(meesho="Belt",       myntra="Comes with a belt", flipkart_belt="Yes"),
    "Hairband":   dict(meesho="Hairband",   myntra="NA",                flipkart_belt="No"),
    "Head Band":  dict(meesho="Head Band",  myntra="NA",                flipkart_belt="No"),
    "Bag":        dict(meesho="Bag",        myntra="NA",                flipkart_belt="No"),
    "Jacket":     dict(meesho="Jacket",     myntra="NA",                flipkart_belt="No"),
    "Camisole":   dict(meesho="Camisole",   myntra="NA",                flipkart_belt="No"),
}

MYNTRA_THEMES = ["NA", "Diwali", "Christmas", "Holi", "Raksha Bandhan",
                 "Krishna Janmashtami", "Wedding", "Beach", "Resort",
                 "Valentines", "Eid Al Fitr"]

# Which (channel, template column) each mapped key feeds -- used by the self-check.
CHECKS = [
    # (vocab dict, key in mapping, channel, allowed-values list name)
    (COLOURS, "meesho", "meesho", "Color"),
    (COLOURS, "flipkart", "flipkart", "Primary Color"),
    (COLOURS, "myntra", "myntra", "Prominent Colour"),
    (COLOURS, "amazon", "amazon", "color#1.standardized_values#1"),
    (FABRICS, "meesho", "meesho", "Fabric"),
    (FABRICS, "flipkart", "flipkart", "Fabric"),
    (FABRICS, "myntra", "myntra", "Fabric"),
    (FABRICS, "myntra_type", "myntra", "Fabric Type"),
    (FABRICS, "amazon", "amazon", "material#1.value"),
    (SHAPES, "meesho", "meesho", "Fit/ Shape"),
    (SHAPES, "flipkart", "flipkart", "Type"),
    (SHAPES, "myntra", "myntra", "Shape"),
    (SHAPES, "amazon", "amazon", "style#1.value"),
    (SHAPES, "amazon_silhouette", "amazon", "apparel_silhouette#1.value"),
    (LENGTHS, "meesho", "meesho", "Length"),
    (LENGTHS, "flipkart", "flipkart", "Length"),
    (LENGTHS, "myntra", "myntra", "Length"),
    (LENGTHS, "amazon", "amazon", "item_length_description#1.value"),
    (NECKS, "meesho", "meesho", "Neck"),
    (NECKS, "flipkart", "flipkart", "Neck Type"),
    (NECKS, "myntra", "myntra", "Neck"),
    (NECKS, "amazon", "amazon", "neck#1.neck_style#1.value"),
    (NECKS, "amazon_collar", "amazon", "collar_style#1.value"),
    (SLEEVE_LENGTHS, "meesho", "meesho", "Sleeve Length"),
    (SLEEVE_LENGTHS, "flipkart", "flipkart", "Sleeve Type"),
    (SLEEVE_LENGTHS, "myntra", "myntra", "Sleeve Length"),
    (SLEEVE_LENGTHS, "amazon", "amazon", "sleeve#1.length_description#1.value"),
    (SLEEVE_STYLES, "flipkart", "flipkart", "Sleeve Style"),
    (SLEEVE_STYLES, "myntra", "myntra", "Sleeve Styling"),
    (SLEEVE_STYLES, "amazon", "amazon", "sleeve#1.type#1.value"),
    (PATTERNS, "meesho", "meesho", "Pattern"),
    (PATTERNS, "flipkart", "flipkart", "Pattern"),
    (PATTERNS, "myntra", "myntra", "Pattern"),
    (PATTERNS, "amazon", "amazon", "pattern#1.value"),
    (PATTERNS, "flipkart_print", "flipkart", "Pattern/Print Type"),
    (PATTERNS, "myntra_print", "myntra", "Print or Pattern Type"),
    (PATTERNS, "myntra_trend", "myntra", "Main Trend"),
    (OCCASIONS, "meesho", "meesho", "Occasion"),
    (OCCASIONS, "flipkart", "flipkart", "Occasion"),
    (OCCASIONS, "flipkart_suitable", "flipkart", "Suitable For"),
    (OCCASIONS, "myntra", "myntra", "Occasion"),
    (OCCASIONS, "myntra_usage", "myntra", "Usage"),
    (OCCASIONS, "amazon", "amazon", "lifestyle#1.value"),
    (OCCASIONS, "amazon_type", "amazon", "item_type_name#1.value"),
    (OCCASIONS, "amazon_formality", "amazon", "formality_level#1.value"),
    (SURFACE_STYLING, "meesho", "meesho", "Surface Styling"),
    (SURFACE_STYLING, "flipkart", "flipkart", "Surface Styling"),
    (SURFACE_STYLING, "myntra", "myntra", "Surface Styling"),
    (CLOSURES, "flipkart", "flipkart", "Closure"),
    (CLOSURES, "myntra", "myntra", "Closure"),
    (CLOSURES, "amazon", "amazon", "closure#1.type#1.value"),
    (CLOSURES, "amazon_back", "amazon", "back#1.style#1.value"),
    (WASH_CARE, "flipkart", "flipkart", "Fabric Care"),
    (WASH_CARE, "myntra", "myntra", "Wash Care"),
    (WASH_CARE, "amazon", "amazon", "care_instructions#1.value"),
    (ADD_ONS, "meesho", "meesho", "Add On"),
    (ADD_ONS, "myntra", "myntra", "Add-Ons"),
]


def self_check(allowed):
    problems = []
    for vocab, key, ch, list_name in CHECKS:
        options = set(allowed[ch].get(list_name, []))
        if not options:
            problems.append(f"{ch}.{list_name}: no allowed list found")
            continue
        for master, m in vocab.items():
            v = m.get(key)
            if v is not None and v not in options:
                problems.append(f"{ch}.{list_name}: '{master}' -> '{v}' is NOT an allowed value")
    for s in SIZES:
        checks = [("meesho", "Variation", size_for("meesho", s)),
                  ("flipkart", "Size", size_for("flipkart", s)),
                  ("myntra", "Brand Size", size_for("myntra", s)),
                  ("amazon", "apparel_size#1.size", amazon_size_range(s)[0]),
                  ("amazon", "apparel_size#1.size_to", amazon_size_range(s)[1]),
                  ("meesho", "Kids Weight (In Kgs)", MEESHO_KIDS_WEIGHT[s])]
        for ch, ln, v in checks:
            if v not in set(allowed[ch].get(ln, [])):
                problems.append(f"SIZE {s}: {ch}.{ln} -> '{v}' not allowed")
    return problems


if __name__ == "__main__":
    import json, os
    here = os.path.dirname(os.path.abspath(__file__))
    allowed = json.load(open(os.path.join(here, "config", "allowed_values.json"), encoding="utf-8"))
    probs = self_check(allowed)
    print("\n".join(probs) if probs else "All vocabulary mappings are valid.")
