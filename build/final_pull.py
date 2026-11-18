# v1.3 final pull (read Nov 17, 2026; archive frozen at election day, Nov 3, 2026).
# 1. Re-read of every Meta ad already in the archive: final run dates, spend and impressions.
# 2. Ads that were delivering between Oct 24 and Nov 3 from sponsors already in the archive.
# 3. Largest new sponsors in the same window (keyword searches, first page of results, sorted by impressions).
# 4. Space / subsea / floating data-center ads found on Nov 12.
# 5. YouTube view counts and Google "last shown" dates re-read Nov 17.
import datetime as _dt

def _d(s):
    d = _dt.date.fromisoformat(s); return f"{d.day} {d.strftime('%b %Y')}"
def _rng(st, en, act):
    if act == "A": return f"{_d(st)} – still running 17 Nov 2026"
    a, b = _dt.date.fromisoformat(st), _dt.date.fromisoformat(en)
    if a.year == b.year and a.month == b.month: return f"{a.day} – {b.day} {b.strftime('%b %Y')}"
    if a.year == b.year: return f"{a.day} {a.strftime('%b')} – {b.day} {b.strftime('%b %Y')}"
    return f"{_d(st)} – {_d(en)}"
def _sp(spend, imp):
    spend = (spend or "").replace("-", "–"); imp = (imp or "").replace("-", "–")
    return "; ".join(x for x in (spend, (imp + " impressions") if imp else "") if x)

# ---- 1. re-read of existing ads
_by = {m["library_id"]: m for m in meta}
FINAL_GONE = []
for _ln in open(os.path.join(B, "final_read_2026-11-17.txt"), encoding="utf-8"):
    _id, _act, _st, _en, _spend, _imp = _ln.rstrip("\n").split("|")
    m = _by.get(_id)
    if not m: continue
    if _act == "X": continue
    if _act == "G":
        FINAL_GONE.append(_id)
        old = m["dates"].replace(" – active", "").replace("Oct 1 2026", "Started 1 Oct 2026").replace("Sep 20 2026", "Started 20 Sep 2026")
        m["dates"] = old + "; no longer in the Ad Library on 17 Nov 2026"
        continue
    _par = re.search(r"\s*\((one of|video also)[^)]*\)", m["dates"])
    m["dates"] = _rng(_st, _en, _act) + (_par.group(0) if _par else "")
    if _spend: m["spend"] = _sp(_spend, _imp)

