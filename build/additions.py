# ---- audit fixes + new entries (v0.4, 30 Oct 2026) ----
fix = {
 "US-04": dict(date="Jun 11, 2026", title="'Businesses are Rethinking Data Centers: Water' (TV/YouTube) + billboard"),
 "US-06": dict(claim="\"paying for every watt of energy they use\"; energy projects \"enough to power at least 75,000 homes\"; water spot: \"a small fraction of the state's water use\"",
               evidence="Primary (YouTube transcript) + press", verbatim="Verbatim (auto-captions)", url_primary="https://www.youtube.com/watch?v=8Ba9MUPARqU", claim_type="Energy + Water"),
 "US-07": dict(claim="\"Some data centers in Oregon don't use water for cooling 93% of the time\"; energy projects to power \"over 31,000 homes\"; \"paying for every watt\"",
               evidence="Primary (YouTube transcript) + press", verbatim="Verbatim (auto-captions)", url_primary="https://www.youtube.com/watch?v=amDE7M-7wK4", claim_type="Energy + Water"),
 "US-08": dict(claim="Water spots: \"Some data centers in [state] don't use water for cooling X% of the time\" (PA 95, OH 97, IN 98, GA 92); energy spots: \"paying for every watt\" + homes-powered figure",
               evidence="Primary (Google Ads Transparency + YouTube transcripts)", verbatim="Verbatim (auto-captions)"),
 "US-12": dict(url_primary="https://sustainability.aboutamazon.com/aws-sustainability-fact-sheets/aws-fact-sheet-virginia.pdf"),
 "US-19": dict(claim="\"Some data centers don't use water for cooling 90% of the time\"; national figure: projects \"enough to power nearly 8 million homes\"",
               evidence="Primary (YouTube transcript)", verbatim="Verbatim (auto-captions)"),
 "US-20": dict(notes="About 190 ads since Oct 2024. Also paid to boost news articles arguing data centers are not behind rising electricity prices. See the Meta ads tab."),
}
for a in ads:
    if a['id'] in fix: a.update(fix[a['id']])

