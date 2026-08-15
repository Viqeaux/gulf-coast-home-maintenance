#!/usr/bin/env python3
"""
Build the Storm Season Binder as HTML, then hand it to headless Chrome.

Same three print constraints as the kit, for the same reasons: nothing bleeds,
ink is the buyer's money, and it has to read in grayscale. The design system is
literally the kit's, imported rather than copied, so the two products look like
they came from the same shop and a fix to one fixes both.

What is different is that the binder is mostly blanks. The kit is a thing you
read; this is a thing you fill in. So the pages are built around ruled fields
and log rows, every one of them marked data-fill, and build_fillable.stamp()
turns the whole set into a real AcroForm.

Pages are checked for overflow on every build. The binder has far more dense
tables than the kit does and a page that silently runs past the sheet is
invisible in HTML and truncated in the PDF.

Run:  python build_storm_binder.py            print edition
      python build_storm_binder.py --fillable both, needs pypdf and reportlab
Out:  product/gulf-coast-storm-season-binder.html
      product/gulf-coast-storm-season-binder.pdf
      product/gulf-coast-storm-season-binder-fillable.pdf
"""

import json
import os
import re
import subprocess
import sys

from build_calendars import VERSION
from build_printables import (CHROME_CANDIDATES, CSS, DOCUMENT, OUT_DIR, esc,
                              find_chrome, page)
import binder_pages as C

BASENAME = "gulf-coast-storm-season-binder"


# --- small helpers ----------------------------------------------------------

def fill_row(label, hint=""):
    """A captioned blank. The label sits above the rule rather than beside it,
    which keeps the writing space full width on a narrow column."""
    return ('        <div class="rec-row">\n'
            '          <p class="rec-label">{0}</p>\n'
            '          <div class="rec-line" data-fill="text"></div>\n'
            '{1}'
            '        </div>\n'.format(
                esc(label),
                '          <p class="rec-hint">{0}</p>\n'.format(esc(hint)) if hint else ""))


def rec_block(title, labels):
    rows = "".join(fill_row(label) for label in labels)
    return ('      <div class="rec-block">\n'
            '        <p class="rec-title">{0}</p>\n{1}'
            '      </div>\n'.format(esc(title), rows))


def checklist(items, tight=False):
    out = ""
    for item in items:
        out += ('      <li><span class="box" data-fill="check"></span>{0}</li>\n'
                .format(esc(item)))
    return '    <ul class="checklist{0}">\n{1}    </ul>\n'.format(
        " checklist--tight" if tight else "", out)


def widths(columns):
    """Column widths arrive as rough inches. Normalize to percentages so the
    table always fills the text block whatever the margins do later."""
    total = sum(w for _, w in columns)
    return [(name, 100.0 * w / total) for name, w in columns]


def log_table(columns, rows, klass="log-table"):
    head = "".join(
        '<th style="width:{0:.2f}%">{1}</th>'.format(pct, esc(name))
        for name, pct in widths(columns))
    body = ""
    for _ in range(rows):
        body += ('        <tr>{0}</tr>\n'.format(
            "".join('<td class="fill" data-fill="text"></td>' for _ in columns)))
    return ('    <table class="{0}">\n'
            '      <thead><tr>{1}</tr></thead>\n'
            '      <tbody>\n{2}      </tbody>\n'
            '    </table>\n'.format(klass, head, body))


# --- the pages --------------------------------------------------------------

def cover_page():
    return page(
        '    <div class="cover">\n'
        '      <p class="kicker">The Gulf Coast</p>\n'
        '      <h1 class="cover-title">Storm&nbsp;Season<br>Binder</h1>\n'
        '      <div class="cover-rule"></div>\n'
        '      <p class="cover-sub">Everything you will be asked for in a hurry, '
        'written down while it was calm.</p>\n'
        '      <p class="cover-note">Undated &middot; Fill it in once &middot; '
        'Print it again next season</p>\n'
        '      <p class="cover-feeds-note">Insurance and account numbers &middot; '
        'Room by room home inventory &middot; What to photograph &middot; Water and '
        'supply calculator &middot; The 72 hour sequence &middot; Shutdown and '
        'evacuation &middot; Damage log &middot; Claim call log &middot; Contractor '
        'vetting</p>\n'
        '    </div>',
        foot="")


