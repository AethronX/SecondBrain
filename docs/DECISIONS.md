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
| No bulk delete, and no API to build a "clear demo data" button | The **Remove the demo data** page: nine views pre-filtered to the sample rows, so clearing them is select-all + Delete, nine times. |
| Charts cannot group by a formula property | Every chart groups by a select, relation or date instead; formulas are still used freely as chart *filters*. |
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

**Remove the demo data** (a child of Settings & Help) carries nine linked views, one per
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

## The chart layer, and the one rule that governs it

Analytics carries **22 charts**: six number tiles across the top, then shape, then money,
then the trend. Every Notion chart capability the API exposes is in use — all five types
(number, donut, column, bar, line), count / sum / average aggregates, `STACK BY`, captions,
three heights, seven colour themes, and value sorting.

**The rule: you can filter on a formula, but you cannot group by one.**

This was found by testing, not assumed. `GROUP BY "Health"` on a formula property returns
a bare `Created view` with no view URI and no config echo — the chart is created but never
registers, and re-fetching the block shows no view at all. The identical call with
`GROUP BY "Status"` returns a full config. Same silent-failure class as the boolean-filter
drop found earlier in the build: no error, just a broken view.

So every chart groups by something real — select, multi-select, relation or date — while
filters still use the formulas freely (`Timeline = "Overdue"`, `Done This Week IS NOT EMPTY`,
`This Month IS NOT EMPTY` all work and are verified in the returned configs).

Where a formula was the natural grouping, the question was re-asked against a real property:

| Wanted | Shipped instead |
|---|---|
| Projects by `Health` | Projects by `Status`, plus health on the project gallery cards |
| Tasks by `Workload` | Time owed by `Priority`, and average task size by `Area` |
| Money by `Month` | Money by `Date` (Notion groups it by day) and by `Category` |
| Habits by `Habit Health` | Habits by `Frequency` |

Date grouping works but the API gives no granularity directive, so it defaults to `day`.
`Money over time` is therefore per-transaction rather than per-month. Honest, and still
readable; monthly rollup is a two-click change in the Notion UI.

## Sample data was extended so the charts have shape

A chart with no rows is worse than no chart. Finance and Reviews were empty, which left the
money and score charts blank — the two most persuasive charts in the product.

Added 17 sample transactions across July–September and six sample reviews (five weekly, one
monthly, scores 6/7/6/8/7). The review text is written as a real person's review, because
the score line is meaningless without something to read behind it.

Both are prefixed `Sample ·` and both now appear on **Remove the demo data**, which carries
nine filtered views rather than seven.

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

## The Pro edition, and what deleting a database actually leaves behind

NAZZIM Pro is a second live workspace, not a marketing tier. It was duplicated from
Ultimate and reduced to the nine databases that carry the two spines: Areas, Goals,
Projects, Tasks, Inbox, Notes, Resources, Daily Log, Reviews. Cut: Books, Learning,
Habits, Finance, People — and with them five pages (Learning, Life, AI Workflow Center,
Blueprints, Mobile Home).

**Deleting a database does not clean up after itself**, and every remnant is user-visible:

| What breaks | Where it turned up |
|---|---|
| Linked views render as a dead block marked `deleted` | Analytics (5), Remove the demo data (3), Knowledge (1), Archive (1) |
| A relation keeps pointing at a trashed data source | `Resources.Learning` survived the first sweep and was found only by reading the schema back |
| Page-bar links point at trashed pages | Knowledge, Start Here, Settings & Help, System — Databases |
| Prose names things that no longer exist | habit streaks, currency, Blueprints, "five Habits", "fourteen databases", the Ultimate changelog |

None of it was found by trusting the delete. Each page and each data source was fetched
and read — sixteen separate corrections in Settings & Help alone.

Rollups are the one thing Notion does handle: dropping a relation drops its rollups with
it, and Areas, Notes and Daily Log came back clean.

## Pro gained a chart band rather than only losing one

Ultimate carries 22 charts and not one reads from Notes or Resources — habits and money
crowded them out. Pro carries 20, and three are new:

- **Waiting to be read** — number tile, Resources filtered to `To Review`
- **Where your thinking lives** — Notes by `Area`, donut
- **What you actually save** — Resources by `Type`, column, sorted by value

Knowledge is half of what Pro sells. It now appears on the analytics page.

Three more API facts, each learned by being rejected:

- `COLOR` is not a top-level view directive. It belongs inside the `CHART` clause,
  alongside `AGGREGATE`, `HEIGHT`, `SORT` and `CAPTION`.
- Chart sort takes `x_ascending`, `x_descending`, `y_ascending`, `y_descending`. Plain
  `ASC` / `DESC` is rejected.
- After an edit, Notion rewrites inline links from `[text](/p/<id>?pvs=25)` to the full
  `https://app.notion.com/p/<id>` form. A later `update_content` matching the old shape
  fails with "No matches found" — re-fetch before the second edit to a page you just
  edited.

## The page grammar, rebuilt around fewer clicks

Every dashboard in Pro was the same shape: a prose callout, a paragraph, four to
seven linked views stacked vertically, another prose callout. On a phone that is six
screens of scrolling before you reach an answer. The rebuild gives all ten pages one
grammar:

