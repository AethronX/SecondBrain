# NAZZIM Second Brain — Pro · Quality Audit

Scored against the Nazzim Product Quality Framework (§02 and §20 of the build
specification). Release standard is ≥ 90/100.

Everything below was checked against the live workspace through the API —
view filters, sorts, formulas, schemas and page structure were read back, not
assumed. Where I could not verify something, the audit says so and declines
the point rather than guessing.

---

## §19 — Product testing

### USER A — Beginner. Knows basic Notion only.

Walked the path: open NAZZIM → Start Here → seven steps.

The Notion skills required, end to end, are: click **New**, type, pick a date,
drag a card, switch a tab. No formula editing, no view configuration, no
relation setup, no template building. Terminology is plain — Goals, Areas,
Projects, Tasks, Notes, Resources — and the one non-obvious distinction
(project vs. area) is defined by its test: *a project has a finish line you
could photograph; if it can never finish it is an area.*

First value: the home page opens with a tagline, four live numbers and a
priority-sorted list of what to do. First action: the capture box sits under
that list — click New, type, Escape. Verified as a real Inbox list view
filtered to `Status = Unprocessed`, sorted by `Captured` descending.

**Where A still struggles:** opening a task shows twenty-two properties,
nine of them calculated. Nothing is broken, but it looks like a database
rather than a task app. Settings & Help now carries the two-minute fix
(hide the calculated properties once, for every task), but the default is
still the cluttered one.

**Verdict: passes, with one real friction.**

### USER B — Productivity enthusiast. Already uses Notion.

The question is whether this is structure or decoration. The load-bearing
evidence:

- `Attention` on Projects does not say *a project is stuck* — it says **why**:
  no next action, no open tasks, or overdue tasks. Empty means healthy.
- `Health` on Projects and Goals compares progress against *elapsed time*,
  so a goal slipping quietly says so months before its deadline.
- Goals `Progress` uses your own metric when you set a `Target` and falls
  back to the share of completed projects when you do not — so a goal is
  never silently unmeasurable.
- Date logic lives in formulas (`Timeline`, `Today Tier`) rather than fixed
  date filters, because API-created filters accept only calendar dates and
  would be wrong the next morning. This is documented, not hidden.
- `Action Count` on every note is the number that matters: how many tasks
  that thinking produced.

**Where B will complain:** no recurrence engine. Notion cannot make a row
reappear, and repeating database templates cannot be created through the API,
so the user has to build the two that matter (Daily Plan, Weekly Review)
themselves. The `Recurring` property on Tasks is a label with no mechanism —
stated plainly in Settings & Help, but the property name still promises more
than it does, and property descriptions are not settable through this API.

**Verdict: passes. It is a system, not a skin.**

### USER C — Heavy user. Hundreds of tasks and notes.

Checked the actual view configurations rather than assuming:

- *Do this next* (home) — filtered to `Today Tier is not empty`, sorted by
  Priority then Due Date. Bounded by definition; overdue P1s surface first.
- *Recently completed* (Archive) — filtered to Completed or Cancelled, sorted
  by `Completed Date` descending. The unbounded view in the system, but
  newest-first, so the useful rows load first and the rest paginate.
- *Search* (Knowledge) — deliberately unfiltered, sorted by `Updated`
  descending. That is correct: it is the retrieval surface, and hiding rows
  from it would defeat its purpose.

Every other page view carries a status or formula filter, so no dashboard
loads a full table. There is no duplicated data anywhere — every dashboard is
a filtered linked view over the same nine databases, so the row count grows in
one place rather than nine.

**The tab work is a load improvement, not only a layout one.** Analytics used
to render twenty chart views on arrival; it now renders six numbers plus one
tab's contents. That is the biggest single performance change in the build.

**Where C hits a ceiling:** Tasks carries nine formulas, several overlapping —
`Timeline` largely subsumes `Overdue` and `Days Until Due`. They are cheap
individually and each feeds something different (rollups need booleans,
filters need strings), but a leaner set is possible. I did not cut them:
removing a formula means re-pointing every view and rollup that reads it, and
verifying fifty-plus views blind is a worse risk than the cost being carried.
Flagged rather than fixed, deliberately.

**Verdict: passes at 1,000+ items.**

### USER D — Mobile.