# ---- 2–4. new Meta ads: (sponsor, state, id, start, end, A/I, spend, impressions, claim type, text)
_V = " (one of {} versions delivering 24 Oct – 3 Nov)"
new_meta7 = [
 # America Connects state groups: the energy message, new in the final wave
 ("Virginia Connects","Virginia","1937295901048443","2026-10-19","2026-11-17","A","","","Energy (costs)","Data centers \"fund new energy projects—enough to power 325,000+ homes\" while \"paying for every watt\" (no issue-ad label).",36),
 ("Virginia Connects","Virginia","29363106506620329","2026-10-13","2026-11-17","A","","","Water","\"Some data centers in Virginia don't use water for cooling 96% of the time\" (no issue-ad label).",36),
 ("Pennsylvania Connects","Pennsylvania","1427060622647550","2026-09-17","2026-11-17","A","","","Energy (costs)","\"PA data centers fund new energy projects, enough to power over 1.6M homes\" (no issue-ad label).",9),
 ("Oregon Connects","Oregon","1361320452652801","2026-09-22","2026-11-17","A","","","Energy (costs)","\"Oregon data centers fund new energy projects—enough to power 31,000+ homes\" (no issue-ad label).",9),
 ("Connected Georgia","Georgia","1091053473672069","2026-09-22","2026-11-17","A","","","Energy (costs)","\"GA data centers fund new energy projects, enough to power 140,000+ homes\" (no issue-ad label).",27),
 ("Connected Ohio","Ohio","1644287020617322","2026-09-17","2026-11-17","A","","","Energy (costs)","\"Ohio data centers fund new energy projects, enough to power 590k homes\" (no issue-ad label).",9),
 ("Indiana Connects","Indiana","2278009809631619","2026-09-03","2026-11-17","A","","","Energy (costs)","Data centers \"pay for every watt of energy they use\" and \"help upgrade Indiana's aging electric grid\" (no issue-ad label).",5),
 # QTS
 ("QTS Data Centers (Blackstone)","US (national)","1152975787297827","2026-11-02","2026-11-17","A","","","Energy (costs)","\"We cover 100% of our energy costs while upgrading the local grid.\" Headline: \"We cover our costs.\"",43),
 ("QTS Data Centers (Blackstone)","US (national)","2192046634687863","2026-11-02","2026-11-17","A","","","Taxes","\"Millions in local tax revenue. Thousands of hours giving back.\"",43),
 ("QTS Data Centers (Blackstone)","US (national)","2189981561908235","2026-10-05","2026-11-17","A","","","Jobs","QTS \"supports local economies by investing in communities, creating jobs and partnering with local suppliers\".",43),
 # Meta's own local ads
 ("Meta","Texas (El Paso)","2205240850050436","2026-10-05","2026-11-17","A","","","Water","\"We'll restore twice the water we consume at our El Paso data center.\" Also runs in Spanish (no issue-ad label).",49),
 ("Meta","Alabama (Montgomery)","1436667177798336","2026-10-21","2026-11-17","A","","","Energy (costs)","\"We pay the full costs for our electricity and help fund grid upgrades\" (no issue-ad label).",49),
 ("Meta","Indiana","2107409233471965","2026-10-12","2026-11-17","A","$25K-$30K","700K-800K","Water","\"We will restore 100% of the water we consume in our data center operations.\" Headline: \"Investing in Indiana.\"",49),
 ("Meta","Indiana (Lebanon)","2587876388330240","2026-09-08","2026-11-17","A","","","Jobs","The Lebanon data center \"is creating economic opportunities\" for small business owners (no issue-ad label).",49),
 # Texans for Economic Liberty: the 19 ads not in the first pull
 ("Texans for Economic Liberty","Texas","1099444266054670","2026-10-22","2026-10-24","I","$10K-$15K","60K-70K","National security","Build \"the data centers that keep American data out of the hands of hostile nations\".",0),
 ("Texans for Economic Liberty","Texas","1152197807376924","2026-10-22","2026-10-24","I","$15K-$20K","100K-125K","National security","Data centers \"keep American data out of the Chinese Communist Party\".",0),
 ("Texans for Economic Liberty","Texas","1135995179081485","2026-10-22","2026-10-24","I","$6K-$7K","30K-35K","National security","Same 'Chinese Communist Party' text (second version).",0),
 ("Texans for Economic Liberty","Texas","1439856308275610","2026-10-23","2026-10-28","I","$3.5K-$4K","25K-30K","National security","Same 'Chinese Communist Party' text (third version).",0),
 ("Texans for Economic Liberty","Texas","1139512795232176","2026-09-09","2026-11-07","I","$9K-$10K","100K-125K","National security","\"Texas data centers keep Texas data on Texas soil, and out of the hands of enemies like China.\"",0),
 ("Texans for Economic Liberty","Texas","2165780317708768","2026-09-09","2026-11-06","I","$7K-$8K","40K-45K","National security","\"Your data, stored in Texas, under Texas standards. That's leadership.\"",0),
 ("Texans for Economic Liberty","Texas","2297263294527874","2026-10-22","2026-10-25","I","$6K-$7K","50K-60K","Jobs","\"Behind every Texas data center is a welder, electrician or pipefitter earning a good living.\"",0),
 ("Texans for Economic Liberty","Texas","1111718257925494","2026-10-23","2026-10-28","I","$9K-$10K","125K-150K","Jobs","Same 'welder, electrician or pipefitter' text (second version).",0),
 ("Texans for Economic Liberty","Texas","2335756646962155","2026-10-22","2026-10-24","I","$6K-$7K","50K-60K","Jobs","Same 'welder, electrician or pipefitter' text (third version).",0),
 ("Texans for Economic Liberty","Texas","1440111811604925","2026-10-23","2026-10-28","I","$9K-$10K","80K-90K","Jobs","Same 'welder, electrician or pipefitter' text (fourth version).",0),
 ("Texans for Economic Liberty","Texas","1446092404279510","2026-10-22","2026-10-24","I","$4.5K-$5K","30K-35K","Jobs","Same 'welder, electrician or pipefitter' text (fifth version).",0),
 ("Texans for Economic Liberty","Texas","1791545561895294","2026-10-23","2026-10-28","I","$1K-$1.5K","20K-25K","Jobs","Same 'welder, electrician or pipefitter' text (sixth version).",0),
 ("Texans for Economic Liberty","Texas","2857363984636952","2026-10-22","2026-10-24","I","$2.5K-$3K","20K-25K","Jobs","Same 'welder, electrician or pipefitter' text (seventh version).",0),
 ("Texans for Economic Liberty","Texas","4423960154487729","2026-09-09","2026-11-07","I","$30K-$35K","175K-200K","Jobs","\"Data centers create jobs for Texas electricians, welders and pipefitters.\"",0),
 ("Texans for Economic Liberty","Texas","28803374022604118","2026-09-09","2026-11-06","I","$5K-$6K","70K-80K","Jobs","\"Data centers create good-paying jobs for the skilled trades.\"",0),
 ("Texans for Economic Liberty","Texas","2275952023247967","2026-09-09","2026-11-06","I","$10K-$15K","80K-90K","Regulation","\"Blue states are blocking data centers. Texas is setting the standard for how they get built.\"",0),
 ("Texans for Economic Liberty","Texas","1392687498985291","2026-09-10","2026-11-06","I","$4K-$4.5K","45K-50K","Regulation","Same 'Blue states are blocking data centers' text (second version).",0),
 ("Texans for Economic Liberty","Texas","1385410257116629","2026-09-09","2026-11-06","I","$9K-$10K","35K-40K","Energy (costs)","Data centers \"pay for their own power and water, so the cost never lands on Texas families\".",0),
 ("Texans for Economic Liberty","Texas","1590788092507693","2026-09-09","2026-11-07","I","$2K-$2.5K","10K-15K","Energy (costs)","Data centers \"provide their own power, reuse their own water, lower electricity costs\" (smaller version of the lead ad).",0),
 # Southwestern Illinois Coalition for Job Growth
 ("Southwestern Illinois Coalition for Job Growth","Illinois","945807044879403","2026-10-16","2026-11-04","I","$800-$899","100K-125K","Jobs","\"Who knows how to build a data center the right way? The people who build them.\" Promotes local hiring and apprenticeships.",42),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","29170911075868498","2026-10-16","2026-11-04","I","$400-$499","40K-45K","Water","Granite City code \"already requires closed-loop cooling, noise limits, light limits\" and a community benefit agreement.",42),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","1736774410723971","2026-10-16","2026-11-04","I","<$100","6K-7K","Taxes","In DeKalb in 2025, \"one data center paid $30.4 million in property taxes\"; about 60% went to schools.",42),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","1662611835379333","2026-10-16","2026-11-04","I","$300-$399","25K-30K","Energy (costs)","Ameren Illinois \"confirmed large customers like data centers pay for the system upgrades they need\".",42),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","4674635626102080","2026-10-20","2026-11-04","I","$100-$199","15K-20K","Energy (costs)","\"Indiana utility is decreasing power rates thanks to payments made by local data centers.\"",42),
 ("Southwestern Illinois Coalition for Job Growth","Illinois","1082409191331414","2026-10-16","2026-11-04","I","$100-$199","20K-25K","National security","\"Staying ahead takes secure, US-based data centers.\"",42),
 # Built Here Oklahoma, EEI, Wyoming, Related Digital
 ("Built Here Oklahoma","Oklahoma","1063635146576957","2026-09-21","2026-11-17","A","","","Jobs","\"When Google announced a $9 billion investment in Oklahoma, local trades took notice\" (no issue-ad label).",10),
 ("Built Here Oklahoma","Oklahoma","1757093043083412","2026-09-21","2026-11-17","A","","","Regulation","\"This infrastructure already runs daily life – and Oklahoma set the rules for how it gets built here\" (no issue-ad label).",10),
 ("Edison Electric Institute","Indiana","1070161062661609","2026-09-16","2026-11-01","I","$5K-$6K","30K-35K","Energy (costs)","Under HEA 1007, data centers \"are required to pay their fair share of costs\". Page name: 'We Stand For Energy'.",0),
 ("Edison Electric Institute","Indiana","1039532835799443","2026-09-16","2026-11-03","I","$5K-$6K","30K-35K","Energy (costs)","Adding data centers means \"shared grid costs are spread across a broader customer base\".",0),
 ("Wyoming Driven Innovation","Wyoming","1276251964713428","2026-11-02","2026-11-17","A","","","Water","\"Most modern data centers in construction use closed-loop systems because they are more efficient\" (no issue-ad label).",0),
 ("Wyoming Driven Innovation","Wyoming","1131079932632500","2026-10-19","2026-10-31","I","$100-$199","10K-15K","Jobs","Quotes Compass Datacenters' CEO on the end of a \"war on blue-collar jobs\" and demand for electricians.",0),
 ("Wyoming Driven Innovation","Wyoming","2725572121213934","2026-10-19","2026-10-31","I","$100-$199","7K-8K","Taxes","\"Data center infrastructure has become foundational to modern American life.\"",0),
 ("Related Digital","Michigan","1010892208696475","2026-10-30","2026-11-17","A","","","Jobs","Union workers at the Saline site: \"more than 2,000 trade workers\" on \"the largest economic investment in Michigan's history\" (no issue-ad label).",0),
 ("Related Digital","Michigan","961700786604260","2026-10-30","2026-11-17","A","","","Jobs","\"From the ground up, skilled tradespeople make progress possible\" (no issue-ad label).",0),
 # industry side of local ballot measures and moratoria
 ("Consumer Action for a Strong Economy","Ohio (Pataskala)","1651691906330806","2026-10-21","2026-11-04","I","$2.5K-$3K","200K-250K","Jobs","\"Hundreds of good jobs, right here at home. Vote NO on the so-called 'data center ban' Nov. 3.\"",6),
 ("Consumer Action for a Strong Economy","Ohio (Pataskala)","1571093961719236","2026-10-20","2026-10-30","I","$700-$799","45K-50K","Taxes","\"$22 million for Pataskala schools is on the ballot.\"",6),
 ("NetChoice","Ohio (Sunbury)","1034718296292498","2026-10-16","2026-11-04","I","$4K-$4.5K","175K-200K","Jobs","The \"data center ban\" \"threatens our jobs and blocks property tax relief in Sunbury\". Marked 'Digitally created'.",3),
 ("NetChoice","Ohio (Sunbury)","1743934946712725","2026-10-16","2026-11-04","I","$3K-$3.5K","200K-250K","Taxes","\"61% of the [money] behind the proposed data center ban is from California.\"",3),
 ("Building Our Future Ohio","Ohio (Oregon)","1081068958077381","2026-10-21","2026-11-04","I","$400-$499","80K-90K","Energy (costs)","\"The project pays for the power it uses and required infrastructure improvements.\"",13),
 ("Building Our Future Ohio","Ohio (Oregon)","1777937970180695","2026-10-21","2026-11-04","I","$400-$499","70K-80K","Water","The project \"is designed to reduce water consumption\".",13),
 ("Building Our Future Ohio","Ohio (Oregon)","1559148382924127","2026-10-17","2026-11-04","I","$500-$599","60K-70K","Taxes","\"A NO vote could mean $7 million every year for Oregon schools.\"",13),
 ("Mississippi Black Chamber of Commerce","Mississippi (Jackson)","1469193108465218","2026-10-01","2026-10-28","I","$8K-$9K","400K-450K","Taxes","Urges Jackson City Council to \"lift the data center moratorium\"; \"more resources\" for first responders and youth programs.",0),
 ("San Jose Silicon Valley Chamber of Commerce","California (San Jose)","1614435140415327","2026-10-26","2026-11-17","A","$700-$799","80K-90K","Regulation","Calls for \"clear, balanced regulations\" on data centers and large energy users.",0),
 ("Bright Future Iowa","Iowa","1408398778070134","2026-10-07","2026-10-27","I","$900-$999","45K-50K","Jobs","\"Construction jobs. A stronger tax base. Permanent technical roles.\"",0),
 # space, subsea and floating data centers (found 12 Nov)
 ("World Economic Forum","Global","1685225826054515","2026-06-16","2026-06-29","I","","","Energy","Starcloud's CEO: build data centres \"out in orbit\"; AI energy demand \"could rise 50% a year until 2030\" (no issue-ad label).",0),
 ("Virtus Solis","US (national)","1337562348365029","2026-08-07","2026-08-22","I","","","Energy","\"Clean baseload power from space\" for data centres and heavy industry; \"We are running into a power wall\" (no issue-ad label; one of 5 versions).",0),
 ("Change.org (counter-ad)","Maine","1336700171235689","2026-06-29","2026-07-10","I","$500-$599","50K-60K","Water (counter-claim)","\"A tech company is seeking federal approval to sink an AI data center into Maine's coast.\" One of 3 versions.",0),
 ("The Alliance for Secure AI (counter-ad)","Maine","1397108472386456","2026-08-24","2026-09-01","I","$100-$199","50K-60K","Water (counter-claim)","Eastport council \"unanimously approved a 180-day moratorium\" on a \"$100 million underwater AI data center\".",0),
 ("Sullivan Watch (counter-ad)","Alaska","2269627393603877","2026-10-26","2026-11-03","I","$1.5K-$2K","60K-70K","Water (counter-claim)","A Cook Inlet proposal \"calls for as many as 350 underwater turbines\" and 66 \"hives\" housing AI servers.",0),
 # largest counter-ads in the final window
 ("No on Prop 45 (counter-ad)","California","2352225115545933","2026-10-26","2026-11-05","I","$100K-$125K",">1M","Regulation (counter-claim)","Says the measure's \"fine print\" delivers for data centers, not lower living costs.",0),
 ("Connie Chan for Congress (counter-ad)","California","2235720447823627","2026-10-20","2026-11-05","I","$70K-$80K",">1M","Energy (counter-claim)","\"Connie Chan wants housing, not data centers. And she's not funded by AI.\"",0),
 ("Restoration of America (counter-ad)","Wisconsin","2395024634239439","2026-10-26","2026-11-05","I","$50K-$60K",">1M","Regulation (counter-claim)","\"Don't let David Crowley turn Wisconsin into the world's data center.\" A second version spent $35K–$40K.",0),
 ("The Alaska Center (counter-ad)","Alaska","1666627071854024","2026-10-23","2026-11-04","I","$35K-$40K",">1M","Energy (counter-claim)","\"$80 billion in tax breaks to data center developers as our electric bills go up?\"",0),
 ("House Majority PAC (counter-ad)","Ohio","2216859099714936","2026-10-06","2026-11-04","I","$30K-$35K",">1M","Energy (counter-claim)","Candidate \"took money from data center developers\"; data centers \"are raising electric bills for Ohio families\".",0),
 ("Leila Namvar for Assembly (counter-ad)","California","2085015378859569","2026-10-23","2026-11-05","I","$30K-$35K",">1M","Water + energy (counter-claim)","\"The data centers get our water and we get the bill.\"",0),
 ("State + Local Election Alliance (counter-ad)","North Carolina","1405324455114852","2026-09-17","2026-11-04","I","$30K-$35K",">1M","Regulation (counter-claim)","County candidate will \"keep data centers out of our backyard\".",0),
 ("Government That Works PAC (counter-ad)","South Carolina","3166638176869194","2026-10-22","2026-11-04","I","$25K-$30K",">1M","Regulation (counter-claim)","Candidate \"told South Carolina exactly where she stands: 'I'm for data centers.'\"",0),
 ("The Ohio Independent (counter-ad)","Ohio","1813102973155015","2026-10-08","2026-11-04","I","$20K-$25K",">1M","Regulation (counter-claim)","\"NW Ohioans call out pro-data center Husted.\"",0),
 ("Ohio Democratic Party (counter-ad)","Ohio","1481154680727896","2026-10-21","2026-10-31","I","$15K-$20K",">1M","Energy (counter-claim)","Acton will \"make sure data centers pay 100% of their own utility costs, not Ohio families\". Page name: 'Vivek Profits. Ohio Pays.'",0),
 ("Ohio Democratic Party (counter-ad)","Ohio","2916146378762235","2026-10-21","2026-10-30","I","$4K-$4.5K","900K-1M","Energy (counter-claim)","\"Lower electric bills start with making data centers pay their fair share.\"",0),
 ("Sierra Club Florida (counter-ad)","Florida","1487041359951570","2026-10-12","2026-11-04","I","$15K-$20K",">1M","Regulation (counter-claim)","Attorney General candidate \"will protect Floridians from hyperscale data centers\".",0),
 ("Elect Katie Hobbs (counter-ad)","Arizona","1122802630298197","2026-10-11","2026-11-04","I","$15K-$20K",">1M","Taxes (counter-claim)","\"A three-year freeze on tax giveaways for new data centers.\" Page name: 'Arizona Daily Briefing'.",0),
 ("Gina Hinojosa Campaign (counter-ad)","Texas","1090793656914049","2026-10-26","2026-11-04","I","$15K-$20K","500K-600K","Taxes (counter-claim)","\"Abbott's Texas: 335 data centers, 248 more coming. They get billions in tax breaks.\"",0),
 ("LCV Victory Fund (counter-ad)","Iowa","1674590694098686","2026-10-05","2026-11-03","I","$10K-$15K",">1M","Taxes (counter-claim)","Congressman \"took money from data center developers and voted to give them a $80 billion tax break\". Same script ran against at least six House members.",0),
 ("LCV Victory Fund (counter-ad)","Montana","1721048120020595","2026-10-05","2026-11-03","I","$10K-$15K",">1M","Water + energy (counter-claim)","\"Dirty water! Sky-high electric bills! A new data center could be yours, Montana!\"",0),
 ("League of Conservation Voters (counter-ad)","US (national)","1563534862105909","2026-10-06","2026-11-03","I","$8K-$9K",">1M","Energy (counter-claim)","\"Dirty data centers could increase U.S. climate pollution up to 30%.\"",0),
 ("Beau Bayh for Indiana (counter-ad)","Indiana","1376932351095317","2026-10-12","2026-10-27","I","$10K-$15K",">1M","Energy (counter-claim)","Opponent \"would give data centers a free ride\"; \"fight to lower your electric bills\".",0),
 ("Michigan Senate Republican Campaign Committee (counter-ad)","Michigan","1143131671482283","2026-10-19","2026-11-04","I","$10K-$15K",">1M","Taxes (counter-claim)","Opponent \"wrote the bill giving Big Tech data centers a $90 million tax break\".",0),
 ("NC WARN (counter-ad)","North Carolina","940563782214883","2026-10-26","2026-11-10","I","$10K-$15K",">1M","Energy (counter-claim)","\"Duke Energy is recruiting data centers to justify new fossil fuel power plants - and you'll pay for them!\"",0),
 ("Future of Life Institute (counter-ad)","US (national)","1112407328295851","2026-10-24","2026-11-17","A","$10K-$15K","200K-250K","Regulation (counter-claim)","\"Whether it's a data center in our backyards or a chatbot in our classrooms, Americans should have a say.\" Page name: 'Protect What's Human'.",0),
 ("Pennsylvania Accountability Fund (counter-ad)","Pennsylvania","4960723094172984","2026-10-01","2026-10-27","I","$9K-$10K",">1M","Regulation (counter-claim)","Congressman \"says he'll regulate data centers, but he owns millions in data center stocks\". Page name: 'Ban Insider Trading'.",0),
 ("Friends for Kathy Hochul (counter-ad)","New York","1086140594032696","2026-10-19","2026-11-03","I","$8K-$9K",">1M","Regulation (counter-claim)","Hochul \"passed the nation's first moratorium on new data centers\".",8),
 ("Blaise Ingoglia for CFO (counter-ad)","Florida","2526349944558755","2026-10-26","2026-11-05","I","$7K-$8K",">1M","Taxes (counter-claim)","Opponent \"voted to give YOUR tax dollars away to billion dollar data center companies\".",0),
 ("350.org (counter-ad)","US (national)","921662913973183","2026-09-18","2026-11-17","A","$4.5K-$5K","200K-250K","Regulation (counter-claim)","\"Join thousands demanding a moratorium until real safeguards are in place.\"",0),
 ("MO Protect PAC (counter-ad)","Missouri","1872380414215516","2026-10-16","2026-10-31","I","$4K-$4.5K","400K-450K","Energy (counter-claim)","\"Billionaires want to put massive data centers in our backyards\"; \"we could be stuck paying higher electric bills\". Urges 'No on 6'.",0),
 ("Make the Road Action (counter-ad)","New York","1709389554095155","2026-10-21","2026-11-04","I","$3K-$3.5K","900K-1M","Regulation (counter-claim)","Hochul \"signed the first statewide data center moratorium in the country\".",0),
 ("Adamson Ahdoot LLP (counter-ad)","US (national)","2338413763656808","2026-10-22","2026-11-05","I","$2.5K-$3K","500K-600K","Water (counter-claim)","Law-firm video: a woman says a Meta data center \"left her without drinkable water\". \"Meta denies it is responsible.\"",0),
 ("NRDC Action Fund (counter-ad)","New Jersey","1426197826132476","2026-10-09","2026-10-30","I","$2.5K-$3K","90K-100K","Energy (counter-claim)","\"NJ electric bills jumped 20% in June 2025. Data centers were the main driver.\"",0),
 ("Friends of Sherrod Brown (counter-ad)","Ohio","2306425966784285","2026-10-22","2026-11-03","I","$2K-$2.5K","200K-250K","Energy (counter-claim)","\"Husted calls Ohio a data center state. But all Ohioans got was higher bills and lower property values.\"",0),
 ("VPIRG (counter-ad)","Vermont","29011023718533555","2026-10-19","2026-11-04","I","$1.5K-$2K","300K-350K","Regulation (counter-claim)","\"Don't Data Center Vermont\": petition after the governor vetoed a data-center bill.",9),
 ("Montanans for Responsible Leadership (counter-ad)","Montana","1432634749021670","2026-10-23","2026-11-04","I","$1.5K-$2K","125K-150K","Regulation (counter-claim)","\"15,000 of your neighbors signed to put data centers on the ballot.\"",0),
 ("Georgia Conservation Voters Education Fund (counter-ad)","Georgia","1113746518099934","2026-10-16","2026-11-04","I","$1K-$1.5K","150K-175K","Taxes (counter-claim)","\"Georgia gave up $474 million in one year because of its data center tax breaks.\"",0),
]
_have = {m['library_id'] for m in meta}
for (sp, st, lid, a, b, act, spend, imp, ct, tx, nver) in new_meta7:
    if lid in _have: continue
    meta.append(dict(sponsor=sp, state=st, library_id=lid, dates=_rng(a, b, act) + (_V.format(nver) if nver else ""),
                     spend=_sp(spend, imp), claim_type=ct, text=tx, url=f"https://www.facebook.com/ads/library/?id={lid}"))