```
page bar          one line, zone colour
number strip      two or three tiles, side by side
the primary view  the reason you opened the page
paired views      two per row instead of one
<details>         every word of prose, collapsed
```

Nothing was deleted from the writing — it moved into a single toggle per page, so the
page opens as an instrument and explains itself only when asked.

**Three separate views became one board.** Today had *Must do*, *Should do* and *If time*
as three stacked tables; it now has one board grouped by `Priority`, filtered to today's
work, with `hideEmptyGroups` on — so a light day shows one column, not four, and a task
changes priority by being dragged. The same move collapsed Tasks (five tables → one board
plus a calendar), Inbox (the five processing answers → five board columns you drag into),
Reviews (three tables → one board grouped by `Type`) and Goals (four tables → a gallery
and a board by horizon).

Three view types that were never used now carry real weight: **timeline** on Projects
(`Start Date` → `Deadline`, drag a bar to reschedule), **calendar** on Tasks, and
**gallery** wherever the objects are few and each carries several numbers worth seeing
at once — Areas, active Projects, Goals, Notes, finished work.

Analytics kept all twenty charts and lost half its height: they are banded into four
titled sections — *Today, in six numbers* · *Where the work sits* · *Are the weeks getting
better* · *What you read* — laid out three-up and two-up instead of one per row.

Reviews got the biggest readability win with no new views at all: the ten weekly questions
were a vertical list four screens long, and are now four columns — Look back, Look at the
system, Look for the lesson, Look forward — read left to right in one screen.

## Five more API facts, each learned by being rejected or silently ignored

Tested on a scratch page before touching the product, then deleted.

| Fact | How it showed up |
|---|---|
| Columns and toggles both accept linked database views | Confirmed by round-trip: a `<columns>` holding two views and a `<details>` holding a third all survived |
| **Boards cannot `GROUP BY` a formula** — same silent failure as charts | `GROUP BY "Today Tier"` returned a board config with no `groupBy` key at all. Re-based on `Priority`, which returned `groupBy` with `hideEmptyGroups: true` |
| Boolean-formula filters are still dropped silently | `FILTER "Overdue" IS NOT EMPTY` came back as `filters: []`. `Overdue` stayed boolean because the Projects rollups depend on it; every such filter now uses the string formula `Timeline` instead |
| `COLOR`, `HEIGHT`, `SORT` and `CAPTION` belong **inside** the `CHART` clause | `COLOR` as its own directive is "Unknown directive" |
| Chart sort is `x_ascending`/`x_descending`/`y_ascending`/`y_descending` | Plain `DESC` is rejected by name |
| Averaging a property is `AGGREGATE average ON "Score"` | Both `AGGREGATE average OF` and `AGGREGATE average "Score"` are parse errors |

**And the one that cost real time: `replace_content` reuses existing blocks, and a reused
block can keep its old position.** Rewriting a page whole does not lay the blocks out in
the order you wrote. On four pages exactly one `<columns>` row jumped above the page bar,
and on Reviews a callout whose text had been replaced stayed where the old callout sat.
Pages with a single columns row came out correct; pages with two or more did not.

The fix is to read the page back after every `replace_content` and move the stray block
with a targeted `update_content` — a delete and a re-insert in one call, which the tool
applies as a move rather than a delete. Every page in this rebuild was verified this way,
and four needed the second pass.

## One label per thing

The number tiles shipped with the label written twice. A Notion chart block renders
its **view name** as the block heading and its **caption** underneath, so a tile created
with `name: "Due today"` and `CAPTION "Due today"` reads the same words twice, stacked.
Twenty-six tiles did that.

`CAPTION ""` clears it, and the filter survives the update — so every tile now carries a
single short label above its number, and nothing else.

Captions were kept wherever they say something the name does not. *Active projects* on
Analytics is captioned "Three to five is a healthy load"; *Waiting to be read* is captioned
"Over ten means you are collecting, not learning." Those are judgements, not repetition.

The same audit caught twin names **within** a page — two blocks that mean the same thing
under different words:

| Page | Was | Now |
|---|---|---|
| Command Center | an *Overdue* tile above a *Late* list | the list is gone; Today owns overdue triage, Command Center shows the count |
| Command Center | *Waiting on someone else* and *Waiting to be processed* | *Blocked on someone else* and *Still to decide* |
| Reviews | a *Reviews run* tile above an *Every review you have run* board | *Reviews* and *Your review history* |
| Inbox | a *Decided* tile above a *Decide what each one is* board | *Processed* and *Decide what each one is* |
| Archive | a *Goals closed* tile above *Goals, achieved and let go* | *Goals* and *Achieved and let go* |

Across pages the opposite rule applies: the same concept keeps the same word everywhere.
Overdue is *Overdue* on Today, Command Center and Tasks — repeating a name for one idea is
consistency, and only repeating it for two different things, or twice on one tile, is noise.

## One bar, every page

Each page bar used to list only its own zone's siblings, so Today → Projects was two
taps: home, then Projects. Thirteen pages now carry the **same single-line bar**, with
the current page bold and unlinked and every other destination a link:

