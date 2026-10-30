# v1.0 gap-filling (Oct 30, 2026): Bloom Energy, more counter-ads, outside-US ads, transcripts found after the audit.
ads.extend([
 dict(id="OI-05", region="US", place="National (Google Search)", sponsor="Bloom Energy", sponsor_type="Fuel cell maker",
      format="Google search ads", title="'Bloom Energy for Data Centers - Onsite Power for Data Centers'", date="2024 – Oct 2026", claim_type="Energy",
      claim="\"Onsite Power for Data Centers\"; \"Renewable Energy Microgrids\"; fuel cells that \"Lower Emissions. Move Towards Zero Carbon\"; \"Generate onsite electricity without combustion using natural gas, biogas or hydrogen\"",
      verbatim="Verbatim (Google Ads Transparency ad previews, read Oct 30, 2026)", url_primary="https://adstransparency.google.com/advertiser/AR17124372949495709697?region=US",
      url_source="", evidence="Primary (Google Ads Transparency)",
      notes="Fuel-cell maker whose servers power data centers including Oracle's Project Jupiter plan and Equinix sites. 36 Google ads, mostly search text ads; no data-center Meta ads found."),
 dict(id="GL-13", region="Global", place="Australia", sponsor="AirTrunk", sponsor_type="Data center operator",
      format="Facebook/Instagram ads", title="'Water use is a fair question'", date="Oct 2026 (running)", claim_type="Water",
      claim="\"Using dry air cooling in a closed loop… there's no added pressure on local water resources\"",
      verbatim="Verbatim (Meta Ad Library, AU)", url_primary="https://www.facebook.com/ads/library/?id=1810827893585871", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Hyperscale operator owned by Blackstone. The ad ran without an issue-ad label."),
 dict(id="GL-14", region="Global", place="Canada (Alberta)", sponsor="Government of Alberta", sponsor_type="Government",
      format="Facebook/Instagram ads", title="Alberta's data centre approach", date="Sep – Oct 2026", claim_type="Energy + Water",
      claim="\"Alberta's approach limits data centres to industrial zones, puts them last for water and makes them supply their own power\"",
      verbatim="Verbatim (Meta Ad Library, CA)", url_primary="https://www.facebook.com/ads/library/?id=1601780274686250", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Provincial government ad (CA$10K–15K, over 1M impressions). 'Supply their own power' mostly means on-site gas plants."),
 dict(id="GL-15", region="Global", place="Canada (Saskatchewan)", sponsor="Saskatchewan Party Caucus (Premier Scott Moe)", sponsor_type="Political (supporting)",
      format="Facebook/Instagram ads", title="'Home ice matters': Bell data centre", date="Sep 2026", claim_type="National security",
      claim="Bell's data centre near Regina \"will create thousands of good paying jobs\" and is \"about building to protect Canada's data sovereignty\"",
      verbatim="Verbatim (Meta Ad Library, CA)", url_primary="https://www.facebook.com/ads/library/?id=1071752032382332", url_source="",
      evidence="Primary (Meta Ad Library)", notes="The 'data sovereignty' frame parallels US ads about keeping data from China."),
 dict(id="GL-16", region="Global", place="UK, Australia, Canada", sponsor="Environmental groups and candidates abroad", sponsor_type="Political (opposing)",
      format="Facebook/Instagram ads", title="Counter-ads outside the US", date="Aug – Oct 2026", claim_type="Water + energy (counter-claim)",
      claim="Data centres \"competing with [communities] for limited water and energy\" (Friends of the Earth, UK); \"will guzzle our water\" (Environment Centre NT, Australia); \"big power bill hikes\" (Nova Scotia NDP)",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=2172889726617169", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Includes Australian Greens petitions for a data-centre moratorium and Toronto mayoral ads."),
])

def _m(spend, imp): return "; ".join(x for x in (spend, (imp + " impressions") if imp else "") if x)
new_meta6 = [
 ("Earthjustice (counter-ad)","Mississippi","1730516554619571","Started 7 May 2026",_m("$7K–$8K","200K–250K"),"Energy (counter-claim)","xAI is \"illegally polluting nearby communities in Southaven, Mississippi\" to power Grok."),
 ("Earthjustice (counter-ad)","Mississippi","4301839766740670","Started 14 Apr 2026",_m("$1K–$1.5K","250K–300K"),"Energy (counter-claim)","\"We're suing… xAI, for building an illegal power plant in Mississippi to fuel its data center.\""),
 ("Earthjustice (counter-ad)","Mississippi","1511733583996891","Started 16 Apr 2026",_m("$5K–$6K","125K–150K"),"Energy (counter-claim)","Same xAI Southaven message (third of about a dozen placements)."),
 ("NRDC (counter-ad)","US (national)","1641018310411783","Started 3 Feb 2026",_m("$3K–$3.5K","600K–700K"),"Energy (counter-claim)","Creator video: \"AI is frying our planet.\""),
 ("Montana Conservation Voters (counter-ad)","Montana","1048346007649229","Started 13 Jul 2026",_m("$700–$799","70K–80K"),"Energy (counter-claim)","A 5,000-acre data center near Broadview \"could demand 10 times the power\" of current county use."),
 ("Williams Companies","US (national)","1400627271367785","Started 10 Mar 2026",_m("$800–$899","90K–100K"),"Energy","CEO on Fox Business on \"powering the AI-driven economy\" with gas infrastructure."),
 ("AirTrunk","Australia","1810827893585871","Started 14 Oct 2026","","Water","\"Dry air cooling in a closed loop… there's no added pressure on local water resources\" (no issue-ad label)."),
 ("Government of Alberta","Canada (Alberta)","1601780274686250","14 Sep – 10 Oct 2026",_m("CA$10K–CA$15K",">1M"),"Energy + Water","Data centres limited \"to industrial zones\", \"last for water\" and must \"supply their own power\"."),
 ("Saskatchewan Party Caucus","Canada (Saskatchewan)","1071752032382332","18 – 26 Sep 2026",_m("CA$100–CA$199","60K–70K"),"National security","Bell data centre: \"thousands of good paying jobs\"; \"protect Canada's data sovereignty\"."),
 ("Friends of the Earth (counter-ad)","United Kingdom","2172889726617169","28 Aug – 17 Sep 2026",_m("£2K–£2.5K","350K–400K"),"Water + energy (counter-claim)","Data centres \"competing with [communities] for limited water and energy supplies\"; petition to pause expansion."),
 ("Environment Centre NT (counter-ad)","Australia","2012700756027978","11 Aug – 18 Oct 2026",_m("AU$2.5K–AU$3K",">1M"),"Water (counter-claim)","\"These data centres will guzzle our water and fast-track the fracking of our underground reservoirs.\""),
 ("Katherine Copsey, Greens (counter-ad)","Australia","1617839936414098","Started 16 Sep 2026",_m("AU$4K–AU$4.5K","100K–125K"),"Water + energy (counter-claim)","\"AI data centres use massive amounts of water and energy. We need to pause.\""),
 ("Nova Scotia NDP (counter-ad)","Canada (Nova Scotia)","3082818265257315","Started 23 Oct 2026",_m("CA$300–CA$399","45K–50K"),"Energy (counter-claim)","\"Big data centres could mean big power bill hikes for Nova Scotians.\""),
 ("Olivia Chow for Mayor (counter-ad)","Canada (Toronto)","1790561518818248","21 – 27 Oct 2026",_m("CA$1.5K–CA$2K","125K–150K"),"Energy (counter-claim)","\"Brad Bradford wants data centres in Toronto.\""),
]
for (sp,st,lid,dt,spend,ct,tx) in new_meta6:
    if lid not in {m['library_id'] for m in meta}:
        meta.append(dict(sponsor=sp,state=st,library_id=lid,dates=dt,spend=spend,claim_type=ct,text=tx,url=f"https://www.facebook.com/ads/library/?id={lid}"))

# transcripts read after the audit
TX_NEW = {
 "-AOJOKtomfE": "\"We'll pay our own way on electricity, not shift costs onto Michigan families\"; closed-loop air cooling uses \"less water than it would take to farm the land\"",
 "q7deAI_ooMI": "Materials from across the country; \"re-energizing manufacturing and creating thousands of American jobs\"",
 "jgoi3ilu0mo": "\"An independent study confirmed that across the nation, data centers are paying their own energy costs\"; they \"may even help lower rates for everyone\"",
}
for v in videos:
    if v["youtube_id"] in TX_NEW: v["key_claim"] = TX_NEW[v["youtube_id"]]; v["transcribed"] = "yes"

for a in ads:
    if a["id"] == "US-29":
        a["notes"] = (a.get("notes") or "") + " Earthjustice ran about a dozen Meta ads (Apr–May 2026) on its suit over xAI's Southaven, Mississippi power plant."
meta_counts += [("Bloom Energy", "36 Google ads (search ads for data-center onsite power); no data-center Meta ads found"),
                ("Outside the US (sweep, Oct 30, 2026)", "AirTrunk (AU), Government of Alberta, Saskatchewan Party; counter-ads in the UK, Australia and Canada")]
