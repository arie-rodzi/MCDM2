import streamlit as st
from style import apply_style, hero, card, kpi
st.set_page_config(page_title='MCDM Masterclass', page_icon='📊', layout='wide')
apply_style()
hero('MCDM Masterclass', 'A detailed English learning app for Multi-Criteria Decision-Making with proper equations, real case study, downloadable data, step-by-step calculations, quiz, marks, and marks dashboard.')
cols=st.columns(4)
with cols[0]: kpi('Methods covered','5','SAW, TOPSIS, AHP, VIKOR, WASPAS')
with cols[1]: kpi('Case study','Real','University digital project selection')
with cols[2]: kpi('Calculation style','Step-by-step','Matrix, normalization, scores, ranking')
with cols[3]: kpi('Download','Excel','Raw data + calculation sheets')
card('How to use this app','<ol><li>Start with General MCDM Foundation.</li><li>Open each method page and study the concept, assumptions, formulas, and case study.</li><li>Download the Excel workbook from each page to verify the calculation manually.</li><li>Use Quiz and Marks for student assessment.</li><li>The marks dashboard can view, upload, and download assessment records.</li></ol>','blue')
