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

**20 pages** — NAZZIM (home), Start Here, Today, Command Center, Inbox, Tasks,
Projects, Goals, Knowledge, Learning, Life, Reviews, Analytics, Archive,
AI Workflow Center, Blueprints, Mobile Home, Settings & Help, Remove the demo data,
System — Databases.

**89 linked views** composing the dashboards, plus view tabs on every database
(Tasks alone carries ten: Today, Overdue, Next Actions, Upcoming, Waiting,
Completed, Board, Calendar, By Area, By Project).

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the schema and
[`docs/DECISIONS.md`](docs/DECISIONS.md) for the reasoning and the limits.

## Object registry

`build/ids.env` maps every database, data source, page and key view to its Notion ID.