```
NAZZIM · Today · Inbox · Command · Tasks · Projects · Goals · Knowledge · Reviews · Analytics · Archive
```

One tap from anywhere to anywhere. The zone label in the bar was dropped — the callout's
colour and icon already carry it, and a word that repeats what the colour says is the
same duplication the labels audit removed. Setup pages get a second line for Start Here,
Settings & Help and System — Databases.

This is the piece that makes thirteen pages read as one product rather than thirteen
documents that happen to share a workspace.

## The home page, finally rebuilt

Home was the last page still shaped the old way, and the first one anybody opens: a quote,
a callout, five zone cards, then **seven stacked linked views** duplicating Today and
Command Center between them.

It now runs brand line → promise → five zone cards → *What should I do now?* → three
compact numbers (Overdue · Due today · Inbox) → **one list**, *Do this next*, sorted by
priority then due date → one toggle explaining the loop.

Six of the seven views are gone. The cards stay above the fold because they are what a
buyer sees first and what makes the breadth of the system legible in one screen; the
answer sits directly under them.

## Compact by default

Every number tile is now `HEIGHT small`, matching the tiles the original build shipped
with. This matters most on a phone: Notion stacks columns vertically there, so a
three-tile strip becomes three stacked blocks, and the difference between the default
height and `small` is roughly a third of a screen on every dashboard.

Three constraints remain outside the API's reach and are worth stating plainly: column
stacking on mobile cannot be turned off, buttons and database templates still cannot be
created programmatically, and none of this layout work has ever been seen rendered from
here — every claim above is verified by reading the page and view configs back, not by
looking at the result.

## Closing the last three gaps

**Start Here was the last page still shaped the old way** — seven prose sections in a
column, and the second page any buyer opens. Its job is "get running in ten minutes", so
the ten minutes are now three side-by-side steps in one screen (edit your areas, empty
your head, name one big thing) and everything else — first day, first week, the four
levels, the three rules, what to open later — sits in five toggles under them. All
thirteen pages now share one grammar.

**Two view types were missing where they would earn their place.** Goals gained a
timeline on `Deadline`, so a year of commitments reads as a line rather than a list;
Knowledge gained a board of notes grouped by `Type`, paired in columns with the reading
queue, which turns the two boards into one row instead of two.

**What is left is honest to name.** Visual identity in Notion without images is capped:
colour and typography carry everything, and the one lever that would lift it — page
covers — was explicitly removed at the user's instruction earlier in the build. That is
their call to reverse, not a limitation to work around silently.

And the ceiling that no amount of layout work moves: **Notion stacks columns vertically
on phones.** The number strips, the paired views and the Analytics bands are all a
desktop gain and a mobile no-op. Every page is still correct and readable on a phone —
just taller than the layout implies.

## PARA was missing a letter

I rated the information architecture 20/20 and was wrong. **Areas had no page.** Projects,
Resources and Archive each had a destination; Areas — the hub every project, task, note and
resource links to, and the *A* in PARA — existed only as a gallery inside Command Center.
Anyone who knows the method would have gone looking for it and not found it.

It exists now, in the BUILD group, and carries the one view no other page has: **Areas
grouped by `Type` — Life, Work, Growth.** Three columns that are wildly uneven is the most
useful sentence this system will ever say about someone's life, and no number on Analytics
says it as plainly. Above it sit three counts and a gallery of the areas themselves with
purpose, standard, and their live project and task counts.

The page also states the thing that makes Areas worth having: an area with zero open tasks
for a month is not a failure, it is information — you have quietly stopped maintaining
that part of your life.

## The Sunday ritual was only half built

Reviews looked backwards and stopped. The four question columns end with "write three
priorities for next week" and there was nowhere to put them.

A calendar of the week ahead now sits directly under the review board, so the ritual
closes properly: read the score, work the four columns, write the review, then drag those
three priorities onto real days. That last step is the whole value proposition of the
weekly-planning apps this audience already pays for, and it was one view away.

Fourteen pages now, and every one of the nine databases has a destination that answers a
question nothing else answers.

## What the reviews of the market leaders actually say

Researched against what reviewers and buyers write about the two templates this product
competes with — Thomas Frank's Ultimate Brain ($129) and Easlo's Second Brain ($39,
4.95 from 51 ratings, 96% five-star) — rather than against my own taste.

| What reviewers say | Where NAZZIM already stands | Action |
|---|---|---|
| Ultimate Brain's **horizontal top navigation is rated above Easlo's sidebar column** | Same pattern, and one tap to every destination rather than only the zone's siblings | none |
| Ultimate Brain's most common criticism is that it **lacks a cohesive colour scheme** | Two registers — status colours on data, zone colours on navigation — applied everywhere and documented | none |
| Easlo's nav **"works worse on mobile"**; the design **"can feel plain"** | Inline text links rather than a sidebar, so the bar wraps and stays tappable on a phone. Plain is accurate and is the owner's deliberate choice: no covers | none |
| **"Templates hide complexity. When something breaks, you're lost."** | Every page carries one toggle answering the question a stuck user would ask, and Settings carries troubleshooting plus a plain-language formula reference | none |
| **"The more sophisticated your second brain, the more maintenance it demands. What starts as a few minutes a week becomes hours."** | Nothing is filed by hand — every list is a filter and every number is computed | **say so on the home page** |
| **"Templates are too big to adopt in one shot."** · **"Most templates don't survive a week of real use."** | Fourteen destinations presented with equal weight on first open | **fix** |

