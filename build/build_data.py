import csv, json, re, os, sys
B = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# ---------- YouTube ad videos (America Connects network) ----------
gat = {}
baai = {"X-S4py1uM3M":(3,"2026-09-18","2026-10-01"),"DYm0Cr-XGso":(4,"2026-09-18","2026-10-01"),"ShWj7Rlz8Pw":(4,"2026-09-09","2026-10-01"),"53QC6xVmIZo":(4,"2026-09-09","2026-09-18")}
for l in open(os.path.join(B, 'gat_ids.txt')):
    if l.strip():
        i, n, f, la = l.strip().split(',')
        gat[i] = dict(gads_creatives=int(n), gads_first=f, gads_last=la)

chan_state = {"Build American AI": "Ohio/Kansas (Build American AI)", "Virginia Connects": "Virginia", "Texas Connects": "Texas", "NC Connects": "North Carolina",
              "OR Connects": "Oregon", "Pennsylvania Connects": "Pennsylvania", "Connected OH": "Ohio",
              "IN Connects": "Indiana", "ConnectedGA": "Georgia", "Louisiana Connects": "Louisiana"}

# Key claim lines from YouTube's auto-generated transcripts (short excerpts only)
claims = {
 "0rAjHVnkXAA": ("Water", "\"Many data centers use no water 96% of the time\"; \"many don't use water at all\"; when they do it's \"often recycled non-drinking water\""),
 "HpDH_znD6DE": ("Water", "\"Some Virginia data centers don't use water for cooling 96% of the time\"; water infrastructure \"spending to exceed $4 billion by 2030\""),
 "oecVwMWyFeE": ("Energy", "\"paying for every watt of energy they use\"; funding energy projects \"to power 325,000 Virginia homes\"; \"helping upgrade Virginia's aging electric grid\""),
 "Ilt7_2XKnn8": ("Energy", "Investing in new energy projects \"enough to power 325,000 homes\"; \"paying for every watt of energy they use\""),
 "jAiyivVAhCE": ("Facts (energy + tax)", "Data centers \"fund new energy projects\", help upgrade \"our aging electric grid\", \"pay for every watt of energy they use\""),
 "gyZYyQDI2mI": ("Affordability", "Data centers supply \"40% of Loudoun's total budget\" using \"only 3% of developable land\"; tax rates falling"),
 "S8Xb7YwvIAU": ("None (jobs, taxes)", "Testimonial spot: jobs and falling property tax rate; \"It is a good neighbor\""),
 "cmzzf9zActQ": ("Water", "\"some data centers use minimal water for cooling once operational\"; invest in technologies that \"reduce and recycle water\""),
 "qJohMKs6c5M": ("Water", "Texas data centers \"use less than half a % of all water used in the state\"; \"many recycle the water they do use\""),
 "UKPwuA2hWjk": ("Energy", "\"paying for every watt of energy they use\"; energy projects \"enough to power at least 3 million homes\""),
 "v72N9D7w4NE": ("Water", "NC data centers \"account for a small fraction of the state's water use\""),
 "8Ba9MUPARqU": ("Energy", "\"paying for every watt of energy they use\"; projects \"enough to power at least 75,000 homes\""),
 "3QroEOG6DdM": ("Energy", "\"Did you know data centers are paying for every watt of energy they use?\""),
 "amDE7M-7wK4": ("Water", "\"Some data centers in Oregon don't use water for cooling 93% of the time\"; \"$4 billion by 2030\" water infrastructure"),
 "UatW5tVYF64": ("Energy", "Energy projects \"to power over 31,000 homes\"; \"paying for every watt of energy they use\""),
 "WOiFlBCIHw4": ("Facts (energy + tax)", "Data centers \"fund new energy projects, help upgrade our electric grid\"; \"over $1 billion\" in state and local tax"),
 "lnMPirn6Vss": ("Water", "\"Some data centers in Pennsylvania don't use water for cooling 95% of the time\""),
 "eMywznSSrtM": ("Energy", "\"paying for every watt of energy they use\"; projects \"enough to power over 1.6 million homes\""),
 "zF54V7HB7NU": ("Water", "\"Some data centers in Ohio don't use water for cooling 97% of the time\"; \"$4 billion by 2030\" water infrastructure"),
 "SKjboEY9bGc": ("Energy", "Energy projects \"enough to power 590,000 homes\"; \"paying for every watt of energy they use\""),
 "qvC9CceYe70": ("Facts (energy + tax)", "Data centers \"fund new energy projects, help upgrade our electric grid\"; \"over a billion dollars\" in tax"),
 "KmBqBgI27Xc": ("Water", "\"Some data centers in Indiana don't use water for cooling 98% of the time\""),
 "ySvxwzQRa8s": ("Energy", "Energy projects \"enough to power over 130,000 homes\"; \"paying for every watt of energy they use\""),
 "IjbFDNM-ep0": ("Facts (energy + tax)", "\"don't use water for cooling 98% of the time\"; \"pay for every watt of energy they use\""),
 "kf5ZQr3ll8o": ("Energy", "\"Did you know data centers are paying for every watt of energy they use?\""),
 "3-pJ0cSKvv8": ("Water", "\"Some data centers in Georgia don't use water for cooling 92% of the time\"; \"$4 billion by 2030\" water infrastructure"),
 "Ns1QMFCUtK8": ("Energy", "Energy projects \"enough to power over 140,000 homes\"; \"paying for every watt of energy they use\""),
 "z84ux4Oi5ow": ("Facts (energy + tax)", "Data centers \"fund new energy projects, help upgrade our electric grid\"; \"over $2 billion\" in tax"),
 "aSO_L69uRjg": ("Water", "\"Some data centers don't use water for cooling 90% of the time\"; \"$4 billion by 2030\" water infrastructure"),
 "NCkkuQ7rULo": ("Energy", "\"paying for every watt of energy they use\"; nationally, projects \"enough to power nearly 8 million homes\""),
 "E83yCe0Lv3E": ("Facts (energy + tax)", "Data centers \"fund new energy projects, help upgrade our electric grid\"; \"over $300 million\" in tax"),
 "X-S4py1uM3M": ("Energy", "\"those data centers use power. A lot of it. So, who pays?\" … \"your electric bill stays the same\""),
 "DYm0Cr-XGso": ("Energy", "\"those data centers use power. A lot of it. So, who pays?\" … \"your electric bill stays the same\""),
 "ShWj7Rlz8Pw": ("Energy", "Ohio data centers are creating jobs, investment and \"decreasing energy rates\""),
 "53QC6xVmIZo": ("General", ""),
}
manual_titles_from_site = {
 "X-S4py1uM3M": ("Ratepayer Pledge - Ohio", "Build American AI", 2322574, 30, "2026-09-18"),
 "DYm0Cr-XGso": ("Ratepayer Pledge - Kansas", "Build American AI", 2344318, 30, "2026-09-18"),
 "ShWj7Rlz8Pw": ("Built by American Workers - Ohio", "Build American AI", 2411737, 30, "2026-09-08"),
 "53QC6xVmIZo": ("Built by American Workers - Kansas", "Build American AI", 1843839, 30, "2026-09-08"),
 "0rAjHVnkXAA": ("Businesses are Rethinking Data Centers: Water", "Virginia Connects", 333261, 30, "2026-06-11"),
 "oecVwMWyFeE": ("Businesses are Rethinking Data Centers: Energy", "Virginia Connects", 321207, 30, "2026-06-11"),
 "S8Xb7YwvIAU": ("Virginia Connects: Loudoun Data Centers", "Virginia Connects", 1191353, None, "2026-09-23"),
 "gyZYyQDI2mI": ("Virginia Connects: Affordability", "Virginia Connects", 2134253, None, "2026-09-18"),
 "qJohMKs6c5M": ("Built Responsibly", "Texas Connects", 5922861, 30, "2026-06-22"),
}

