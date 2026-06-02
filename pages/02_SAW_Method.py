import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

from style import apply_style, hero, card, step, kpi
from mcdm_utils import CASE_DF, WEIGHT_DF, CRITERIA, TYPES, WEIGHTS, show_case_intro, normalize_saw, rank_df

st.set_page_config(page_title="SAW Method", layout="wide")
apply_style()

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def excel_bytes(sheets: dict) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=name[:31])
    return output.getvalue()


def matrix_df(arr, columns=CRITERIA, index=CASE_DF["Alternative"]):
    return pd.DataFrame(np.round(arr, 6), columns=columns, index=index).reset_index()


def safe_divide_cost(min_value, value):
    if value == 0:
        return np.nan
    return min_value / value


def quiz_block(questions):
    st.subheader("Knowledge Check: 15 Questions")
    st.caption("Answer all questions. The score is shown immediately after submission.")

    with st.form("saw_quiz_form"):
        answers = []
        for idx, q in enumerate(questions, start=1):
            st.markdown(f"**Q{idx}. {q['question']}**")
            answers.append(st.radio("Choose one answer", q["options"], key=f"saw_q{idx}", label_visibility="collapsed"))
            st.write("")
        submitted = st.form_submit_button("Submit SAW Quiz")

    if submitted:
        score = sum(ans == q["answer"] for ans, q in zip(answers, questions))
        st.success(f"Your score: {score} / {len(questions)}")
        review = []
        for idx, (ans, q) in enumerate(zip(answers, questions), start=1):
            review.append({
                "Question": idx,
                "Your Answer": ans,
                "Correct Answer": q["answer"],
                "Result": "Correct" if ans == q["answer"] else "Review needed",
                "Explanation": q["explanation"],
            })
        st.dataframe(pd.DataFrame(review), use_container_width=True)


# -----------------------------------------------------------------------------
# Page title
# -----------------------------------------------------------------------------
hero(
    "02 | SAW Method: Simple Additive Weighting",
    "A detailed step-by-step learning page with proper mathematical notation, manual calculation, real case study, interpretation, sensitivity analysis, downloadable Excel workbook and 15-question quiz."
)

# -----------------------------------------------------------------------------
# Learning outcomes
# -----------------------------------------------------------------------------
card(
    "Learning outcomes",
    """
    <p>After completing this page, learners should be able to:</p>
    <ol>
        <li>explain the logic of the Simple Additive Weighting method;</li>
        <li>distinguish benefit criteria from cost criteria;</li>
        <li>construct the decision matrix, normalized matrix and weighted normalized matrix;</li>
        <li>perform manual SAW calculation step by step;</li>
        <li>interpret the final ranking in a real decision-making context;</li>
        <li>identify the strengths and limitations of SAW;</li>
        <li>perform a simple sensitivity analysis by changing criterion weights.</li>
    </ol>
    """,
    "gold",
)

# -----------------------------------------------------------------------------
# Concept
# -----------------------------------------------------------------------------
st.header("1. What is SAW?")
st.write(
    "Simple Additive Weighting (SAW) is one of the most transparent Multi-Criteria Decision-Making methods. "
    "The main idea is simple: each alternative is evaluated across several criteria, each criterion is normalized, "
    "each normalized value is multiplied by its criterion weight, and the weighted values are added to obtain a final score."
)

card(
    "Core intuition",
    """
    <p>SAW treats the total performance of an alternative as an additive score. If an alternative performs well on highly weighted criteria, its final score will increase. The alternative with the highest total score is considered the best alternative.</p>
    <p>This makes SAW very suitable for teaching, dashboard development, preliminary screening and transparent committee-based evaluation.</p>
    """,
    "blue",
)

st.latex(r"S_i=\sum_{j=1}^{n} w_j r_{ij}")
st.markdown(
    "Where:  "
    "\(S_i\) = final SAW score of alternative \(i\); "
    "\(w_j\) = weight of criterion \(j\); "
    "\(r_{ij}\) = normalized performance value of alternative \(i\) under criterion \(j\); "
    "\(n\) = number of criteria."
)

