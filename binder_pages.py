#!/usr/bin/env python3
"""
Content for the Storm Season Binder. Paid product, kit-only rules apply.

Kept apart from build_storm_binder.py for the same reason task_steps.py is kept
apart from build_calendars.py: this is the bulk of the writing and it changes
for different reasons than the layout does.

The binder is not the kit. The kit is bought in January by somebody being
responsible. This is bought in August with a cone on the television, and every
page has to survive being read by someone who is frightened and in a hurry.
That sets the voice: short lines, the order things actually happen in, and the
reason attached to the instruction so it is obeyed rather than skimmed.

Three things separate this from the free advice already on the internet:

1. It is Gulf specific. Wind deductibles as a percentage, flood as a separate
   policy, two weeks without power rather than three days, mold in 24 hours,
   fire ants rafting in flood water.
2. It is a record, not a leaflet. Most of these pages are blanks the buyer
   fills in while it is calm, which is the only time they can be filled in.
3. It carries the claim. The money in a hurricane is lost after the storm, in
   the documentation, not during it.

Plain text only in this file. The renderer escapes everything here, so an HTML
entity written into a string would print as its own source code.
"""

# --- policy and account numbers --------------------------------------------

# Grouped the way you reach for them: the wind and flood policies first,
# because those are the two calls made on day one and they are almost never the
# same company.
POLICY_BLOCKS = [
    ("Homeowners and wind", [
        "Insurance company",
        "Policy number",
        "Agent name",
        "Agent phone",
        "24 hour claims line",
        "Standard deductible, in dollars",
        "Hurricane or wind deductible, in dollars",
        "Dwelling coverage limit",
        "Contents coverage limit",
        "Loss of use coverage limit",
    ]),
    ("Flood, which is a separate policy", [
        "Insurance company or NFIP",
        "Policy number",
        "Agent phone",
        "Claims line",
        "Building coverage limit",
        "Contents coverage limit",
        "Deductible, in dollars",
        "Policy renewal date",
    ]),
    ("Vehicles", [
        "Auto insurance company",
        "Policy number",
        "Claims line",
        "Comprehensive coverage, yes or no",
    ]),
]

# The second column. Shorter fields, and the ones you need in the first hour
# rather than the first week.
UTILITY_BLOCKS = [
    ("Utilities", [
        "Electric provider",
        "Outage reporting number",
        "Account number",
        "Water provider and number",
        "Gas or propane supplier",
        "Propane tank number",
    ]),
    ("The house", [
        "Alarm company and passcode",
        "Pest or termite bond company",
        "Home warranty company",
        "Roofer or contractor you trust",
        "Plumber",
        "Electrician",
    ]),
    ("People", [
        "Out of state contact name",
        "Out of state contact phone",
        "Neighbor with a key",
        "Employer storm line",
        "Doctor and pharmacy",
        "Vet and pet microchip numbers",
    ]),
    # Sits here rather than with the policies because the lender is somebody you
    # call, and because the policies page measured over the sheet with it on.
    ("Mortgage and escrow", [
        "Lender",
        "Loan number",
        "Phone",
        "Is insurance paid from escrow",
    ]),
]

POLICY_WATCH = (
    "Your hurricane deductible is almost never a flat dollar amount. It is a "
    "percentage of your dwelling coverage, and on a house insured for $400,000 "
    "a 2 percent wind deductible is $8,000 out of your pocket before the policy "
    "pays anything at all. Look it up and write the dollar figure in that box, "
    "not the percentage. People find this out for the first time while an "
    "adjuster is explaining it to them, and it is the single most common "
    "unpleasant surprise of a Gulf Coast claim."
)

POLICY_NOTE = (
    "Wind and flood are different policies, usually from different companies, "
    "and they argue with each other about which one caused the damage. That "
    "argument is the reason the damage log later in this binder asks you to "
    "name a cause for every line. Water that blew in through a broken window is "
    "wind. The same water arriving across the yard is flood."
)

