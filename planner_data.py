"""Reference data for the Home Systems Register and Replacement Fund Forecaster.

This is the whole of what the planner knows. `build_planner.py` reads it and
writes the `Reference Data` and `Lists` tabs; nothing else in the workbook holds
a number that came from us.

Three things about this file are deliberate.

**The base numbers are Gulf South, not national.** The kit already prints
lifespans on its Big Ticket Watch List and says out loud why they run shorter
than the figures online. If this file carried national averages the same buyer
would own two products that disagree about their own roof. `KIT_ITEMS` maps the
overlapping systems onto `WATCH_LIST` in `build_printables.py` and
`check_against_kit()` fails the build if a default ever falls outside the range
the kit prints. That check is the only thing stopping the two from drifting.

**Region is a factor, not a rewrite.** Everything outside the Gulf South is
reached by the two factors in `REGIONS`, applied at the top of the register.
Cost scales for every system. Lifespan scales only for the ones flagged
`exposure` here, because heat, humidity and UV shorten a roof and do nothing at
all to a dishwasher. A regional edition is a factor change, and if it ever needs
to be more than that, it needs its own copy of `SYSTEMS` rather than a fudge.

**Costs are defaults, not quotes.** Every row carries a range as well as a
point figure, both tabs say so, and the register has an override column beside
each one. See "Costs in the planner" in HANDOFF.md for why this product carries
dollar amounts when the earlier note said not to.

Costs are 2026 dollars, installed, Gulf South, before the regional factor.

Columns, in order:
    system, category, life, life_range, cost, cost_range, tier, exposure, source
"""

