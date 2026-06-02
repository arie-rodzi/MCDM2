import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='DEMATEL Method', page_icon='⚫', layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #C5A01733, transparent 30%), linear-gradient(135deg, #F7F4EA 0%, #FFFFFF 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {padding:34px; border-radius:30px; background:linear-gradient(135deg,#111111, #C5A017); color:white; box-shadow:0 24px 55px #C5A01744; margin-bottom:24px;}
.hero h1 {font-size:44px; margin:0; font-weight:900;}
.hero p {font-size:18px; opacity:.92; margin-top:8px;}
.card {background:rgba(255,255,255,.94); border:1px solid rgba(0,0,0,.07); padding:24px; border-radius:24px; box-shadow:0 16px 38px rgba(0,0,0,.07); margin:18px 0;}
.mini {background:#F7F4EA; border-left:7px solid #C5A017; padding:18px; border-radius:18px; margin:12px 0;}
.badge {display:inline-block; background:#C5A017; color:white; padding:7px 13px; border-radius:999px; font-weight:800;}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><span class='badge'>Dark Grey Gold Theme</span><h1>⚫ DEMATEL Method</h1><p>Premium MCDM learning page with real equations, manual calculation, visualization and quiz.</p></div>""", unsafe_allow_html=True)

st.markdown("""<div class='card'><h2>1. Concept</h2>DEMATEL explains <b>cause and effect</b> relationships among criteria. It is not a normal ranking method.</div>""", unsafe_allow_html=True)
st.markdown('## 2. Core Equations')
st.latex(r"N=\frac{A}{\max_i \sum_{j=1}^{n}a_{ij}}")
st.latex(r"T=N(I-N)^{-1}")
st.latex(r"D_i=\sum_{j=1}^{n}t_{ij}, \quad R_i=\sum_{j=1}^{n}t_{ji}")
st.latex(r"Prominence=D_i+R_i, \quad Relation=D_i-R_i")
criteria=['Service Quality','System Usability','Cost Pressure','Management Support','User Trust']; A=np.array([[0,3,2,2,3],[2,0,1,3,3],[3,1,0,2,1],[3,3,2,0,3],[2,3,1,2,0]],float); df=pd.DataFrame(A,index=criteria,columns=criteria)
st.markdown('## 3. Direct Influence Matrix'); st.dataframe(df,use_container_width=True)
N=A/A.sum(axis=1).max(); T=N.dot(np.linalg.inv(np.eye(len(criteria))-N)); D=T.sum(axis=1); R=T.sum(axis=0); res=pd.DataFrame({'Criterion':criteria,'D Giving Influence':D,'R Receiving Influence':R,'D+R Prominence':D+R,'D-R Relation':D-R}); res['Group']=np.where(res['D-R Relation']>=0,'Cause Group','Effect Group')
st.markdown('## 4. Total Relation Results'); st.dataframe(res.round(4),use_container_width=True)
st.plotly_chart(px.bar(res.sort_values('D-R Relation'),x='D-R Relation',y='Criterion',orientation='h',color='Group',title='Cause and Effect Classification'),use_container_width=True)
fig=go.Figure(); fig.add_trace(go.Scatter(x=res['D+R Prominence'],y=res['D-R Relation'],mode='markers+text',text=res['Criterion'],textposition='top center',marker_size=16)); fig.add_hline(y=0,line_dash='dash'); fig.update_layout(title='DEMATEL Prominence-Relation Map',xaxis_title='Prominence (D + R)',yaxis_title='Relation (D - R)',height=520); st.plotly_chart(fig,use_container_width=True)
threshold=pd.DataFrame(T,index=criteria,columns=criteria).values.mean(); edges=[]
for i,a in enumerate(criteria):
    for j,b in enumerate(criteria):
        if i!=j and T[i,j]>=threshold: edges.append({'From':a,'To':b,'Influence':T[i,j]})
st.markdown('## 5. Strong Influence Links'); st.dataframe(pd.DataFrame(edges).round(4),use_container_width=True)
