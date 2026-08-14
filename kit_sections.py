#!/usr/bin/env python3
"""
The "if you have one" pages. Kit only.

Not every Gulf Coast house has a septic tank, a pool, a generator, or a dock,
so none of this belongs in the twelve months. Put it on its own pages and a
buyer who has the thing gets a section nobody else needed, which reads as
thorough rather than as padding.

Each section carries:
    lead    one line saying who this page is for
    when    timed jobs, keyed to a month or a season
    always  things that are true year round
    watch   the mistake that costs real money, or hurts someone

The Gulf Coast angle is the point. Generic advice about septic tanks ignores a
high water table; generic pool advice ignores storm surge; generic generator
advice ignores that most carbon monoxide deaths happen in the week after a
hurricane, not during it.
"""

SECTIONS = [
    {
        "title": "If you have a septic system",
        "lead": "Common once you are outside city limits, and unforgiving of "
                "neglect. A drain field is far more expensive than a pump-out.",
        "when": [
            ("Every 3 to 5 years",
             "Have the tank pumped. More often with a garbage disposal or a "
             "full house."),
            ("Before hurricane season",
             "Know where the lid and the cleanout are, and photograph the "
             "location. Finding them under a foot of storm debris is worse."),
            ("After any flooding",
             "Use as little water as possible until the ground drains. A "
             "saturated drain field cannot accept anything, and forcing it "
             "backs sewage into the house."),
        ],
        "always": [
            "Nothing down the toilet but waste and paper. Not wipes, however "
            "the packet is labeled, and not grease.",
            "Keep vehicles and heavy equipment off the drain field. Compacted "
            "soil stops it draining.",
            "Keep roof runoff and downspouts away from the field.",
            "Do not plant trees near the lines. Roots find them.",
        ],
        "watch": "Slow drains everywhere at once, a patch of grass greener and "
                 "lusher than the rest of the yard, or a sewage smell outside. "
                 "Any of those means call someone this week, not next month. "
                 "The high water table down here means a failing field shows up "
                 "faster and floods more completely than it would inland.",
    },
    {
        "title": "If you are on a well",
        "lead": "Nobody tests your water but you. There is no utility sending "
                "an annual report.",
        "when": [
            ("Once a year",
             "Test for bacteria and nitrates. County extension offices often "
             "do this cheaply."),
            ("After any flood",
             "Assume the well is contaminated. Test before drinking, and "
             "disinfect if the water reached the wellhead."),
            ("Spring",
             "Check the pressure tank and listen to how often the pump cycles. "
             "Rapid cycling wears the pump out fast."),
        ],
        "always": [
            "Keep the wellhead above grade and capped, so surface water cannot "
            "run in.",
            "Keep chemicals, fuel and fertilizer well away from it.",
            "Know where your pressure switch and breaker are.",
        ],
        "watch": "Close to the shore, over-pumping can pull salt water into the "
                 "aquifer. A gradual change in taste is worth testing for rather "
                 "than getting used to.",
    },
    {
        "title": "If you have a pool",
        "lead": "Most of the year it is routine. The exception is the week a "
                "storm is coming, when the usual instinct is the wrong one.",
        "when": [
            ("Before a named storm",
             "Do NOT drain it. Add extra chlorine, drop the level by a foot or "
             "two at most, cut power to the pump and heater at the breaker, and "
             "bring loose furniture indoors."),
            ("After the storm",
             "Skim the debris out before it sinks and stains. Do not run the "
             "equipment until you are sure it did not go under water."),
            ("Annually",
             "Have the bonding and the GFCI protection checked by an "
             "electrician."),
        ],
        "always": [
            "Keep the water balanced. Chemistry is cheaper than resurfacing.",
            "Check the barrier, gate and latch actually work.",
        ],
        "watch": "An empty pool can float out of the ground. Ground water "
                 "pressure is what holds it down, and after days of rain that "
                 "pressure is at its highest. Draining a pool ahead of a storm "
                 "is how people turn a cleanup into a replacement.",
    },
    {
        "title": "If you have a generator",
        "lead": "The thing that makes the week after a storm bearable, and the "
                "thing that kills people in it.",
        "when": [
            ("May",
             "Start it and run it under load for half an hour. Fresh fuel, or "
             "stabilizer in what is there."),
            ("Monthly, standby units",
             "Let it run its self-test and watch it. Check the oil."),
            ("Annually, standby units",
             "Service it the way you would service a small engine, or have the "
             "installer do it."),
        ],
        "always": [
            "Store fuel safely and rotate it. Ethanol fuel goes bad within "
            "months and is the usual reason a generator will not start.",
            "Know which circuits you actually need. Most people need the "
            "fridge, a few lights, and a way to charge phones.",
            "Keep a working carbon monoxide alarm indoors regardless.",
        ],
        "watch": "Never run a portable generator indoors, in a garage, or under "
                 "a carport, and keep it at least twenty feet from any window or "
                 "door. Carbon monoxide has no smell and kills more people in "
                 "the days after a hurricane than the storm itself does. Never "
                 "plug a generator into a wall socket to feed the house: it "
                 "sends power back down the line and can kill the crew working "
                 "to restore it.",
    },
    {
        "title": "If your house is raised or on piers",
        "lead": "Common on this coast, and it puts a whole floor of your house "
                "in the weather that nobody inspects.",
        "when": [
            ("July",
             "Go under with a flashlight. Standing water, damp soil, sagging "
             "insulation, rusted duct straps."),
            ("Spring and fall",
             "Check piers and posts for settling, cracking, or shims that have "
             "worked loose."),
            ("Before hurricane season",
             "Check the skirting and any flood vents are intact and clear."),
        ],
        "always": [
            "Keep the vapor barrier intact and overlapped across the ground.",
            "Keep vents clear if the space is vented, or the dehumidifier "
            "running if it is encapsulated. Pick one approach and commit.",
            "Watch the piers for mud tubes. A raised house gives termites more "
            "routes up, not fewer.",
        ],
        "watch": "Flood vents are structural, not decorative. Blocking them so "
                 "the crawlspace looks tidier can invalidate a flood claim and, "
                 "worse, lets water push against the walls instead of through.",
    },
    {
        "title": "If you have shutters or impact protection",
        "lead": "Protection you have not tested is protection you do not have.",
        "when": [
            ("May",
             "Test fit every panel on the opening it belongs to, and label each "
             "one to its window. Do it once and never do it in the dark again."),
            ("May",
             "Work the tracks on accordion and roll-down shutters, and "
             "lubricate them."),
            ("After any storm",
             "Rinse the salt off everything and check the anchors."),
        ],
        "always": [
            "Keep the wing nuts, bolts and tools in one labeled box with the "
            "panels, not scattered in the garage.",
            "Check anchors and fasteners for corrosion. Salt air eats them "
            "faster than the panels.",
            "On impact windows, check the seals and the frames rather than "
            "assuming the glass is the whole system.",
        ],
        "watch": "Plywood cut to the wrong window is plywood you cannot use. If "
                 "you are cutting panels, cut them before the season and write "
                 "the room on each one in permanent marker.",
    },
    {
        "title": "If you are on the water",
        "lead": "A dock, a lift, or a bulkhead is a structure in salt water that "
                "no home inspector looked at.",
        "when": [
            ("Spring",
             "Walk the dock and sound the boards. Check pilings at the "
             "waterline, which is where they go first."),
            ("Before hurricane season",
             "Service the lift, check cables for broken strands, and know how "
             "you will secure or remove the boat."),
            ("After any storm",
             "Inspect before using. A lift with a damaged cable fails with a "
             "boat on it."),
        ],
        "always": [
            "Check bulkhead tiebacks and weep holes. A bulkhead fails from "
            "behind, through soil washing out, not from the face.",
            "Replace corroded hardware with hot-dip galvanised or stainless.",
            "Rinse lift motors and cables with fresh water.",
        ],
        "watch": "Look for soil settling or sinkholes on the land side of a "
                 "bulkhead. That is the fill washing out through a failure you "
                 "cannot see yet, and it is far cheaper to fix at that stage "
                 "than after the wall leans.",
    },
]
