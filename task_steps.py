#!/usr/bin/env python3
"""
Step-by-step detail for each of the 36 tasks.

Kept apart from build_calendars.py because this is the bulk of the writing and
it changes for different reasons than the schedule does.

Each entry may carry:
    need    things to have to hand before starting (omit if none)
    steps   the actual sequence, in order
    watch   a caution. Safety, or the mistake that costs money
    pro     True when this is a hire-someone job, so the steps are about
            what to ask for and how to check it was done

Some of these tasks are genuinely dangerous to get wrong, scalding water,
live circuits, ladders, carbon monoxide. Where that is true the caution says
so plainly rather than assuming the reader already knows.
"""

STEPS = {

    # --- JANUARY ----------------------------------------------------------
    "jan-detectors": {
        "need": ["Step ladder", "Fresh batteries"],
        "steps": [
            "Press and hold the test button on each unit until it sounds.",
            "Replace batteries in anything weak or chirping, usually a 9V or two AAs.",
            "Check the manufacture date printed on the back. Over ten years old means "
            "replace the whole unit, however well it tests.",
            "Confirm coverage: one inside each bedroom, one outside each sleeping area, "
            "and at least one on every floor.",
            "Vacuum the vents to clear dust, which is the usual cause of false alarms.",
        ],
        "watch": "An intermittent chirp usually means a low battery. A chirp that "
                 "continues after a fresh battery usually means the sensor has reached "
                 "end of life.",
    },
    "jan-freeze-prep": {
        "steps": [
            "Find the main shutoff. Commonly near the water heater, in the garage, or "
            "in a meter box by the street.",
            "Turn it fully off and back on. Old gate valves seize, and you want to find "
            "that out now rather than during a burst.",
            "Tag it so anyone in the house can find it without you.",
            "Fit insulated caps on outdoor spigots.",
            "If your shutoff is at the street, buy a meter key and keep it somewhere "
            "you will remember.",
        ],
    },
    "jan-attic-check": {
        "need": ["Flashlight", "Dust mask"],
        "steps": [
            "Go up in daylight with the attic light off and look for pinholes of daylight "
            "through the roof deck.",
            "Look for dark staining on the rafters and the underside of the decking.",
            "Press the insulation in several places. Damp or matted means water is getting in.",
            "Check around plumbing vents and any chimney flashing, the usual culprits.",
            "Photograph anything suspect so you can compare next year.",
        ],
        "watch": "Step only on the joists. The material between them will not hold you, "
                 "and the fall is through a ceiling.",
    },

    # --- FEBRUARY ---------------------------------------------------------
    "feb-termite-inspection": {
        "pro": True,
        "steps": [
            "Get quotes from two or three licensed pest control companies.",
            "Ask whether the price is inspection only or includes a bond, and exactly what "
            "the bond pays for: treatment, repairs, or both.",
            "Book before March. Schedules fill as soon as swarming starts.",
            "Clear access to the perimeter, the crawlspace hatch, and garage walls before "
            "they arrive.",
            "Keep the written report. It matters when you sell.",
        ],
    },
    "feb-hvac-filter": {
        "steps": [
            "Note the size printed on the edge of the old filter before you throw it out.",
            "Slide the new one in with the arrow pointing toward the unit.",
            "Set the thermostat to cool, several degrees below room temperature.",
            "Let it run ten to fifteen minutes. Air at the vents should be noticeably cold "
            "and the outdoor unit should be running.",
            "Listen for grinding, rattling, or the system starting and stopping repeatedly.",
        ],
    },
    "feb-caulk": {
        "need": ["Exterior-grade caulk", "Caulk gun", "Utility knife"],
        "steps": [
            "Walk the perimeter and look at every window, every door, and every pipe or "
            "wire that passes through a wall.",
            "Cut out any caulk that is cracked, shrunken, or pulling away.",
            "Clean and dry the gap. New caulk will not stick to dust.",
            "Run a fresh bead and tool it smooth with a wet fingertip.",
            "Leave the small weep holes at the bottom of window frames open. They are "
            "meant to drain and sealing them traps water in the wall.",
        ],
    },

    # --- MARCH ------------------------------------------------------------
    "mar-hvac-service": {
        "pro": True,
        "steps": [
            "Book a licensed technician before the first genuinely hot week.",
            "Ask them to check refrigerant charge, the capacitor, the contactor, coil "
            "condition, and the condensate line.",
            "Ask for the measured readings rather than an assurance that it is fine.",
            "Get the age of the equipment and their estimate of remaining life.",
            "Put that estimate straight onto your Watch List.",
        ],
    },
    "mar-gutters": {
        "need": ["Ladder", "Gloves", "Garden hose"],
        "steps": [
            "Scoop debris out by hand, moving the ladder often rather than reaching.",
            "Flush with a hose from the end furthest from the downspout.",
            "Watch that the water runs away freely and does not back up.",
            "Confirm every downspout discharges at least four to six feet from the "
            "foundation. Add an extension if it does not.",
            "Note any sagging sections or loose fasteners for repair.",
        ],
        "watch": "Have someone steady the ladder, and never rest it against the gutter "
                 "itself. It will bend and you will come down with it.",
    },
    "mar-grading": {
        "steps": [
            "Walk the perimeter during or straight after heavy rain, when problems show.",
            "Look for water pooling within a few feet of the wall.",
            "The ground should fall roughly six inches over the first ten feet away from "
            "the house.",
            "Note settled trenches over utility lines. They channel water back to the wall.",
            "Fill low spots with compacted soil. Mulch washes away and holds moisture "
            "against the foundation.",
        ],
    },

    # --- APRIL ------------------------------------------------------------
    "apr-swarm-season": {
        "steps": [
            "Check window sills and light fixtures for discarded wings after warm, humid "
            "evenings. That is often the only sign you get.",
            "Look along the slab edge, piers, and foundation walls for mud tubes about the "
            "width of a pencil.",
            "Break a tube open. If it is rebuilt within a few days, the colony is active.",
            "Tap suspect trim and baseboards. Hollow or papery means damage behind it.",
            "Call your pest company immediately if you find any of the above.",
        ],
        "watch": "Winged ants swarm at the same time and look similar. Termites have "
                 "straight antennae, two pairs of wings the same length, and no pinched waist.",
    },
    "apr-wash-exterior": {
        "steps": [
            "Wash from the bottom up with a garden hose and mild detergent.",
            "If you use a pressure washer, keep it on a low setting and never aim upward "
            "under siding laps. You will drive water into the wall.",
            "As you work, look for soft spots, cracks, and gaps you cannot see from a distance.",
            "Check soffits for holes. Wasps, squirrels, and birds all use them.",
            "Note anything needing paint or caulk while you can still see it wet.",
        ],
    },
    "apr-spigots-irrigation": {
        "steps": [
            "Turn each outdoor spigot fully on and look for weeping at the handle or where "
            "the pipe enters the wall.",
            "Replace worn hose washers. A few cents fixes most drips.",
            "Run each irrigation zone in turn and watch for broken heads and geysers.",
            "Adjust any head spraying the house, the drive, or the pavement.",
            "Check the backflow preventer if you have one.",
        ],
    },

    # --- MAY --------------------------------------------------------------
    "may-insurance-hurricane-prep": {
        "steps": [
            "Call your agent. Confirm wind coverage, your deductible (often a percentage "
            "of the insured value rather than a flat sum), and whether you carry flood at all.",
            "If you need flood cover, buy it now. NFIP policies generally take 30 days to "
            "take effect, so June 1 is already too late.",
            "Walk every room filming or photographing, opening closets and cabinets as you go.",
            "Photograph all four elevations of the house and the roof from the ground.",
            "Store all of it off the property: cloud storage, or email it to yourself.",
            "Trim limbs so nothing overhangs the roof.",
        ],
        "watch": "Percentage deductibles surprise people. On a $300,000 home a 2% wind "
                 "deductible is $6,000 out of your pocket before the policy pays anything.",
    },
    "may-generator-supplies": {
        "steps": [
            "Start the generator and run it under load for twenty to thirty minutes.",
            "Drain old fuel or treat it with stabilizer. Ethanol fuel degrades within months "
            "and is the usual reason one will not start.",
            "Restock: a gallon of water per person per day for a week, batteries, "
            "medications, and cash.",
            "Test-fit shutters or plywood on at least one opening, and label every piece to "
            "the window it fits.",
            "Confirm your evacuation route and where you would actually go.",
        ],
        "watch": "Never run a generator indoors, in a garage, or near an open window. "
                 "Carbon monoxide from generators kills people after every major storm.",
    },
    "may-secure-exterior": {
        "steps": [
            "Look up under the roof edge for lifted shingles and open or loose soffit panels.",
            "Have loose flashing and drip edge refastened before the season.",
            "Anchor sheds, and check fence posts for movement.",
            "Write the list of what comes indoors once a storm is named, so nobody has to "
            "think about it later.",
            "Remove dead limbs, which come down first.",
        ],
    },

    # --- JUNE -------------------------------------------------------------
    "jun-condensate-line": {
        "need": ["Wet/dry vacuum", "Distilled vinegar"],
        "steps": [
            "Turn the system off at the thermostat and at the breaker.",
            "Find the PVC drain line at the indoor unit, and its outdoor end.",
            "Hold the wet/dry vacuum to the outdoor end and run it two to three minutes to "
            "pull the blockage out.",
            "Pour a cup of distilled vinegar into the access port on the indoor side to "
            "clear the slime that causes it.",
            "Check the overflow pan is dry and the float switch moves freely.",
            "Restore power and confirm water is draining outside.",
        ],
        "watch": "If the pan has standing water, the line was already blocked and the "
                 "ceiling below may have been getting wet for a while.",
    },
    "jun-condenser-coils": {
        "steps": [
            "Cut power at the outdoor disconnect box, not just the thermostat.",
            "Clear leaves, grass clippings, and dirt from around the base.",
            "Rinse the coil fins gently with a hose from the inside outward. Never a "
            "pressure washer, it flattens the fins permanently.",
            "Straighten bent fins with a fin comb if you have one.",
            "Cut vegetation back two feet on all sides.",
            "Restore power and let it run.",
        ],
    },
    "jun-attic-ventilation": {
        "steps": [
            "From outside, check the soffit vents are not painted over or blocked.",
            "In the attic, confirm baffles are keeping insulation clear of the eaves so air "
            "can actually move.",
            "Measure insulation depth. Thirteen to sixteen inches of blown fiberglass is a "
            "reasonable target in this climate.",
            "Confirm bathroom fans vent outside and not into the attic, which is common and "
            "quietly destructive.",
            "Note the temperature. An attic far hotter than outside means the ventilation "
            "is not working.",
        ],
    },

    # --- JULY -------------------------------------------------------------
    "jul-leak-hunt": {
        "steps": [
            "Empty the cabinet under every sink and run a dry paper towel along each supply "
            "line and trap. Paper finds what fingers miss.",
            "Look for buckled cabinet floors and dark rings, which are evidence of a leak "
            "that has already dried.",
            "Check behind each toilet at the supply valve, and where the base meets the "
            "floor. Rock the bowl gently; movement means a failing seal.",
            "Look at the water heater base and its drip pan.",
            "Read the water meter with everything off, wait an hour, and read it again. "
            "Movement means a leak you have not found yet.",
        ],
    },
    "jul-crawlspace": {
        "need": ["Flashlight", "Old clothes", "Dust mask"],
        "steps": [
            "Look for standing water and consistently damp soil.",
            "Check the vapor barrier is intact, overlapped, and still covering the ground.",
            "Look up. Dark staining, sagging insulation, and rusted duct straps all mean "
            "moisture.",
            "Check piers and foundation walls for mud tubes.",
            "Note rodent droppings and chewed insulation.",
        ],
        "watch": "Wasps and snakes both like crawlspaces. If you smell gas or sewage, come "
                 "out and call someone rather than investigating.",
    },
    "jul-humidity": {
        "steps": [
            "Put an inexpensive hygrometer in the main living area and another in the least "
            "used room.",
            "Read over several days rather than once, humidity swings with the weather.",
            "Above 60% indoors, run a dehumidifier or have your A/C sizing checked. An "
            "oversized unit cools fast and never runs long enough to dry the air.",
            "Check bathroom fans actually pull by holding a tissue to the grille.",
            "Look for condensation on windows and on supply vents.",
        ],
    },

    # --- AUGUST -----------------------------------------------------------
    "aug-peak-season-check": {
        "steps": [
            "Re-read the declarations page of your policy and confirm it is paid and active.",
            "Refresh water and food, and check expiry dates on batteries and medication.",
            "Confirm your evacuation destination and route, and tell someone out of state "
            "what it is.",
            "Photograph or scan IDs, the deed, vehicle titles, and policies. Store them in "
            "the cloud.",
            "Fill vehicles and draw cash when a storm enters the Gulf, not once it has a name "
            "and everyone else is in line.",
        ],
    },
    "aug-gutters-again": {
        "steps": [
            "Clear the gutters again. Summer storms fill them faster than fall leaves do.",
            "Flush through and confirm flow at every downspout.",
            "Check downspout extensions have not been kicked or mown out of position.",
            "Look for shingle granules collecting in the gutter. A heavy amount means the "
            "roof is wearing out.",
            "Note any section that has begun to sag.",
        ],
    },
    "aug-photograph-valuables": {
        "steps": [
            "Photograph appliances, electronics, tools, and furniture room by room.",
            "Capture the model and serial plate on anything major, close enough to read.",
            "Keep receipts for big purchases in the same folder.",
            "Upload to cloud storage rather than leaving it on the phone that travels with you.",
            "Give someone off the coast access, in case you cannot get to it.",
        ],
    },

    # --- SEPTEMBER --------------------------------------------------------
    "sep-dryer-vent": {
        "need": ["Dryer vent brush kit", "Screwdriver", "Vacuum"],
        "steps": [
            "Unplug the dryer. If it is gas, shut the gas valve too.",
            "Pull it out and disconnect the duct from the back.",
            "Brush and vacuum the entire run, working from both the dryer end and the "
            "exterior hood.",
            "Check the exterior flap opens freely. It should not be screened, because "
            "screens trap lint immediately.",
            "Replace any foil accordion duct with rigid or semi-rigid metal.",
            "Reconnect, push back, and run the dryer while you check for strong airflow outside.",
        ],
        "watch": "Foil accordion duct is a known fire risk and is not permitted under many "
                 "codes. If yours has it, replacing it is the single most useful thing here.",
    },
    "sep-roof-inspection": {
        "steps": [
            "Walk all four sides with binoculars in good light.",
            "Look for lifted, curled, cracked, or missing shingles.",
            "Check the ridge and hip caps, which fail first.",
            "Look at flashing around chimneys, vents, and in the valleys.",
            "Look for dark patches, which usually mean lost granules.",
            "Photograph anything you find, dated, for comparison and for any claim.",
        ],
        "watch": "Stay off the roof. Everything that matters is visible from the ground, "
                 "and a fall costs far more than a repair.",
    },
    "sep-sump-drainage": {
        "steps": [
            "Pour a bucket of water into the sump pit and confirm the pump starts and "
            "empties it.",
            "Check the discharge line runs well away from the house and is not blocked.",
            "Clear leaves and silt from drainage swales and ditches.",
            "Confirm the check valve is not letting water run back into the pit.",
            "Test the battery backup if you have one, since the power tends to go at the "
            "same time as the rain arrives.",
        ],
    },

    # --- OCTOBER ----------------------------------------------------------
    "oct-flush-water-heater": {
        "need": ["Garden hose", "Flathead screwdriver"],
        "steps": [
            "Turn off power at the breaker for an electric heater, or set the gas valve to "
            "pilot for gas.",
            "Close the cold water supply valve on top of the tank.",
            "Attach a hose to the drain valve at the base and run it somewhere that can take "
            "scalding water.",
            "Open a hot faucet somewhere in the house to break the vacuum.",
            "Open the drain valve and let it run until the water is clear. Expect sediment, "
            "and expect it to take a while.",
            "Close the drain, refill fully with that hot faucet still open until water runs "
            "steady, then restore power or gas.",
        ],
        "watch": "The water is hot enough to scald badly. Let the tank cool for a few hours "
                 "first. Never restore power to an electric heater before it is full: the "
                 "element burns out in seconds.",
    },
    "oct-weatherstripping": {
        "steps": [
            "Close each exterior door on a strip of paper. If it pulls out with no "
            "resistance, the seal has gone.",
            "Replace worn weatherstripping and door sweeps.",
            "Check the attic hatch has a gasket and insulation on its back face.",
            "Feel around outlets on exterior walls for drafts.",
            "Check the door from the garage into the house seals and self-closes.",
        ],
    },
    "oct-chimney": {
        "pro": True,
        "steps": [
            "Have a sweep inspect and clean before the first fire of the year.",
            "Ask them to check the cap, the crown, and the flashing while they are up there.",
            "Confirm the damper opens and closes fully.",
            "Look for nests and debris, which accumulate over a long warm season.",
            "Check the firebox for cracked mortar.",
        ],
    },

    # --- NOVEMBER ---------------------------------------------------------
    "nov-post-season-inspection": {
        "steps": [
            "Walk all four elevations and the roof line with binoculars.",
            "Photograph anything new and compare against the photographs you took in May.",
            "Check the fence, shed, and window screens.",
            "Look in the attic for daylight or staining that was not there before.",
            "File any claim now. Most policies require prompt notice, and insurers get "
            "harder to convince the longer you wait.",
        ],
    },
    "nov-filter-heat-test": {
        "steps": [
            "Replace the filter.",
            "Set the thermostat to heat, a few degrees above room temperature.",
            "Expect a burning-dust smell for the first few minutes. That is normal.",
            "Confirm warm air at the vents within a few minutes.",
            "If it will not fire, or you smell gas at any point, shut it down and call "
            "someone.",
        ],
    },
    "nov-gutters-fascia": {
        "steps": [
            "Clear the gutters once the leaves have finished dropping.",
            "Look closely at the fascia board behind the gutter for soft, dark, or peeling wood.",
            "Press it with a screwdriver. If the tip sinks in, it is rotten.",
            "Check the drip edge is present and tucked under the shingles.",
            "Note repairs for spring rather than starting them in the wet.",
        ],
    },

    # --- DECEMBER ---------------------------------------------------------
    "dec-freeze-prep": {
        "steps": [
            "Fit foam sleeves on exposed pipes in the garage, crawlspace, and along "
            "exterior walls.",
            "Cover spigots with insulated caps.",
            "Disconnect and drain garden hoses. A hose left connected is the single most "
            "common cause of a burst pipe.",
            "Confirm you know where the main shutoff is and that it still turns.",
            "On a hard freeze night, open the cabinet doors under sinks and let the faucet "
            "furthest from the meter drip.",
        ],
    },
    "dec-gfci-breakers": {
        "steps": [
            "Press TEST on every GFCI outlet, kitchen, bathrooms, garage, and outdoors. "
            "The power should cut immediately.",
            "Press RESET to restore it.",
            "Replace any that will not trip, or will not reset.",
            "Remember one GFCI often protects several ordinary outlets downstream, so test "
            "those too.",
            "Label the panel: switch breakers off one at a time and write down what stops "
            "working.",
        ],
    },
    "dec-watch-list": {
        "steps": [
            "Get out the Watch List.",
            "Enter this year against anything you replaced or had serviced.",
            "Update the 'start watching in' column for those items.",
            "Mark anything now within five years of its expected life.",
            "Decide a monthly amount to set aside for whichever item is closest.",
        ],
    },
}
