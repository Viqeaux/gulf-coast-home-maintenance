"""The lists, labels and rule text the storm season workbook is built from.

`build_workbook.py` holds the layout and the formulas; everything here is
content, and it is **paid product only and must not reach the site**, the same
as `binder_pages.py`, `task_steps.py`, `kit_sections.py` and `planner_data.py`.

**The rooms and the supply rules are imported from the binder, not retyped.**
A buyer who owns both products works from the paper pages into the sheet, and a
room called "Living and family room" on paper and "Living room" in the workbook
makes them stop and translate. `check_against_binder()` fails the build if the
two ever drift, which is the same trick `planner_data.check_against_kit()` plays
against the kit's Watch List.

The supply table is a subset on purpose. The binder has twelve rows and two of
them, prescriptions and batteries, are "check every bottle" and "count them".
Those are not arithmetic, they belong on paper, and putting them in a column
headed "Your number" would print a zero next to something that matters.
"""

from binder_pages import CONTRACTOR_CHECKS, INVENTORY_ROOMS, SUPPLY_ROWS

# The nine inventory sections, character-identical to the binder's tabs.
ROOMS = [name for name, _prompt, _rows in INVENTORY_ROOMS]

# Policy sub-limits. These six are the categories that are commonly capped well
# below the contents limit, and they are the ones the binder's warning names.
SPECIAL = ["Jewelry", "Firearms", "Cameras & electronics", "Tools",
           "Art & collectibles", "Cash"]

# What goes in the inventory's Special category column. "None" is first so the
# common case is one keystroke away.
SPECIAL_WITH_NONE = ["None"] + SPECIAL

SUBLIMIT_HELP = ("Commonly $1,000 to $2,500 for the whole category, whatever your "
                 "contents limit says. Read your declarations page and enter yours.")

WIND_TYPES = ["Percentage of dwelling", "Flat dollar amount"]

# Damage causes, in the insurer's own words. No em dashes anywhere in the
# workbook, including inside a dropdown value, because these strings are also
# SUMIF criteria and a punctuation fix later would silently break a subtotal.
CAUSES = ["Wind", "Wind-driven rain", "Tree", "Flood", "Surge",
          "Unknown, described below"]
WIND_SIDE = ["Wind", "Wind-driven rain", "Tree"]
FLOOD_SIDE = ["Flood", "Surge"]
UNCATEGORIZED = "Unknown, described below"

RECEIPT_CATEGORIES = ["Lodging", "Meals", "Laundry", "Storage", "Transport",
                      "Mitigation supplies", "Generator fuel", "Other"]
# Loss of use draws on its own limit. Mitigation does not, and the tab says so.
ALE_CATEGORIES = ["Lodging", "Meals", "Laundry", "Storage", "Transport"]
MITIGATION_CATEGORIES = ["Mitigation supplies", "Generator fuel"]

YES_NO = ["Yes", "No"]
REPAIRED = ["Yes", "No", "In progress"]
REIMBURSED = ["Yes", "No", "Partial"]
CHECK_ANSWERS = ["Yes", "No", "Pending"]

# The ten contractor checks. Nine come off the binder's vetting page; the tenth,
# verifying the license on the state board site rather than reading it off the
# card, is split out of the first one because they are two different actions and
# only one of them is the one people skip.
CHECKS = [
    ("State license number on the estimate", CONTRACTOR_CHECKS[0][1]),
    ("License verified on the state board site",
     "Type the number into the state licensing board's own search. A number that "
     "does not come back, or comes back expired, ends the conversation."),
    ("Liability certificate, sent by their agent", CONTRACTOR_CHECKS[1][1]),
    ("Workers compensation certificate", CONTRACTOR_CHECKS[2][1]),
    ("A local physical address", CONTRACTOR_CHECKS[3][1]),
    ("Three local references, called", CONTRACTOR_CHECKS[4][1]),
    ("Written scope, materials by brand and model", CONTRACTOR_CHECKS[5][1]),
    ("They pull the permit, in their name", CONTRACTOR_CHECKS[6][1]),
    ("Payment schedule in writing, deposit a third or less", CONTRACTOR_CHECKS[7][1]),
    ("Lien waiver agreed at final payment", CONTRACTOR_CHECKS[8][1]),
]

# The eight red flags, short enough to be a row label. The long form is on the
# binder's scam page, which is where the reasoning lives.
RED_FLAGS = [
    "They knocked on your door",
    "Offered to waive, absorb or cover your deductible",
    "The price is only good today",
    "Large cash deposit before materials are ordered",
    "Asked for an assignment of benefits",
    "Wants to inspect the roof alone",
    "Out of state plates, no license number on the estimate",
    "Discouraged involving your insurer",
]

# (index into the binder's SUPPLY_ROWS, unit, what to put in Your number, format)
SUPPLY = [
    (0, "gallons", "=$B$4*$B$6", "0"),
    (1, "gallons", "=$B$4*$B$6*0.5", "0"),
    (2, "gallons", "=$B$5*$B$6", "0"),
    (3, "meals", "=$B$4*$B$6*3", "0"),
    (4, "days", "=$B$5*$B$6", "0"),
    (5, "bags", "=$B$7*$B$6", "0"),
    (6, "dollars", "=$B$4*100", '"$"#,##0'),
    (8, "tanks to fill", "=$B$8", "0"),
    (9, "gallons", '=IF($B$9="Yes",ROUNDUP($B$10/9*5,0)*$B$6,0)', "0"),
    # Two tanks is two tanks. It does not depend on any input, so it is written
    # as the constant it is rather than dressed up as arithmetic.
    (10, "tanks", 2, "0"),
]


def supply_rows():
    """The supply table, with the binder's own label and rule text on each row."""
    out = []
    for index, unit, value, fmt in SUPPLY:
        label, rule, _arithmetic = SUPPLY_ROWS[index]
        out.append((label, rule, unit, value, fmt))
    return out


def check_against_binder():
    """Fail the build if the workbook and the binder have drifted apart.

    Both of these are cheap to get wrong in a way nothing else notices: a room
    renamed here still produces a working dropdown and a working SUMIF, it just
    stops matching the paper the buyer is copying from.
    """
    problems = []
    if len(ROOMS) != 9:
        problems.append("the binder has {0} inventory sections, not 9".format(len(ROOMS)))
    if len(set(ROOMS)) != len(ROOMS):
        problems.append("two rooms share a name, which would double a SUMIF")
    if len(CONTRACTOR_CHECKS) != 9:
        problems.append("the binder's contractor page has {0} checks, not 9"
                        .format(len(CONTRACTOR_CHECKS)))
    if len(CHECKS) != 10:
        problems.append("the score is out of 10 and there are {0} checks".format(len(CHECKS)))
    if len(RED_FLAGS) != 8:
        problems.append("the red flag block is built 8 rows deep")
    for name in SPECIAL + CAUSES + RECEIPT_CATEGORIES + ROOMS:
        if "—" in name or "–" in name:
            problems.append("{0!r} has a dash in it that will not survive a fix".format(name))
    for label, _rule, _unit, _value, _fmt in supply_rows():
        if not label:
            problems.append("a supply row lost its label")
    if problems:
        raise SystemExit("the workbook and the binder disagree:\n  " + "\n  ".join(problems))
    return len(ROOMS)
