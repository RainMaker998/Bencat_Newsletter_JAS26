"""
Step 2 - Build the newsletter HTML.
Usage:  python build_newsletter.py
Output: Bencat_Digital_Newsletter_JAS26.html  (single file, all photos embedded)

HOW TO EDIT
- Text/numbers: search this file for the section markers  # ===== 1. EXEC SUMMARY  etc.
- Photos: drop a file into ./images/ named exactly as the slot key (e.g. qa_alert_chat.jpg / .png).
  Missing photo -> dashed "Photo to add" placeholder.  Full slot list: see README.md
- Colors: palette constants right below.
"""
import base64, os, glob
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"Bencat_Digital_Newsletter_JAS26.html")

# ===== PALETTE
NAVY="#0B2545";BLUE="#0B5CAD";GREEN="#1E8E3E";ORANGE="#E06A10";PURPLE="#6B3FA0";TEAL="#0E9AA7";GREY="#4A5568";BG="#F2F5F9";GOLD="#FFC000";RED="#C62828"
F="font-family:'Segoe UI',Arial,sans-serif;"

# ===== HELPERS
_cache={}
def A(n):
    if n in _cache: return _cache[n]
    for ext in ("jpg","jpeg","png","webp"):
        p=os.path.join(HERE,"images",f"{n}.{ext}")
        if os.path.exists(p):
            mime="jpeg" if ext in("jpg","jpeg") else ext
            _cache[n]=f"data:image/{mime};base64,"+base64.b64encode(open(p,'rb').read()).decode(); return _cache[n]
    _cache[n]=None; return None

def slot(key,label,h=None,fit="cover",radius=10,extra="",bg="#fff"):
    d=A(key)
    if d:
        hh="auto" if h is None else f"{h}px"
        return (f'<div class="zoomwrap" style="border-radius:{radius}px;overflow:hidden;background:{bg};box-shadow:0 2px 8px rgba(11,37,69,.10);{extra}">'
                f'<img class="zoom" src="{d}" alt="{label}" title="Click to enlarge" style="display:block;width:100%;height:{hh};object-fit:{fit};object-position:center top;"></div>')
    h=h or 160
    return (f'<div style="position:relative;height:{h}px;border-radius:{radius}px;overflow:hidden;background:#E6ECF3;border:2px dashed #9AA8BC;{extra}">'
            f'<div style="position:absolute;inset:0;{F}color:#6B7A90;font-size:12px;text-align:center;display:flex;flex-direction:column;justify-content:center;padding:8px;">'
            f'<span style="font-size:20px;">&#128247;</span><b>{label}</b><span style="font-size:10.5px;">images/{key}.jpg</span></div></div>')
def gallery(prefix,label,main_h=170,thumb_h=60):
    # Collects images/<prefix>_01.jpg, <prefix>_02.jpg ... : first one big, the rest as thumbnails
    files=[]
    for ext in ("jpg","jpeg","png","webp"):
        files+=glob.glob(os.path.join(HERE,"images",f"{prefix}_*.{ext}"))
    keys=[os.path.splitext(os.path.basename(f))[0] for f in sorted(files)]
    if not keys: return slot(prefix,label,main_h)
    big=slot(keys[0],label,main_h,"cover",10)
    if len(keys)==1: return big
    thumbs="".join(f'<div style="flex:0 0 calc(25% - 5px);">{slot(k,label,thumb_h,"cover",6,"box-shadow:none;")}</div>' for k in keys[1:])
    return f'<div class="gal">{big}<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{thumbs}</div></div>'
def tbc(t): return f'<span style="background:#FFF3BF;color:#8A6D00;font-weight:600;padding:0 5px;border-radius:3px;font-size:.9em;">{t}</span>'
def pill(t,c): return f'<span style="display:inline-block;font-size:10.5px;font-weight:800;color:#fff;background:{c};border-radius:10px;padding:2px 9px;letter-spacing:.5px;">{t}</span>'
def sec(num,title,sub,c,id_=""):
    return f'''<div id="{id_}" style="display:flex;align-items:center;gap:12px;margin:38px 0 14px;">
<div style="width:40px;height:40px;border-radius:20px;background:{c};color:#fff;{F}font-weight:800;font-size:18px;text-align:center;line-height:40px;flex:none;">{num}</div>
<div><div style="{F}font-size:24px;font-weight:800;color:{NAVY};line-height:1.1;">{title}</div><div style="{F}font-size:13.5px;color:{GREY};">{sub}</div></div>
<div style="flex:1;height:2px;background:linear-gradient(90deg,{c},transparent);margin-left:10px;"></div></div>'''
def card(inner,border=None,bg="#fff",pad=18,extra=""):
    b=f"border-top:5px solid {border};" if border else "border:1px solid #DCE3EC;"
    return f'<div class="lift" style="background:{bg};{b}border-radius:12px;padding:{pad}px;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);{extra}">{inner}</div>'
def ul(items,size=13.5,color="#333F4F"):
    return f'<ul style="margin:6px 0 0;padding-left:18px;font-size:{size}px;color:{color};line-height:1.5;">'+"".join(f'<li style="margin:2px 0;">{i}</li>' for i in items)+'</ul>'
def kicker(t,c): return f'<div style="font-size:11px;font-weight:800;color:{c};letter-spacing:1.5px;">{t}</div>'
def h3(t,size=18): return f'<div style="font-size:{size}px;font-weight:800;color:{NAVY};margin:3px 0 4px;line-height:1.2;">{t}</div>'
def fromto(a,b): return f'<div style="font-size:13px;margin:2px 0 4px;"><span style="color:{RED};font-weight:700;">{a}</span> &rarr; <span style="color:{GREEN};font-weight:700;">{b}</span></div>'
def stat(v,l,c): return f'<div style="text-align:center;padding:8px 6px;"><div style="font-size:26px;font-weight:800;color:{c};line-height:1.1;">{v}</div><div style="font-size:11.5px;color:{GREY};font-weight:600;">{l}</div></div>'
def slicebtn(target,label,c=NAVY):
    return f'<button class="slice-btn" data-target="{target}" style="--c:{c};"><span class="blade">{RAZOR_ICON}</span> <span class="lbl">{label}</span> <span class="chev">&#9662;</span></button>'

RAZOR_ICON=('<svg class="rz" width="22" height="22" viewBox="0 0 36 36" style="vertical-align:-5px;"><g transform="rotate(-40 18 18)">'
 '<rect x="5" y="4" width="26" height="9" rx="2.5" fill="currentColor"/><rect x="7" y="5.5" width="22" height="2" rx="1" fill="#fff" opacity=".6"/>'
 '<rect x="7" y="10" width="22" height="1.4" fill="#fff" opacity=".8"/><rect x="16" y="13" width="4" height="20" rx="2" fill="#E06A10"/></g></svg>')

# ===== HERO
hero=f'''<div style="background:linear-gradient(120deg,#0B2545 0%,#0B5CAD 70%,#0E9AA7 100%);padding:40px 44px 34px;{F}position:relative;overflow:hidden;">
<div style="position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;border:40px solid rgba(255,255,255,.06);"></div>
<div style="position:absolute;right:120px;bottom:-90px;width:200px;height:200px;border-radius:50%;background:rgba(95,224,160,.10);"></div>
<div style="display:flex;justify-content:space-between;align-items:flex-start;">
<div style="font-size:12.5px;letter-spacing:4px;color:#7FD3FF;font-weight:700;">BENCAT DIGITAL NEWSLETTER</div>
<div style="text-align:right;"><div style="font-size:30px;font-weight:800;color:{GOLD};line-height:1;">JAS&rsquo;26</div><div style="font-size:12px;color:#C9D8EA;letter-spacing:2px;">JUL &ndash; SEP 2026</div></div></div>
<div style="display:flex;gap:30px;align-items:flex-end;margin-top:14px;">
<div style="flex:1.3;"><div style="font-size:44px;line-height:1.08;font-weight:800;color:#fff;">Digital Progress.<br>Real Impact.<br><span style="color:#5FE0A0;">A Stronger Bencat.</span></div>
<div style="font-size:15px;color:#C9D8EA;margin-top:14px;">From solid foundation to DUO scale &nbsp;&bull;&nbsp; <i>At Bencat, we strive to win</i></div>
<div class="hint">{RAZOR_ICON} Your cursor is a razor today &ndash; <b>shave</b> any button to open it, click any picture to see it bigger. Watch the hair fall!</div></div>
<div style="flex:1;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:14px 18px;color:#E6EEF8;font-size:13px;line-height:1.7;">
<div style="font-size:11px;letter-spacing:2px;color:{GOLD};font-weight:800;margin-bottom:4px;">IN THIS ISSUE</div>
<a class="toc" href="#s1">1 Executive Summary &amp; Control Tower</a><br><a class="toc" href="#s2">2 5 Impacts at a Glance</a><br><a class="toc" href="#s3">3 Key Deliverables</a><br>
<a class="toc" href="#s4">4 Emerging Skills &amp; Benchmark</a><br><a class="toc" href="#s5">5 Org Corner</a> &nbsp;&bull;&nbsp; <a class="toc" href="#s6">6 What&rsquo;s Next</a><br><a class="toc" href="#s7">7 One Winning Digital Team</a></div></div></div>'''