videos = []
seen = set()
def topic_of(t):
    tl = t.lower()
    if 'water' in tl: return 'Water'
    if 'energy' in tl or 'watt' in tl or 'powering' in tl: return 'Energy'
    if 'fact' in tl: return 'Facts (energy + tax)'
    if 'tax' in tl: return 'Tax revenue'
    if 'afford' in tl: return 'Affordability'
    return 'General'
rows = [l.split(' | ') for l in open(os.path.join(B, 'meta.txt')) if l.strip()]
for vid, (t, ch, v, ln, d) in manual_titles_from_site.items():
    rows.append([vid, t, ch, str(v), str(ln or ''), d])
for r in rows:
    vid, title, ch, views, ln, pub = [x.strip() for x in r[:6]]
    if vid in seen: continue
    seen.add(vid)
    g = gat.get(vid, {})
    if vid in baai: g = dict(gads_creatives=baai[vid][0], gads_first=baai[vid][1], gads_last=baai[vid][2])
    ct, cl = claims.get(vid, (None, None))
    videos.append(dict(
        youtube_id=vid, state=(("Ohio" if "Ohio" in title else "Kansas") if ch=="Build American AI" else chan_state.get(ch, ch)), channel=ch, title=title, topic=ct or topic_of(title),
        length_sec=ln, views=int(views), published=pub,
        google_ads_creatives=g.get('gads_creatives', ''), google_ads_first_shown=g.get('gads_first', ''), google_ads_last_shown=g.get('gads_last', ''),
        key_claim=cl or '', transcribed='yes' if cl else 'no',
        youtube_url=f"https://www.youtube.com/watch?v={vid}",
        advertiser=("Build American AI (verified Google advertiser)" if ch=="Build American AI" else "America Connects (verified Google advertiser; paid via GMMB, Inc.)") if g else "",
    ))