# ---- campaign-level entries
ads.extend([
 dict(id="US-49", region="US", place="Texas (El Paso), Alabama (Montgomery), Indiana (Lebanon), Ohio", sponsor="Meta", sponsor_type="Hyperscaler",
      format="Facebook/Instagram ads", title="'Building El Paso', 'Building Montgomery', 'Investing in Indiana'", date="Sep – Nov 2026 (running)", claim_type="Water + Energy",
      claim="\"We'll restore twice the water we consume at our El Paso data center\"; \"We pay the full costs for our electricity and help fund grid upgrades\" (Montgomery); \"We will restore 100% of the water we consume\" (Indiana)",
      verbatim="Verbatim (Meta Ad Library, read Nov 17, 2026)", url_primary="https://www.facebook.com/ads/library/?id=2205240850050436", url_source="",
      evidence="Primary (Meta Ad Library)",
      notes="49 data-center ads on Meta's own page were delivering between Oct 24 and Nov 3, 2026, aimed at the towns where it is building. All but one ran without an issue-ad label, so Meta's library shows no spend or audience for them."),
 dict(id="US-50", region="US", place="Ohio (Pataskala, Sunbury, Oregon)", sponsor="Consumer Action for a Strong Economy; NetChoice PAC; Building Our Future Ohio", sponsor_type="Industry/advocacy group",
      format="Facebook/Instagram ads", title="Vote NO on the 'data center ban'", date="Oct 16 – Nov 4, 2026", claim_type="Jobs + Taxes",
      claim="\"Hundreds of good jobs, right here at home\"; \"$22 million for Pataskala schools is on the ballot\"; \"A NO vote could mean $7 million every year for Oregon schools\"",
      verbatim="Verbatim (Meta Ad Library, read Nov 17, 2026)", url_primary="https://www.facebook.com/ads/library/?id=1651691906330806",
      url_source="https://www.newsfromthestates.com/node/437398", evidence="Primary (Meta Ad Library) + reported result",
      notes="Three groups ran 22 Facebook ads against local measures to ban large data centers. Voters backed restrictions in all 18 Ohio communities that voted on Nov 3, 2026 (States Newsroom); Oregon's ban passed with 61% (Fox 8)."),
 dict(id="GL-17", region="Global", place="Orbit; coasts of Maine and Alaska", sponsor="World Economic Forum; Virtus Solis; opponents in Maine and Alaska", sponsor_type="Industry/advocacy group",
      format="Facebook/Instagram ads", title="Space, subsea and floating data centers", date="Jun – Nov 2026", claim_type="Energy + Water",
      claim="Build data centres \"out in orbit\" (WEF video with Starcloud's CEO); \"clean baseload power from space\" (Virtus Solis); opponents: \"sink an AI data center into Maine's coast\" (Change.org)",
      verbatim="Verbatim (Meta Ad Library, read Nov 12 and 17, 2026)", url_primary="https://www.facebook.com/ads/library/?id=1685225826054515", url_source="",
      evidence="Primary (Meta Ad Library)",
      notes="Searched Meta's library on Nov 12, 2026 for orbital, underwater and floating data centers. No ads found from Google, SpaceX, Starcloud, Nautilus or Keppel. What exists: a WEF explainer, a space-solar start-up, and opponents of the DeepGreen proposal off Eastport, Maine and of a Cook Inlet proposal in Alaska."),
])

