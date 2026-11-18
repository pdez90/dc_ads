# v1.3 final pull: enrichment for the records added in final_pull.py. Run from enrich.py with HOOK = "A", "B" or "C".
if HOOK == "A":
    SRC.update(
        METAEP="https://about.fb.com/news/2025/10/metas-new-ai-optimized-data-center-el-paso/",
        IMRATE="https://www.wvpe.org/wvpe-news/2026-08-26/i-m-announces-electric-rate-cut-plan-enabled-by-data-centers",
        IN1007="https://indianacapitalchronicle.com/2025/03/28/utility-customer-advocates-say-protections-inadequate-in-large-load-users-nuclear-development-bill/",
        STLPR="https://stlpr.org/government-politics-issues/2026-11-02/madison-county-data-center-development",
    )
    FC.update({
     "metawater": ("Not checkable", "A pledge for a data center that is not yet running. Meta announced it in October 2025. 'Restoring' water means paying for projects elsewhere in the watershed; it does not mean the site uses less. Local reports put the site's permitted maximum between 750,000 and 2.5 million gallons a day.", "METAEP"),
     "imrate": ("Missing context", "Indiana Michigan Power did propose a rate cut in August 2026 and credited revenue from large customers including data centers. Regulators have not approved it; a ruling is expected by mid-2027. The same utility has asked to speed up new power-plant construction to serve that demand.", "IMRATE"),
     "in1007": ("Missing context", "Indiana's HEA 1007 (2025) requires large new customers to reimburse at least 80% of the cost of projects built for them, not all of it. Consumer advocates told lawmakers the protections were inadequate and left ways around the 80% share.", "IN1007"),
     "granite": ("No public data", "We could not find the cited Granite City code text online to confirm what it requires. St. Louis Public Radio reports the city's data center proposal was tabled and that township advisory votes in the area went against data center development.", "STLPR"),
     "projection": ("Not checkable", "A projection for a project that has not been built. The amount depends on final tax agreements and abatements.", ""),
     "jobsconstr": ("Not checkable", "The company's own count of construction workers; no public record to check it against. Construction jobs end when building does. Good Jobs First finds an operating data center needs 30 to 50 permanent workers on average.", "JOBS"),
     "orbit": ("Not checkable", "Describes a technology that is not operating at commercial scale. There is nothing to check yet.", ""),
    })
    C.update({
     "US-49": ("Meta", "Meta Platforms (one ad carries a 'Facebook Inc.' disclaimer; the rest ran without an issue-ad label)", "Yes: company brand", "Residents near Meta's data center sites", "metawater", "Company under inquiry"),
     "US-50": ("Ohio 'Vote NO on the ban' groups", "CASE for Consumers; NetChoice PAC; Building Our Future Ohio (Meta disclaimers)", "Partly: group names only", "Voters in Pataskala, Sunbury and Oregon, Ohio", "projection", ""),
     "GL-17": ("Space, subsea and floating data centers", "World Economic Forum; Virtus Solis; Change.org; Future Tech Insights Inc; Alaskans for Mary", "Mixed", "US and international", "orbit", ""),
    })