videos.sort(key=lambda x: (x['state'], x['topic'], -x['views']))

# ---------- Meta Ad Library: energy/water/cost ads ----------
meta = [
 dict(sponsor="Virginia Connects", state="Virginia", library_id="1603022260291240", dates="Oct 2024 – Mar 2025 (18 ad versions)", spend="e.g. $2.5K–$3K per version", claim_type="Energy",
      text="By supporting innovative 21st-century industries and enabling new clean energy technologies, Virginia's data centers are helping make the future possible."),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="1355279849204870", dates="Apr – Aug 2025; Oct 2025", spend="", claim_type="Energy",
      text="Taking steps to protect our environment – accelerating clean energy development, managing energy use responsibly. (\"Committed to sustainability\")"),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="1108111641257542", dates="Dec 2025 – Apr 2026 (video, several runs)", spend="", claim_type="Energy (costs)",
      text="Virginia's data centers are committed to paying their costs, so Virginians don't."),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="1148486016949172", dates="Nov – Dec 2025", spend="$3.5K–$4K; 250K–300K impressions", claim_type="Energy (prices)",
      text="Boosted Washington Post link: rising electricity prices are \"not data centers\"."),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="2102349793504832", dates="Nov – Dec 2025", spend="$1.5K–$2K", claim_type="Energy (prices)",
      text="\"New study shows data centers can help lower energy costs!\" (boosted Washington Post link)"),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="1813952416150473", dates="Nov – Dec 2025", spend="$2K–$2.5K", claim_type="Energy (prices)",
      text="Boosted PBS link: how data center power demand could help lower electricity prices."),
 dict(sponsor="Virginia Connects", state="Virginia", library_id="908224605261545", dates="Mar – May 2026", spend="$15K–$20K; >1M impressions", claim_type="Energy (costs)",
      text="Video: data centers \"making life more affordable\"."),
 dict(sponsor="Texas Connects", state="Texas", library_id="874918655658106", dates="Jun 23 – Jul 30 2026", spend="$2K–$2.5K", claim_type="Water",
      text="Texas data centers are built responsibly, \"using less than 0.5% of all water used in the state.\""),
 dict(sponsor="Texas Connects", state="Texas", library_id="1300660238797502", dates="Apr – Jul 2026", spend="", claim_type="Water",
      text="\"FACT: Texas data centers consume less than 0.5% of the state's total water\"; cooling tech keeps driving it down."),
 dict(sponsor="Texas Connects", state="Texas", library_id="4368691783381214", dates="Apr 21 – Aug 1 2026", spend="$2.5K–$3K", claim_type="Water",
      text="Engineered for the Texas climate, \"maximizing water efficiency\"."),
 dict(sponsor="Texas Connects", state="Texas", library_id="946918801539771", dates="Apr – Jul 2026", spend="$1.5K–$2K", claim_type="Water",
      text="New technologies deployed \"to reduce their water footprint\"; \"Cleaner. Smarter. More Efficient Every Year.\""),
 dict(sponsor="Texas Connects", state="Texas", library_id="2068150173768978", dates="Apr – Jun 2026", spend="$1K–$1.5K", claim_type="Water",
      text="Jobs and tax revenue \"all while consuming minimal water.\""),
]
for m in meta:
    m['url'] = f"https://www.facebook.com/ads/library/?id={m['library_id']}"
