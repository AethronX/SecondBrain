#!/usr/bin/env python3
"""Covers for the Free edition.

Same system as Pro, with the Free edition's OWN fourteen-day completion shape
as the bar motif — the ornament has to be that product's data, not a copy of
another product's."""
import sys
import gen

gen.BARS = [1, 2, 1, 3, 1, 2, 1, 1, 2, 3, 2, 4, 3, 2]   # Free's Sep 6-19

PAGES = [                        # slug, page name (small), zone, masthead word
    ("free-root",      "NAZZIM FREE",       "ROOT",   "NAZZIM"),
    ("free-today",     "FREE · TODAY",      "DAILY",  "DAILY"),
    ("free-inbox",     "FREE · INBOX",      "DAILY",  "DAILY"),
    ("free-tasks",     "FREE · TASKS",      "BUILD",  "BUILD"),
    ("free-projects",  "FREE · PROJECTS",   "BUILD",  "BUILD"),
    ("free-areas",     "FREE · AREAS",      "BUILD",  "BUILD"),
    ("free-start",     "FREE · START HERE", "SYSTEM", "SYSTEM"),
    ("free-databases", "FREE · DATABASES",  "SYSTEM", "SYSTEM"),
    ("free-pro",       "FREE · UPGRADE",    "RHYTHM", "PRO"),
]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for slug, eyebrow, zone, name in PAGES:
        if only and slug != only:
            continue
        print(gen.build(slug, eyebrow, zone, name))
