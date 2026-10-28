"""
Wish Karo Listing Tool - website.

    python app.py            -> open http://localhost:5050

Anyone on the same office Wi-Fi can open http://<this-PC-IP>:5050
(the exact link is printed when it starts).
Nothing is stored: each upload is processed in a temp folder and deleted after 2 hours.
"""
import io
import os
import shutil
import socket
import tempfile
import threading
import time
import traceback
import uuid
import zipfile
from collections import Counter

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

import generate
import master_spec

HERE = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(HERE, "frontend", "dist")          # built by `npm run build` in frontend/
WORK = os.path.join(tempfile.gettempdir(), "wishkaro_listing_jobs")
BLANK_MASTER = os.path.join(HERE, "Wishkaro_Master_Listing.xlsx")
KEEP_SECONDS = 2 * 60 * 60
PORT = int(os.environ.get("PORT", 5050))        # 5000 is often used by other programs

app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024        # 25 MB upload limit
LOCK = threading.Lock()                                     # LibreOffice: one job at a time
os.makedirs(WORK, exist_ok=True)


def _cleanup_old():
    now = time.time()
    for name in os.listdir(WORK):
        p = os.path.join(WORK, name)
        try:
            if now - os.path.getmtime(p) > KEEP_SECONDS:
                shutil.rmtree(p, ignore_errors=True)
        except OSError:
            pass


def _job_dir(job):
    if not job or not all(c in "0123456789abcdef" for c in job):
        abort(404)
    d = os.path.join(WORK, job, "out")
    if not os.path.isdir(d):
        abort(404)
    return d


@app.get("/")
def index():
    if not os.path.isfile(os.path.join(UI, "index.html")):
        return ("The website files are missing. On a PC with Node.js, run in the frontend folder: "
                "npm install, then npm run build.", 500)
    res = send_from_directory(UI, "index.html")
    res.headers["Cache-Control"] = "no-cache"          # always pick up a new build
    return res


@app.get("/assets/<path:name>")
def ui_assets(name):
    return send_from_directory(os.path.join(UI, "assets"), name, max_age=31536000)   # file names change per build


@app.get("/favicon.svg")
def favicon():
    return send_from_directory(UI, "favicon.svg")


@app.get("/api/info")
def info():
    """Read-only facts for the page: which templates are in use and how long files are kept."""
    max_rows = dict(master_spec.CHANNEL_SETTINGS).get("Max Rows per File", [])
    platforms = []
    for i, (key, t) in enumerate(generate.TEMPLATES.items()):
        path = os.path.join(generate.TPL, t["file"])
        platforms.append(dict(
            key=key, name=generate.CH_NAME[key], ext=t["ext"], template=t["file"],
            template_updated=time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path))) if os.path.exists(path) else None,
            max_rows=max_rows[i] if i < len(max_rows) else None))
    return jsonify(platforms=platforms, keep_hours=KEEP_SECONDS // 3600, max_upload_mb=25)


@app.get("/blank-master")
def blank_master():
    return send_file(BLANK_MASTER, as_attachment=True, download_name="Wishkaro_Master_Listing.xlsx")


@app.post("/generate")
def do_generate():
    _cleanup_old()
    f = request.files.get("master")
    if not f or not f.filename:
        return jsonify(error="Please choose the filled master sheet first."), 400
    if not f.filename.lower().endswith(".xlsx"):
        return jsonify(error="That is not the master sheet. Please upload the .xlsx master file."), 400

    job = uuid.uuid4().hex
    root = os.path.join(WORK, job)
    out = os.path.join(root, "out")
    os.makedirs(out)
    src = os.path.join(root, "master.xlsx")
    f.save(src)

    try:
        with LOCK:
            summary, rep, report_path = generate.run(src, out)
    except SystemExit as e:                      # friendly messages raised by the generator
        shutil.rmtree(root, ignore_errors=True)
        return jsonify(error=str(e)), 400
    except Exception as e:
        traceback.print_exc()
        shutil.rmtree(root, ignore_errors=True)
        msg = str(e)
        if "LibreOffice" in msg:
            return jsonify(error="Flipkart file needs LibreOffice on this PC. " + msg), 500
        return jsonify(error="Could not read this file. Is it the Wish Karo master sheet? (" + msg[:200] + ")"), 500

    platforms = []
    for name, styles, rows, files in summary:
        names = [x.strip() for x in str(files).split(",") if x.strip() and not x.strip().startswith("-")]
        platforms.append(dict(name=name, products=styles, rows=rows, files=names))
    issues = [dict(level=r[0], platform=r[1], style=r[2], sku=r[3], field=r[4], msg=r[5]) for r in rep.rows]
    counts = Counter(i["level"] for i in issues)
    return jsonify(job=job, platforms=platforms, issues=issues,
                   report=os.path.basename(report_path),
                   counts=dict(error=counts["ERROR"], check=counts["CHECK"], info=counts["INFO"]))


@app.get("/download/<job>/<path:name>")
def download(job, name):
    d = _job_dir(job)
    if name == "all.zip":
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for fn in sorted(os.listdir(d)):
                z.write(os.path.join(d, fn), fn)
        buf.seek(0)
        stamp = time.strftime("%d-%b-%Y_%H%M")
        return send_file(buf, as_attachment=True, download_name=f"Listing_Files_{stamp}.zip",
                         mimetype="application/zip")
    if os.path.basename(name) != name or name not in os.listdir(d):
        abort(404)
    return send_file(os.path.join(d, name), as_attachment=True, download_name=name)


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "this-pc-ip"


if __name__ == "__main__":
    print("\n  Wish Karo Listing Tool is running")
    print(f"  On this PC:            http://localhost:{PORT}")
    print(f"  Others on office Wi-Fi: http://{lan_ip()}:{PORT}")
    print("  Keep this window open. Close it to stop.\n")
    if os.environ.get("DEV"):                      # dev.bat: restart by itself when a .py file is saved
        app.run(host="0.0.0.0", port=PORT, debug=True)
        raise SystemExit
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=PORT, threads=4)
    except ImportError:
        app.run(host="0.0.0.0", port=PORT)
