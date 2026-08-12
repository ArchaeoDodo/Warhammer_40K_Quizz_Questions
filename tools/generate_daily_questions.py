#!/usr/bin/env python3
"""
Generates the daily question-ID set for the WH40K quiz app's "daily challenge" feature.

Picks, from the full live question pool, 25 questions per difficulty (easy/medium/hard)
for each category (lore/rules) = 150 IDs total. Selection is deterministic per calendar
date (seeded off the UTC date string) so re-running this script on the same day always
produces the same set - safe to re-trigger (e.g. via workflow_dispatch) without spoiling
a different set for users who already fetched today's file.

Always operates against whatever questions.json currently contains, so the pool grows
automatically as new factions/questions are added - no hardcoded counts or IDs.

Usage:
    python3 generate_daily_questions.py questions.json daily.json [--date YYYY-MM-DD]
"""
import argparse
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone

PER_BUCKET = 25
DIFFICULTIES = ("easy", "medium", "hard")
CATEGORIES = ("lore", "rules")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("questions_file")
    parser.add_argument("output_file")
    parser.add_argument("--date", help="Override date (YYYY-MM-DD), defaults to today (UTC)")
    args = parser.parse_args()

    date_str = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with open(args.questions_file, encoding="utf-8") as f:
        data = json.load(f)

    buckets = defaultdict(list)
    for q in data["questions"]:
        category = q.get("category", "rules")
        difficulty = q.get("difficulty")
        if category in CATEGORIES and difficulty in DIFFICULTIES:
            buckets[(category, difficulty)].append(q["id"])

    result = {"date": date_str, "sourceVersion": data.get("version")}
    rng = random.Random(date_str)  # deterministic per calendar date

    for category in CATEGORIES:
        result[category] = {}
        for difficulty in DIFFICULTIES:
            pool = buckets[(category, difficulty)]
            if len(pool) < PER_BUCKET:
                print(f"ERROR: only {len(pool)} {category}/{difficulty} questions available, "
                      f"need {PER_BUCKET}", file=sys.stderr)
                sys.exit(1)
            picked = sorted(rng.sample(pool, PER_BUCKET))
            result[category][difficulty] = picked

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    total = sum(len(v) for cat in CATEGORIES for v in result[cat].values())
    print(f"Wrote {args.output_file}: {total} question IDs for {date_str} "
          f"(source questions.json version {data.get('version')})")


if __name__ == "__main__":
    main()
