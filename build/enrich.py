# Adds: who the ad appears as, who paid, funding disclosure, audience, lawsuit links,
# fact-check ratings; builds ads_all.csv (one row per ad record) and word_freq.csv.
# Run after build_data.py:  python3 -I build/enrich.py dc_ads_app/data
import csv, json, os, re, sys, collections

D = sys.argv[1]
B = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: list(csv.DictReader(open(os.path.join(D, f), encoding="utf-8")))
def wcsv(name, rows, cols=None):
    cols = cols or list(rows[0].keys())
    with open(os.path.join(D, name), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

camp, vids, meta, laws = rd("campaigns.csv"), rd("youtube_ads.csv"), rd("meta_ads.csv"), rd("lawsuits.csv")
aud = {r["library_id"]: r for r in csv.DictReader(open(os.path.join(B, "meta_audience.csv"), encoding="utf-8"))}

# ---------------------------------------------------------------- sources for fact checks
SRC = dict(
  JLARC="https://jlarc.virginia.gov/landing-2024-data-centers-in-virginia.asp",
  HARC="https://www.hppr.org/hppr-news/2025-09-29/data-centers-are-thirsty-for-texas-water-but-state-planners-dont-know-how-much-they-will-need",
  PEAK="https://arxiv.org/html/2603.02705",
  INDIRECT="https://cardinalnews.org/2026/08/24/data-centers-are-drinking-more-water-but-overall-water-use-in-virginia-has-gone-down-anyway-here-are-the-numbers/",
  MI="https://michiganadvance.com/2025/11/19/advocates-warn-michigan-strategic-fund-guidelines-for-data-center-tax-breaks-not-in-line-with-law/",
  JUP="https://www.abqjournal.com/business/project-jupiter-developers-revise-plan-swapping-gas-turbines-for-fuel-cell-system/3031145",
  WPR="https://www.wpr.org/news/microsoft-data-centers-8-million-gallons-water-each-year",
  ADANI="https://www.adanienterprises.com/digital-reports/enterprises/2026/data-center.html",
  OR="https://opb.org/article/2026/07/07/oregon-data-center-general-electric-rate-hikes",
  AZ="https://www.circleofblue.org/2025/supply/data-centers-a-small-but-growing-factor-in-arizonas-water-budget/",
)
L = {l["id"]: l for l in laws}
SRC["L01"], SRC["L02"], SRC["L05"], SRC["L09"] = L["L-01"]["url"], L["L-02"]["url"], L["L-05"]["url"], L["L-09"]["url"]

# rating, note, source key
FC = {
 "water96": ("Missing context", "Counts hours, not gallons: water use peaks on the hottest days (peak demand can run 6–10 times the average). No facility data is published, and the ads were later reworded to 'Some… for cooling'. Virginia Connects is a co-defendant in L-01, which challenges AWS's similar '97% of the year' claim.", "PEAK"),
 "aws97": ("Disputed", "A former AWS water manager alleges in court (L-01) that these figures were misleading; a leaked memo (L-03) shows indirect water was left out.", "L01"),
 "waterpct": ("No public data", "No published, facility-level data shows the share of hours with no water use for cooling. The figure counts time, not gallons, and leaves out water used at power plants.", "PEAK"),
 "watt": ("Missing context", "Data centers do pay for the electricity they use. JLARC (2024) found Virginia data centers currently pay their full cost of service, but warned that new generation and transmission built for them could raise costs for other customers. The homes-powered figures have no published source.", "JLARC"),
 "costs": ("Missing context", "JLARC (2024) found data centers currently pay their full cost of service in Virginia, but that future grid build-out risks shifting costs to residential customers.", "JLARC"),
 "paycost": ("Missing context", "Data centers pay for the power they use. Whether grid upgrades built for them shift costs to other customers depends on each state's tariffs; Virginia's JLARC (2024) found that risk there.", "JLARC"),
 "orcosts": ("Missing context", "The ad cites an unnamed 'independent study'. Oregon's 2025 POWER Act created a separate rate class for big data centers; in July 2026 regulators approved a 29.7% rate rise for PGE's data-center class and a 1.3% cut for homes.", "OR"),
 "txbuilt": ("Missing context", "'Minimal water' is undefined. HARC estimates Texas data centers used about 0.4% of state water in 2025, rising to as much as 2.7% by 2030. The ad gives no source for funding power 'for everyone'.", "HARC"),
 "compasswater": ("No public data", "'Zero city water for cooling' leaves out other water sources and the water used to generate the electricity it buys. Compass doesn't publish annual water-use figures for its sites.", "PEAK"),
 "compassrates": ("No public data", "The '$300 million' for substations and transmission is self-reported, with no breakdown by site or utility filing in the ad.", ""),
 "adani59": ("Missing context", "Adani's own 2026 report gives 59% renewable energy for Chennai 1; 'up to 100%' is a general offering.", "ADANI"),
 "txwater": ("Supported", "HARC estimates Texas data centers used about 0.4% of state water in 2025, rising to as much as 2.7% by 2030.", "HARC"),
 "azwater": ("Supported", "Published estimates put Arizona data centers' direct water use well under 1% of state use (one estimate is below 0.1%). These figures leave out water used to generate their electricity.", "AZ"),
 "renew100": ("Missing context", "'100% renewable' claims rely partly on unbundled renewable energy certificates (RECs). 16 state attorneys general sent inquiry letters in Sept 2025; no findings have been reported.", "L02"),
 "zerocool": ("Missing context", "'Zero water for cooling' covers on-site cooling only. Closed loops still need an initial fill and top-ups, and the water used to generate the electricity can exceed direct use.", "PEAK"),
 "selfpower": ("Missing context", "Generalizes from a few sites: HPPR reports only some Texas projects building on-site power. The ad gives no source for 'lower electricity costs'.", "HARC"),
 "mi90": ("Missing context", "The 90% clean-energy condition is in Michigan law. But state guidelines let data centers qualify just by contracting with a utility, which advocates say makes the requirement meaningless.", "MI"),
 "jupiter": ("Missing context", "The 'cleaner energy' plan is a fuel-cell microgrid that runs on natural gas. It needs a one-time fill of about 960,000 gallons of water.", "JUP"),
 "pledge": ("Not checkable", "A promise about the future or a pledge. There is nothing to check yet.", ""),
 "vague": ("Not checkable", "Too vague to test (no figure, place or time period).", ""),
 "notyet": ("Not yet checked", "This is a specific claim that could be checked against public filings, but we haven't checked it yet.", ""),
 "nodata": ("No public data", "This could be checked, but the company or group hasn't published the underlying data.", ""),
 "fairwater": ("Missing context", "Records released after a public-records suit (L-05) project ~2.8M gal/yr for Phase 1 and up to 8.4M gal/yr later. Actual use isn't published.", "WPR"),
 "counter": ("Counter-ad (not rated)", "Parody or advocacy against data center water use.", ""),
 "none": ("No energy/water claim", "", ""),
}

# ---------------------------------------------------------------- campaign-level fields
AC_PAID = "America Connects (Data Center Coalition's state-campaign nonprofit); Google lists the payer as GMMB, Inc."
AC_DISC = "Partly: the ad shows only the state group's name; the industry funder appears only in ad libraries"
VA_WHO = "Meta: 96–99% of impressions in Virginia. Some ads skewed young (72–86% aged 18–34); others were spread across ages 25–64."
TX_WHO = "Meta: Texas only; under-35s not targeted; about 65% of impressions to men."
C = {  # id: (appears_as, paid_for_by, funding_disclosed, audience_who, factcheck_key, lawsuit_role)
 "US-01": ("Virginia Connects", AC_PAID, AC_DISC, "Virginia TV viewers", "costs", "Sponsor named in suit"),
 "US-02": ("Virginia Connects", AC_PAID, AC_DISC, "Virginia; YouTube and Google video ads", "water96", "Sponsor named in suit"),
 "US-03": ("Virginia Connects", AC_PAID, AC_DISC, "Fredericksburg newspaper readers and drivers", "water96", "Sponsor named in suit"),
 "US-04": ("Virginia Connects", AC_PAID, AC_DISC, "Northern Virginia TV and YouTube", "water96", "Sponsor named in suit"),
 "US-05": ("Texas Connects", AC_PAID, AC_DISC, TX_WHO, "txwater", ""),
 "US-06": ("North Carolina Connects", AC_PAID, AC_DISC, "NC TV (Fox News, Spectrum News Raleigh), radio and billboards", "watt", ""),
 "US-07": ("Oregon Connects", AC_PAID, AC_DISC, "Portland TV and digital", "waterpct", ""),
 "US-08": ("PA / OH / IN / GA Connects", AC_PAID, AC_DISC, "State-targeted YouTube, TV and web", "waterpct", ""),
 "US-09": ("Meta", "Meta Platforms", "Yes: company brand", "TV viewers in state capitals (Sacramento, Salt Lake City, Tallahassee, DC)", "renew100", "Company under inquiry"),
 "US-10": ("Meta", "Meta Platforms", "Yes: company brand", "Los Lunas, NM community", "renew100", "Company under inquiry"),
 "US-11": ("Amazon / AWS", "Amazon", "Yes: company brand", "Virginia", "aws97", "Claim challenged in suit"),
 "US-12": ("Amazon / AWS", "Amazon", "Yes: company brand", "Northern Virginia public and officials", "aws97", "Claim challenged in suit"),
 "US-13": ("Microsoft", "Microsoft", "Yes: company brand", "Lowell and Gaines Township residents (open house)", "pledge", ""),
 "US-14": ("Google", "Google", "Yes: company brand", "National", "pledge", "Related records fight"),
 "US-15": ("Build American AI", "Build American AI (nonprofit tied to the Leading the Future super PAC)", "Partly: donors not disclosed", "Ohio and Kansas TV and YouTube", "pledge", ""),
 "US-16": ("Starwood Digital Ventures", "Starwood Digital Ventures", "Yes: company brand", "Delaware Facebook users", "pledge", ""),
 "US-17": ("Sherrod Brown for Senate", "Sherrod Brown campaign", "Yes: campaign disclaimer", "Ohio TV viewers", "pledge", ""),
 "US-18": ("Virginia Connects", AC_PAID, AC_DISC, "Virginia broadcast TV (World Cup, GMA, The View, Jeopardy!)", "water96", "Sponsor named in suit"),
 "US-19": ("Louisiana Connects", AC_PAID, AC_DISC, "Louisiana YouTube and Google video", "waterpct", ""),
 "US-20": ("Virginia Connects", "Virginia Connects (Meta disclaimer)", AC_DISC, VA_WHO, "costs", "Sponsor named in suit"),
 "US-21": ("QTS Data Centers", "QTS Data Centers (owned by Blackstone)", "Yes: company brand. Meta ads aren't labeled as issue ads, so spend and audience aren't published", "National; Meta publishes no audience data", "zerocool", ""),
 "US-22": ("Texans for Economic Liberty", "Texans for Economic Liberty (Meta disclaimer; contact at Harris Media LLC)", "Partly: group named, funders not disclosed", "Meta: 99% in Texas; 93% of impressions to people 55+, 80% to 65+", "selfpower", ""),
 "US-23": ("Michigan for Responsible Data Centers", "Michigan for Responsible Data Centers (Meta disclaimer)", "No: funders not disclosed; launched with help from the Michigan Chamber of Commerce (Mar 2026)", "Meta: Michigan only; mixed ages (one ad 53% aged 55+)", "mi90", ""),
 "US-24": ("Fight Back Fund", "Fight Back Fund", "Partly: union-affiliated; funders not listed", "Illinois", "vague", ""),
 "US-25": ("Project Jupiter", "Oracle ($3.44M paid to Brabender Cox, disclosed as lobbying)", "Yes, after Ethics Commission disclosure", "Doña Ana County and New Mexico; English and Spanish", "jupiter", "Disclosure finding"),
 "US-26": ("Project 48 Arizona", "Project 48 Arizona", "Partly: funders not disclosed", "Phoenix-area drivers", "azwater", ""),
 "US-27": ("Meta", "Meta Platforms", "Yes: company brand", "Northwest and Central Ohio", "none", ""),
 "US-28": ("Microsoft", "Microsoft", "Yes: company brand", "Press / public", "fairwater", "Related records fight"),
 "US-29": ("xAI / Greater Memphis Chamber", "xAI", "Yes", "Memphis public and officials", "pledge", ""),
 "US-30": ("Liquid Death + Garage Beer", "Liquid Death, Garage Beer", "Yes: brand", "National", "counter", ""),
 "US-31": ("Planet Water Foundation", "Planet Water Foundation / TBWA\\SMP", "Yes: brand", "National", "counter", ""),
 "US-32": ("Texas Connects", AC_PAID.replace("Google lists the payer as GMMB, Inc.", "Google verified advertiser 'Texas Connects'"), AC_DISC, "Texas YouTube viewers (12.2M views); Google publishes no age or gender data", "txbuilt", ""),
 "US-33": ("Oregon Connects", AC_PAID.replace("Google lists the payer as GMMB, Inc.", "Google verified advertiser 'Oregon Connects'"), AC_DISC, "Oregon YouTube viewers (6M+ views); Google publishes no age or gender data", "orcosts", ""),
 "US-34": ("Compass Datacenters", "Compass Datacenters (Meta ads not labeled as issue ads; verified Google advertiser)", "Yes: company brand. Meta publishes no spend or audience", "National; Meta publishes no audience data", "compasswater", ""),
 "US-35": ("Google", "Google LLC (verified Google advertiser)", "Yes: company brand", "Communities near Google data centers (GA, IN, MO, OH, TX, VA)", "none", ""),
 "US-36": ("Wyoming Driven Innovation", "Wyoming Driven Innovation LLC (Meta disclaimer)", "Partly: LLC named, funders not disclosed", "Wyoming", "vague", ""),
 "US-37": ("Election ads against data centers", "Candidates, PACs and advocacy groups (Meta disclaimers)", "Yes: campaign disclaimers", "Voters in 2026 races (OR, OH, MI, TX, GA, AK and others)", "counter", ""),
 "GL-01": ("Polaroid", "Polaroid", "Yes: brand", "Coney Island, London Underground, South Korea", "counter", ""),
 "GL-02": ("Avaada Group", "Avaada Group", "Yes: brand", "Indian national TV", "vague", ""),
 "GL-03": ("Microsoft", "Microsoft", "Yes: brand", "Hyderabad launch audience", "zerocool", ""),
 "GL-04": ("Amazon", "Amazon", "Yes: brand", "India (web)", "nodata", "Related leak (L-03)"),
 "GL-05": ("AdaniConneX", "AdaniConneX", "Yes: brand", "Corporate / investors", "adani59", ""),
 "GL-06": ("CtrlS Datacenters", "CtrlS", "Yes: brand", "Press", "pledge", ""),
 "GL-07": ("STT GDC India", "STT GDC", "Yes: brand", "Corporate site", "nodata", ""),
 "GL-08": ("Sify Technologies", "Sify", "Yes: brand", "Corporate site", "nodata", ""),
 "GL-09": ("Colt DCS + RMZ", "Colt DCS, RMZ", "Yes: brand", "Press / corporate site", "nodata", ""),
 "GL-10": ("Techno Digital", "Techno Digital", "Yes: brand", "Press", "pledge", ""),
 "GL-11": ("Nxtra by Airtel", "Nxtra", "Yes: brand", "Corporate", "pledge", ""),
 "GL-12": ("Google + AdaniConneX + Airtel", "Google, AdaniConneX, Airtel", "Yes: brand", "Launch event / press", "pledge", ""),
}
lawmap = collections.defaultdict(list)
for l in laws:
    for x in re.split(r"[,\s]+", l.get("links_to") or ""):
        if x: lawmap[x].append(l["id"])
lawmap["US-11"].append("L-01")
VA_IDS = ["US-01", "US-02", "US-03", "US-04", "US-18", "US-20"]
for x in VA_IDS:
    if "L-01" not in lawmap[x]: lawmap[x].append("L-01")

for r in camp:
    a = C[r["id"]]
    k = a[4]; fc = FC[k]
    r.update(appears_as=a[0], paid_for_by=a[1], funding_disclosed=a[2], audience_where=r["place"], audience_who=a[3],
             lawsuit_ids=", ".join(sorted(set(lawmap.get(r["id"], [])))), lawsuit_role=a[5] if lawmap.get(r["id"]) else "",
             factcheck=fc[0], factcheck_note=fc[1], factcheck_url=SRC.get(fc[2], ""))
# keep lawsuits' links_to in sync
for l in laws:
    l["links_to"] = ", ".join(sorted(c for c, ids in lawmap.items() if l["id"] in ids))

# ---------------------------------------------------------------- videos
STATE_GROUP = {"Oregon Connects": "Oregon Connects", "Connected OH": "Connected Ohio", "ConnectedGA": "Connected Georgia", "IN Connects": "Indiana Connects",
               "NC Connects": "North Carolina Connects", "OR Connects": "Oregon Connects"}
VID_FC = {"IwQCwpzG_GY": "txbuilt", "L-g5j8Dah_o": "orcosts", "F-lA8tM5ytg": "orcosts", "0JS96iU0k0o": "compasswater",
          "XNaTFb_tYXM": "compasswater", "Cwh4o5H-rtU": "compassrates", "IQqPY39Vpes": "none", "Li0ap16ReOQ": "none"}
def vid_fc(v):
    if v["youtube_id"] in VID_FC: return VID_FC[v["youtube_id"]]
    ch, t, ti = v["channel"], v["topic"], v["title"]
    if "Connect" in ch:
        if t == "Water": return "water96" if v["state"] == "Virginia" else ("txwater" if v["state"] == "Texas" else "waterpct")
        if t in ("Energy", "Facts (energy + tax)"): return "watt"
        if t == "Affordability": return "vague"
        return "none"
    if ch == "Build American AI": return "pledge" if "Pledge" in ti else ("notyet" if t == "Energy" else "none")
    if ch == "QTS Data Centers": return "zerocool" if t == "Water" else "none"
    if ch == "Texans for Economic Liberty": return "selfpower" if t == "Water" else "none"
    return "none"
for v in vids:
    ch = v["channel"]
    if "Connect" in ch:
        v["appears_as"] = STATE_GROUP.get(ch, ch); v["funding_disclosed"] = AC_DISC
        adv = v.get("advertiser") or ""
        v["paid_for_by"] = AC_PAID if ("America Connects" in adv or not adv) else \
            "America Connects network; Google verified advertiser: " + adv.split(" (")[0]
        v["audience_where"] = v["state"]
    elif ch == "Build American AI":
        v["appears_as"] = ch; v["paid_for_by"] = C["US-15"][1]; v["funding_disclosed"] = C["US-15"][2]; v["audience_where"] = v["state"]
    elif ch == "QTS Data Centers":
        v["appears_as"] = ch; v["paid_for_by"] = C["US-21"][1]; v["funding_disclosed"] = "Yes: company brand"; v["audience_where"] = "US"
    elif ch == "Compass Datacenters":
        v["appears_as"] = ch; v["paid_for_by"] = C["US-34"][1]; v["funding_disclosed"] = "Yes: company brand"; v["audience_where"] = v["state"]
    elif ch in ("Google", "Grow with Google"):
        v["appears_as"] = "Google"; v["paid_for_by"] = "Google LLC (verified Google advertiser)"; v["funding_disclosed"] = "Yes: company brand"; v["audience_where"] = v["state"]
    elif ch == "Texans for Economic Liberty":
        v["appears_as"] = ch; v["paid_for_by"] = "Texans for Economic Liberty"; v["funding_disclosed"] = C["US-22"][2]; v["audience_where"] = "Texas"
    else:
        v["appears_as"] = ch; v["paid_for_by"] = v.get("advertiser") or ch; v["funding_disclosed"] = ""; v["audience_where"] = v["state"]
    v["audience_who"] = "Google publishes no age or gender data for these ads"
    k = vid_fc(v); fc = FC[k]
    v["factcheck"], v["factcheck_note"], v["factcheck_url"] = fc[0], fc[1], SRC.get(fc[2], "")
    v["lawsuit_ids"] = "L-01" if v["appears_as"] == "Virginia Connects" else ""
    v["lawsuit_role"] = "Sponsor named in suit" if v["lawsuit_ids"] else ""

# ---------------------------------------------------------------- Meta ads
M_FC = {"1603022260291240": "vague", "1355279849204870": "vague", "1108111641257542": "costs", "1148486016949172": "costs",
        "2102349793504832": "costs", "1813952416150473": "costs", "908224605261545": "vague", "874918655658106": "txwater",
        "1300660238797502": "txwater", "4368691783381214": "vague", "946918801539771": "vague", "2068150173768978": "vague",
        "1399130278973163": "zerocool", "2223518221527867": "zerocool", "1115108704501247": "paycost", "2096764071716470": "selfpower",
        "1595817172204916": "mi90", "982172037575661": "mi90", "1615312140006989": "notyet", "1666489028820952": "mi90",
        "1086975924010981": "vague", "4395830997313964": "vague", "1077055241572370": "waterpct", "1913744136701738": "waterpct",
        "4680740768826912": "waterpct", "1064803106540533": "waterpct", "970055792802575": "waterpct",
        "1592085222563156": "counter", "3153289668213763": "counter", "953059753993074": "counter"}
M_FC.update({"1007646302344543": "compasswater", "1442097564548229": "compassrates", "1927445971757558": "none", "1821241565897458": "vague"})
UNLABELED = {"1007646302344543", "1442097564548229", "1927445971757558", "1077055241572370", "1913744136701738", "4680740768826912", "1064803106540533", "970055792802575"}
for m in meta:
    i = m["library_id"]; s = m["sponsor"]; a = aud.get(i)
    m["appears_as"] = re.sub(r"\s*\(.*?\)", "", s)
    if a:
        m["paid_for_by"] = a["paid_for_by"] + " (Meta 'Paid for by' disclaimer)"
        m["audience_where"] = a["locations"]; m["audience_who"] = a["audience_summary"]
        m["reach"] = f"{a['spend']} spent; {a['impressions']} impressions"
        for f in ("age_18_34", "age_35_54", "age_55_plus", "women", "men"): m[f] = a[f]
    else:
        if i in UNLABELED:
            m["paid_for_by"] = ("Compass Datacenters: " if "Compass" in s else "") + "Not shown: ad ran as 'Sponsored' without an issue-ad label, so Meta publishes no payer, spend or audience"
        elif "Wyoming" in s:
            m["paid_for_by"] = "Wyoming Driven Innovation LLC (Meta disclaimer)"
        elif "counter" in s and m["library_id"] not in M_FC:
            m["paid_for_by"] = m["appears_as"] + " (Meta disclaimer)"
        elif "QTS" in s:
            m["paid_for_by"] = "QTS Data Centers (commercial ad; no issue-ad label)"
        elif "counter" in s:
            m["paid_for_by"] = m["appears_as"] + " (commercial ad)"
        else:
            m["paid_for_by"] = m["appears_as"] + " (from earlier ad-library read)"
        m["audience_where"] = m["state"]; m["audience_who"] = "Not published by Meta for this ad"
        m["reach"] = m.get("spend", "")
    if "Connect" in s: m["funding_disclosed"] = AC_DISC
    elif "Michigan" in s: m["funding_disclosed"] = C["US-23"][2]
    elif "Texans" in s: m["funding_disclosed"] = C["US-22"][2]
    else: m["funding_disclosed"] = ""
    fc = FC[M_FC.get(i, "counter" if "counter" in m["sponsor"] else "vague")]
    m["factcheck"], m["factcheck_note"], m["factcheck_url"] = fc[0], fc[1], SRC.get(fc[2], "")
    m["lawsuit_ids"] = "L-01" if m["appears_as"] == "Virginia Connects" else ""
    m["lawsuit_role"] = "Sponsor named in suit" if m["lawsuit_ids"] else ""

# ---------------------------------------------------------------- unified table
TYPE = {r["appears_as"]: r["sponsor_type"] for r in camp}
def stype(g):
    if "Connect" in g: return "Industry trade group"
    return TYPE.get(g, "")
allrows = []
for r in camp:
    allrows.append(dict(uid=r["id"], kind="Campaign entry", appears_as=r["appears_as"], paid_for_by=r["paid_for_by"],
        funding_disclosed=r["funding_disclosed"], sponsor_type=r["sponsor_type"], platform=r["format"], date=r["date"],
        claim_type=r["claim_type"], claim=r["claim"], factcheck=r["factcheck"], factcheck_note=r["factcheck_note"],
        factcheck_url=r["factcheck_url"], lawsuit_ids=r["lawsuit_ids"], lawsuit_role=r["lawsuit_role"],
        audience_where=r["audience_where"], audience_who=r["audience_who"], reach="", url=r["url_primary"] or r["url_source"]))
for v in vids:
    allrows.append(dict(uid=v["youtube_id"], kind="YouTube ad", appears_as=v["appears_as"], paid_for_by=v["paid_for_by"],
        funding_disclosed=v["funding_disclosed"], sponsor_type=stype(v["appears_as"]) or "Advocacy group", platform="YouTube / Google video ads",
        date=v["published"], claim_type=v["topic"], claim=v["key_claim"] or v["title"], factcheck=v["factcheck"],
        factcheck_note=v["factcheck_note"], factcheck_url=v["factcheck_url"], lawsuit_ids=v["lawsuit_ids"], lawsuit_role=v["lawsuit_role"],
        audience_where=v["audience_where"], audience_who=v["audience_who"],
        reach=f"{int(v['views']):,} views" + (f"; {v['google_ads_creatives']} Google ad creatives" if v.get("google_ads_creatives") else ""),
        url=v["youtube_url"]))
for m in meta:
    allrows.append(dict(uid=m["library_id"], kind="Meta ad", appears_as=m["appears_as"], paid_for_by=m["paid_for_by"],
        funding_disclosed=m["funding_disclosed"], sponsor_type=stype(m["appears_as"]) or ("Consumer brand (counter-ad)" if "counter" in m["sponsor"] else ""),
        platform="Facebook / Instagram", date=m["dates"], claim_type=m["claim_type"], claim=m["text"], factcheck=m["factcheck"],
        factcheck_note=m["factcheck_note"], factcheck_url=m["factcheck_url"], lawsuit_ids=m["lawsuit_ids"], lawsuit_role=m["lawsuit_role"],
        audience_where=m["audience_where"], audience_who=m["audience_who"], reach=m["reach"], url=m["url"],
        age_18_34=m.get("age_18_34", ""), age_55_plus=m.get("age_55_plus", ""), women=m.get("women", "")))
for r in allrows:
    r["in_lawsuit"] = "Yes" if r["lawsuit_ids"] else "No"
    r["checkable"] = "Yes" if r["factcheck"] in ("Supported", "Missing context", "Disputed", "No public data", "Not yet checked") else "No"

# ---------------------------------------------------------------- word frequencies
STOP = set("""a about above after again all also am an and any are as at be because been before being below between both but by can
could did do does doing down during each few for from further had has have having he her here hers him his how i if in into is it its
itself just let me more most my no nor not now of off on once only or other our ours out over own same she should so some such than
that thats the their theirs them then there these they this those through to too under until up very was we were what when where which
while who whom why will with would you your yours re ve ll s t don dont doesn isn aren didn won d m o y us one even many every get
make makes made like way go going keep see well new also it's that's we're they're you're data center centers datacenter datacenters
said says per may might much us let's here's what's ad ads learn more click link watch don't rev doesn't isn't""".split())
tx = {}
p = os.path.join(B, "tx.jsonl")
if os.path.exists(p):
    for line in open(p, encoding="utf-8"):
        try: o = json.loads(line); tx[o["id"]] = o["tx"]
        except Exception: pass
def words(text):
    for w in re.findall(r"[a-z][a-z'\-]+", (text or "").lower().replace("’", "'")):
        w = w.strip("'-")
        if len(w) > 2 and w not in STOP and not w.endswith("'s"): yield w
freq = []
REPRESENTED = set(["US-02", "US-04", "US-05", "US-06", "US-07", "US-08", "US-15", "US-19", "US-20", "US-21", "US-22", "US-23", "US-24"])
units = []
vkey = {v["youtube_id"]: v["key_claim"] for v in vids}
for r in allrows:
    if r["kind"] == "Campaign entry" and r["uid"] in REPRESENTED: continue
    text = tx.get(r["uid"]) if r["kind"] == "YouTube ad" else None
    if r["kind"] == "YouTube ad" and not text and not vkey.get(r["uid"]): continue  # title-only cut-downs
    if not text: text = r["claim"]
    units.append((r, text))
for r, text in units:
    c = collections.Counter(words(text))
    for w, n in c.items():
        freq.append(dict(uid=r["uid"], kind=r["kind"], appears_as=r["appears_as"], claim_type=r["claim_type"],
                         factcheck=r["factcheck"], in_lawsuit=r["in_lawsuit"], word=w, n=n))

wcsv("campaigns.csv", camp); wcsv("youtube_ads.csv", vids); wcsv("meta_ads.csv", meta); wcsv("lawsuits.csv", laws)
wcsv("ads_all.csv", allrows, ["uid", "kind", "appears_as", "paid_for_by", "funding_disclosed", "sponsor_type", "platform", "date",
     "claim_type", "claim", "factcheck", "factcheck_note", "factcheck_url", "checkable", "in_lawsuit", "lawsuit_ids", "lawsuit_role",
     "audience_where", "audience_who", "reach", "age_18_34", "age_55_plus", "women", "url"])
wcsv("word_freq.csv", freq)
wcsv("meta_audience.csv", list(aud.values()))
print("ads_all", len(allrows), "| word rows", len(freq), "| units", len(units))
print(collections.Counter(r["factcheck"] for r in allrows))
print(collections.Counter(r["in_lawsuit"] for r in allrows))