SECURITY_NOTE = (
    "This page is worth stealing. Last four digits are enough to start almost "
    "any call, so consider writing only those for account numbers, and keep the "
    "filled binder somewhere you would keep a passport rather than on the "
    "kitchen counter."
)

# --- what to photograph -----------------------------------------------------

PHOTO_SETS = [
    ("Every room, the same way each time", [
        "Stand in the doorway and take one photo of each of the four walls.",
        "Then the ceiling and the floor. Water damage is argued about at both.",
        "Open every closet, cabinet and drawer and photograph what is inside.",
        "Pull out anything expensive and photograph it on its own.",
    ]),
    ("The plates and the numbers", [
        "The data plate on the outdoor A/C unit and on the indoor air handler.",
        "The label on the water heater.",
        "Model and serial stickers inside the door of every appliance.",
        "The electrical panel with the door open and the labels readable.",
        "The roof from the ground, all four elevations, plus any flashing you can see.",
    ]),
    ("Outside and underneath", [
        "All four sides of the house from far enough back to see the whole wall.",
        "The fence, the shed, the driveway, the trees near the roof.",
        "Under the house if it is raised, with a flashlight.",
        "The attic, including the underside of the roof deck.",
        "The dock, the lift and the bulkhead if you have them.",
    ]),
]

PHOTO_METHOD = (
    "Walk the house once with the phone on video and narrate as you go, naming "
    "rooms and items out loud. Ten minutes of video is easier to make than four "
    "hundred photographs and your own voice describing a thing is worth more in "
    "a claim than a silent picture of it. Then go back and take stills of "
    "anything expensive."
)

PHOTO_WATCH = (
    "Photographs taken after a storm prove that damage exists. Photographs "
    "taken before it prove the house was not already like that, which is the "
    "thing actually in dispute. Pre existing damage is the most common reason a "
    "wind claim is reduced, and the only defense is a dated picture from before."
)

PHOTO_STORAGE = [
    "Get them off the phone. A phone is a thing you can drop in flood water.",
    "Upload to cloud storage and check that the upload actually finished.",
    "Email the important ones to yourself as well, on a different account.",
    "Keep the originals rather than anything a messaging app has compressed. "
    "The date and location are written inside the original file.",
    "Photograph these filled binder pages too, and put them in the same place.",
]

# Half of what an adjuster, a lender or a contractor asks for in the first week
# is a document somebody has to go and find. This is the page that says where.
DOCUMENT_LOCATIONS = [
    "Deed or lease",
    "Vehicle titles",
    "Policy declarations pages",
    "Birth certificates and passports",
    "Wills and powers of attorney",
    "Safe location and who knows the combination",
    "Safe deposit box, bank and number",
    "Spare house and vehicle keys",
]

# A worked line, so nobody has to guess how much detail is enough. Detail is
# what an adjuster pays on, and this is roughly the floor.
INVENTORY_EXAMPLE = [
    ("Item", "Refrigerator, french door"),
    ("Make and model", "Whirlpool WRF555SDFZ"),
    ("Serial or ID", "HRB1234567"),
    ("Year", "2021"),
    ("What it would cost today", "$2,100"),
]

INVENTORY_EXAMPLE_NOTE = (
    "That is the standard. A line reading “fridge, about $2,000” gets paid too, "
    "but it gets paid slowly and it gets argued about. A make, a model and a "
    "serial number turn a conversation into a calculation, and the photographs "
    "you took of the plates are where all three of them come from."
)

# --- the inventory ----------------------------------------------------------

INVENTORY_INTRO = (
    "Contents coverage is usually 50 to 70 percent of what the house itself is "
    "insured for, which on most policies is a six figure number. To collect it "
    "you have to say what you owned, and the adjuster is not going to help you "
    "remember. People routinely settle for a fraction of their contents limit "
    "because listing four hundred items from memory, in a rental, three weeks "
    "after losing them, is impossible."
)

