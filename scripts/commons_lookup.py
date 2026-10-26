"""Find and check Wikimedia Commons photos for the real craft examples.

    python scripts/commons_lookup.py check             # every photo in reference_data exists
                                                       # and is freely licensed
    python scripts/commons_lookup.py search OUT TERM…  # candidate photos per search term:
                                                       # OUT/results.json + small previews

Needs internet access to Commons, so it runs in GitHub Actions (workflow "Commons photos").
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {
    "User-Agent": "SWE573-indigenous-crafts/1.0 (https://github.com/bakalit01/SWE573-2025719006)"
}
FREE = re.compile(r"^(CC0|CC BY(-SA)? [0-9.]+|Public domain|PD|GFDL|FAL)", re.I)


def api(**params):
    params |= {"format": "json", "formatversion": "2"}
    url = API + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=HEADERS)  # noqa: S310 (fixed https URL)
    with urllib.request.urlopen(request, timeout=30) as r:  # noqa: S310
        return json.load(r)


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def info(pages):
    out = []
    for page in pages:
        ii = (page.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        out.append(
            {
                "file": page["title"].removeprefix("File:"),
                "missing": page.get("missing", False),
                "license": strip_html(meta.get("LicenseShortName", {}).get("value")),
                "artist": strip_html(meta.get("Artist", {}).get("value"))[:120],
                "description": strip_html(meta.get("ImageDescription", {}).get("value"))[:300],
                "width": ii.get("width"),
                "height": ii.get("height"),
                "thumb": ii.get("thumburl", ""),
            }
        )
    return out


def check():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from crafts.reference_data import CRAFTS  # noqa: PLC0415

    names = [img[0] for craft in CRAFTS for img in craft["images"]]
    problems = []
    for i in range(0, len(names), 40):
        batch = names[i : i + 40]
        data = api(
            action="query",
            titles="|".join("File:" + n for n in batch),
            prop="imageinfo",
            iiprop="extmetadata|size",
        )
        for item in info(data["query"]["pages"]):
            ok = not item["missing"] and FREE.match(item["license"] or "")
            print(("OK  " if ok else "BAD ") + f"{item['license']:<16} {item['file']}")
            if not ok:
                problems.append(item["file"])
    if problems:
        sys.exit(f"{len(problems)} photo(s) missing or not freely licensed")
    print(f"All {len(names)} photos exist and are freely licensed.")


def search(out_dir, terms):
    out = Path(out_dir)
    (out / "previews").mkdir(parents=True, exist_ok=True)
    results = {}
    for term in terms:
        data = api(
            action="query",
            generator="search",
            gsrsearch=f"filetype:bitmap {term}",
            gsrnamespace=6,
            gsrlimit=12,
            prop="imageinfo",
            iiprop="extmetadata|size|url",
            iiurlwidth=360,
        )
        items = info(data.get("query", {}).get("pages", []))
        for n, item in enumerate(items):
            slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
            preview = f"previews/{slug}-{n:02d}.jpg"
            try:
                req = urllib.request.Request(item["thumb"], headers=HEADERS)  # noqa: S310
                with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
                    (out / preview).write_bytes(r.read())
                item["preview"] = preview
            except Exception as error:  # noqa: BLE001
                item["preview"] = f"failed: {error}"
        results[term] = items
        print(f"{term}: {len(items)} files")
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        check()
    elif sys.argv[1:2] == ["search"] and len(sys.argv) > 3:
        search(sys.argv[2], sys.argv[3:])
    else:
        sys.exit(__doc__)