new_ads = [
 dict(id="US-21", region="US", place="National (Meta, Google/YouTube)", sponsor="QTS Data Centers (Blackstone)", sponsor_type="Operator", format="Facebook/Instagram + YouTube video ads",
      title="'Zero water wasted' / 'Self-funded energy' / 1.5 billion gallons", date="Apr – Oct 2026", claim_type="Energy + Water",
      claim="\"We use a closed-loop system that consumes zero water for cooling, once operational\"; \"We pay for our power and infrastructure, so you don't foot the bill\"; YouTube: \"Saving Nearly 1.5 Billion Gallons a Year\"",
      verbatim="Verbatim (Meta Ad Library; YouTube titles)", url_primary="https://www.facebook.com/ads/library/?id=1399130278973163",
      url_source="https://adstransparency.google.com/advertiser/AR09116677971116032001?region=US", evidence="Primary (Meta Ad Library + Google Ads Transparency)",
      notes="QTS Realty Trust has ~95 Google ads (verified). Water videos have no captions (on-screen text). 'Once operational' and 'for cooling' are qualifiers."),
 dict(id="US-22", region="US", place="Texas", sponsor="Texans for Economic Liberty", sponsor_type="Advocacy group", format="Facebook ads + YouTube video ads",
      title="'The Texas Standard' / 'How Data Centers Benefit Texas'", date="May – Oct 2026", claim_type="Energy + Water",
      claim="\"Data centers provide their own power, reuse their own water, lower electricity costs\" (Meta, $100K–$125K); YouTube: \"many new data centers now use zero water for cooling\"; golf courses use more water",
      verbatim="Verbatim (Meta Ad Library; YouTube transcript)", url_primary="https://www.youtube.com/watch?v=XTsm24wKu_I",
      url_source="https://www.facebook.com/ads/library/?id=2096764071716470", evidence="Primary (Meta Ad Library + YouTube transcript)",
      notes="21 Google ads (verified advertiser). 'How Data Centers Benefit Texas' has 1.5M views. Separate national-security spots ('keep American data in American hands') have 2M views."),
 dict(id="US-23", region="US", place="Michigan", sponsor="Michigan for Responsible Data Centers", sponsor_type="Industry/advocacy group", format="Facebook ads",
      title="'Michigan's existing protections'", date="Apr – Oct 2026", claim_type="Energy + Water",
      claim="To get incentives, data centers \"must secure 90% of their electricity from clean, renewable sources\"; \"You aren't on the hook to pay for the power data centers use\"; water regulations \"in place\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1595817172204916", url_source="https://mifordatacenters.org",
      evidence="Primary (Meta Ad Library)", notes="Funding not disclosed on the ads. Claims describe state rules, not company performance."),
 dict(id="US-24", region="US", place="Illinois", sponsor="Fight Back Fund", sponsor_type="Union-affiliated advocacy", format="Facebook ad",
      title="'Data centers can benefit us'", date="Aug 4 – 27 2026", claim_type="Water",
      claim="Illinois towns work with data centers \"to keep water safe, usage low, and costs even lower\"", verbatim="Verbatim (Meta Ad Library)",
      url_primary="https://www.facebook.com/ads/library/?id=1086975924010981", url_source="", evidence="Primary (Meta Ad Library)", notes="Cites DeKalb and Elk Grove Village."),
 dict(id="US-25", region="US", place="Doña Ana County, NM", sponsor="Oracle (Project Jupiter / Stargate)", sponsor_type="Hyperscaler", format="Bilingual TV, radio, digital, social + canvassing",
      title="Project Jupiter campaign (ProjectJupiterTogether.com)", date="May 26 2026 – (several months)", claim_type="Energy + Water",
      claim="Spotlights a \"cleaner energy plan\" (Bloom fuel cells) and \"lower water usage\"; closed-loop, non-evaporative cooling; $50M for local water systems",
      verbatim="Quoted from press release", url_primary="https://www.oracle.com/news/announcement/oracle-lanza-una-nueva-campana-que-destaca-sus-compromisos-2026-05-26/",
      url_source="https://www.abqjournal.com/news/project-jupiter-files-disclosures-over-34m-ad-campaign/3122758", evidence="Primary (press release) + press",
      notes="$3.4M disclosed; NM State Ethics Commission says the ads were lobbying activity. NPR reports Oracle now says the campus and fuel cells will use about 11 million gallons of recycled non-potable water."),
 dict(id="US-26", region="US", place="Phoenix area, AZ", sponsor="Project 48 Arizona", sponsor_type="Advocacy nonprofit", format="Billboards",
      title="Pro-data center billboard campaign", date="Sep 2026", claim_type="Water + Energy",
      claim="Data centers \"only account for .15% of Arizona's annual water use\" (founder); nearby site \"uses a closed-loop system\"", verbatim="Quoted by press (founder, not billboard text)",
      url_primary="", url_source="https://www.abc15.com/news/local-news/new-arizona-billboards-defend-data-centers", evidence="Reported by press",
      notes="Says it is self-funded, with no data center company money. Co-founder Stephen Richer cited 0.8% if every proposed Phoenix project were built. Billboard text not yet captured."),
 dict(id="US-27", region="US", place="Northwest & Central Ohio (New Albany)", sponsor="Meta", sponsor_type="Hyperscaler", format="Facebook/Instagram ads",
      title="'We don't just build here. We invest here.' (meta.com/buildingohio)", date="Aug 26 – Oct 2026", claim_type="None (investment, community)",
      claim="\"Meta is investing more than $1 billion in Northwest Ohio\"; no energy or water claim in the ad text", verbatim="Verbatim (Meta Ad Library)",
      url_primary="https://www.facebook.com/ads/library/?id=1067460622353986", url_source="", evidence="Primary (Meta Ad Library)",
      notes="Check the landing page (meta.com/buildingohio) for water and energy claims."),
 dict(id="US-28", region="US", place="Mount Pleasant, WI", sponsor="Microsoft", sponsor_type="Hyperscaler", format="Launch blog / video",
      title="Fairwater AI datacenter launch", date="Sep 18 2025", claim_type="Energy + Water",
      claim="Closed-loop liquid cooling for 90%+ of the site, \"zero water waste\"; water use like a typical restaurant's per year; pre-paying for energy infrastructure",
      verbatim="Quoted by press", url_primary="", url_source="https://www.datacenterdynamics.com/en/news/microsoft-increases-wisconsin-data-center-investment-to-73bn-says-fairwater-site-will-be-worlds-most-powerful-data-center/",
      evidence="Reported by press", notes="PR, not a paid ad. Related: Milwaukee Riverkeeper public-records suit (L-05)."),
 dict(id="US-29", region="US", place="Memphis, TN", sponsor="xAI (SpaceXAI) / Greater Memphis Chamber", sponsor_type="AI company", format="Announcements / chamber materials",
      title="Colossus Water Recycling Plant promise", date="2025 – 2026", claim_type="Water",
      claim="$80M plant to recycle up to 13M gallons/day of wastewater, sparing the Memphis Sand Aquifer", verbatim="Paraphrase",
      url_primary="https://memphischamber.com/?p=89051", url_source="https://www.fox13memphis.com/news/why-did-xai-pause-construction-of-wastewater-treatment-plant/article_de21744c-bf87-4691-b79e-3cc0ff342ed8.html",
      evidence="Primary (chamber page) + press", notes="Construction was paused in 2026; a restart is reported for Q1 2027. A promise vs. delivery case."),
 dict(id="US-30", region="US", place="National (TV, social)", sponsor="Liquid Death + Garage Beer (Jason Kelce)", sponsor_type="Consumer brand (counter-ad)", format="Video ad + social",
      title="'We Want Your Pee' / 'Data Center Coolant'", date="Aug 2026", claim_type="Water (counter-claim)",
      claim="Parody: data centers \"use millions of gallons of water to cool servers\"", verbatim="Verbatim (Meta Ad Library)",
      url_primary="https://www.facebook.com/ads/library/?id=2054840681894781", url_source="https://www.adweek.com/?p=1956109", evidence="Primary (Meta Ad Library) + press",
      notes="Agency: LD Death Machine. Counter-ad category."),
 dict(id="US-31", region="US", place="National (Chrome plug-in promo)", sponsor="Planet Water Foundation / TBWA\\SMP", sponsor_type="Nonprofit (counter-ad)", format="Facebook ads",
      title="'Bottle It Back'", date="May 2026", claim_type="Water (counter-claim)",
      claim="\"AI data centers rely on water for cooling\"; converts AI use into water donations", verbatim="Verbatim (Meta Ad Library)",
      url_primary="https://www.facebook.com/ads/library/?id=953059753993074", url_source="", evidence="Primary (Meta Ad Library)", notes="Counter-ad / awareness category."),
]
ads.extend(new_ads)