INVENTORY_METHOD = [
    "Do one room at a time and do not try to finish the house in one sitting.",
    "Start with the expensive things. Twenty items at $500 and up matter more "
    "than two hundred at $20.",
    "Where you cannot remember the price, write what it would cost to buy the "
    "same thing today. That is what replacement cost coverage pays.",
    "A rough list beats no list. An adjuster can work with approximate.",
    "Anything over about $2,000, check whether your policy has a sub limit. "
    "Jewelry, firearms, cameras, tools and collectibles usually do, and the "
    "limit is often far lower than people expect.",
]

INVENTORY_WATCH = (
    "Jewelry, cash, firearms and art are commonly capped at $1,000 to $2,500 "
    "total, whatever your contents limit says. If you own more than that, the "
    "fix is a scheduled endorsement bought before the season, and it costs very "
    "little. Finding out afterward is finding out too late."
)

# name, the prompt under it, how many ruled rows the sheet gets
INVENTORY_ROOMS = [
    ("Kitchen",
     "Refrigerator, range, dishwasher, microwave, small appliances, cookware, "
     "china, the contents of the pantry.", 24),
    ("Living and family room",
     "Televisions and mounts, sound equipment, gaming consoles, furniture, "
     "rugs, lamps, art, curtains and blinds.", 24),
    ("Primary bedroom",
     "Bed and mattress, dressers, jewelry, watches, clothing by category rather "
     "than by garment, anything in the closet safe.", 24),
    ("Bedrooms",
     "One line per child or per room. Beds, desks, instruments, sports "
     "equipment, computers, the expensive toys.", 24),
    ("Bathrooms and linen",
     "Linens, towels, medical equipment, anything stored in the hall closet.", 24),
    ("Office, electronics and hobbies",
     "Computers, monitors, printers, cameras and lenses, drones, instruments, "
     "sewing and craft equipment, books.", 24),
    ("Garage, shed and tools",
     "Power tools, hand tools, lawn equipment, generator, pressure washer, "
     "ladders, bicycles, the second refrigerator.", 24),
    ("Outdoor, yard and water",
     "Patio furniture, grill, outdoor kitchen, pool equipment, boat and "
     "trailer, dock hardware, lift motor.", 24),
    ("Attic, storage and everything else",
     "Holiday decorations, stored furniture, luggage, files, anything in a "
     "storage unit under this address.", 24),
]

INVENTORY_COLUMNS = ["Item", "Make and model", "Serial or ID", "Year",
                     "What it would cost today"]

# --- water and supplies -----------------------------------------------------

SUPPLY_INTRO = (
    "The federal advice is three days. Three days is for a house that is merely "
    "inconvenienced. After a Gulf hurricane that made landfall near you, the "
    "realistic number is seven days, and fourteen if you are rural, on a well, "
    "or at the end of a long feeder line. Power restoration in the last several "
    "major storms on this coast ran one to three weeks for the outer streets."
)

# label, the rule in words, and the arithmetic spelled out so nobody has to
# work it out with a cone on the television
SUPPLY_ROWS = [
    ("Drinking water",
     "1 gallon per person per day",
     "people x days"),
    ("Water for cooking and washing",
     "Another half gallon per person per day",
     "people x days x 0.5"),
    ("Pet water",
     "1 gallon per day for a large dog, less for anything smaller",
     "pets x days"),
    ("Non perishable food",
     "Three meals a day that need no cooking, no refrigeration and no can opener "
     "you have to find",
     "people x days x 3"),
    ("Pet food",
     "Full days, plus the medication",
     "pets x days"),
    ("Ice",
     "One bag per cooler per day, and it will not be for sale afterward",
     "coolers x days"),
    ("Cash, in small bills",
     "Card readers and ATMs both need power and a network. $100 per person is a "
     "floor, not a target",
     "people x 100, minimum"),
    ("Prescriptions",
     "A 30 day supply, refilled before the season rather than during it",
     "check every bottle"),
    ("Vehicle fuel",
     "Every tank full at 72 hours. Stations run dry, and the pumps are electric",
     "all vehicles"),
    ("Generator fuel",
     "A portable running eight to ten hours a day burns roughly 5 gallons. "
     "Stabilizer in every can",
     "5 x days"),
    ("Propane",
     "Two full tanks if you are cooking on the grill for a week",
     "2 tanks"),
    ("Batteries and power banks",
     "Sized to the flashlights and the radio you actually own, checked now",
     "count them"),
]