# ===== 1. EXEC SUMMARY
def kpi(v,l,s,c):
    return f'<div class="kpi lift" style="flex:1;background:#fff;border-radius:12px;border-top:5px solid {c};padding:14px 10px;text-align:center;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);"><div style="font-size:34px;font-weight:800;color:{c};line-height:1;">{v}</div><div style="font-size:11.5px;font-weight:800;color:{NAVY};letter-spacing:.6px;margin-top:4px;">{l}</div><div style="font-size:11.5px;color:{GREY};">{s}</div></div>'
LANDED=["<b>AI Assistant of Soft-service (BCSSE)</b> &ndash; live; bus &amp; dining answers in one chat",
"<b>Quality Alert Assistant</b> &ndash; live; QA DDS simplified",
"<b>M&#7855;t Th&#7847;n dev phase</b> &ndash; save 15&ndash;20 mins/FTE on daily loss analysis",
"<b>Utility eDDS</b> &ndash; live; ~1 hour/day saved for the utility team",
"<b>Foundation BOS Revamp</b> &ndash; eDDS data linkage fixed, new UI/UX (launch after KEA audit)",
"<b>FAM Digital Solution P1</b> &ndash; ready to roll out Oct&rsquo;26 to enhance stewardship",
"<b>Proficy PE Base &ndash; BLD</b> &ndash; configured for 100% of BLD machines"]
MOVING=["eKANBAN &ndash; JFM&rsquo;27","M&#7855;t Th&#7847;n production phase &ndash; OND&rsquo;26","Foundation Agent dev phase &ndash; OND&rsquo;26","Bootcamp S2 &ndash; 50% delivered (Create + Automate + Build)","Auto 6W2H infrastructure &ndash; OND&rsquo;26","PCS controlled-state dashboard P2 &ndash; OND&rsquo;26","WISE: VAC predictive maintenance &amp; Packing TD optimization &ndash; OND&rsquo;26","Production Monitoring Fusion/BLD &bull; CBM sitewide &ndash; OND&rsquo;26","Quality eDDS &ndash; OND&rsquo;26"]
watch=f'''<div style="font-size:13.5px;line-height:1.5;"><div style="background:#FFF4EC;border-left:4px solid {ORANGE};border-radius:8px;padding:12px 14px;">
<b style="color:{NAVY};font-size:15px;">Online PI/SPS data access for EOs</b><br>
<span style="color:{RED};">No API endpoint or application yet to connect and view PI/SPS data online &ndash; EOs still download data manually for offline use.</span><br>
<span style="color:{GREY};font-size:12.5px;">Next: waiting for platform response on a global solution.</span></div></div>'''
def panel(id_,title,sub,c,body):
    return f'''<div id="{id_}" class="panel"><div style="background:#fff;border-radius:12px;overflow:hidden;{F}box-shadow:0 2px 8px rgba(11,37,69,.08);border-top:5px solid {c};margin-top:12px;">
<div style="padding:12px 18px 4px;display:flex;justify-content:space-between;align-items:baseline;"><div style="font-size:16px;font-weight:800;color:{c};letter-spacing:1px;">{title}</div><div style="font-size:12px;color:{GREY};">{sub}</div></div>
<div style="padding:4px 18px 16px;">{body}</div></div></div>'''
def twocol(items):
    h=(len(items)+1)//2
    return f'<div style="display:flex;gap:20px;"><div style="flex:1;">{ul(items[:h],13)}</div><div style="flex:1;">{ul(items[h:],13)}</div></div>'
CT_ROWS=[("Machine Status (SeeQ / Grafana)",["BLD PRF ✔","BLD SHR/HRD ⏳","3B Assy / BAM","3B Assy / BAM"]),
("Alert List (SeeQ / Grafana)",["BLD PRF ✔","BLD SHR/HRD ⏳","3B Assy / BAM","3B Assy / BAM"]),
("Troubleshooting Guide (SeeQ / Grafana)",["BLD PRF, 2B Molding ✔","BLD SHR/HRD ⏳ + 2B Assy","3B Assy / BAM","3B Assy / BAM"]),
("CBM Dashboard (Power BI)",["BLD pilot ✔","BLD &amp; Fusion ✔","",""]),
("Production Monitoring 4h",["3B ✔","Fusion + BLD + 2B ⏳","",""]),
("Production Monitoring 30 mins",["","","VAC ⏳",""]),
("MTBT Dashboard",["3B pilot ✔","3B improve ⏳","Reapply across VS",""])]
def ctcell(t,i):
    if not t: return '<td style="padding:6px;border-bottom:1px solid #EDF1F6;"></td>'
    c=GREEN if ("&#10004;" in t or "✔" in t) else (BLUE if "⏳" in t else "#8FA3BC")
    return f'<td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;"><div class="chip" style="background:{c};color:#fff;border-radius:6px;padding:4px 6px;font-size:11.5px;font-weight:700;text-align:center;">{t}</div></td>'
ct="".join(f'<tr><td style="padding:6px 8px;font-size:12.5px;font-weight:700;color:{NAVY};border-bottom:1px solid #EDF1F6;">{n}</td>'+"".join(ctcell(t,i) for i,t in enumerate(v))+'</tr>' for n,v in CT_ROWS)
glide=card(f'''<div style="display:flex;gap:22px;align-items:flex-start;">
<div style="flex:0 0 250px;">{kicker("SEE &bull; CONTROL TOWER GLIDEPATH",TEAL)}{h3("Control Tower goes beyond Molding",20)}
<div style="font-size:13.5px;color:#333F4F;line-height:1.5;">Partnering with each value stream, the team brought <b>SeeQ live in BLD</b> and launched key <b>central dashboards</b> &ndash; CBM, Production Monitoring and MTBT &ndash; so every VS can <b>see, alert and act</b> faster.</div>
<div style="margin-top:10px;font-size:12.5px;color:{GREY};"><b style="color:{NAVY};">Help needed:</b> each VS to tell us what it wants to see, by when.</div>
<div style="margin-top:8px;font-size:11.5px;">{pill("LIVE",GREEN)} {pill("IN PROGRESS",BLUE)} {pill("PLANNED","#8FA3BC")}</div></div>
<div style="flex:1;"><table width="100%" cellpadding="0" cellspacing="0" style="{F}border-collapse:collapse;">
<tr><th style="text-align:left;font-size:11px;color:{GREY};padding:4px 8px;">CAPABILITY</th>'''+"".join(f'<th style="font-size:12px;color:#fff;background:{c};padding:6px;border-radius:6px 6px 0 0;">{q}</th>' for q,c in [("JAS&rsquo;26",GREEN),("OND&rsquo;26",BLUE),("JFM&rsquo;27","#8FA3BC"),("AMJ&rsquo;27","#8FA3BC")])+f'</tr>{ct}</table></div></div>',border=TEAL)
def tile(target,icon,num,label,sub,c):
    return f'''<button class="tile slice-btn" data-target="{target}" style="--c:{c};"><div style="display:flex;align-items:center;gap:12px;">
<div style="font-size:30px;font-weight:800;color:{c};line-height:1;">{num}</div><div style="text-align:left;"><div style="font-size:14px;font-weight:800;color:{NAVY};letter-spacing:1px;">{icon} {label}</div><div style="font-size:11.5px;color:{GREY};">{sub}</div></div>
<div class="chev" style="margin-left:auto;color:{c};">{RAZOR_ICON}</div></div></button>'''
exec_html=f'''{sec("1","Executive Summary","3 months. Fewer slides, more real life.",GREEN,"s1")}
<div style="display:flex;gap:18px;align-items:stretch;">
<div class="lift" style="flex:1.25;background:#fff;border-left:6px solid {GREEN};border-radius:12px;padding:18px 22px;{F}font-size:15.5px;line-height:1.6;color:#1F2937;box-shadow:0 2px 8px rgba(11,37,69,.06);">
In JAS&rsquo;26, <b>7 solutions were completed</b> and <b>80% of study-phase projects moved into execution</b>. AI is already saving effort: the <b>Quality Alert</b> and <b>Soft Service</b> assistants are live, and <b>M&#7855;t Th&#7847;n</b>, our first Reimagine DDS agent, has finished development and moves to production in OND&rsquo;26. <b>eDDS for GPO</b> is live for Utility and WH (RCCP measures). The <b>Site Control Tower</b> now reaches beyond Molding, with SeeQ live in BLD and central dashboards in more VS. <b>12 WISE ML use cases</b> have identified <b>$142.2M in potential savings</b> for the AugFF scope, and <b>simpler apps</b> (BENVOICE, Mover, BOS Revamp) make daily work easier. All of this runs on a solid foundation with <b>0 cyber incidents</b>.
<div style="margin-top:10px;font-size:13px;color:{GREEN};font-weight:700;font-style:italic;">Good news: projects are leaving PowerPoint and entering real life!</div></div>
<div style="flex:1;display:flex;flex-wrap:wrap;gap:10px;">
<div style="display:flex;gap:10px;width:100%;">{kpi("7","GO-LIVE / DONE","&#9650; +7 in JAS&rsquo;26",GREEN)}{kpi("9","ON TRACK","&#9650; +2 new requests",BLUE)}</div>
<div style="display:flex;gap:10px;width:100%;">{kpi("1","NEED ATTENTION","PI/SPS online access",ORANGE)}{kpi("~$200M","VALUE CREATION","in FY26-27 scope",PURPLE)}</div></div></div>
<div style="display:flex;gap:12px;margin-top:16px;">
{tile("pLanded","&#10004;","7","LANDED","Live / completed &ndash; shave to see",GREEN)}
{tile("pMoving","&#10148;","9","MOVING","On track &ndash; shave to see",BLUE)}
{tile("pWatch","&#9888;","1","WATCH","Need support &ndash; shave to see",ORANGE)}</div>
{panel("pLanded","&#10004; LANDED","Good news: projects have left PowerPoint and entered real life!",GREEN,twocol(LANDED))}
{panel("pMoving","&#10148; MOVING","On track to next milestone",BLUE,twocol(MOVING))}
{panel("pWatch","&#9888; WATCH","Dependency / need support",ORANGE,watch)}
<div style="margin-top:16px;">{glide}</div>'''

