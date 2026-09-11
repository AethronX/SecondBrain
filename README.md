# NAZZIM Second Brain — Ultimate

> Turn information into execution.

A production Notion personal operating system, built live in the connected workspace.
This repository holds the architecture record: what was built, why it is shaped that
way, and where Notion's real limits are.

**Root page:** [NAZZIM](https://app.notion.com/p/3d78c7645f3681c695a0cb3e7b29c3a0)

## The loop

```
CAPTURE → ORGANIZE → THINK → PRIORITIZE → EXECUTE → REVIEW
```

Every page and database exists to serve one step of that loop. Anything that only
stored information without improving a decision was cut.

## What exists

**14 databases** — Areas, Goals, Projects, Tasks, Inbox, Notes, Resources, Books,
Learning, Habits, Finance, People, Daily Log, Reviews.

**19 pages** — NAZZIM (home), Start Here, Today, Command Center, Inbox, Tasks,
Projects, Goals, Knowledge, Learning, Life, Reviews, Analytics, Archive,
AI Workflow Center, Blueprints, Mobile Home, Settings & Help, System — Databases.

**~75 views** — database view tabs plus filtered linked views composing every dashboard.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the schema and
[`docs/DECISIONS.md`](docs/DECISIONS.md) for the reasoning and the limits.

## Object registry

`build/ids.env` maps every database, data source, page and key view to its Notion ID.