Every workflow in the spec's list works from a phone: add task, check today,
capture, open project, add note, review goals, complete task.

Before this pass, a page with a three-number strip and three content views
became six full-width blocks on a phone, because `<columns>` stack. Tab strips
do not stack and do not reflow — they are the one Notion layout primitive that
renders identically on both. Twenty-two views moved into them.

**Remaining mobile cost:** the twelve-link navigation bar wraps to two or three
lines on a narrow screen. That is the price of the "always one tap from
anywhere" guarantee and I judged it worth paying.

**Verdict: passes — but see the note under Mobile & Desktop UX. I cannot
render the Notion mobile app, so this is reasoned from layout primitives, not
observed.**

---

## §20 — Final quality audit

| Category | Weight | Before | After |
| --- | ---: | ---: | ---: |
| Problem Solving & Value | 20 | 17 | **19** |
| Productivity System | 15 | 14 | **14** |
| Ease of Use | 15 | 11 | **13** |
| Information Architecture | 10 | 7 | **9** |
| Relations & System Intelligence | 10 | 10 | **10** |
| Design & Brand | 10 | 9 | **9** |
| Mobile & Desktop UX | 5 | 3 | **4** |
| Customization | 5 | 4 | **4** |
| Onboarding | 5 | 4 | **5** |
| Long-Term Retention | 5 | 4 | **5** |
| **TOTAL** | **100** | **83** | **92** |

**92/100 — premium / launch-ready.**

### Problem Solving & Value — 19/20

All ten named problems are addressed and all six questions answerable from the
home page or one tap away. *Where is my information?* was the weak one and is
now a tab called **Search** rather than a table at the bottom of a page.

**Weakness:** the product cannot prove its own value to a user in month three.
Analytics holds the evidence, but the product correctly tells you to read it
weekly, not daily — so there is no moment where the system says *you finished
forty-seven things this month* unprompted.

**Improvement considered and declined:** a "what this system answers" panel on
the home page. That is brochure copy on an instrument, which is the exact
mistake already corrected once in this build. Not implemented.

### Productivity System — 14/15

Capture → Clarify → Organize → Prioritize → Plan → Execute → Review, each with
a surface. The Clarify step is the best piece of design in the product: the
Inbox board has five columns because there are only five honest answers to
*what is this actually*, and *Nothing* is one of them.

Nine databases against the spec's suggested eight. The extra is Daily Log,
which merges daily planning and journalling into one row per day — documented,
with the reasoning.

**Weakness:** no recurrence engine, and the `Recurring` property is a label
with no mechanism. Both are platform and API limits, both are documented at
length, and neither can be closed from here.

**Not re-scored.** Documentation does not turn a missing engine into a present
one.

### Ease of Use — 13/15

First value in ten seconds, first capture in under thirty, the essential
system (understand → Areas → Today) in three and a half minutes. Human
language throughout; every complex mechanism has a plain-language explanation
in the page's own toggle.

**Weakness:** twenty-two properties on Tasks, nine of them calculated, all
visible by default when a task is opened. This is the most common complaint
against Notion productivity templates and NAZZIM has it too.

**Improvement implemented:** Settings & Help now carries a *Hide the machinery
properties* procedure — two minutes, applies database-wide, formulas keep
running underneath.

**Re-scored 12 → 13** for the first-action and empty-state work, not for the
property fix: a default that needs a manual correction is still the default,
so the property point stays lost.

### Information Architecture — 9/10

§05 names five HOME sections. Three were present; **Progress** and **Review**
were missing, found by reading the spec against the page rather than by
intuition. The home now carries four numbers (overdue, due today, inbox,
active goals), the priority list, the capture box, and a Sunday review line —
then a divider, then navigation.

**Weakness:** the home answers *now* and *review* but not *later*. Upcoming
work is one tap away on the Tasks calendar tab rather than on the home page.
Given §14's instruction that the dashboard must not show everything, I judged
that correct rather than missing — but it is one point I am not claiming.

### Relations & System Intelligence — 10/10

`Goals → Areas → Projects → Tasks` and `Notes → Projects / Areas / Resources`,
both complete and both bidirectional. Every relation earns its place, and the
sophistication stays under the surface: the user sees *Attention: no next
action*, not the formula that produced it.