SUPPLY_KIT = [
    "Flashlights, one per person, and headlamps if you can. Not candles.",
    "A battery or crank NOAA weather radio.",
    "Power banks, all charged, plus a car charger for every phone.",
    "First aid kit, and the specific things your household takes.",
    "Manual can opener.",
    "Coolers, more than you think, and the ice to fill them.",
    "Trash bags, paper plates, disposable cutlery. There may be no water to wash up.",
    "Bleach, wet wipes, hand sanitizer.",
    "Tarps, rope, duct tape and a staple gun, for covering what breaks.",
    "A wrench or the shutoff key for the gas and the water.",
    "Work gloves, boots, and safety glasses for the cleanup.",
    "Baby formula, diapers, and anything else nobody else will remember.",
    "Pet carrier, leash, and the vaccination records, which shelters ask for.",
    "Insect repellent. The mosquitoes afterward are their own event.",
]

SUPPLY_WATCH = (
    "Fill the bathtubs and every large container the day before, but that water "
    "is for flushing toilets and washing, not for drinking. A tub is not clean. "
    "Freeze bottles of water in whatever freezer space is empty: they keep the "
    "freezer cold far longer than air does, and then you drink them."
)

# --- the timeline -----------------------------------------------------------

TIMELINE = [
    ("5 to 7 days out",
     "While it is still a disturbance and nobody is worried",
     [
         "Refill every prescription. Pharmacies will authorize an early refill "
         "with a storm in the Gulf, and will not once the power is out.",
         "Get cash. Small bills.",
         "Confirm this binder is filled in. This is the last calm week you get.",
         "Check that the shutter panels are labeled to their windows and the "
         "hardware is in one box with them.",
         "Do not wait for the cone to include you. The cone is where the center "
         "might track, not where the damage reaches.",
     ]),
    ("72 hours",
     "Decide now whether you are staying or going. Not at 24 hours",
     [
         "Fill every vehicle, and every fuel can, before the queues.",
         "Buy water, food and batteries today. Shelves are empty at 48 hours.",
         "Start the generator and run it under load. Fresh fuel or stabilizer.",
         "Set the refrigerator and freezer to their coldest settings.",
         "Freeze water in bottles and in any container that will fit.",
         "Wash every load of laundry and run the dishwasher.",
         "Charge every phone, power bank, tool battery and laptop.",
         "If you are leaving, book somewhere now and tell your out of state contact.",
     ]),
    ("48 hours",
     "Everything outdoors, in daylight, while it is still calm",
     [
         "Put the shutters or panels up. Not in the wind, and not in the dark.",
         "Bring in furniture, planters, grills, trash cans, toys, flags, anything "
         "loose. What stays out becomes a projectile.",
         "Clear gutters, drains and the yard inlets.",
         "Photograph the whole property again in its current condition.",
         "Trim nothing. There is no collection left and cut limbs at the curb are "
         "worse than limbs on the tree.",
         "Fill the bathtubs and large containers for flushing.",
     ]),
    ("24 hours",
     "Inside the house, and the last hour anyone leaves",
     [
         "If you are evacuating, go. Fuel and traffic decide this, not wind speed.",
         "Move documents, photographs and electronics up high and into plastic bins.",
         "Put furniture legs on blocks and roll the rugs up off the floor.",
         "Unplug electronics. The surge when power is restored destroys more "
         "equipment than the outage does.",
         "Park vehicles away from trees, on the highest ground you have, full.",
         "Pool: extra chlorine, drop the level a foot at most, kill the pump and "
         "heater at the breaker. Never drain it.",
     ]),
    ("When the wind arrives",
     "There is nothing left to do outside and nothing worth going out for",
     [
         "Interior room, no windows. A hallway, a closet, or a bathroom.",
         "Shoes on, everyone, including the children. Bike helmets are not silly.",
         "Turn the propane off at the tank.",
         "Phones charged, weather radio on, emergency alerts enabled.",
         "Stay off the road when the wind drops. That is the eye, and the second "
         "half arrives from the opposite direction.",
     ]),
]