st.latex(r"A^*=\arg\max_i(S_i)")
st.write("The best alternative is the alternative with the highest SAW score.")

# -----------------------------------------------------------------------------
# Case study
# -----------------------------------------------------------------------------
st.header("2. Real Case Study: Selecting a Digital Transformation Project")
st.write(
    "A university committee needs to choose one digital transformation initiative. The committee considers five criteria: "
    "implementation cost, expected impact, technical feasibility, implementation time and risk exposure. "
    "This case is realistic because universities normally need to balance budget, impact, readiness, delivery time and risk before approving a project."
)
show_case_intro()

st.subheader("2.1 Alternatives")
st.markdown(
    "The alternatives represent possible university digital transformation initiatives. "
    "Each alternative is evaluated using both benefit and cost criteria."
)
st.dataframe(CASE_DF, use_container_width=True)

st.subheader("2.2 Criteria, criterion type and weight")
st.write(
    "A benefit criterion means a higher value is better. A cost criterion means a lower value is better. "
    "The weights show the relative importance of each criterion. The total weight should equal 1."
)
st.dataframe(WEIGHT_DF, use_container_width=True)

c1, c2, c3 = st.columns(3)
with c1:
    kpi("Number of alternatives", len(CASE_DF), "The decision options being compared")
with c2:
    kpi("Number of criteria", len(CRITERIA), "The evaluation dimensions")
with c3:
    kpi("Total weight", f"{WEIGHTS.sum():.2f}", "The sum should be equal to 1")

# -----------------------------------------------------------------------------
# Step by step calculation
# -----------------------------------------------------------------------------
st.header("3. Step-by-Step SAW Calculation")

X = CASE_DF[CRITERIA].to_numpy(dtype=float)
R = normalize_saw(X)
V = R * WEIGHTS
S = V.sum(axis=1)
rank = rank_df(S, "SAW Score")

raw_matrix = CASE_DF[["Alternative"] + CRITERIA]
normalized_matrix = matrix_df(R)
weighted_matrix = matrix_df(V)
score_table = pd.DataFrame({
    "Alternative": CASE_DF["Alternative"],
    "SAW Score": np.round(S, 6),
}).sort_values("SAW Score", ascending=False).reset_index(drop=True)
score_table["Rank"] = range(1, len(score_table) + 1)

step(
    "Step 1: Construct the decision matrix",
    "The decision matrix contains the original performance values. Each row represents one alternative and each column represents one criterion."
)
st.latex(r"X=[x_{ij}]_{m\times n}")
st.dataframe(raw_matrix, use_container_width=True)

step(
    "Step 2: Identify benefit and cost criteria",
    "Expected Impact and Technical Feasibility are benefit criteria because higher values are preferred. Implementation Cost, Implementation Time and Risk Exposure are cost criteria because lower values are preferred."
)
criteria_explanation = WEIGHT_DF.copy()
criteria_explanation["Decision logic"] = [
    "Lower cost is preferred, therefore this is a cost criterion.",
    "Higher expected impact is preferred, therefore this is a benefit criterion.",
    "Higher feasibility means easier implementation, therefore this is a benefit criterion.",
    "Shorter time is preferred, therefore this is a cost criterion.",
    "Lower risk is preferred, therefore this is a cost criterion.",
]
st.dataframe(criteria_explanation, use_container_width=True)

step(
    "Step 3: Normalize the decision matrix",
    "Normalization converts different units into comparable dimensionless values. This is necessary because USD, scores, months and risk values cannot be directly added."
)
st.write("For benefit criteria, the normalized value is calculated as:")
st.latex(r"r_{ij}=\frac{x_{ij}}{\max_i x_{ij}}")
st.write("For cost criteria, the normalized value is calculated as:")
st.latex(r"r_{ij}=\frac{\min_i x_{ij}}{x_{ij}}")
st.write(
    "After normalization, values closer to 1 are better for both benefit and cost criteria. "
    "This is important because SAW later sums all weighted normalized values."
)
st.dataframe(normalized_matrix, use_container_width=True)

