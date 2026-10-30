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
  LBNL="https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers",
  IEA="https://www.artificialintelligence-news.com/news/iea-opportunities-and-challenges-ai-for-global-energy/",
  CEG="https://www.businesswire.com/news/home/20260107185180/en",
  OR="https://opb.org/article/2026/07/07/oregon-data-center-general-electric-rate-hikes",
  JOBS="https://qz.com/data-center-jobs-employment-investment-economic-development-051326",
  PWC="https://ppc.land/content/files/2026/05/Data-Center-Economic-Contribution-Study-2026_Final.pdf",
  UCS="https://www.utilitydive.com/news/gas-power-plants-reliability-winter-union-concerned-scientists/704031/",
  ENTERGY="https://www.ktbs.com/news/louisiana/entergy-says-meta-will-save-ratepayers-billions-here-s-how/article_0eb5a464-25ef-5c86-a9eb-a6ccbc71904c.html",
  EPOCH="https://epoch.ai/data-insights/ai-supercomputers-performance-share-by-country",
  DTE="https://www.michiganpublic.org/environment-climate-change/2025-12-18/michigan-regulators-approve-saline-twp-data-center-request-with-conditions",
  DTE2="https://www.bridgedetroit.com/?p=232469",
  PJMIMM="https://energynow.com/2025/06/data-centers-added-9-4-billion-in-costs-on-biggest-us-grid",
  DH="https://www.dailyherald.com/?p=1349282",
  PWCOR="https://olis.oregonlegislature.gov/liz/2025I1/Downloads/CommitteeMeetingDocument/311430",
  COAL="https://energyinnovation.org/report/the-coal-cost-crossover-3-0/",
  OHRATES="https://www.axios.com/local/columbus/2025/08/11/ohio-electricity-prices-data-center-rules",
  OKLAW="https://www.aarp.org/states/oklahoma/oklahoma-enacts-data-center-consumer-protection-law/",
  MOSB4="https://psc.mo.gov/General/Utility_Tariffs_for_Large_Load_Customers",
  MIWATER="https://environmentenergyleader.com/stories/michigan-bill-targets-data-center-water-disclosure,138033",
  BLOOM="https://www.datacenterdynamics.com/en/news/aws-looks-to-deploy-bloom-fuel-cells-at-oregon-data-centers-as-as-primary-fuel-source",
  AIRTRUNK="https://inthecove.com.au/2025/12/05/data-centre-cluster-boom-sydney-water-infrastructure-under-pressure-as-data-centre-approvals-surge",
  ALBERTA="https://www.mondaq.com/canada/utilities/1814978/albertas-byog-framework-what-data-centre-and-generation-proponents-need-to-know",
  JOBSGJF="https://qz.com/data-center-jobs-employment-investment-economic-development-051326",
  E3="https://ppc.land/data-centers-5-5m-jobs-927bn-gdp-and-no-proof-they-raised-your-energy-bills/",
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
 "neidemand": ("Missing context", "The IEA projects global data-center electricity use to more than double by 2030, which matches the ad. For the US, DOE/LBNL projects use to 'double or triple' by 2028, so 'triple' is the top of the range. 'The only source that's both clean and reliable' leaves out hydro and geothermal.", "LBNL"),
 "nukeslogan": ("Not checkable", "A slogan ('Nuclear makes it happen'); no figure to test.", ""),
 "nmpowering": ("Missing context", "Some data centers buy power from existing nuclear plants, but most announced nuclear-for-data-center deals depend on restarts or new reactors not yet online; the IEA expects the first small modular reactors around 2030.", "IEA"),
 "ceglean": ("Missing context", "Constellation bought Calpine in January 2026, adding over 50 natural-gas plants. 'Emissions free' describes its nuclear fleet, not all of its generation; the spots kept running after the deal.", "CEG"),
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
 "jobsmodel": ("Missing context", "These are modeled totals from PwC's study for the Data Center Coalition: direct jobs plus 'indirect and induced' jobs estimated with an economic multiplier, not jobs inside data centers. Facilities themselves employ few permanent staff (often 30–50, up to a few hundred), and Good Jobs First puts the average subsidy in large deals near $2M per job. Georgia's state auditor cut its own data center job estimate by about two-thirds (see Internal documents, ID-17).", "JOBS"),
 "jobsvague": ("Not checkable", "Says data centers create jobs without a number, place or time period. Permanent staffing at a data center is usually small; most jobs are temporary construction work.", "JOBS"),
 "gasreliable": ("Missing context", "Gas plants made up most of the capacity that failed in recent winter storms: 56% in Winter Storm Uri (2021) and 63% in Winter Storm Elliott (2022), per the Union of Concerned Scientists using FERC/NERC data. Gas supply can freeze off when demand peaks.", "UCS"),
 "coalbills": ("Disputed", "Studies disagree. Energy Innovation's Coal Cost Crossover (2023) finds 99% of US coal plants cost more to run than replacement with new local wind, solar and storage; an Energy Ventures Analysis study (2025) argues replacing retiring coal plants would cost more. Keeping retiring plants open by federal order has been estimated to cost ratepayers over $3B a year.", "COAL"),
 "entergy": ("Missing context", "Entergy's own 20-year projection (about $650M plus $2B from the Meta deals), which depends on Meta's rates exceeding the cost of serving it. Consumer advocates say the savings rest on optimistic assumptions, and gas-plant costs were redacted in the rate case (Internal documents, ID-13).", "ENTERGY"),
 "chinadata": ("Missing context", "Implies the alternative to building in Texas is data going to China. Epoch AI estimates the US already hosts about three-quarters of global AI computing capacity and China about 15%; where data is stored depends on company and federal rules, not one state's permits.", "EPOCH"),
 "chinaspend": ("No public data", "No source is given for China 'investing trillions'. Epoch AI estimates the US hosts about three-quarters of global AI computing capacity and China about 15%.", "EPOCH"),
 "golf": ("Missing context", "Compares only on-site water. National golf-course and data-center totals are not published on the same basis, and on-site figures leave out the water used to generate a data center's electricity. HARC estimates Texas data centers used about 0.4% of state water in 2025, rising to as much as 2.7% by 2030.", "HARC"),
 "notx": ("Not yet checked", "No captions or text available; we haven't transcribed this ad yet.", ""),
 "taxmodel": ("Missing context", "Statewide 'tax revenue' figures like these match PwC's model for the Data Center Coalition, which counts direct, indirect and induced taxes (Oregon: $789M in 2023 on that basis). They don't subtract the sales-tax exemptions most of these states give data centers.", "PWCOR"),
 "related300": ("Missing context", "The $300M a year is DTE's own projection of what Oracle's payments will add to fixed grid costs. Michigan regulators approved the contracts with conditions, including that DTE absorbs any shortfall; the Attorney General appealed, and critics say the cost of serving the site could offset the savings.", "DTE"),
 "eeispread": ("Missing context", "Spreading fixed costs over more sales can lower rates only if a large customer pays more than the new costs it causes. In PJM, the independent market monitor found data center demand added about $9.3B to capacity costs paid by all customers.", "PJMIMM"),
 "ssgatax": ("Supported", "Local reporting cites an estimate of $5–6 million a year in property taxes for the CyrusOne project.", "DH"),
 "ibewtax": ("Missing context", "Local reporting gives a $31.1 million property-tax bill for Meta's DeKalb campus (2025). The campus also has a 20-year, 55% property-tax abatement and state sales-tax exemptions.", "DH"),
 "wmmstudy": ("Missing context", "The ad doesn't name its 'independent study'. The best-known study with this finding, by E3 (May 2026), was commissioned by the Data Center Coalition, which funds these ads; it also found data-center demand drove about half of PJM's capacity price increase and flagged risks where new supply lags demand.", "E3"),
 "ohiorates": ("Disputed", "Ohio electricity bills rose as data-center demand drove up PJM capacity prices: AEP Ohio's June 2025 change added about $27 to an average monthly bill, and Ohio residential prices rose about 37% from 2019 to 2025.", "OHRATES"),
 "oklaw": ("Missing context", "Oklahoma's Data Center Consumer Ratepayer Protection Act (HB 2992, in force July 1, 2026) requires loads of 75 MW or more to pay for the infrastructure they need. It is new and untested; 'ensures' goes beyond what any rate case has yet shown.", "OKLAW"),
 "mosb4": ("Missing context", "Senate Bill 4 does require large-load tariffs, and regulators approved them for Ameren and Evergy. The same law lets utilities charge customers for plants under construction, and Missouri's consumer advocate and the Consumers Council say its protections leave room for cost shifts.", "MOSB4"),
 "miwater": ("Missing context", "Michigan regulates large water withdrawals and requires tax-break data centers to use public water systems, but sets no data-center water caps and does not require facility-level disclosure; bills to add both were introduced in 2026.", "MIWATER"),
 "jobs100": ("Missing context", "Large campuses can employ 100 or more, but typical permanent staffing is 30–50, and the '150 to 400 more' jobs are a multiplier estimate, not counted jobs.", "JOBSGJF"),
 "bloom": ("Missing context", "'Without combustion' is accurate, but most Bloom servers run on natural gas. Bloom's own range is 679–833 lb of CO2 per MWh, about the US grid average. 'Renewable' applies only when they run on biogas or hydrogen; Oregon regulators said gas fuel cells would raise AWS's emissions there.", "BLOOM"),
 "airtrunk": ("Missing context", "Dry closed-loop cooling avoids evaporative water use on site, but leaves out water used to generate the electricity. AirTrunk has not disclosed water use for its Sydney sites, some of which use adiabatic (evaporative) cooling.", "AIRTRUNK"),
 "alberta": ("Missing context", "Alberta's 'bring your own generation' rule is now law (Data Centre Regulation, June 2026), and most self-supplied power will come from on-site gas plants. We found no rule placing data centres last for water.", "ALBERTA"),
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
 "NU-01": ("Nuclear Energy Institute", "Nuclear Energy Institute (verified Google advertiser; Meta disclaimer)", "Yes: trade group named", "National YouTube and Google viewers; Meta audience not published for these ads", "neidemand", ""),
 "NU-02": ("Nuclear Matters", "Nuclear Matters (Meta disclaimer)", "Partly: group named, funders not disclosed", "National (Meta)", "nmpowering", ""),
 "NU-03": ("Constellation", "Constellation Energy Corporation (verified Google advertiser)", "Partly: some spots run on a 'Clean Jobs for Pennsylvania' channel paid for by Constellation", "National; Pennsylvania", "ceglean", ""),
 "OI-01": ("Williams Companies", "Williams Companies, Inc. (Meta disclaimer; verified Google advertiser)", "Yes: company named", "National (Meta audience data not pulled)", "gasreliable", ""),
 "OI-02": ("Coal and fossil-fuel advocates", "American Energy Institute; Brian Helton for West Virginia (Meta disclaimers)", "Partly: groups named, funders not disclosed", "National; West Virginia", "coalbills", ""),
 "OI-03": ("Entergy Louisiana", "Not shown: ran without an issue-ad label, so Meta publishes no payer, spend or audience", "Yes: company brand", "Louisiana", "entergy", ""),
 "US-38": ("Texans for Economic Liberty", "Texans for Economic Liberty (Meta disclaimer; contact at Harris Media LLC)", "Partly: group named, funders not disclosed", "Texas (Meta)", "chinadata", ""),
 "US-39": ("NetChoice", "NetChoice (Meta disclaimer)", "Partly: trade group named; member companies not shown in the ad", "National; South Dakota", "chinaspend", ""),
 "US-40": ("American Edge Project", "American Edge (Meta disclaimer; verified Google advertiser)", "Partly: group named; donors not disclosed, but CNBC reported Facebook (now Meta) gave $34M in 2020–21 after a $4M seed grant", "National", "jobsvague", ""),
 "US-41": ("Connects state groups", AC_PAID.replace("Google lists the payer as GMMB, Inc.", "Meta disclaimers name each state group"), AC_DISC, "Ohio, Indiana, Oregon, Pennsylvania, Virginia (Meta)", "jobsmodel", ""),
 "US-42": ("Related Companies", "Related Companies / Related Digital (Meta disclaimers; verified Google advertisers)", "Yes: developer named; the end user (Oracle) is not named in the ads", "Michigan and national (Meta; YouTube)", "related300", ""),
 "US-43": ("Springfield Sangamon Growth Alliance", "Springfield Sangamon Growth Alliance (Meta disclaimer on labeled ads)", "Partly: some ads unlabeled; CyrusOne named in the ads", "Sangamon County, Illinois", "zerocool", ""),
 "US-44": ("Southwestern Illinois Coalition for Job Growth", "Southwestern Illinois Coalition for Job Growth (Meta disclaimer)", "Partly: coalition named, members not listed in the ads", "Metro East Illinois", "golf", ""),
 "US-45": ("Future Ready Frederick", "Future Ready Frederick (Meta disclaimer; verified Google advertiser)", "Partly: group named, funders not disclosed", "Frederick County, Maryland", "vague", ""),
 "US-46": ("Built Here Oklahoma", "Not shown: ads ran without an issue-ad label", "No", "Oklahoma", "oklaw", ""),
 "US-47": ("NWI Data Facts", "Not shown on most ads (no issue-ad label)", "No", "Northwest Indiana", "jobsvague", ""),
 "US-48": ("Power Connection, IBEW Local 364", "Not shown: ad ran without an issue-ad label", "Partly: union named", "DeKalb area, Illinois", "ibewtax", ""),
 "OI-04": ("Edison Electric Institute", "EEI (Meta disclaimer on its 'We Stand For Energy' page; verified Google advertiser)", "Partly: page name differs from the payer", "Missouri (Meta); national (Google)", "eeispread", ""),
 "OI-05": ("Bloom Energy", "Bloom Energy Corp (verified Google advertiser)", "Yes: company brand", "US Google search users", "bloom", ""),
 "GL-13": ("AirTrunk", "Not shown: ad ran without an issue-ad label", "Yes: company brand", "Australia", "airtrunk", ""),
 "GL-14": ("Government of Alberta", "YourAlberta (Government of Alberta) (Meta disclaimer)", "Yes: government", "Alberta", "alberta", ""),
 "GL-15": ("Saskatchewan Party Caucus", "Saskatchewan Party Caucus (Meta disclaimer)", "Yes: party caucus", "Saskatchewan", "jobsvague", ""),
 "GL-16": ("Counter-ads outside the US", "Friends of the Earth, Environment Centre NT, Greens MPs, NSNDP and others (Meta disclaimers)", "Yes: campaign disclaimers", "UK, Australia, Canada", "counter", ""),
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
VID_FC = {"ShWj7Rlz8Pw": "ohiorates", "u-sHlkSxmsw": "notx", "dyhMX1Gt3OA": "notx", "XTsm24wKu_I": "golf", "9WjL1mNgkjY": "paycost", "-qFK2gX70J8": "notx", "jgoi3ilu0mo": "wmmstudy", "1i0K-Ejk6o8": "notx", "qPI8sUP1ebQ": "related300", "zKdCn0Y-MRQ": "notx", "aEfo8Wqg8fM": "notx", "a8A6vcZs194": "notx", "q7deAI_ooMI": "jobsvague", "-AOJOKtomfE": "related300", "ma3SBpoNmL8": "vague", "Z3RD_ho5Pt8": "jobsvague", "T0cNo2jAEu0": "vague", "jhvGXO2wIGM": "vague", "jytG-SMKgIo": "notx", "EqG8jj64flk": "jobsvague", "Io7h_19LHWE": "nukeslogan", "ffDG_n1zcis": "nukeslogan", "oThjI485c3U": "nukeslogan", "4GwRC82WLzs": "neidemand",
          "TsiNMFTxjF0": "ceglean", "1zTYeqE1VVc": "ceglean", "bj9dZxbgKu0": "none", "zu_AH_cVtLk": "none", "IwQCwpzG_GY": "txbuilt", "L-g5j8Dah_o": "orcosts", "F-lA8tM5ytg": "orcosts", "0JS96iU0k0o": "compasswater",
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
    elif ch in ("Nuclear Energy Institute", "Constellation", "Clean Jobs for Pennsylvania"):
        v["appears_as"] = ch; v["audience_where"] = v["state"]
        v["paid_for_by"] = "Nuclear Energy Institute (verified Google advertiser)" if ch.startswith("Nuclear") else "Constellation Energy Corporation (verified Google advertiser)"
        v["funding_disclosed"] = "Partly: channel name differs from the payer" if ch == "Clean Jobs for Pennsylvania" else "Yes"
    elif ch == "Compass Datacenters":
        v["appears_as"] = ch; v["paid_for_by"] = C["US-34"][1]; v["funding_disclosed"] = "Yes: company brand"; v["audience_where"] = v["state"]
    elif ch in ("Google", "Grow with Google"):
        v["appears_as"] = "Google"; v["paid_for_by"] = "Google LLC (verified Google advertiser)"; v["funding_disclosed"] = "Yes: company brand"; v["audience_where"] = v["state"]
    elif ch in ("Related Companies", "Future Ready Frederick") or ch.startswith("Project Jupiter"):
        v["appears_as"] = ch.split(" (")[0]; v["paid_for_by"] = v.get("advertiser") or ch; v["audience_where"] = v["state"]
        v["funding_disclosed"] = C["US-42"][2] if ch == "Related Companies" else (C["US-45"][2] if ch.startswith("Future") else "Partly: campaign name; STACK Infrastructure is the verified advertiser")
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
M_FC.update({"1669008000286846": "vague", "374094262207192": "vague", "1628561594449326": "nmpowering", "805063845222669": "none"})
M_FC.update({"1007646302344543": "compasswater", "1442097564548229": "compassrates", "1927445971757558": "none", "1821241565897458": "vague"})
M_FC.update({"1293519818383322": "gasreliable", "587902634262124": "gasreliable", "717843787472163": "vague", "892580369759098": "vague",
  "703723472302769": "vague", "1441711237344326": "coalbills", "39910901075163809": "entergy", "1058363043622922": "chinadata",
  "943500362131502": "chinadata", "3049723345231314": "chinadata", "2755475634846898": "jobsvague", "1602684917471991": "chinaspend",
  "1160273426235067": "jobsvague", "1649238866660651": "jobsvague", "1651381009885730": "jobsvague", "2630526374051685": "jobsvague",
  "2206183790208701": "jobsmodel", "1470542390873188": "jobsmodel", "2124533385058477": "jobsmodel", "4266661140310707": "jobsmodel",
  "26196583389979722": "jobsmodel"})
M_FC.update({"2354723418684252": "jobsvague", "1094460799605149": "jobsvague", "1097501102754397": "jobsvague", "2547339009120724": "jobsvague",
  "1550680310423772": "jobsvague", "2862833327433517": "chinadata", "951757917360097": "chinadata", "2063664707611988": "chinadata", "1090651106914529": "chinadata",
  "3386975414803944": "chinaspend", "1076917745072871": "jobsvague", "1600467024909948": "jobsvague", "1744760690072742": "jobsvague", "2182059112743694": "jobsvague",
  "1742995237835583": "jobsvague", "1272138085104271": "jobsmodel", "825735950567625": "jobsmodel", "1333681062048725": "vague", "1303405985187214": "taxmodel",
  "1059638200321804": "taxmodel", "2591474914616984": "taxmodel", "1760680921635866": "taxmodel", "994343963380862": "vague", "1089916010172765": "taxmodel",
  "2104731653767779": "taxmodel", "1108461391525372": "taxmodel", "1639529273807981": "vague", "1107646538861160": "entergy", "1055641820404525": "vague",
  "1791895145337885": "vague", "2250211189162737": "pledge", "1272981641648678": "related300", "2785184291821003": "related300", "1272495225070609": "vague",
  "1982285979053620": "nodata", "862531826652827": "vague", "1351760670154303": "zerocool", "2160503341546394": "ssgatax", "2031856607408530": "golf",
  "2076591636312533": "zerocool",  "1590508512808580": "vague", "1754136019201009": "oklaw", "2372537626883774": "oklaw",
  "1146371605015712": "vague", "1401579901604310": "jobsvague", "28792759310375561": "ibewtax", "2358942264597308": "eeispread", "2236644027133626": "mosb4", "1120497433890697": "jobs100", "1615312140006989": "miwater", "1441711237344326": "coalbills", "1400627271367785": "vague", "1810827893585871": "airtrunk", "1601780274686250": "alberta", "1071752032382332": "jobsvague"})
PAID6 = {"1730516554619571": "Earthjustice", "4301839766740670": "Earthjustice", "1511733583996891": "Earthjustice", "1641018310411783": "Natural Resources Defense Council",
  "1048346007649229": "Montana Conservation Voters", "1400627271367785": "Williams Companies, Inc.", "1601780274686250": "YourAlberta (Government of Alberta)",
  "1071752032382332": "Saskatchewan Party Caucus", "2172889726617169": "Friends of the Earth (EWNI)", "2012700756027978": "Environment Centre NT",
  "1617839936414098": "Katherine Copsey", "3082818265257315": "NSNDP", "1790561518818248": "Olivia Chow for Mayor"}
PAID5 = {"2354723418684252": "Texans for Economic Liberty", "1094460799605149": "Texans for Economic Liberty", "1097501102754397": "Texans for Economic Liberty",
  "2547339009120724": "Texans for Economic Liberty", "1550680310423772": "Texans for Economic Liberty", "2862833327433517": "Texans for Economic Liberty",
  "951757917360097": "Texans for Economic Liberty", "2063664707611988": "Texans for Economic Liberty", "1090651106914529": "Texans for Economic Liberty",
  "3386975414803944": "NetChoice", "1076917745072871": "American Edge", "1600467024909948": "American Edge", "1744760690072742": "American Edge",
  "2182059112743694": "American Edge", "1742995237835583": "American Edge", "1272138085104271": "Virginia Connects", "825735950567625": "Virginia Connects",
  "1333681062048725": "Virginia Connects", "994343963380862": "Connected Georgia, a Project of America Connects", "1639529273807981": "North Carolina Connects",
  "1791895145337885": "Wyoming Driven Innovation LLC", "1272981641648678": "Related Companies", "2785184291821003": "Related Companies",
  "1272495225070609": "Related Companies", "1982285979053620": "Related Companies", "862531826652827": "Related Digital",
  "2160503341546394": "Springfield Sangamon Growth Alliance", "2031856607408530": "Southwestern Illinois Coalition for Job Growth",
  "2076591636312533": "Southwestern Illinois Coalition for Job Growth", "1120497433890697": "Southwestern Illinois Coalition for Job Growth",
  "1590508512808580": "Future Ready Frederick", "1146371605015712": "NWI Data Facts", "2358942264597308": "EEI", "2236644027133626": "EEI",
  "912252061727422": "Conservation Voters of Michigan PAC", "1638176964326002": "DAGA People's Lawyer Project NV", "1091363737137522": "Half Court Political Fund",
  "1120874683614951": "Sierra Club Florida", "2060421341232960": "Friends of Tina Kotek", "2228839401023928": "Dr Theresa Brooks for State Senate",
  "1787510099256086": "The Wisco Project PAC", "2784983821860945": "WorkMoney", "2026394025414584": "Texans for Henry Cuellar Congressional Campaign",
  "1221109883504437": "Tiffany for Wisconsin", "1119207593924689": "Maine Conservation Voters Action Fund", "1815074113136528": "Citizens for Common Sense Michigan",
  "1375768711074811": "Government That Works PAC", "28194997226868784": "Innovation Ohio", "2167025290881029": "Friends for Kathy Hochul",
  "1751481502753963": "Utility Information Alliance"}
UNL5 = {"1303405985187214", "1059638200321804", "2591474914616984", "1760680921635866", "1089916010172765", "2104731653767779", "1108461391525372",
  "1107646538861160", "1055641820404525", "1351760670154303", "1754136019201009", "2372537626883774", "1401579901604310", "28792759310375561"}
import ast
_s = open(os.path.join(B, "sectors.py"), encoding="utf-8").read()
M_PAID4 = ast.literal_eval(_s[_s.index("M_PAID4 = ") + 10:_s.index("}", _s.index("M_PAID4 = ")) + 1])
UNLABELED = {"1007646302344543", "1442097564548229", "1927445971757558", "1077055241572370", "1913744136701738", "4680740768826912", "1064803106540533", "970055792802575", "39910901075163809"}
for m in meta:
    i = m["library_id"]; s = m["sponsor"]; a = aud.get(i)
    m["appears_as"] = re.sub(r"\s*\(.*?\)", "", s)
    if a:
        m["paid_for_by"] = a["paid_for_by"] + " (Meta 'Paid for by' disclaimer)"
        m["audience_where"] = a["locations"]; m["audience_who"] = a["audience_summary"]
        m["reach"] = f"{a['spend']} spent; {a['impressions']} impressions"
        for f in ("age_18_34", "age_35_54", "age_55_plus", "women", "men"): m[f] = a[f]
    else:
        if i in PAID6:
            m["paid_for_by"] = PAID6[i] + " (Meta 'Paid for by' disclaimer)"
        elif i == "1810827893585871":
            m["paid_for_by"] = "AirTrunk: Not shown: ad ran without an issue-ad label, so Meta publishes no payer, spend or audience"
        elif i in PAID5:
            m["paid_for_by"] = PAID5[i] + " (Meta 'Paid for by' disclaimer)"
        elif i in UNL5 or i == "2250211189162737":
            m["paid_for_by"] = (m["appears_as"] + ": " if True else "") + ("Meta says this ad ran without a required disclaimer" if i == "2250211189162737" else "Not shown: ad ran without an issue-ad label, so Meta publishes no payer, spend or audience")
        elif i in M_PAID4:
            m["paid_for_by"] = M_PAID4[i] + " (Meta 'Paid for by' disclaimer)"
        elif i in UNLABELED:
            m["paid_for_by"] = ("Compass Datacenters: " if "Compass" in s else "Entergy Louisiana: " if "Entergy" in s else "") + "Not shown: ad ran as 'Sponsored' without an issue-ad label, so Meta publishes no payer, spend or audience"
        elif s in ("Nuclear Energy Institute", "Nuclear Matters"):
            m["paid_for_by"] = s + " (Meta disclaimer)"
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
NUC = {"Nuclear Energy Institute", "Nuclear Matters", "Constellation", "Clean Jobs for Pennsylvania"}
def stype(g):
    if g.startswith("Power Connection"): return "Labor union"
    if g == "AirTrunk": return "Data center operator"
    if g == "Government of Alberta": return "Government"
    if g == "Saskatchewan Party Caucus": return "Political (supporting)"
    if "Connect" in g: return "Industry trade group"
    if g in NUC: return "Nuclear industry"
    if g == "American Energy Institute" or g.startswith("Brian Helton"): return "Coal and fossil advocacy"
    if g == "Edison Electric Institute": return "Electric utility trade group"
    if g in ("Related Companies", "Related Digital"): return "Data center developer"
    if g in ("Springfield Sangamon Growth Alliance", "Southwestern Illinois Coalition for Job Growth", "Future Ready Frederick", "Built Here Oklahoma", "NWI Data Facts"): return "Local pro-data-center group"
    if g.startswith("Power Connection"): return "Labor union"
    if g == "AirTrunk": return "Data center operator"
    if g == "Government of Alberta": return "Government"
    if g == "Saskatchewan Party Caucus": return "Political (supporting)"
    if g.startswith("Project Jupiter"): return "Data center developer"
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
        funding_disclosed=m["funding_disclosed"], sponsor_type=stype(m["appears_as"]) or ("Advocacy group or campaign (counter-ad)" if "counter" in m["sponsor"] else ""),
        platform="Facebook / Instagram", date=m["dates"], claim_type=m["claim_type"], claim=m["text"], factcheck=m["factcheck"],
        factcheck_note=m["factcheck_note"], factcheck_url=m["factcheck_url"], lawsuit_ids=m["lawsuit_ids"], lawsuit_role=m["lawsuit_role"],
        audience_where=m["audience_where"], audience_who=m["audience_who"], reach=m["reach"], url=m["url"],
        age_18_34=m.get("age_18_34", ""), age_55_plus=m.get("age_55_plus", ""), women=m.get("women", "")))