The last two were real. Both are now answered on the first screen anybody sees.

The home callout states the upkeep cost honestly — *nothing is filed by hand, the only
upkeep is thirty minutes on a Sunday* — because the maintenance tax is the single most
repeated complaint in every review of every template in this category, and the honest
answer to it is this product's strongest claim.

And the five zone cards now carry a weight cue: **DAILY · start here**, **BUILD · from
day two**, **RHYTHM · from week two**, **THINK · later**, SYSTEM already said *rarely
needed*. Nothing is hidden — the buyer still sees the full system on open, which is what
they paid for — but they can now tell in one glance which three pages week one actually
needs, and that the rest is depth rather than homework.

That is progressive adoption without progressive disclosure, and it is the one thing the
reviews say every template in this category gets wrong.

## A view's name is invisible, and I shipped 29 unlabelled tiles

Seen rendered for the first time, on a phone, in dark mode. Two things were wrong and one
of them was a mistake of mine.

**A linked database block does not display its view name.** It shows the *source database*
name with an open-source arrow — `↗ Tasks` — and the view name appears nowhere. So the
only human label a chart tile can carry is its **caption**, and the earlier labels audit
removed all twenty-nine of them on the grounds that name and caption were saying the same
thing twice.

They were not duplicates. The name was never on screen. Three tiles on the home page read
`↗ Tasks · Count all · 4`, `↗ Tasks · Count all · 5`, `↗ Inbox · Count all · 0` — three
numbers with no meaning at all, on the first screen a buyer sees.

Every caption is restored. The rule that replaces the old one: **the block header already
says which database this is, so the caption says which cut** — `Tasks · Overdue`,
`Projects · Need attention`, `Reviews · Average score`. Still one label per tile, but now
it is the one that renders.

## The home page was a brochure, not an instrument

The second problem was structural. A visitor scrolled roughly a thousand pixels of prose
and five stacked colour blocks before reaching a single live number, because on a phone
the five zone cards stack and each page link inside them renders as its own full-width
block — a five-card row becomes about twenty blocks.

The page now opens with the work: tagline, two lines of promise, three numbers, the
*Do this next* list. Navigation sits below a divider as five compact cards whose links are
**inline text** rather than child-page blocks — two lines each instead of five or six.

The fourteen child pages still have to exist as real `<page>` blocks somewhere, or Notion
deletes them, so they live in the closing toggle alongside the explanation of how the
system fits together. Nothing is lost, nothing is hidden that matters, and the first
screen is now an instrument.

## Tabs existed the whole time, and they undo the mobile ceiling

Twice in this build I told the user that Notion's column-stacking behaviour set a hard
ceiling on how good the phone layout could get: `<columns>` collapse to a vertical stack
on a narrow screen, so a page with a three-number strip and three content views becomes
six full-width blocks to scroll past. I priced that at about three points and moved on.

It was wrong. The enhanced-markdown spec carries a `<tabs>` block, and a linked database
view lives inside a `<tab>` perfectly well — proved by inserting a throwaway two-tab block
on Analytics, reading it back, then removing it.

A tab strip is the one layout primitive that behaves *identically* on desktop and phone.
It does not stack, it does not reflow, and it costs one tap instead of a screen of scroll.

Eight pages, twenty-two views, now in tab strips:

| Page | Tabs |
| --- | --- |
| Analytics | Where the work sits · Are the weeks getting better · What you read |
| Tasks | Board · Calendar |
| Projects | Active · Timeline · Board |
| Goals | Active · Timeline · Board |
| Areas | Overview · By type |
| Knowledge | Ideas · By type · Reading queue · Search |
| Reviews | Board · Week ahead |
| Archive | Projects · Goals · Tasks |

Analytics is the clearest win: twenty charts in four banded sections became six always-visible
numbers plus three tabs. That is a load improvement as well as a layout one — a phone now
renders six views on arrival instead of twenty.

**Two pages deliberately kept their stacked layout.** Today is the daily driver and the
overdue strip sits *above* the board on purpose, so you see what is late before you plan
anything new; hiding either behind a tap defeats it. Command Center exists to answer "is
anything wrong anywhere", and that question needs every surface visible at once — a tab
you have to open to discover it is empty is worse than a short list that is visibly empty.

### Three API facts learned here

- `<tab>` takes its **title as the first indented line**, then its children below it.
- Tab icons are validated server-side: `icons/magnifying-glass_gray` is rejected by name,
  `icons/search_gray` is accepted. A rejected icon fails the whole call, so an icon that
  round-trips is a confirmed-valid icon.
- Creating `<database data-source-url>` with no `url` makes a linked-view block that the
  API counts as a **child database** — removing it later needs `allow_deleting_content`,
  even though it holds no data of its own.

## Empty-state guidance nobody could read