if HOOK == "B":
    M_FC.update({
     "1937295901048443": "watt", "29363106506620329": "waterpct", "1427060622647550": "watt", "1361320452652801": "watt", "1091053473672069": "watt",
     "1644287020617322": "watt", "2278009809631619": "watt", "1152975787297827": "paycost", "2192046634687863": "vague", "2189981561908235": "jobsvague",
     "2205240850050436": "metawater", "1436667177798336": "paycost", "2107409233471965": "pledge", "2587876388330240": "none",
     "1099444266054670": "chinadata", "1152197807376924": "chinadata", "1135995179081485": "chinadata", "1439856308275610": "chinadata", "1139512795232176": "chinadata",
     "2165780317708768": "vague", "2297263294527874": "jobsvague", "1111718257925494": "jobsvague", "2335756646962155": "jobsvague", "1440111811604925": "jobsvague",
     "1446092404279510": "jobsvague", "1791545561895294": "jobsvague", "2857363984636952": "jobsvague", "4423960154487729": "jobsvague", "28803374022604118": "jobsvague",
     "2275952023247967": "vague", "1392687498985291": "vague", "1385410257116629": "selfpower", "1590788092507693": "selfpower",
     "945807044879403": "jobsvague", "29170911075868498": "granite", "1736774410723971": "ibewtax", "1662611835379333": "paycost", "4674635626102080": "imrate",
     "1082409191331414": "vague", "1063635146576957": "none", "1757093043083412": "vague", "1070161062661609": "in1007", "1039532835799443": "eeispread",
     "1276251964713428": "zerocool", "1131079932632500": "jobsvague", "2725572121213934": "none", "1010892208696475": "jobsconstr", "961700786604260": "none",
     "1651691906330806": "jobsvague", "1571093961719236": "projection", "1034718296292498": "jobsvague", "1743934946712725": "none",
     "1081068958077381": "paycost", "1777937970180695": "vague", "1559148382924127": "projection", "1469193108465218": "vague", "1614435140415327": "none",
     "1408398778070134": "jobsvague", "1685225826054515": "orbit", "1337562348365029": "orbit"})
    TEL7 = "1099444266054670 1152197807376924 1135995179081485 1439856308275610 1139512795232176 2165780317708768 2297263294527874 1111718257925494 2335756646962155 1440111811604925 1446092404279510 1791545561895294 2857363984636952 4423960154487729 28803374022604118 2275952023247967 1392687498985291 1385410257116629 1590788092507693".split()
    SWIL7 = "945807044879403 29170911075868498 1736774410723971 1662611835379333 4674635626102080 1082409191331414".split()
    PAID6.update({i: "Texans for Economic Liberty" for i in TEL7})
    PAID6.update({i: "Southwestern Illinois Coalition for Job Growth" for i in SWIL7})
    PAID6.update({
     "2107409233471965": "Facebook Inc.", "1070161062661609": "EEI", "1039532835799443": "EEI",
     "1131079932632500": "Wyoming Driven Innovation LLC", "2725572121213934": "Wyoming Driven Innovation LLC",
     "1651691906330806": "CASE for Consumers", "1571093961719236": "CASE for Consumers", "1034718296292498": "NetChoice PAC", "1743934946712725": "NetChoice PAC",
     "1081068958077381": "Building Our Future Ohio", "1777937970180695": "Building Our Future Ohio", "1559148382924127": "Building Our Future Ohio",
     "1469193108465218": "Mississippi Black Chamber of Commerce", "1614435140415327": "San Jose Silicon Valley Chamber of Commerce", "1408398778070134": "Bright Future Iowa",
     "1336700171235689": "Change.org", "1397108472386456": "Future Tech Insights Inc", "2269627393603877": "Alaskans for Mary",
     "2352225115545933": "No on Prop 45, sponsored by labor, health and environmental organizations", "2235720447823627": "Connie Chan For Congress",
     "2395024634239439": "Restoration of America", "1666627071854024": "The Alaska Center IE", "2216859099714936": "HMP (House Majority PAC)",
     "2085015378859569": "Leila Namvar for Assembly 2026", "1405324455114852": "State + Local Election Alliance", "3166638176869194": "Government That Works PAC",
     "1813102973155015": "The American Independent Foundation", "1481154680727896": "Ohio Democratic Party", "2916146378762235": "Ohio Democratic Party",
     "1487041359951570": "Sierra Club Florida", "1122802630298197": "Elect Katie Hobbs", "1090793656914049": "Gina Hinojosa Campaign",
     "1674590694098686": "LCV Victory Fund", "1721048120020595": "LCV Victory Fund", "1563534862105909": "League of Conservation Voters, Inc.",
     "1376932351095317": "Beau Bayh for Indiana", "1143131671482283": "Senate Republican Campaign Committee", "940563782214883": "NC WARN",
     "1112407328295851": "Future of Life Institute", "4960723094172984": "Pennsylvania Accountability Fund", "1086140594032696": "Friends for Kathy Hochul",
     "2526349944558755": "Blaise Ingoglia for CFO", "921662913973183": "350 Org", "1872380414215516": "MO Protect PAC", "1709389554095155": "Make the Road Action",
     "2338413763656808": "Adamson Ahdoot LLP", "1426197826132476": "NRDC Action Fund", "2306425966784285": "Friends of Sherrod Brown",
     "29011023718533555": "Vermont Public Interest Research Group", "1432634749021670": "Montanans for Responsible Leadership",
     "1113746518099934": "Georgia Conservation Voters Education Fund Inc"})
    LABELED7 = set(PAID6) & {m["library_id"] for m in meta if m["library_id"] in M_FC or "counter" in m["sponsor"]}
    UNL5.update("1937295901048443 29363106506620329 1427060622647550 1361320452652801 1091053473672069 1644287020617322 2278009809631619 "
                "1152975787297827 2192046634687863 2189981561908235 2205240850050436 1436667177798336 2587876388330240 1063635146576957 "
                "1757093043083412 1276251964713428 1010892208696475 961700786604260 1685225826054515 1337562348365029".split())
    NEW7 = set(TEL7) | set(SWIL7) | set(UNL5) | {k for k in PAID6}

if HOOK == "C":
    # spend and impressions as re-read on Nov 17 replace the earlier audience-file figures
    for m in meta:
        if m.get("spend") and "impressions" in m["spend"]:
            s, _, i = m["spend"].partition("; ")
            m["reach"] = f"{s} spent; {i}"
        if m["audience_who"] == "Not published by Meta for this ad" and "Not shown" not in m["paid_for_by"] and "commercial" not in m["paid_for_by"]:
            m["audience_who"] = "Not collected for this ad (Meta publishes age, gender and location in the Ad Library)"
