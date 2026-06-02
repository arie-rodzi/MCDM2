import streamlit as st, pandas as pd, os, datetime
from style import apply_style, hero, card
st.set_page_config(page_title='Quiz and Marks', layout='wide')
apply_style()
RESULT='data/results.csv'
hero('08 | Student Quiz and Marks', 'Students enter their details, answer the MCDM quiz, submit their answers, and check their own marks using Student ID.')
with st.expander('Student Details', expanded=True):
    name=st.text_input('Full Name')
    student_id=st.text_input('Student ID / Matric No')
    email=st.text_input('Email')
questions=[
('MCDM is used when a decision involves several criteria at the same time.', 'tf', True),
('For a cost criterion, a higher value is always preferred.', 'tf', False),
('In SAW, the final score is calculated using:', 'mcq', 'Weighted summation', ['Random sampling','Weighted summation','Image compression','Regression residual']),
('In TOPSIS, the best alternative should be closest to the positive ideal solution and farthest from the ____ ideal solution.', 'blank', 'negative'),
('AHP is strongly associated with which process?', 'mcq', 'Pairwise comparison', ['Pairwise comparison','Image compression','Regression residual','Random sampling']),
('In VIKOR, the best alternative usually has the ____ Q value.', 'blank', 'minimum'),
('WASPAS combines the Weighted Sum Model and Weighted Product Model.', 'tf', True),
('Benefit criteria prefer ____ values.', 'blank', 'higher'),
('Sensitivity analysis checks whether the ranking remains stable when weights change.', 'tf', True),
('Implementation cost is usually a cost criterion.', 'tf', True),
('In AHP, CR means Consistency Ratio.', 'tf', True),
('In TOPSIS, CC stands for closeness coefficient.', 'tf', True),
]
answers=[]
st.subheader('Quiz')
for i,q in enumerate(questions,1):
    st.markdown(f'<div class="card blue"><h3>Q{i}. {q[0]}</h3></div>', unsafe_allow_html=True)
    if q[1]=='tf': answers.append(st.radio('Choose one',[True,False],format_func=lambda x:'True' if x else 'False',key=f'q{i}'))
    elif q[1]=='mcq': answers.append(st.radio('Choose one',q[3],key=f'q{i}'))
    else: answers.append(st.text_input('Fill in the blank',key=f'q{i}').strip().lower())
if st.button('Submit Quiz'):
    if not name or not student_id:
        st.error('Please fill in name and student ID.')
    else:
        correct=0
        for ans,q in zip(answers,questions):
            if q[1]=='blank': correct += (str(ans).strip().lower()==q[2])
            else: correct += (ans==q[2])
        score=round(correct/len(questions)*100,2)
        row={'timestamp':datetime.datetime.now().isoformat(timespec='seconds'),'name':name,'student_id':student_id,'email':email,'score':score,'correct':correct,'total':len(questions)}
        os.makedirs('data',exist_ok=True)
        df=pd.read_csv(RESULT) if os.path.exists(RESULT) else pd.DataFrame()
        df=pd.concat([df,pd.DataFrame([row])],ignore_index=True)
        df.to_csv(RESULT,index=False)
        st.success(f'Your score: {score}% ({correct}/{len(questions)})')
st.subheader('Check Your Marks')
check=st.text_input('Enter your Student ID to check marks')
if st.button('Check Marks'):
    if os.path.exists(RESULT):
        df=pd.read_csv(RESULT); out=df[df['student_id'].astype(str)==check]
        if len(out): st.dataframe(out.sort_values('timestamp',ascending=False),use_container_width=True)
        else: st.warning('No record found.')
    else: st.warning('No marks yet.')