meta_counts = [
 ("Virginia Connects","~190"),("Texas Connects","14"),("North Carolina Connects","5"),("Oregon Connects","13"),
 ("Pennsylvania Connects","12"),("Connected Ohio","~23"),("Indiana Connects","20"),("Build American AI","~370 (mostly national AI policy, not data centers)")]

# ---------- campaign-level entries (from v0.1 + updates) ----------
ads = json.load(open(os.path.join(B, '..', 'ads.json')))
upd = {
 "US-02": dict(claim="Water spot: \"Many data centers use no water 96% of the time.\" Energy spot: \"paying for every watt of energy they use\"",
               evidence="Primary (YouTube transcript)", url_primary="https://www.youtube.com/watch?v=0rAjHVnkXAA",
               notes="13 videos on the site. Water and Energy spots published Jun 11, 2026. The Oct 13 'Building Responsibly' version changes the line to 'Some Virginia data centers don't use water for cooling 96% of the time'. The AWS lawsuit alleges a Virginia Connects video campaign ran the same day AWS posted its '42% reduction' claim. See the YouTube ads tab."),
 "US-03": dict(title="\"96% of the time\" print ad (Free Lance-Star) + Rt. 1 billboard, Stafford Co.",
               claim="\"many data centers use NO WATER 96% of the time\"; \"many don't use water at all\" (billboard); print ad: \"building responsibly\"",
               evidence="Reported (photos in opinion columns)", url_source="https://www.counterpunch.org/2026/08/14/the-data-center-disinformation-campaign-ramps-up/",
               notes="Billboard on Rt. 1 near Crane's Corner was reported removed by Aug 23, 2026 (judwilson.substack.com). Scan of the print ad still needed: Free Lance-Star e-edition or the local library's archive."),
 "US-04": dict(evidence="Primary (YouTube transcript)", verbatim="Verbatim", url_primary="https://www.youtube.com/watch?v=0rAjHVnkXAA",
               claim="\"Many data centers use no water 96% of the time\" (Virginia Connects 'Water' spot, 30s; 15s and 6s cut-downs also ran as Google ads)",
               notes="Confirmed: this is the 'Businesses are Rethinking Data Centers: Water' spot. AWS's Shannon Kellogg made the same claim to WTOP in Oct 2026 ('For 96% of the year, we don't use any water')."),
 "US-05": dict(claim="\"some data centers use minimal water for cooling once operational\" (Water spot); Meta ads: \"less than 0.5% of all water used in the state\"",
               evidence="Primary (YouTube transcript + Meta Ad Library)", url_primary="https://www.youtube.com/watch?v=cmzzf9zActQ"),
 "US-08": dict(title="America Connects state campaigns (PA, OH, IN, GA, LA, OR, NC)", claim_type="Energy + Water",
               claim="Same 'Building Responsibly: Water / Energy / Facts' spots made for each state; scripts not yet transcribed (see YouTube ads tab)",
               evidence="Primary (Google Ads Transparency + YouTube metadata)", url_primary="https://adstransparency.google.com/advertiser/AR15194143977281421313?region=US",
               notes="About 300 Google ads from 'America Connects' (funded via GMMB, Inc.) using ~80 YouTube videos on 9 state channels, Aug 27 – Oct 29 2026. Louisiana Connects is newly identified."),
 "US-11": dict(claim="No AWS-branded TV spot found yet. AWS's spokespeople repeat the industry line: \"For 96% of the year, we don't use any water\"",
               url_source="https://wtop.com/virginia/2026/10/amazon-explains-shift-in-position-on-future-data-center-developments-in-northern-va/",
               notes="Futurism/NYT mention an Amazon Virginia campaign ('connect us to the entire world'). It is not in Google Ads Transparency (the 63 ads pointing to aboutamazon.com are seller, jobs and tax ads) or in Meta's Ad Library. It is likely broadcast-only; check the FCC political files (publicfiles.fcc.gov) for Virginia stations."),
 "US-15": dict(claim="'Ratepayer Pledge' (OH, KS): data centers \"use power. A lot of it. So, who pays?\" … \"your electric bill stays the same\"; 'Built by American Workers – Ohio': \"decreasing energy rates\"", claim_type="Energy",
               evidence="Primary (Google Ads Transparency + YouTube transcript)", url_primary="https://www.youtube.com/watch?v=X-S4py1uM3M", url_source="https://www.wfae.org/science-technology/2026-10-29/who-benefits-when-massive-ai-data-centers-come-to-town",
               notes="$10M effort across KS, OH and WI (NPR). Four 30s spots ran as Google ads Sep 9 – Oct 1 2026 (2 advertiser accounts, 38 ads), each with 1.8–2.4M views. No Wisconsin version found in Google ads; it may be TV-only. No water claims. Its ~370 Meta ads are mostly national AI-policy messages."),
}
for a in ads:
    if a['id'] in upd: a.update(upd[a['id']])