# Manual calculation section
st.subheader("3.1 Manual normalization calculation")
st.write("The calculation below shows exactly how the normalized values are obtained for Alternative A1.")

A1 = CASE_DF.iloc[0]
manual_rows = []
for j, crit in enumerate(CRITERIA):
    value = float(A1[crit])
    col = X[:, j]
    if TYPES[j] == "benefit":
        ref = col.max()
        normalized = value / ref
        formula_text = f"{value:g} / {ref:g}"
        logic = "Benefit criterion: divide by the maximum value."
    else:
        ref = col.min()
        normalized = safe_divide_cost(ref, value)
        formula_text = f"{ref:g} / {value:g}"
        logic = "Cost criterion: minimum value divided by the observed value."
    manual_rows.append({
        "Criterion": crit,
        "Type": TYPES[j],
        "A1 original value": value,
        "Reference value": ref,
        "Manual formula": formula_text,
        "Normalized value": round(normalized, 6),
        "Logic": logic,
    })
manual_df = pd.DataFrame(manual_rows)
st.dataframe(manual_df, use_container_width=True)

with st.expander("Show detailed A1 calculation using equations", expanded=True):
    st.markdown("**Implementation Cost (cost criterion)**")
    st.latex(r"r_{11}=\frac{\min(42000,35000,50000,38000)}{42000}=\frac{35000}{42000}=0.833333")
    st.markdown("**Expected Impact Score (benefit criterion)**")
    st.latex(r"r_{12}=\frac{82}{\max(82,78,90,86)}=\frac{82}{90}=0.911111")
    st.markdown("**Technical Feasibility (benefit criterion)**")
    st.latex(r"r_{13}=\frac{88}{\max(88,80,84,76)}=\frac{88}{88}=1.000000")
    st.markdown("**Implementation Time (cost criterion)**")
    st.latex(r"r_{14}=\frac{\min(8,6,10,7)}{8}=\frac{6}{8}=0.750000")
    st.markdown("**Risk Exposure (cost criterion)**")
    st.latex(r"r_{15}=\frac{\min(35,42,30,38)}{35}=\frac{30}{35}=0.857143")

step(
    "Step 4: Calculate the weighted normalized matrix",
    "Each normalized value is multiplied by the corresponding criterion weight. This step converts normalized performance into weighted contribution."
)
st.latex(r"v_{ij}=w_j r_{ij}")
st.dataframe(weighted_matrix, use_container_width=True)

with st.expander("Show detailed A1 weighted calculation", expanded=True):
    st.latex(r"v_{11}=0.22(0.833333)=0.183333")
    st.latex(r"v_{12}=0.30(0.911111)=0.273333")
    st.latex(r"v_{13}=0.20(1.000000)=0.200000")
    st.latex(r"v_{14}=0.15(0.750000)=0.112500")
    st.latex(r"v_{15}=0.13(0.857143)=0.111429")

step(
    "Step 5: Sum the weighted normalized values",
    "The final SAW score is obtained by adding all weighted normalized values for each alternative."
)
st.latex(r"S_i=v_{i1}+v_{i2}+\cdots+v_{in}")
st.latex(r"S_{A1}=0.183333+0.273333+0.200000+0.112500+0.111429=0.880595")
st.dataframe(score_table, use_container_width=True)

# -----------------------------------------------------------------------------
# Interpretation
# -----------------------------------------------------------------------------
st.header("4. Ranking Interpretation")
best_alt = score_table.iloc[0]["Alternative"]
best_score = score_table.iloc[0]["SAW Score"]
card(
    "How to read the result",
    f"""
    <p>The best alternative is <b>{best_alt}</b> because it has the highest SAW score of <b>{best_score}</b>.</p>
    <p>A higher score means that the alternative performs better after considering all normalized criteria and their weights. However, the ranking should not be interpreted as absolute truth. It depends on the selected criteria, data quality, criterion type and weights.</p>
    """,
    "green",
)