Notion's "No results" cannot be customised, so every page carried its empty-state answer
in prose — *"No plan above?"*, *"Nothing archived yet?"*, *"All of it empty?"*. All of it
was inside a collapsed `<details>` toggle. A first-time user staring at an empty board sees
`No results` and a closed toggle titled something like *What the states and priorities mean*,
which does not look like it holds the answer.

The fix costs nothing and works: **the toggle summary is always visible, so put the promise
there.** Eight summaries rewritten to name the empty case — *"…and what to do when the
board is empty"*, *"…and why it is empty at first"*, *"…and what it means when all of it is
empty"*, *"…and why week one looks flat"*. Tasks also gained the missing answer itself,
which had never been written: click New, type one thing, set a due date, and every other
property can stay blank forever.

## Start Here is seven timed steps

The three-column "three things to do today" opening was friendly but it hid the shape of
the setup — a reader could not tell whether they were five minutes or five hours from a
working system. It is now seven numbered steps in the order the spec asks for, each with
its own cost: understand the loop (30s), Areas (2m), one Goal (1m), one Project (1m),
three Tasks and one Note (2m), Today (1m), first Weekly Review (Sunday, 30m).

Above them sits the thirty-second escape hatch, because the seven steps are still too much
for someone who opened the product on a phone in a queue: open NAZZIM, the capture box is
under *Do this next*, click New, type, Escape. That is the only habit that has to survive a
bad day, and it should not be gated behind an onboarding.

## The four rhythms, named once

Retention was the weakest of the ten spec categories and the reason was findable: the daily
close lived on Today, the weekly ritual on Reviews, and monthly and yearly existed only as
`Type` options on a database — a cadence the product never actually told you to run. The
Reviews page now opens with all four named, costed and located: Daily 2 minutes on Today,
Weekly 30 minutes here, Monthly 45 minutes, Yearly 2 hours, with an explicit adoption order
— start weekly, add monthly after the fourth week, yearly can wait until there is a year
worth reading.

## The title was last in every view I built

A screenshot of the home page's *Do this next* list:

```
P1 Critical  ·  September 10, 2026  ·  📄 Sample · Build a 3x per week training
routine  ·  Next  ·  📄 Sample · P…
```

The project name dominates every row, the same project repeats down the whole
list, and the task name — the only thing the list exists to show — is last and
truncated to `Sample · P…`. The user's rating was 0/10 and it was correct.

The cause is one line of stored config:

```json
"displayProperties": ["Priority","Due Date","Project","Status","Task"]
```

**`displayProperties` order is render order, and `Task` is the title.** Putting
the title last in that array pushes it to the far right of the row, where it is
the first thing to be clipped. Nothing about the DSL warns you: `SHOW` accepts
any order and the API returns success.

I had written every view this way. Twenty-six content views across eleven pages,
built over the whole project, every one of them with the title last — because
the first one I wrote read naturally as *"show me priority, date, project,
status, and the task"* and I copied that shape forward without ever seeing it
render.

### The rules now

1. **The title is always the first entry in `SHOW`.** No exceptions.
2. **Never show the property the view is grouped or filtered by.** A board
   grouped by `Status` does not need a Status chip on every card; a view filtered
   to `Overdue` does not need an overdue flag.
3. **Property budget by view type** — list 2, board card 2–3, gallery card 3–5,
   calendar/timeline 1–2, table as many as useful. Lists and cards are one line
   of horizontal space; a table has real columns.
4. **Relations are the most expensive thing you can put in a row.** They render
   with a page icon and the full page title, so one `Project` relation can be
   longer than the title plus every chip combined. They belong on the item's own
   page, not in a list.

Applied across all twenty-six views. The same *Do this next* list now reads
`Draft the weekly plan · P1 Critical · Sep 10`.

### Why the audit did not catch this

The quality audit scored Design & Brand 9/10 the day before this screenshot, and
it was wrong — not by a point, by a category. Every check in that audit was an
API round-trip: filters correct, sorts correct, relations sound, structure
verified. All of it true, and none of it looks at the rendered page.

This is the second time in this build that a user screenshot found something no
amount of structural verification could: the first was the home page opening
with a thousand pixels of prose, this is the title being last in every view. The
lesson is not "verify more carefully" — the round-trips were accurate. It is that
**structural correctness and visual correctness are different properties, and I
can only observe one of them.**

## ↗ Tasks, three times in a row

A screenshot of the Today page: three number tiles side by side, each headed
`↗ Tasks`, each labelled `Count all`, showing 5, 4 and 0. Six identical strings
of chrome for three numbers.

The distinct labels were there — `Due today`, `Overdue`, `Done today` sit as
captions under each number, below the crop. What repeated was the header.

### That header cannot be renamed, and finding out cost something

A linked database block renders the **source database name** as its header. The
Notion-flavored Markdown `<database>` tag has a title slot that fetches back
empty, so it looked settable. It is not a block label — **it is a mirror of the
data source name.** Writing `TITLETEST` into one tile's tag renamed the entire
**Tasks** database to "TITLETEST", everywhere in the product, in one call.

Caught on the read-back and reverted immediately with `update_data_source`
`title: "Tasks"`. Nothing else was affected — the tag is the data source's name,
so setting it back restored every reference at once.