def how_to_use_page():
    phases = [
        ("Now, while it is calm",
         "Fill in the record pages: policies, accounts, the inventory. This is "
         "the only time these can be filled in, and it is the whole reason the "
         "binder exists."),
        ("When a storm is named",
         "Work the countdown pages in order. They are written as a sequence "
         "because the order is what people get wrong, not the individual jobs."),
        ("After it passes",
         "Read the re-entry page before you touch anything, then photograph "
         "before you clean."),
        ("The claim, for the next six months",
         "The damage log and the call log. This is where the money actually is, "
         "and it is the part everybody underestimates."),
    ]
    rows = ""
    for name, text in phases:
        rows += ('      <div class="when-row">\n'
                 '        <p class="when-label">{0}</p>\n'
                 '        <p class="when-text">{1}</p>\n'
                 '      </div>\n'.format(esc(name), esc(text)))

    return page(
        '    <p class="eyebrow">How to use this</p>\n'
        '    <h2>Four moments, in order</h2>\n'
        '    <p class="lede">A binder is not a leaflet. Most of these pages are '
        'blanks, and a blank page is worth nothing on the day it is needed unless '
        'somebody filled it in months earlier.</p>\n'
        '{0}'
        '    <p class="sub-label">Two things to do before you file this away</p>\n'
        '    <ul class="plain">\n'
        '      <li><strong>Put it in a real binder, in a bag that seals.</strong> '
        'Paper in a Gulf Coast house in September is a temporary format.</li>\n'
        '      <li><strong>Photograph every page once it is filled in</strong> and '
        'put the pictures in cloud storage. The paper copy is the one you lose. '
        'The photographs are the ones that survive, and they are readable from a '
        'phone in a hotel three states away, which is where a great many of these '
        'claims actually get made.</li>\n'
        '    </ul>\n'
        '    <p class="pull">Nothing in here asks you to buy anything you do not '
        'already own. It asks you to write down what you own, what it costs to '
        'replace, and who to call, before the week when none of that can be '
        'looked up.</p>\n'.format(rows),
        foot="How to use this")


def before_season_page():
    jobs = [
        "Read your declarations page and write the wind deductible here as a "
        "dollar figure",
        "Check whether you have flood coverage at all. Most homeowners policies "
        "have none",
        "If you are buying flood cover, buy it now: it takes 30 days to take effect",
        "Ask about scheduled endorsements for jewelry, firearms, cameras and tools",
        "Fill in the policy and account pages in this binder",
        "Photograph and video every room, then get the files off the phone",
        "Fill in the inventory sheets, one room at a time",
        "Refill prescriptions and check what a 30 day supply looks like",
        "Test the generator under load, and rotate the fuel",
        "Label every shutter panel to its window, and box the hardware with them",
        "Agree the evacuation trigger with everyone in the house, and write it down",
        "Photograph these pages and upload them",
    ]
    return page(
        '    <p class="eyebrow">Before June 1</p>\n'
        '    <h2>The calm week list</h2>\n'
        '    <p class="lede">Twelve things, none of which can be done once a storm '
        'is in the Gulf. Work down them in an evening or two in the spring and the '
        'rest of this binder is already written.</p>\n'
        '{0}'
        '    <p class="pull">A flood policy generally takes 30 days to take effect. '
        'That is why this list belongs in May, and why June 1 is already too late '
        'to start the only part of it that cannot be hurried.</p>\n'.format(
            checklist(jobs, tight=True)),
        foot="Before the season")


def policy_page_one():
    left = rec_block(*C.POLICY_BLOCKS[0])
    right = "".join(rec_block(title, labels)
                    for title, labels in C.POLICY_BLOCKS[1:])
    return page(
        '    <p class="eyebrow">The record</p>\n'
        '    <h2>Policies and coverage</h2>\n'
        '    <p class="lede">{0}</p>\n'
        '    <div class="rec-grid">\n'
        '      <div>\n{1}      </div>\n'
        '      <div>\n{2}      </div>\n'
        '    </div>\n'
        '    <p class="watch watch--block"><span>Watch out</span>{3}</p>\n'.format(
            esc(C.SECURITY_NOTE), left, right, esc(C.POLICY_WATCH)),
        foot="Policies")


def policy_page_two():
    blocks = [rec_block(title, labels) for title, labels in C.UTILITY_BLOCKS]
    # Four blocks into three columns: the short one rides under the third.
    blocks = [blocks[0], blocks[1], "".join(blocks[2:])]
    return page(
        '    <p class="eyebrow">The record</p>\n'
        '    <h2>Numbers you will want in the first hour</h2>\n'
        '    <p class="lede">Outage lines are busy and their websites go down with '
        'the grid. Write the numbers rather than planning to look them up.</p>\n'
        '    <div class="rec-grid rec-grid--three">\n'
        '      <div>\n{0}      </div>\n'
        '      <div>\n{1}      </div>\n'
        '      <div>\n{2}      </div>\n'
        '    </div>\n'
        '    <p class="pull">{3}</p>\n'.format(
            blocks[0], blocks[1], blocks[2], esc(C.POLICY_NOTE)),
        foot="Contacts")