contribution = weighted_matrix.copy()
contribution["Total SAW Score"] = np.round(S, 6)
st.subheader("4.1 Contribution analysis")
st.write(
    "This table helps learners trace how each criterion contributes to the final score. "
    "It is useful for explaining why an alternative wins or loses."
)
st.dataframe(contribution, use_container_width=True)

# -----------------------------------------------------------------------------
# Common mistakes
# -----------------------------------------------------------------------------
st.header("5. Common Mistakes in SAW")
common_mistakes = pd.DataFrame({
    "Mistake": [
        "Treating cost criteria as benefit criteria",
        "Adding raw values directly without normalization",
        "Using weights that do not sum to 1",
        "Assuming SAW ranking is always stable",
        "Ignoring zero values in cost criteria",
    ],
    "Why it is a problem": [
        "It rewards high cost, high time or high risk even though these should be minimized.",
        "Different units such as USD and months cannot be added meaningfully.",
        "The final score becomes difficult to interpret and compare.",
        "Small weight changes may change the final ranking.",
        "Cost normalization requires division by x_ij; zero values can cause division errors.",
    ],
    "How to avoid it": [
        "Clearly label each criterion as benefit or cost before calculation.",
        "Normalize every criterion before applying weights.",
        "Check that the total weight equals 1 before ranking.",
        "Perform sensitivity analysis using several weight scenarios.",
        "Use a justified small epsilon or redesign the scale when zero means a special condition.",
    ],
})
st.dataframe(common_mistakes, use_container_width=True)

# -----------------------------------------------------------------------------
# Strengths and limitations
# -----------------------------------------------------------------------------
st.header("6. Strengths and Limitations")
col1, col2 = st.columns(2)
with col1:
    card(
        "Strengths",
        """
        <ul>
            <li>Easy to understand and explain to non-technical stakeholders.</li>
            <li>Calculation is transparent and can be checked manually.</li>
            <li>Suitable for dashboard-based decision support systems.</li>
            <li>Works well for preliminary screening and simple ranking problems.</li>
            <li>Can handle both benefit and cost criteria after normalization.</li>
        </ul>
        """,
        "green",
    )
with col2:
    card(
        "Limitations",
        """
        <ul>
            <li>Assumes full compensation among criteria.</li>
            <li>Highly sensitive to criterion weights.</li>
            <li>Does not measure distance from ideal and anti-ideal solutions.</li>
            <li>Does not model regret, outranking or interdependence among criteria.</li>
            <li>Ranking may change if the normalization method is changed.</li>
        </ul>
        """,
        "red",
    )

# -----------------------------------------------------------------------------
# Sensitivity analysis
# -----------------------------------------------------------------------------
st.header("7. Sensitivity Analysis")
st.write(
    "Sensitivity analysis checks whether the ranking remains stable when the weights change. "
    "This is important because criterion weights are often based on expert judgement."
)

scenarios = {
    "Base weights": np.array([0.22, 0.30, 0.20, 0.15, 0.13]),
    "Impact-focused": np.array([0.15, 0.45, 0.20, 0.10, 0.10]),
    "Cost-focused": np.array([0.40, 0.20, 0.15, 0.15, 0.10]),
    "Risk-focused": np.array([0.15, 0.25, 0.15, 0.15, 0.30]),
}

scenario_rows = []
for scenario, w in scenarios.items():
    scores = R @ w
    order = np.argsort(-scores)
    for rank_no, alt_idx in enumerate(order, start=1):
        scenario_rows.append({
            "Scenario": scenario,
            "Alternative": CASE_DF.loc[alt_idx, "Alternative"],
            "Score": round(scores[alt_idx], 6),
            "Rank": rank_no,
        })
sensitivity_df = pd.DataFrame(scenario_rows)
st.dataframe(sensitivity_df, use_container_width=True)