# What the source note means, spelled out because "estimate" has to be honest:
#   kit          the lifespan is the one the kit prints. Locked by check_against_kit().
#   consensus    widely published figure, in the middle of what the trade sources agree on
#   estimate     our figure. Directional. Verify before relying on it for a real budget.
SYSTEMS = [
    # system, category, life, life_range, cost, cost_range, tier, exposure, source
    ("Roof - asphalt shingle, 3-tab", "Roof & Structure", 12, "12-15", 9500, "6,000-14,000", 1, "Yes",
     "kit lifespan; cost consensus, full tear-off and replace on a typical single-story"),
    ("Roof - asphalt shingle, architectural", "Roof & Structure", 15, "12-15", 12500, "8,000-18,000", 1, "Yes",
     "kit lifespan; cost consensus. Rated far longer nationally, shortened here for Gulf exposure"),
    ("Roof - metal", "Roof & Structure", 35, "30-40", 22000, "14,000-35,000", 1, "Yes",
     "kit lifespan; cost consensus, standing seam"),
    ("Roof - tile, concrete or clay", "Roof & Structure", 35, "30-50", 26000, "15,000-45,000", 1, "Yes",
     "consensus. Tile outlasts its underlayment, which is the part that actually fails"),
    ("Gutters & downspouts", "Roof & Structure", 20, "15-25", 1800, "1,000-3,500", 2, "Yes",
     "consensus, seamless aluminum"),
    ("Siding - vinyl", "Roof & Structure", 25, "20-35", 12000, "7,000-20,000", 2, "Yes", "consensus"),
    ("Siding - fiber cement", "Roof & Structure", 30, "25-50", 18000, "11,000-28,000", 2, "Yes", "consensus"),
    ("Exterior paint", "Roof & Structure", 6, "5-7", 4500, "2,500-8,000", 2, "Yes",
     "kit lifespan; cost consensus, two-story repaint"),
    ("Exterior caulk & sealants", "Roof & Structure", 3, "2-4", 600, "300-1,200", 2, "Yes",
     "kit lifespan; cost estimate, whole-house re-caulk by a painter"),
    ("Windows - whole house", "Roof & Structure", 20, "15-25", 14000, "8,000-25,000", 2, "Yes",
     "kit lifespan; cost consensus, around 12 openings"),
    ("Exterior doors", "Roof & Structure", 25, "20-40", 2200, "1,000-4,500", 2, "Yes", "consensus, per door installed"),
    ("Garage door", "Roof & Structure", 22, "15-30", 2400, "1,200-4,500", 2, "Yes", "consensus, single double-wide door"),
    ("Garage door opener", "Roof & Structure", 11, "10-12", 650, "400-1,100", 3, "No",
     "kit lifespan; cost consensus"),
    ("Chimney / flue liner", "Roof & Structure", 25, "15-50", 4000, "2,000-8,000", 2, "No", "consensus"),
    ("Attic insulation", "Roof & Structure", 30, "20-40", 2500, "1,500-5,000", 2, "No",
     "consensus. Blown-in settles rather than fails, so this is a top-up interval"),
    ("Foundation vapor barrier", "Roof & Structure", 12, "8-20", 3000, "1,500-6,000", 2, "Yes",
     "estimate, crawlspace encapsulation liner only"),

    ("HVAC condenser - outdoor unit", "HVAC", 11, "10-12", 6500, "4,500-10,000", 1, "Yes",
     "kit lifespan; cost consensus, 3-ton condenser and coil"),
    ("HVAC air handler / furnace", "HVAC", 16, "15-18", 5000, "3,000-8,000", 1, "No",
     "kit lifespan; cost consensus"),
    ("Ductwork", "HVAC", 18, "15-20", 4500, "2,500-9,000", 2, "No", "kit lifespan; cost consensus, full replacement"),
    ("Mini-split heat pump", "HVAC", 14, "10-20", 5000, "3,000-9,000", 2, "Yes", "consensus, two-head system"),

    ("Water heater - tank", "Plumbing", 9, "8-10", 2000, "1,300-3,500", 1, "No",
     "kit lifespan; cost consensus, 50 gallon installed"),
    ("Water heater - tankless", "Plumbing", 18, "15-20", 4200, "3,000-7,000", 1, "No", "consensus, installed"),
    ("Water heater anode rod", "Plumbing", 4, "4-5", 175, "100-300", 3, "No",
     "kit lifespan; cost estimate. The cheapest line here and the one that buys the tank above"),
    ("Water softener", "Plumbing", 12, "10-15", 2200, "1,200-4,000", 3, "No", "consensus"),
    ("Well pump", "Plumbing", 12, "8-15", 2200, "1,200-4,500", 1, "No", "consensus, submersible"),
    ("Sump pump", "Plumbing", 8, "7-10", 900, "500-1,800", 1, "No", "consensus"),
    ("Septic tank pump-out", "Plumbing", 4, "3-5", 500, "300-900", 1, "No",
     "kit interval; cost consensus. A service, not a replacement, and it repeats forever"),
    ("Septic drain field", "Plumbing", 28, "20-40", 12000, "6,000-25,000", 1, "No",
     "consensus. The single largest number most homeowners have never heard of"),
    ("Toilets", "Plumbing", 25, "15-35", 450, "250-900", 3, "No", "consensus, per toilet installed"),
    ("Faucets", "Plumbing", 15, "10-20", 300, "150-700", 3, "No", "consensus, per faucet installed"),
    ("Supply lines - braided", "Plumbing", 7, "5-10", 120, "60-250", 1, "No",
     "consensus. Tier 1 for what it costs to ignore, not for what it costs to replace"),
    ("Garbage disposal", "Plumbing", 10, "8-12", 350, "200-700", 3, "No", "consensus"),

    ("Main electrical panel", "Electrical", 35, "25-50", 3200, "1,800-5,500", 1, "No", "consensus, 200 amp service"),
    ("Whole-house generator", "Electrical", 18, "15-25", 12000, "7,000-20,000", 2, "No",
     "consensus, standby unit with transfer switch and pad"),
    ("Smoke & CO detectors", "Electrical", 9, "7-10", 350, "150-700", 1, "No",
     "consensus. Manufacturers date-stamp these and they expire whether or not they beep"),

    ("Refrigerator", "Appliances", 12, "10-13", 1900, "900-3,500", 2, "No", "kit lifespan; cost consensus"),
    ("Range / oven", "Appliances", 14, "12-17", 1400, "700-3,000", 2, "No", "consensus"),
    ("Dishwasher", "Appliances", 9, "9", 900, "500-1,600", 3, "No", "kit lifespan; cost consensus"),
    ("Microwave - over-range", "Appliances", 9, "8-10", 500, "250-1,000", 3, "No", "consensus"),
    ("Washer", "Appliances", 11, "10-13", 950, "500-1,800", 2, "No", "kit lifespan; cost consensus"),
    ("Dryer", "Appliances", 12, "10-13", 900, "500-1,700", 2, "No", "kit lifespan; cost consensus"),

    ("Flooring - carpet", "Interior", 9, "5-15", 3500, "2,000-7,000", 3, "No", "consensus, whole house"),
    ("Flooring - luxury vinyl plank", "Interior", 20, "15-25", 6000, "3,500-12,000", 3, "No", "consensus, whole house"),
    ("Flooring - hardwood refinish", "Interior", 12, "10-15", 3500, "2,000-6,500", 3, "No",
     "consensus. A refinish interval, not a replacement. The floor itself outlives the house"),
    ("Interior paint", "Interior", 8, "5-10", 3000, "1,800-6,000", 3, "No", "consensus, whole house"),
    ("Countertops", "Interior", 25, "20-40", 4500, "2,500-9,000", 3, "No",
     "estimate. Replaced for taste far more often than for wear"),

    ("Deck - wood", "Outdoor", 15, "10-20", 6500, "3,500-13,000", 3, "Yes", "kit lifespan; cost consensus"),
    ("Fence - wood", "Outdoor", 12, "10-15", 4500, "2,500-9,000", 3, "Yes",
     "kit lifespan; cost consensus, around 150 linear feet"),
    ("Driveway - concrete", "Outdoor", 30, "25-40", 8000, "4,500-15,000", 3, "Yes", "consensus, two-car driveway"),
]

