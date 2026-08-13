#!/usr/bin/env python3
"""
Build the three Gulf Coast Home Maintenance calendar feeds (.ics).

One file per tier: Must Do, Should Do, Going Above.
Twelve all-day events each, recurring yearly with no end date, matching the
undated print edition.

Run:  python build_calendars.py
Out:  docs/gulf-coast-must-do.ics
      docs/gulf-coast-should-do.ics
      docs/gulf-coast-going-above.ics

Editing content: change TASKS below and re-run. If subscribers already have the
feed, bump SEQUENCE so calendar clients treat it as an update.
"""

import os
from datetime import date, timedelta

# --- Build constants -------------------------------------------------------

# Anchor year for the first occurrence. The events recur yearly forever, so this
# only decides how far back the series starts, not when it ends.
ANCHOR_YEAR = 2026

# Bump on every content change you publish, so subscribers pick up the edit.
SEQUENCE = 0
DTSTAMP = "20260813T000000Z"

UID_DOMAIN = "gulfcoast-home-maintenance"

# GitHub Pages can only serve a site from the repo root or from /docs — not from
# an arbitrary folder — so the build lands in docs/ and Pages needs no config.
OUT_DIR = "docs"

DISCLAIMER = (
    "General maintenance guidance, not a substitute for a licensed inspector, "
    "contractor, or your insurance policy terms."
)

# Calendar names lead with the tier because sidebars truncate. "Gulf Coast Home
# Mainten..." is what a subscriber actually sees otherwise, which hides the one
# word that distinguishes the three feeds from each other.
#
# COLOR is RFC 7986 (CSS3 color names) and X-APPLE-CALENDAR-COLOR is Apple's
# hex equivalent, both matched to the print tiers. Apple and some other clients
# honor them. Google ignores both and assigns its own color per subscriber, so
# the tier has to be legible from the name alone.

TIERS = {
    "must": {
        "file": "gulf-coast-must-do.ics",
        "name": "Must Do — Gulf Coast Home Maintenance",
        "color": ("firebrick", "#9C3722"),
        "desc": (
            "Safety, or skipping it costs you thousands. If you do nothing "
            "else, do these twelve things. " + DISCLAIMER
        ),
    },
    "should": {
        "file": "gulf-coast-should-do.ics",
        "name": "Should Do — Gulf Coast Home Maintenance",
        "color": ("teal", "#1F5F6B"),
        "desc": (
            "Protects your home's value and makes what you own last longer. "
            + DISCLAIMER
        ),
    },
    "above": {
        "file": "gulf-coast-going-above.ics",
        "name": "Going Above — Gulf Coast Home Maintenance",
        "color": ("olivedrab", "#5D6B3A"),
        "desc": (
            "For the homeowner who wants to stay ahead of everything. "
            + DISCLAIMER
        ),
    },
}

# --- Content ---------------------------------------------------------------
# (month, day, tier, uid slug, title, body)
# Day is 1 unless the date is deliberate: May 1 gives the 30-day flood
# insurance window room before June 1, and November 30 is the season close.