# ---- 5. YouTube: views read Nov 17, 2026; Google 'last shown' for videos still in America Connects' Google ads
YT_VIEWS = dict(x.split(":") for x in "jgoi3ilu0mo:3162074,bH3YMwpwp1w:100965,Ns1QMFCUtK8:30598,fnlcr5Q_t5s:30367,-zfNePwjzWs:89624,khJB92_jVsc:37352,z84ux4Oi5ow:24503,IQqPY39Vpes:1773098,pkZRwfDVo_c:119433,PjV2YORxww8:34468,3-pJ0cSKvv8:24493,ySvxwzQRa8s:982986,kf5ZQr3ll8o:629819,OAcGOl4DYK0:118677,IjbFDNM-ep0:407391,rTZLx-qwWmY:429653,jY8GsRcInMk:56413,Wo0CN_JEW48:82222,KmBqBgI27Xc:565549,-_j4DyrwtKM:106403,DYm0Cr-XGso:2344320,53QC6xVmIZo:1843839,IoTG4q65N84:183880,NCkkuQ7rULo:111580,NQmU2DPPQLc:58656,zZGSzgW4gjs:183935,E83yCe0Lv3E:92689,yVgDu8BeR7U:38725,lmLQV5dhSa0:251046,aSO_L69uRjg:79634,qK-q4TFgx9E:61414,1i0K-Ejk6o8:5245243,qPI8sUP1ebQ:4430495,zKdCn0Y-MRQ:3681656,a8A6vcZs194:2556474,-AOJOKtomfE:1844031,jytG-SMKgIo:14156,9WjL1mNgkjY:2687805,3QroEOG6DdM:2473570,ejgSaWjdJ7A:2373344,8Ba9MUPARqU:250340,rVIADkHe4sQ:2020602,vNDFktmU4hE:221590,v72N9D7w4NE:242205,ShWj7Rlz8Pw:2411738,X-S4py1uM3M:2322575,e4BHe-GFFsI:519583,SKjboEY9bGc:376797,TH8TGA0dlsw:195896,qvC9CceYe70:297603,GPviVX65gmQ:280017,Rcq25r9Umc8:82691,d5QTM2v_Nwk:402239,zF54V7HB7NU:349362,WPDq_QLIww4:177875,L-g5j8Dah_o:4026753,F-lA8tM5ytg:2024635,YUsXX5FLsJY:777187,UatW5tVYF64:367924,0Q0BS4S44ks:261022,ou96__c-5Dk:687808,WOiFlBCIHw4:350740,mqyQeKixYQ8:154652,M87UBNxfDO8:738052,amDE7M-7wK4:294191,jrfSmrV0GH0:135923,-qFK2gX70J8:3255457,zO9SvmZ-bJw:1352045,eMywznSSrtM:636036,1NlwEokWCMc:510842,zu_AH_cVtLk:56948,bj9dZxbgKu0:46254,EmtbaKfzoQM:1276997,5M2n5OOwZNI:491581,oQJW-VC96FE:513438,YukGJZ_6PWo:72252,Bi5wEdJh28M:1405152,lnMPirn6Vss:595613,M9kHXR-rZdM:445563,2sLdcb9jjFU:194793,6ILMVNmcEn0:189188,Is8QA48A_kk:121290,ta3HhLRdt_E:65983,CADpCqrdeLg:27028,UKPwuA2hWjk:295405,nxU0tKVbHtc:225498,FqfvrIFqA0c:216312,IwQCwpzG_GY:12221455,dyhMX1Gt3OA:2012856,u-sHlkSxmsw:243373,Li0ap16ReOQ:1823064,rlrmpWOx-Zc:1886101,_0ZWQfcnjDM:401010,djyVUNkjZf4:327536,qJohMKs6c5M:5922901,XTsm24wKu_I:1507613,cmzzf9zActQ:338234,UMfeRNFJdSQ:320031,1YcHxwGd9v4:209428,Io7h_19LHWE:2070179,1zTYeqE1VVc:1835611,ffDG_n1zcis:900244,TsiNMFTxjF0:641903,oThjI485c3U:349027,4GwRC82WLzs:2747,Cwh4o5H-rtU:775,aEfo8Wqg8fM:3670576,q7deAI_ooMI:2182665,EqG8jj64flk:1272,XNaTFb_tYXM:1254,gyZYyQDI2mI:2134297,oecVwMWyFeE:321238,Ilt7_2XKnn8:548465,iKokXUMOPbA:562978,f80vKjblqXY:191330,jAiyivVAhCE:532538,Z3RD_ho5Pt8:40376,S8Xb7YwvIAU:1191403,hSnYrXzxbPk:612148,4L82KjXGF5Y:257885,T0cNo2jAEu0:362776,jhvGXO2wIGM:325727,ma3SBpoNmL8:47225,0rAjHVnkXAA:333318,HpDH_znD6DE:598701,WRe5nO-1aPc:578305,Em9nQ1zngUE:176781,0JS96iU0k0o:4873".split(","))
AC_STILL = set("aSO_L69uRjg GPviVX65gmQ 5M2n5OOwZNI OAcGOl4DYK0 ySvxwzQRa8s eMywznSSrtM lnMPirn6Vss zO9SvmZ-bJw WOiFlBCIHw4 WPDq_QLIww4 TH8TGA0dlsw YUsXX5FLsJY zF54V7HB7NU SKjboEY9bGc zZGSzgW4gjs d5QTM2v_Nwk pkZRwfDVo_c Rcq25r9Umc8 e4BHe-GFFsI oQJW-VC96FE amDE7M-7wK4 M87UBNxfDO8 yVgDu8BeR7U Ilt7_2XKnn8 IoTG4q65N84 qvC9CceYe70 3-pJ0cSKvv8 bH3YMwpwp1w mqyQeKixYQ8 NCkkuQ7rULo ou96__c-5Dk Ns1QMFCUtK8 0Q0BS4S44ks E83yCe0Lv3E kf5ZQr3ll8o UatW5tVYF64".split())
for v in videos:
    if v["youtube_id"] in YT_VIEWS: v["views"] = int(YT_VIEWS[v["youtube_id"]])
    if v["youtube_id"] in AC_STILL: v["google_ads_last_shown"] = "2026-11-17"

