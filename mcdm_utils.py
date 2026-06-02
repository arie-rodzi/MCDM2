from io import BytesIO
import pandas as pd, numpy as np
import streamlit as st
CRITERIA = ['Implementation Cost (USD) ↓','Expected Impact Score ↑','Technical Feasibility ↑','Implementation Time (months) ↓','Risk Exposure ↓']
TYPES = ['cost','benefit','benefit','cost','cost']
WEIGHTS = np.array([0.22,0.30,0.20,0.15,0.13])
WEIGHT_DF = pd.DataFrame({'Criterion':CRITERIA,'Type':TYPES,'Weight':WEIGHTS})
CASE_DF = pd.DataFrame({'Alternative':['A1 Smart Attendance System','A2 AI Student Advisory Chatbot','A3 Learning Analytics Dashboard','A4 Digital Assessment Platform'],'Implementation Cost (USD) ↓':[42000,35000,50000,38000],'Expected Impact Score ↑':[82,78,90,86],'Technical Feasibility ↑':[88,80,84,76],'Implementation Time (months) ↓':[8,6,10,7],'Risk Exposure ↓':[35,42,30,38]})
def to_excel_bytes(sheets):
    bio=BytesIO()
    with pd.ExcelWriter(bio, engine='openpyxl') as writer:
        for name, df in sheets.items(): df.to_excel(writer, sheet_name=name[:31], index=False)
    return bio.getvalue()
def download_workbook(filename, sheets): st.download_button('⬇️ Download complete calculation workbook (Excel)', data=to_excel_bytes(sheets), file_name=filename, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
def show_case_intro():
    st.markdown('<span class="badge">Real case study</span><span class="badge">Higher education digital transformation</span><span class="badge">Benefit + Cost criteria</span>', unsafe_allow_html=True)
    st.write('A university committee must select the best digital transformation initiative. Alternatives are evaluated using cost, expected impact, feasibility, implementation time, and risk exposure. This is realistic because public universities must balance impact, budget, feasibility, time, and risk before approving projects.')
    c1,c2=st.columns([2,1])
    with c1: st.dataframe(CASE_DF, use_container_width=True)
    with c2: st.dataframe(WEIGHT_DF, use_container_width=True)
def normalize_saw(X):
    R=np.zeros_like(X,dtype=float)
    for j,t in enumerate(TYPES):
        col=X[:,j]; R[:,j]=col/col.max() if t=='benefit' else col.min()/np.where(col==0,1e-9,col)
    return R
def saw_calc(): X=CASE_DF[CRITERIA].to_numpy(float); R=normalize_saw(X); return R,R@WEIGHTS
def topsis_calc():
    X=CASE_DF[CRITERIA].to_numpy(float); R=X/np.sqrt((X**2).sum(axis=0)); V=R*WEIGHTS
    Aplus=np.array([V[:,j].max() if TYPES[j]=='benefit' else V[:,j].min() for j in range(len(TYPES))])
    Aminus=np.array([V[:,j].min() if TYPES[j]=='benefit' else V[:,j].max() for j in range(len(TYPES))])
    Dp=np.sqrt(((V-Aplus)**2).sum(axis=1)); Dm=np.sqrt(((V-Aminus)**2).sum(axis=1)); C=Dm/(Dp+Dm)
    return R,V,Aplus,Aminus,Dp,Dm,C
def vikor_calc(v=0.5):
    X=CASE_DF[CRITERIA].to_numpy(float); fstar=np.array([X[:,j].max() if TYPES[j]=='benefit' else X[:,j].min() for j in range(len(TYPES))]); fminus=np.array([X[:,j].min() if TYPES[j]=='benefit' else X[:,j].max() for j in range(len(TYPES))])
    denom=np.where(np.abs(fstar-fminus)<1e-12,1e-9,np.abs(fstar-fminus)); gap=np.zeros_like(X,float)
    for j,t in enumerate(TYPES): gap[:,j]=(fstar[j]-X[:,j])/denom[j] if t=='benefit' else (X[:,j]-fstar[j])/denom[j]
    WG=gap*WEIGHTS; S=WG.sum(axis=1); R=WG.max(axis=1); Q=v*(S-S.min())/(S.max()-S.min()+1e-9)+(1-v)*(R-R.min())/(R.max()-R.min()+1e-9)
    return fstar,fminus,gap,WG,S,R,Q
def waspas_calc(lam=0.5):
    X=CASE_DF[CRITERIA].to_numpy(float); R=normalize_saw(X); Q1=(R*WEIGHTS).sum(axis=1); Q2=np.prod(np.power(np.where(R==0,1e-9,R),WEIGHTS),axis=1); Q=lam*Q1+(1-lam)*Q2; return R,Q1,Q2,Q
def rank_df(values, name, ascending=False):
    df=pd.DataFrame({'Alternative':CASE_DF['Alternative'], name:np.round(values,6)}).sort_values(name, ascending=ascending).reset_index(drop=True); df['Rank']=range(1,len(df)+1); return df
def df_matrix(arr, cols=CRITERIA): return pd.DataFrame(np.round(arr,6), columns=cols, index=CASE_DF['Alternative']).reset_index()
