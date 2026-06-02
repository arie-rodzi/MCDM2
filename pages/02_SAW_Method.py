import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="SAW Method", page_icon="🌿", layout="wide")

# =========================================================
# MATTE GREEN PREMIUM THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(121, 166, 135, 0.25), transparent 32%),
        linear-gradient(135deg, #F4F8F0 0%, #E8F0E3 45%, #DDE9D8 100%);
}
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1250px;}

.hero {
    padding: 34px 34px 30px 34px;
    border-radius: 30px;
    background: linear-gradient(135deg, #0F2F25 0%, #244B3A 55%, #6E8F72 100%);
    color: white;
    box-shadow: 0 24px 60px rgba(15, 47, 37, 0.28);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    right: -70px;
    top: -60px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.13);
}
.hero h1 {font-size: 48px; line-height: 1.05; margin: 0; font-weight: 900; letter-spacing: -1.2px;}
.hero p {font-size: 18px; color: #EAF2E5; margin-top: 12px; max-width: 850px;}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.28);
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 12px;
}

.card {
    background: rgba(255,255,255,0.84);
    border: 1px solid rgba(95, 125, 101, 0.18);
    border-radius: 24px;
    padding: 26px;
    margin: 18px 0;
    box-shadow: 0 14px 38px rgba(33, 64, 46, 0.10);
}
.card h2, .card h3 {color: #173C2D;}
.note {
    background: linear-gradient(135deg, #F8FBF4, #EAF3E5);
    border-left: 7px solid #3E6B4F;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #20372C;
}
.gold-note {
    background: linear-gradient(135deg, #FFF9E7, #F5E7B8);
    border-left: 7px solid #B99535;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3C321C;
}
.success-note {
    background: linear-gradient(135deg, #EAF7EF, #D7EBDC);
    border-left: 7px solid #2D6A4F;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #173C2D;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF, #EFF6EA);
    border: 1px solid rgba(62,107,79,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(33, 64, 46, 0.09);
    text-align: center;
}
.metric-card .big {font-size: 36px; font-weight: 900; color: #173C2D;}
.metric-card .small {font-size: 14px; color: #5A6B5E; font-weight: 700;}
.quiz-box {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(62,107,79,0.18);
    box-shadow: 0 10px 25px rgba(33, 64, 46, 0.06);
    margin: 16px 0 8px 0;
}
[data-testid="stDataFrame"] {border-radius: 18px; overflow: hidden;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #244B3A, #6E8F72) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.1rem !important;
    font-weight: 800 !important;
}
hr {border: none; height: 1px; background: rgba(62,107,79,0.22); margin: 26px 0;}
</style>
""", unsafe_allow_html=True)

GREEN_SCALE = ["#DDEAD7", "#BFD3B7", "#8FB28E", "#5F8C6A", "#2D6A4F", "#173C2D"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def saw_calculation(df, criteria_types, weights):
    matrix = df.set_index("Alternative")
    norm = pd.DataFrame(index=matrix.index)

    for c in matrix.columns:
        values = matrix[c].astype(float)
        if criteria_types[c] == "Benefit":
            max_val = values.max()
            norm[c] = values / max_val if max_val != 0 else 0
        else:
            min_val = values[values > 0].min() if (values > 0).any() else 0
            denominator = values.replace(0, np.nan)
            norm[c] = min_val / denominator if min_val != 0 else 0
            norm[c] = norm[c].replace([np.inf, -np.inf], np.nan).fillna(0)

    weight_series = pd.Series(weights)
    weighted = norm * weight_series
    score = weighted.sum(axis=1)

    result = pd.DataFrame({"Alternative": score.index, "SAW Score": score.values})
    result["Rank"] = result["SAW Score"].rank(ascending=False, method="dense").astype(int)
    return norm, weighted, result.sort_values("Rank")


def to_excel_bytes(original, normalized, weighted, result, sensitivity_df=None):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        original.to_excel(writer, sheet_name="Original Data", index=False)
        normalized.to_excel(writer, sheet_name="Normalized Matrix")
        weighted.to_excel(writer, sheet_name="Weighted Matrix")
        result.to_excel(writer, sheet_name="SAW Result", index=False)
        if sensitivity_df is not None:
            sensitivity_df.to_excel(writer, sheet_name="Sensitivity Analysis", index=False)
    return output.getvalue()


def plotly_green_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#173C2D")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.58)",
        font=dict(color="#20372C"),
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0.65)", bordercolor="rgba(62,107,79,0.20)", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="rgba(62,107,79,0.13)", zerolinecolor="rgba(62,107,79,0.2)")
    fig.update_yaxes(gridcolor="rgba(62,107,79,0.13)", zerolinecolor="rgba(62,107,79,0.2)")
    return fig

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="pill">MCDM Learning Module • Matte Green Edition</div>
    <h1>SAW Method</h1>
    <p>A premium interactive note with real mathematical equations, clear calculation steps, ranking graphs, sensitivity analysis, downloadable Excel output, and a short self-assessment quiz.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
default_df = pd.DataFrame({
    "Alternative": ["Platform A", "Platform B", "Platform C", "Platform D"],
    "Cost": [12000, 15000, 10000, 18000],
    "Usability": [80, 90, 75, 85],
    "Features": [70, 85, 65, 95],
    "Support Time": [12, 8, 15, 6]
})

criteria_types = {"Cost": "Cost", "Usability": "Benefit", "Features": "Benefit", "Support Time": "Cost"}
weights = {"Cost": 0.30, "Usability": 0.30, "Features": 0.25, "Support Time": 0.15}
normalized, weighted, result = saw_calculation(default_df, criteria_types, weights)
best_alt = result.iloc[0]["Alternative"]
best_score = result.iloc[0]["SAW Score"]

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(default_df)}</div><div class='small'>Alternatives</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(weights)}</div><div class='small'>Criteria</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='big'>{best_alt}</div><div class='small'>Best Alternative • Score {best_score:.4f}</div></div>", unsafe_allow_html=True)

# =========================================================
# INTRODUCTION
# =========================================================
st.markdown("""
<div class="card">
<h2>1. Concept Overview</h2>
<p><b>SAW</b> is a transparent MCDM technique that converts different criteria into comparable normalized values, applies criterion weights, and combines them into one final score.</p>
<p>The strength of this method is its simplicity: every step can be explained clearly to students, supervisors, panels, or decision makers. However, the result depends strongly on how the weights are selected, so sensitivity analysis is recommended.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<h3>Real Case Study</h3>
<p>A university wants to choose the most suitable digital learning platform. Four platforms are evaluated using annual cost, usability score, number of features, and support response time.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 2. Original Decision Matrix")
st.dataframe(default_df, use_container_width=True, hide_index=True)

# =========================================================
# EQUATION SECTION WITH REAL LATEX
# =========================================================
st.markdown("""
<div class="card">
<h2>3. Mathematical Formulation</h2>
<p>The decision matrix contains alternatives as rows and criteria as columns. Each value is denoted as <b>x<sub>ij</sub></b>, where alternative <b>i</b> is evaluated under criterion <b>j</b>.</p>
</div>
""", unsafe_allow_html=True)

st.latex(r"X = [x_{ij}]_{m \times n}")
st.latex(r"A_i = \text{alternative } i, \qquad C_j = \text{criterion } j")

left, right = st.columns(2)
with left:
    st.markdown("""
    <div class="success-note">
    <h3>Benefit Criterion</h3>
    <p>Use this when a higher value is better, such as quality, usability, satisfaction, or number of useful features.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_{ij}=\frac{x_{ij}}{\max_i(x_{ij})}")
with right:
    st.markdown("""
    <div class="gold-note">
    <h3>Cost Criterion</h3>
    <p>Use this when a lower value is better, such as cost, time, error, distance, risk, or delay.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_{ij}=\frac{\min_i(x_{ij})}{x_{ij}}")

st.markdown("""
<div class="card">
<h3>Final Weighted Score</h3>
<p>After normalization, every normalized value is multiplied by its criterion weight. The final score is the sum of all weighted normalized values.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"S_i = \sum_{j=1}^{n} w_j r_{ij}, \qquad \sum_{j=1}^{n}w_j=1")

# =========================================================
# STEP-BY-STEP CALCULATION
# =========================================================
st.markdown("## 4. Step-by-Step Worked Calculation")

criteria_df = pd.DataFrame({
    "Criterion": list(weights.keys()),
    "Type": [criteria_types[c] for c in weights.keys()],
    "Weight": [weights[c] for c in weights.keys()],
    "Normalization Logic": ["Lower is better", "Higher is better", "Higher is better", "Lower is better"]
})
st.dataframe(criteria_df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="note">
<h3>Example 1: Cost Normalization</h3>
<p>Cost is a cost criterion, so the minimum value becomes the benchmark. The lowest cost is RM10,000.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\min(12000,15000,10000,18000)=10000")
st.latex(r"r_{A,Cost}=\frac{10000}{12000}=0.8333")
st.latex(r"r_{B,Cost}=\frac{10000}{15000}=0.6667")
st.latex(r"r_{C,Cost}=\frac{10000}{10000}=1.0000")
st.latex(r"r_{D,Cost}=\frac{10000}{18000}=0.5556")

st.markdown("""
<div class="note">
<h3>Example 2: Usability Normalization</h3>
<p>Usability is a benefit criterion, so the maximum value becomes the benchmark. The highest usability score is 90.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\max(80,90,75,85)=90")
st.latex(r"r_{A,Usability}=\frac{80}{90}=0.8889")
st.latex(r"r_{B,Usability}=\frac{90}{90}=1.0000")
st.latex(r"r_{C,Usability}=\frac{75}{90}=0.8333")
st.latex(r"r_{D,Usability}=\frac{85}{90}=0.9444")

st.markdown("## 5. Normalized Matrix")
st.dataframe(normalized.round(4), use_container_width=True)

st.markdown("## 6. Weighted Normalized Matrix")
st.dataframe(weighted.round(4), use_container_width=True)

st.markdown("## 7. Final Score and Ranking")
st.dataframe(result.round(4), use_container_width=True, hide_index=True)

# =========================================================
# GRAPH SECTION
# =========================================================
st.markdown("## 8. Visual Ranking")
fig_score = px.bar(
    result.sort_values("SAW Score", ascending=True),
    x="SAW Score",
    y="Alternative",
    orientation="h",
    text="SAW Score",
    color="SAW Score",
    color_continuous_scale=GREEN_SCALE,
)
fig_score.update_traces(texttemplate="%{text:.4f}", textposition="outside", marker_line_width=0)
fig_score.update_layout(height=440, showlegend=False, coloraxis_showscale=False, xaxis_title="Final Score", yaxis_title="")
fig_score = plotly_green_layout(fig_score, "Final Score by Alternative")
st.plotly_chart(fig_score, use_container_width=True)

st.markdown("""
<div class="success-note">
<h3>Interpretation</h3>
<p>The best alternative is the one with the highest final score. A high score means the alternative performs well after considering criterion type, normalization, weighting, and summation.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SENSITIVITY ANALYSIS
# =========================================================
st.markdown("## 9. Sensitivity Analysis")
st.markdown("""
<div class="card">
<p>Sensitivity analysis checks whether the final ranking remains stable when the weights change. This is important because MCDM results can be influenced by the selected weight structure.</p>
</div>
""", unsafe_allow_html=True)

scenarios = {
    "Base": {"Cost": 0.30, "Usability": 0.30, "Features": 0.25, "Support Time": 0.15},
    "Cost Focus": {"Cost": 0.45, "Usability": 0.20, "Features": 0.20, "Support Time": 0.15},
    "Usability Focus": {"Cost": 0.20, "Usability": 0.45, "Features": 0.20, "Support Time": 0.15},
    "Feature Focus": {"Cost": 0.20, "Usability": 0.20, "Features": 0.45, "Support Time": 0.15},
    "Support Focus": {"Cost": 0.20, "Usability": 0.25, "Features": 0.20, "Support Time": 0.35},
}

sensitivity_rows, rank_rows = [], []
for scenario_name, scenario_weights in scenarios.items():
    _, _, scenario_result = saw_calculation(default_df, criteria_types, scenario_weights)
    for _, row in scenario_result.iterrows():
        sensitivity_rows.append({"Scenario": scenario_name, "Alternative": row["Alternative"], "SAW Score": row["SAW Score"]})
        rank_rows.append({"Scenario": scenario_name, "Alternative": row["Alternative"], "Rank": row["Rank"]})

sensitivity_df = pd.DataFrame(sensitivity_rows)
rank_df = pd.DataFrame(rank_rows)
st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="SAW Score").round(4), use_container_width=True)

fig_sens = px.line(
    sensitivity_df,
    x="Scenario",
    y="SAW Score",
    color="Alternative",
    markers=True,
    color_discrete_sequence=["#173C2D", "#2D6A4F", "#6E8F72", "#B99535"],
)
fig_sens.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens.update_layout(height=500, xaxis_title="Weight Scenario", yaxis_title="Final Score")
fig_sens = plotly_green_layout(fig_sens, "Sensitivity Analysis Across Weight Scenarios")
st.plotly_chart(fig_sens, use_container_width=True)

fig_rank = px.line(
    rank_df,
    x="Scenario",
    y="Rank",
    color="Alternative",
    markers=True,
    color_discrete_sequence=["#173C2D", "#2D6A4F", "#6E8F72", "#B99535"],
)
fig_rank.update_traces(line=dict(width=4), marker=dict(size=10))
fig_rank.update_yaxes(autorange="reversed", dtick=1)
fig_rank.update_layout(height=500, xaxis_title="Weight Scenario", yaxis_title="Rank")
fig_rank = plotly_green_layout(fig_rank, "Ranking Stability Across Scenarios")
st.plotly_chart(fig_rank, use_container_width=True)

# =========================================================
# ZERO VALUE NOTE
# =========================================================
st.markdown("""
<div class="gold-note">
<h3>Important Note on Zero Values</h3>
<p>For cost criteria, the formula contains the original value in the denominator. If a cost value is zero, direct division becomes problematic. In practice, the researcher must justify a treatment strategy such as replacing zero with a very small positive value, using domain-based minimum thresholds, or redesigning the normalization rule.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"r_{ij}=\frac{\min_i(x_{ij})}{x_{ij}}, \qquad x_{ij}\neq 0")

# =========================================================
# DOWNLOAD
# =========================================================
st.markdown("## 10. Download Worked Example")
excel_bytes = to_excel_bytes(default_df, normalized, weighted, result, sensitivity_df)
st.download_button(
    label="Download Worked Example Excel",
    data=excel_bytes,
    file_name="SAW_Method_Worked_Example.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# COMMON MISTAKES
# =========================================================
st.markdown("## 11. Common Mistakes")
st.markdown("""
<div class="card">
<ol>
<li>Using the benefit formula for cost criteria.</li>
<li>Applying weights before normalization.</li>
<li>Using weights that do not sum to 1.</li>
<li>Ignoring zero values in cost criteria.</li>
<li>Assuming the result is always stable without sensitivity analysis.</li>
<li>Using the method when the decision problem requires non-compensatory or outranking logic.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# QUIZ
# =========================================================
st.markdown("## 12. Self-Assessment Quiz")
st.markdown("""
<div class="note">
<p>This quiz contains exactly <b>10 questions</b>: 5 True/False and 5 Multiple Choice questions.</p>
</div>
""", unsafe_allow_html=True)

tf_questions = [
    {"question": "Normalization is needed because criteria may use different units.", "answer": "True"},
    {"question": "Criterion weights are not used in the final score.", "answer": "False"},
    {"question": "Benefit and cost criteria use different normalization formulas.", "answer": "True"},
    {"question": "This method is an outranking method similar to ELECTRE.", "answer": "False"},
    {"question": "The method assumes additive and compensatory scoring.", "answer": "True"},
]

mcq_questions = [
    {"question": "What does SAW stand for?", "options": ["Sequential Alternative Weighting", "Simple Additive Weighting", "Standard Analytical Weight", "Simple Average Weighting"], "answer": "Simple Additive Weighting"},
    {"question": "What is the final score based on?", "options": ["Only the highest criterion value", "Only the cost criterion", "The distance from the ideal solution", "The sum of weighted normalized values"], "answer": "The sum of weighted normalized values"},
    {"question": "Which formula is suitable for benefit criteria?", "options": ["xij / max(xij)", "min(xij) / xij", "max(xij) / xij", "xij - min(xij)"], "answer": "xij / max(xij)"},
    {"question": "Which formula is suitable for cost criteria?", "options": ["xij / max(xij)", "xij / min(xij)", "min(xij) / xij", "max(xij) - xij"], "answer": "min(xij) / xij"},
    {"question": "Why is sensitivity analysis useful?", "options": ["To delete all alternatives", "To change all criteria into cost criteria", "To check ranking stability when weights change", "To avoid calculation"], "answer": "To check ranking stability when weights change"},
]

answers = {}
st.markdown("### Part A: True / False")
for i, q in enumerate(tf_questions, start=1):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"tf_{i}"] = st.radio(f"Answer Q{i}", ["Select answer", "True", "False"], key=f"tf_{i}", label_visibility="collapsed")

st.markdown("### Part B: Multiple Choice")
for i, q in enumerate(mcq_questions, start=6):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"mcq_{i}"] = st.radio(f"Answer Q{i}", ["Select answer"] + q["options"], key=f"mcq_{i}", label_visibility="collapsed")

if st.button("Submit Quiz"):
    incomplete = any(v == "Select answer" for v in answers.values())
    if incomplete:
        st.error("Please answer all 10 questions before submitting.")
    else:
        score = 0
        review_rows = []
        for i, q in enumerate(tf_questions, start=1):
            correct = answers[f"tf_{i}"] == q["answer"]
            score += int(correct)
            review_rows.append({"Question": f"Q{i}", "Your Answer": answers[f"tf_{i}"], "Correct Answer": q["answer"], "Status": "Correct" if correct else "Incorrect"})
        for i, q in enumerate(mcq_questions, start=6):
            correct = answers[f"mcq_{i}"] == q["answer"]
            score += int(correct)
            review_rows.append({"Question": f"Q{i}", "Your Answer": answers[f"mcq_{i}"], "Correct Answer": q["answer"], "Status": "Correct" if correct else "Incorrect"})

        percentage = score / 10 * 100
        st.subheader(f"Your Score: {score}/10 ({percentage:.0f}%)")
        if percentage >= 90:
            st.success("Excellent. You have mastered the fundamental concept.")
        elif percentage >= 70:
            st.info("Good. Review normalization and sensitivity analysis to improve further.")
        else:
            st.warning("Please revisit the worked calculation before moving to another MCDM method.")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)

st.markdown("""
<hr>
<div class="card">
<h2>Final Summary</h2>
<p>This method is simple, transparent, and easy to defend. The most important parts are correct normalization, justified weights, clear ranking interpretation, and sensitivity analysis.</p>
</div>
""", unsafe_allow_html=True)