def photograph_page():
    sets = ""
    for title, items in C.PHOTO_SETS:
        rows = "".join(
            '        <li><span class="box" data-fill="check"></span>{0}</li>\n'
            .format(esc(item)) for item in items)
        sets += ('      <div class="photo-set">\n'
                 '        <p class="rec-title">{0}</p>\n'
                 '        <ul class="checklist checklist--flush">\n{1}        </ul>\n'
                 '      </div>\n'.format(esc(title), rows))

    return page(
        '    <p class="eyebrow">Do this before anything happens</p>\n'
        '    <h2>What to photograph</h2>\n'
        '    <p class="lede">{0}</p>\n'
        '{1}'
        '    <p class="watch watch--block"><span>Watch out</span>{2}</p>\n'.format(
            esc(C.PHOTO_METHOD), sets, esc(C.PHOTO_WATCH)),
        foot="What to photograph")


def photo_storage_page():
    items = "".join('      <li>{0}</li>\n'.format(esc(item))
                    for item in C.PHOTO_STORAGE)
    photos = ["Where the photographs live",
              "Account and login hint",
              "Date of the last full walkthrough",
              "Who else in the household can get to them"]
    left = "".join(fill_row(label) for label in
                   photos + C.DOCUMENT_LOCATIONS[:2])
    right = "".join(fill_row(label) for label in C.DOCUMENT_LOCATIONS[2:])

    return page(
        '    <p class="eyebrow">Facing the photographs</p>\n'
        '    <h2>Where it all lives</h2>\n'
        '    <p class="lede">A photograph on the phone in your pocket is a '
        'photograph in the same flood as the house. Getting the files somewhere '
        'else is the half of this job people skip, and the same is true of every '
        'document underneath.</p>\n'
        '    <ul class="plain plain--tight">\n{0}    </ul>\n'
        '    <p class="sub-label">Photographs, and where the paper is</p>\n'
        '    <div class="rec-grid">\n'
        '      <div>\n{1}      </div>\n'
        '      <div>\n{2}      </div>\n'
        '    </div>\n'.format(items, left, right),
        foot="Where it lives")


def inventory_intro_page():
    method = "".join('      <li>{0}</li>\n'.format(esc(item))
                     for item in C.INVENTORY_METHOD)
    head = "".join('<th>{0}</th>'.format(esc(label))
                   for label, _ in C.INVENTORY_EXAMPLE)
    cells = "".join('<td>{0}</td>'.format(esc(value))
                    for _, value in C.INVENTORY_EXAMPLE)

    return page(
        '    <p class="eyebrow">The largest number in your policy</p>\n'
        '    <h2>The home inventory</h2>\n'
        '    <p class="lede">{0}</p>\n'
        '    <p class="sub-label">How much detail is enough</p>\n'
        '    <table class="log-table example-table">\n'
        '      <thead><tr>{1}</tr></thead>\n'
        '      <tbody><tr>{2}</tr></tbody>\n'
        '    </table>\n'
        '    <p class="example-note">{3}</p>\n'
        '    <p class="sub-label">How to actually get it done</p>\n'
        '    <ul class="plain plain--tight">\n{4}    </ul>\n'
        '    <p class="watch watch--block"><span>Watch out</span>{5}</p>\n'.format(
            esc(C.INVENTORY_INTRO), head, cells,
            esc(C.INVENTORY_EXAMPLE_NOTE), method, esc(C.INVENTORY_WATCH)),
        foot="The inventory")


def inventory_page(name, prompt, rows):
    cols = [(c, 1.0) for c in C.INVENTORY_COLUMNS]
    # The item column carries most of the writing, the year almost none.
    weights = [2.0, 1.5, 1.1, 0.5, 1.15]
    cols = [(c, w) for (c, _), w in zip(cols, weights)]

    head = "".join('<th style="width:{0:.2f}%">{1}</th>'.format(pct, esc(cname))
                   for cname, pct in widths(cols))
    body = ""
    for _ in range(rows):
        body += '        <tr>{0}</tr>\n'.format(
            "".join('<td class="fill" data-fill="text"></td>' for _ in cols))

    return page(
        '    <p class="eyebrow">Home inventory</p>\n'
        '    <h2 class="inv-name">{0}</h2>\n'
        '    <p class="inv-prompt">{1}</p>\n'
        '    <table class="log-table inv-table">\n'
        '      <thead><tr>{2}</tr></thead>\n'
        '      <tbody>\n{3}      </tbody>\n'
        '    </table>\n'.format(esc(name), esc(prompt), head, body),
        foot=name)