ads.append(dict(id="US-18", region="US", place="Virginia (broadcast TV: World Cup, GMA, The View, Jeopardy!)", sponsor="Virginia Connects", sponsor_type="Industry trade group",
                format="Broadcast TV buys (FCC political files)", title="Prime-time TV flight", date="Jun 9 – Nov 2026", claim_type="Energy + Water",
                claim="At least $708,000 in TV time since June 9, 2026 for spots downplaying water and cost concerns", verbatim="Reported (FCC filings)",
                url_primary="", url_source="https://www.notus.org/metro/northern-virginia-data-centers-politics", evidence="Reported by press (FCC documents)",
                notes="NOTUS analysis of FCC public files; ~$243K booked for Oct–Nov. FCC Public Inspection Files are a further source of buy details."))
ads.append(dict(id="US-19", region="US", place="Louisiana", sponsor="Louisiana Connects", sponsor_type="Industry trade group", format="YouTube / Google video ads",
                title="Building Responsibly: Water / Energy / Facts", date="Sep 18 – Oct 29 2026", claim_type="Energy + Water",
                claim="State versions of the Water and Energy spots; scripts not yet transcribed", verbatim="—",
                url_primary="https://www.youtube.com/watch?v=aSO_L69uRjg", url_source="https://adstransparency.google.com/advertiser/AR15194143977281421313?region=US",
                evidence="Primary (Google Ads Transparency + YouTube metadata)", notes="Not previously reported as part of the America Connects network."))
ads.append(dict(id="US-20", region="US", place="Virginia", sponsor="Virginia Connects", sponsor_type="Industry trade group", format="Facebook / Instagram ads",
                title="Clean energy and cost messaging on Meta", date="Oct 2024 – 2026", claim_type="Energy",
                claim="\"enabling new clean energy technologies\"; \"accelerating clean energy development\"; \"committed to paying their costs, so Virginians don't\"",
                verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1603022260291240",
                url_source="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q=%22Virginia%20Connects%22&search_type=keyword_exact_phrase",
                evidence="Primary (Meta Ad Library)", notes="About 190 ads. Also paid to boost news articles arguing data centers are not behind rising electricity prices. See the Meta ads tab."))