# Region, cost factor, lifespan factor, note. Both factors are relative to the
# Gulf South, which is why it sits at 1.00 on both: it is the base the numbers
# above were written for, not the average of the seven.
#
# The lifespan factor only reaches systems flagged `exposure` in SYSTEMS. It is
# above 1.00 everywhere else on the list because nowhere else on it combines
# this much heat, humidity and UV. That is the same claim the kit makes on the
# Watch List, applied in the other direction.
REGIONS = [
    ("Gulf Coast", 1.00, 1.00, "Base. Every other row is relative to this one"),
    ("Southeast", 1.00, 1.05, "Similar labor and materials, marginally less exposure"),
    ("Northeast", 1.25, 1.15, "Highest labor cost on the list. Freeze-thaw replaces UV as the driver"),
    ("Midwest", 1.05, 1.15, "Moderate cost, long exterior life, hard on anything holding water"),
    ("Southwest", 1.05, 1.05, "UV as punishing as the Gulf, without the humidity"),
    ("Mountain", 1.10, 1.15, "Freight and snow load. Roofs age on snow rather than heat"),
    ("Pacific NW", 1.20, 1.20, "High labor cost, mild UV, and the longest exterior life on the list"),
]

# The twelve almost every house has. The Quick Check tab is built from these and
# nothing else, because its whole job is an answer in sixty seconds from one
# number: a new owner should not have to scroll past well pumps and septic drain
# fields to find out about their roof. The register carries all 49.
#
# `docs/calculator/index.html` shows four of these twelve, and
# `build_calculator.py` checks its four are a subset of this list, so a lifespan
# cannot be free at one number and paid at another.
COMMON = [
    "Roof - asphalt shingle, architectural",
    "HVAC condenser - outdoor unit",
    "HVAC air handler / furnace",
    "Ductwork",
    "Water heater - tank",
    "Water heater anode rod",
    "Windows - whole house",
    "Exterior paint",
    "Exterior caulk & sealants",
    "Main electrical panel",
    "Refrigerator",
    "Dishwasher",
]