TASKS = [
    # JANUARY
    (1, 1, "must", "jan-detectors",
     "Test smoke and CO detectors",
     "Test every smoke and carbon monoxide detector. Replace the batteries. "
     "Replace any detector over 10 years old.\n\n"
     "Why: sensors degrade with age whether or not the unit still chirps, and "
     "a detector past its rated life can pass a button test and still fail in "
     "a real fire."),
    (1, 1, "should", "jan-freeze-prep",
     "Freeze prep — find your water shutoff",
     "Locate your main water shutoff and make sure you can actually turn it. "
     "Cover outdoor spigots.\n\n"
     "Why: coastal plumbing is often run through uninsulated exterior walls "
     "because it rarely needs to survive a freeze. When one comes, knowing "
     "where the shutoff is turns a flooded house into a wet floor."),
    (1, 1, "above", "jan-attic-check",
     "Check the attic after winter rain",
     "Look for daylight through the roof deck, damp or matted insulation, and "
     "water stains on the framing.\n\n"
     "Why: a small roof leak shows up in the attic long before it shows up on "
     "your ceiling. Winter rain is the easiest time to catch one."),

    # FEBRUARY
    (2, 1, "must", "feb-termite-inspection",
     "Schedule the annual termite inspection",
     "Book it now, before spring swarm season fills the schedule.\n\n"
     "Why: Formosan and native subterranean termites are endemic across the "
     "Gulf Coast, and damage is almost never covered by homeowners insurance. "
     "An annual inspection is the cheapest insurance you can buy."),
    (2, 1, "should", "feb-hvac-filter",
     "Replace the HVAC filter, test the A/C",
     "Swap the filter and run the air conditioning briefly.\n\n"
     "Why: finding a cooling problem in February means an appointment. Finding "
     "it in July means a wait list, a premium, and a hot house."),
    (2, 1, "above", "feb-caulk",
     "Walk the exterior and re-caulk",
     "Re-caulk gaps around windows, doors, and any penetration through the "
     "wall.\n\n"
     "Why: caulk is the cheapest material on the house and the first line "
     "against wind-driven rain. On the coast it fails in 2–4 years."),

    # MARCH
    (3, 1, "must", "mar-hvac-service",
     "Service the HVAC before cooling season",
     "Get a professional service call before the cooling season starts.\n\n"
     "Why: down here the system runs eight or nine months a year, roughly "
     "double the load it was rated against. Service is what buys back the "
     "years that heat takes off."),
    (3, 1, "should", "mar-gutters",
     "Clear the gutters, check the downspouts",
     "Clear the gutters and confirm every downspout discharges away from the "
     "foundation, not against it.\n\n"
     "Why: water dumped at the foundation is the start of settling, slab "
     "cracks, and a wet crawlspace — all of them expensive, all of them "
     "avoidable with a splash block."),
    (3, 1, "above", "mar-grading",
     "Check the grading around the house",
     "Walk the perimeter after a hard rain. Look for settling, cracks, and "
     "standing water.\n\n"
     "Why: the ground should fall away from the house. Gulf Coast soils shift, "
     "and grading that worked at closing may not work three years later."),

    # APRIL
    (4, 1, "must", "apr-swarm-season",
     "Swarm season — watch for termites",
     "Watch for winged termites indoors and around lights. Check for mud tubes "
     "along the slab, piers, and foundation walls.\n\n"
     "Why: a swarm is the one time termites are visible to you. Mud tubes mean "
     "an active colony is already feeding on the house."),
    (4, 1, "should", "apr-wash-exterior",
     "Wash the exterior, inspect the siding",
     "Wash the house down and inspect siding, brick, and soffits for damage or "
     "gaps.\n\n"
     "Why: salt air and humidity feed mildew and rot, and washing is how you "
     "find the soft spot behind it. Open soffits are also how squirrels and "
     "wasps get into the attic."),
    (4, 1, "above", "apr-spigots-irrigation",
     "Check spigots and service irrigation",
     "Check hose bibs and outdoor spigots for leaks. Service the irrigation "
     "system if you have one.\n\n"
     "Why: a spigot that weeps against the foundation all summer does quiet, "
     "steady damage — and shows up on the water bill."),

    # MAY
    (5, 1, "must", "may-insurance-hurricane-prep",
     "Verify insurance — season opens June 1",
     "Verify your coverage BEFORE the season starts: wind, and flood if you "
     "carry it. Photograph every room and the full exterior for your claim "
     "file. Trim limbs back from the roof.\n\n"
     "Why: flood policies generally take 30 days to take effect, so June 1 is "
     "already too late to start. Photos taken before a storm are what get a "
     "claim paid after one."),
    (5, 1, "should", "may-generator-supplies",
     "Test the generator, restock supplies",
     "Start and load-test the generator. Restock water, batteries, and fuel. "
     "Confirm shutters or plywood are on hand and actually fit your "
     "openings.\n\n"
     "Why: a generator that has sat with old fuel since last season will not "
     "start when you need it, and plywood cut to the wrong window is plywood "
     "you cannot use."),
    (5, 1, "above", "may-secure-exterior",
     "Inspect roof edges, secure loose items",
     "Inspect soffit vents and roof edges. Secure sheds, fencing, and anything "
     "that becomes a projectile.\n\n"
     "Why: most wind damage starts at an edge. Once wind gets under the roof "
     "edge or through an open soffit, it works on the whole roof."),

    # JUNE
    (6, 1, "must", "jun-condensate-line",
     "Clear the A/C condensate drain line",
     "Flush the condensate drain line and check the overflow pan and float "
     "switch.\n\n"
     "Why: a clogged condensate line is one of the most common causes of "
     "ceiling damage on the coast. The unit keeps running and quietly drains "
     "into your drywall."),
    (6, 1, "should", "jun-condenser-coils",
     "Clean the condenser, clear vegetation",
     "Clean the outdoor condenser coils and cut vegetation back two feet on "
     "all sides of the unit.\n\n"
     "Why: a coil that cannot breathe makes the compressor work harder in the "
     "hottest months, which is exactly how a 12-year unit becomes an 8-year "
     "unit."),
    (6, 1, "above", "jun-attic-ventilation",
     "Check attic ventilation and insulation",
     "Check that soffit and ridge vents are clear, and measure insulation "
     "depth.\n\n"
     "Why: a poorly vented attic bakes the roof deck from underneath and "
     "shortens shingle life, on top of what it costs you in cooling."),

    # JULY
    (7, 1, "must", "jul-leak-hunt",
     "Hunt for leaks",
     "Check under every sink, behind every toilet, and around the base of the "
     "water heater.\n\n"
     "Why: slow leaks are found by looking, not by waiting. In this humidity a "
     "cabinet leak becomes mold long before it becomes a stain you notice."),
    (7, 1, "should", "jul-crawlspace",
     "Inspect the crawlspace",
     "Inspect the crawlspace or under-house area for moisture, pests, and "
     "vapor barrier damage.\n\n"
     "Why: it is the part of the house nobody looks at and the part humidity "
     "attacks hardest. Rot and pests both start down there."),
    (7, 1, "above", "jul-humidity",
     "Check indoor humidity",
     "Measure indoor relative humidity. Aim for 45–55%. Run a "
     "dehumidifier if you are above that.\n\n"
     "Why: above 60% indoors you are growing mold and inviting dust mites, "
     "whatever the thermostat says."),

    # AUGUST
    (8, 1, "must", "aug-peak-season-check",
     "Peak season — re-check kit and plan",
     "Re-check your supply kit, your documents, and your evacuation plan. "
     "Confirm your insurance is still active and paid.\n\n"
     "Why: this is the peak of the season. A lapsed policy or an expired "
     "document is something you want to find now, not while you are "
     "packing."),
    (8, 1, "should", "aug-gutters-again",
     "Clear the gutters again",
     "Clear the gutters a second time.\n\n"
     "Why: summer storms fill them fast, and a full gutter in a tropical "
     "downpour sends the whole roof's water straight down your wall."),
    (8, 1, "above", "aug-photograph-valuables",
     "Photograph big-ticket items",
     "Photograph big-ticket items and store the photos somewhere off-site or "
     "in the cloud.\n\n"
     "Why: proof of ownership is what turns a claim into a payment, and it is "
     "worthless if it only exists on a phone that went with the house."),

    # SEPTEMBER
    (9, 1, "must", "sep-dryer-vent",
     "Clean the dryer vent",
     "Clean the full dryer vent run, not just the lint trap.\n\n"
     "Why: dryer lint is a leading cause of house fires, and coastal humidity "
     "makes it pack into the duct harder and faster."),
    (9, 1, "should", "sep-roof-inspection",
     "Inspect the roof from the ground",
     "Inspect the roof from the ground with binoculars after the summer storm "
     "run. Look for lifted, curled, or missing shingles.\n\n"
     "Why: you can see almost everything that matters from the driveway, and "
     "nobody has ever fallen off a driveway."),
    (9, 1, "above", "sep-sump-drainage",
     "Test the sump pump, clear drainage",
     "Test the sump pump if you have one. Clear drainage swales and "
     "ditches.\n\n"
     "Why: a sump pump that has not run in months is a sump pump you should "
     "not assume works. Blocked ditches move the water to your yard."),

    # OCTOBER
    (10, 1, "must", "oct-flush-water-heater",
     "Flush the water heater",
     "Drain and flush the tank to clear sediment.\n\n"
     "Why: sediment insulates the burner from the water and cooks the tank "
     "from the inside. Gulf Coast water heaters are already short-lived; this "
     "is most of the difference between 8 years and 12."),
    (10, 1, "should", "oct-weatherstripping",
     "Check weatherstripping and seals",
     "Check weatherstripping, door sweeps, and the attic hatch seal.\n\n"
     "Why: those gaps are your largest uncontrolled air exchange, which on the "
     "coast means you are paying to dehumidify the outdoors."),
    (10, 1, "above", "oct-chimney",
     "Service the fireplace or chimney",
     "Service the fireplace or chimney before first use.\n\n"
     "Why: an unused flue collects nests, debris, and moisture damage over a "
     "long warm season."),

    # NOVEMBER
    (11, 30, "must", "nov-post-season-inspection",
     "Post-season inspection — season closed",
     "Walk the roof line and the whole property for storm damage. File any "
     "claims now, not in spring.\n\n"
     "Why: hurricane season closes November 30. Insurers get much harder to "
     "convince about damage the longer you wait, and most policies require "
     "prompt notice."),
    (11, 1, "should", "nov-filter-heat-test",
     "Replace the filter, test the heat",
     "Replace the HVAC filter and run the heat once.\n\n"
     "Why: the burner or heat strips have sat unused since spring. Better to "
     "smell the dust burn off in November than to find a dead system during a "
     "cold snap."),
    (11, 1, "above", "nov-gutters-fascia",
     "Clear gutters, check fascia and trim",
     "Clear the gutters after leaf drop. Check the fascia and trim for "
     "rot.\n\n"
     "Why: fascia is where a gutter that overflowed all year finally shows the "
     "damage, and rotten fascia is how the gutter comes off in the next "
     "storm."),

    # DECEMBER
    (12, 1, "must", "dec-freeze-prep",
     "Freeze prep — protect the pipes",
     "Insulate exposed pipes, cover spigots, and confirm you know where the "
     "main shutoff is.\n\n"
     "Why: coastal homes are built for heat, not cold. A hard freeze here "
     "bursts pipes that would be fine anywhere north of us."),
    (12, 1, "should", "dec-gfci-breakers",
     "Test GFCI outlets, label the panel",
     "Press test and reset on every GFCI outlet. Label the breaker panel if it "
     "is not already labeled.\n\n"
     "Why: a GFCI that will not trip is not protecting anyone, and a labeled "
     "panel is what lets you kill the right circuit in a hurry."),
    (12, 1, "above", "dec-watch-list",
     "Update the Big Ticket Watch List",
     "Update your Big Ticket Watch List with anything you replaced or "
     "serviced this year.\n\n"
     "Why: the list is what turns a surprise roof into a planned roof. One "
     "update a year keeps it honest."),
]