# ===== 2. 5 IMPACTS  (Foundation tall on the left, 2-5 in a 2x2 grid on the right)
def imp(n,title,c,head,items,extra=""):
    return f'''<div class="lift" style="background:#fff;border-radius:14px;padding:16px 18px;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);position:relative;overflow:hidden;height:100%;box-sizing:border-box;{extra}">
<div style="position:absolute;right:-6px;top:-22px;font-size:110px;font-weight:900;color:{c};opacity:.08;line-height:1;">{n}</div>
<div style="display:flex;align-items:center;gap:8px;"><div style="width:30px;height:30px;border-radius:8px;background:{c};color:#fff;font-weight:800;text-align:center;line-height:30px;">{n}</div><div style="font-size:12px;font-weight:800;letter-spacing:1.5px;color:{c};">{title}</div></div>
<div style="font-size:17px;font-weight:800;color:{NAVY};margin:8px 0 2px;line-height:1.25;">{head}</div>{ul(items,13)}</div>'''
i1=imp("1","FOUNDATION",NAVY,"Zero incidents. Zero compromise.",
 ["<b>0</b> cyber incidents","<b>EVP 100%</b> (+2% IYA)","Cyber DMS healthcheck <b>100%</b> (+2% IYA)","Strong progress on obsolete OS devices","Good track in Cyber DMS qualification","<b>Special thanks</b> to 2B, 3B, WH, Engineering (Utility, HSE) for their outstanding contribution in powering our EVP score",
  "<b>Opportunity:</b> application compliance <b>99%</b> (-1% IYA) &rarr; stronger myHub review ownership by business owners"],
 extra="background:linear-gradient(165deg,#fff 55%,#E9EEF6);")
i2=imp("2","VALUE CREATION",GREEN,"Data strategy built for <span style='color:#1E8E3E'>$0.2MM</span> hard savings in FY26/27",["Holistic data strategy &amp; building blocks for the <b>Unattended Operations</b> glidepath","<b>12 WISE use cases</b> &bull; 7 depts &bull; <b>$142.2M</b> quantified, supporting AugFF scope"])
i3=imp("3","PRODUCTIVITY &amp; CAPABILITY",BLUE,"From manual analysis to AI-assisted decisions",["<b>Control Tower beyond Molding</b>: SeeQ live in BLD, production monitoring scaling across VS","<b>M&#7855;t Th&#7847;n</b>: optimizes <b>3&ndash;4 FTE</b> site effort/day",
"Bencat locked into MVP scope of the <b>Global Real-time DDS Agent</b>","<b>Quality Alert AI Assistant</b>: optimizes <b>1.1 FTE</b> effort/day","<b>Utility eDDS</b> live: ~1 hr/day saved for the utility team","<b>Bootcamp S2</b> + hosting <b>WISE Advanced Qualification</b> (Dec&rsquo;26)"])
i4=imp("4","ANTI-FRAGILE &amp; IWS",ORANGE,"Digital Integrated Assessment: <span style='color:#E06A10'>96%</span>",["PRIME VM &amp; ALICS server refresh: capacity, availability, continuity","OctoPlant continuity toolkit adoption started","WH eDDS phase 2: RCCP measures live on DDS board"])
i5=imp("5","PEOPLE &bull; EVE &bull; SUSTAINABILITY",TEAL,"A self-sufficient team, a greener dashboard",["Smooth transition &amp; onboarding of new leader","Core team &amp; pillar members self-sufficient in O365 (Power BI / Apps / Automate) &amp; GenAI","Data activation for the sustainability (WAGES) dashboard &ndash; data validation in progress"])
impacts=f'''{sec("2","5 Impacts at a Glance","What JAS&rsquo;26 delivered for the business &ndash; aligned to Ben Cat CBN",PURPLE,"s2")}<div class="lift" style="background:#fff;border-radius:14px;padding:14px 18px;{F}display:flex;align-items:center;gap:8px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,37,69,.06);">{pill("1 FOUNDATION",NAVY)}{pill("2 VALUE CREATION",GREEN)}{pill("3 PRODUCTIVITY &amp; CAPABILITY",BLUE)}{pill("4 ANTI-FRAGILE &amp; IWS",ORANGE)}{pill("5 PEOPLE &bull; EVE &bull; SUSTAINABILITY",TEAL)}<div style="margin-left:auto;">{slicebtn("pImpacts","Shave to open the 5 impacts",PURPLE)}</div></div>
<div id="pImpacts" class="panel"><div style="padding-top:14px;">
<div style="display:grid;grid-template-columns:0.9fr 1fr 1fr;grid-template-rows:auto auto;gap:14px;">
<div style="grid-row:1/3;grid-column:1;">{i1}</div><div>{i2}</div><div>{i3}</div><div>{i4}</div><div>{i5}</div></div>
<div class="lift" style="margin-top:14px;background:{NAVY};border-radius:12px;padding:12px 20px;{F}color:#fff;display:flex;align-items:center;gap:16px;font-size:13px;">
<b style="color:{GOLD};letter-spacing:2px;font-size:12px;flex:none;">THE ROAD TO DUO</b>
<span>1 Solid Data Foundations</span><span style="color:#7FD3FF;">&#10140;</span><span>2 Data Activation Enablement</span><span style="color:#7FD3FF;">&#10140;</span><span>3 AI &amp; Agentic Operations</span><span style="color:#7FD3FF;">&#10140;</span><b style="color:#5FE0A0;">Unattended Operations</b>
<i style="margin-left:auto;color:#C9D8EA;">Data first &ndash; then AI.</i></div></div></div>'''

