# -*- coding: utf-8 -*-
"""The words on the generated resource pages.

Separate from build_resource_pages.py so the prose is editable without reading
past a template. Every agency named here was read on its own site on the date
in build_resource_pages.CHECKED.

The discipline, which is the whole reason anybody should trust these pages:
where a number varies by policy, by carrier or by state, say that it varies and
send the reader to the document that decides. Do not print a figure that would
be wrong for most readers in order to have a figure.
"""

CHECKED_LINE = "Checked against the named sources on 10 October 2026"

DOI_LINKS = """    <ul>
      <li><a href="https://www.mid.ms.gov/" target="_blank" rel="noopener">Mississippi Insurance Department</a></li>
      <li><a href="https://aldoi.gov/" target="_blank" rel="noopener">Alabama Department of Insurance</a></li>
      <li><a href="https://ldi.la.gov/consumers" target="_blank" rel="noopener">Louisiana Department of Insurance, consumers</a></li>
      <li><a href="https://myfloridacfo.com/division/consumers" target="_blank" rel="noopener">Florida Department of Financial Services, consumer services</a></li>
      <li><a href="https://www.tdi.texas.gov/consumer/index.html" target="_blank" rel="noopener">Texas Department of Insurance, consumer help</a></li>
    </ul>"""

LIMITS = ("This site is not affiliated with, or endorsed by, any insurance "
          "department, wind pool, licensing board or standards body named "
          "above. Their rules are theirs, they change, and their pages always "
          "win over this one. Nothing here is insurance, legal or financial "
          "advice: it is a map, drawn on the date stamped at the top.")