**Rule: never put text in the title slot of a `<database>` tag.** It is a rename
of the database, not a caption. The caption is the only per-block label, and it
is set through the view's `CHART … CAPTION` or the view name.

### The fix is fewer blocks, not better labels

Since the header is always the database name, three blocks from one database
side by side will always print that name three times. The only fix is to stop
having three blocks — and the moment that was forced, the better question became
obvious: **what were three counts of the same database doing above a list of the
same rows?** Every one of those tiles sat directly on top of a view containing
exactly the items it counted. They were decoration.

One tile per database per row, keeping the number the view below does *not*
already answer:

| Page | Was | Now |
| --- | --- | --- |
| Home | Overdue · Due today · Inbox · Active goals | Overdue · Inbox · Active goals |
| Today | Due today · Overdue · Done today | none — the overdue list *is* the signal |
| Tasks | Open · Overdue · Done this week | Overdue |
| Projects | Active · Need attention · Completed | Need attention |
| Goals | Active · Achieved · Dropped | Active |
| Inbox | Waiting · Processed | Waiting |
| Knowledge | Written · Saved · Still to read | Written · Still to read |
| Reviews | Run so far · Average score · Weekly | Average score |
| Analytics | six, in two rows of three | three, one per database |

Today loses its number strip entirely and is better for it: the page already
pulls overdue tasks out above the board, so a count of them one block higher was
the same four rows twice, and it made three consecutive `↗ Tasks` headers.

Areas, Archive and Command Center were already one-per-database and unchanged.

Thirteen tiles deleted. The captions that survive are now the only label on
their block, which is what they were always meant to be.

## The Free edition, built as a real product

The competitor's advantage was never their feature list — it was a free template
with 23,000 downloads and 334 public five-star ratings feeding a paid upsell.
NAZZIM had a paid product and no funnel. So the Free edition, which had existed
only as a paragraph in Settings & Help, is now a real, standalone, giveaway-ready
workspace.

**It is not a stripped copy of Pro.** It has its own four databases, so it can be
duplicated and handed to a stranger without touching anything in Pro.

| | Free | Pro |
| --- | --- | --- |
| Databases | Areas, Projects, Tasks, Inbox | those four plus Goals, Notes, Resources, Daily Log, Reviews |
| Pages | Home, Today, Inbox, Tasks, Projects, Areas, Start Here | those plus Command Center, Knowledge, Reviews, Analytics, Archive |
| Computed | `Attention`, `Progress`, `Timeline`, `Today Tier`, area rollups | all of that plus `Health` on projects and goals, twenty charts, a scored review rhythm |
| Onboarding | five timed steps, six minutes | seven timed steps, ten minutes |

**`Attention` is deliberately in Free.** It was tempting to hold the computed
judgements back for Pro, but `Attention` — *No next action*, *Overdue tasks*,
*No open tasks* — is the single thing that makes NAZZIM feel like an instrument
rather than a filing cabinet. A free product that does not demonstrate the reason
to upgrade is not a funnel, it is just a giveaway. One of the two seeded sample
projects ships **without** a Next Action on purpose, so the column fires on first
open and the mechanism explains itself.

`Health` — the elapsed-time comparison — stays in Pro. That is the honest tier
line: Free tells you *what* is stuck, Pro tells you *how far behind* you are.

### Three API facts this build cost

- **Multi-statement DDL is validated against the pre-update schema.** A batch
  that adds `Open` and then adds `Overdue` referencing `prop("Open")` fails with
  a bare `Type error with formula`, because `Open` does not exist yet when the
  batch is checked. Split ADD COLUMN statements by dependency level: independent
  formulas together, dependent ones in a following call. The error message names
  neither the statement nor the property, so this is worth remembering.
- **`formulaCode://` URIs cannot be fetched.** There is no way to read an
  existing formula's expression back through this API — only its name and type.
  Formula source has to be kept in the repo or re-derived.
- **`replace_content` scrambles order when a page already has appended blocks.**
  Creating views with `parent_page_id` appends them to the page end; a subsequent
  `replace_content` reuses those blocks but does not honour the new ordering. On
  the Free home page it produced divider → upsell → capture → nav → list → title.
  The repair is the same delete-and-reinsert move in a single `update_content`
  call that fixed the Pro pages, and it is reliable. Better: build the page text
  first and let the `<database>` tags create the views inline, rather than
  creating views and then writing text around them.

## The home page opened on debt

Every number on the home page was a number you owed. Seven tasks open. Three
things waiting in the inbox. Overdue, in red, above everything else. The page
was structurally correct and it was a guilt machine, and a guilt machine is not
something anyone wants to open on a Sunday night — which is the moment the whole
system depends on.

The competitor research had already said it without my hearing it: the templates
that sell show streaks, completion rings, "you shipped twelve things this week."
I had read that as decoration. It is not decoration. It is the only thing that
makes a system survive month three. People rarely abandon a life OS over a
missing feature. They abandon it when they stop seeing the progress they made.

So the page was inverted. It now opens on the result and closes on the
obligation:

