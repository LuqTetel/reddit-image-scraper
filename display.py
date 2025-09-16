#!/usr/bin/env python3
import os, json
from glob import glob
from threading import Thread
from typing import Optional
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import send_from_directory

from scraper import RedditScraper  # your class

# Flask app must be defined before using @app.route decorators
app = Flask(__name__, template_folder="templates")

def _all_json_files():
    out = "output"
    if not os.path.isdir(out): return []
    files = glob(os.path.join(out, "*.json"))
    files.sort(key=os.path.getmtime, reverse=True)  # newest by modified time
    return [os.path.basename(p) for p in files]

def _load_json(filename: Optional[str]):
    """Load output/<filename> if given, else newest."""
    if filename:
        path = os.path.join("output", filename)
        if not os.path.isfile(path):
            from flask import abort
            abort(404, f"File not found: {filename}")
    else:
        files = _all_json_files()
        if not files:
            return [], "-"
        path = os.path.join("output", files[0])
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), os.path.basename(path)

@app.route("/list")
def list_view():
    """
    Simple page: Title followed by Image.
    Works with full scraper JSON or *_images_only.json.
    Optional query: ?f=<filename.json> to pick a specific file from /output.
    """
    filename = request.args.get("f")  # e.g. malaysia_posts_images_only.json
    raw, fname = _load_json(filename)

    posts = []
    for p in raw if isinstance(raw, list) else []:
        img = p.get("image_url")
        if not img: 
            continue
        title = p.get("post_title") or p.get("title") or "Untitled"
        posts.append({"title": title, "image_url": img})

    files = _all_json_files()
    return render_template("list.html", posts=posts, filename=fname, files=files)

def latest_json_path() -> str:
    out = "output"
    if not os.path.isdir(out):
        return ""
    files = sorted(glob(os.path.join(out, "*.json")), key=os.path.getctime, reverse=True)
    return files[0] if files else ""

def load_posts():
    path = latest_json_path()
    if not path:
        return [], "-"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    return data, os.path.basename(path)

def _normalize_posts(raw):
    if not isinstance(raw, list):
        return []
    out = []
    for p in raw:
        q = dict(p)
        if "title" not in q:
            q["title"] = p.get("post_title") or p.get("title") or "Untitled"
        out.append(q)
    return out

@app.route("/")
def index():
    posts, fname = load_posts()
    return render_template("index.html", posts=_normalize_posts(posts), filename=fname)

@app.route("/api/posts")
def api_posts():
    posts, _ = load_posts()
    return jsonify(_normalize_posts(posts))

@app.route("/download-images-json")
def download_images_json():
    """Create and return an images-only JSON for the chosen or latest file."""
    from flask import abort
    # Determine input file
    arg = (request.args.get("f") or "").strip()
    if arg:
        in_path = os.path.join("output", arg)
        if not os.path.isfile(in_path):
            abort(404, f"File not found: {arg}")
    else:
        in_path = latest_json_path()
        if not in_path:
            abort(404, "No output files available to process")

    # Load input data
    try:
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        abort(400, f"Failed to read input JSON: {e}")

    # Filter down to images-only using existing helper
    try:
        from filter_images import filter_posts
        filtered = filter_posts(data)
    except Exception:
        # Minimal inline fallback
        filtered = []
        for r in data if isinstance(data, list) else []:
            url = r.get("image_url")
            if not url:
                continue
            title = r.get("post_title") or r.get("title") or "Untitled"
            filtered.append({"post_title": title, "image_url": url})

    # Save to output dir with *_images_only.json suffix
    os.makedirs("output", exist_ok=True)
    stem = os.path.splitext(os.path.basename(in_path))[0]
    out_name = f"{stem}_images_only.json"
    out_path = os.path.join("output", out_name)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(filtered, f, indent=2, ensure_ascii=False)
    except Exception as e:
        abort(500, f"Failed to write output JSON: {e}")

    # Return file as download
    return send_from_directory("output", out_name, as_attachment=True, mimetype="application/json")


@app.route("/popules")
def popules_landing():
    """Serve the Popules.com landing page replica template."""
    return render_template("popules.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    sub = (request.form.get("subreddit") or "malaysia").strip()
    try:
        pages = int(request.form.get("pages") or 3)
    except ValueError:
        pages = 3
    pages = max(1, min(50, pages))  # clamp for safety

    def run_job():
        try:
            s = RedditScraper(subreddit=sub)
            # Prefer positional to avoid keyword mismatch (pages vs num_pages)
            s.scrape(pages)                     # works if signature is (pages)
        except TypeError:
            # Fallback for older signature (num_pages=...)
            s.scrape(num_pages=pages)
        s.save_to_json(f"{sub}_posts.json")
        print(f"[scrape] Finished r/{sub} pages={pages}")

    Thread(target=run_job, daemon=True).start()
    return redirect(url_for("index"))

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    print("Open http://localhost:5000")
    app.run(debug=True)