# What the Quick Check tab offers instead of a date. No "Known" option: if you
# know the year, that is the register's job and this tab is the ramp onto it.
QUICK_STATUSES = [
    "Replaced on schedule",
    "Never replaced",
    "Roughly half way",
    "Not in my house",
]

INSTALL_STATUSES = [
    "Known",
    "IDK - Assume Original",
    "IDK - Assume Mid-Life",
    "IDK - Assume On Schedule",
]

# Identical wording to the calendar, the kit and the binder. The bundle only
# reads as one system if the tier names match everywhere, so these are not free
# to reword here.
TIERS = ["1 - Critical", "2 - Important", "3 - Nice to have"]

YES_NO = ["Yes", "No"]

# planner system name -> the item as the kit's Watch List prints it.
KIT_ITEMS = {
    "Roof - asphalt shingle, 3-tab": "Roof, asphalt shingle",
    "Roof - asphalt shingle, architectural": "Roof, asphalt shingle",
    "Roof - metal": "Roof, metal",
    "Water heater - tank": "Water heater, tank",
    "Water heater anode rod": "Water heater anode rod",
    "HVAC condenser - outdoor unit": "A/C condenser (outdoor)",
    "HVAC air handler / furnace": "Furnace / air handler",
    "Ductwork": "Ductwork",
    "Exterior paint": "Exterior paint",
    "Exterior caulk & sealants": "Exterior caulk & sealants",
    "Windows - whole house": "Windows",
    "Garage door opener": "Garage door opener",
    "Dishwasher": "Dishwasher",
    "Refrigerator": "Refrigerator",
    "Washer": "Washer / dryer",
    "Dryer": "Washer / dryer",
    "Septic tank pump-out": "Septic tank, pump out",
    "Fence - wood": "Fence, wood",
    "Deck - wood": "Deck, wood",
}


def _kit_range(text):
    """Pull the low and high years out of a Watch List string.

    The kit writes these for a reader rather than a parser: "12-15 years",
    "9 years", "every 3-5 years", with an en dash. Anything it cannot read it
    refuses to guess at, so a reworded kit entry fails the check below rather
    than passing it by accident.
    """
    digits, numbers = "", []
    for ch in text:
        if ch.isdigit():
            digits += ch
        else:
            if digits:
                numbers.append(int(digits))
            digits = ""
    if digits:
        numbers.append(int(digits))
    if not numbers:
        raise ValueError("no years found in kit lifespan {0!r}".format(text))
    return numbers[0], numbers[-1]


def check_against_kit():
    """Fail the build if a shared lifespan drifts from the one the kit prints.

    The kit is the published number: it is in a PDF on a listing, and a buyer
    who owns both products can hold them side by side. So this compares rather
    than imports, and the planner is the one that has to move.
    """
    from build_printables import WATCH_LIST

    kit = dict(WATCH_LIST)
    problems = []
    for system, _cat, life, _lr, _c, _cr, _t, _e, _s in SYSTEMS:
        item = KIT_ITEMS.get(system)
        if item is None:
            continue
        if item not in kit:
            problems.append("{0}: kit no longer lists {1!r}".format(system, item))
            continue
        low, high = _kit_range(kit[item])
        if not low <= life <= high:
            problems.append("{0}: {1} yrs is outside the kit's {2} for {3!r}".format(
                system, life, kit[item], item))
    if problems:
        raise SystemExit(
            "planner and kit disagree about lifespans:\n  " + "\n  ".join(problems) +
            "\n\nThe kit is published, so fix planner_data.py rather than the kit.")
    return len(KIT_ITEMS)