# ---------- lawsuits / challenges ----------
law = [
 dict(id="L-01", type="Lawsuit (consumer protection)", title="Wangusi v. Amazon Web Services & Virginia Connects", jurisdiction="Circuit Court of Arlington County, VA (CL26002535-00)", filed="Jul 2026",
      parties="Dr Nathan Wangusi (former AWS water sustainability manager) v. AWS; Virginia Connects",
      claims_challenged="AWS: NoVA \"dropped water use by 42 percent\"; \"75 percent of the way to water positive\"; facilities run \"ninety-seven percent of the year… not using any water\". Alleges Virginia Connects ran a coordinated video campaign the same day.",
      status="Pending; jury trial sought. AWS declined to comment; says its water data were third-party assured.",
      url="https://www.theregister.com/a/5269723", links_to="US-12, US-02, US-04"),
 dict(id="L-02", type="State AG investigation", title="16-state AG investigation into '100% renewable' claims", jurisdiction="Montana AG + 15 Republican AGs", filed="Sep 2025",
      parties="Microsoft, Meta, Google, Amazon",
      claims_challenged="Claims to be '100% renewable' / 'powered by renewable energy' using unbundled RECs; cites Meta's 100% renewable claim vs diesel generator emissions.",
      status="Information demands due Oct 27, 2025; possible violations of Montana's Unfair Trade Practices and Consumer Protection Act.",
      url="https://dojmt.gov/attorney-general-knudsen-launches-investigation-into-big-tech-companies/", links_to="US-09, US-10, GL-04"),
 dict(id="L-03", type="Leaked document (disclosure)", title="Amazon 'AWS Water Positive Public Launch' memo", jurisdiction="Media investigation (SourceMaterial / The Guardian)", filed="Oct 2025",
      parties="Amazon",
      claims_challenged="2022 memo planning the 'water positive' campaign warned transparency was \"a one-way door\" and advised keeping projections confidential; indirect water (~90% of footprint) left out.",
      status="Amazon calls the memo \"obsolete\".", url="https://www.source-material.org/amazon-leak-reveals-true-data-centres-water-usage-secret-plan/", links_to="US-12, GL-04"),
 dict(id="L-04", type="Public-records lawsuit", title="The Rambler v. Western Virginia Water Authority", jurisdiction="Virginia", filed="2026",
      parties="The Rambler (news outlet) v. Western Virginia Water Authority (re Google, Botetourt Co.)",
      claims_challenged="Sought disclosure of Google's planned water use; Google's announcement centred on 'water stewardship'.",
      status="Contracts released: 2 million gallons/day, rising to 8 million with expansion.",
      url="https://heatmap.news/plus/the-fight/hotspots/google-virginia-water-use", links_to="US-14"),
 dict(id="L-05", type="Public-records lawsuit", title="Milwaukee Riverkeeper v. City of Racine", jurisdiction="Wisconsin", filed="Sep 2025",
      parties="Midwest Environmental Advocates for Milwaukee Riverkeeper v. City of Racine (re Microsoft Mount Pleasant)",
      claims_challenged="Alleges public-records violations over Microsoft data center water use.", status="Reported Sep 2025.",
      url="https://spectrumnews1.com/wi/milwaukee/news/2025/09/16/data-center--mount-pleasant--lawsuit--microsoft-", links_to="US-28"),
 dict(id="L-06", type="Lawsuit (environmental)", title="Municipality of Cerrillos v. Google data center", jurisdiction="Chile (environmental court)", filed="2020",
      parties="Municipality of Cerrillos, residents v. Google",
      claims_challenged="Projected 169 litres/second of water for cooling; climate impacts on water supply not assessed.",
      status="Project halted.", url="https://blogs.law.columbia.edu/climatechange/2026/02/19/data-center-litigation-an-emerging-frontier-for-climate-litigation", links_to=""),
 dict(id="L-07", type="Research / trend report", title="LSE Grantham: Global trends in climate litigation 2026", jurisdiction="Global (Ireland a hotspot)", filed="Jun 2026",
      parties="Friends of the Irish Environment v. EPA (South Dublin) and others",
      claims_challenged="Energy and water impacts of data centres not properly assessed.", status="Multiple pending.",
      url="https://www.business-humanrights.org/en/latest-news/rise-in-litigation-against-data-centres-over-their-environmental-impact-lse-report-finds/", links_to=""),
 dict(id="L-08", type="Judicial review (UK)", title="Foxglove & Global Action Plan v. UK government data centre approval", jurisdiction="England", filed="2026",
      parties="Foxglove, Global Action Plan v. Secretary of State",
      claims_challenged="Energy use of the data centre not considered.",
      status="Government admitted the plans should be quashed; mitigation to be made binding.",
      url="https://www.digit.fyi/?p=129789", links_to=""),
]