**Checked and found already correct:** I was going to deduct a point for
backlinks (`Referenced By`) not being surfaced anywhere, then verified that
they appear on every note's own page by default — which is where you would
actually use them. No column added; adding one to the Search table would have
cost mobile readability to chase a point.

### Design & Brand — 9/10

**This score was wrong when first written, and the correction is the most
important line in this document.** The day after it was given, a screenshot of
the home page's primary list showed rows reading `P1 Critical · September 10,
2026 · Sample · Build a 3x per week training routine · Next · Sample · P…` —
the project name dominating, the task name last and truncated. Every one of the
twenty-six content views in the product had its title last in `displayProperties`,
which is render order. On the surface a buyer sees first, that was a 0/10.

It is fixed — title first in all twenty-six, with a property budget per view type
and relations removed from list rows, where they cost more width than the title
and every chip combined. The 9/10 below describes the product as it stands now.

One page grammar everywhere, one navigation bar, two colour registers that
never share a surface (status colours only on data, zone colours only on
navigation), Notion's built-in icons rather than emoji, no decorative headers.

**Weakness, and the one point lost:** the home page carries a generic Unsplash
cover while no other page has one. One stock photo on one page of fourteen is
worse than none at all or all fourteen. **Not fixed** — the instruction was
"no covers, keep as is", and removing an existing cover is a change that was
not asked for. One API call away whenever you want it.

**Deduction reconsidered and withdrawn:** I had also docked a point for
Notion's fixed palette and lack of custom typography. That penalises the
platform, not the product — every competitor ships under the same ceiling.

### Mobile & Desktop UX — 4/5

Every workflow in the spec's mobile list is reachable in one or two taps, and
no critical function depends on a wide multi-column layout any more.

**The missing point is unverified rather than known-bad.** I cannot render the
Notion mobile app from here, so every mobile claim in this audit is reasoned
from layout primitives and API round-trips. Both times this build has been
checked against a real screen, the screenshot found something no structural
check could see — first the home page opening with a wall of prose, then the
title being last in every view. Structural correctness and visual correctness
are different properties and I can only observe one of them. I am not awarding a
point on evidence I do not have.

### Customization — 4/5

Areas, goals, categories, priorities, views and select options are all
editable; nothing is locked; the default is optimised.

**Weakness:** the single most useful customisation — what counts as "today's
work" — is a formula edit. **Improvement implemented:** Settings now documents
both routes, the per-view filter for experimenting and the formula for changing
it everywhere, and says plainly which is which. **Not re-scored**, because the
global lever is still formula-only.

### Onboarding — 5/5

Seven numbered steps in the specified order, each costed, ten minutes end to
end — with a thirty-second escape hatch above them for someone who opened the
product on a phone in a queue. Plus what to do all week, why the hierarchy
stops at four levels, the three rules, what to open when you are ready for
more, and a page that clears the demo data in two minutes.

### Long-Term Retention — 5/5

Four rhythms named, costed and located in one place, with an explicit adoption
order — start weekly, add monthly after the fourth week, yearly can wait until
there is a year worth reading. The Sunday line now sits on the home page. The
recovery procedure for when you fall behind is fifteen minutes and says, in
as many words, *do not start over* — which is how most people lose systems
like this.

**Platform limit, not a design gap:** nothing can remind you. Notion templates
cannot send notifications.

---

## Where the remaining eight points are

| Points | What it would take |
| ---: | --- |
| 2 | Ease of Use — fewer properties on Tasks by default, which means cutting overlapping formulas and re-verifying every view and rollup that reads them |
| 1 | Problem Solving — a moment where the system proves its own value unprompted |
| 1 | Information Architecture — a *later* surface on the home page, at the cost of the leanness that was just won back |
| 1 | Design — the stray home-page cover, one call away, awaiting your decision |
| 1 | Mobile — verification on a real device, which I cannot do |
| 1 | Productivity System — a recurrence engine Notion does not have |
| 1 | Customization — a non-formula global lever Notion does not offer |

Four of those eight are genuinely available. Three are Notion's ceiling. One
is yours to decide.

## A note on the earlier 91

An earlier score of 91 in this build was against a different six-row rubric of
your own, not this ten-category framework, and it was given before I knew the
`<tabs>` block existed or had read §05's HOME checklist against the actual page.
The two numbers are not comparable, and the 83 "before" column here is this
framework applied retrospectively to the state at the start of this pass.