PAGES = [

    # ---------------------------------------------------------------- 1
    {
        "slug": "hurricane-deductibles",
        "title": "Hurricane Deductible: How the Percentage Works, in Dollars",
        "description": "A coastal hurricane deductible is usually a percentage of your dwelling limit, not a flat amount. How to work out yours in two minutes, and why it decides what a claim is worth.",
        "og_title": "Your hurricane deductible is a percentage, not a number",
        "og_description": "Most Gulf Coast policies carry a separate hurricane deductible set as a percentage of the dwelling limit. Here is how to find yours and turn it into a dollar figure.",
        "h1": "Your hurricane deductible, in dollars: how the percentage works",
        "standfirst": "Most homeowners can tell you their deductible and most of them are quoting the wrong one. On this coast there are usually two, and the one that applies to a named storm is not written as a dollar amount at all.",
        "checked": CHECKED_LINE,
        "body": """    <p class="lede">
      <strong>Work this out before you need it.</strong> It takes two minutes
      and one piece of paper, and it is the number that decides whether a storm
      claim is worth filing at all. Nobody can look it up for you, because it
      is a fact about your policy rather than about your state.
    </p>

    <h2>Why there are two deductibles</h2>
    <p>
      An ordinary homeowners deductible is a flat figure. A separate
      <strong>hurricane, named storm or windstorm deductible</strong> is common
      on coastal policies and works differently: it is normally set as a
      <strong>percentage of the dwelling limit</strong>, which is the
      Coverage&nbsp;A figure on your policy, rather than as an amount of money.
      When a qualifying storm causes the damage, that percentage deductible
      applies instead of the flat one.
    </p>
    <p>
      The percentage varies by carrier, by state and by how close to the water
      you are. The point of this page is not to tell you which percentage you
      have. It is to tell you that <em>a percentage is what you are looking
      for</em>, because that is the part most people do not know until a storm
      has already happened.
    </p>

    <h2>The arithmetic</h2>
    <p>
      Take the dwelling limit and multiply it by the percentage. That is the
      money that comes out of your pocket before the policy pays anything.
    </p>
    <ul>
      <li>A <strong>2 percent</strong> deductible on a
      <strong>$400,000</strong> dwelling limit is <strong>$8,000</strong>.</li>
      <li>A <strong>5 percent</strong> deductible on the same house is
      <strong>$20,000</strong>.</li>
    </ul>
    <p>
      Note what the percentage is taken from. It is the insured value of the
      structure, not what you paid for the house, not the land, and not the
      size of the claim. A small claim can be worth less than the deductible,
      which is a thing worth knowing on the day rather than three weeks later.
    </p>

    <h2>Where to find yours</h2>
    <ol>
      <li><strong>Pull your declarations page.</strong> It is the summary page
      at the front of the policy, and your agent or your insurer's website will
      send it to you the same day.</li>
      <li><strong>Find Coverage A, the dwelling limit.</strong> That is the
      number the percentage is taken from.</li>
      <li><strong>Find the deductible section</strong> and read it for a second
      entry: a hurricane, named storm or windstorm deductible shown as a
      percentage. If there is one, multiply.</li>
      <li><strong>Ask what triggers it.</strong> This is the part people get
      wrong. Policies differ on what sets the percentage deductible off: a
      named storm, a declared hurricane, or wind damage generally, and
      sometimes on when the trigger period starts and ends. Your policy defines
      it, and your agent can read you the definition.</li>
    </ol>

    <h2>Why it is worth knowing in April rather than September</h2>
    <p>
      Three things change once the figure is in front of you. You find out
      whether your emergency savings actually cover it. You find out whether
      raising or lowering the percentage is worth discussing with your agent
      while there is nothing in the Gulf. And the value of a
      <a href="../">roof grant</a> stops being abstract: if a stronger roof
      earns a
      <a href="../wind-mitigation-discounts/">wind mitigation credit</a> and
      the state pays toward the roof itself, the arithmetic is against a number
      you can now name.
    </p>

    <h2>Who to ask</h2>
    <p>
      Your agent first, because the answer is in your policy. If the answer you
      get does not match the policy, or you want to check what a carrier is
      allowed to do in your state, your insurance department is free and is not
      on the carrier's side of the table:
    </p>
""" + DOI_LINKS,
        "next": [
            ("../../storm/", "Storm season, start to claim",
             "the three numbers to find while the map is empty, and what to photograph after."),
            ("../wind-mitigation-discounts/", "Wind mitigation discounts",
             "the credit a stronger roof earns, state by state."),
            ("../", "The roof grant programs",
             "four Gulf states pay toward the roof that earns it."),
        ],
        "limits": LIMITS,
    },

    # ---------------------------------------------------------------- 2
    {
        "slug": "gulf-wind-pools",
        "title": "Wind Pools and Insurers of Last Resort, Gulf State by State",
        "description": "When no ordinary carrier will write wind coverage on your coastal home, each Gulf state has a fallback. What they are called, who runs them, and where to look.",
        "og_title": "The insurer of last resort in each Gulf state",
        "og_description": "TWIA, Citizens, Louisiana Citizens, MWUA and AIUA: what a wind pool is, when it is the answer, and the page in each state that decides.",
        "h1": "Wind pools, and the insurer of last resort in each Gulf state",
        "standfirst": "If no ordinary carrier will write wind coverage on your house, that is not the end of the conversation. Every Gulf state has a fallback, and each one has a different name, a different operator and different rules.",
        "checked": CHECKED_LINE,
        "body": """    <p class="lede">
      <strong>These are last resorts on purpose.</strong> They exist because
      the private market will not always write coastal wind, and they are
      generally intended for people who cannot get comparable coverage
      elsewhere. Eligibility, territory and what is covered are decided by each
      one's own plan of operation, not by us.
    </p>

    <h2>What a wind pool is</h2>
    <p>
      A residual market mechanism: a state-created association that writes the
      coverage the ordinary market is declining, usually windstorm and hail,
      often only inside a defined coastal territory. Some are wind-only, so the
      homeowner keeps a separate policy for everything else. Some also require
      flood insurance in a special flood hazard area. Whether one is right for
      you is a question for an agent and for the association itself.
    </p>
    <p>
      They matter on this site for a second reason:
      <strong>membership is sometimes the gate to a grant</strong>. The current
      phase of Mississippi's roof grant program, for example, is open to wind
      pool policyholders, which is on
      <a href="../strengthen-mississippi-homes/">its own page here</a>.
    </p>

    <h2>State by state</h2>

    <h3>Texas</h3>
    <p>
      The <strong>Texas Windstorm Insurance Association</strong>, TWIA, writes
      wind and hail in designated coastal territory. Texas also runs the WPI-8
      certificate system, which is how construction gets documented as
      compliant, and the two are connected: the certificate matters to what
      TWIA will insure. Both are covered on
      <a href="../texas-windstorm-coverage/">the Texas page</a>.
    </p>
    <ul><li><a href="https://www.twia.org" target="_blank" rel="noopener">twia.org</a></li></ul>

    <h3>Louisiana</h3>
    <p>
      <strong>Louisiana Citizens Property Insurance Corporation</strong>, the
      state's residual market property insurer, regulated by the Louisiana
      Department of Insurance.
    </p>
    <ul><li><a href="https://www.lacitizens.com/" target="_blank" rel="noopener">lacitizens.com</a></li></ul>

    <h3>Mississippi</h3>
    <p>
      The <strong>Mississippi Windstorm Underwriting Association</strong>,
      MWUA, commonly called the wind pool, writing wind and hail in the coastal
      counties. Mississippi also has the residential and commercial FAIR plans
      administered alongside it.
    </p>
    <ul>
      <li><a href="https://www.msplans.com/mwua/" target="_blank" rel="noopener">msplans.com/mwua</a>,
        the association's own pages. It is not at mwua.org, which belongs to an
        unrelated organization in Maine.</li>
      <li><a href="https://msplans.com/" target="_blank" rel="noopener">msplans.com</a>, the shared administrator site</li>
    </ul>

    <h3>Alabama</h3>
    <p>
      The <strong>Alabama Insurance Underwriting Association</strong>, AIUA,
      the state's beach and windstorm plan for the coastal area.
    </p>
    <ul><li><a href="https://www.aiua.org/" target="_blank" rel="noopener">aiua.org</a></li></ul>

    <h3>Florida</h3>
    <p>
      <strong>Citizens Property Insurance Corporation</strong>, which is
      considerably larger than the others and whose eligibility rules have
      moved repeatedly in recent years. Treat anything you read about Citizens
      eligibility, including on this page, as needing a check against their own
      site before you rely on it.
    </p>
    <ul><li><a href="https://www.citizensfla.com/" target="_blank" rel="noopener">citizensfla.com</a></li></ul>

    <h2>Do not wait for the storm</h2>
    <p>
      Like flood insurance, a wind pool will not sell you cover with a storm
      already in the Gulf. On October 7, 2026, with Named Storm Isaias
      approaching, the
      <a href="https://www.aiua.org/" target="_blank" rel="noopener">AIUA homepage</a>
      announced it had stopped accepting new business applications, and
      <a href="https://www.twia.org" target="_blank" rel="noopener">TWIA's</a>
      carried notices of a policy moratorium for the same storm, and of its
      lifting. Each pool's own homepage
      is where a suspension shows up, and the time to apply is while the map
      is empty.
    </p>

    <h2>Two things worth doing either way</h2>
    <ol>
      <li><strong>Ask an agent to shop the ordinary market first.</strong> A
      last resort is a last resort, and the pricing usually says so.</li>
      <li><strong>Ask what mitigation credits the pool itself offers.</strong>
      Several of these associations recognize FORTIFIED construction or wind
      mitigation features, which is the same lever as
      <a href="../wind-mitigation-discounts/">the discounts page</a>, and the
      roof grant programs are the cheapest way to pull it.</li>
    </ol>
""",
        "next": [
            ("../wind-mitigation-discounts/", "Wind mitigation discounts",
             "what a stronger roof earns you, state by state."),
            ("../hurricane-deductibles/", "Your hurricane deductible, in dollars",
             "the percentage that decides what a claim is worth."),
            ("../", "The roof grant programs",
             "four Gulf states pay toward a stronger roof."),
        ],
        "limits": LIMITS,
    },

    # ---------------------------------------------------------------- 3
    {
        "slug": "storm-contractors",
        "title": "Checking a Roofer After a Storm: Licenses, and the Deal to Walk Away From",
        "description": "Contractors follow landfalls, and the good ones and the bad ones knock on the same doors. How to check a license in each Gulf state, and the paperwork worth refusing.",
        "og_title": "How to check a roofer after a storm, in each Gulf state",
        "og_description": "The license lookup for each Gulf state, what a deposit demand tells you, and why signing your insurance claim over to a contractor is the paperwork to walk away from.",
        "h1": "Checking a contractor after a storm",
        "standfirst": "Contractors follow landfalls. Most are working honestly in a week when everyone needs them at once, and some are not, and they knock on the same doors on the same afternoon.",
        "checked": CHECKED_LINE,
        "body": """    <p class="lede">
      <strong>The check is free and it takes about five minutes.</strong> Every
      Gulf state runs a public license lookup, and the difference between a
      licensed contractor and a truck with a magnetic sign is a search box.
    </p>

    <h2>Look the license up yourself</h2>
    <p>
      Not the copy they hand you, and not the number on the card: the state's
      own register. Ask for the legal business name and the license number,
      then check it against the board that issues it. Requirements and
      thresholds differ by state and by the size of the job, so if you are not
      sure what a job needs, the board is the place to ask.
    </p>
    <ul>
      <li><a href="https://www.msboc.us/" target="_blank" rel="noopener">Mississippi State Board of Contractors</a></li>
      <li><a href="https://hblb.alabama.gov/" target="_blank" rel="noopener">Alabama Home Builders Licensure Board</a></li>
      <li><a href="https://lslbc.gov/" target="_blank" rel="noopener">Louisiana State Licensing Board for Contractors</a></li>
      <li><a href="https://www2.myfloridalicense.com/" target="_blank" rel="noopener">Florida DBPR license search</a></li>
      <li><a href="https://www.tdlr.texas.gov/" target="_blank" rel="noopener">Texas Department of Licensing and Regulation</a></li>
    </ul>
    <p>
      Texas is the one to read carefully rather than assume: it does not
      license general residential contractors the way its neighbors do, so
      "licensed" means something narrower there, and checking what a particular
      trade actually requires matters more.
    </p>

    <h2>The paperwork worth refusing</h2>
    <ul>
      <li><strong>Anything that hands over your insurance claim.</strong> An
      agreement that lets a contractor deal with your insurer on your behalf,
      or that assigns them your claim benefits, changes who controls the money
      and who can settle. Read anything like that slowly, and get advice before
      signing rather than after.</li>
      <li><strong>A large deposit before materials are on site.</strong> Ask
      what the deposit buys and when the materials arrive. A schedule of
      payments tied to work completed is normal; a big check tied to nothing
      is not.</li>
      <li><strong>An offer to cover your deductible.</strong> Your deductible
      is what you owe under the policy. Anyone offering to make it disappear is
      describing something for the insurer to look at, and it is your name on
      the claim.</li>
      <li><strong>Pressure to sign today.</strong> The roof will still need
      doing tomorrow. A contractor who cannot leave a written scope and a price
      overnight is telling you something.</li>
    </ul>

    <h2>What to keep</h2>
    <p>
      A written scope of work and a written price. Proof of license and
      insurance. Every invoice and receipt, including the emergency tarping.
      And a log of every call: the date, who you spoke to, and what they
      promised. That log is the single most useful thing a homeowner keeps
      after a storm and almost nobody keeps it.
    </p>

    <h2>Where to complain, and it is free</h2>
    <p>
      Two different places, depending on what went wrong. Licensing boards,
      above, handle the contractor. Insurance departments handle the claim:
    </p>
""" + DOI_LINKS + """
    <p>
      If the job is being done because a storm took the roof off, it is also
      the cheapest moment to rebuild to a stronger standard, and four Gulf
      states will pay toward that. <a href="../">The programs are here.</a>
    </p>
""",
        "next": [
            ("../../storm/", "Storm season, start to claim",
             "what to photograph before the cleanup, and how a wind claim differs from a flood claim."),
            ("../", "The roof grant programs",
             "rebuilding is the cheapest moment to build back stronger."),
            ("../hurricane-deductibles/", "Your hurricane deductible, in dollars",
             "the number an offer to \\u201ccover your deductible\\u201d is talking about."),
        ],
        "limits": LIMITS,
    },

    # ---------------------------------------------------------------- 4
    {
        "slug": "roof-age-and-insurance",
        "title": "Roof Age and Home Insurance on the Gulf Coast",
        "description": "Carriers care about roof age, and on this coast an older roof can affect what you are offered at renewal. What they look at, and what to do about it before you find out.",
        "og_title": "Roof age is the thing your insurer is looking at",
        "og_description": "Why roof age drives coastal underwriting, what an inspection actually looks for, and the lever that connects it to the grant programs.",
        "h1": "Roof age, and what your insurer is looking at",
        "standfirst": "The roof is the part of a coastal house an insurer thinks about first, because it is the part a hurricane takes first. Age is the cheapest signal they have, and it is the one most homeowners never look at until renewal.",
        "checked": CHECKED_LINE,
        "body": """    <p class="lede">
      <strong>This page does not print an age threshold, because there is no
      single one.</strong> Underwriting rules are set carrier by carrier and
      filed state by state, and a number that was right for one company this
      year is wrong for another. What is general enough to be useful is what
      they look at, and what you can do about it.
    </p>

    <h2>Why the roof and not the rest of the house</h2>
    <p>
      Wind damage tends to start at an edge and work inward. Once the covering
      or the deck goes, water follows, and a roof claim quickly becomes a
      contents and interior claim. That is why mitigation standards concentrate
      on how the deck is fastened and sealed and how the roof ties to the
      walls, and why a roof's age, material and condition carry more weight in
      a coastal file than almost anything else about the building.
    </p>

    <h2>What actually gets looked at</h2>
    <ul>
      <li><strong>Age and material.</strong> An architectural shingle roof and
      a metal roof of the same age are not the same risk. Typical Gulf Coast
      service lives are shorter than national averages because heat, humidity
      and UV do more work here, which is what the
      <a href="../../calculator/">Borrowed Time Calculator</a> is built
      on.</li>
      <li><strong>Condition, from an inspection.</strong> Lifted, curled or
      missing shingles, exposed fasteners, failed flashing and soft decking.
      Some of this is visible from the ground with binoculars, which is a task
      on <a href="../../guides/">the maintenance calendar</a> for exactly this
      reason.</li>
      <li><strong>Documented mitigation.</strong> This is the part homeowners
      can change. Features that reduce the chance of the roof coming off can
      earn premium credits when they are documented by an inspection or a
      certificate, which has
      <a href="../wind-mitigation-discounts/">its own page here</a>. An insurer
      prices what it can verify, not what is probably up there.</li>
    </ul>

    <h2>What to do before the renewal notice</h2>
    <ol>
      <li><strong>Find out how old it actually is.</strong> If the previous
      owner left you nothing, the county appraisal record and any permit
      history are the usual starting points, and a roofer can date a covering
      by looking at it.</li>
      <li><strong>Get the wind mitigation inspection.</strong> In Florida the
      state program performs one free, which is on
      <a href="../my-safe-florida-home/">the My Safe Florida Home page</a>, and
      the report is useful whether or not you take the grant. Elsewhere it is
      an inspection you pay for and it can pay for itself in credits.</li>
      <li><strong>Ask your agent the direct question.</strong> "What does my
      carrier do with roof age, and what documentation would improve my
      position?" is a question an agent can answer in a phone call.</li>
      <li><strong>If the roof is near the end anyway, look at the grant
      first.</strong> Four Gulf states put money toward rebuilding to a
      stronger standard, and doing it as a planned job rather than an emergency
      one is the difference between choosing a contractor and taking the one
      who knocked. <a href="../">The programs, state by state.</a></li>
    </ol>

    <h2>If you are non-renewed or cannot find cover</h2>
    <p>
      It happens on this coast and it is not automatically the end of the
      conversation. Shop the ordinary market through an agent first. If nobody
      will write it, every Gulf state has an insurer of last resort, which has
      <a href="../gulf-wind-pools/">its own page here</a>. And your state
      insurance department takes questions and complaints for free:
    </p>
""" + DOI_LINKS,
        "next": [
            ("../../calculator/", "The Borrowed Time Calculator",
             "how much life your roof and three other systems likely have left, from one number."),
            ("../wind-mitigation-discounts/", "Wind mitigation discounts",
             "the credits documented mitigation earns."),
            ("../gulf-wind-pools/", "Wind pools and insurers of last resort",
             "what happens when the ordinary market says no."),
        ],
        "limits": LIMITS,
    },
    # ---------------------------------------------------------------- 5
    {
        "slug": "wpi-8-certificate",
        "title": "WPI-8 Certificate Lookup: Which Texas Search to Use",
        "description": "How to find a Texas WPI-8 windstorm certificate for a house: TDI's search, TWIA's lookup for 2017 to 2020 work, what one costs, and what to do if there isn't one.",
        "og_title": "Finding a WPI-8 certificate, and which search to use",
        "og_description": "Texas keeps windstorm certificates in two places, depending on when the work was done. Which one to search, what an inspection costs, and what to ask a seller.",
        "h1": "Finding a WPI-8 certificate, and which search to use",
        "standfirst": "On the Texas coast, the WPI-8 is the paper that shows a house, a repair or an addition was built to the windstorm code. Insurers look it up. Buyers should too. It lives in one of two databases, depending on when the work was done.",
        "checked": CHECKED_LINE,
        "body": """    <p class="lede">
      <strong>Which search to use depends on when the work was
      finished.</strong> TDI's own page sends work completed between January
      2017 and May 2020 to TWIA's lookup, and everything else to TDI's. If you
      do not know the date, search both. Each takes a minute.
    </p>

    <h2>The two searches</h2>
    <ul>
      <li><strong>TDI's certificate search.</strong> The Texas Department of
      Insurance issues the WPI-8, for construction inspected while it was
      built, and the WPI-8E, for construction certified after it was
      finished. Both are in
      <a href="https://appscenter.tdi.texas.gov/windstorm/p/searchForAppl" target="_blank" rel="noopener">TDI's windstorm certificate search</a>.</li>
      <li><strong>TWIA's lookup, for 2017 to 2020.</strong> For a while the
      Texas Windstorm Insurance Association issued its own certificate, the
      WPI-8-C. TWIA's page says it accepted those applications from January 1,
      2017 to May 31, 2020. They are in
      <a href="https://www.twia.org/wpi-8-lookup/" target="_blank" rel="noopener">TWIA's WPI-8 lookup</a>,
      searched by ZIP code and street number, and TWIA sends you a copy of
      the certificate you request.</li>
    </ul>
    <p>
      Both are linked from
      <a href="https://www.tdi.texas.gov/wind/index.html" target="_blank" rel="noopener">TDI's windstorm inspections page</a>,
      which is the page that decides everything on this one. For older
      records TDI's page gives an address: engineering@tdi.texas.gov.
    </p>

    <h2>Who needs one</h2>
    <p>
      Per TDI's <a href="https://www.tdi.texas.gov/wind/documents/WPI-8-fact-sheet-eng-sp.pdf" target="_blank" rel="noopener">WPI-8 fact sheet</a>,
      homeowners in Aransas, Brazoria, Calhoun, Cameron, Chambers, Galveston,
      Jefferson, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio and
      Willacy counties, and in Harris County east of Highway 146. The fact
      sheet also says the reason in one line: TWIA and insurance companies
      can look certificates up to make sure the work is certified.
    </p>
    <p>
      Not every repair needs one. The fact sheet's advice is to call your
      local windstorm inspections office before starting any work and ask.
    </p>

    <h2>What one costs</h2>
    <p>
      The fact sheet gives two routes: request a free inspector from TDI, or
      hire a Texas-licensed professional engineer or an appointed qualified
      inspector. <strong>TDI does not regulate what those inspectors
      charge</strong>, so a private inspection is priced like any other
      professional service. Get the price in writing before the work starts.
    </p>
    <p>
      Timing matters more than price. The certificate is easiest when the
      inspections happen while the work is open, before the shingles cover
      what needs seeing. That is the point of calling before work starts.
    </p>

    <h2>If there is no certificate</h2>
    <p>
      Finished work can still be certified. TDI calls it completed
      construction certification, and its
      <a href="https://www.tdi.texas.gov/wind/completed-construction-certificates.html" target="_blank" rel="noopener">completed construction page</a>
      says the process changed on June 1, 2020. Per that page, TDI issues a
      WPI-8E after receiving a signed WPI-2E application and a sealed
      post-construction inspection report or sealed design, and any Texas
      licensed professional engineer can do the inspection. Whether a given
      house can be certified that way is a question for the engineer and for
      TDI, at Windstorm@tdi.texas.gov.
    </p>

    <h2>Buying a house on the coast</h2>
    <ol>
      <li><strong>Search both databases before you make an offer
      final.</strong> Then check the dates: a certificate for the house in 2009 says
      nothing about a roof replaced in 2021.</li>
      <li><strong>Ask the seller for the certificates.</strong> Sellers who
      have them usually keep them with the house papers.</li>
      <li><strong>Ask your agent how a missing certificate affects
      coverage.</strong> TWIA's own advice is to talk to an agent about all
      your options, and this is the question to bring.</li>
    </ol>

    <h2>Keep it with the house papers</h2>
    <p>
      A certificate is what makes compliant work visible to an insurer, and
      it matters again when you sell. The rest of the Texas picture, TWIA and
      the grant program Texas does not have, is on
      <a href="../texas-windstorm-coverage/">the Texas windstorm page</a>.
    </p>
""",
        "next": [
            ("../texas-windstorm-coverage/", "Texas windstorm coverage",
             "TWIA, the building standards, and the grant Texas does not have."),
            ("../wind-mitigation-discounts/", "Wind mitigation discounts",
             "what documented mitigation earns, state by state."),
            ("../storm-contractors/", "Checking a contractor",
             "the license lookup, and the paperwork worth refusing."),
        ],
        "limits": LIMITS,
    },
]
