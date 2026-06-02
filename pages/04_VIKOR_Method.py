import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='VIKOR Method', page_icon='🟪', layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #7B2CBF33, transparent 30%), linear-gradient(135deg, #F5EDFF 0%, #FFFFFF 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {padding:34px; border-radius:30px; background:linear-gradient(135deg,#2D0A4E, #7B2CBF); color:white; box-shadow:0 24px 55px #7B2CBF44; margin-bottom:24px;}
.hero h1 {font-size:44px; margin:0; font-weight:900;}
.hero p {font-size:18px; opacity:.92; margin-top:8px;}
.card {background:rgba(255,255,255,.94); border:1px solid rgba(0,0,0,.07); padding:24px; border-radius:24px; box-shadow:0 16px 38px rgba(0,0,0,.07); margin:18px 0;}
.mini {background:#F5EDFF; border-left:7px solid #7B2CBF; padding:18px; border-radius:18px; margin:12px 0;}
.badge {display:inline-block; background:#7B2CBF; color:white; padding:7px 13px; border-radius:999px; font-weight:800;}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><span class='badge'>Royal Purple Theme</span><h1>🟪 VIKOR Method</h1><p>Premium MCDM learning page with real equations, manual calculation, visualization and quiz.</p></div>""", unsafe_allow_html=True)

st.markdown("""<div class='card'><h2>1. Concept</h2>VIKOR is a <b>compromise ranking method</b>. It balances group utility and individual regret.</div>""", unsafe_allow_html=True)
st.markdown('## 2. Core Equations')
st.latex(r"S_i=\sum_{j=1}^{n}w_j\frac{f_j^*-f_{ij}}{f_j^*-f_j^-}")
st.latex(r"R_i=\max_j\left[w_j\frac{f_j^*-f_{ij}}{f_j^*-f_j^-}\right]")
st.latex(r"Q_i=v\frac{S_i-S^*}{S^- - S^*}+(1-v)\frac{R_i-R^*}{R^- - R^*}")
df=pd.DataFrame({'Alternative':['Platform A','Platform B','Platform C','Platform D'],'Cost':[12000,15000,10000,18000],'Usability':[80,90,75,85],'Features':[70,85,65,95],'Support Time':[12,8,15,6]})
types={'Cost':'Cost','Usability':'Benefit','Features':'Benefit','Support Time':'Cost'}; weights=pd.Series({'Cost':.30,'Usability':.30,'Features':.25,'Support Time':.15})
X=df.drop(columns='Alternative').astype(float); best=pd.Series({c:(X[c].min() if types[c]=='Cost' else X[c].max()) for c in X.columns}); worst=pd.Series({c:(X[c].max() if types[c]=='Cost' else X[c].min()) for c in X.columns})
gap=(best-X).abs()/(best-worst).abs().replace(0,np.nan); Wgap=gap*weights; S=Wgap.sum(axis=1); R=Wgap.max(axis=1); Q=.5*(S-S.min())/(S.max()-S.min())+.5*(R-R.min())/(R.max()-R.min())
res=pd.DataFrame({'Alternative':df['Alternative'],'S Group Utility':S,'R Individual Regret':R,'Q Compromise Index':Q}); res['Rank']=res['Q Compromise Index'].rank(ascending=True,method='dense').astype(int)
st.markdown('## 3. Decision Matrix'); st.dataframe(df,use_container_width=True)
st.markdown('## 4. Best and Worst Values'); st.dataframe(pd.DataFrame([best,worst],index=['Best','Worst']),use_container_width=True)
st.markdown('## 5. S, R and Q Results'); st.dataframe(res.sort_values('Rank').round(4),use_container_width=True)
st.plotly_chart(px.bar(res.sort_values('Q Compromise Index',ascending=False),x='Q Compromise Index',y='Alternative',orientation='h',text='Q Compromise Index',title='VIKOR Q Index: Lower is Better'),use_container_width=True)
st.plotly_chart(px.scatter(res,x='S Group Utility',y='R Individual Regret',text='Alternative',size='Q Compromise Index',title='VIKOR Utility-Regret Map'),use_container_width=True)
