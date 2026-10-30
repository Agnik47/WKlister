"""
Writers that put rows into the marketplaces' OWN template files.

- .xlsx / .xlsm (Meesho, Myntra, Amazon): edits the sheet XML directly, so
  dropdowns, hidden sheets, macros and formatting stay exactly as the
  marketplace shipped them (openpyxl would silently delete the dropdowns).
- .xls (Flipkart): drives LibreOffice headless to write cells and save as .xls.
"""
import os
import re
import shutil
import subprocess
import tempfile
import time
import zipfile

from lxml import etree

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PNS = "http://schemas.openxmlformats.org/package/2006/relationships"
q = lambda tag: f"{{{NS}}}{tag}"


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _split_ref(ref):
    m = re.match(r"([A-Z]+)(\d+)", ref)
    return col_index(m.group(1)), int(m.group(2))


def _sheet_path(z, sheet_name):
    wb = etree.fromstring(z.read("xl/workbook.xml"))
    rels = etree.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = None
    for s in wb.iter(q("sheet")):
        if s.get("name") == sheet_name:
            rid = s.get(f"{{{RNS}}}id")
    if rid is None:
        raise ValueError(f"Sheet '{sheet_name}' not found")
    for r in rels:
        if r.get("Id") == rid:
            t = r.get("Target")
            return t.lstrip("/") if t.startswith("/") else "xl/" + t
    raise ValueError("sheet rel missing")


class SharedStrings:
    def __init__(self, xml_bytes):
        self.root = etree.fromstring(xml_bytes)
        self.items = list(self.root.iter(q("si")))
        self.index = {}
        for i, si in enumerate(self.items):
            ts = si.findall(q("t"))
            if len(ts) == 1 and len(si) == 1:
                self.index.setdefault(ts[0].text or "", i)

    def add(self, text):
        if text in self.index:
            return self.index[text]
        si = etree.SubElement(self.root, q("si"))
        t = etree.SubElement(si, q("t"))
        t.text = text
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        i = len(self.items)
        self.items.append(si)
        self.index[text] = i
        return i

    def tobytes(self, extra_refs):
        self.root.set("uniqueCount", str(len(self.items)))
        old = int(self.root.get("count", len(self.items)))
        self.root.set("count", str(old + extra_refs))
        return etree.tostring(self.root, xml_declaration=True, encoding="UTF-8", standalone=True)


def fill_ooxml(template, out_path, sheet_name, data_row, rows):
    """rows: list of {column_index(int): value}. Values: str/int/float/None."""
    zin = zipfile.ZipFile(template)
    sheet_file = _sheet_path(zin, sheet_name)
    sheet = etree.fromstring(zin.read(sheet_file))
    sst = SharedStrings(zin.read("xl/sharedStrings.xml"))
    sd = sheet.find(q("sheetData"))

    # style per column from the template's first data row (before clearing)
    col_style = {}
    row_els = {int(r.get("r")): r for r in sd.findall(q("row"))}
    first = row_els.get(data_row)
    if first is not None:
        for c in first.findall(q("c")):
            ci, _ = _split_ref(c.get("r"))
            if c.get("s"):
                col_style[ci] = c.get("s")

    # clear old data, keep cell styling
    for rnum, r in row_els.items():
        if rnum < data_row:
            continue
        r.attrib.pop("spans", None)
        for c in r.findall(q("c")):
            for child in list(c):
                c.remove(child)
            c.attrib.pop("t", None)

    refs = 0
    for i, values in enumerate(rows):
        rnum = data_row + i
        r = row_els.get(rnum)
        if r is None:
            r = etree.Element(q("row"), r=str(rnum))
            later = [n for n in row_els if n > rnum]
            if later:
                row_els[min(later)].addprevious(r)
            else:
                sd.append(r)
            row_els[rnum] = r
        cells = {_split_ref(c.get("r"))[0]: c for c in r.findall(q("c"))}
        for ci in sorted(values):
            v = values[ci]
            if v is None or v == "":
                continue
            c = cells.get(ci)
            if c is None:
                c = etree.Element(q("c"), r=f"{col_letter(ci)}{rnum}")
                if ci in col_style:
                    c.set("s", col_style[ci])
                later = [k for k in cells if k > ci]
                if later:
                    cells[min(later)].addprevious(c)
                else:
                    r.append(c)
                cells[ci] = c
            if isinstance(v, bool):
                v = "Yes" if v else "No"
            if isinstance(v, (int, float)):
                etree.SubElement(c, q("v")).text = repr(v) if isinstance(v, float) else str(v)
            else:
                c.set("t", "s")
                etree.SubElement(c, q("v")).text = str(sst.add(str(v)))
                refs += 1

    dim = sheet.find(q("dimension"))
    if dim is not None:
        last_row = max(row_els) if row_els else data_row
        m = re.match(r"([A-Z]+\d+):?([A-Z]+)?\d*", dim.get("ref"))
        if m and m.group(2):
            dim.set("ref", f"{m.group(1)}:{m.group(2)}{last_row}")

    new_sheet = etree.tostring(sheet, xml_declaration=True, encoding="UTF-8", standalone=True)
    new_sst = sst.tobytes(refs)

    # rebuild package; drop calcChain (old formula cells were cleared)
    tmp = out_path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name = item.filename
            if name == "xl/calcChain.xml":
                continue
            data = zin.read(name)
            if name == sheet_file:
                data = new_sheet
            elif name == "xl/sharedStrings.xml":
                data = new_sst
            elif name == "[Content_Types].xml":
                data = re.sub(rb'<Override[^>]*PartName="/xl/calcChain.xml"[^>]*/>', b"", data)
            elif name == "xl/_rels/workbook.xml.rels":
                data = re.sub(rb'<Relationship[^>]*Target="[^"]*calcChain.xml"[^>]*/>', b"", data)
            zout.writestr(item, data)
    zin.close()
    os.replace(tmp, out_path)
    return out_path