# ===== 3. KEY DELIVERABLES
SUPERPOWERS=[("Ask before it acts","Confirms line, shift, time window before pulling any number"),("Finds the real bottleneck","Ranks losses, spots recurring stops"),("Thinks &amp; uses tools","Reasons step-by-step, picks the right tool"),("Sees the whole site","Site-wide loss portfolio at a glance"),("Digs into the details","By machine, cause, time &ndash; the why"),("Answers &ldquo;What if?&rdquo;","Tests scenarios before you commit")]
spg="".join(f'<div class="power"><div style="font-size:13px;font-weight:800;color:{GOLD};">{a}</div><div style="font-size:11.5px;color:#C9D8EA;line-height:1.35;">{b}</div></div>' for a,b in SUPERPOWERS)
VALIDATION=[("Composite score","0.969","&ge;0.90"),("Bottleneck accuracy","12/12","&ge;95%"),("Numerical accuracy &plusmn;1%","11/11","&ge;99%"),("Loss ranking","12/12","&ge;90%"),("Recommendation quality","4.33/5","&ge;4.0"),("Trust / usefulness","4.08/5","&ge;4.0"),("Behaviour checks","60/60","All")]
vt="".join(f'<tr><td style="padding:4px 6px;color:#E6EEF8;">{a}</td><td style="padding:4px 6px;color:#fff;font-weight:800;text-align:right;">{b}</td><td style="padding:4px 6px;color:#8FA3BC;text-align:right;">{c}</td><td style="padding:4px 6px;text-align:right;"><span style="color:#5FE0A0;font-weight:800;">PASS</span></td></tr>' for a,b,c in VALIDATION)
matthan=f'''<div class="lift" style="background:linear-gradient(135deg,#071A33,#0B2545 55%,#13325C);border-radius:16px;padding:22px;{F}color:#fff;box-shadow:0 4px 16px rgba(11,37,69,.25);">
<div style="display:flex;gap:20px;">
<div style="flex:0 0 210px;">{slot("matthan_logo","M&#7855;t Th&#7847;n logo",None,"contain",12,"",bg="#0B1C33")}
<div style="margin-top:12px;display:grid;gap:8px;">
<div style="background:rgba(95,224,160,.12);border-radius:8px;padding:8px 10px;font-size:12.5px;"><b style="color:#5FE0A0;font-size:16px;">100%</b> trusted data from iODS (1% variance vs eDDS) &bull; no hallucination</div>
<div style="background:rgba(127,211,255,.12);border-radius:8px;padding:8px 10px;font-size:12.5px;"><b style="color:#7FD3FF;font-size:16px;">&le;60s</b> response (p95)</div>
<div style="background:rgba(255,192,0,.12);border-radius:8px;padding:8px 10px;font-size:12.5px;"><b style="color:{GOLD};font-size:16px;">3&ndash;4 FTE</b> site effort optimized / day</div></div></div>
<div style="flex:1;">
<div style="display:flex;justify-content:space-between;align-items:center;">{kicker("TRANSFORM &bull; AGENTIC AI &bull; REIMAGINED DDS",GOLD)}{pill("DEV DONE &bull; PRODUCTION OND&rsquo;26",GREEN)}</div>
<div style="font-size:26px;font-weight:800;margin:4px 0 2px;">M&#7855;t Th&#7847;n &ndash; One Agent, Six Superpowers</div>
<div style="font-size:13.5px;margin-bottom:12px;"><span style="color:#FF8A80;font-weight:700;">Hours of manual loss analysis</span> &rarr; <span style="color:#5FE0A0;font-weight:700;">answers in &le;60 seconds</span> &nbsp;&bull;&nbsp; save 15&ndash;20 mins/FTE daily</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">{spg}</div>
<div style="margin-top:14px;">{slicebtn("pMT","Shave to see lead-user validation, recognition &amp; superusers",GOLD)}</div>
<div id="pMT" class="panel"><div style="display:flex;gap:16px;margin-top:12px;">
<div style="flex:1.1;"><div style="font-size:11.5px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;">VALIDATED BY LEAD USERS &ndash; 128 PROMPTS &bull; 12 USERS &bull; 5 VS</div>
<table width="100%" style="font-size:12px;border-collapse:collapse;margin-top:4px;">{vt}</table></div>
<div style="flex:1;font-size:12.5px;line-height:1.5;">
<div style="font-size:11.5px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;">GOING BEYOND BENCAT</div>
<b style="color:{GOLD};">GSMC</b> &ndash; recognition for the agentic AI DDS walkthrough<br><b style="color:{GOLD};">Berlin</b> &ndash; seen as a reusable framework for other sites<br><b style="color:#5FE0A0;">Next:</b> scale with Grooming Digital team; Phase 2 = Dept/Tech knowledge base, integrate with quality alert data and daily auto report
<div style="font-size:11.5px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;margin-top:10px;">SINCERE THANKS TO SUPERUSERS</div>
<span style="color:#C9D8EA;">Stefan, chi Nhung, anh Ky &bull; anh Phuong, anh Viet &bull; anh Phat &bull; anh Tuyen, anh Thuong (3B), anh Hoang (BLD), anh Nghia (2B)</span></div></div></div></div></div>
<div style="display:flex;gap:12px;margin-top:14px;align-items:flex-start;">
<div style="flex:1.1;"><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;margin-bottom:6px;">LIVE ANSWER: TOP 3 MACHINES BY WEIGHTED IMPACT</div>{slot("matthan_chat","M&#7855;t Th&#7847;n chat screenshot",230,"cover",10,"",bg="#fff")}</div>
<div style="flex:1;"><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;margin-bottom:6px;">GSMC RECOGNITION</div>{slot("gsmc_recognition","GSMC recognition",230,"contain",10,"",bg="#fff")}</div>
<div style="flex:1;"><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:#7FD3FF;margin-bottom:6px;">BERLIN WALKTHROUGH</div>{slot("berlin_walkthrough","Berlin walkthrough",230,"cover",10,"",bg="#fff")}</div></div></div>'''

edds=card(f'''<div style="display:flex;gap:18px;">
<div style="flex:0 0 320px;">{kicker("SEE &bull; eDDS CUSTOM FOR GPO",TEAL)}{h3("eDDS Custom for GPO &ndash; One DDS Board per Function",20)}
{fromto("Scattered GPO data, manual checks","one eDDS board per function")}
<div style="display:grid;gap:8px;margin-top:8px;font-size:13px;">
<div style="border-left:4px solid {GREEN};background:#F0F8F2;border-radius:6px;padding:8px 10px;"><b style="color:{NAVY};">Utility eDDS</b> {pill("LIVE",GREEN)}<br><span style="color:{GREY};">Utility measures configured into the DDS board &ndash; energy per good/scrap, power by equipment, uptime/downtime consumption, compressed air.</span><br><b style="color:{GREEN};font-size:14px;">&#9201; ~1 hour/day saved for the utility team</b></div>
<div style="border-left:4px solid {PURPLE};background:#F6F2FB;border-radius:6px;padding:8px 10px;"><b style="color:{NAVY};">Quality (QA) eDDS</b> {pill("OND&rsquo;26",BLUE)}<br><span style="color:{GREY};">Configure QA measures into the DDS board</span></div>
<div style="border-left:4px solid {GREEN};background:#F0F8F2;border-radius:6px;padding:8px 10px;"><b style="color:{NAVY};">WH eDDS phase 2 &ndash; RCCP</b> {pill("LIVE",GREEN)}<br><span style="color:{GREY};">RCCP visualization on the DDS board: hot-room capacity, insert monitoring, WH area C/D &amp; empty locations</span></div></div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:10px;">
<div><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:{GREEN};margin-bottom:4px;">UTILITY eDDS &ndash; LIVE</div>{slot("utility_edds","Utility eDDS",None,"contain",10,"border:1px solid #DCE3EC;")}</div>
<div><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:{GREEN};margin-bottom:4px;">WH eDDS PHASE 2 + RCCP &ndash; LIVE</div>{slot("rccp_whedds","WH eDDS + RCCP",None,"contain",10,"border:1px solid #DCE3EC;")}</div></div></div></div>''',border=TEAL)

