# NAZZIM — Architecture

## The two spines

**Execution**

```
Goals  →  Areas  →  Projects  →  Tasks
```

**Knowledge**

```
Resources  →  Notes  →  Areas / Projects  →  Tasks
```

The spines meet at **Tasks**. That junction is the product: a note that produces no
task is storage, a task with no source is busywork.

## Databases

| Database | Title property | Purpose |
|---|---|---|
| Areas | `Area` | Ongoing domains you maintain. Never finish. Hub of the system. |
| Goals | `Goal` | Outcomes with a deadline. Self-relation gives yearly → quarterly. |
| Projects | `Project` | Finite efforts with a finish line. |
| Tasks | `Task` | Single physical actions. |
| Inbox | `Captured` | Frictionless capture. Emptied weekly. |
| Notes | `Note` | Your thinking. Self-relation gives links + backlinks. |
| Resources | `Resource` | External material worth keeping. |
| Books | `Book` | Reading pipeline. |
| Learning | `Skill` | Skills, courses, topics being actively built. |
| Habits | `Habit` | Behaviours being installed. Ticked from Daily Log. |
| Finance | `Transaction` | Money in/out. Deliberately not accounting software. |
| People | `Person` | Relationships with a contact cadence. |
| Daily Log | `Day` | One row per day. Plan (morning) + journal (evening). |
| Reviews | `Review` | Weekly / Monthly / Quarterly / Yearly in one history. |

## Relation graph

Areas is the hub. Backlinks land on Areas from Goals, Projects, Tasks, Notes,
Resources, Learning and Habits.

```
Areas ←── Goals ──→ Projects ──→ Tasks
  ↑         ↑ (self: Parent Goal / Sub-Goals)    ↑
  │         └────────────────────────────────────┘
  │
  ├── Notes ──→ Actions (Tasks)          ← the knowledge→action link
  │     ├── Related Notes / Referenced By (self)
  │     ├── Resource, Book, Learning, People, Project
  │
  ├── Resources ──→ Projects, Learning
  ├── Learning  ──→ Goal, Projects, Books, Notes, Resources
  └── Habits    ──→ Daily Log ("Completed On" / "Habits Done")

Daily Log ──→ Tasks  ("One Big Thing" / "Big Thing On")
Reviews   ──→ Goals, Projects  ("Goals Reviewed" / "Projects Reviewed")
Inbox     ──→ Areas, Projects  (one-way, keeps Areas clean)
```

## Calculated fields

Nothing below is typed by hand.

### Tasks
| Field | Type | Meaning |
|---|---|---|
| `Done` | formula (bool) | Status is Completed. Feeds project progress. |
| `Open` | formula (bool) | Not Completed, not Cancelled. |
| `Overdue` | formula (bool) | Past due and not closed. Feeds overdue rollups. |
| `Days Until Due` | formula (num) | Negative means overdue. |
| `Timeline` | formula (str) | Overdue / Today / Tomorrow / This Week / Later / No Date / Closed. |
| `Today Tier` | formula (str) | Must Do / Should Do / If Time. Drives the three Today sections. |
| `Workload` | formula (str) | Quick <15m, Short <1h, Medium <3h, Deep beyond. |
| `Done Today` / `Done This Week` | formula (str) | Completion windows. |

### Projects
| Field | Type | Meaning |
|---|---|---|
| `Progress` | rollup | % of this project's tasks complete (`percent_checked` on Tasks.Done). |
| `Tasks Total` / `Tasks Open` / `Tasks Overdue` | rollup | Counts. |
| `Complete` / `Is Active` | formula (bool) | Feed goal + area rollups. |
| `Health` | formula (str) | Not Started (Idea/Planning) / Blocked (Waiting) / On Track / At Risk / Behind / Overdue / Done. Status decides first; only a project that is actually running gets compared against elapsed time. |
| `Attention` | formula (str) | **Why** a project is stuck: no next action / no open tasks / has overdue tasks. Empty = healthy. |

### Goals
| Field | Type | Meaning |
|---|---|---|
| `Project Progress` | rollup | % of linked projects complete. |
| `Progress` | formula | Uses `Current`/`Target` when a target is set, else falls back to project progress. |
| `Health` | formula (str) | Same elapsed-time comparison as projects. |
| `Last Reviewed` | rollup | Latest linked review period. |

