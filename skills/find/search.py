#!/usr/bin/env python3
"""
Search klibs.io for Kotlin / KMP libraries.

Usage:
    search.py <query> [--limit N] [--page N] [--platforms p1,p2,...] [--packages]

Hits the public klibs.io backend (https://api.klibs.io) and prints a compact
JSON array to stdout. Strip-down keeps the response token-cheap for the agent.

Valid platforms: androidJvm, common, js, jvm, native, wasm
(`native` covers iOS / macOS / Linux / Windows KMP native targets.)
"""

import argparse
import json
import sys

import requests

API = "https://api.klibs.io"
PROJECT_FIELDS = ("name", "description", "scmLink", "scmStars",
                  "licenseName", "latestReleaseVersion", "platforms", "tags")
PACKAGE_FIELDS = ("groupId", "artifactId", "description", "scmLink",
                  "licenseName", "latestVersion", "platforms", "targets")


def search(query, limit=5, page=1, platforms=None, packages=False):
    endpoint = "/search/packages" if packages else "/search/projects"
    params = {"query": query, "limit": limit, "page": page}
    if platforms:
        params["platforms"] = ",".join(platforms)
    r = requests.get(f"{API}{endpoint}", params=params, timeout=15)
    r.raise_for_status()
    items = r.json()
    if isinstance(items, dict) and "error" in items:
        return {"error": items["error"]}
    fields = PACKAGE_FIELDS if packages else PROJECT_FIELDS
    return [{k: it.get(k) for k in fields if it.get(k) not in (None, [], "")}
            for it in items]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--platforms", default="",
                    help="comma-separated: androidJvm,common,js,jvm,native,wasm")
    ap.add_argument("--packages", action="store_true",
                    help="search Maven packages instead of projects")
    args = ap.parse_args()
    plats = [p.strip() for p in args.platforms.split(",") if p.strip()]
    try:
        result = search(args.query, args.limit, args.page, plats, args.packages)
    except requests.RequestException as e:
        result = {"error": str(e)}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