tl="".join(f'<td style="text-align:center;font-size:11px;color:{GREY};padding-top:4px;">{d}</td>' for d in range(10,18))
vac=card(f'''<div style="display:flex;justify-content:space-between;">{kicker("OPTIMIZE &bull; WISE AI/ML",GREEN)}{pill("PILOT &bull; REDPACK 1",GREEN)}</div>
{h3("VAC Slip4way Predictive Maintenance")}{fromto("Unplanned maintenance cycles","AI-enabled, right-time replacement")}
<div style="display:flex;gap:6px;margin:8px 0;">{stat("$7M","savings / year",GREEN)}{stat("75%","faster response<br>100 &rarr; 25 mins",BLUE)}{stat("&plusmn;3 days","prediction variance",ORANGE)}</div>
<table width="100%" cellpadding="0" cellspacing="0" style="{F}"><tr><td colspan="8" style="padding:0;"><div style="position:relative;height:30px;background:#EEF2F7;border-radius:6px;">
<div style="position:absolute;left:12.5%;width:37.5%;top:4px;bottom:4px;background:#FFE3B3;border:1px solid #E0A030;border-radius:4px;font-size:10.5px;font-weight:700;color:#8A5A00;text-align:center;line-height:20px;">Predicted 11&ndash;13 Aug</div>
<div style="position:absolute;left:75%;width:12.5%;top:4px;bottom:4px;background:{GREEN};border-radius:4px;font-size:10.5px;font-weight:700;color:#fff;text-align:center;line-height:20px;">16 Aug</div></div></td></tr><tr>{tl}</tr></table>
<div style="font-size:12.5px;color:#333F4F;margin-top:6px;">Collect &rarr; Learn &rarr; <b>Predict</b> &rarr; Act &rarr; Monitor. Replacement combined with changeover; less manual monitoring.</div>
<div style="display:flex;gap:10px;margin-top:10px;align-items:center;"><div style="flex:0 0 140px;">{slot("vac_rtd","Slip ring / RTD",105,"contain",10,"",bg="#000")}</div><div style="flex:1;font-size:12.5px;color:#333F4F;line-height:1.45;"><b style="color:{NAVY};">What this proves</b><br>&#10004; Actionable warning ahead of failure<br>&#10004; Practical foundation for proactive maintenance</div></div><div style="margin-top:12px;font-size:11px;font-weight:800;letter-spacing:1.5px;color:{BLUE};">NEXT STEPS</div>
<div style="display:grid;gap:6px;margin-top:6px;font-size:12.5px;color:#333F4F;">
<div style="display:flex;align-items:center;gap:10px;background:#F2F7FD;border-left:4px solid {BLUE};border-radius:6px;padding:8px 10px;"><div style="flex:1;">Continue validating the model on other <b>Redpack machines</b></div>{pill("DEC&rsquo;26",BLUE)}</div>
<div style="display:flex;align-items:center;gap:10px;background:#F2F7FD;border-left:4px solid {BLUE};border-radius:6px;padding:8px 10px;"><div style="flex:1;">Integrate breakdown prediction into the <b>Packing Command Center</b></div>{pill("AMJ&rsquo;27","#8FA3BC")}</div>
</div>''',border=GREEN)
funnel="".join(f'<div style="margin:3px auto;width:{w}%;background:{c};color:#fff;border-radius:5px;font-size:11.5px;font-weight:700;text-align:center;padding:4px 0;">{t}</div>' for w,c,t in [(100,"#5B7FB5","Many TD candidates"),(82,"#4A6FA5","Feasible fits"),(64,"#3A5F95","Similar groups"),(46,"#2A4F85","Golden TDs"),(30,GREEN,"Lowest E2E cost")])
td=card(f'''<div style="display:flex;justify-content:space-between;">{kicker("OPTIMIZE &bull; WISE AI/ML",GREEN)}{pill("PILOT",GREEN)}</div>
{h3("Packaging TD Optimization")}{fromto("Manual packaging selection","AI-proposed golden TD &amp; cost optimization")}
<div style="display:flex;gap:14px;margin-top:8px;"><div style="flex:1;">{funnel}</div>
<div style="flex:1;">{stat("30&ndash;50%","fewer TD variants",GREEN)}<div style="font-size:12.5px;color:#333F4F;line-height:1.45;">Find minimal box sizes &rarr; group by similarity &rarr; select golden primary TD &rarr; business options &rarr; end-to-end cost</div></div></div>
<div style="font-size:12.5px;color:#333F4F;margin-top:8px;"><b>Value:</b> less packaging complexity, more standardization, lower material, warehousing &amp; logistics cost.</div>
<div style="margin-top:10px;">{slot("td_optimization","TD optimization visual",None,"contain",10,"border:1px solid #DCE3EC;")}</div><div style="margin-top:12px;font-size:11px;font-weight:800;letter-spacing:1.5px;color:{BLUE};">NEXT STEPS</div>
<div style="display:grid;gap:6px;margin-top:6px;font-size:12.5px;color:#333F4F;">
<div style="display:flex;align-items:center;gap:10px;background:#F2F7FD;border-left:4px solid {BLUE};border-radius:6px;padding:8px 10px;"><div style="flex:1;">Validate the model with <b>TechHub</b></div>{pill("NOV&rsquo;26",BLUE)}</div>
<div style="display:flex;align-items:center;gap:10px;background:#F2F7FD;border-left:4px solid {BLUE};border-radius:6px;padding:8px 10px;"><div style="flex:1;">Build the <b>AI app for end users</b></div>{pill("JFM&rsquo;27","#8FA3BC")}</div>
</div>''',border=GREEN)
wise_card=card(f'''<div style="display:flex;justify-content:space-between;align-items:flex-end;"><div>{kicker("OPTIMIZE &bull; WISE PROGRAM",GREEN)}{h3("12 WISE use cases powering AugFF scope delivery",20)}</div>{pill("WEEK 13",TEAL)}</div>
<div style="margin-top:8px;">{slot("wise_usecases","WISE use cases",None,"contain",10)}</div>''',border=GREEN)
soft=card(f'''<div style="display:flex;gap:20px;align-items:flex-start;">
<div style="flex:0 0 300px;">{slot("softservice_chat","BCSSE AI Assistant launch poster",430,"cover",12,"border:1px solid #DCE3EC;")}</div>
<div style="flex:1;">
<div style="display:flex;justify-content:space-between;">{kicker("PEOPLE &bull; AI ASSISTANT",TEAL)}{pill("LIVE &bull; NEW VERSION 8 AUG&rsquo;26",GREEN)}</div>
{h3("BCSSE &ndash; BenCat Soft Service Expert AI Assistant",21)}
{fromto("Asking around for bus &amp; canteen info","one AI assistant, fast &ndash; accurate &ndash; friendly")}
<div style="font-size:13.5px;color:#333F4F;line-height:1.5;margin-top:6px;">The new version <b>combines Bencat Bus &amp; Dining Service</b> in one chat &ndash; lifting <b>GPO productivity</b> and <b>people experience</b>.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px;font-size:12.5px;">
<div class="mini">&#128652; <b>Bus info</b><br>Routes, pickup points, departure times, delays</div>
<div class="mini">&#127860; <b>Dining info</b><br>Menus, meal times, favorite dishes</div>
<div class="mini">&#128179; <b>Meal policy</b><br>Allowance, rules, visitor meals</div>
<div class="mini">&#127978; <b>Minishop</b><br>Prices, promotions, locations</div></div>
<div style="margin-top:12px;background:#EEF7F8;border-radius:10px;padding:10px 14px;font-size:12.5px;color:#333F4F;">
<b style="color:{TEAL};letter-spacing:1px;">HOW TO USE</b><br>chatPG &rarr; Explore AI Hub &rarr; search <b>&ldquo;BC Soft Service Expert&rdquo;</b> &rarr; start chatting</div>
<div style="margin-top:12px;font-size:11px;font-weight:800;letter-spacing:1.5px;color:{TEAL};">KEY BENEFITS</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px;font-size:12.5px;color:#333F4F;">
<div class="mini">&#10004; <b>One place, all answers</b></div>
<div class="mini">&#10004; <b>Instant &amp; accurate 24/7</b></div>
<div class="mini">&#10004; <b>Personalized for you</b></div>
<div class="mini">&#10004; <b>Always up-to-date</b></div>
</div>
<div style="margin-top:8px;background:{GREEN};color:#fff;border-radius:10px;padding:10px 14px;font-size:14px;font-weight:800;">&#9201; Optimizes 30 mins/day for each admin</div></div></div>''',border=TEAL)
qa=card(f'''<div style="display:flex;justify-content:space-between;">{kicker("PRODUCTIVITY &bull; AI ASSISTANT",BLUE)}{pill("LIVE",GREEN)}</div>{h3("Quality Alert Assistant")}
<div style="font-size:13px;color:#333F4F;line-height:1.5;">A <b>platinum partnership</b> between QA and Digital brought an AI-powered assistant into <b>QA DDS simplification</b>. 100% completion.</div>
<div style="font-size:12.5px;margin-top:6px;"><b style="color:#1E8E3E;">&#9201; Optimizes ~1.1 FTE effort/day</b></div><div style="margin-top:10px;">{slot("qa_alert_chat","AI chatbox example",170)}</div>''',border=BLUE)
pe=card(f'''<div style="display:flex;justify-content:space-between;">{kicker("FOUNDATION &bull; DATA",NAVY)}{pill("DONE",GREEN)}</div>{h3("Proficy PE Base &ndash; BLD")}
<div style="font-size:13px;color:#333F4F;line-height:1.5;">Configured for <b>100% of BLD machines</b>. Activates production &amp; Proficy data and simplifies the healthcheck process.</div>
<div style="font-size:12.5px;margin-top:6px;">Soft savings: <b style="color:#1E8E3E;">$110M USD</b></div><div style="margin-top:10px;">{slot("pebase_timeline","PE Base timeline view",170,"cover",10,"border:1px solid #DCE3EC;")}</div>''',border=NAVY)
def app(f1,f2,name,tag,c,status):
    return f'''<div style="flex:1;"><div style="display:flex;gap:8px;align-items:flex-start;"><div style="flex:1;">{slot(f1,name,230,"contain",10,"border:1px solid #DCE3EC;")}</div><div style="flex:1;">{slot(f2,name,230,"contain",10,"border:1px solid #DCE3EC;")}</div></div><div style="margin-top:8px;"><b style="font-size:14.5px;color:{NAVY};">{name}</b> {pill(status,c)}<div style="font-size:12.5px;color:{GREY};">{tag}</div></div></div>'''
