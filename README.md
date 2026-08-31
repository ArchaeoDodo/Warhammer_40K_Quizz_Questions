# Wartome Trivia — Question Pack

This repo is the question-data source for
[Wartome Trivia](https://github.com/ArchaeoDodo/Wartome-Trivia), an
unofficial, fan-made lore/rules trivia app for tabletop sci-fi
wargaming. It holds no app code — just the trivia content and the
scripts/workflows that publish it.

## Contents

- **`questions.json`** — the full question pool (`version` field +
  `questions` array). The app's `QuestionService` downloads whatever
  file is attached to this repo's [latest
  release](https://github.com/ArchaeoDodo/Wartome-Trivia-Questions/releases/latest)
  on first launch and on every subsequent version bump. See the app
  repo's README for the exact JSON schema.
- **`daily.json`** — today's Daily Challenge set: 150 question IDs (25
  per lore/rules × easy/medium/hard bucket), deterministically sampled
  from `questions.json` off that day's UTC calendar date so every
  player fetching on the same day gets the identical set. IDs only,
  never full question content.
- **`tools/generate_daily_questions.py`** — regenerates `daily.json`
  from whatever `questions.json` currently contains. Usage:
  `python3 generate_daily_questions.py questions.json daily.json [--date YYYY-MM-DD]`.

## Automation

- **`.github/workflows/daily-questions.yml`** — runs
  `generate_daily_questions.py` every day at 00:00 UTC and commits the
  refreshed `daily.json` straight to `master`.
- **`.github/workflows/release.yml`** — pushing a `v*` tag cuts a
  GitHub Release with `questions.json` attached. The app always
  downloads whatever's attached to the *latest* release, so the tag
  name itself doesn't matter beyond being a `v*` you haven't used yet.

## Legal notice

This repo is an unofficial, non-commercial, fan-made data source. It
is not affiliated with, endorsed, sponsored, or specifically approved
by Games Workshop Limited in any way.

Warhammer, Warhammer 40,000, and all associated names, races,
factions, characters, and other distinctive likenesses referenced in
`questions.json`/`daily.json` are either registered trademarks or
trademarks of Games Workshop Limited, variably registered around the
world, and used here without permission, purely for identification
and educational/trivia purposes. All related copyrights, trademarks,
and other intellectual property rights are the exclusive property of
Games Workshop Limited. No rules text, artwork, or other copyrighted
material belonging to Games Workshop is reproduced here — every
question is original trivia-question text written to test knowledge
of that publicly known setting, not excerpted from any Games Workshop
publication.

This data is provided free of charge and is not a substitute for
Games Workshop's own rulebooks, codexes, or official digital
products — always refer to those for official, up-to-date rules.
