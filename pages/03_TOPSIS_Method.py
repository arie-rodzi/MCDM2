import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='TOPSIS Method', page_icon='🟥', layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #C1121F33, transparent 30%), linear-gradient(135deg, #FFF0F1 0%, #FFFFFF 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {padding:34px; border-radius:30px; background:linear-gradient(135deg,#5A0B12, #C1121F); color:white; box-shadow:0 24px 55px #C1121F44; margin-bottom:24px;}
.hero h1 {font-size:44px; margin:0; font-weight:900;}
.hero p {font-size:18px; opacity:.92; margin-top:8px;}
.card {background:rgba(255,255,255,.94); border:1px solid rgba(0,0,0,.07); padding:24px; border-radius:24px; box-shadow:0 16px 38px rgba(0,0,0,.07); margin:18px 0;}
.mini {background:#FFF0F1; border-left:7px solid #C1121F; padding:18px; border-radius:18px; margin:12px 0;}
.badge {display:inline-block; background:#C1121F; color:white; padding:7px 13px; border-radius:999px; font-weight:800;}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><span class='badge'>Premium Red Theme</span><h1>🟥 TOPSIS Method</h1><p>Premium MCDM learning page with real equations, manual calculation, visualization and quiz.</p></div>""", unsafe_allow_html=True)

st.markdown("""<div class='card'><h2>1. Concept</h2>TOPSIS is a <b>distance-based ranking method</b>. The best alternative should be closest to the Positive Ideal Solution and farthest from the Negative Ideal Solution.</div>""", unsafe_allow_html=True)
st.markdown('## 2. Core Equations')
st.latex(r"r_{ij}=\frac{x_{ij}}{\sqrt{\sum_{i=1}^{m}x_{ij}^{2}}}")
st.latex(r"v_{ij}=w_jr_{ij}")
st.latex(r"D_i^{+}=\sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^{+})^2},\quad D_i^{-}=\sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^{-})^2}")
st.latex(r"C_i=\frac{D_i^{-}}{D_i^{+}+D_i^{-}}")
df=pd.DataFrame({'Alternative':['Platform A','Platform B','Platform C','Platform D'],'Cost':[12000,15000,10000,18000],'Usability':[80,90,75,85],'Features':[70,85,65,95],'Support Time':[12,8,15,6]})
types={'Cost':'Cost','Usability':'Benefit','Features':'Benefit','Support Time':'Cost'}; weights={'Cost':.30,'Usability':.30,'Features':.25,'Support Time':.15}
st.markdown('## 3. Decision Matrix'); st.dataframe(df,use_container_width=True)
X=df.drop(columns='Alternative').astype(float); R=X/np.sqrt((X**2).sum()); V=R*pd.Series(weights)
pis={c:(V[c].max() if types[c]=='Benefit' else V[c].min()) for c in V.columns}; nis={c:(V[c].min() if types[c]=='Benefit' else V[c].max()) for c in V.columns}
Dpos=np.sqrt(((V-pd.Series(pis))**2).sum(axis=1)); Dneg=np.sqrt(((V-pd.Series(nis))**2).sum(axis=1)); C=Dneg/(Dpos+Dneg)
res=pd.DataFrame({'Alternative':df['Alternative'],'D+ Ideal Distance':Dpos,'D- Worst Distance':Dneg,'TOPSIS Closeness':C}); res['Rank']=res['TOPSIS Closeness'].rank(ascending=False,method='dense').astype(int)
st.markdown('## 4. Weighted Normalized Matrix'); st.dataframe(V.round(4),use_container_width=True)
st.markdown('## 5. Ideal Solutions'); st.dataframe(pd.DataFrame([pis,nis],index=['Positive Ideal','Negative Ideal']).round(4),use_container_width=True)
st.markdown('## 6. Final Ranking'); st.dataframe(res.sort_values('Rank').round(4),use_container_width=True)
st.plotly_chart(px.bar(res.sort_values('TOPSIS Closeness'),x='TOPSIS Closeness',y='Alternative',orientation='h',text='TOPSIS Closeness',title='TOPSIS Closeness Coefficient'),use_container_width=True)
fig=go.Figure(); fig.add_trace(go.Scatter(x=res['D+ Ideal Distance'],y=res['D- Worst Distance'],mode='markers+text',text=res['Alternative'],textposition='top center',marker_size=16)); fig.update_layout(title='Distance Map',xaxis_title='Distance from Positive Ideal',yaxis_title='Distance from Negative Ideal',height=500); st.plotly_chart(fig,use_container_width=True)