simp=card(f'''<div style="display:flex;justify-content:space-between;align-items:flex-end;"><div>{kicker("SIMPLIFY &bull; FEWER APPS, FASTER FLOWS",TEAL)}{h3("Three apps. Fewer clicks. Happier users.",20)}</div>
<div style="font-size:12.5px;color:{GREY};">Built by Digital &times; GPO superusers</div></div>
<div style="display:flex;gap:14px;margin-top:10px;">
{app("benvoice","benvoice2","BENVOICE","&ldquo;&#272;&agrave;i ti&#7871;ng n&oacute;i Bencat&rdquo; &ndash; one central feedback channel",GREEN,"LIVE")}
{app("mover_apps","mover2","Mover Apps","Faster flows, more secure &bull; ~0.2 FTE",GREEN,"LIVE")}
{app("bos_logo","bos_revamp","BOS Apps Revamp","Faster loading, no missing eDDS",PURPLE,"LAUNCH NOV&rsquo;26")}</div>''',border=TEAL)
secure=f'''<div style="display:flex;gap:16px;align-items:stretch;">
<div class="lift" style="flex:1;background:#fff;border:2px solid {NAVY};border-top:6px solid {NAVY};border-radius:12px;padding:18px;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);">
{kicker("SECURE &bull; CYBER INITIATIVES &amp; FOUNDATION",NAVY)}{h3("Zero incident. Zero compromise.")}
<div style="display:flex;gap:6px;">{stat("0","cyber incidents",GREEN)}{stat("100%","EVP (+2% IYA)",BLUE)}{stat("99%","app compliance",ORANGE)}</div>
{ul(["<b>Cyber Program</b>: 100% Cyber DMS qualification glidepath (AMJ&rsquo;27) &ndash; Basic &amp; Intermediate tracks","<b>Cyber Month 2026</b>: 3 weekly games + booth game at plant canteen; employees share real stories on Viva Engage","<b>Special thanks</b> to 2B, 3B, WH, Engineering (Utility, HSE) for their outstanding contribution in powering our EVP score"],12.5)}
<div style="margin-top:10px;">{slot("cyber_foundation","Cyber initiatives visual",None,"contain",10,"border:1px solid #DCE3EC;")}</div></div>
<div class="lift" style="flex:1;background:#FFF9F4;border:2px solid {ORANGE};border-top:6px solid {ORANGE};border-radius:12px;padding:18px;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);">
{kicker("ANTI-FRAGILE &bull; IT INFRASTRUCTURE READINESS",ORANGE)}{h3("Built to keep running")}
{ul(["<b>PRIME virtual machine ready &amp; ALICS server refresh</b> (FY26/27): expand capacity, increase availability &amp; continuity, foundation for unattended ops &amp; AI","<b>Digital Continuity Toolkit &ndash; OctoPlant</b>: PLC programming backup for critical systems; drill tests on eCS / PRIME OND&rsquo;26 &ndash; JFM&rsquo;27","Digital Integrated Assessment re-scored at <b>96%</b>"],12.5)}
<div style="margin-top:10px;">{slot("prime_alics","PRIME / ALICS refresh",None,"contain",10,"border:1px solid #DCE3EC;")}</div></div></div>
<div class="lift" style="margin-top:16px;background:#fff;border:2px solid {NAVY};border-top:6px solid {NAVY};border-radius:12px;padding:18px;{F}box-shadow:0 2px 8px rgba(11,37,69,.06);">
{kicker("SECURE &bull; BEN CAT CYBER MONTH 2026",NAVY)}{h3("Small actions. A safer Ben Cat.")}
<div style="display:flex;gap:14px;align-items:flex-start;margin-top:6px;">
<div style="flex:1;"><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:{NAVY};margin-bottom:4px;">CYBERSECURITY MONTH PLAN</div>{slot("cyber_month","Cyber Month plan",None,"contain",10,"border:1px solid #DCE3EC;")}</div>
<div style="flex:1;"><div style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:{NAVY};margin-bottom:4px;">CYBER MONTH GAME</div>{slot("cyber_game","Cyber Month game photo",None,"contain",10,"border:1px solid #DCE3EC;")}</div>
</div></div>'''
deliv=f'''{sec("3","Key Deliverables","From ideas to everyday impact &ndash; click any picture to see it bigger",ORANGE,"s3")}<div class="lift" style="background:#fff;border-radius:14px;padding:14px 18px;{F}display:flex;align-items:center;gap:8px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,37,69,.06);">{pill("M&#7855;T TH&#7846;N",PURPLE)}{pill("eDDS FOR GPO",TEAL)}{pill("BCSSE",TEAL)}{pill("WISE ML",GREEN)}{pill("QA ALERT",BLUE)}{pill("PE BASE",NAVY)}{pill("APPS",TEAL)}<div style="margin-left:auto;">{slicebtn("pDeliv","Shave to open key deliverables",ORANGE)}</div></div>
<div id="pDeliv" class="panel"><div style="padding-top:14px;">

{matthan}
<div style="margin-top:16px;">{edds}</div>
<div style="margin-top:16px;">{soft}</div>
<div style="display:flex;gap:16px;margin-top:16px;"><div style="flex:1.1;">{vac}</div><div style="flex:1;">{td}</div></div>
<div style="margin-top:16px;">{wise_card}</div>
<div style="display:flex;gap:16px;margin-top:16px;"><div style="flex:1;">{qa}</div><div style="flex:1;">{pe}</div></div>
<div style="margin-top:16px;">{simp}</div>
<div style="margin-top:16px;">{secure}</div></div></div>'''

# ===== 4. EMERGING SKILLS & BENCHMARK
skills=f'''{sec("4","Emerging Skills &amp; Benchmark","Building digital muscle at scale",GREEN,"s4")}<div class="lift" style="background:#fff;border-radius:14px;padding:14px 18px;{F}display:flex;align-items:center;gap:8px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,37,69,.06);">{pill("BOOTCAMP S2",GREEN)}{pill("DIGITAL ACADEMY",BLUE)}{pill("WISE ADVANCED COACH",PURPLE)}{pill("VN PS BENCHMARK",ORANGE)}<div style="margin-left:auto;">{slicebtn("pSkills","Shave to open skills &amp; benchmark",GREEN)}</div></div>
<div id="pSkills" class="panel"><div style="padding-top:14px;">
<div style="display:flex;gap:16px;">
<div style="flex:0 0 300px;">{slot("bootcamp_s2_poster","Bootcamp S2 poster",None,"contain",12,"border:1px solid #DCE3EC;")}</div>
<div style="flex:1;display:flex;flex-direction:column;gap:14px;">
{slot("fy2627_emerging_capability","FY26/27 Emerging Capability",None,"contain",12)}
<div style="display:flex;gap:12px;">
{card(f'{kicker("DATA ACTIVATION BOOTCAMP S2",GREEN)}<div style="font-size:12.5px;color:#333F4F;line-height:1.45;margin-top:4px;">Automate (Sep 10) &bull; Build (Sep 11) &bull; Create (Oct 1&ndash;2) &bull; Analyze (Oct 8&ndash;9). <b>50% delivered</b>.</div>',extra="flex:1;padding:12px;")}
{card(f'{kicker("GROOMING DIGITAL ACADEMY",BLUE)}<div style="font-size:12.5px;color:#333F4F;line-height:1.45;margin-top:4px;">Learn &ndash; Qualify &ndash; Actualize: Create &bull; Analyze &bull; Automate &bull; Build &bull; Transform.</div>',extra="flex:1;padding:12px;")}
{card(f'{kicker("WISE ADVANCED COACH",PURPLE)}<div style="font-size:12.5px;color:#333F4F;line-height:1.45;margin-top:4px;">APAC regional hosting with Corporate Engineering, Dec&rsquo;26 &ndash; scale analytics &amp; AI across APAC.</div>',extra="flex:1;padding:12px;")}
</div></div></div>
<div style="display:flex;gap:16px;margin-top:16px;align-items:stretch;">
<div style="flex:1;transform:rotate(-1.2deg);">{slot("benchmark_vnps","Vietnam PS benchmarking photo",330,"cover",12,"border:6px solid #fff;box-shadow:0 6px 18px rgba(0,0,0,.18);")}</div>
<div style="flex:1.15;">{card(f"""{kicker("BENCHMARK &bull; VIETNAM PS DIGITAL &bull; AUG&rsquo;26",PURPLE)}{h3("5 ideas we bring home")}
<table width="100%" style="font-size:12.5px;border-collapse:collapse;color:#333F4F;">
<tr><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;"><b>1</b> One-touch laptop auto-scan</td><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;color:{GREY};">Faster gate flow, EVE + cyber</td></tr>
<tr><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;"><b>2</b> Proficy MCT for material handling</td><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;color:{GREY};">~30&ndash;60 mins/EO/shift (up to 60&ndash;120 in grooming)</td></tr>
<tr><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;"><b>3</b> Academy approach to training</td><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;color:{GREY};">Scale digital capability</td></tr>
<tr><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;"><b>4</b> Data activation for IT Command Center</td><td style="padding:5px 4px;border-bottom:1px solid #EDF1F6;color:{GREY};">Simplify Digital Operation DDS</td></tr>
<tr><td style="padding:5px 4px;"><b>5</b> WISE: prepare use cases before Dec&rsquo;26 workshop</td><td style="padding:5px 4px;color:{GREY};">Max AI/ML learning, min travel cost</td></tr></table>""",border=PURPLE,extra="height:100%;box-sizing:border-box;")}</div></div></div></div>'''