| Position | Before | After |
|---|---|---|
| 1 | Open tasks · Inbox waiting · Goals on track | Finished this week · Average goal progress · Weeks you showed up |
| 2 | Today's work, overdue first | A bar for every day you completed something |
| 3 | Inbox capture | Active goals with percent, health and days left |
| 4 | Sunday review | Today's work, overdue first |
| 5 | Navigation | Inbox capture, then Sunday review, then navigation |

Nothing was invented to make this possible. `Done This Week`, `Completed Date`,
`Progress` and `Health` were already computed and were already being ignored by
the page that mattered most. The three old tiles were deleted rather than kept
alongside the new ones: two rows of numbers is not twice the proof, it is half
the attention.

The Sunday-review callout was rewritten to earn its place in the new order —
"that half hour is what turns the green numbers above into a line that keeps
climbing" — because a habit is easier to keep when you can see what it pays for.

### Three API facts this cost

- The view DSL is **semicolon-separated directives**, not newline-separated, and
  the content parameter is called `configure`. `CHART` and `GROUP BY` are
  separate directives: `CHART column AGGREGATE count; GROUP BY "Completed Date"`.
  Putting `AGGREGATE` after `GROUP BY` fails with `Unknown directive`.
- `FILTER "Status" is "Active"` is invalid. After `is` the parser expects only
  `EMPTY`. Select equality is `=`.
- `replace_content` did **not** scramble block order this time, because every
  view was written inline as a `<database url data-source-url>` tag in the new
  content rather than appended and then described around. That is the reliable
  way to reorder a page that holds linked views.

### And a marketing frame, because the images were selling features

The three showcase renders were accurate and cold. They showed chips and counts
— the mechanism. They now carry a benefit headline above the device, set in two
weights so the payoff lands on its own line:

- Desktop — "End every week knowing **exactly what you finished.**"
- Mobile — "The first thing you see **is what you did.**"
- Both — "Most systems show what you owe. **This one shows what you did.**"

The renders were rebuilt from the new page, so the claim and the screenshot are
the same artifact. That constraint is the point: if the headline ever stops
being true, the image stops matching the product, and the mismatch is visible
rather than arguable.

## One designed page and thirteen bare ones

The home page was good. Every other page opened on nothing — no cover, just
a title. That is the exact seam where a template stops feeling like a product:
the buyer clicks the second page in the sidebar and the design falls away.
Top-selling templates are consistent everywhere, and consistency across pages
is worth more than sophistication on one.

Fifteen covers now, one per page, all the same composition: `NAZZIM · <PAGE>`
in mono, an accent rule, the **zone** as the masthead word, and a bar motif.
The bars are the product's own fourteen-day completion shape — the same
numbers the home page charts — so the ornament is the data.

| Zone | Accent | Pages |
|---|---|---|
| ROOT | green | NAZZIM Pro |
| DAILY | purple | Today, Inbox, Command Center |
| BUILD | blue | Tasks, Projects, Goals, Areas |
| THINK | green | Knowledge |
| RHYTHM | orange | Reviews, Analytics, Archive |
| SYSTEM | grey | Start Here, Settings & Help, System — Databases |

### Two mistakes the mockup caught that an API round-trip never would

**The cover said the page name, and so did the H1 directly beneath it.** Two
identical titles a hundred pixels apart reads as a bug. The cover now carries
the zone; the page name is small, in the eyebrow. Nothing is said twice, and
the zone — the thing actually worth knowing at a glance — is what the band
announces.

**The page icon landed on the cover's text.** Notion always puts the icon at
the left edge of the content column, and its exact position moves with window
width. Tuning the padding would have fixed one width. Moving the text to the
right and the bars to the left fixes every width.

Both were invisible in the API response and obvious the moment the real cover
replaced the placeholder in the laptop render. The audit's blind spot, again:
structural correctness and visual correctness are different properties.

### The delivery path, and its one dependency

Notion page covers require an **external HTTPS URL** — `file-upload://` is
rejected with "Invalid page cover URL", and this container cannot reach
`api.notion.com` to do a direct multipart upload anyway. The repository is
public, so the covers are served from `raw.githubusercontent.com` pinned to a
commit SHA, which is immutable and survives a branch rename.

**That is a real dependency worth stating: if this repository is ever made
private, all fifteen covers break.** Making them Notion-hosted means dragging
each PNG into the page by hand once, in the Notion UI.

### A rendering defect that had been silent all along

Headless Chromium's `--window-size` sets the WINDOW; the viewport comes out
87px shorter, and `--screenshot` still writes a window-sized image whose
bottom strip was never painted. It went unnoticed across every 2000×2000 sheet
in this repo only because the dead strip happened to match the paper colour —
on a dark cover it was a visible band. `brand/pngcrop.py` crops in pure Python
(no Pillow here), and both render paths now draw 87px taller and crop back,
rather than hiding the strip behind a matching background.

### What is still not best-in-class

Page **icons** are still Notion's built-ins, zone-coloured. They are crisp and
consistent, and at the ~20px the sidebar renders them, a custom set is as
likely to look worse as better. That is the remaining visible gap against the
top sellers, and it is a judgement call rather than an oversight.

## The funnel's front door was still built the old way

