import streamlit as st

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
:root{--navy:#061A40;--royal:#003566;--gold:#FFC300;--amber:#FFD60A;--cyan:#7BDFF2;--mint:#80ED99;--pink:#FF70A6;--white:#F8FAFC;--dark:#0F172A;}
html, body, [class*="css"] {font-family: Inter, sans-serif;}
.stApp {background: radial-gradient(circle at top left,#1E3A8A 0,#061A40 32%,#160B36 72%,#050816 100%); color:var(--white);} 
.block-container {padding-top:1.2rem; max-width:1280px;}
h1,h2,h3,h4,p,li,div,label,span {color:#F8FAFC !important;}
.hero {padding:2.4rem 2.2rem; border-radius:34px; background:linear-gradient(135deg,rgba(255,255,255,.20),rgba(255,255,255,.07)); border:1px solid rgba(255,255,255,.28); box-shadow:0 22px 60px rgba(0,0,0,.32); margin-bottom:1.3rem; position:relative; overflow:hidden;}
.hero:before{content:""; position:absolute; top:-55px; right:-35px; width:220px; height:220px; border-radius:50%; background:rgba(255,195,0,.25); filter:blur(3px);} 
.hero h1 {font-size:2.65rem; margin:0; font-weight:900; letter-spacing:-1.2px;}
.hero p {font-size:1.08rem; line-height:1.75; max-width:980px; color:#EAF2FF !important;}
.card {padding:1.35rem 1.45rem; border-radius:24px; background:linear-gradient(135deg,rgba(255,255,255,.14),rgba(255,255,255,.06)); border:1px solid rgba(255,255,255,.20); box-shadow:0 14px 32px rgba(0,0,0,.20); margin:1rem 0;}
.gold {border-left:8px solid #FFC300}.green {border-left:8px solid #80ED99}.red {border-left:8px solid #FF70A6}.blue {border-left:8px solid #7BDFF2}.purple{border-left:8px solid #C77DFF}
.kpi {padding:1.15rem; border-radius:22px; background:linear-gradient(135deg,rgba(255,195,0,.22),rgba(123,223,242,.12)); border:1px solid rgba(255,255,255,.22); min-height:120px;}
.kpi .num{font-size:2rem; font-weight:900; color:#FFD60A !important;}
.badge{display:inline-block; padding:.35rem .65rem; border-radius:999px; background:rgba(255,195,0,.18); border:1px solid rgba(255,195,0,.45); font-weight:800; margin:.15rem .25rem .15rem 0;}
.step {padding:1rem 1.15rem; border-radius:18px; background:rgba(255,255,255,.10); margin:.7rem 0; border-left:5px solid #FFC300;}
.formula-box{padding:1rem 1.2rem; border-radius:20px; background:rgba(2,6,23,.45); border:1px solid rgba(255,255,255,.22); margin:.8rem 0;}
.small {font-size:.92rem; opacity:.95; line-height:1.6;}
.stTextInput input, .stNumberInput input, textarea {background:#ffffff !important; color:#111827 !important; border-radius:14px !important;}
.stButton button, .stDownloadButton button {border-radius:16px; font-weight:900; background:linear-gradient(90deg,#FFC300,#FFB703); color:#061A40 !important; border:0; padding:.7rem 1.2rem;}
[data-testid="stDataFrame"] {border-radius:18px; overflow:hidden; border:1px solid rgba(255,255,255,.18);} 
hr {border-color:rgba(255,255,255,.18);} 

/* Clear, readable sidebar */
[data-testid="stSidebar"] {background:linear-gradient(180deg,#FFFFFF 0%,#EAF2FF 100%) !important; border-right:1px solid rgba(15,23,42,.15);}
[data-testid="stSidebar"] * {color:#0F172A !important;}
[data-testid="stSidebar"] a, [data-testid="stSidebar"] a span {color:#061A40 !important; font-weight:800 !important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#0F172A !important;}
[data-testid="stSidebarNav"] li div a {border-radius:12px !important; padding:.55rem .75rem !important;}
[data-testid="stSidebarNav"] li div a:hover {background:#DDEBFF !important;}
[data-testid="stSidebarNav"] li div a[aria-current="page"] {background:#003566 !important;}
[data-testid="stSidebarNav"] li div a[aria-current="page"] span {color:#FFFFFF !important;}
</style>
"""

def apply_style(): st.markdown(APP_CSS, unsafe_allow_html=True)
def hero(title, subtitle): st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
def card(title, body, kind='gold'): st.markdown(f'<div class="card {kind}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)
def step(title, body): st.markdown(f'<div class="step"><b>{title}</b><br>{body}</div>', unsafe_allow_html=True)
def kpi(label, value, note=''): st.markdown(f'<div class="kpi"><div class="num">{value}</div><b>{label}</b><div class="small">{note}</div></div>', unsafe_allow_html=True)
