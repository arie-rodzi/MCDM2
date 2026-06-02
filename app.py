import streamlit as st
from style import apply_style

st.set_page_config(page_title="MCDM Masterclass", page_icon="📊", layout="wide")
apply_style()

st.markdown("""
<style>
.intro-hero{
    padding:42px;
    border-radius:32px;
    background:linear-gradient(135deg,#071B3A,#20143F 55%,#321B4F);
    color:white;
    box-shadow:0 25px 70px rgba(0,0,0,.35);
    border:1px solid rgba(255,255,255,.16);
}
.intro-hero h1{
    font-size:54px;
    font-weight:900;
    margin-bottom:12px;
}
.intro-hero p{
    font-size:20px;
    line-height:1.75;
    color:#E8ECFF;
}
.premium-card{
    margin-top:26px;
    padding:32px;
    border-radius:28px;
    background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.16);
    color:white;
    box-shadow:0 18px 50px rgba(0,0,0,.22);
}
.premium-card h2{
    font-size:34px;
    font-weight:850;
    margin-bottom:18px;
}
.method-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:18px;
    margin-top:20px;
}
.method-box{
    padding:22px;
    border-radius:22px;
    background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.06));
    border:1px solid rgba(255,255,255,.16);
}
.method-box h3{
    font-size:22px;
    margin-bottom:8px;
}
.method-box p{
    color:#E7E9FF;
    font-size:16px;
    line-height:1.55;
}
.path-box{
    padding:18px 22px;
    border-radius:18px;
    margin:12px 0;
    background:rgba(255,255,255,.10);
    border-left:6px solid #7DE3FF;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-hero">
    <h1>MCDM Masterclass</h1>
    <p>
    A premium learning platform for Multi-Criteria Decision-Making, designed for
    students, researchers, lecturers, and decision-makers who want to understand
    how alternatives are evaluated, weighted, ranked, and interpreted using
    structured mathematical decision models.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="premium-card">
    <h2>Welcome to the MCDM Masterclass</h2>
    <p>
    Multi-Criteria Decision-Making is used when a decision cannot be made using
    one factor alone. In real situations, decision-makers often need to balance
    cost, quality, risk, performance, usability, expert judgement, and strategic
    importance at the same time.
    </p>
    <p>
    This app introduces six important MCDM methods through clear explanations,
    proper mathematical equations, real case studies, step-by-step calculations,
    interactive visualisation, quizzes, and downloadable Excel workbooks.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="premium-card">
    <h2>Six Core Methods Covered</h2>
    <div class="method-grid">
        <div class="method-box">
            <h3>🌿 SAW Method</h3>
            <p>Simple weighted ranking method based on normalization and weighted summation.</p>
        </div>
        <div class="method-box">
            <h3>❤️ TOPSIS Method</h3>
            <p>Ranks alternatives based on distance from the positive and negative ideal solutions.</p>
        </div>
        <div class="method-box">
            <h3>💜 VIKOR Method</h3>
            <p>Provides a compromise solution using utility, regret, and Q index analysis.</p>
        </div>
        <div class="method-box">
            <h3>🔵 AHP Method</h3>
            <p>Determines criteria weights using expert pairwise comparison and consistency checking.</p>
        </div>
        <div class="method-box">
            <h3>🧡 CRITIC Method</h3>
            <p>Produces objective weights using standard deviation and correlation among criteria.</p>
        </div>
        <div class="method-box">
            <h3>⚫ DEMATEL Method</h3>
            <p>Analyses cause-and-effect relationships among factors using influence matrices.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="premium-card">
    <h2>Recommended Learning Path</h2>
    <div class="path-box">Step 1: Understand the general foundation of MCDM.</div>
    <div class="path-box">Step 2: Learn AHP and CRITIC for weight determination.</div>
    <div class="path-box">Step 3: Study SAW as the basic ranking method.</div>
    <div class="path-box">Step 4: Move to TOPSIS and VIKOR for advanced ranking analysis.</div>
    <div class="path-box">Step 5: Explore DEMATEL for cause-and-effect analysis.</div>
    <div class="path-box">Step 6: Complete quizzes and verify the calculation using Excel workbooks.</div>
</div>
""", unsafe_allow_html=True)