# ---- excerpts kept under 15 words (codebook rule), applied to every Meta ad
SHORT = {
 "2096764071716470": "Data centers \"provide their own power, reuse their own water, lower electricity costs\" (\"The Texas Standard\").",
 "1293519818383322": "\"Data centers need power 24/7 and natural gas is the most reliable source\".",
 "1058363043622922": "\"Do you trust China with your data?\" Texas data centers \"keep American data in American hands\".",
 "1160273426235067": "Data centers \"can bring GOOD JOBS, property tax relief & energy investment to South Dakota\".",
 "1434338615267432": "Georgia Power is raising bills to \"overbuild expensive gas plants, largely to power data centers\".",
 "1550680310423772": "\"Behind every Texas data center is a welder, electrician or pipefitter\" earning a good living.",
 "1751481502753963": "As data centers drive up demand, \"the bills, and the risks, fall on to everyday families\".",
 "4301839766740670": "\"We're suing… xAI, for building an illegal power plant in Mississippi\" to fuel its data center.",
 "1810827893585871": "\"Dry air cooling in a closed loop\"; \"no added pressure on local water resources\" (no issue-ad label).",
 "2012700756027978": "\"These data centres will guzzle our water\" and fast-track fracking of underground reservoirs.",
 "1139512795232176": "Texas data centers keep data \"on Texas soil, and out of the hands of enemies like China\".",
 "2297263294527874": "\"Behind every Texas data center is a welder, electrician or pipefitter\" earning a good living.",
 "2275952023247967": "\"Blue states are blocking data centers.\" Texas \"is setting the standard for how they get built\".",
 "1385410257116629": "Data centers \"pay for their own power and water\", so the cost \"never lands on Texas families\".",
 "945807044879403": "\"Who knows how to build a data center the right way?\" Promotes local hiring and apprenticeships.",
 "1757093043083412": "\"Oklahoma set the rules for how it gets built here\" (no issue-ad label).",
 "1651691906330806": "\"Hundreds of good jobs, right here at home.\" Urges a No vote on the \"data center ban\".",
 "1336700171235689": "A tech company wants \"to sink an AI data center into Maine's coast\". One of 3 versions.",
 "1666627071854024": "\"$80 billion in tax breaks to data center developers\" while electric bills go up.",
 "1674590694098686": "Congressman \"took money from data center developers\" and voted for \"a $80 billion tax break\". Same script ran against at least six House members.",
 "940563782214883": "\"Duke Energy is recruiting data centers to justify new fossil fuel power plants\"; customers will pay.",
 "1112407328295851": "On data centers and chatbots, \"Americans should have a say\". Page name: 'Protect What's Human'.",
 "2306425966784285": "Husted calls Ohio a data center state; Ohioans got \"higher bills and lower property values\".",
 "1113746518099934": "\"Georgia gave up $474 million in one year\" because of data center tax breaks.",
}
for m in meta:
    if m["library_id"] in SHORT: m["text"] = SHORT[m["library_id"]]