template = [
 dict(state="Virginia", water_line="Many data centers use no water 96% of the time (Jun 2026); revised to 'Some Virginia data centers don't use water for cooling 96% of the time' (Oct 2026)", water_pct="96", homes_powered="325,000", tax_line="billions of dollars every year", water_video="0rAjHVnkXAA", water_video_2="HpDH_znD6DE", energy_video="oecVwMWyFeE"),
 dict(state="Texas", water_line="use minimal water for cooling once operational; 'less than half a %' of state water", water_pct="", homes_powered="3 million", tax_line="", water_video="cmzzf9zActQ", water_video_2="qJohMKs6c5M", energy_video="UKPwuA2hWjk"),
 dict(state="North Carolina", water_line="a small fraction of the state's water use", water_pct="", homes_powered="75,000", tax_line="", water_video="v72N9D7w4NE", water_video_2="", energy_video="8Ba9MUPARqU"),
 dict(state="Oregon", water_line="Some data centers in Oregon don't use water for cooling 93% of the time", water_pct="93", homes_powered="31,000", tax_line="over $1 billion", water_video="amDE7M-7wK4", water_video_2="", energy_video="UatW5tVYF64"),
 dict(state="Pennsylvania", water_line="Some data centers in Pennsylvania don't use water for cooling 95% of the time", water_pct="95", homes_powered="1.6 million", tax_line="", water_video="lnMPirn6Vss", water_video_2="", energy_video="eMywznSSrtM"),
 dict(state="Ohio", water_line="Some data centers in Ohio don't use water for cooling 97% of the time", water_pct="97", homes_powered="590,000", tax_line="over a billion dollars", water_video="zF54V7HB7NU", water_video_2="", energy_video="SKjboEY9bGc"),
 dict(state="Indiana", water_line="Some data centers in Indiana don't use water for cooling 98% of the time", water_pct="98", homes_powered="130,000", tax_line="nearly a billion", water_video="KmBqBgI27Xc", water_video_2="", energy_video="ySvxwzQRa8s"),
 dict(state="Georgia", water_line="Some data centers in Georgia don't use water for cooling 92% of the time", water_pct="92", homes_powered="140,000", tax_line="over $2 billion", water_video="3-pJ0cSKvv8", water_video_2="", energy_video="Ns1QMFCUtK8"),
 dict(state="Louisiana", water_line="Some data centers don't use water for cooling 90% of the time", water_pct="90", homes_powered="nearly 8 million (national figure)", tax_line="over $300 million", water_video="aSO_L69uRjg", water_video_2="", energy_video="NCkkuQ7rULo"),
]

exec(open(os.path.join(B,'additions.py')).read())

def wcsv(name, rows, cols=None):
    cols = cols or list(rows[0].keys())
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); [w.writerow(r) for r in rows]
cols = ["id","region","place","sponsor","sponsor_type","format","title","date","claim_type","claim","verbatim","evidence","url_primary","url_source","notes"]
wcsv('campaigns.csv', ads, cols)
wcsv('youtube_ads.csv', videos)
wcsv('meta_ads.csv', meta)
wcsv('lawsuits.csv', law)
wcsv('template_by_state.csv', template)
with open(os.path.join(OUT, 'meta_counts.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['sponsor','meta_ads_found']); w.writerows(meta_counts)
print(len(ads), 'campaigns;', len(videos), 'videos;', len(meta), 'meta;', len(law), 'lawsuits')
print('transcribed', sum(v['transcribed']=='yes' for v in videos))
