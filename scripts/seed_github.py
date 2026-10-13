#!/usr/bin/env python3
"""Create milestones and issues in GitHub from docs/USER_STORIES.md.

Uses the repository's existing label scheme (type:, priority:, effort:, area:, status:)
and adds one `epic:` label per epic. Talks to the GitHub REST API through `gh api`.

Usage:
    gh auth login                                   # once (not needed in GitHub Actions)
    python3 scripts/seed_github.py --repo OWNER/REPO --dry-run
    python3 scripts/seed_github.py --repo OWNER/REPO

Safe to re-run: existing labels/milestones are reused and issues whose title
already exists are skipped.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORIES = ROOT / "docs" / "USER_STORIES.md"

MILESTONES = {
    "M1": (
        "M1 – Running demo (week 2)",
        "2026-10-25T20:59:59Z",
        "Deployed site: browse sample crafts, craft detail page, sign up / log in / log out.",
    ),
    "M2": (
        "M2 – Contribute (week 4)",
        "2026-11-08T20:59:59Z",
        "Logged-in users add/edit crafts with photos; fields change by craft type.",
    ),
    "M3": (
        "M3 – MVP (week 6)",
        "2026-11-22T20:59:59Z",
        "Search/filter, roles, visibility & consent, steward review, reporting, profiles.",
    ),
    "M4": (
        "M4 – Enrich (week 8)",
        "2026-12-06T20:59:59Z",
        "Admin-managed attributes, TK labels, multilingual names, collections, accessibility.",
    ),
    "M5": (
        "M5 – Final product (week 10)",
        "2026-12-20T20:59:59Z",
        "Hardened, documented, tested v1.0 release.",
    ),
}

EPICS = {
    "E0": "setup & devops",
    "E1": "accounts",
    "E2": "craft catalogue",
    "E3": "flexible attributes",
    "E4": "discovery",
    "E5": "media",
    "E6": "cultural protocols",
    "E7": "administration",
    "E8": "quality",
}
EPIC_COLOR = "5319e7"

# Labels that already exist in the repo's documented scheme (created only if missing).
BASE_LABELS = {
    "type: feature": "1d76db",
    "type: documentation": "1d76db",
    "type: research": "1d76db",
    "type: test": "1d76db",
    "priority: critical": "b60205",
    "priority: high": "d93f0b",
    "priority: medium": "e99695",
    "priority: low": "f9d0c4",
    "effort: small": "74bbd9",
    "effort: medium": "b7037c",
    "effort: large": "cdbcd2",
    "status: to do": "c2e0c6",
    "area: backend": "2b4a12",
    "area: database": "7f367b",
    "area: frontend": "7c6550",
    "area: requirements": "e9b671",
    "area: wiki": "92af50",
    "Functional requirement-Accounts and login": "ad3aaf",
    "Functional requirement-Email": "04473f",
    "Functional requirement-Gallery": "46cfe0",
}

TYPE = {  # default for US-* is "feature"
    "T-01": "documentation",
    "T-02": "research",
    "T-03": "feature",
    "T-04": "test",
    "T-05": "feature",
    "T-06": "documentation",
    "T-07": "documentation",
    "T-08": "test",
    "US-29": "test",
    "US-32": "documentation",
}

AREA = {
    "T-01": ["requirements"],
    "T-02": ["requirements"],
    "T-03": ["backend"],
    "T-04": ["backend"],
    "T-05": ["database"],
    "T-06": ["frontend"],
    "T-07": ["wiki"],
    "T-08": ["backend"],
    "US-01": ["backend"],
    "US-02": ["backend", "frontend"],
    "US-03": ["backend"],
    "US-04": ["frontend"],
    "US-05": ["backend"],
    "US-06": ["frontend"],
    "US-07": ["frontend"],
    "US-08": ["backend", "frontend"],
    "US-09": ["backend"],
    "US-10": ["database"],
    "US-11": ["backend", "database"],
    "US-12": ["frontend"],
    "US-13": ["backend"],
    "US-14": ["backend"],
    "US-15": ["backend", "database"],
    "US-16": ["frontend"],
    "US-17": ["frontend"],
    "US-18": ["backend"],
    "US-19": ["database"],
    "US-20": ["backend"],
    "US-21": ["frontend"],
    "US-22": ["backend"],
    "US-23": ["database"],
    "US-24": ["backend"],
    "US-25": ["frontend"],
    "US-26": ["frontend"],
    "US-27": ["backend"],
    "US-28": ["database"],
    "US-29": ["frontend"],
    "US-30": ["backend"],
    "US-31": ["frontend"],
    "US-32": ["wiki"],
}

FUNCTIONAL = {
    "Functional requirement-Accounts and login": {"US-01", "US-02", "US-03", "US-04", "US-05"},
    "Functional requirement-Email": {"US-03"},
    "Functional requirement-Gallery": {"US-06", "US-20", "US-21"},
}

HEADER = re.compile(r"^### ((?:US|T)-\d+) · (.+)$")
META = re.compile(
    r"\*\*Epic:\*\* (E\d) · \*\*Milestone:\*\* (M\d) · "
    r"\*\*Priority:\*\* (\w+) · \*\*Points:\*\* (\d+)"
)


def epic_label(code):
    return f"epic: {EPICS[code]}"


def priority_label(moscow, milestone):
    if moscow == "must":
        return "priority: critical" if milestone == "M1" else "priority: high"
    return {"should": "priority: medium", "could": "priority: low"}[moscow]


def effort_label(points):
    return "effort: small" if points <= 2 else "effort: medium" if points <= 5 else "effort: large"


def parse():
    items, cur = [], None
    for line in STORIES.read_text(encoding="utf-8").splitlines():
        m = HEADER.match(line)
        if m:
            cur = {"id": m.group(1), "title": f"{m.group(1)} · {m.group(2)}", "lines": []}
            items.append(cur)
        elif cur and (line.startswith("## ") or line.strip() == "---"):
            cur = None
        elif cur is not None:
            cur["lines"].append(line)
    for it in items:
        body = "\n".join(it.pop("lines")).strip()
        meta = META.search(body)
        if not meta:
            sys.exit(f"Missing metadata line in {it['id']}")
        epic, ms, prio, pts = meta.groups()
        key = it["id"]
        it.update(milestone=ms, points=int(pts))
        labels = [
            f"type: {TYPE.get(key, 'feature')}",
            priority_label(prio.lower(), ms),
            effort_label(int(pts)),
            "status: to do",
            epic_label(epic),
            *[f"area: {a}" for a in AREA[key]],
            *[lbl for lbl, ids in FUNCTIONAL.items() if key in ids],
        ]
        it["labels"] = labels
        it["body"] = body
    return items


def gh(*args, payload=None):
    cmd = ["gh", "api", *args]
    if payload is not None:
        cmd += ["--input", "-"]
    r = subprocess.run(  # noqa: S603
        cmd,  # noqa: S607
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
    )
    if r.returncode:
        raise RuntimeError(f"gh api {args[0]}: {r.stderr.strip() or r.stdout.strip()}")
    return json.loads(r.stdout) if r.stdout.strip() else None


def paged(path):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        chunk = gh(f"{path}{sep}per_page=100&page={page}")
        out += chunk
        if len(chunk) < 100:
            return out
        page += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="OWNER/REPO")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    items = parse()
    repo = f"repos/{a.repo}"

    if a.dry_run:
        print(f"{len(MILESTONES)} milestones, {len(items)} issues")
        for it in items:
            labels = ", ".join(it["labels"])
            print(f"  [{it['milestone']}] {it['title']}  ({labels}, {it['points']} pts)")
        return

    wanted = {**BASE_LABELS, **{epic_label(k): EPIC_COLOR for k in EPICS}}
    have_labels = {lbl["name"].lower() for lbl in paged(f"{repo}/labels")}
    for name, color in wanted.items():
        if name.lower() not in have_labels:
            gh(f"{repo}/labels", "-X", "POST", payload={"name": name, "color": color})
            print(f"label  + {name}")

    ms_num = {m["title"]: m["number"] for m in paged(f"{repo}/milestones?state=all")}
    for title, due, desc in MILESTONES.values():
        if title not in ms_num:
            m = gh(
                f"{repo}/milestones",
                "-X",
                "POST",
                payload={"title": title, "due_on": due, "description": desc},
            )
            ms_num[title] = m["number"]
            print(f"milestone + {title}")

    have = {i["title"] for i in paged(f"{repo}/issues?state=all")}
    url = f"https://github.com/{a.repo}/blob/main/docs/USER_STORIES.md"
    source = f"\n\n_Source: [`docs/USER_STORIES.md`]({url})_"
    for it in items:
        if it["title"] in have:
            print(f"skip   {it['title']}")
            continue
        issue = gh(
            f"{repo}/issues",
            "-X",
            "POST",
            payload={
                "title": it["title"],
                "body": it["body"] + source,
                "labels": it["labels"],
                "milestone": ms_num[MILESTONES[it["milestone"]][0]],
            },
        )
        print(f"issue  #{issue['number']} {it['title']}")
        time.sleep(1.5)  # stay well under GitHub's content-creation rate limit


if __name__ == "__main__":
    main()