# ===== 5. ORG CORNER
orgc=f'''{sec("5","People &bull; EVE &bull; Sustainability","Recognition, energy &amp; a greener Ben Cat",TEAL,"s5")}<div class="lift" style="background:#fff;border-radius:14px;padding:14px 18px;{F}display:flex;align-items:center;gap:8px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,37,69,.06);">
{pill("WAGES DASHBOARD",GREEN)}
{pill("R&amp;R",ORANGE)}
{pill("HAPPY HOURS",PURPLE)}
<div style="margin-left:auto;">{slicebtn("pPeople","Shave to open People, EVE &amp; Sustainability",TEAL)}</div>
</div>
<div id="pPeople" class="panel"><div style="padding-top:14px;">
<div style="display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:14px;margin-top:16px;">
<div>{card(f'{kicker("SUSTAINABILITY",GREEN)}{h3("WAGES Dashboard",16)}<div style="font-size:12.5px;color:#333F4F;">Data activation completed to visualize sustainability measures.<div style="margin-top:6px;">{pill("IN PROGRESS",ORANGE)} <span style="font-size:12px;color:#E06A10;font-weight:700;">Data validation in progress</span></div></div><div style="margin-top:8px;">{slot("wages_dashboard","WAGES dashboard",150)}</div>',border=GREEN)}</div>
<div style="transform:rotate(1.5deg);margin-top:8px;">{card(f'{kicker("R&amp;R",ORANGE)}{h3("Monthly &amp; Quarterly R&amp;R",16)}<div style="margin-top:6px;">{gallery("rr","R&amp;R photos",170)}</div>',border=ORANGE)}</div>
<div style="transform:rotate(-1.5deg);">{card(f'{kicker("HAPPY HOURS",PURPLE)}{h3("&ldquo;Food for Thoughts&rdquo;",16)}<div style="font-size:12.5px;color:#333F4F;">Our drumbeat to refuel energy and share learnings.</div><div style="margin-top:6px;">{gallery("happy_hours","Happy Hours photo",150)}</div>',border=PURPLE)}</div></div></div></div>'''

# ===== 6. WHAT'S NEXT & HELP NEEDED
NEXT_OND=[
("Agentic AI",PURPLE,["<b>M&#7855;t Th&#7847;n</b> (Gap Analysis Agent) to production phase &ndash; roll out to team leader group",
 "Integrate <b>Quality Alert</b> data into M&#7855;t Th&#7847;n",
 "Partner with Global to configure data &amp; feedback UI in the <b>Global Real-time DDS Agent</b>"]),
("Control Tower",TEAL,["Production Monitoring &amp; CBM reapplied sitewide",
 "MTBT improved &amp; reapplied sitewide",
 "Validate data accuracy in the <b>WAGES</b> dashboard",
 "Troubleshooting guide + Alert list in <b>BLD SHR/HRD</b>"]),
("Apps",BLUE,["Adopt the <b>eKANBAN</b> solution",
 "<b>Auto 6W2H</b> configuration",
 "<b>Global Real-time DDS Agent</b> configuration",
 "<b>FAM</b> phase 1 roll-out",
 "<b>BOS Revamp</b> launch",
 "<b>BENVOICE</b>: UI for form owners to manage tickets"]),
("WISE Program",GREEN,["Validate <b>VAC Predictive Maintenance</b> &amp; <b>Packing TD optimization</b>",
 "Host the <b>WISE workshop</b> in Dec&rsquo;26"]),
("eDDS for GPO",ORANGE,["<b>Quality eDDS</b> goes live",
 "<b>Utility eDDS</b> phase 2 study"]),
("Capability",NAVY,["<b>Bootcamp Season 2</b> completion",
 "Grow <b>Citizen Developers &amp; Qualifiers</b> across VS"])]
LT_HELP=["Invest time for <b>TPE &amp; LL</b> to build the troubleshooting agent in the <b>Auto 6W2H</b> solution",
"Invest time for employees to join <b>Bootcamp</b> &amp; <b>WISE Advanced Qualification</b>",
"Re-check <b>WISE use cases</b> against each department&rsquo;s top losses",
"Tell us what each VS needs in its <b>Control Tower</b> beyond the current portfolio",
"Drive <b>myHub review ownership</b> to bring app compliance back to 100%"]
nxt_groups="".join(f'<div style="background:#F7F9FC;border-left:4px solid {c};border-radius:8px;padding:10px 12px;"><div style="font-size:13px;font-weight:800;color:{c};letter-spacing:.5px;">{t}</div>{ul(items,12.5)}</div>' for t,c,items in NEXT_OND)
lt_help="".join(f'<div style="display:flex;gap:10px;margin:8px 0;"><b style="color:#5FE0A0;font-size:18px;line-height:1.2;">{i}</b><div>{x}</div></div>' for i,x in enumerate(LT_HELP,1))
nxt=f'''{sec("6","What&rsquo;s Next &amp; How LT Can Help","OND&rsquo;26 priorities &ndash; and where you can unlock them",NAVY,"s6")}<div class="lift" style="background:#fff;border-radius:14px;padding:14px 18px;{F}display:flex;align-items:center;gap:8px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,37,69,.06);">{pill("AGENTIC AI",PURPLE)}{pill("CONTROL TOWER",TEAL)}{pill("APPS",BLUE)}{pill("WISE",GREEN)}{pill("eDDS FOR GPO",ORANGE)}{pill("CAPABILITY",NAVY)}{pill("5 LT ASKS",GOLD)}<div style="margin-left:auto;">{slicebtn("pNext","Shave to see what&rsquo;s next",NAVY)}</div></div>
<div id="pNext" class="panel"><div style="padding-top:14px;">
<div style="display:flex;gap:16px;align-items:flex-start;{F}">
<div class="lift" style="flex:1.55;background:#fff;border-radius:14px;padding:18px 20px;box-shadow:0 2px 8px rgba(11,37,69,.06);">
<div style="font-size:12px;font-weight:800;letter-spacing:2px;color:{BLUE};">NEXT IN OND&rsquo;26</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;">{nxt_groups}</div></div>
<div class="lift" style="flex:1;background:linear-gradient(150deg,#0B2545,#0B5CAD);border-radius:14px;padding:18px 22px;color:#fff;">
<div style="font-size:12px;font-weight:800;letter-spacing:2px;color:{GOLD};">HOW LT CAN HELP</div>
<div style="font-size:13.5px;line-height:1.5;margin-top:6px;">{lt_help}</div></div></div></div></div>'''