### Areas
`Active Projects`, `Open Tasks`, `Overdue Tasks`, `Note Count`, `Goal Count` — all rollups.

### Habits
`Times Done`, `Last Done` (rollups) → `Days Since`, `Habit Health` (formulas, judged
against the habit's own frequency). There is deliberately **no** automatic streak —
see DECISIONS.

### Finance
`Signed Amount` (income +, expense −, so a sum gives net), `Month`, `This Month`.

### People
`Days Since Contact`, `Follow Up Due`.

### Daily Log
`Habits Completed` (rollup), `Is Today` (formula).

## Which view type, and why

The choice is driven by how many rows there are and what you do with them.

| View | Used for | Why |
|---|---|---|
| Table | Tasks, Reviews, Notes, Resources | Scanning many rows down one column. |
| Board | Task status, Areas, Timeframes | Moving something between states. |
| List | Compact mobile reading | No horizontal scroll on a phone. |
| Calendar / Timeline | Due dates, project spans | Time is the question being asked. |
| Chart | Analytics | The shape matters more than the rows. |
| **Gallery** | **Areas, active Projects, active Goals** | **Few items, each carrying several numbers worth reading at once.** |

Galleries are used in exactly three places. A gallery of two hundred tasks is worse than a
table of two hundred tasks — cards cost vertical space, and that space is only earned when
each card carries more than a row could.

## Colour language

Two registers. They never share a surface, so they never compete: status colours only
appear on data, zone colours only on navigation.

**Status** — one meaning, one colour, on every row and every board:

| Meaning | Colour |
|---|---|
| Critical / late | red |
| Important / in flight | orange |
| Active / primary | purple |
| Scheduled / normal | blue |
| Complete / healthy | green |
| Waiting / caution | yellow |
| Inactive / neutral | gray |

**Zone** — navigation. Same hues, same connotations, applied to a *place* rather than a
state. A zone's colour appears in three places at once: its card on Home, the bar at the
top of every page inside it, and the page icons in the sidebar.

| Zone | Colour | Contains |
|---|---|---|
| Daily | purple | Today, Inbox, Command Center |
| Build | blue | Tasks, Projects, Goals |
| Think and live | green | Knowledge, Learning, Life |
| Rhythm | orange | Reviews, Analytics, Archive |
| Tools | gray | Start Here, AI Workflow Center, Blueprints |
| System | gray | Mobile Home, Settings & Help, System — Databases |

The rule that generates this: **colour marks where you spend time, gray marks what you
rarely touch.** Four zones of use are tinted; setup and plumbing recede. That is the whole
hierarchy, and it is why the last two cards deliberately share a colour — Tools and System
are one register, and reading them as one thing is correct.

Each Home card is a Notion callout carrying a coloured icon, an uppercase zone label, one
line of purpose and its three page links. Notion has no button block that an API can
create, so a tinted callout is the closest honest thing: it groups, it carries colour, and
its page links are already the pill-shaped tap targets a button would be.

## The page bar

Every page opens with the same two-line callout, tinted to its zone:

```
NAZZIM › DAILY
Today · Inbox · Command Center
```

Line one is the breadcrumb, line two the zone's three pages. The page you are on is bold
plain text rather than a link — you never click through to where you already are.

Three things this replaced, and why:

**`<mention-page>` became `[text](url)`.** Inline page mentions render with a `↗` glyph in
front of every item, so a row of six produced six arrows and read as clutter. A plain
markdown link renders as plain text, which is what a nav row should be.

**Eight arbitrary cross-links became three zone siblings.** The old row listed whichever
pages seemed related, differently on every page, so it taught the reader nothing and could
not be scanned. Three fixed siblings can be — and they are the same three every time you
are in that zone.

**The trailing divider went.** A callout already draws its own boundary; a rule underneath
it was a second separator doing the first one's job.

Page icons carry the zone colour too, so the sidebar is colour-coded without anyone having
to read it. Pages in Tools and System keep gray icons, which is the same rule working:
colour marks where you spend time.
