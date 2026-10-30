# v0.7 (Oct 30, 2026): "Nuclear industry" category — nuclear-themed ads that tie nuclear power to data centers or AI.
ads.extend([
 dict(id="NU-01", region="US", place="National (YouTube, Google, Meta)", sponsor="Nuclear Energy Institute (NEI)", sponsor_type="Nuclear industry",
      format="YouTube / Google video ads + Facebook/Instagram ads", title="'Nuclear Makes It Happen' and 'Electricity Demand Is Now Surging'", date="2023 – Oct 2026",
      claim_type="Energy",
      claim="Data center electricity use \"expected to double by 2030\" globally and \"triple\" in the US; nuclear is \"the only source that's both clean and reliable\"; AI spot: nuclear powers \"billions of devices\"",
      verbatim="Verbatim (YouTube captions; Meta Ad Library)", url_primary="https://www.youtube.com/watch?v=4GwRC82WLzs",
      url_source="https://adstransparency.google.com/advertiser/AR05636844967671365633?region=US", evidence="Primary (Google Ads Transparency + YouTube + Meta Ad Library)",
      notes="Nuclear industry trade group. 75 Google ads since Jul 2024 (53 video), still running in Oct 2026. Earlier Meta ads (2023–24) boosted coverage of Microsoft's interest in nuclear for AI data centers."),
 dict(id="NU-02", region="US", place="National (Meta)", sponsor="Nuclear Matters", sponsor_type="Nuclear industry",
      format="Facebook/Instagram video ads", title="Nuclear for AI and data centers", date="Mar – Sep 2025", claim_type="Energy",
      claim="\"Investments in nuclear energy are powering America's data centers, meeting AI's growing demands\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1628561594449326", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Pro-nuclear advocacy campaign. A second ad pitches nuclear careers as AI drives energy demand."),
 dict(id="NU-03", region="US", place="National; Pennsylvania (Three Mile Island / Crane)", sponsor="Constellation Energy", sponsor_type="Nuclear industry",
      format="YouTube / Google video ads (incl. 'Clean Jobs for Pennsylvania' channel)", title="'We Bring The Energy' and Three Mile Island restart spots", date="Jun 2025 – Oct 2026",
      claim_type="Energy",
      claim="\"Nation's largest producer of clean and reliable American-made energy\", powering \"the biggest data centers\" with \"emissions free electricity\"",
      verbatim="Verbatim (YouTube captions)", url_primary="https://www.youtube.com/watch?v=TsiNMFTxjF0",
      url_source="https://adstransparency.google.com/advertiser/AR16739891918153973761?region=US", evidence="Primary (Google Ads Transparency + YouTube)",
      notes="About 33 Google ads across four Constellation accounts. One account also pays for a 'Clean Jobs for Pennsylvania' channel featuring Three Mile Island workers; those spots don't mention that the Crane restart will supply Microsoft data centers."),
])

extra_vids3 = [
 ("Io7h_19LHWE","US (national)","Nuclear Energy Institute","Nuclear Makes It Happen","Energy",30,2033512,"2025-04-27","Nuclear powers \"billions of devices\" … \"OH, hello AI\"; \"Nuclear makes it happen\""),
 ("ffDG_n1zcis","US (national)","Nuclear Energy Institute","Nuclear Makes It Happen","Energy",30,867315,"2025-04-27",""),
 ("oThjI485c3U","US (national)","Nuclear Energy Institute","Nuclear Makes It Happen","Energy",15,314871,"2025-04-22",""),
 ("4GwRC82WLzs","US (national)","Nuclear Energy Institute","Electricity Demand Is Now Surging","Energy",30,2745,"2026-06-10","Data center electricity use \"expected to double by 2030\" globally, US \"expected to triple\""),
 ("TsiNMFTxjF0","US (national)","Constellation","We Bring The Energy","Energy",32,641876,"2025-06-09","Powering \"the biggest data centers\" by \"generating emissions free electricity\""),
 ("1zTYeqE1VVc","US (national)","Constellation","we bring the energy 15 spot","Energy",15,1835610,"2026-02-24","\"The nation's largest producer of clean and reliable American-made energy\""),
 ("bj9dZxbgKu0","Pennsylvania","Clean Jobs for Pennsylvania","A Legacy Pennsylvanians Built","None (jobs, taxes)",28,46253,"2025-10-29","Three Mile Island worker's family story (jobs)"),
 ("zu_AH_cVtLk","Pennsylvania","Clean Jobs for Pennsylvania","Step Into the Control Room","None (jobs, taxes)",17,56948,"2025-10-29",""),
]
for (vid,st,ch,t,tp,ln,vw,pub,cl) in extra_vids3:
    adv = "Nuclear Energy Institute (verified Google advertiser)" if ch.startswith("Nuclear") else "Constellation Energy Corporation (verified Google advertiser)"
    videos.append(dict(youtube_id=vid,state=st,channel=ch,title=t,topic=tp,length_sec=ln,views=vw,published=pub,
        google_ads_creatives="",google_ads_first_shown=None,google_ads_last_shown=None,key_claim=cl,transcribed='yes' if cl else 'no',
        youtube_url=f"https://www.youtube.com/watch?v={vid}",advertiser=adv))
videos.sort(key=lambda x: (x['state'], x['topic'], -int(x['views'])))

new_meta3 = [
 ("Nuclear Energy Institute","US (national)","1669008000286846","13 Oct – 3 Nov 2023","$1.5K–$2K; 100K–125K impressions","Energy","Boosted Business Insider story: why Microsoft \"may look to nuclear energy to power its AI data centers\"."),
 ("Nuclear Energy Institute","US (national)","374094262207192","23 Mar – 12 Apr 2024","$700–$799; 125K–150K impressions","Energy","\"From data centers to industrial companies\", major players are \"looking to nuclear technologies\"."),
 ("Nuclear Matters","US (national)","1628561594449326","11 – 16 Mar 2025","$400–$499; 80K–90K impressions","Energy","Nuclear investments are \"powering America's data centers, meeting AI's growing demands\"."),
 ("Nuclear Matters","US (national)","805063845222669","22 – 29 Sep 2025","","None (jobs)","As AI drives energy demand, pitches careers in nuclear."),
 ("NRDC (counter-ad)","Georgia","927526629754689","3 Feb – 1 Apr 2026","","Energy + Water (counter-claim)","Data centers are \"pulling more power than nuclear reactors\" and \"swallowing millions of gallons of water a day\"."),
 ("West Virginia Democratic Party (counter-ad)","West Virginia","1120880277181055","Started 16 Oct 2026","$1.5K–$2K; 400K–450K impressions","Energy (counter-claim)","15s attack ads on legislative candidates: \"blank checks for AI data centers\" (multiple versions; on-screen text only)."),
]
for (sp,st,lid,dt,spend,ct,tx) in new_meta3:
    if lid not in {m['library_id'] for m in meta}:
        meta.append(dict(sponsor=sp,state=st,library_id=lid,dates=dt,spend=spend,claim_type=ct,text=tx,url=f"https://www.facebook.com/ads/library/?id={lid}"))
meta_counts += [("Nuclear Energy Institute","75 on Google (Jul 2024 – Oct 2026); data-center-themed Meta ads 2023–24"),
                ("Nuclear Matters","2 data-center/AI-themed Meta ads (2025)"),
                ("Constellation Energy","~33 on Google across 4 accounts, incl. 'Clean Jobs for Pennsylvania'")]