# ===== 7. ONE WINNING DIGITAL TEAM (bottom, collapsible)
def node(key,name,role,tag,c,size=78):
    d=A(key)
    inner=(f'<img class="zoom" src="{d}" alt="{name}" style="width:100%;height:100%;object-fit:cover;display:block;">' if d
           else f'<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:{size//3}px;font-weight:800;color:#fff;background:{c};">{name[0]}</div>')
    return f'''<div class="member" style="text-align:center;width:150px;margin:0 auto;{F}">
<div style="width:{size}px;height:{size}px;border-radius:50%;margin:0 auto;border:4px solid {c};overflow:hidden;background:#E6ECF3;">{inner}</div>
<div style="font-size:14.5px;font-weight:800;color:{NAVY};margin-top:6px;">{name}</div>
<div style="font-size:11.5px;color:{GREY};line-height:1.25;min-height:28px;">{role}</div>
<div style="display:inline-block;margin-top:4px;font-size:10.5px;color:#fff;background:{c};border-radius:10px;padding:2px 9px;font-style:italic;">&ldquo;{tag}&rdquo;</div></div>'''
V=lambda h=18: f'<div style="width:2px;height:{h}px;background:#9AA8BC;margin:0 auto;"></div>'
def tree(parent,kids,w=None):
    n=len(kids);w=w or [1]*n
    cols="".join(f'<div style="flex:{w[i]};position:relative;">'
      +(f'<div style="position:absolute;top:0;height:2px;background:#9AA8BC;left:{"50%" if i==0 else "0"};right:{"50%" if i==n-1 else "0"};"></div>' if n>1 else '')
      +V(14)+k+'</div>' for i,k in enumerate(kids))
    return f'{parent}{V(14)}<div style="display:flex;">{cols}</div>'
xuan_sub=tree(node("xuan","Xuan","App Governance Leader","Digital asset Guardian",BLUE),[node("luan","Luan","Digital KU","Bug Buster",TEAL,70),node("thuc","Thuc","Site Cybersecurity Leader","Anti-Hacker",ORANGE,70)])
digital_tree=tree(node("ky","Ky","IWS &amp; Site Digital Leader","I&rsquo;m here to serve the &lsquo;table&rsquo;",NAVY,86)+V()+node("minh","Minh","Site Digital Leader","Site Digital Transformer",ORANGE,82),[xuan_sub,node("nghi","Nghi","Data Activation Leader","Data is gold",GREEN)],[1.5,1])
digital=f'''<div style="flex:1.6;background:#fff;border-radius:14px;padding:16px 10px 18px;border-top:6px solid {ORANGE};box-shadow:0 2px 8px rgba(11,37,69,.06);">
<div style="text-align:center;{F}font-size:13px;font-weight:800;letter-spacing:2px;color:{ORANGE};margin-bottom:10px;">SITE DIGITAL TEAM</div>{digital_tree}</div>'''
it=f'''<div style="flex:1;background:#fff;border-radius:14px;padding:16px 10px 18px;border-top:6px solid {BLUE};box-shadow:0 2px 8px rgba(11,37,69,.06);">
<div style="text-align:center;{F}font-size:13px;font-weight:800;letter-spacing:2px;color:{BLUE};margin-bottom:10px;">IT TEAM</div>
{node("angarish","Angarish","AMA GC Grooming Digital Supply Chain Leader","Digital Supply Chain Sponsor",PURPLE,86)}{V()}
{node("dom","Dom","Digital Technology Leader","Site Digital &amp; Data Pioneer",BLUE,82)}{V()}
{node("quyen","Quyen","IT Operation Leader","Wi-Fi, find me",TEAL,78)}</div>'''
faces="".join(f'<div class="face" style="margin-left:-12px;width:46px;height:46px;border-radius:50%;overflow:hidden;border:3px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.2);background:{c};">'+(f'<img src="{A(k)}" style="width:100%;height:100%;object-fit:cover;">' if A(k) else f'<div style="color:#fff;font-weight:800;text-align:center;line-height:40px;{F}">{k[0].upper()}</div>')+'</div>' for k,c in [("ky",NAVY),("minh",ORANGE),("xuan",BLUE),("nghi",GREEN),("luan",TEAL),("thuc",ORANGE),("angarish",PURPLE),("dom",BLUE),("quyen",TEAL)])
team=f'''{sec("7","One Winning Digital Team","Two teams. One partnership. One goal.",BLUE,"s7")}
<div class="lift" style="background:#fff;border-radius:14px;padding:18px 22px;{F}display:flex;align-items:center;gap:20px;box-shadow:0 2px 8px rgba(11,37,69,.06);">
<div style="display:flex;padding-left:12px;">{faces}</div>
<div style="flex:1;"><div style="font-size:16px;font-weight:800;color:{NAVY};">The people behind the progress</div><div style="font-size:12.5px;color:{GREY};">Site Digital &times; IT &ndash; 9 people, one winning team</div></div>
{slicebtn("pTeam","Shave to open the org chart",BLUE)}</div>
<div id="pTeam" class="panel"><div style="display:flex;gap:0;align-items:stretch;margin-top:14px;">{digital}
<div style="flex:0 0 96px;display:flex;flex-direction:column;align-items:center;justify-content:center;{F}">
<div style="width:62px;height:62px;border-radius:50%;background:linear-gradient(135deg,{ORANGE},{BLUE});color:#fff;font-size:34px;font-weight:800;text-align:center;line-height:60px;box-shadow:0 4px 12px rgba(0,0,0,.15);">+</div>
<div style="font-size:11px;font-weight:800;color:{NAVY};letter-spacing:1px;text-align:center;margin-top:8px;line-height:1.3;">PARTNER<br>TOGETHER</div></div>
{it}</div>
<div style="text-align:center;margin-top:12px;{F}font-size:16px;font-weight:800;letter-spacing:3px;color:{NAVY};">ONE <span style="color:{ORANGE};">WINNING</span> DIGITAL <span style="color:{BLUE};">TEAM</span></div>
<div style="margin-top:18px;{F}font-size:12px;font-weight:800;letter-spacing:1.5px;color:{BLUE};margin-bottom:8px;">FULL DIGITAL PILLAR MEMBERSHIP</div>{slot("pillar_membership","Digital Pillar Membership",None,"contain",14)}</div>'''

footer=f'''<div style="margin-top:36px;background:{NAVY};padding:22px 44px;{F}color:#C9D8EA;display:flex;justify-content:space-between;align-items:center;">
<div><div style="font-size:18px;font-weight:800;color:#fff;">Data first &ndash; then AI.</div><div style="font-size:12px;">Bencat Digital Team &bull; Questions or ideas? Reply to this email.</div></div>
<div style="text-align:right;font-size:11px;letter-spacing:3px;color:#7FD3FF;">HIGHER &bull; FASTER &bull; TOGETHER<br><span style="color:#8FA3BC;letter-spacing:1px;">Business Use</span></div></div>'''

# ===== INTERACTIVITY (razor cursor, slice buttons, lightbox)
razor=("<svg xmlns='http://www.w3.org/2000/svg' width='36' height='36' viewBox='0 0 36 36'><g transform='rotate(-40 18 18)'>"
 "<rect x='5' y='4' width='26' height='9' rx='2.5' fill='%230B5CAD' stroke='white' stroke-width='1.5'/>"
 "<rect x='7' y='5.5' width='22' height='2' rx='1' fill='%23CFE8FF'/><rect x='7' y='10' width='22' height='1.4' fill='%237FD3FF'/>"
 "<rect x='16' y='13' width='4' height='20' rx='2' fill='%23E06A10' stroke='white' stroke-width='1.2'/>"
 "<rect x='16.8' y='18' width='2.4' height='1.2' fill='white' opacity='.7'/><rect x='16.8' y='22' width='2.4' height='1.2' fill='white' opacity='.7'/></g></svg>")
CSS=open(os.path.join(HERE,"assets","style.css")).read().replace("__RAZOR__",razor).replace("__NAVY__",NAVY)
JS=open(os.path.join(HERE,"assets","script.js")).read()

html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bencat Digital Newsletter JAS'26</title><style>{CSS}</style></head>
<body style="margin:0;padding:0;background:#DDE3EA;">
<div style="max-width:1040px;margin:24px auto;background:{BG};border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(11,37,69,.18);">
{hero}
<div style="padding:4px 40px 0;">{exec_html}{impacts}{deliv}{skills}{orgc}{nxt}{team}</div>
{footer}</div>
<div id="lb"><span class="x">&#10005; Close</span><img alt=""></div>
<script>{JS}</script></body></html>'''
open(OUT,'w',encoding='utf-8').write(html)
missing=sorted(k for k,v in _cache.items() if v is None)
print(f"Built {os.path.basename(OUT)} ({len(html)//1024} KB)")
print("Missing photos ->", ", ".join(missing) if missing else "none")
