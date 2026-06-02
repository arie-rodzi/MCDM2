import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='CRITIC Method', page_icon='🟧', layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #F77F0033, transparent 30%), linear-gradient(135deg, #FFF3E0 0%, #FFFFFF 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {padding:34px; border-radius:30px; background:linear-gradient(135deg,#5C2E00, #F77F00); color:white; box-shadow:0 24px 55px #F77F0044; margin-bottom:24px;}
.hero h1 {font-size:44px; margin:0; font-weight:900;}
.hero p {font-size:18px; opacity:.92; margin-top:8px;}
.card {background:rgba(255,255,255,.94); border:1px solid rgba(0,0,0,.07); padding:24px; border-radius:24px; box-shadow:0 16px 38px rgba(0,0,0,.07); margin:18px 0;}
.mini {background:#FFF3E0; border-left:7px solid #F77F00; padding:18px; border-radius:18px; margin:12px 0;}
.badge {display:inline-block; background:#F77F00; color:white; padding:7px 13px; border-radius:999px; font-weight:800;}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><span class='badge'>Orange Theme</span><h1>🟧 CRITIC Method</h1><p>Premium MCDM learning page with real equations, manual calculation, visualization and quiz.</p></div>""", unsafe_allow_html=True)

st.markdown("""<div class='card'><h2>1. Concept</h2>CRITIC is an <b>objective weighting method</b>. It derives weights from data using variation and conflict among criteria.</div>""", unsafe_allow_html=True)
st.markdown('## 2. Core Equations')
st.latex(r"r_{ij}=\frac{x_{ij}-\min(x_j)}{\max(x_j)-\min(x_j)}")
st.latex(r"C_j=\sigma_j\sum_{k=1}^{n}(1-\rho_{jk})")
st.latex(r"w_j=\frac{C_j}{\sum_{j=1}^{n}C_j}")
df=pd.DataFrame({'Alternative':['Platform A','Platform B','Platform C','Platform D','Platform E'],'Cost':[12000,15000,10000,18000,13000],'Usability':[80,90,75,85,88],'Features':[70,85,65,95,82],'Support Time':[12,8,15,6,9]})
types={'Cost':'Cost','Usability':'Benefit','Features':'Benefit','Support Time':'Cost'}; X=df.drop(columns='Alternative').astype(float); R=pd.DataFrame(index=df.index)
for c in X.columns:
    R[c]=(X[c]-X[c].min())/(X[c].max()-X[c].min()) if types[c]=='Benefit' else (X[c].max()-X[c])/(X[c].max()-X[c].min())
std=R.std(ddof=0); corr=R.corr(); info=std*((1-corr).sum()); weights=info/info.sum(); res=pd.DataFrame({'Criterion':weights.index,'Standard Deviation':std.values,'Information Content':info.values,'CRITIC Weight':weights.values}).sort_values('CRITIC Weight',ascending=False)
st.markdown('## 3. Decision Matrix'); st.dataframe(df,use_container_width=True)
st.markdown('## 4. Normalized Matrix'); st.dataframe(R.round(4),use_container_width=True)
st.markdown('## 5. Correlation Matrix'); st.dataframe(corr.round(4),use_container_width=True)
st.markdown('## 6. Objective Weights'); st.dataframe(res.round(4),use_container_width=True)
st.plotly_chart(px.bar(res,x='Criterion',y='CRITIC Weight',text='CRITIC Weight',title='CRITIC Objective Weights'),use_container_width=True)
st.plotly_chart(px.imshow(corr,text_auto=True,title='Criteria Correlation Heatmap'),use_container_width=True)
