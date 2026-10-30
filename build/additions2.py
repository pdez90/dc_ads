# v0.6 additions (Oct 30, 2026): ads found via Google Ads Transparency advertiser search and Meta sweeps.
ads.extend([
 dict(id="US-32", region="US", place="Texas (YouTube / Google video ads)", sponsor="Texas Connects (America Connects network)", sponsor_type="Industry trade group",
      format="YouTube / Google video ad (30s)", title="'Built For Texas'", date="Apr – Aug 2026", claim_type="Energy + Water",
      claim="New technology means data centers \"consume minimal water while funding new power generation for everyone\"; taxes \"can lower your bills\"",
      verbatim="Verbatim (YouTube captions)", url_primary="https://www.youtube.com/watch?v=IwQCwpzG_GY",
      url_source="https://adstransparency.google.com/advertiser/AR03648286654495457281?region=US", evidence="Primary (Google Ads Transparency + YouTube)",
      notes="Separate verified Google advertiser 'Texas Connects' (16 video ads, Apr 16 – Aug 1, 2026). 12.2M YouTube views, the most-viewed ad in the archive."),
 dict(id="US-33", region="US", place="Oregon (YouTube / Google video ads)", sponsor="Oregon Connects (America Connects network)", sponsor_type="Industry trade group",
      format="YouTube / Google video ads (30s, 15s)", title="'What Matters Most'", date="May – Sep 2026", claim_type="Energy",
      claim="\"An independent study confirmed\" data centers nationally \"are paying their own energy costs\"; may \"help lower rates for everyone\"",
      verbatim="Verbatim (YouTube captions)", url_primary="https://www.youtube.com/watch?v=L-g5j8Dah_o",
      url_source="https://adstransparency.google.com/advertiser/AR07874741731701293057?region=US", evidence="Primary (Google Ads Transparency + YouTube)",
      notes="Ran while Oregon regulators were implementing the 2025 POWER Act. In July 2026 they approved a 29.7% rate increase for PGE's data-center class and a 1.3% cut for homes. The 'independent study' is not named in the ad."),
 dict(id="US-34", region="US", place="National; Leesburg, VA; Red Oak, TX; Meridian, MS", sponsor="Compass Datacenters", sponsor_type="Operator",
      format="Facebook/Instagram + YouTube reels ('We Agree'), YouTube video", title="'We Agree' campaign + 'The Legacy Lie About Data Center Water Use'", date="Aug – Oct 2026",
      claim_type="Energy + Water",
      claim="\"Since 2011, Compass has used zero city water for cooling\"; \"Compass pays its own way\" with \"more than $300 million\" for substations and transmission; water video says community systems \"leak more in one day than Compass would use in a year\"",
      verbatim="Verbatim (Meta Ad Library; YouTube captions)", url_primary="https://www.facebook.com/ads/library/?id=1007646302344543",
      url_source="https://adstransparency.google.com/advertiser/AR18151846499565174785?region=US", evidence="Primary (Meta Ad Library + Google Ads Transparency + YouTube)",
      notes="About 155 Google ads since 2024 (image, text and video). The Oct 2026 'We Agree' Meta ads ran without an issue-ad label, so Meta publishes no payer, spend or audience."),
 dict(id="US-35", region="US", place="Douglas County (GA), Indiana, Missouri, Ohio, Texas, Virginia", sponsor="Google", sponsor_type="Hyperscaler",
      format="YouTube video ads + 171 display banners (datacenters.google)", title="'Investing in [community]' and 'Empowering the Future of Electrical Workers'", date="Sep 3 – Oct 1, 2026",
      claim_type="None (jobs, community grants)",
      claim="Community grants and electrician training (\"training thousands of local electricians\"); no energy or water claim in the ads",
      verbatim="Verbatim (banner, captions)", url_primary="https://www.youtube.com/watch?v=IQqPY39Vpes",
      url_source="https://adstransparency.google.com/?region=US&domain=datacenters.google", evidence="Primary (Google Ads Transparency + YouTube)",
      notes="191 Google ads pointing to datacenters.google. The banner file names show versions made for Texas, Ohio and Virginia. Included because it's a data-center image campaign, even though it makes no energy or water claim."),
 dict(id="US-36", region="US", place="Wyoming", sponsor="Wyoming Driven Innovation", sponsor_type="Advocacy group",
      format="Facebook/Instagram ads", title="'Empowering Wyoming's data economy'", date="Sep – Oct 2026", claim_type="Energy",
      claim="Data centers could \"create a new demand for Wyoming's energy\"; \"leading in energy, innovation and responsible growth\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1821241565897458", url_source="",
      evidence="Primary (Meta Ad Library)", notes="New pro-data-center group (Wyoming Driven Innovation LLC). One ad quotes Compass Datacenters' CEO. Funders not disclosed."),
 dict(id="US-37", region="US", place="OR, OH, MI, TX, GA, AK, MT and other 2026 races", sponsor="Candidates, PACs and advocacy groups (e.g., Friends of Tina Kotek, Evergreen Action, Duty and Country, Run For Something PAC)",
      sponsor_type="Political (opposing)", format="Facebook/Instagram ads", title="2026 election ads attacking data centers",
      date="Aug – Oct 2026", claim_type="Energy + Water (counter-claim)",
      claim="Data centers \"push our energy bills higher\", are \"taking our water\"; Oregon's POWER Act \"stops data centers from passing their energy costs onto you\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1118435840747957", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Dozens of 2026 midterm ads, mostly attacking opponents over data centers, bills and water. A sample is in the Meta tab."),
])

extra_vids2 = [
 ("IwQCwpzG_GY","Texas","Texas Connects","Built For Texas","Energy + Water",30,12221296,"2026-04-16","","2026-04-16","2026-08-01","\"consume minimal water while funding new power generation for everyone\"","Texas Connects (verified Google advertiser)"),
 ("L-g5j8Dah_o","Oregon","Oregon Connects","What Matters Most","Energy",30,4026620,"2026-05-04","","2026-05-06","2026-09-01","\"An independent study confirmed\"… data centers \"are paying their own energy costs\"","Oregon Connects (verified Google advertiser)"),
 ("F-lA8tM5ytg","Oregon","OR Connects","Oregon Connects - What Matters Most - 15","Energy",15,2024635,"2026-07-14","","2026-05-06","2026-09-01","","Oregon Connects (verified Google advertiser)"),
 ("0JS96iU0k0o","Virginia","Compass Datacenters","The \"Legacy Lie\" About Data Center Water Use — Debunked by Water Expert","Water",177,4466,"2026-08-17","","","","Community systems \"leak more in one day than Compass would use in a year\"","Compass Datacenters, LLC (verified Google advertiser)"),
 ("XNaTFb_tYXM","US (national)","Compass Datacenters","WeAgree_Water_Reel_Ad_Final_V3","Water",15,1006,"2026-10-05","","","","'We Agree' water reel (no captions); Meta version: \"zero city water for cooling\"","Compass Datacenters, LLC (verified Google advertiser)"),
 ("Cwh4o5H-rtU","US (national)","Compass Datacenters","WeAgree_Rates_Reel_Ad_Final","Energy",16,169,"2026-10-05","","","","'We Agree' rates reel (no captions); Meta version: \"Compass pays its own way\"","Compass Datacenters, LLC (verified Google advertiser)"),
 ("IQqPY39Vpes","Georgia","Google","Investing in Douglas County","None (jobs, taxes)",15,1773098,"2026-08-31","","2026-09-03","2026-10-01","","Google LLC (verified Google advertiser)"),
 ("Li0ap16ReOQ","Texas","Grow with Google","Empowering the Future of Electrical Workers - TX","None (jobs, taxes)",30,1823063,"2026-07-30","","2026-09-03","2026-10-01","","Google LLC (verified Google advertiser)"),
]
for (vid,st,ch,t,tp,ln,vw,pub,n,f,l,cl,adv) in extra_vids2:
    videos.append(dict(youtube_id=vid,state=st,channel=ch,title=t,topic=tp,length_sec=ln,views=vw,published=pub,
        google_ads_creatives=n,google_ads_first_shown=f or None,google_ads_last_shown=l or None,key_claim=cl,transcribed='yes' if cl and 'no captions' not in cl else 'no',
        youtube_url=f"https://www.youtube.com/watch?v={vid}",advertiser=adv))
videos.sort(key=lambda x: (x['state'], x['topic'], -int(x['views'])))

new_meta2 = [
 ("Compass Datacenters","US (national)","1007646302344543","Started 18 Oct 2026","","Water","\"Data centers shouldn't use your water. We agree.\" Claims \"zero city water for cooling\" since 2011."),
 ("Compass Datacenters","US (national)","1442097564548229","Started 18 Oct 2026","","Energy (costs)","\"Data centers shouldn't raise electricity rates. We agree.\" Cites \"more than $300 million\" for substations and lines."),
 ("Compass Datacenters","US (national)","1927445971757558","Started 18 Oct 2026","","None (jobs)","'We Agree' jobs ad: development should create lasting careers."),
 ("Wyoming Driven Innovation","Wyoming","1821241565897458","28 Sep – 15 Oct 2026","$200–$299","Energy","Data centers need \"more reliable energy\"; Wyoming \"has powered America for generations\"."),
 ("Friends of Tina Kotek (counter-ad)","Oregon","1118435840747957","Aug – Oct 2026","$25K–$30K","Energy (counter-claim)","POWER Act \"stops data centers from passing their energy costs onto you\"."),
 ("Evergreen Action (counter-ad)","Michigan","2266859057417720","Aug – Oct 2026","","Energy (counter-claim)","\"Data centers use as much electricity as entire cities\"; \"Don't Pay Big Tech's Bill\"."),
 ("Duty and Country (counter-ad)","Ohio","2082368675714884","Oct 2026","","Energy (counter-claim)","Attacks Sen. Husted for championing AI data centers \"driving up our electric bills\"."),
 ("Georgia Conservation Voters (counter-ad)","Georgia","2113109242626847","Oct 2026","$9K–$10K","Energy (counter-claim)","PSC candidates support data centers \"that raise our bills\"."),
 ("Tucker for Texas (counter-ad)","Texas","1674139377577442","Started 27 Oct 2026","<$100","Water + energy (counter-claim)","\"AI data centers are taking our water and jacking up our power bills\"."),
 ("Run For Something PAC (counter-ad)","US","1116433990767657","Started 26 Oct 2026","$900–$999","Energy (counter-claim)","\"Data centers are driving up our energy bills, wrecking our environment\"."),
 ("Alaskans for Mary (counter-ad)","Alaska","1481236440573506","Started 26 Oct 2026","","Water (counter-claim)","Quotes Sen. Sullivan inviting data centers: \"we got water\"; says those resources belong to Alaskans."),
]
for (sp,st,lid,dt,spend,ct,tx) in new_meta2:
    if lid not in {m['library_id'] for m in meta}:
        meta.append(dict(sponsor=sp,state=st,library_id=lid,dates=dt,spend=spend,claim_type=ct,text=tx,url=f"https://www.facebook.com/ads/library/?id={lid}"))
meta_counts += [("Compass Datacenters","4 on Meta ('We Agree', Oct 2026); ~155 on Google"),("Wyoming Driven Innovation","9"),
                ("Google LLC (datacenters.google)","191 on Google (Sep 3 – Oct 1, 2026)")]