# --- ICS generation --------------------------------------------------------

def escape(text):
    """Escape a value per RFC 5545 section 3.3.11."""
    out = text.replace("\\", "\\\\")
    out = out.replace(";", "\\;").replace(",", "\\,")
    out = out.replace("\r\n", "\n").replace("\n", "\\n")
    return out


def fold(line):
    """Fold a content line to 75 octets, continuing with a leading space."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    pieces = []
    start = 0
    limit = 75
    while start < len(raw):
        end = min(start + limit, len(raw))
        # Do not split a multi-byte UTF-8 character.
        while end > start and end < len(raw) and (raw[end] & 0xC0) == 0x80:
            end -= 1
        pieces.append(raw[start:end].decode("utf-8"))
        start = end
        limit = 74  # continuation lines carry a leading space
    return "\r\n ".join(pieces)


def stamp(day):
    """Format a date as an RFC 5545 DATE value."""
    return "{0}{1:02d}{2:02d}".format(day.year, day.month, day.day)


def build_event(month, day, slug, title, body):
    # An all-day event's DTEND is exclusive, so it is the following day. Letting
    # the date module carry the month and year rollovers keeps leap years right
    # without a table of month lengths to maintain.
    start = date(ANCHOR_YEAR, month, day)
    return [
        "BEGIN:VEVENT",
        "UID:{0}-{1}@{2}".format(ANCHOR_YEAR, slug, UID_DOMAIN),
        "DTSTAMP:" + DTSTAMP,
        "DTSTART;VALUE=DATE:" + stamp(start),
        "DTEND;VALUE=DATE:" + stamp(start + timedelta(days=1)),
        "RRULE:FREQ=YEARLY",
        "SEQUENCE:{0}".format(SEQUENCE),
        "SUMMARY:" + escape(title),
        "DESCRIPTION:" + escape(body + "\n\n" + DISCLAIMER),
        "TRANSP:TRANSPARENT",
        "CATEGORIES:Home Maintenance",
        "END:VEVENT",
    ]


def build_calendar(tier_key):
    """Return the .ics text for one tier, and how many events it holds."""
    tier = TIERS[tier_key]
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Gulf Coast Home Maintenance//Perpetual Edition//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:" + escape(tier["name"]),
        "X-WR-CALDESC:" + escape(tier["desc"]),
        "X-WR-TIMEZONE:America/Chicago",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
        "COLOR:" + tier["color"][0],
        "X-APPLE-CALENDAR-COLOR:" + tier["color"][1],
    ]
    events = [t for t in TASKS if t[2] == tier_key]
    for month, day, _, slug, title, body in events:
        lines.extend(build_event(month, day, slug, title, body))
    lines.append("END:VCALENDAR")

    # Fold once, here, rather than at each place a line is built — every line in
    # the file has to obey the 75-octet limit, so nowhere else has to remember.
    return "\r\n".join(fold(line) for line in lines) + "\r\n", len(events)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for tier_key in ("must", "should", "above"):
        text, count = build_calendar(tier_key)
        path = os.path.join(OUT_DIR, TIERS[tier_key]["file"])
        with open(path, "wb") as handle:
            handle.write(text.encode("utf-8"))
        print("{0}  {1} events".format(path, count))


if __name__ == "__main__":
    main()