THEMES = [("Jobs", r"\bjobs?\b|workers|electrician|welder|pipefitter|employ|trades|hiring|careers?"),
          ("China / national security", r"china|national security|foreign|america wins|ai race|tech race|american hands|american data"),
          ("Water", r"water|gallon|drought|aquifer"),
          ("Energy & rates", r"electric|power|energy|\bbills?\b|\brates?\b|grid|gas\b|coal|nuclear|renewable|megawatt|fuel cell"),
          ("Taxes & economy", r"\btax|revenue|econom|investment|billion")]
def themes(r):
    t = " ".join([r.get("claim") or "", r.get("claim_type") or ""]).lower()
    return "; ".join(n for n, p in THEMES if re.search(p, t))
def category(r):
    st = (r.get("sponsor_type") or "").lower(); ct = (r.get("claim_type") or "").lower()
    if "nuclear industry" in st: return "Nuclear industry"
    if st in ("gas industry", "coal and fossil advocacy", "electric utility", "electric utility trade group", "fuel cell maker"): return "Other industries riding the boom"
    if "counter" in ct or "counter" in st or "opposing" in st: return "Opposition and counter-ads"
    return "Data center industry and allies"
for r in allrows:
    r["category"] = category(r)
    r["themes"] = themes(r)
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
        freq.append(dict(uid=r["uid"], kind=r["kind"], category=r["category"], appears_as=r["appears_as"], claim_type=r["claim_type"],
                         factcheck=r["factcheck"], in_lawsuit=r["in_lawsuit"], word=w, n=n))

wcsv("campaigns.csv", camp); wcsv("youtube_ads.csv", vids); wcsv("meta_ads.csv", meta); wcsv("lawsuits.csv", laws)
wcsv("ads_all.csv", allrows, ["uid", "kind", "category", "themes", "appears_as", "paid_for_by", "funding_disclosed", "sponsor_type", "platform", "date",
     "claim_type", "claim", "factcheck", "factcheck_note", "factcheck_url", "checkable", "in_lawsuit", "lawsuit_ids", "lawsuit_role",
     "audience_where", "audience_who", "reach", "age_18_34", "age_55_plus", "women", "url"])
wcsv("word_freq.csv", freq)
wcsv("meta_audience.csv", list(aud.values()))
print("ads_all", len(allrows), "| word rows", len(freq), "| units", len(units))
print(collections.Counter(r["factcheck"] for r in allrows))
print(collections.Counter(t for r in allrows for t in r["themes"].split("; ") if t));print(collections.Counter(r["in_lawsuit"] for r in allrows)); print(collections.Counter(r["category"] for r in allrows))