pivot_rank = sensitivity_df.pivot(index="Alternative", columns="Scenario", values="Rank").reset_index()
st.subheader("7.1 Ranking stability summary")
st.dataframe(pivot_rank, use_container_width=True)
st.write(
    "If the same alternative remains Rank 1 across several scenarios, the decision is more robust. "
    "If the rank changes easily, the committee should discuss the weights more carefully or compare the result with other MCDM methods such as TOPSIS or VIKOR."
)

# -----------------------------------------------------------------------------
# Viva questions
# -----------------------------------------------------------------------------
st.header("8. Possible Viva / Presentation Questions")
viva = pd.DataFrame({
    "Question": [
        "Why did you choose SAW?",
        "Why is normalization required?",
        "How do you treat cost criteria?",
        "What is the main limitation of SAW?",
        "Can a weak criterion be compensated by a strong criterion?",
        "What happens if all values for one criterion are zero?",
        "How do you justify the weights?",
        "How do you check whether the ranking is stable?",
    ],
    "Suggested answer": [
        "SAW is chosen because it is simple, transparent and suitable when the decision problem requires an explainable weighted ranking.",
        "Normalization is required because criteria may use different units such as cost, score, time and risk. Without normalization, the values cannot be meaningfully added.",
        "For cost criteria, lower values are preferred. Therefore, the normalized value is computed using minimum value divided by the observed value.",
        "The main limitation is full compensation. A very good score in one criterion may compensate for poor performance in another criterion.",
        "Yes. SAW is an additive compensatory method. This is useful for simple ranking but may be problematic if some criteria are non-negotiable.",
        "The calculation becomes problematic because division by zero may occur or the criterion may have no discriminating power. The scale and data should be reviewed.",
        "Weights can be justified using expert judgement, AHP, entropy, CRITIC, stakeholder consultation or policy priority.",
        "Ranking stability can be checked through sensitivity analysis by changing weights and observing whether the best alternative remains the same.",
    ],
})
st.dataframe(viva, use_container_width=True)

# -----------------------------------------------------------------------------
# Download
# -----------------------------------------------------------------------------
st.header("9. Downloadable Data and Calculation Workbook")
st.write(
    "The workbook contains raw data, weights, normalized matrix, weighted normalized matrix, final ranking, manual A1 calculation and sensitivity analysis."
)

workbook_sheets = {
    "Raw Data": raw_matrix,
    "Criteria Weights": WEIGHT_DF,
    "Normalized Matrix": normalized_matrix,
    "Weighted Matrix": weighted_matrix,
    "Final Ranking": score_table,
    "Manual A1 Calculation": manual_df,
    "Sensitivity Analysis": sensitivity_df,
    "Ranking Stability": pivot_rank,
    "Viva Questions": viva,
}

