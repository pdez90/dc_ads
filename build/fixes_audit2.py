# v0.9 audit (Oct 30, 2026): every Meta ad re-read from the Ad Library; every YouTube video re-read.
# 1) corrections to stored Meta rows; 2) ads found in a fresh sweep; 3) new campaigns and videos.

# ---------------------------------------------------------------- 1) corrections (dates / spend read from each ad)
META_FIX = {
 "1603022260291240": dict(dates="14 Nov 2024 – 6 Feb 2025 (one of 18 versions, Oct 2024 – Mar 2025)", spend="$10K–$15K; >1M impressions"),
 "1355279849204870": dict(dates="25 Apr – 17 Aug 2025", spend="$5K–$6K; 350K–400K impressions"),
 "1108111641257542": dict(dates="16 Dec 2025 – 12 Jan 2026 (video also ran in later versions)", spend="$7K–$8K; >1M impressions"),
 "2102349793504832": dict(spend="$1.5K–$2K; 100K–125K impressions"),
 "1813952416150473": dict(spend="$2K–$2.5K; 150K–175K impressions"),
 "874918655658106": dict(spend="$2K–$2.5K; 500K–600K impressions"),
 "1300660238797502": dict(dates="21 Apr – 30 Jul 2026", spend="$300–$399; 80K–90K impressions"),
 "4368691783381214": dict(spend="$2.5K–$3K; 600K–700K impressions"),
 "946918801539771": dict(dates="21 Apr – 31 Jul 2026", spend="$1.5K–$2K; 500K–600K impressions"),
 "2068150173768978": dict(dates="15 Apr – 23 Jun 2026", spend="$1K–$1.5K; 250K–300K impressions"),
 "1615312140006989": dict(spend="$3.5K–$4K; 900K–1M impressions"),
 "1666489028820952": dict(spend="$2.5K–$3K; 700K–800K impressions"),
 "1086975924010981": dict(spend="$20K–$25K; >1M impressions",
     text="A \"NO\" to data centers means \"fewer union jobs and less tax revenue\"; Illinois towns work with data centers \"to keep water safe, usage low, and costs even lower.\""),
 "1821241565897458": dict(spend="$200–$299; 15K–20K impressions",
     text="\"Wyoming has powered America for generations\"; as AI and cloud computing \"require more reliable energy\", Wyoming \"is ready to help power what comes next.\""),
 "1118435840747957": dict(dates="9 – 24 Sep 2026", spend="$25K–$30K; 800K–900K impressions"),
 "2266859057417720": dict(dates="13 Aug – 4 Sep 2026", spend="$7K–$8K; >1M impressions"),
 "2082368675714884": dict(dates="2 – 8 Oct 2026", spend="$40K–$45K; >1M impressions"),
 "2113109242626847": dict(dates="Started 7 Oct 2026", spend="$9K–$10K; 800K–900K impressions"),
 "1674139377577442": dict(spend="<$100; 5K–6K impressions"),
 "1116433990767657": dict(spend="$900–$999; 30K–35K impressions"),
 "1481236440573506": dict(spend="$1K–$1.5K; 35K–40K impressions"),
 "805063845222669": dict(spend="$300–$399; 60K–70K impressions"),
 "927526629754689": dict(spend="$2K–$2.5K; 350K–400K impressions"),
 # dynamic (DCO) ads: card text now read
 "1384001292758929": dict(state="Georgia", text="\"Stop burning fossil fuels for data centers\": Georgia Power is \"breaking its promises to retire coal plants\"."),
 "1434338615267432": dict(text="Georgia Power is raising bills \"to prop up old coal plants and overbuild expensive gas plants, largely to power data centers\"."),
 "1467768011311573": dict(text="\"Trump's coal mandate, the rise of data centers\" and slow clean-energy hookups are \"causing electric bills to skyrocket\"."),
 "1160273426235067": dict(text="\"Data centers can bring GOOD JOBS, property tax relief & energy investment to South Dakota.\""),
 "4266661140310707": dict(text="Pennsylvania's data centers are \"supporting almost 100,000 jobs and thousands of high-wage construction roles\"."),
}
for m in meta:
    if m["library_id"] in META_FIX: m.update(META_FIX[m["library_id"]])