Pro was inverted to open on accomplishment. The Free edition — the thing that
will actually be listed on Gumroad Discover, seen by far more people, and
judged first — still opened on debt: three tiles counting open tasks, unsorted
inbox, and projects. That is backwards for a paid product and worse for a free
one, because a free product only earns the upgrade if it is good enough to keep
using.

Free now mirrors Pro:

- A `Done This Week` formula, which Free did not have. Written with both bounds
  (`>= 0 and <= 7`) rather than copied, so a future-dated completion cannot
  inflate the number.
- **27 sample completed tasks** across Sep 6–19, giving a contiguous bar for
  every day. The persona is deliberately different from Pro's — an ordinary
  week of work, admin, health and home, not a course-shipping operator. Free
  and Pro are sold to different people and the sample data should say so.
- Two views: a green number, and the momentum column chart.
- The three debt tiles deleted; the page opens on the result and closes on the
  obligation.
- The upgrade callout moved from grey to orange. It is an invitation, and grey
  reads as fine print — the same argument as Pro's Sunday review callout.

**One number, not three.** Pro shows finished / goal progress / weeks reviewed.
Free has no Goals and no Reviews, so padding the row to three would have meant
inventing metrics. A single large green number is stronger than three weak
ones, and the absence is itself the upgrade argument.

Nine covers, using Free's **own** fourteen-day shape rather than Pro's. The
motif is only meaningful if it is that product's data; a copied shape would
make it decoration.

### The Gumroad listing, and what could not be automated

There is no Gumroad connector in the directory and `gumroad.com` is unreachable
from this environment, so the listing itself cannot be created from here. What
exists instead: `store/gumroad-listing.md` with the copy for both listings, and
`brand/gumroad/` with the five assets at the sizes Gumroad actually uses —
four 1280×720 covers and a 600×600 thumbnail, as separate layouts rather than
crops, because Gumroad shows covers at 16:9 and the library tile as a square.

Notion cannot publish a page to the web through this API either, so the two
"Duplicate as template" links have to come from the account owner.

**A rendering trap worth recording:** scaling a 1820px-wide device with a CSS
transform leaves its un-scaled box outside the viewport, and Chromium does not
paint what never landed there — half the laptop screen came back as bare page
background. Devices are now rendered standalone at natural size and placed as
`<img>`, which scales without a layout box. Same root cause as the 87px window
offset: **Chromium paints the viewport, not the layout.**

## The palette was invented, and the brand already existed

Everything visual in this repo was built on warm paper and green: the sheets,
the Gumroad layouts, twenty-four page covers, the accomplishment colour inside
the product. All of it chosen on reasoning — warmth drives approach, green
means progress — and none of it checked against the brand that already exists.

The live site is purple-violet on light lavender, with a near-black first line
and a gradient second line. A buyer who saw the site and then a Gumroad cover
would have seen two companies. No amount of colour psychology outranks that.

`brand/palette.md` now records the tokens, read off the site rather than
reasoned toward:

| Token | Hex |
|---|---|
| ink | `#0B0B14` |
| paper | `#F7F6FD` |
| gradient | `#4F52E8` → `#9B51E0` |
| cover base | `#0E0E18` |

The headline follows the site's own treatment — line one in ink, line two in
the gradient — rather than the grey-to-black split I had designed. The wordmark
is the site's lockup, **Nazzim نظّم**, not all-caps NAZZIM. DejaVu Sans carries
the Arabic; nothing bundled here has Arabic coverage, so it will not match the
site's Arabic face.

### What moved inside the product, and what did not

Purple took the surfaces the brand should own: the finished-this-week number,
the momentum chart, the hero callout. Goals moved to blue so two brand-adjacent
colours would not sit side by side.

Status and priority chips kept their colours. Those are Notion's semantics and
the user's own data — green for Completed, red for Overdue — and recolouring
them to purple would have cost meaning to gain nothing. That is a judgement,
stated here so it can be overruled.

### Covers now track the branch instead of a commit

Re-pointing twenty-four covers after every palette change is twenty-four API
calls that produce nothing. `raw.githubusercontent.com/.../refs/heads/<branch>/...`
resolves (verified, 200) and follows the branch, so a cover redesign now
propagates on push with no Notion calls at all.

The trade is immutability: a SHA-pinned cover can never break, a branch-pinned
one moves if files move. **Before launch these should be re-pinned to a SHA**,
because a template sold to strangers should not depend on a branch that is
still being edited.

### Credibility: what these images are, exactly

They are not screenshots. They are pixel-level recreations of the product's
real structure, rendered in HTML — which means every claim in them is something
I chose to draw, and three of them had been invented: a Today's plan that did
not exist, an overdue task that did not exist, and open "Next actions" that
were really completed rows.

Fixed by making the product true rather than the picture vaguer. Ten open tasks
now continue the same seeded story, two of them genuinely overdue; a Today's
plan row exists for the date the mockup shows, with the Focus line the mockup
quotes and a One Big Thing relation to the task it names.

**The remaining gap is honest and worth stating: a recreation is not a
screenshot.** Notion's own font stack, spacing and chart rendering differ in
small ways from anything drawn by hand. The only way to close it completely is
screenshots taken from the real workspace — which needs a signed-in browser,
and this environment has neither.