st.download_button(
    label="Download SAW complete worked example as Excel",
    data=excel_bytes(workbook_sheets),
    file_name="SAW_complete_worked_example.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# -----------------------------------------------------------------------------
# Quiz
# -----------------------------------------------------------------------------
st.header("10. SAW Quiz")
quiz_questions = [
    {
        "question": "What does SAW stand for?",
        "options": ["Simple Additive Weighting", "Sequential Alternative Weighting", "Standard Analytical Weight", "Simple Average Weighting"],
        "answer": "Simple Additive Weighting",
        "explanation": "SAW means Simple Additive Weighting.",
    },
    {
        "question": "What is the final SAW score based on?",
        "options": ["The sum of weighted normalized values", "Only the highest criterion value", "Only the cost criterion", "The distance from the ideal solution"],
        "answer": "The sum of weighted normalized values",
        "explanation": "SAW adds all weighted normalized criterion values.",
    },
    {
        "question": "Why is normalization required in SAW?",
        "options": ["To convert different units into comparable values", "To remove all weights", "To make all criteria cost criteria", "To avoid ranking alternatives"],
        "answer": "To convert different units into comparable values",
        "explanation": "Criteria may have different units such as USD, months and scores.",
    },
    {
        "question": "Which formula is suitable for benefit criteria in SAW?",
        "options": ["xij / max(xij)", "min(xij) / xij", "max(xij) / xij", "xij - min(xij)"],
        "answer": "xij / max(xij)",
        "explanation": "For benefit criteria, higher is better, so each value is divided by the maximum value.",
    },
    {
        "question": "Which formula is suitable for cost criteria in SAW?",
        "options": ["min(xij) / xij", "xij / max(xij)", "xij / min(xij)", "max(xij) - xij"],
        "answer": "min(xij) / xij",
        "explanation": "For cost criteria, lower is better, so the minimum value is divided by each observed value.",
    },
    {
        "question": "In SAW, the best alternative is usually selected by:",
        "options": ["Highest final score", "Lowest final score", "Highest cost", "Lowest weight"],
        "answer": "Highest final score",
        "explanation": "The alternative with the highest SAW score is preferred.",
    },
    {
        "question": "What does wj represent in the SAW formula?",
        "options": ["Criterion weight", "Alternative number", "Normalized matrix", "Risk value"],
        "answer": "Criterion weight",
        "explanation": "wj represents the importance weight of criterion j.",
    },
    {
        "question": "What does rij represent?",
        "options": ["Normalized value of alternative i under criterion j", "Raw cost value only", "Final rank", "Criterion weight"],
        "answer": "Normalized value of alternative i under criterion j",
        "explanation": "rij is the normalized performance value.",
    },
    {
        "question": "Which statement best describes SAW?",
        "options": ["A compensatory additive method", "A non-compensatory outranking method", "A distance-based method only", "A pairwise comparison method only"],
        "answer": "A compensatory additive method",
        "explanation": "SAW allows strong performance in one criterion to compensate for weaker performance in another.",
    },
    {
        "question": "What is one limitation of SAW?",
        "options": ["It is sensitive to weights", "It cannot use weights", "It cannot use benefit criteria", "It always requires qualitative data only"],
        "answer": "It is sensitive to weights",
        "explanation": "SAW ranking may change when criterion weights change.",
    },
    {
        "question": "If implementation time is a criterion, it is normally treated as:",
        "options": ["Cost criterion", "Benefit criterion", "Random criterion", "Weight criterion"],
        "answer": "Cost criterion",
        "explanation": "Shorter implementation time is usually preferred.",
    },
    {
        "question": "If expected impact is a criterion, it is normally treated as:",
        "options": ["Benefit criterion", "Cost criterion", "Penalty criterion", "Zero criterion"],
        "answer": "Benefit criterion",
        "explanation": "Higher expected impact is preferred.",
    },
    {
        "question": "Why should the total weight normally equal 1?",
        "options": ["To make the score interpretable as a weighted total", "To remove normalization", "To make all ranks equal", "To avoid using criteria"],
        "answer": "To make the score interpretable as a weighted total",
        "explanation": "Weights summing to 1 make the final score easier to interpret.",
    },
    {
        "question": "What is sensitivity analysis used for?",
        "options": ["Checking ranking stability under weight changes", "Deleting all alternatives", "Changing all criteria to cost criteria", "Avoiding calculation"],
        "answer": "Checking ranking stability under weight changes",
        "explanation": "Sensitivity analysis shows whether ranking is robust when weights change.",
    },
    {
        "question": "Which issue may occur when a cost criterion contains zero values?",
        "options": ["Division by zero or undefined normalization", "Weights become negative automatically", "All alternatives become best", "No ranking is ever possible"],
        "answer": "Division by zero or undefined normalization",
        "explanation": "Cost normalization divides by the observed value, so zero values must be handled carefully.",
    },
]
quiz_block(quiz_questions)

# -----------------------------------------------------------------------------
# Closing note
# -----------------------------------------------------------------------------
st.header("11. Summary")
card(
    "Key takeaway",
    """
    <p>SAW is powerful when the purpose is transparent ranking. The method is easy to teach and easy to explain, but it must be applied carefully. The researcher must clearly define criteria, classify benefit and cost criteria, justify weights, normalize correctly, and test ranking stability using sensitivity analysis.</p>
    """,
    "purple",
)
