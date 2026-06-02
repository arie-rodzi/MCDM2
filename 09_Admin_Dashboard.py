import streamlit as st, pandas as pd, os
from style import apply_style, hero, card

st.set_page_config(page_title='Marks Dashboard', layout='wide')
apply_style()

RESULT='data/results.csv'
hero('09 | Marks Dashboard', 'View assessment marks, download marks, and upload a CSV marks file to replace current records. For live deployment, use institutional login or Streamlit access control rather than storing passwords inside the app code.')

os.makedirs('data',exist_ok=True)
if os.path.exists(RESULT):
    df=pd.read_csv(RESULT)
else:
    df=pd.DataFrame(columns=['timestamp','name','student_id','email','score','correct','total'])

st.subheader('Current Marks')
st.dataframe(df,use_container_width=True)
st.download_button('⬇️ Download marks CSV', df.to_csv(index=False), 'mcdm_marks.csv', 'text/csv')

card('Upload marks file', '<p>Upload a CSV with the required columns only when you intentionally want to replace the current marks file.</p>', 'blue')
upload=st.file_uploader('Upload marks CSV to replace current marks', type=['csv'])
if upload is not None:
    new=pd.read_csv(upload)
    required={'timestamp','name','student_id','email','score','correct','total'}
    if required.issubset(set(new.columns)):
        new.to_csv(RESULT,index=False)
        st.success('Marks uploaded successfully. Refresh page to view.')
    else:
        st.error('Uploaded CSV must include timestamp, name, student_id, email, score, correct and total columns.')
