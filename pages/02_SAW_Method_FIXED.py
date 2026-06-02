
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="SAW Method", page_icon="📘", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 900;
    color: #12355B;
    margin-bottom: 0px;
}
.sub-title {
    font-size: 18px;
    color: #5B6470;
    margin-top: 0px;
}
.section-card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E8ECF3;
    box-shadow: 0 4px 18px rgba(18, 53, 91, 0.06);
    margin-bottom: 20px;
}
.info-box {
    background: #F7FAFF;
    padding: 18px;
    border-left: 6px solid #12355B;
    border-radius: 12px;
    margin-bottom: 18px;
}
.warning-box {
    background: #FFF8E7;
    padding: 18px;
    border-left: 6px solid #C58A00;
    border-radius: 12px;
    margin-bottom: 18px;
}
.success-box {
    background: #F0FFF7;
    padding: 18px;
    border-left: 6px solid #0E8F5A;
    border-radius: 12px;
    margin-bottom: 18px;
}
.quiz-box {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E1E7F0;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPER FUNCTIONS
# =========================
def saw_calculation(df, criteria_types, weights):
    matrix = df.set_index("Alternative")
    norm = pd.DataFrame(index=matrix.index)

    for c in matrix.columns:
        values = matrix[c].astype(float)
        if criteria_types[c] == "Benefit":
            max_val = values.max()
            norm[c] = values / max_val if max_val != 0 else 0
        else:
            min_val = values.min()
            norm[c] = min_val / values.replace(0, np.nan)
            norm[c] = norm[c].replace([np.inf, -np.inf], np.nan).fillna(0)

    weight_series = pd.Series(weights)
    weighted = norm * weight_series
    score = weighted.sum(axis=1)

    result = pd.DataFrame({
        "Alternative": score.index,
        "SAW Score": score.values
    })
    result["Rank"] = result["SAW Score"].rank(ascending=False, method="dense").astype(int)
    result = result.sort_values("Rank")

    return norm, weighted, result

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

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">Simple Additive Weighting (SAW) Method</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A detailed step-by-step MCDM learning page with real case study, equations, calculation, graphs, sensitivity analysis and quiz.</div>', unsafe_allow_html=True)

# =========================
# INTRODUCTION
# =========================
st.markdown("""
<div class="section-card">

## 1. Introduction to SAW

Simple Additive Weighting (SAW) is one of the most widely used Multi-Criteria Decision-Making (MCDM) methods.
It is also known as the weighted sum model.

SAW evaluates each alternative by normalizing the performance values, multiplying them by criterion weights, and summing them into one final score.

The alternative with the highest final SAW score is usually selected as the best alternative.

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">

### Real Case Study

A university wants to select the best digital learning platform for students.

Four platforms are evaluated:

1. Platform A  
2. Platform B  
3. Platform C  
4. Platform D  

The decision is based on four criteria:

| Criterion | Meaning | Type |
|---|---|---|
| Cost | Annual subscription cost in RM | Cost |
| Usability | Ease of use score | Benefit |
| Features | Number of useful features | Benefit |
| Support Time | Average support response time in hours | Cost |

</div>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
default_df = pd.DataFrame({
    "Alternative": ["Platform A", "Platform B", "Platform C", "Platform D"],
    "Cost": [12000, 15000, 10000, 18000],
    "Usability": [80, 90, 75, 85],
    "Features": [70, 85, 65, 95],
    "Support Time": [12, 8, 15, 6]
})

criteria_types = {
    "Cost": "Cost",
    "Usability": "Benefit",
    "Features": "Benefit",
    "Support Time": "Cost"
}

weights = {
    "Cost": 0.30,
    "Usability": 0.30,
    "Features": 0.25,
    "Support Time": 0.15
}

st.markdown("## 2. Original Decision Matrix")
st.dataframe(default_df, use_container_width=True)

st.markdown("""
### Decision Matrix Notation

Let:

- \( A_i \) = alternative \( i \)
- \( C_j \) = criterion \( j \)
- \( x_{ij} \) = original value of alternative \( i \) under criterion \( j \)

The decision matrix is:

\[
X =
[x_{ij}]_{m \\times n}
\]

where \( m \) is the number of alternatives and \( n \) is the number of criteria.
""")

# =========================
# EQUATIONS
# =========================
st.markdown("## 3. SAW Mathematical Formulation")

st.markdown("""
### Benefit Criterion Normalization

For benefit criteria, a higher value is better.

\[
r_{ij} = \\frac{x_{ij}}{\\max(x_{ij})}
\]

Example: usability score, expected impact, quality score.

### Cost Criterion Normalization

For cost criteria, a lower value is better.

\[
r_{ij} = \\frac{\\min(x_{ij})}{x_{ij}}
\]

Example: cost, time, risk, error rate.

### Final SAW Score

\[
S_i = \\sum_{j=1}^{n} w_j r_{ij}
\]

where:

- \( S_i \) = final SAW score for alternative \( i \)
- \( w_j \) = weight of criterion \( j \)
- \( r_{ij} \) = normalized value
""")

# =========================
# STEP BY STEP CALCULATION
# =========================
st.markdown("## 4. Step-by-Step Manual Calculation")

st.markdown("""
### Step 1: Identify Benefit and Cost Criteria

| Criterion | Type | Normalization Formula |
|---|---|---|
| Cost | Cost | min(x) / x |
| Usability | Benefit | x / max(x) |
| Features | Benefit | x / max(x) |
| Support Time | Cost | min(x) / x |
""")

st.markdown("""
### Step 2: Example Calculation for Cost

Cost values:

\[
12000, 15000, 10000, 18000
\]

Minimum cost:

\[
\\min(x) = 10000
\]

For Platform A:

\[
r_{A,Cost} = \\frac{10000}{12000} = 0.8333
\]

For Platform B:

\[
r_{B,Cost} = \\frac{10000}{15000} = 0.6667
\]

For Platform C:

\[
r_{C,Cost} = \\frac{10000}{10000} = 1.0000
\]

For Platform D:

\[
r_{D,Cost} = \\frac{10000}{18000} = 0.5556
\]
""")

st.markdown("""
### Step 3: Example Calculation for Benefit

Usability values:

\[
80, 90, 75, 85
\]

Maximum usability:

\[
\\max(x) = 90
\]

For Platform A:

\[
r_{A,Usability} = \\frac{80}{90} = 0.8889
\]

For Platform B:

\[
r_{B,Usability} = \\frac{90}{90} = 1.0000
\]

For Platform C:

\[
r_{C,Usability} = \\frac{75}{90} = 0.8333
\]

For Platform D:

\[
r_{D,Usability} = \\frac{85}{90} = 0.9444
\]
""")

normalized, weighted, result = saw_calculation(default_df, criteria_types, weights)

st.markdown("## 5. Normalized Matrix")
st.dataframe(normalized.round(4), use_container_width=True)

st.markdown("## 6. Weight Vector")

weight_df = pd.DataFrame({
    "Criterion": list(weights.keys()),
    "Weight": list(weights.values()),
    "Type": [criteria_types[c] for c in weights.keys()]
})
st.dataframe(weight_df, use_container_width=True)

st.markdown("""
The total weight is:

\[
0.30 + 0.30 + 0.25 + 0.15 = 1.00
\]

This means the final SAW score can be interpreted as a weighted total of normalized performance.
""")

st.markdown("## 7. Weighted Normalized Matrix")
st.dataframe(weighted.round(4), use_container_width=True)

st.markdown("## 8. Final SAW Score and Ranking")
st.dataframe(result.round(4), use_container_width=True)

# =========================
# GRAPH 1
# =========================
st.markdown("## 9. Graph: Final SAW Score by Alternative")

fig_score = px.bar(
    result.sort_values("SAW Score", ascending=True),
    x="SAW Score",
    y="Alternative",
    orientation="h",
    text="SAW Score",
    title="Final SAW Score Ranking"
)
fig_score.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_score.update_layout(
    height=430,
    xaxis_title="SAW Score",
    yaxis_title="Alternative",
    showlegend=False
)
st.plotly_chart(fig_score, use_container_width=True)

st.markdown("""
<div class="success-box">

### Interpretation

The best alternative is the one with the highest SAW score.

A high score means the alternative performs well after considering:

- criterion type,
- normalization,
- criterion weight, and
- weighted summation.

</div>
""", unsafe_allow_html=True)

# =========================
# SENSITIVITY ANALYSIS
# =========================
st.markdown("## 10. Sensitivity Analysis")

st.markdown("""
Sensitivity analysis checks whether the final ranking remains stable when the weights are changed.

This is important because MCDM results may be sensitive to subjective weighting.
If a small change in weight produces a major ranking change, the decision is not very stable.
""")

scenarios = {
    "Base": {"Cost": 0.30, "Usability": 0.30, "Features": 0.25, "Support Time": 0.15},
    "Cost Focus": {"Cost": 0.45, "Usability": 0.20, "Features": 0.20, "Support Time": 0.15},
    "Usability Focus": {"Cost": 0.20, "Usability": 0.45, "Features": 0.20, "Support Time": 0.15},
    "Feature Focus": {"Cost": 0.20, "Usability": 0.20, "Features": 0.45, "Support Time": 0.15},
    "Support Focus": {"Cost": 0.20, "Usability": 0.25, "Features": 0.20, "Support Time": 0.35},
}

sensitivity_rows = []
rank_rows = []

for scenario_name, scenario_weights in scenarios.items():
    _, _, scenario_result = saw_calculation(default_df, criteria_types, scenario_weights)
    for _, row in scenario_result.iterrows():
        sensitivity_rows.append({
            "Scenario": scenario_name,
            "Alternative": row["Alternative"],
            "SAW Score": row["SAW Score"]
        })
        rank_rows.append({
            "Scenario": scenario_name,
            "Alternative": row["Alternative"],
            "Rank": row["Rank"]
        })

sensitivity_df = pd.DataFrame(sensitivity_rows)
rank_df = pd.DataFrame(rank_rows)

st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="SAW Score").round(4), use_container_width=True)

# =========================
# GRAPH 2
# =========================
st.markdown("## 11. Graph: Sensitivity Analysis Score Pattern")

fig_sens = px.line(
    sensitivity_df,
    x="Scenario",
    y="SAW Score",
    color="Alternative",
    markers=True,
    title="Sensitivity Analysis: SAW Score Across Weight Scenarios"
)
fig_sens.update_layout(
    height=500,
    xaxis_title="Weight Scenario",
    yaxis_title="SAW Score",
    legend_title="Alternative"
)
st.plotly_chart(fig_sens, use_container_width=True)

# =========================
# GRAPH 3
# =========================
st.markdown("## 12. Graph: Ranking Stability")

fig_rank = px.line(
    rank_df,
    x="Scenario",
    y="Rank",
    color="Alternative",
    markers=True,
    title="Ranking Stability Across Weight Scenarios"
)
fig_rank.update_yaxes(autorange="reversed", dtick=1)
fig_rank.update_layout(
    height=500,
    xaxis_title="Weight Scenario",
    yaxis_title="Rank"
)
st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("""
<div class="warning-box">

### Important Note

If the ranking changes significantly across scenarios, the decision maker must be careful.
It means the result depends strongly on the selected weight structure.

</div>
""", unsafe_allow_html=True)

# =========================
# DOWNLOAD
# =========================
st.markdown("## 13. Download Worked Example Data")

excel_bytes = to_excel_bytes(default_df, normalized, weighted, result, sensitivity_df)

st.download_button(
    label="Download SAW Worked Example Excel",
    data=excel_bytes,
    file_name="SAW_Worked_Example_With_Sensitivity.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================
# COMMON MISTAKES
# =========================
st.markdown("## 14. Common Mistakes in SAW")

st.markdown("""
1. Using the benefit formula for cost criteria.
2. Forgetting to normalize data before applying weights.
3. Using weights that do not sum to 1.
4. Assuming SAW can model interaction among criteria.
5. Ignoring sensitivity analysis.
6. Treating all criteria as equally important without justification.
7. Using SAW when the decision problem requires outranking logic.
8. Not checking zero values in cost criteria.
""")

# =========================
# QUIZ
# =========================
st.markdown("## 15. Self-Assessment Quiz")

st.markdown("""
This quiz contains exactly 10 questions:

- 5 True / False questions
- 5 Multiple Choice questions
""")

tf_questions = [
    {
        "question": "SAW requires normalization because criteria may have different units.",
        "answer": "True"
    },
    {
        "question": "SAW does not use criterion weights.",
        "answer": "False"
    },
    {
        "question": "Benefit and cost criteria use different normalization formulas in SAW.",
        "answer": "True"
    },
    {
        "question": "SAW is an outranking method similar to ELECTRE.",
        "answer": "False"
    },
    {
        "question": "SAW assumes that criteria are independent and additive.",
        "answer": "True"
    }
]

mcq_questions = [
    {
        "question": "What does SAW stand for?",
        "options": [
            "Sequential Alternative Weighting",
            "Simple Additive Weighting",
            "Standard Analytical Weight",
            "Simple Average Weighting"
        ],
        "answer": "Simple Additive Weighting"
    },
    {
        "question": "What is the final SAW score based on?",
        "options": [
            "Only the highest criterion value",
            "Only the cost criterion",
            "The distance from the ideal solution",
            "The sum of weighted normalized values"
        ],
        "answer": "The sum of weighted normalized values"
    },
    {
        "question": "Which formula is suitable for benefit criteria in SAW?",
        "options": [
            "xij / max(xij)",
            "min(xij) / xij",
            "max(xij) / xij",
            "xij - min(xij)"
        ],
        "answer": "xij / max(xij)"
    },
    {
        "question": "Which formula is suitable for cost criteria in SAW?",
        "options": [
            "xij / max(xij)",
            "xij / min(xij)",
            "min(xij) / xij",
            "max(xij) - xij"
        ],
        "answer": "min(xij) / xij"
    },
    {
        "question": "What is sensitivity analysis used for in SAW?",
        "options": [
            "Deleting all alternatives",
            "Changing all criteria to cost criteria",
            "Checking ranking stability under weight changes",
            "Avoiding calculation"
        ],
        "answer": "Checking ranking stability under weight changes"
    }
]

answers = {}

st.markdown("### Part A: True / False")

for i, q in enumerate(tf_questions, start=1):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"tf_{i}"] = st.radio(
        label=f"Answer Q{i}",
        options=["Select answer", "True", "False"],
        key=f"tf_{i}",
        label_visibility="collapsed"
    )

st.markdown("### Part B: Multiple Choice")

for i, q in enumerate(mcq_questions, start=6):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"mcq_{i}"] = st.radio(
        label=f"Answer Q{i}",
        options=["Select answer"] + q["options"],
        key=f"mcq_{i}",
        label_visibility="collapsed"
    )

if st.button("Submit Quiz"):
    incomplete = any(v == "Select answer" for v in answers.values())

    if incomplete:
        st.error("Please answer all 10 questions before submitting.")
    else:
        score = 0

        for i, q in enumerate(tf_questions, start=1):
            if answers[f"tf_{i}"] == q["answer"]:
                score += 1

        for i, q in enumerate(mcq_questions, start=6):
            if answers[f"mcq_{i}"] == q["answer"]:
                score += 1

        percentage = score / 10 * 100

        st.subheader(f"Your Score: {score}/10 ({percentage:.0f}%)")

        if percentage >= 90:
            st.success("Excellent. You have mastered the fundamental concept of SAW.")
        elif percentage >= 70:
            st.info("Good. You understand the main ideas, but you should revisit normalization and sensitivity analysis.")
        else:
            st.warning("Needs improvement. Please review the step-by-step calculation before proceeding to another MCDM method.")

        review_rows = []

        for i, q in enumerate(tf_questions, start=1):
            review_rows.append({
                "Question": f"Q{i}",
                "Your Answer": answers[f"tf_{i}"],
                "Correct Answer": q["answer"],
                "Status": "Correct" if answers[f"tf_{i}"] == q["answer"] else "Incorrect"
            })

        for i, q in enumerate(mcq_questions, start=6):
            review_rows.append({
                "Question": f"Q{i}",
                "Your Answer": answers[f"mcq_{i}"],
                "Correct Answer": q["answer"],
                "Status": "Correct" if answers[f"mcq_{i}"] == q["answer"] else "Incorrect"
            })

        review_df = pd.DataFrame(review_rows)
        st.dataframe(review_df, use_container_width=True)

# =========================
# CLOSING
# =========================
st.markdown("""
---
### Summary

SAW is simple, transparent and easy to explain. However, it is sensitive to criterion weights and assumes that criteria are independent and compensatory.

Therefore, SAW should always be supported by:

1. clear normalization,
2. justified weights,
3. step-by-step calculation,
4. ranking interpretation, and
5. sensitivity analysis.
""")