# --- the shutdown sequence --------------------------------------------------

SHUTDOWN = [
    ("Photograph the house, last thing",
     "Inside and out, the condition you are leaving it in. This is the "
     "photograph that dates the damage to the storm."),
    ("Turn the water off at the main",
     "A supply line that lets go while nobody is home floods the house from the "
     "inside, and it is not a storm claim."),
    ("Turn off the water heater",
     "Gas to off, electric at the breaker. If the water is off and the tank "
     "drains, an electric element burns itself out dry within minutes."),
    ("Turn the propane off at the tank",
     "At the tank valve, not just at the appliance."),
    ("Unplug electronics and small appliances",
     "Televisions, computers, the microwave. Restoration surges are what kill "
     "them, and that happens whether you are home or not."),
    ("Decide about the air conditioning",
     "If you are not in a flood or surge zone, leave it running around 78 to 80. "
     "A closed house in Gulf humidity grows mold within days of the cooling "
     "stopping, and that is a bigger loss than the food. If water is coming, "
     "this does not apply."),
    ("Deal with the refrigerator",
     "Freeze a cup of water solid, lay a coin on top of the ice, and leave it in "
     "the freezer. If the coin is at the bottom when you get back, everything "
     "thawed and refroze and none of it is safe, however cold it feels."),
    ("Main breaker off, only if flooding is expected",
     "If surge or flood water is likely to reach the house, kill the main. If it "
     "is only wind, leaving it on is usually the better call. Never stand in "
     "water to touch a panel, in either direction."),
    ("Take the binder with you",
     "This one. Filled in. Plus the photographs of it that live in the cloud."),
]

GO_BAG = [
    "This binder, and a phone photograph of every filled page.",
    "Drivers licenses and passports.",
    "Insurance cards, the policy declarations page for each policy.",
    "Birth certificates, social security cards, marriage license, deed or lease.",
    "The last two years of tax returns, or where they live online.",
    "Prescriptions in their labeled bottles, and a written list of doses.",
    "Cash in small bills.",
    "Phone chargers, power banks, a car charger.",
    "A week of clothes, closed shoes, rain gear.",
    "Pet carrier, food, medication, vaccination records.",
    "Chargers and comfort items for children. A tablet loaded before you leave.",
    "Spare keys to the house and the vehicles.",
]

EVAC_FIELDS = [
    "Our evacuation zone",
    "How we confirm it is called",
    "Trigger: we leave when",
    "Primary destination and address",
    "Phone there",
    "Backup destination",
    "Route we take",
    "Backup route, inland not coastal",
    "Who we tell before leaving",
    "Where the pets go",
    "Pet friendly shelter or hotel booked",
    "Who is not able to drive themselves",
    "Medical needs and equipment that travels with us",
    "Where the documents and valuables are kept",
    "Boat, trailer or RV plan",
    "Where we meet if we are separated",
    "How we reach each other with no cell service",
    "Who checks the house before we come back",
]

# Deadlines are the quiet way a good claim goes bad. None of these are the same
# number in every state or on every policy, which is exactly why there is a
# blank rather than a printed figure.
CLAIM_DEADLINES = [
    "Notice of loss due within",
    "Proof of loss due within",
    "Deadline to file suit",
    "Date of loss",
]

CLAIM_DEADLINE_NOTE = (
    "Read these off your own policy and write them down on the day you report "
    "the claim. A proof of loss is a sworn, itemized statement of what you are "
    "claiming, and on many policies it is due within 60 days of the insurer "
    "asking for it. Miss it and the claim can be denied on the deadline alone, "
    "whatever the damage was. If the deadline is close and your numbers are not "
    "final, ask for an extension in writing rather than letting it pass."
)