# same rule for campaign entries and video key claims
_WM = "\"An independent study confirmed\"… data centers \"are paying their own energy costs\"; they \"may even help lower rates for everyone\""
SHORT_V = {"jgoi3ilu0mo": _WM, "9WjL1mNgkjY": _WM.replace("confirmed", "confirms"), "-qFK2gX70J8": _WM}
SHORT_C = {
 "GL-04": "\"We do not currently use water for cooling\" in any India data centre; returned 120% of water used",
 "OI-01": "\"Data centers need power 24/7 and natural gas is the most reliable source\"; \"Natural gas is America's affordability superpower\"",
 "OI-03": "\"Creating 100,000 jobs for Louisiana families\"; \"$2.8B in customer bill savings from data centers\"",
 "US-46": "\"Oklahomans wanted assurances data centers wouldn't impact ratepayers - now the law ensures they won't\"".replace("Oklahomans wanted assurances data centers wouldn't impact ratepayers - now the law ensures they won't", "Oklahomans wanted assurances\" on rates; \"now the law ensures they won't"),
 "GL-13": "\"Dry air cooling in a closed loop\"; \"no added pressure on local water resources\"",
 "GL-14": "Alberta \"limits data centres to industrial zones, puts them last for water\" and requires own power",
}
for v in videos:
    if v["youtube_id"] in SHORT_V: v["key_claim"] = SHORT_V[v["youtube_id"]]
for a in ads:
    if a["id"] in SHORT_C: a["claim"] = SHORT_C[a["id"]]