# ---------------------------------------------------------------- 2) campaigns found in the audit sweep
ads.extend([
 dict(id="US-42", region="US", place="Michigan (Saline Township); national", sponsor="Related Companies / Related Digital", sponsor_type="Data center developer",
      format="Facebook/Instagram ads + YouTube/Google video ads", title="Saline Township ('The Barn', for Oracle/OpenAI): 'Our Commitment to Michigan'", date="Jan – Jul 2026",
      claim_type="Energy + Water",
      claim="\"Will pay for 100% of its energy costs, so your bills don't go up\"; grid investments \"will result in $300 million in annual savings for customers\"; closed-loop air cooling \"saves hundreds of millions of gallons of water\"",
      verbatim="Verbatim (Meta Ad Library; YouTube descriptions)", url_primary="https://www.facebook.com/ads/library/?id=1272981641648678",
      url_source="https://adstransparency.google.com/advertiser/AR12516430811110572033?region=US", evidence="Primary (Meta Ad Library + Google Ads Transparency + YouTube)",
      notes="Developer of the 1.4 GW Saline Township campus built for Oracle (with OpenAI), powered by DTE. 30 Meta ads (several over 1M impressions, $9K–$15K each) and 59 Google video ads; its YouTube spots have 1.8M–5.2M views each. Michigan's Attorney General appealed the regulators' approval of the DTE contracts."),
 dict(id="US-43", region="US", place="Illinois (Sangamon County)", sponsor="Springfield Sangamon Growth Alliance", sponsor_type="Local pro-data-center group",
      format="Facebook/Instagram ads", title="CyrusOne Sangamon County data center", date="Mar – Oct 2026 (running)", claim_type="Water + taxes",
      claim="Water use \"comparable to 15 new homes\"; closed-loop cooling \"won't require ongoing water consumption\"; \"nearly $6 million annually in local property taxes\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1351760670154303", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Local economic-development group promoting CyrusOne's project. Several ads ran without an issue-ad label."),
 dict(id="US-44", region="US", place="Illinois (Granite City / Metro East)", sponsor="Southwestern Illinois Coalition for Job Growth", sponsor_type="Local pro-data-center group",
      format="Facebook/Instagram ads", title="'Data center myths'", date="Oct 2026 (running)", claim_type="Water + jobs",
      claim="\"Nationally, golf courses use more water than data centers do on site\"; \"New data centers use closed-loop recycling\"; a large data center \"employs more than 100 full-time workers and supports 150 to 400 more jobs\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=2031856607408530", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Building-trades group; ads cite Granite City's closed-loop cooling requirement."),
 dict(id="US-45", region="US", place="Maryland (Frederick County)", sponsor="Future Ready Frederick", sponsor_type="Local pro-data-center group",
      format="Facebook/Instagram ads + YouTube/Google video ads", title="'Clean Data Centers' support schools and lower taxes", date="Aug – Sep 2026", claim_type="Water + taxes",
      claim="\"Misinformation has been spreading\"; today's data centers \"use advanced technology to reduce water consumption\", \"create high paying local jobs\" and \"generate millions in local tax revenue\"",
      verbatim="Verbatim (Meta Ad Library; YouTube titles)", url_primary="https://www.facebook.com/ads/library/?id=1590508512808580",
      url_source="https://adstransparency.google.com/advertiser/AR11779974830449754113?region=US", evidence="Primary (Meta Ad Library + Google Ads Transparency)",
      notes="Pro-data-center group active during Frederick County's data center fight. Funders not disclosed."),
 dict(id="US-46", region="US", place="Oklahoma", sponsor="Built Here Oklahoma", sponsor_type="Local pro-data-center group",
      format="Facebook/Instagram ads", title="'Data centers are now required to pay their way'", date="Sep – Oct 2026 (running)", claim_type="Energy (costs)",
      claim="\"Oklahomans wanted assurances data centers wouldn't impact ratepayers - now the law ensures they won't\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1754136019201009", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Ten ads, all without an issue-ad label, so Meta shows no payer, spend or audience."),
 dict(id="US-47", region="US", place="Indiana (Northwest)", sponsor="NWI Data Facts", sponsor_type="Local pro-data-center group",
      format="Facebook/Instagram ads", title="Resident testimonials", date="Oct 2026 (running)", claim_type="Jobs + taxes",
      claim="\"Northwest Indiana data centers create new jobs that keep the next generation here\"; a site \"generating millions to fund housing projects\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=1146371605015712", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Most ads ran without an issue-ad label. One features a Loudoun County, Virginia resident."),
 dict(id="US-48", region="US", place="Illinois (DeKalb)", sponsor="Power Connection, IBEW Local 364", sponsor_type="Labor union",
      format="Facebook/Instagram ads", title="Meta DeKalb property taxes", date="Oct 2026 (running)", claim_type="Taxes",
      claim="\"In 2024 Meta's Dekalb Data Center paid 32.1 million in property taxes\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=28792759310375561", url_source="",
      evidence="Primary (Meta Ad Library)", notes="Electricians' union local."),
 dict(id="OI-04", region="US", place="Missouri and national", sponsor="Edison Electric Institute ('We Stand For Energy')", sponsor_type="Electric utility trade group",
      format="Facebook/Instagram ads + YouTube/Google video ads", title="Data centers 'put downward pressure on electric rates'", date="Jun – Sep 2026", claim_type="Energy (costs)",
      claim="Large data centers \"help put downward pressure on electric rates\" by \"spreading system costs across a broader base\"; Missouri law requires them \"to pay their fair share\"",
      verbatim="Verbatim (Meta Ad Library)", url_primary="https://www.facebook.com/ads/library/?id=2358942264597308",
      url_source="https://adstransparency.google.com/advertiser/AR02146186301588635649?region=US", evidence="Primary (Meta Ad Library + Google Ads Transparency)",
      notes="Trade association of investor-owned electric utilities, running ads on its 'We Stand For Energy' page. Its 63 Google ads in 2026 are mostly general grid and lineworker spots."),
])

def _m(spend, imp): return "; ".join(x for x in (spend, (imp + " impressions") if imp else "") if x)
new_meta5 = [
 # Texans for Economic Liberty: remaining Sep–Oct 2026 ads
 ("Texans for Economic Liberty","Texas","2354723418684252","Started 10 Sep 2026",_m("$125K–$150K",">1M"),"Jobs","\"Every groundbreaking means good-paying work for Texas trades.\""),
 ("Texans for Economic Liberty","Texas","1094460799605149","Started 9 Sep 2026",_m("$90K–$100K",">1M"),"Jobs","\"Every data center built in Texas is built by Texans.\""),
 ("Texans for Economic Liberty","Texas","1097501102754397","21 Sep – 16 Oct 2026",_m("$15K–$20K","600K–700K"),"Jobs","Same text (second placement)."),
 ("Texans for Economic Liberty","Texas","2547339009120724","21 Sep – 17 Oct 2026",_m("$30K–$35K",">1M"),"Jobs","Same trades-jobs text (second placement)."),
 ("Texans for Economic Liberty","Texas","1550680310423772","23 – 28 Oct 2026",_m("$15K–$20K","300K–350K"),"Jobs","\"Behind every Texas data center is a welder, electrician or pipefitter earning a good living.\""),
 ("Texans for Economic Liberty","Texas","2862833327433517","21 Sep – 16 Oct 2026",_m("$50K–$60K","300K–350K"),"National security","\"Do you trust China with your data?\" (second placement)."),
 ("Texans for Economic Liberty","Texas","951757917360097","21 Sep – 16 Oct 2026",_m("$60K–$70K","250K–300K"),"National security","Keep data \"out of the hands of hostile foreign nations like China\" (second placement)."),
 ("Texans for Economic Liberty","Texas","2063664707611988","23 – 28 Oct 2026",_m("$45K–$50K","400K–450K"),"National security","Data centers \"keep American data out of the hands of hostile nations.\""),
 ("Texans for Economic Liberty","Texas","1090651106914529","23 – 28 Oct 2026",_m("$40K–$45K","350K–400K"),"National security","Data centers \"keep American data out of the Chinese Communist Party.\""),
 # NetChoice, American Edge: further placements
 ("NetChoice","US (national)","3386975414803944","30 Apr – 6 Jun 2026",_m("$9K–$10K","700K–800K"),"National security","Same 'China is investing trillions' text (second placement)."),
 ("American Edge Project","US (national)","1076917745072871","14 – 20 Sep 2026",_m("$15K–$20K",">1M"),"Jobs","\"Data centers create jobs, benefit local communities, and ensure America wins.\""),
 ("American Edge Project","US (national)","1600467024909948","24 Sep – 5 Oct 2026",_m("$10K–$15K",">1M"),"Jobs","Same text."),
 ("American Edge Project","US (national)","1744760690072742","14 – 21 Sep 2026",_m("$15K–$20K",">1M"),"Jobs","\"America's data center buildout is strengthening local communities.\""),
 ("American Edge Project","US (national)","2182059112743694","24 Sep – 4 Oct 2026",_m("$10K–$15K",">1M"),"Jobs","Same text."),
 ("American Edge Project","US (national)","1742995237835583","22 – 26 Sep 2026",_m("$6K–$7K",">1M"),"Jobs","Same text."),
 # Connects: jobs and tax-revenue ads
 ("Virginia Connects","Virginia","1272138085104271","3 Apr – 16 Jun 2026",_m("$15K–$20K",">1M"),"Jobs","\"Every job inside a Virginia data center supports 3.5 additional jobs.\""),
 ("Virginia Connects","Virginia","825735950567625","3 Apr – 16 Jun 2026",_m("$15K–$20K",">1M"),"Jobs","Same text (second placement)."),
 ("Virginia Connects","Virginia","1333681062048725","29 May – 1 Jul 2026",_m("$7K–$8K",">1M"),"Taxes","\"Virginia's data centers are the engine behind our economy.\""),
 ("Virginia Connects","Virginia","1303405985187214","Started 13 Oct 2026","","Taxes","Data centers \"generate billions of dollars in tax revenue every year\" (no issue-ad label)."),
 ("Connected Ohio","Ohio","1059638200321804","Started 17 Sep 2026","","Taxes","\"Ohio data centers generate nearly $1 billion in tax revenue\" (no issue-ad label)."),
 ("Oregon Connects","Oregon","2591474914616984","Started 22 Sep 2026","","Taxes","\"Oregon data centers generate over $1 billion in tax revenue\" (no issue-ad label)."),
 ("Connected Georgia","Georgia","1760680921635866","Started 23 Sep 2026","","Taxes","\"Georgia data centers generate over $2 billion in tax revenue\" (no issue-ad label)."),
 ("Connected Georgia","Georgia","994343963380862","23 Jun – 1 Sep 2026",_m("$3.5K–$4K","200K–250K"),"Taxes","Data centers contribute \"critical tax revenue\" and support \"high-skilled jobs\". Disclaimer: 'Connected Georgia, a Project of America Connects'."),
 ("Louisiana Connects","Louisiana","1089916010172765","Started 24 Sep 2026","","Taxes","\"Louisiana data centers generate over $300 million in tax revenue\" (no issue-ad label)."),
 ("Pennsylvania Connects","Pennsylvania","2104731653767779","Started 17 Sep 2026","","Taxes","\"Pennsylvania data centers generate over $1 billion in tax revenue every year\" (no issue-ad label)."),
 ("Indiana Connects","Indiana","1108461391525372","Started 3 Sep 2026","","Taxes","\"Indiana data centers generate nearly $1 billion in tax revenue\" (no issue-ad label)."),
 ("North Carolina Connects","North Carolina","1639529273807981","30 Jun – 27 Jul 2026",_m("$5K–$6K","700K–800K"),"Taxes","Data centers contribute \"critical tax revenue\" and support \"high-skilled jobs\"."),
 # Other industries / companies: further placements
 ("Entergy Louisiana","Louisiana","1107646538861160","Started 12 Oct 2026","","Energy","Same '$2.8B in customer bill savings' text (second version)."),
 ("Williams Companies","Ohio","1055641820404525","Started 14 Sep 2026","","Energy","Cato Institute analysis says on-site power can serve data centers \"without shifting costs to Ohio families\" (Socrates project; no issue-ad label)."),
 ("Wyoming Driven Innovation","Wyoming","1791895145337885","21 Sep – 1 Oct 2026",_m("$100–$199","7K–8K"),"Jobs","Data centers \"could also create a new demand for Wyoming's energy\" and bring jobs and tax revenue."),
 ("Wyoming Driven Innovation","Wyoming","2250211189162737","17 – 27 Sep 2026",_m("<$100","10K–15K"),"Energy (costs)","Families \"should not be left holding the bill\" for new data centers. Meta: \"This ad ran without a required disclaimer.\""),
 ("Related Companies","Michigan","1272981641648678","13 May – 8 Jun 2026",_m("$10K–$15K",">1M"),"Energy (costs)","Saline Township data center \"will pay for 100% of its energy costs\"; grid investments \"will result in $300 million in annual savings for customers.\""),
 ("Related Companies","Michigan","2785184291821003","13 May – 10 Jun 2026",_m("$9K–$10K",">1M"),"Energy (costs)","Same text (second placement)."),
 ("Related Companies","Michigan","1272495225070609","1 – 12 May 2026",_m("$9K–$10K",">1M"),"Water","Project \"protects Michigan's water\" and \"preserves 750 acres of land\"."),
 ("Related Companies","Michigan","1982285979053620","7 – 15 Apr 2026",_m("$1K–$1.5K","350K–400K"),"Water","Closed-loop air cooling \"saves hundreds of millions of gallons of water compared to other data centers.\""),
 ("Related Digital","US (national)","862531826652827","16 – 28 Jul 2026",_m("$5K–$6K","600K–700K"),"Energy (costs)","CEO on CNBC: Related Digital is \"paying our own way on energy, protecting local resources\"."),
 ("Springfield Sangamon Growth Alliance","Illinois","1351760670154303","Started 28 May 2026","","Water","Water use \"comparable to 15 new homes\"; closed loop \"won't require ongoing water consumption\" (no issue-ad label)."),
 ("Springfield Sangamon Growth Alliance","Illinois","2160503341546394","Started 15 Jul 2026",_m("$1.5K–$2K","175K–200K"),"Taxes","\"Nearly $6 million annually in local property taxes\"; CyrusOne gets no local tax breaks."),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","2031856607408530","Started 16 Oct 2026",_m("$400–$499","35K–40K"),"Water","\"Nationally, golf courses use more water than data centers do on site.\""),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","2076591636312533","3 – 16 Oct 2026",_m("$700–$799","60K–70K"),"Water","\"Myth: Data centers use massive amounts of water. Fact: Older data centers did.\""),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","1120497433890697","Started 16 Oct 2026",_m("$400–$499","35K–40K"),"Jobs","A large data center \"employs more than 100 full-time workers and supports 150 to 400 more jobs\"."),
 ("Future Ready Frederick","Maryland","1590508512808580","13 Aug – 5 Sep 2026",_m("$2.5K–$3K","175K–200K"),"Water","\"Misinformation has been spreading\"; data centers \"use advanced technology to reduce water consumption\"."),
 ("Built Here Oklahoma","Oklahoma","1754136019201009","Started 21 Sep 2026","","Energy (costs)","\"Now the law ensures they won't\" impact ratepayers (no issue-ad label)."),
 ("Built Here Oklahoma","Oklahoma","2372537626883774","21 Sep – 25 Oct 2026","","Energy (costs)","\"State law now prohibits passing data center costs to residents\" (no issue-ad label)."),
 ("NWI Data Facts","Indiana","1146371605015712","26 – 29 Oct 2026",_m("$1K–$1.5K","175K–200K"),"Taxes","A Michigan City data center site will be \"generating millions to fund housing projects\"."),
 ("NWI Data Facts","Indiana","1401579901604310","Started 6 Oct 2026","","Jobs","\"Northwest Indiana data centers create new jobs that keep the next generation here\" (no issue-ad label)."),
 ("Power Connection, IBEW Local 364","Illinois","28792759310375561","Started 19 Oct 2026","","Taxes","\"In 2024 Meta's Dekalb Data Center paid 32.1 million in property taxes\" (no issue-ad label)."),
 ("Edison Electric Institute","Missouri","2358942264597308","23 Jun – 1 Sep 2026",_m("$1K–$1.5K","400K–450K"),"Energy (costs)","Large data centers \"help put downward pressure on electric rates\" by spreading system costs."),
 ("Edison Electric Institute","Missouri","2236644027133626","23 Jun – 1 Sep 2026",_m("$1K–$1.5K","400K–450K"),"Energy (costs)","Missouri's 2025 Senate Bill 4 requires data centers \"to pay their fair share of costs\"."),
 # Largest 2026 election and advocacy counter-ads found in the sweep
 ("Conservation Voters of Michigan (counter-ad)","Michigan","912252061727422","21 Sep – 24 Oct 2026",_m("$35K–$40K",">1M"),"Energy (counter-claim)","John James \"cashed in over $113,000 from data center donors\"; families \"stuck paying the bill\"."),
 ("DAGA People's Lawyer Project NV (counter-ad)","Nevada","1638176964326002","Started 14 Oct 2026",_m("$35K–$40K",">1M"),"Water + energy (counter-claim)","Attacks an AG candidate over data centers \"driving up costs and draining our water\"."),
 ("Half Court Political Fund (counter-ad)","Wisconsin","1091363737137522","Started 7 Oct 2026",_m("$40K–$45K",">1M"),"Water (counter-claim)","State Senate candidate: \"Clean water\" and \"No data center hand outs\"."),
 ("Sierra Club Florida (counter-ad)","Florida","1120874683614951","Started 10 Oct 2026",_m("$30K–$35K",">1M"),"Energy (counter-claim)","'Data Center Donalds' attack on Byron Donalds' support for data centers."),
 ("Friends of Tina Kotek / The Choice 2026 (counter-ad)","Oregon","2060421341232960","17 Sep – 16 Oct 2026",_m("$25K–$30K",">1M"),"Energy (counter-claim)","\"As data centers push our energy bills higher\", Drazan \"voted against requiring data centers to pay their fair share\"."),
 ("Dr Theresa Brooks for State Senate (counter-ad)","Michigan","2228839401023928","28 Sep – 20 Oct 2026",_m("$25K–$30K",">1M"),"Energy (counter-claim)","Patients shouldn't \"pay higher energy bills to subsidize data centers\"."),
 ("The Wisco Project (counter-ad)","Wisconsin","1787510099256086","8 Sep – 14 Oct 2026",_m("$20K–$25K",">1M"),"Energy (counter-claim)","Backs a House candidate who \"supports a data center moratorium\"."),
 ("WorkMoney (counter-ad)","Iowa","2784983821860945","23 Jul – 18 Sep 2026",_m("$15K–$20K","700K–800K"),"Energy (counter-claim)","\"Data centers already consume about 11% of Iowa's electricity supply.\""),
 ("Texans for Henry Cuellar (counter-ad)","Texas","2026394025414584","22 Sep – 9 Oct 2026",_m("$10K–$15K",">1M"),"Energy (counter-claim)","\"Tano Tijerina wants data centers to move in next door.\""),
 ("Tiffany for Wisconsin (counter-ad)","Wisconsin","1221109883504437","18 Aug – 1 Sep 2026",_m("$9K–$10K",">1M"),"Water + energy (counter-claim)","Republican attack: opponent's data center plan leaves \"community water supplies drained\" and \"sky-high electric bills\"."),
 ("Maine Conservation Voters Action Fund (counter-ad)","Maine","1119207593924689","Started 3 Oct 2026",_m("$9K–$10K","600K–700K"),"Energy (counter-claim)","Backs a candidate to \"push pause on large scale data centers\"."),
 ("Citizens for Common Sense Michigan (counter-ad)","Michigan","1815074113136528","9 – 23 Oct 2026",_m("$7K–$8K",">1M"),"Taxes (counter-claim)","Attacks a bill giving data centers \"$90 Million in tax breaks\"."),
 ("Government That Works PAC (counter-ad)","South Dakota","1375768711074811","16 – 21 Jun 2026",_m("$7K–$8K",">1M"),"Water + energy (counter-claim)","Sioux Falls mayoral attack: \"bigger bills for electricity and endangering our water supply\"."),
 ("Innovation Ohio (counter-ad)","Ohio","28194997226868784","18 Sep – 8 Oct 2026",_m("$4.5K–$5K","500K–600K"),"Energy (counter-claim)","\"Ohio data centers could increase bills by $70 monthly, report finds.\""),
 ("Friends for Kathy Hochul (counter-ad)","New York","2167025290881029","30 Sep – 16 Oct 2026",_m("$4.5K–$5K","600K–700K"),"Energy (counter-claim)","Opponent \"opposes Governor Hochul's moratorium on new data centers. He'll raise your electric bills.\""),
 ("Utility Information Alliance (counter-ad)","North Carolina","1751481502753963","28 Sep – 9 Oct 2026",_m("$3.5K–$4K","800K–900K"),"Energy (counter-claim)","\"As data centers drive up demand for energy, the bills, and the risks, fall on to everyday families.\""),
]
for (sp,st,lid,dt,spend,ct,tx) in new_meta5:
    if lid not in {m['library_id'] for m in meta}:
        meta.append(dict(sponsor=sp,state=st,library_id=lid,dates=dt,spend=spend,claim_type=ct,text=tx,url=f"https://www.facebook.com/ads/library/?id={lid}"))

# ---------------------------------------------------------------- 3) videos found in the audit sweep
def _v(vid, st, ch, t, tp, ln, vw, pub, cl, adv, tr="no"):
    videos.append(dict(youtube_id=vid, state=st, channel=ch, title=t, topic=tp, length_sec=ln, views=vw, published=pub, google_ads_creatives="",
        google_ads_first_shown=None, google_ads_last_shown=None, key_claim=cl, transcribed=tr, youtube_url=f"https://www.youtube.com/watch?v={vid}", advertiser=adv))
AC2 = "America Connects (second verified Google account, AR07615609037425475585)"
_v("9WjL1mNgkjY","North Carolina","NC Connects","North Carolina Connects: Keeping What Matters Most","Energy",30,2687735,"2026-06-25","Description: \"North Carolina Data Centers are paying the cost, so North Carolina families don't.\"",AC2)
_v("-qFK2gX70J8","Pennsylvania","Pennsylvania Connects","PA Connects: What Matters Most - 15","Energy",15,3255453,"2026-07-14","",AC2)
_v("jgoi3ilu0mo","Georgia","ConnectedGA","What Matters Most","Energy",30,3162007,"2026-06-22","On-screen: \"Georgia data centers paying their costs, so Georgia families don't.\"",AC2)
RD = "RELATED DIGITAL LLC (verified Google advertiser)"
for (vid,st,t,ln,vw,pub,cl) in [
 ("1i0K-Ejk6o8","Michigan","RDMI 2026 3008 Our Commitment 15s Cutdown",15,5245241,"2026-03-13",""),
 ("qPI8sUP1ebQ","Michigan","Our Commitment to Michigan",15,4430495,"2026-01-27","Description: \"paying our own way for energy and infrastructure, protecting Michigan's water\""),
 ("zKdCn0Y-MRQ","Michigan","RDMI 2026 3005 Michigan's Heritage 15s Cutdown",15,3681655,"2026-03-09",""),
 ("aEfo8Wqg8fM","US (national)","RD National 15 HORZ v1 MIX",15,3670575,"2026-06-22",""),
 ("a8A6vcZs194","Michigan","RDMI 2026 3011 \"Your Input\" 15s Cutdown",15,2556473,"2026-04-24",""),
 ("q7deAI_ooMI","US (national)","RD National 30 HORZ v1 MIX",30,2182663,"2026-06-22",""),
 ("-AOJOKtomfE","Michigan","Our Commitment to Michigan",30,1844030,"2026-01-27","Description: \"paying our own way for energy and infrastructure, protecting Michigan's water\"")]:
    _v(vid,st,"Related Companies",t,"Energy + Water",ln,vw,pub,cl,RD)
FR = "FUTURE READY FREDERICK (verified Google advertiser)"
_v("ma3SBpoNmL8","Maryland","Future Ready Frederick","Clean Data Centers Support Funding for Schools and Help Lower Taxes","Taxes",30,47224,"2026-08-03","Title claim: data centers \"help lower taxes\"",FR)
_v("Z3RD_ho5Pt8","Maryland","Future Ready Frederick","Clean Data Centers Will Bring High Paying Jobs and Tax Relief to Their Community","Jobs",30,40376,"2026-08-03","Title claim: \"high paying jobs and tax relief\"",FR)
_v("T0cNo2jAEu0","Maryland","Future Ready Frederick","Clean Data Centers Support Funding for Schools and Help Lower Taxes (5s cut)","Taxes",5,362776,"2026-08-12","",FR)
_v("jhvGXO2wIGM","Maryland","Future Ready Frederick","Clean Data Centers Support Funding for Schools and Help Lower Taxes (13s cut)","Taxes",13,325727,"2026-08-12","",FR)
_v("jytG-SMKgIo","New Mexico","Project Jupiter Together (STACK Infrastructure)","Project Jupiter Together | Jobs","Jobs",60,14118,"2026-05-29","","STACK Infrastructure, Inc. (verified Google advertiser)")
_v("EqG8jj64flk","US (national)","Compass Datacenters","WeAgree_Jobs_Reel_Ad_FINAL","Jobs",15,1057,"2026-10-05","'We Agree' jobs spot (no captions)","Compass Datacenters, LLC (verified Google advertiser)")
videos.sort(key=lambda x: (x['state'], x['topic'], -int(x['views'])))
for v in videos:  # lengths missing from earlier reads; topic consistency
    if v["youtube_id"] in ("gyZYyQDI2mI", "S8Xb7YwvIAU") and not str(v.get("length_sec") or ""): v["length_sec"] = 30
    if v["youtube_id"] == "dyhMX1Gt3OA": v["topic"] = "National security"

# ---------------------------------------------------------------- campaign text corrections
for a in ads:
    if a["id"] == "US-38":
        a["notes"] = ("Since Sep 9, 2026: seven China and national-security Meta ads, six trades-jobs ads and one 'Texas Standard' ad, about $970K–$1.16M combined (Meta ranges), "
                      "the largest Meta spender in this archive. Earlier YouTube spots were titled 'Data Centers Protect America's National Security'.")
    if a["id"] == "US-40":
        a["notes"] = a["notes"].replace("Three Meta ads, each over 1M impressions ($10K–$20K each).", "Eight Meta ad placements (Sep–Oct 2026), each over 1M impressions ($6K–$20K each).")
    if a["id"] == "US-39":
        a["notes"] += " Two placements of the China ad."
    if a["id"] == "US-36":
        a["notes"] += " Meta marks one of its ads (Sep 2026) as having run without a required disclaimer."
    if a["id"] == "US-33":
        a["notes"] = (a.get("notes") or "") + " The 'What Matters Most' spot also ran in North Carolina, Pennsylvania and Georgia (2.7M–3.3M views each) from a second America Connects Google account."
    if a["id"] == "US-41":
        a["notes"] += " The same groups also ran unlabeled 'tax revenue' ads (Sep–Oct 2026) in seven states."
    if a["id"] == "OI-01":
        a["notes"] += " A Sep 2026 Ohio ad cites a Cato Institute analysis of its on-site 'Socrates' power project."
meta_counts += [("Related Companies / Related Digital", "30 Meta ads (Saline Township, MI); 59 + 43 Google ads"),
                ("Local pro-data-center coalitions", "Springfield Sangamon Growth Alliance (IL), SW Illinois Coalition for Job Growth, Future Ready Frederick (MD), Built Here Oklahoma, NWI Data Facts (IN), IBEW Local 364"),
                ("Edison Electric Institute", "2 data-center Meta ads (Missouri, 2026); 63 Google ads, mostly general grid spots"),
                ("2026 election counter-ads", "Dozens of candidate and PAC ads; the archive lists the largest (over $20K or 1M impressions) found on Oct 30, 2026")]