def supply_page():
    rows = ""
    for label, rule, math in C.SUPPLY_ROWS:
        rows += ('        <tr>\n'
                 '          <td class="calc-item">{0}</td>\n'
                 '          <td class="calc-rule">{1}</td>\n'
                 '          <td class="calc-math">{2}</td>\n'
                 '          <td class="fill" data-fill="text"></td>\n'
                 '        </tr>\n'.format(esc(label), esc(rule), esc(math)))

    heads = "".join(
        '        <div class="head-cell">\n'
        '          <p class="rec-label">{0}</p>\n'
        '          <div class="rec-line rec-line--short" data-fill="text"></div>\n'
        '        </div>\n'.format(esc(label))
        for label in ["People in the household", "Pets", "Days of supply",
                      "Coolers"])

    return page(
        '    <p class="eyebrow">Work it out once</p>\n'
        '    <h2>Water and supplies</h2>\n'
        '    <p class="lede">{0}</p>\n'
        '    <div class="calc-head">\n{1}    </div>\n'
        '    <table class="calc-table">\n'
        '      <thead><tr>\n'
        '        <th>What</th><th>The rule</th><th>Your arithmetic</th>'
        '<th>Your number</th>\n'
        '      </tr></thead>\n'
        '      <tbody>\n{2}      </tbody>\n'
        '    </table>\n'
        '    <p class="watch watch--block"><span>Watch out</span>{3}</p>\n'.format(
            esc(C.SUPPLY_INTRO), heads, rows, esc(C.SUPPLY_WATCH)),
        foot="Water and supplies")


def supply_kit_page():
    return page(
        '    <p class="eyebrow">Facing the calculator</p>\n'
        '    <h2>The rest of the kit</h2>\n'
        '    <p class="lede">Check this in May, not in August. Every item here is '
        'sold out on this coast within a day of a name being given to something in '
        'the Gulf.</p>\n'
        '{0}'
        '    <p class="pull">Buy the boring half now. The flashlights, the radio, '
        'the manual can opener and the work gloves cost nothing in the spring and '
        'cannot be had at any price in the queue.</p>\n'.format(
            checklist(C.SUPPLY_KIT, tight=True)),
        foot="The kit")


def timeline_pages():
    pages = []
    for part, blocks in ((1, C.TIMELINE[:2]), (2, C.TIMELINE[2:])):
        body = ""
        for when, sub, items in blocks:
            rows = "".join(
                '          <li><span class="box" data-fill="check"></span>{0}</li>\n'
                .format(esc(item)) for item in items)
            body += ('      <div class="tl-block">\n'
                     '        <p class="tl-when">{0}</p>\n'
                     '        <p class="tl-sub">{1}</p>\n'
                     '        <ul class="checklist checklist--flush">\n{2}        </ul>\n'
                     '      </div>\n'.format(esc(when), esc(sub), rows))

        if part == 1:
            head = ('    <p class="eyebrow">When a storm is named</p>\n'
                    '    <h2>The countdown</h2>\n'
                    '    <p class="lede">Written as a sequence because the order is '
                    'what goes wrong. Almost nobody fails because they did not know '
                    'to buy water. They fail because they bought it on the wrong '
                    'day.</p>\n')
        else:
            head = ('    <p class="eyebrow">When a storm is named</p>\n'
                    '    <h2 class="month-name">The countdown'
                    '<span class="cont">continued</span></h2>\n'
                    '    <div class="tl-gap"></div>\n')

        pages.append(page('{0}{1}'.format(head, body),
                          foot="The countdown"))
    return pages


def shutdown_page():
    steps = ""
    for index, (title, text) in enumerate(C.SHUTDOWN, start=1):
        steps += ('      <div class="seq-row">\n'
                  '        <p class="seq-num">{0}</p>\n'
                  '        <div class="seq-body">\n'
                  '          <p class="seq-title">{1}'
                  '<span class="box box--task" data-fill="check"></span></p>\n'
                  '          <p class="seq-text">{2}</p>\n'
                  '        </div>\n'
                  '      </div>\n'.format(index, esc(title), esc(text)))
    return page(
        '    <p class="eyebrow">The last hour in the house</p>\n'
        '    <h2>Shutdown sequence</h2>\n'
        '    <p class="lede">In this order. Two of these undo each other if you '
        'do them the wrong way round, and one of them is the difference between a '
        'spoiled freezer and a house full of mold.</p>\n'
        '    <div class="seq">\n{0}    </div>\n'.format(steps),
        foot="Shutdown")


def go_bag_page():
    return page(
        '    <p class="eyebrow">If you leave</p>\n'
        '    <h2>What goes in the car</h2>\n'
        '    <p class="lede">Packed as a list rather than as a decision. Standing '
        'in a hallway at four in the morning is not when anyone should be working '
        'out whether the deed matters.</p>\n'
        '{0}'
        '    <p class="pull">Everything on this list that is paper should also '
        'exist as a photograph in the cloud. Then losing the bag is an '
        'inconvenience rather than a second disaster.</p>\n'.format(
            checklist(C.GO_BAG, tight=True)),
        foot="The go bag")