EVAC_NOTE = (
    "Write the trigger down now, in words, while nobody is anxious. Something "
    "like “we leave when our zone is under a voluntary order” or “we leave 48 "
    "hours before landfall, whatever the category.” A decision made in advance "
    "gets followed. A decision made at midnight with a forecast changing does "
    "not, and that is how families end up leaving at the worst possible hour or "
    "not leaving at all."
)

# --- coming home ------------------------------------------------------------

REENTRY = [
    ("Do not go back until the area is opened",
     "Roads that look fine are undermined underneath, and the bridges have not "
     "all been inspected yet."),
    ("Treat every downed line as live",
     "And every puddle near one as energized. Power gets restored in pieces and "
     "a dead line becomes a live one without warning."),
    ("Never drive or walk through standing water",
     "You cannot see that the road is gone, and in this part of the country you "
     "cannot see what is swimming in it either."),
    ("If you smell gas, leave and call from somewhere else",
     "Do not switch anything on or off inside, including a light."),
    ("Do not turn breakers back on if anything got wet",
     "A panel, an outlet or an appliance that has been under water needs an "
     "electrician before it is energized. This is how house fires start in the "
     "week after a storm."),
    ("Generator outside only, twenty feet from any opening",
     "Not the garage with the door open, not under the carport. Carbon monoxide "
     "kills more people in the days after a Gulf hurricane than the wind does "
     "during it, and it has no smell. Never back feed the house through a wall "
     "socket: it kills the crew working on the line."),
    ("Assume the water is not safe until you are told it is",
     "Boil notices last days after the taps come back. On a well, assume "
     "contamination and test it."),
    ("Watch for wildlife in the debris",
     "Snakes move into anything dry. Fire ants raft in flood water and the raft "
     "looks like a patch of floating dirt until you touch it."),
]

MITIGATION = (
    "You have a duty to prevent further damage, and an insurer can reduce a "
    "claim for failing it. So tarp the roof, board the opening, pull the soaked "
    "carpet and get air moving, even before an adjuster has been. The rule is: "
    "photograph it thoroughly first, then mitigate, then keep every receipt. "
    "Reasonable mitigation spending is reimbursable, and in Gulf humidity mold "
    "is established within 24 to 48 hours, so waiting a week for permission "
    "turns a water claim into a mold claim."
)

# --- the logs ---------------------------------------------------------------

DAMAGE_COLUMNS = [
    ("Date", 0.62),
    ("Room or area", 1.15),
    ("What is damaged", 1.85),
    ("Cause", 0.78),
    ("Photo ref", 0.72),
    ("Value", 0.7),
]

DAMAGE_NOTE = (
    "Name a cause on every line, and use the insure’ words: wind, wind driven "
    "rain, tree, flood, or surge. Wind and flood are separate policies and the "
    "two companies will each argue the other one owes it. Rain that entered "
    "through a hole the wind made is a wind loss. The same water arriving across "
    "the ground is a flood loss. Guessing wrong out loud to an adjuster is "
    "expensive, so if you do not know, write what you saw rather than a "
    "conclusion."
)

CLAIM_COLUMNS = [
    ("Date", 0.6),
    ("Time", 0.5),
    ("Company", 1.0),
    ("Who, and their title", 1.25),
    ("Direct number", 0.9),
    ("What was said, and what they promised", 1.9),
]

CLAIM_NOTE = (
    "Get a name every single time, and the direct number or extension, because "
    "you will never reach the same person twice otherwise. Ask for anything "
    "important by email so it exists in writing. A claim is decided by a file, "
    "and the person keeping the better file usually wins the argument about what "
    "was agreed six weeks ago."
)

