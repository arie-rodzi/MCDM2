import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='AHP Method', page_icon='🟦', layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #1E5AA833, transparent 30%), linear-gradient(135deg, #EAF1FF 0%, #FFFFFF 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {padding:34px; border-radius:30px; background:linear-gradient(135deg,#0B1F4D, #1E5AA8); color:white; box-shadow:0 24px 55px #1E5AA844; margin-bottom:24px;}
.hero h1 {font-size:44px; margin:0; font-weight:900;}
.hero p {font-size:18px; opacity:.92; margin-top:8px;}
.card {background:rgba(255,255,255,.94); border:1px solid rgba(0,0,0,.07); padding:24px; border-radius:24px; box-shadow:0 16px 38px rgba(0,0,0,.07); margin:18px 0;}
.mini {background:#EAF1FF; border-left:7px solid #1E5AA8; padding:18px; border-radius:18px; margin:12px 0;}
.badge {display:inline-block; background:#1E5AA8; color:white; padding:7px 13px; border-radius:999px; font-weight:800;}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><span class='badge'>Navy Blue Theme</span><h1>🟦 AHP Method</h1><p>Premium MCDM learning page with real equations, manual calculation, visualization and quiz.</p></div>""", unsafe_allow_html=True)

st.markdown("""<div class='card'>
<h2>1. Concept</h2>
AHP is used to generate <b>subjective weights</b> from expert judgement. Instead of directly assigning weights, AHP asks the expert to compare criteria two at a time.
<br><br><b>Example case:</b> selecting the best digital learning platform using Cost, Usability, Features and Support.
</div>""", unsafe_allow_html=True)
st.markdown("## 2. Core Equations")
st.latex(r"A=[a_{ij}]_{n\times n}, \quad a_{ji}=\frac{1}{a_{ij}}, \quad a_{ii}=1")
st.latex(r"GM_i=\left(\prod_{j=1}^{n}a_{ij}\right)^{1/n}, \quad w_i=\frac{GM_i}{\sum_{i=1}^{n}GM_i}")
st.latex(r"\lambda_{max}=\frac{1}{n}\sum_{i=1}^{n}\frac{(Aw)_i}{w_i}")
st.latex(r"CI=\frac{\lambda_{max}-n}{n-1}, \quad CR=\frac{CI}{RI}")
criteria=['Cost','Usability','Features','Support']
mat=np.array([[1,1/3,1/2,2],[3,1,2,4],[2,1/2,1,3],[1/2,1/4,1/3,1]],float)
df=pd.DataFrame(mat,index=criteria,columns=criteria)
st.markdown("## 3. Pairwise Comparison Matrix"); st.dataframe(df.round(4), use_container_width=True)
gm=np.prod(mat,axis=1)**(1/len(criteria)); w=gm/gm.sum()
weight_df=pd.DataFrame({'Criterion':criteria,'AHP Weight':w}).sort_values('AHP Weight',ascending=False)
st.markdown("## 4. Criteria Weights"); st.dataframe(weight_df.round(4), use_container_width=True)
fig=px.bar(weight_df,x='Criterion',y='AHP Weight',text='AHP Weight',title='AHP Criteria Priority'); fig.update_traces(texttemplate='%{text:.4f}', textposition='outside'); st.plotly_chart(fig,use_container_width=True)
Aw=mat.dot(w); lam=np.mean(Aw/w); ci=(lam-len(criteria))/(len(criteria)-1); cr=ci/0.90
st.markdown("## 5. Consistency Check"); c1,c2,c3=st.columns(3); c1.metric('Lambda Max',f'{lam:.4f}'); c2.metric('CI',f'{ci:.4f}'); c3.metric('CR',f'{cr:.4f}')
st.markdown("""<div class='mini'><b>Interpretation:</b> CR below 0.10 is usually acceptable. It means the pairwise judgement is reasonably consistent.</div>""", unsafe_allow_html=True)
perf=pd.DataFrame({'Alternative':['Platform A','Platform B','Platform C','Platform D'],'Cost':[.80,.65,1.00,.55],'Usability':[.85,1.00,.78,.92],'Features':[.74,.90,.68,1.00],'Support':[.70,.85,.60,1.00]})
scores=perf.set_index('Alternative').dot(pd.Series(w,index=criteria)).reset_index(name='AHP Final Score'); scores['Rank']=scores['AHP Final Score'].rank(ascending=False,method='dense').astype(int)
st.markdown('## 6. Final Alternative Ranking'); st.dataframe(scores.sort_values('Rank').round(4), use_container_width=True)
st.plotly_chart(px.bar(scores.sort_values('AHP Final Score'),x='AHP Final Score',y='Alternative',orientation='h',text='AHP Final Score',title='Final AHP Ranking'),use_container_width=True)