def evacuation_page():
    half = -(-len(C.EVAC_FIELDS) // 2)
    left = "".join(fill_row(label) for label in C.EVAC_FIELDS[:half])
    right = "".join(fill_row(label) for label in C.EVAC_FIELDS[half:])
    return page(
        '    <p class="eyebrow">Agree it in the spring</p>\n'
        '    <h2>The evacuation plan</h2>\n'
        '    <p class="lede">{0}</p>\n'
        '    <div class="rec-grid">\n'
        '      <div>\n{1}      </div>\n'
        '      <div>\n{2}      </div>\n'
        '    </div>\n'
        '    <p class="watch watch--block"><span>Watch out</span>Contraflow turns '
        'the interstate one way and closes the crossings you would normally use, '
        'so the route you drive every day may not exist on the day you need it. '
        'Look up your parish or county evacuation route now, write it in the box, '
        'and pick an inland backup rather than a coastal one.</p>\n'.format(
            esc(C.EVAC_NOTE), left, right),
        foot="Evacuation")


def reentry_page():
    rows = ""
    for title, text in C.REENTRY:
        rows += ('      <div class="when-row">\n'
                 '        <p class="when-label">{0}</p>\n'
                 '        <p class="when-text">{1}</p>\n'
                 '      </div>\n'.format(esc(title), esc(text)))
    return page(
        '    <p class="eyebrow">Coming home</p>\n'
        '    <h2>Before you touch anything</h2>\n'
        '    <p class="lede">More people are hurt in the week after a Gulf '
        'hurricane than during it, and almost none of it is from wind.</p>\n'
        '{0}'
        '    <p class="watch watch--block"><span>Then, and only then</span>{1}</p>\n'
        .format(rows, esc(C.MITIGATION)),
        foot="Coming home")


def damage_log_pages():
    pages = []
    for part in (1, 2):
        if part == 1:
            head = ('    <p class="eyebrow">After the storm</p>\n'
                    '    <h2>Damage log</h2>\n'
                    '    <p class="lede">Photograph first, then write the line. '
                    'One line per item, however small, because the small ones add '
                    'up to more than people expect and none of them are remembered '
                    'six weeks later.</p>\n')
            note = ('    <p class="watch watch--block"><span>Watch out</span>{0}</p>\n'
                    .format(esc(C.DAMAGE_NOTE)))
            rows = 22
        else:
            head = ('    <p class="eyebrow">After the storm</p>\n'
                    '    <h2 class="month-name">Damage log'
                    '<span class="cont">continued</span></h2>\n')
            note = ""
            rows = 25
        pages.append(page('{0}{1}{2}'.format(
            head, log_table(C.DAMAGE_COLUMNS, rows), note), foot="Damage log"))
    return pages


def claim_steps_page():
    steps = ""
    for index, text in enumerate(C.CLAIM_STEPS, start=1):
        steps += ('      <div class="seq-row">\n'
                  '        <p class="seq-num">{0}</p>\n'
                  '        <div class="seq-body">\n'
                  '          <p class="seq-text seq-text--lead">{1}</p>\n'
                  '        </div>\n'
                  '      </div>\n'.format(index, esc(text)))
    numbers = ["Wind or homeowners claim number", "Date reported",
               "Flood claim number", "Date reported",
               "Adjuster assigned", "Adjuster direct number"]
    cells = numbers + C.CLAIM_DEADLINES
    per = -(-len(cells) // 3)
    columns = "".join(
        '      <div>\n{0}      </div>\n'.format(
            "".join(fill_row(label) for label in cells[i:i + per]))
        for i in range(0, len(cells), per))

    return page(
        '    <p class="eyebrow">The part that decides the money</p>\n'
        '    <h2>Making the claim</h2>\n'
        '    <div class="seq seq--tight">\n{0}    </div>\n'
        '    <p class="sub-label">Numbers and dates, from your own policy</p>\n'
        '    <div class="rec-grid rec-grid--three">\n{1}    </div>\n'
        '    <p class="watch watch--block"><span>Watch out</span>{2}</p>\n'.format(
            steps, columns, esc(C.CLAIM_DEADLINE_NOTE)),
        foot="Making the claim")


def claim_log_pages():
    pages = []
    for part in (1, 2):
        if part == 1:
            head = ('    <p class="eyebrow">Every single call</p>\n'
                    '    <h2>Claim call log</h2>\n')
            note = ('    <p class="watch watch--block"><span>Watch out</span>{0}</p>\n'
                    .format(esc(C.CLAIM_NOTE)))
            rows = 24
        else:
            head = ('    <p class="eyebrow">Every single call</p>\n'
                    '    <h2 class="month-name">Claim call log'
                    '<span class="cont">continued</span></h2>\n')
            note = ""
            rows = 25
        pages.append(page('{0}{1}{2}'.format(
            head, log_table(C.CLAIM_COLUMNS, rows), note), foot="Call log"))
    return pages


def contractor_page():
    rows = ""
    for title, text in C.CONTRACTOR_CHECKS:
        rows += ('      <div class="chk-row">\n'
                 '        <span class="box" data-fill="check"></span>\n'
                 '        <div>\n'
                 '          <p class="chk-title">{0}</p>\n'
                 '          <p class="chk-text">{1}</p>\n'
                 '        </div>\n'
                 '      </div>\n'.format(esc(title), esc(text)))
    return page(
        '    <p class="eyebrow">Before you sign anything</p>\n'
        '    <h2>Vetting a contractor</h2>\n'
        '    <p class="lede">The roof is the easy part. Nine checks, all of which '
        'can be done in an afternoon, and every one of them is cheaper than the '
        'thing it prevents.</p>\n'
        '    <div class="chk">\n{0}    </div>\n'.format(rows),
        foot="Vetting")


def contractor_record_page():
    blocks = ""
    for n in (1, 2):
        rows = "".join(fill_row(label) for label in C.CONTRACTOR_FIELDS)
        blocks += ('      <div class="rec-block">\n'
                   '        <p class="rec-title">Contractor {0}</p>\n{1}'
                   '      </div>\n'.format(n, rows))
    signs = "".join('      <li>{0}</li>\n'.format(esc(item))
                    for item in C.FRAUD_SIGNS)
    return page(
        '    <p class="eyebrow">Facing the checks</p>\n'
        '    <h2>What the scams look like</h2>\n'
        '    <ul class="plain plain--tight">\n{0}    </ul>\n'
        '    <p class="sub-label">Who you are considering</p>\n'
        '    <div class="rec-grid">\n{1}    </div>\n'.format(signs, blocks),
        foot="Who you are considering")


def hindsight_page():
    items = "".join('      <li>{0}</li>\n'.format(esc(item))
                    for item in C.HINDSIGHT)
    return page(
        '    <p class="eyebrow">The back page</p>\n'
        '    <h2>What people say afterward</h2>\n'
        '    <p class="lede">Collected from the same conversation had over and '
        'over on this coast. Every one of them is something that had to be done '
        'before, and could not be done after.</p>\n'
        '    <p class="hind-lead">They wish they had:</p>\n'
        '    <ul class="plain">\n{0}    </ul>\n'
        '    <p class="pull">You are holding the binder in the spring, which is '
        'the only useful time to be holding it. Fill in four pages this week and '
        'the whole list above is already behind you.</p>\n'
        '    <p class="footnote">{1}</p>\n'.format(items, esc(C.DISCLAIMER)),
        foot="Afterward")


# --- design -----------------------------------------------------------------

# Appended to the kit's stylesheet rather than replacing it. Everything the two
# products share, the type scale, the tier colors, the footer, the watch-out
# block, comes from there. Only what the binder invents lives here.
BINDER_CSS = """
  /* --- binder cover ----------------------------------------------------- */
  .cover-feeds-note {
    margin: 30pt 0 0; padding-top: 11pt; border-top: 0.5pt solid var(--hair);
    font: 8.5pt/1.7 "Segoe UI", system-ui, sans-serif;
    color: var(--muted); max-width: 4.5in;
  }

  /* --- record blocks ---------------------------------------------------- */
  .rec-grid { display: flex; gap: 26pt; align-items: flex-start; }
  .rec-grid > div { flex: 1 1 0; min-width: 0; }
  .rec-grid--three { gap: 20pt; }
  .rec-block { margin-bottom: 16pt; }
  .rec-block:last-child { margin-bottom: 0; }
  .rec-title {
    font: 700 7pt/1.3 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .18em; text-transform: uppercase; color: var(--accent);
    margin: 0 0 8pt; padding-bottom: 4pt; border-bottom: 1pt solid var(--ink);
  }
  .rec-row { margin-bottom: 9pt; }
  .rec-label {
    font: 6.5pt/1.3 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .1em; text-transform: uppercase; color: var(--muted);
    margin: 0 0 1pt;
  }
  /* The rule is the field. It needs measurable height for build_fillable to
     find it, so it is a block with a bottom border rather than an <hr>. */
  .rec-line { height: 15pt; border-bottom: 0.5pt solid var(--hair); }
  .rec-line--short { max-width: 1.1in; }
  .rec-hint {
    font: italic 7.5pt/1.3 Georgia, serif; color: var(--muted); margin: 2pt 0 0;
  }
  .rec-aside {
    border-left: 1.5pt solid var(--sand); padding: 2pt 0 2pt 12pt;
  }
  .rec-aside-text { margin: 0; font-size: 9.5pt; line-height: 1.45; }

  /* --- log and inventory tables ----------------------------------------- */
  table.log-table { width: 100%; border-collapse: collapse; margin: 4pt 0 0; }
  table.log-table th {
    font: 700 6pt/1.3 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
    text-align: left; padding: 0 5pt 5pt 0; border-bottom: 1.25pt solid var(--ink);
  }
  /* 22pt is about a quarter inch of clear space above the rule, which is what
     an adult's handwriting actually needs. Anything tighter looks roomy on
     screen and is unusable with a pen. */
  table.log-table td {
    height: 22pt; padding: 0 5pt 0 0;
    border-bottom: 0.5pt solid var(--hair);
  }
  .inv-name { font: 400 30pt/1.05 Georgia, serif; margin: 0 0 3pt; }
  .inv-prompt {
    font: italic 9pt/1.45 Georgia, serif; color: var(--muted);
    margin: 0 0 12pt; max-width: 6.1in;
  }

  /* --- the calculator --------------------------------------------------- */
  .calc-head {
    display: flex; gap: 22pt; margin-bottom: 18pt;
    padding-bottom: 14pt; border-bottom: 1.5pt solid var(--ink);
  }
  .head-cell { flex: 0 0 auto; }
  table.calc-table { width: 100%; border-collapse: collapse; }
  table.calc-table th {
    font: 700 6pt/1.3 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
    text-align: left; padding: 0 6pt 5pt 0; border-bottom: 1.25pt solid var(--ink);
  }
  table.calc-table td {
    padding: 5pt 6pt 5pt 0; border-bottom: 0.5pt solid var(--hair);
    font-size: 8.5pt; line-height: 1.35; vertical-align: top;
  }
  .calc-item {
    font: 700 8.5pt/1.35 "Segoe UI", system-ui, sans-serif;
    color: var(--ink); width: 1.5in;
  }
  .calc-rule { color: var(--body); }
  .calc-math {
    font: italic 8pt/1.35 Georgia, serif; color: var(--accent); width: 1.15in;
  }
  table.calc-table .fill { width: 1.05in; border-bottom: 0.5pt solid var(--hair); }

  /* --- the countdown ---------------------------------------------------- */
  .tl-block { margin-bottom: 16pt; }
  .tl-block:last-child { margin-bottom: 0; }
  .tl-when {
    font: 700 12pt/1.1 "Segoe UI", system-ui, sans-serif; color: var(--must);
    margin: 0; padding-top: 7pt; border-top: 1.5pt solid var(--must);
  }
  .tl-sub {
    font: italic 9pt/1.4 Georgia, serif; color: var(--muted); margin: 2pt 0 4pt;
  }
  .tl-gap { height: 14pt; }

  /* Checklist rows inside a block are already inside a bordered group, so they
     lose the top padding that keeps a standalone list breathing. */
  .checklist--flush li { padding: 6pt 0; font-size: 9.5pt; line-height: 1.4; }
  .checklist--flush li:last-child { border-bottom: none; padding-bottom: 0; }
  .checklist--tight li { font-size: 10pt; }

  /* --- numbered sequences ----------------------------------------------- */
  .seq-row { display: flex; gap: 11pt; padding: 7pt 0; border-bottom: 0.5pt solid var(--hair); }
  .seq-row:last-child { border-bottom: none; }
  .seq-num {
    flex: none; width: 17pt; margin: 0;
    font: 700 13pt/1.1 Georgia, serif; color: var(--sand); text-align: right;
  }
  .seq-body { flex: 1 1 auto; min-width: 0; }
  .seq-title {
    font: 700 10pt/1.25 "Segoe UI", system-ui, sans-serif; color: var(--ink);
    margin: 0 0 2pt; display: flex; justify-content: space-between;
    align-items: flex-start; gap: 10pt;
  }
  .seq-text { margin: 0; font-size: 9pt; line-height: 1.42; }
  .seq-text--lead { font-size: 9.5pt; color: var(--ink); }
  .seq--tight .seq-row { padding: 5.5pt 0; }

  /* --- vetting checklist ------------------------------------------------ */
  .chk-row {
    display: flex; align-items: flex-start; gap: 11pt;
    padding: 8pt 0; border-bottom: 0.5pt solid var(--hair);
  }
  .chk-row:last-child { border-bottom: none; }
  .chk-title {
    font: 700 9.5pt/1.25 "Segoe UI", system-ui, sans-serif; color: var(--ink);
    margin: 0 0 2pt;
  }
  .chk-text { margin: 0; font-size: 9pt; line-height: 1.42; }

  /* The worked inventory line. Filled rather than ruled, because it is the one
     row on the page that is an answer instead of a blank. */
  table.example-table { margin: 0 0 8pt; }
  table.example-table td {
    height: auto; padding: 7pt 5pt 7pt 0;
    font: 700 9.5pt/1.3 "Segoe UI", system-ui, sans-serif; color: var(--accent);
  }
  .example-note {
    font-size: 9pt; line-height: 1.45; color: var(--muted); margin: 0;
  }

  .plain--tight li { padding: 3.5pt 0 3.5pt 14pt; font-size: 9pt; }
  .plain--tight li::before { top: 9.5pt; }
  .hind-lead {
    font: 700 8pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .16em; text-transform: uppercase; color: var(--sand);
    margin: 0 0 6pt;
  }
  .photo-set { margin-bottom: 13pt; }
"""


# --- assembly ---------------------------------------------------------------

def build_html():
    pages = [
        cover_page(),
        how_to_use_page(),
        before_season_page(),
        policy_page_one(),
        policy_page_two(),
        photograph_page(),
        photo_storage_page(),
        inventory_intro_page(),
    ]
    for name, prompt, rows in C.INVENTORY_ROOMS:
        pages.append(inventory_page(name, prompt, rows))
    pages += [supply_page(), supply_kit_page()]
    pages += timeline_pages()
    pages += [shutdown_page(), go_bag_page(), evacuation_page(), reentry_page()]
    pages += damage_log_pages()
    pages.append(claim_steps_page())
    pages += claim_log_pages()
    pages += [contractor_page(), contractor_record_page(), hindsight_page()]

    html = DOCUMENT.format(css=CSS + BINDER_CSS, body="\n".join(pages),
                           version=VERSION, disclaimer=C.DISCLAIMER)
    # The kit's title is baked into DOCUMENT. This is a different product.
    html = html.replace(
        "The Gulf Coast Home Maintenance Calendar, print edition v",
        "The Gulf Coast Storm Season Binder v")
    return html, len(pages)


# --- overflow check ---------------------------------------------------------

# The kit found out the hard way that a page can run past its sheet with no
# visible sign in the browser and a silent truncation in the PDF. The binder has
# far more dense tables than the kit, so this runs on every build rather than
# being a thing somebody remembers to check.
OVERFLOW_JS = """
<script>
window.addEventListener('load', function () {
  var out = [];
  document.querySelectorAll('.page').forEach(function (page, i) {
    var sheet = page.querySelector('.sheet');
    // .sheet is flex:1, so it always stretches to the full usable area and its
    // own scrollHeight can never report short. Measure how far the content
    // actually reaches instead, from the top of the sheet to the bottom of its
    // last child, which reads both over and under.
    var kids = sheet.children;
    var used = 0;
    if (kids.length) {
      used = Math.round(kids[kids.length - 1].getBoundingClientRect().bottom
                        - sheet.getBoundingClientRect().top);
    }
    out.push({page: i, used: used, avail: sheet.clientHeight,
              label: (page.querySelector('h1, h2') || {}).textContent || ''});
  });
  var sink = document.createElement('div');
  sink.id = 'overflow';
  sink.textContent = JSON.stringify(out);
  document.body.appendChild(sink);
});
</script>
"""


def check_overflow(chrome, html):
    tmp = os.path.join(OUT_DIR, "_overflow.html")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(html.replace("</body>", OVERFLOW_JS + "</body>"))
    result = subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--virtual-time-budget=8000", "--dump-dom",
        "file:///" + os.path.abspath(tmp).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=180)
    os.remove(tmp)

    match = re.search(r'<div id="overflow">(.*?)</div>',
                      result.stdout.decode("utf-8", "replace"), re.S)
    if not match:
        print("  could not measure page heights")
        return []
    raw = (match.group(1).replace("&quot;", '"').replace("&amp;", "&")
                         .replace("&lt;", "<").replace("&gt;", ">"))
    measured = json.loads(raw)
    bad = [p for p in measured if p["used"] > p["avail"] + 1]
    for p in bad:
        print("  OVERFLOW page {0} ({1}): {2}px of {3}px, over by {4}px".format(
            p["page"] + 1, p["label"].strip()[:40], p["used"], p["avail"],
            p["used"] - p["avail"]))
    if not bad:
        print("  all pages fit")

    # Underfill matters too on a product made of blanks. A ruled sheet that
    # stops two thirds of the way down is writing space the buyer paid for and
    # did not get, and nothing about it looks deliberate.
    if "--fill-report" in sys.argv:
        for p in sorted(measured, key=lambda p: p["used"] / float(p["avail"])):
            share = p["used"] / float(p["avail"])
            if share < 0.85:
                print("  underfilled page {0} ({1}): {2}% used, {3}px spare"
                      .format(p["page"] + 1, p["label"].strip()[:38],
                              int(share * 100), p["avail"] - p["used"]))
    return bad


def main():
    fillable = "--fillable" in sys.argv

    os.makedirs(OUT_DIR, exist_ok=True)
    html_path = os.path.join(OUT_DIR, BASENAME + ".html")
    html, count = build_html()
    with open(html_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)
    print("{0}  {1} pages".format(html_path, count))

    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found. Open the HTML and print to PDF by hand.")
        return 1

    check_overflow(chrome, html)

    pdf_path = os.path.abspath(os.path.join(OUT_DIR, BASENAME + ".pdf"))
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--print-to-pdf-no-header",
        "--print-to-pdf=" + pdf_path,
        "file:///" + os.path.abspath(html_path).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=300)
    print("{0}  {1:,} bytes".format(pdf_path, os.path.getsize(pdf_path)))

    if fillable:
        from build_fillable import stamp
        out_pdf = os.path.join(OUT_DIR, BASENAME + "-fillable.pdf")
        stamp(chrome, html, pdf_path, out_pdf)
        print("{0}  {1:,} bytes".format(out_pdf, os.path.getsize(out_pdf)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
