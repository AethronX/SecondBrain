# Launch audit — 19 September 2026

Scored after inspecting the live product, not from memory. That distinction
matters: three of the defects below were things I believed were fine and were
not, and I only found them by opening the pages.

## Is it ready to sell?

**No. Four blockers, three of which only you can clear.**

| # | Blocker | Whose |
|---|---|---|
| 1 | The Free edition's upgrade link is still a placeholder | Yours — needs your Gumroad name |
| 2 | No Gumroad listing exists, and no "Duplicate as template" links | Yours |
| 3 | Page covers are pinned to a moving branch, not a commit | Mine, once the listing is live |
| 4 | Demo numbers decay with the calendar | Shared — re-seed on launch day |

Everything else is shippable.

## Scores, each out of ten

| Criterion | Score | What holds it back |
|---|---:|---|
| Problem solving & value | 9 | No money module; single-user only by design |
| Productivity system | 8 | `Recurring` is a property with no mechanism behind it |
| Ease of use | 8 | Nine databases and ~30 Task properties is a lot of surface |
| Information architecture | 8 | Every page's parent is a toggle page, so the sidebar tree reads oddly |
| Relations & intelligence | 10 | Nothing manual anywhere; this is the strongest part |
| Design & brand | 8 | Page icons are still Notion built-ins; covers depend on GitHub |
| Mobile & desktop | 8 | Never opened on a real phone; Analytics is heavy on mobile |
| Customization | 7 | Formulas reference literal option names — renaming one breaks them silently |
| Onboarding | 9 | Demo numbers shrink as the seeded fortnight recedes |
| Long-term retention | 7 | Nothing surfaces the fact that you stopped reviewing |
| **Average** | **8.2** | |

## Fixed in this pass

**The demo-data page was lying.** Its six tables filtered on a `Sample ·` title
prefix. The forty-odd rows seeded since then carry no prefix, so a buyer would
have followed the instructions exactly and been left with most of the demo data
still in place, invisible. The tables are now unfiltered and renamed *Every task
in the template*, a seventh was added for the daily log, which was never listed
at all, and a red warning says plainly that these views show everything — so
they must be used before your own work goes in, not after.

**Start Here pointed at a section that no longer exists.** It told a new user
the capture box sits under *Do this next*; the home page was rebuilt around
*Now, today* and no such heading remains. It also repeated the `Sample ·` claim.
Both corrected.

**The Free edition's upgrade line was a note to myself** — "replace this line
with your store link" — sitting in the product in neutral grey, easy to ship by
accident. It is now a red warning block naming the exact URL shape to paste. If
it ships unfilled it will be obvious rather than silent.

## What cannot reach ten, and why

Three of these are Notion's limits, not the product's:

- **Recurring tasks.** The `Recurring` property exists; nothing acts on it.
  Notion cannot create a row on a schedule without a button or an automation
  this API cannot write. Either build it as a documented manual habit or remove
  the property — a control that does nothing is worse than no control.
- **No nudge when you stop.** Retention rests on the weekly review, and nothing
  tells you that you skipped three. A *days since your last review* number on
  the home page is buildable from the Reviews database and is the single highest
  -value addition left.
- **Renaming a select option silently breaks formulas.** `Today Tier`, `Open`,
  `Overdue` and `Health` all test literal strings like `"Completed"` and
  `"P1 Critical"`. A buyer who renames a status gets wrong numbers with no
  error. I have not verified whether Settings & Help warns about this; if it
  does not, it must.

**A note on the ask.** Ten out of ten on every line is not reachable here, and
reporting it would be the inflation this audit exists to avoid. 8.2 with named,
mostly-fixable gaps is a more useful number than a 10 that does not survive
contact with a buyer.
