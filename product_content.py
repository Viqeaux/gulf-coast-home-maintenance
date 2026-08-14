#!/usr/bin/env python3
"""
The pages of the printable edition that are not in the calendar feeds.

The twelve months live in build_calendars.py, shared with the .ics files. What
is here is what the printable adds on top: the Big Ticket Watch List lifespans,
the page on how to date what you own, the first-month checklist, and the licence.

This file is committed, unlike gulf-coast-maintenance-calendar-content.md. That
draft is kept out of a repo that has to be public because it holds the design
and pricing thinking for the paid kit. These pages are not secret — they ship
inside a free download, so anyone who wants them already has them, and keeping
the source out of the repo would only mean a clone could not rebuild the file.

build_pdf.py imports this.
"""

# --- Inside front cover ----------------------------------------------------
# One-time jobs. They never repeat, so they do not belong on a month page.

FIRST_MONTH = [
    "Find and tag the main water shutoff",
    "Find and tag the gas shutoff",
    "Label every breaker in the panel",
    "Locate the septic tank lid or the sewer cleanout",
    "Find the A/C condensate drain line and its cleanout",
    "Write down every air filter size and tape the list inside the closet door",
    "Photograph every room and the full exterior — before anything happens",
    "Register warranties on anything new",
    "Collect appliance manuals in one folder",
    "Open a maintenance fund and start setting money aside monthly",
]

FIRST_MONTH_NOTE = (
    "Ten jobs you do once. Every one of them is something you will want at a "
    "bad moment — a burst pipe at midnight, a claim adjuster asking what "
    "the house looked like before. An afternoon now buys all of it."
)

# --- Back page: the Big Ticket Watch List ----------------------------------
# (item, typical Gulf Coast life). The middle column is pre-printed; the buyer
# fills in the year installed and works out when to start watching.

WATCH_LIST = [
    ("Roof — asphalt shingle", "12–15 years"),
    ("Roof — metal", "30–40 years"),
    ("Water heater — tank", "8–10 years"),
    ("A/C condenser (outdoor)", "10–12 years"),
    ("Furnace / air handler", "15–18 years"),
    ("Ductwork", "15–20 years"),
    ("Exterior paint", "5–7 years"),
    ("Exterior caulk & sealants", "2–4 years"),
    ("Windows", "15–25 years"),
    ("Garage door opener", "10–12 years"),
    ("Dishwasher", "9 years"),
    ("Refrigerator", "10–13 years"),
    ("Washer / dryer", "10–13 years"),
    ("Water heater anode rod", "4–5 years"),
    ("Septic tank — pump out", "every 3–5 years"),
    ("Fence — wood", "10–15 years"),
    ("Deck — wood", "10–20 years"),
]

WATCH_LIST_NOTE_TITLE = "Why these numbers are shorter than what you find online"

WATCH_LIST_NOTE = (
    "Salt air, high humidity, and intense UV wear coastal homes faster than "
    "the national averages assume. These are adjusted for the Gulf Coast. "
    "They are guidelines, not guarantees — a well-maintained roof outlives "
    "a neglected one."
)

# --- Facing page: how to date what you own ---------------------------------
# (subject, how to find it out)

FIND_OUT_INTRO = (
    "Don’t know when something was installed? Most of these take five "
    "minutes to find."
)

FIND_OUT = [
    ("Water heater",
     "The manufacture date is encoded in the serial number on the label. "
     "Search the brand name plus “serial number date” and you will "
     "find the decoder."),
    ("A/C and furnace",
     "Check the data plate on the outdoor unit and inside the air handler "
     "closet. Most list the manufacture date outright."),
    ("Roof",
     "Try the old real estate listing photos, the seller’s disclosure "
     "statement, or your county permit records. A re-roof usually pulls a "
     "permit."),
    ("Appliances",
     "Model and serial are on a sticker inside the door, on the back, or "
     "under the lid."),
    ("Anything original to the house",
     "Use the year the house was built. It is rarely wrong."),
]

FIND_OUT_CLOSE_TITLE = "Still don’t know?"

FIND_OUT_CLOSE = (
    "Write “unknown” and put this year in the last column. Get it "
    "inspected once, note the condition, and you have a baseline going "
    "forward. Unknown is a starting point, not a dead end."
)

# --- Month pages -----------------------------------------------------------
# The three months where the season itself is the headline.

MONTH_NOTES = {
    5: "Hurricane prep month · season opens June 1",
    8: "Peak hurricane season",
    11: "Season closes November 30",
}

# --- Licence ---------------------------------------------------------------
# What someone may do with a free download, in the plainest words that still
# mean something. A free file wants to travel, so the only real ask is that it
# travels as a link rather than as a copy that can go stale.

LICENCE_TITLE = "What you may do with this"

LICENCE = [
    ("Yours to keep and print",
     "Print it as many times as you like, for your own home and for any home "
     "you own. Print a fresh copy every year — it is undated on purpose, "
     "so it never expires."),
    ("Free to pass on",
     "Put it on the fridge, hand it to whoever does the work, give it to a "
     "neighbour or to a buyer at closing. Send them the link rather than the "
     "file, so they get the current version and whatever has been fixed "
     "since."),
    ("Please don’t sell it",
     "It is free everywhere it is meant to be. Reselling it, or listing it "
     "as your own, is the one thing that would make it worth taking down."),
]