CLAIM_STEPS = [
    "Report it as early as you can, even before you know the extent. The claim "
    "number opens the file and the queue is first come.",
    "Report wind and flood separately, to each company, on the same day.",
    "Write your claim number on the top of every page in this section.",
    "Do not throw damaged property away until it has been photographed and, "
    "where practical, seen. Pile it where it can be inspected.",
    "Keep every receipt: tarps, a generator, a hotel, meals, the laundromat. "
    "Loss of use coverage pays for living somewhere else, and it is a separate "
    "limit from the building and the contents.",
    "Read the offer against your own damage log before accepting anything.",
    "You may hire your own licensed public adjuster, who works on a percentage. "
    "Check the license, and check the percentage against what your state caps "
    "it at after a declared disaster.",
]

# --- contractors ------------------------------------------------------------

CONTRACTOR_CHECKS = [
    ("State license number",
     "Look it up yourself on the state licensing boar’ website. Do not read it "
     "off the card they handed you."),
    ("General liability certificate",
     "Ask for it to come from their insurance agent directly to you. A photocopy "
     "proves nothing about whether the policy is still in force."),
    ("Workers compensation certificate",
     "If they do not carry it and someone is hurt on your roof, the claim comes "
     "to your homeowners policy."),
    ("A local physical address",
     "And how long they have been at it. Not a post office box and not a phone "
     "number that is only a cell."),
    ("Three local references from this year",
     "Then call them. Ask whether the final price matched the estimate and "
     "whether the crew came back to fix anything."),
    ("A written scope of work",
     "Materials named by brand and model, quantities, and a start and finish "
     "date. “Repair roof” is not a scope."),
    ("Who pulls the permit",
     "It should be them, in their name and license. A contractor asking you to "
     "pull the permit is asking you to carry the liability."),
    ("The payment schedule, in writing",
     "A deposit of a third at most, progress payments against work actually "
     "completed, and the final payment after your inspection. Never the full "
     "amount up front, and never cash."),
    ("A lien waiver at final payment",
     "Signed by the contractor and by any subcontractor or supplier. Without it "
     "an unpaid supplier can put a lien on your house even though you paid in "
     "full."),
]

CONTRACTOR_FIELDS = ["Company", "Contact and cell", "License number",
                     "License verified on", "Liability certificate received",
                     "Workers comp certificate received", "References called",
                     "Written estimate dated", "Deposit agreed", "Start date"]

FRAUD_SIGNS = [
    "They knocked on your door. The good contractors are already booked by "
    "people who called them.",
    "They offer to waive, absorb or cover your deductible. That is insurance "
    "fraud, the policyholder is a party to it, and it voids the claim.",
    "The price is only good today, or only if you sign now.",
    "They want a large deposit for materials, in cash, before anything is "
    "ordered.",
    "They ask you to sign an assignment of benefits, or a work authorization "
    "that turns out to be one. That signs your claim over to them and you lose "
    "control of the settlement.",
    "A free roof inspection finds serious damage nobody else can see, and they "
    "want to go up alone.",
    "Out of state plates, a magnetic sign on the truck, and no license number "
    "printed on the estimate.",
    "They discourage you from involving your insurer, or from getting a second "
    "quote.",
]

# --- back page --------------------------------------------------------------

HINDSIGHT = [
    "Filled the inventory in while the house was still standing.",
    "Photographed every room before, not just the wreckage after.",
    "Put the documents in the cloud instead of a fireproof box that flooded.",
    "Known the wind deductible as a dollar figure before the adjuster said it.",
    "Bought the scheduled endorsement for the jewelry, which cost almost nothing.",
    "Taken out cash on the Tuesday.",
    "Labeled the shutter panels to their windows the previous spring.",
    "Decided at 72 hours instead of arguing about it at midnight.",
    "Written down the name of everyone they spoke to.",
    "Kept the hotel and the tarp receipts.",
    "Waited a week and hired the local roofer instead of the one who knocked.",
]

DISCLAIMER = (
    "General preparedness and claims guidance, not legal advice and not a "
    "substitute for the terms of your own policy. Read your declarations page, "
    "and follow the instructions of local emergency management, which outrank "
    "anything printed here."
)