# extra YouTube videos (QTS, Texans for Economic Liberty)
extra_vids = [
 ("Is8QA48A_kk","QTS (national)","QTS Data Centers","Saving Nearly 1.5 Billion Gallons a Year with a Closed-Loop Cooling System","Water",30,98234,"2026-04-10",10,"2026-03-18","2026-10-29","Title claim: \"Saving Nearly 1.5 Billion Gallons a Year\" (no captions; on-screen text)"),
 ("ta3HhLRdt_E","QTS (national)","QTS Data Centers","Saving Nearly 1.5 Billion Gallons a Year Through Smarter Cooling","Water",30,53891,"2026-04-10",1,"2026-03-18","2026-10-29","Title claim: \"Saving Nearly 1.5 Billion Gallons a Year\" (no captions)"),
 ("CADpCqrdeLg","QTS (national)","QTS Data Centers","Nearly 1.5 Billion Gallons Saved Each Year Through Closed-Loop Innovation","Water",15,22337,"2026-04-10",1,"2026-04-29","2026-10-29","Title claim (no captions)"),
 ("2sLdcb9jjFU","QTS (national)","QTS Data Centers","QTS Community Commitments","General",84,164811,"2026-03-09",7,"2026-05-20","2026-10-30",""),
 ("6ILMVNmcEn0","QTS (national)","QTS Data Centers","QTS and the Southern Conservation Trust","General",127,153144,"2026-04-23",3,"2026-05-22","2026-10-30",""),
 ("XTsm24wKu_I","Texas","Texans for Economic Liberty","How Data Centers Benefit Texas","Water",30,1507611,"2026-05-12",3,"2026-05-19","2026-08-01","\"golf courses use more water each year than data centers\"; \"many new data centers now use zero water for cooling\""),
 ("dyhMX1Gt3OA","Texas","Texans for Economic Liberty","Data Centers Protect National Security","General",15,2012854,"2026-05-26",3,"2026-05-26","2026-08-01",""),
]
for (vid,st,ch,t,tp,ln,vw,pub,n,f,l,cl) in extra_vids:
    videos.append(dict(youtube_id=vid,state=st,channel=ch,title=t,topic=tp,length_sec=ln,views=vw,published=pub,
        google_ads_creatives=n,google_ads_first_shown=f,google_ads_last_shown=l,key_claim=cl,transcribed='yes' if cl else 'no',
        youtube_url=f"https://www.youtube.com/watch?v={vid}",advertiser=("QTS Realty Trust, LLC (verified Google advertiser)" if ch.startswith("QTS") else "Texans for Economic Liberty (verified Google advertiser)")))
# fill missing advertiser for America Connects channels
ac = {"Virginia Connects","Texas Connects","NC Connects","OR Connects","Pennsylvania Connects","Connected OH","IN Connects","ConnectedGA","Louisiana Connects"}
for v in videos:
    if not v.get('advertiser') and v['channel'] in ac:
        v['advertiser'] = "America Connects (state channel; video not seen in Google ads Jul–Oct 2026 window)"
videos.sort(key=lambda x: (x['state'], x['topic'], -int(x['views'])))

# Meta table: merge new
nm = json.load(open(os.path.join(B, 'new_meta.json')))
for m in nm: m['url'] = f"https://www.facebook.com/ads/library/?id={m['library_id']}"
have = {m['library_id'] for m in meta}
meta.extend([m for m in nm if m['library_id'] not in have])
meta_counts += [("QTS Data Centers","~10 on Meta; ~95 on Google"),("Texans for Economic Liberty","~15 data center ads on Meta; 21 on Google"),
                ("Michigan for Responsible Data Centers","~10 creatives"),("Meta (Ohio 'Building here')","5+ creatives")]

law.append(dict(id="L-09", type="Regulatory disclosure (lobbying)", title="NM State Ethics Commission: Project Jupiter ad campaign", jurisdiction="New Mexico", filed="2026",
    parties="Project Jupiter (Oracle/Stargate partners)", claims_challenged="The $3.4M ad campaign (water, energy and economic claims) was classified as lobbying activity and disclosed.",
    status="Commission calls it likely the largest lobbying advertising campaign ever disclosed in New Mexico.", url="https://www.abqjournal.com/news/project-jupiter-files-disclosures-over-34m-ad-campaign/3122758", links_to="US-25"))