# ----------------------------------------------------------------- XLS ---
_UNO_SCRIPT = r'''
import sys, json, time, uno
from com.sun.star.beans import PropertyValue
def P(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p
job = json.load(open(sys.argv[1], encoding="utf-8"))
local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
for _ in range(60):
    try:
        ctx = resolver.resolve("uno:socket,host=127.0.0.1,port=%d;urp;StarOffice.ComponentContext" % job["port"])
        break
    except Exception:
        time.sleep(0.5)
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(job["template"]), "_blank", 0, (P("Hidden", True),))
if doc is None:
    sys.exit("LibreOffice could not open the Flipkart template. Close any open LibreOffice windows and try again.")
sh = doc.Sheets.getByName(job["sheet"])
try:
    sh.unprotect("")
except Exception:
    pass
cur = sh.createCursor(); cur.gotoEndOfUsedArea(False)
last_row, last_col = cur.RangeAddress.EndRow, cur.RangeAddress.EndColumn
d0 = job["data_row"] - 1
VALUES = 1 | 2 | 4 | 16          # values, dates, text, formulas - cell formats and dropdowns stay
if last_row >= d0:
    used = sh.getCellRangeByPosition(0, d0, last_col, last_row)
    # clear whole blocks of filled cells (a cell-by-cell loop took ~2 min on the Flipkart sheet)
    for a in used.queryContentCells(VALUES).getRangeAddresses():
        sh.getCellRangeByPosition(a.StartColumn, a.StartRow, a.EndColumn, a.EndRow).clearContents(VALUES)
    # the sheet is protected, so a block holding a locked cell is skipped: blank those one by one
    left = 0
    for a in used.queryContentCells(VALUES).getRangeAddresses():
        for r in range(a.StartRow, a.EndRow + 1):
            for c in range(a.StartColumn, a.EndColumn + 1):
                sh.getCellByPosition(c, r).setString("")
                left += 1
    print("CLEARED", d0, last_row, last_col, "one by one:", left, file=sys.stderr)
for i, row in enumerate(job["rows"]):
    for col, val in row.items():
        cell = sh.getCellByPosition(int(col) - 1, d0 + i)
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            cell.setValue(val)
        else:
            cell.setString(str(val))
doc.storeToURL(uno.systemPathToFileUrl(job["out"]), (P("FilterName", "MS Excel 97"), P("Overwrite", True)))
doc.close(True)
print("OK")
'''


def _find_office():
    """Return (soffice, python-with-uno). Works on Linux, macOS and Windows."""
    import sys
    from pathlib import Path
    cands = []
    if os.environ.get("LIBREOFFICE_PROGRAM"):
        cands.append(Path(os.environ["LIBREOFFICE_PROGRAM"]))
    if sys.platform.startswith("win"):
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
            cands.append(Path(base) / "LibreOffice" / "program")
    elif sys.platform == "darwin":
        cands.append(Path("/Applications/LibreOffice.app/Contents/MacOS"))
    for d in cands:
        exe = d / ("soffice.exe" if sys.platform.startswith("win") else "soffice")
        py = d / ("python.exe" if sys.platform.startswith("win") else "python")
        if exe.exists():
            if not py.exists():  # macOS keeps python in Resources
                alt = d.parent / "Resources" / "python"
                py = alt if alt.exists() else Path(sys.executable)
            return str(exe), str(py)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice not found. Install it (free) - it is needed only for the Flipkart .xls file. "
                           "Or set LIBREOFFICE_PROGRAM to its 'program' folder.")
    return soffice, (shutil.which("python3") or sys.executable)


def fill_xls(template, out_path, sheet_name, data_row, rows, port=2083):
    import json
    from pathlib import Path
    soffice, lo_python = _find_office()
    work = tempfile.mkdtemp(prefix="lo_")
    script = os.path.join(work, "uno_fill.py")
    job = os.path.join(work, "job.json")
    # LibreOffice opens a copy: if it crashes, its lock file is left here, not in templates/
    # (a stale templates/.~lock file makes every later Flipkart run fail)
    tpl_copy = os.path.join(work, os.path.basename(template))
    shutil.copyfile(template, tpl_copy)
    with open(script, "w", encoding="utf-8") as fh:
        fh.write(_UNO_SCRIPT)
    with open(job, "w", encoding="utf-8") as fh:
        json.dump({"template": tpl_copy, "out": os.path.abspath(out_path),
                   "sheet": sheet_name, "data_row": data_row, "port": port,
                   "rows": [{str(k): v for k, v in r.items() if v not in (None, "")} for r in rows]}, fh)
    profile = Path(work, "profile").as_uri()
    office = subprocess.Popen(
        [soffice, f"-env:UserInstallation={profile}", "--headless", "--invisible",
         "--nologo", "--norestore", "--nodefault",
         f"--accept=socket,host=127.0.0.1,port={port};urp;"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        res = subprocess.run([lo_python, script, job], capture_output=True, text=True, timeout=300)
        if "OK" not in res.stdout:
            raise RuntimeError("LibreOffice write failed: " + res.stderr[-2000:])
    finally:
        office.terminate()
        try:
            office.wait(timeout=20)
        except subprocess.TimeoutExpired:
            office.kill()
        shutil.rmtree(work, ignore_errors=True)
    return out_path
