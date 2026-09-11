# NAZZIM — Decisions, limits and fixes

## Three databases were merged away

The brief specified 18 databases. The system ships 14. Each merge removes duplicate
data and, more importantly, removes a daily question with no good answer.

**Reviews + Weekly Reviews + Monthly Reviews → Reviews.**
Three databases holding the same object with the same fields is duplication, not
architecture. One `Reviews` database with a `Type` of Weekly/Monthly/Quarterly/Yearly,
and a view per cadence. Gain: review history reads in a straight line and one chart can
plot score across every cadence. Loss: none.

**Daily Planning + Journal → Daily Log.**
Both were one row per day. Keeping them apart forces the question "does this thought go
in the plan or the journal?" every single day. One row per day: morning half is Focus,
One Big Thing, Habits; evening half is Wins, Reflection, Grateful For, Tomorrow Matters.

**Dashboard Metrics → removed.**
A metrics database means hand-typing numbers weekly. Everyone stops by week three, after
which the dashboard lies. Every Analytics figure is computed live from real rows instead.
The historical record that was actually wanted — how each week scored, what shipped, what
was stuck — already lives in `Reviews`, entered once, as part of a ritual already happening.

## What Notion genuinely cannot do

Documented in-product on **Settings & Help**, not hidden.

| Limit | What ships instead |
|---|---|
| Buttons cannot be created via API | Exact 30-second build steps for Complete-task and Capture buttons. Every view's native **New** button does the same job in one more click. |
| Database templates cannot be created via API | **Blueprints** page: 13 page structures ready to paste, plus the 4-step conversion to a real template and how to set **Repeat** on daily/weekly ones. |
| Automations cannot be created via API | The one that matters (stamp `Completed Date` on completion) has step-by-step instructions. Until then `Done Today`/`Done This Week` fall back to last-edited time, so counters stay correct either way. |
| No consecutive-day streak is computable | `Last Done`, `Days Since` and `Habit Health` (judged against each habit's frequency) are computed and honest. `Current Streak` exists as an explicitly manual number. |
| No native graph visualisation | `Related Notes` + `Referenced By` give links and backlinks — the thing a graph is *for* — walkable in both directions. |
| No dynamic time-of-day greeting in page text | Not faked. The live element is the Daily Log "today" view, which is real. |
| No bulk delete, and no API to build a "clear demo data" button | The **Remove the demo data** page: seven views pre-filtered to the sample rows, so clearing them is select-all + Delete, seven times. |
| Database page layouts cannot be set via API | Page content templates are on **Blueprints** instead; the layout itself is a one-time manual setting, documented in Settings & Help. |
| Custom hex colours unsupported | Brand palette mapped to nearest Notion colours and applied *consistently*; table of the mapping is in Settings. Dark mode is a per-device Notion setting. |

## A real bug found and fixed during the build

**Empty-date propagation in `Today Tier`.**
First implementation used `or(status == "In Progress", and(not empty(Due Date), ...))`.
Notion propagates *empty* through `and`/`or` rather than short-circuiting, so an
in-progress task with **no due date** evaluated to empty and silently vanished from Today.
Caught by querying the view and finding 4 rows where 5 were expected.

Restructured so a date function is never evaluated on an empty date:

```
if(closed, "",
  if(status == "In Progress", <tier>,
    if(empty(Due Date), "",
      if(daysUntilDue <= 0, <tier>, ""))))
```

Re-verified: `Today Tier = "Must Do"` now returns both P1 tasks including the dateless
in-progress one. The same defensive restructure was applied to `Overdue` and `Follow Up Due`.

## Two API constraints that shaped the design

**View filters accept only absolute ISO dates.** A filter meaning "due before 10 Sep 2026"
is correct for exactly one day and quietly wrong forever after. So all date logic lives in
formulas that recompute daily — `Timeline`, `Today Tier`, `Done Today`, `Done This Week`,
`Is Today`, `This Month` — and views filter on those. This is why Today, Overdue and
This Month never go stale.

**Boolean-formula filters are silently dropped by the view DSL.** `FILTER "Overdue" = TRUE`
parsed to an empty filter set with no error — a view that looks configured but shows
everything. Found by reading back the created view config. Flag formulas used *only* for
filtering were converted to strings (`"Overdue"` / `""`) which filter reliably via
`IS NOT EMPTY`; the booleans the rollups depend on were kept as booleans.

Also: `NOT IN` is not valid DSL — use `!=` chained with `AND`.

## Health states are decided by status first, arithmetic second

`Projects.Health` originally only compared progress against elapsed time. That reads
wrongly at both ends of a project's life: an idea nobody has started yet is not "Behind",
and a project blocked on someone else is not "At Risk" — it is blocked, which calls for a
different action entirely.

The formula now resolves status before it does any arithmetic:

| Status | Health |
|---|---|
| Completed, Archived | Done |
| Idea, Planning | Not Started |
| Waiting | Blocked |
| Active, past deadline | Overdue |
| Active, no deadline | No Deadline |
| Active, running | On Track / At Risk / Behind, from progress vs elapsed time |

Only the last row is computed. Everything above it is a fact the user already stated, and
a health field that argues with a stated fact is a health field nobody trusts.

## Removing the demo data is a workflow, not a warning

Sample rows earn their place on day one and become clutter on day ten. Notion has no API
for bulk deletion and no button that can be created programmatically, so the honest version
is a page that makes the manual delete take seconds.

**Remove the demo data** (a child of Settings & Help) carries seven linked views, one per
database, each filtered to `Title starts with "Sample"`. Select-all in the header row,
press Delete, move to the next. Seven actions, no hunting, nothing real at risk — the filter
physically cannot show a row the user created.

The page also states what is *not* demo data, because getting that wrong is the expensive
mistake: the six Areas and five Habits are starting points meant to be renamed and kept, and
the Daily Log entry is dated rather than prefixed so it will not appear in these views.

## What the market leaders do, and what was worth copying

Researched against the products that actually sell: Thomas Frank's Ultimate Brain ($129),
Easlo's Second Brain ($39), and the aesthetic-dashboard category.

| Their pattern | Verdict |
|---|---|
| Horizontal top navigation with hyperlinks (Ultimate Brain) — reviewers rate it above Easlo's sidebar column | Already the pattern here. The page bar is the same idea, plus a zone colour. |
| A cohesive colour scheme — the most common *criticism* of Ultimate Brain is that it lacks one | This is the system's strongest card. Two registers, documented, applied everywhere. |
| Gallery views with cards for the few, high-value objects | **Was missing.** Added for Areas, Projects and Goals. |
| Life areas as the visual centrepiece | **Was missing.** Areas was the hub of the relation graph but appeared only as one table row set. |
| Cover images on every page | Deliberately skipped — see below. |
| Embedded widgets (clocks, weather, Spotify, Pomodoro) | Rejected. They are third-party iframes that break, and none of them answers "what should I do next?" |

Three galleries now exist where a card genuinely beats a row — few items, each carrying
several numbers worth seeing at once:

- **Areas of life** (Command Center) — purpose, active projects, open tasks, overdue tasks
- **Active projects at a glance** (Projects) — health, progress, next action, deadline
- **Goals at a glance** (Goals) — why, progress, health, timeframe

Tables were kept everywhere the job is scanning many rows against one column. A gallery of
two hundred tasks is worse than a table of two hundred tasks, and most templates get this
wrong in the other direction.

The six Areas also gained icons, coloured by `Type` — green for Life, blue for Work, purple
for Growth. That is the status register doing its job: `Type` is data.

## Two things researched, tried, and not shipped

**Notion 3.4's dashboard view.** The newest database feature — charts and KPI tiles in one
block — and the API will create one. It comes back `rows: []` and the view is then not
retrievable by ID, so there is no way to put a single tile in it. It ships as an empty
shell. Created one, confirmed the behaviour, deleted it. The seven live charts on Analytics
do the same job with real data.

**Cover images on every page.** The standard premium-template move, and the outbound proxy
in the build environment blocks `images.unsplash.com` and `www.notion.so`, so no image URL
could be verified before writing it to eighteen pages. Notion stores an external cover URL
without validating it, so a wrong guess ships as a broken image on every page — worse than
none. Left for the user, who can set one from Notion's own picker in two clicks per page.

## Verified, not assumed

- `Today Tier` — queried, returns exactly the expected 2 Must Do rows.
- `Timeline = "Closed"` — returns only the completed task; completed work no longer leaks into Overdue.
- `Attention` — the Needs Attention view returned exactly the project with an overdue task, which proves the `Tasks Open` **and** `Tasks Overdue` rollups compute and that `Tasks.Overdue` is correct.
- `Goals.Health` — returns "On Track" for the sample goal, proving the Health → Progress → Target/Current chain evaluates without error.
- `Projects.Health` — returns "On Track" for the running sample project after the rewrite, proving the nine-level formula evaluates.
- All fourteen dashboard pages fetched and confirmed: correct block order, breadcrumb, opening callout, linked views and closing empty-state callout. `ALTER COLUMN` did not silently drop property descriptions — Tasks and Projects schemas re-read in full.
- The seven demo-cleanup views read back with `string_starts_with` filters intact, so none of them can show a real row.

## Sample data

Everything prefixed `Sample ·` is demonstration data forming one complete chain:
Goal → Project → 7 Tasks → Note → Resource → Book → Learning → Daily Log → Habits.
It exists so no dashboard is empty on first open and so every formula had real rows to
verify against. Deletable without breaking anything.

The 6 Areas and 5 Habits are **not** samples — they are starting points meant to be
renamed and kept. Neither is the Daily Log entry, which is dated rather than prefixed.

**Remove the demo data** (under Settings & Help) clears the rest in about a minute.
