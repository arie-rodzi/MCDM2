
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="AHP Method", page_icon="🔵", layout="wide")

# =========================================================
# PREMIUM NAVY BLUE THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.20), transparent 34%),
        radial-gradient(circle at bottom right, rgba(15, 23, 42, 0.14), transparent 30%),
        linear-gradient(135deg, #F5F8FF 0%, #E9F0FF 45%, #DCE8FF 100%);
}
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1280px;}

.hero {
    padding: 36px 36px 32px 36px;
    border-radius: 30px;
    background: linear-gradient(135deg, #07182F 0%, #123B73 52%, #2F80ED 100%);
    color: white;
    box-shadow: 0 24px 62px rgba(18, 59, 115, 0.30);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    right: -70px;
    top: -60px;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.13);
}
.hero:before {
    content: "";
    position: absolute;
    left: -85px;
    bottom: -95px;
    width: 235px;
    height: 235px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
}
.hero h1 {font-size: 50px; line-height: 1.05; margin: 0; font-weight: 900; letter-spacing: -1.3px;}
.hero p {font-size: 18px; color: #EAF2FF; margin-top: 12px; max-width: 920px;}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.28);
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 12px;
}
.card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(37, 99, 235, 0.18);
    border-radius: 24px;
    padding: 26px;
    margin: 18px 0;
    box-shadow: 0 14px 38px rgba(15, 23, 42, 0.10);
}
.card h2, .card h3 {color: #0B2A55;}
.note {
    background: linear-gradient(135deg, #F8FBFF, #E4EDFF);
    border-left: 7px solid #2563EB;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #12243D;
}
.dark-note {
    background: linear-gradient(135deg, #07182F, #123B73);
    border-left: 7px solid #93C5FD;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #F8FBFF;
}
.gold-note {
    background: linear-gradient(135deg, #FFF8E5, #F2DB9B);
    border-left: 7px solid #B88928;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3C2E17;
}
.success-note {
    background: linear-gradient(135deg, #F4FFF8, #DDF4E8);
    border-left: 7px solid #23835A;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #123C2B;
}
.warning-note {
    background: linear-gradient(135deg, #FFF7ED, #FED7AA);
    border-left: 7px solid #EA580C;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #4A2508;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF, #EAF2FF);
    border: 1px solid rgba(37,99,235,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.09);
    text-align: center;
    min-height: 108px;
}
.metric-card .big {font-size: 32px; font-weight: 900; color: #0B2A55;}
.metric-card .small {font-size: 14px; color: #526176; font-weight: 800;}
.quiz-box {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(37,99,235,0.18);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
    margin: 16px 0 8px 0;
}
.step-card {
    background: rgba(255,255,255,0.78);
    border: 1px dashed rgba(37,99,235,0.38);
    border-radius: 20px;
    padding: 19px;
    margin: 10px 0;
}
[data-testid="stDataFrame"] {border-radius: 18px; overflow: hidden;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #123B73, #2F80ED) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.1rem !important;
    font-weight: 800 !important;
}
hr {border: none; height: 1px; background: rgba(37,99,235,0.22); margin: 26px 0;}
</style>
""", unsafe_allow_html=True)

BLUE_SCALE = ["#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA", "#2563EB", "#123B73", "#07182F"]
BLUE_DISCRETE = ["#07182F", "#123B73", "#2563EB", "#60A5FA", "#B88928", "#23835A"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
RI_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}


def calculate_ahp(matrix: pd.DataFrame):
    """Return normalized matrix, priority vector, lambda max, CI, CR for a pairwise matrix."""
    arr = matrix.astype(float).values
    n = arr.shape[0]
    col_sum = arr.sum(axis=0)
    normalized = arr / col_sum
    weights = normalized.mean(axis=1)
    weighted_sum = arr @ weights
    consistency_vector = weighted_sum / weights
    lambda_max = consistency_vector.mean()
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri != 0 else 0.0
    norm_df = pd.DataFrame(normalized, index=matrix.index, columns=matrix.columns)
    weight_series = pd.Series(weights, index=matrix.index, name="Priority Weight")
    consistency_df = pd.DataFrame({
        "Weighted Sum": weighted_sum,
        "Priority Weight": weights,
        "Consistency Vector": consistency_vector
    }, index=matrix.index)
    return norm_df, weight_series, lambda_max, ci, cr, consistency_df


def reciprocal_matrix(items, upper_values):
    """Build reciprocal matrix from upper triangle dictionary."""
    n = len(items)
    mat = np.ones((n, n), dtype=float)
    for (i, j), val in upper_values.items():
        mat[i, j] = val
        mat[j, i] = 1 / val
    return pd.DataFrame(mat, index=items, columns=items)


def consistency_status(cr):
    if cr <= 0.10:
        return "Acceptable", "The judgement matrix is sufficiently consistent for learning and demonstration."
    if cr <= 0.20:
        return "Review Recommended", "The matrix is usable for classroom illustration, but the pairwise judgements should be reviewed."
    return "Not Acceptable", "The pairwise judgements are inconsistent and should be revised before making a final decision."


def plotly_blue_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#0B2A55")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.60)",
        font=dict(color="#12243D"),
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0.70)", bordercolor="rgba(37,99,235,0.20)", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="rgba(37,99,235,0.12)", zerolinecolor="rgba(37,99,235,0.18)")
    fig.update_yaxes(gridcolor="rgba(37,99,235,0.12)", zerolinecolor="rgba(37,99,235,0.18)")
    return fig


def to_excel_bytes(criteria_matrix, criteria_norm, criteria_weights, criteria_consistency,
                   alternative_matrices, alternative_norms, alternative_weights,
                   global_priority, final_result, sensitivity_df, summary_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        criteria_matrix.to_excel(writer, sheet_name="Criteria Pairwise")
        criteria_norm.to_excel(writer, sheet_name="Criteria Normalized")
        criteria_weights.to_frame().to_excel(writer, sheet_name="Criteria Weights")
        criteria_consistency.to_excel(writer, sheet_name="Criteria Consistency")
        global_priority.to_excel(writer, sheet_name="Global Priority Matrix")
        final_result.to_excel(writer, sheet_name="Final Ranking", index=False)
        sensitivity_df.to_excel(writer, sheet_name="Sensitivity", index=False)
        summary_df.to_excel(writer, sheet_name="Consistency Summary", index=False)
        for criterion, mat in alternative_matrices.items():
            safe = criterion[:20].replace("/", "-")
            mat.to_excel(writer, sheet_name=f"Alt {safe}")
            alternative_norms[criterion].to_excel(writer, sheet_name=f"Norm {safe}")
            alternative_weights[criterion].to_frame(name="Local Priority").to_excel(writer, sheet_name=f"Local {safe}")
    return output.getvalue()


# =========================================================
# DEFAULT AHP CASE STUDY DATA
# =========================================================
criteria = ["Cost", "Usability", "Security", "Features", "Support"]
alternatives = ["Platform A", "Platform B", "Platform C", "Platform D"]

# Criteria pairwise judgement matrix.
# Interpretation: value > 1 means row criterion is more important than column criterion.
criteria_matrix = reciprocal_matrix(criteria, {
    (0, 1): 1/2,   # Cost is moderately less important than Usability
    (0, 2): 1/3,   # Cost is less important than Security
    (0, 3): 2,     # Cost is slightly more important than Features
    (0, 4): 3,     # Cost is moderately more important than Support
    (1, 2): 1/2,   # Usability is slightly less important than Security
    (1, 3): 3,     # Usability is moderately more important than Features
    (1, 4): 4,     # Usability is strongly more important than Support
    (2, 3): 4,     # Security is strongly more important than Features
    (2, 4): 5,     # Security is strongly more important than Support
    (3, 4): 2,     # Features is slightly more important than Support
})

# Alternative pairwise matrices under each criterion.
# Cost judgement: lower cost is preferred, so cheaper platform receives stronger preference.
alternative_matrices = {
    "Cost": reciprocal_matrix(alternatives, {
        (0, 1): 2,
        (0, 2): 1/2,
        (0, 3): 4,
        (1, 2): 1/4,
        (1, 3): 3,
        (2, 3): 5,
    }),
    "Usability": reciprocal_matrix(alternatives, {
        (0, 1): 1/3,
        (0, 2): 2,
        (0, 3): 1/2,
        (1, 2): 5,
        (1, 3): 2,
        (2, 3): 1/4,
    }),
    "Security": reciprocal_matrix(alternatives, {
        (0, 1): 1/2,
        (0, 2): 3,
        (0, 3): 1/3,
        (1, 2): 4,
        (1, 3): 1/2,
        (2, 3): 1/5,
    }),
    "Features": reciprocal_matrix(alternatives, {
        (0, 1): 1/2,
        (0, 2): 3,
        (0, 3): 1/4,
        (1, 2): 4,
        (1, 3): 1/3,
        (2, 3): 1/6,
    }),
    "Support": reciprocal_matrix(alternatives, {
        (0, 1): 1/2,
        (0, 2): 3,
        (0, 3): 1/3,
        (1, 2): 4,
        (1, 3): 1/2,
        (2, 3): 1/5,
    }),
}

criteria_norm, criteria_weights, criteria_lambda, criteria_ci, criteria_cr, criteria_consistency = calculate_ahp(criteria_matrix)

alternative_norms = {}
alternative_weights = {}
alternative_metrics = []
for criterion, mat in alternative_matrices.items():
    ndf, w, lmax, ci, cr, cdf = calculate_ahp(mat)
    alternative_norms[criterion] = ndf
    alternative_weights[criterion] = w
    status, message = consistency_status(cr)
    alternative_metrics.append({
        "Matrix": f"Alternatives under {criterion}",
        "n": len(mat),
        "lambda_max": lmax,
        "CI": ci,
        "RI": RI_TABLE[len(mat)],
        "CR": cr,
        "Status": status
    })

local_priority_matrix = pd.DataFrame({c: alternative_weights[c] for c in criteria})
global_priority = local_priority_matrix.multiply(criteria_weights, axis=1)
final_scores = global_priority.sum(axis=1)
final_result = pd.DataFrame({
    "Alternative": final_scores.index,
    "AHP Final Priority": final_scores.values
})
final_result["Rank"] = final_result["AHP Final Priority"].rank(ascending=False, method="dense").astype(int)
final_result = final_result.sort_values("Rank")
best_alt = final_result.iloc[0]["Alternative"]
best_score = final_result.iloc[0]["AHP Final Priority"]

criteria_status, criteria_message = consistency_status(criteria_cr)
summary_df = pd.DataFrame([{
    "Matrix": "Criteria Pairwise Matrix",
    "n": len(criteria_matrix),
    "lambda_max": criteria_lambda,
    "CI": criteria_ci,
    "RI": RI_TABLE[len(criteria_matrix)],
    "CR": criteria_cr,
    "Status": criteria_status
}] + alternative_metrics)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="pill">MCDM Learning Module • Premium Navy Blue Edition</div>
    <h1>AHP Method</h1>
    <p>A detailed interactive learning note for the Analytic Hierarchy Process: pairwise comparison, Saaty scale, priority vector, consistency ratio, local priorities, global priorities, final ranking, sensitivity analysis, viva preparation, and self-assessment quiz.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(criteria)}</div><div class='small'>Criteria</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(alternatives)}</div><div class='small'>Alternatives</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='big'>{criteria_cr:.3f}</div><div class='small'>Criteria CR • {criteria_status}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='big'>{best_alt}</div><div class='small'>Best Alternative • {best_score:.4f}</div></div>", unsafe_allow_html=True)

# =========================================================
# 1. CONCEPT OVERVIEW
# =========================================================
st.markdown("""
<div class="card">
<h2>1. Concept Overview</h2>
<p><b>AHP</b> stands for <b>Analytic Hierarchy Process</b>. It is a structured MCDM method that converts human judgement into numerical priority weights. Instead of asking the decision maker to give direct weights such as 0.30, 0.25, and 0.15, AHP asks a more natural question:</p>
<p><b>Between two criteria, which one is more important, and how strongly?</b></p>
<p>This makes AHP powerful for decision problems where expert judgement is important. It is especially useful when criteria are qualitative, subjective, or difficult to measure directly.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<h3>Why AHP is different from SAW and TOPSIS</h3>
<p>SAW and TOPSIS usually require weights before ranking can be calculated. AHP can be used to <b>derive the weights</b> through pairwise comparison. AHP can also rank alternatives by comparing the alternatives under every criterion.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 2. CASE STUDY
# =========================================================
st.markdown("## 2. Real Case Study")
st.markdown("""
<div class="card">
<h3>Digital Learning Platform Selection</h3>
<p>A university wants to choose the best digital learning platform. Four platforms are evaluated using five criteria:</p>
<ol>
<li><b>Cost</b> — affordability and subscription burden.</li>
<li><b>Usability</b> — ease of use for lecturers and students.</li>
<li><b>Security</b> — data protection, access control, and platform reliability.</li>
<li><b>Features</b> — tools such as analytics, quizzes, grading, and integration.</li>
<li><b>Support</b> — technical response quality and helpdesk availability.</li>
</ol>
<p>The goal is not only to choose a platform, but also to show how expert judgement can be checked using the Consistency Ratio.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 3. AHP HIERARCHY
# =========================================================
st.markdown("## 3. AHP Hierarchy Structure")
st.markdown("""
<div class="note">
<p>AHP normally has three levels: <b>Goal</b>, <b>Criteria</b>, and <b>Alternatives</b>. The hierarchy helps the decision maker break a complex problem into smaller pairwise comparisons.</p>
</div>
""", unsafe_allow_html=True)

fig_hier = go.Figure()
# positions
nodes = {
    "Goal: Select Best Platform": (0.5, 0.95),
    "Cost": (0.10, 0.62), "Usability": (0.30, 0.62), "Security": (0.50, 0.62), "Features": (0.70, 0.62), "Support": (0.90, 0.62),
    "Platform A": (0.20, 0.23), "Platform B": (0.40, 0.23), "Platform C": (0.60, 0.23), "Platform D": (0.80, 0.23)
}
for crit in criteria:
    x0, y0 = nodes["Goal: Select Best Platform"]
    x1, y1 = nodes[crit]
    fig_hier.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(width=2, color="#93C5FD"), showlegend=False))
for crit in criteria:
    for alt in alternatives:
        x0, y0 = nodes[crit]
        x1, y1 = nodes[alt]
        fig_hier.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(width=1, color="rgba(37,99,235,0.18)"), showlegend=False))
for label, (x, y) in nodes.items():
    color = "#07182F" if "Goal" in label else ("#123B73" if label in criteria else "#2563EB")
    size = 34 if "Goal" in label else 24
    fig_hier.add_trace(go.Scatter(
        x=[x], y=[y], mode="markers+text", text=[label], textposition="middle center",
        marker=dict(size=size, color=color, line=dict(width=2, color="white")),
        textfont=dict(color="white", size=11), showlegend=False
    ))
fig_hier.update_layout(height=520, xaxis=dict(visible=False), yaxis=dict(visible=False))
fig_hier = plotly_blue_layout(fig_hier, "AHP Goal–Criteria–Alternatives Hierarchy")
st.plotly_chart(fig_hier, use_container_width=True)

# =========================================================
# 4. SAATY SCALE
# =========================================================
st.markdown("## 4. Saaty Pairwise Comparison Scale")
st.markdown("""
<div class="card">
<p>The Saaty scale is used to express the relative importance between two elements. A value of 1 means equal importance. A value of 9 means extreme importance of the row element over the column element. The reciprocal value is used when the column element is more important than the row element.</p>
</div>
""", unsafe_allow_html=True)

saaty_df = pd.DataFrame({
    "Scale": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Meaning": [
        "Equal importance",
        "Weak or slight importance",
        "Moderate importance",
        "Moderate plus importance",
        "Strong importance",
        "Strong plus importance",
        "Very strong importance",
        "Very, very strong importance",
        "Extreme importance"
    ],
    "Classroom Interpretation": [
        "Both elements contribute equally.",
        "One element is only slightly preferred.",
        "Experience slightly favours one over another.",
        "Between moderate and strong judgement.",
        "One element is clearly more important.",
        "Between strong and very strong judgement.",
        "One element is strongly dominant.",
        "Almost extreme dominance.",
        "Highest possible dominance in the scale."
    ]
})
st.dataframe(saaty_df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="gold-note">
<h3>Important Reciprocal Rule</h3>
<p>If criterion A is 5 times more important than criterion B, then criterion B must be 1/5 as important as criterion A. This reciprocal structure is compulsory in AHP.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"a_{ij}=\frac{1}{a_{ji}}, \qquad a_{ii}=1")

# =========================================================
# 5. MATHEMATICAL FOUNDATION
# =========================================================
st.markdown("## 5. Mathematical Foundation")
st.markdown("""
<div class="card">
<h3>Pairwise Comparison Matrix</h3>
<p>The pairwise matrix compares criteria or alternatives two at a time. Each element <b>a<sub>ij</sub></b> represents how strongly element <b>i</b> is preferred over element <b>j</b>.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"A = [a_{ij}]_{n \times n}")
st.latex(r"a_{ij} > 0, \qquad a_{ij}=\frac{1}{a_{ji}}, \qquad a_{ii}=1")

st.markdown("""
<div class="card">
<h3>Column Normalization</h3>
<p>Each value is divided by its column total. This converts the pairwise matrix into a normalized matrix.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\bar{a}_{ij}=\frac{a_{ij}}{\sum_{i=1}^{n}a_{ij}}")

st.markdown("""
<div class="card">
<h3>Priority Vector</h3>
<p>The priority weight is obtained by averaging each row of the normalized matrix.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"w_i=\frac{1}{n}\sum_{j=1}^{n}\bar{a}_{ij}")
st.latex(r"\sum_{i=1}^{n}w_i=1")

st.markdown("""
<div class="card">
<h3>Consistency Measurement</h3>
<p>AHP does not only calculate weights. It also checks whether the pairwise judgements are logically consistent.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\lambda_{max}=\frac{1}{n}\sum_{i=1}^{n}\frac{(Aw)_i}{w_i}")
st.latex(r"CI=\frac{\lambda_{max}-n}{n-1}")
st.latex(r"CR=\frac{CI}{RI}")

# =========================================================
# 6. CRITERIA PAIRWISE MATRIX
# =========================================================
st.markdown("## 6. Criteria Pairwise Matrix")
st.markdown("""
<div class="note">
<p>This matrix compares the five criteria. For example, if the value in row <b>Security</b> and column <b>Support</b> is 5, it means Security is judged to be strongly more important than Support.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(criteria_matrix.round(4), use_container_width=True)

fig_crit_heat = px.imshow(criteria_matrix, text_auto=".2f", color_continuous_scale=BLUE_SCALE, aspect="auto")
fig_crit_heat.update_layout(height=520, coloraxis_colorbar=dict(title="Judgement"))
fig_crit_heat = plotly_blue_layout(fig_crit_heat, "Criteria Pairwise Comparison Heatmap")
st.plotly_chart(fig_crit_heat, use_container_width=True)

# =========================================================
# 7. COLUMN NORMALIZATION
# =========================================================
st.markdown("## 7. Criteria Matrix Normalization")
st.markdown("""
<div class="card">
<p>To obtain the priority vector, each column is normalized. The sum of every normalized column becomes 1. The row average then becomes the criterion weight.</p>
</div>
""", unsafe_allow_html=True)

col_sum_df = pd.DataFrame({"Criterion": criteria_matrix.columns, "Column Sum": criteria_matrix.sum(axis=0).values})
st.markdown("### 7.1 Column Sums")
st.dataframe(col_sum_df.round(4), use_container_width=True, hide_index=True)

st.markdown("### 7.2 Normalized Criteria Matrix")
st.dataframe(criteria_norm.round(4), use_container_width=True)

st.markdown("""
<div class="step-card">
<b>Manual Example:</b> If the Cost column total is known, every value in the Cost column is divided by that total. This is repeated for all columns before averaging each row.
</div>
""", unsafe_allow_html=True)
st.latex(r"\bar{a}_{Cost,Usability}=\frac{a_{Cost,Usability}}{\sum_i a_{i,Usability}}")

# =========================================================
# 8. CRITERIA PRIORITY VECTOR
# =========================================================
st.markdown("## 8. Criteria Priority Vector")
criteria_weight_df = criteria_weights.sort_values(ascending=False).reset_index()
criteria_weight_df.columns = ["Criterion", "Priority Weight"]
st.dataframe(criteria_weight_df.round(4), use_container_width=True, hide_index=True)

fig_weights = px.bar(criteria_weight_df.sort_values("Priority Weight"), x="Priority Weight", y="Criterion", orientation="h", text="Priority Weight", color="Priority Weight", color_continuous_scale=BLUE_SCALE)
fig_weights.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_weights.update_layout(height=430, coloraxis_showscale=False, xaxis_title="Criteria Weight", yaxis_title="")
fig_weights = plotly_blue_layout(fig_weights, "Derived Criteria Weights from AHP")
st.plotly_chart(fig_weights, use_container_width=True)

# =========================================================
# 9. CONSISTENCY RATIO
# =========================================================
st.markdown("## 9. Consistency Ratio for Criteria Matrix")
st.markdown("""
<div class="card">
<p>Consistency Ratio is one of the strongest features of AHP. It checks whether the pairwise judgements are reasonable. In many applications, <b>CR ≤ 0.10</b> is considered acceptable.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='metric-card'><div class='big'>{criteria_lambda:.4f}</div><div class='small'>lambda max</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='big'>{criteria_ci:.4f}</div><div class='small'>Consistency Index</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><div class='big'>{RI_TABLE[len(criteria)]:.2f}</div><div class='small'>Random Index</div></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='metric-card'><div class='big'>{criteria_cr:.4f}</div><div class='small'>Consistency Ratio</div></div>", unsafe_allow_html=True)

if criteria_cr <= 0.10:
    st.markdown(f"""
    <div class="success-note">
    <h3>{criteria_status}</h3>
    <p>{criteria_message}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="warning-note">
    <h3>{criteria_status}</h3>
    <p>{criteria_message}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 9.1 Consistency Vector")
st.dataframe(criteria_consistency.round(4), use_container_width=True)

# =========================================================
# 10. ALTERNATIVE PAIRWISE COMPARISONS
# =========================================================
st.markdown("## 10. Alternative Pairwise Comparisons Under Each Criterion")
st.markdown("""
<div class="note">
<p>After criteria weights are obtained, AHP compares the alternatives under each criterion. This produces a <b>local priority vector</b> for each criterion.</p>
</div>
""", unsafe_allow_html=True)

for criterion in criteria:
    st.markdown(f"### 10.{criteria.index(criterion)+1} Alternatives Under {criterion}")
    colA, colB = st.columns([1.1, 1])
    with colA:
        st.markdown(f"<div class='card'><h3>Pairwise Matrix: {criterion}</h3><p>The values show preference strength between platforms when only <b>{criterion}</b> is considered.</p></div>", unsafe_allow_html=True)
        st.dataframe(alternative_matrices[criterion].round(4), use_container_width=True)
    with colB:
        local_df = alternative_weights[criterion].sort_values(ascending=False).reset_index()
        local_df.columns = ["Alternative", "Local Priority"]
        fig_local = px.bar(local_df.sort_values("Local Priority"), x="Local Priority", y="Alternative", orientation="h", text="Local Priority", color="Local Priority", color_continuous_scale=BLUE_SCALE)
        fig_local.update_traces(texttemplate="%{text:.4f}", textposition="outside")
        fig_local.update_layout(height=360, coloraxis_showscale=False, xaxis_title="Local Priority", yaxis_title="")
        fig_local = plotly_blue_layout(fig_local, f"Local Priority under {criterion}")
        st.plotly_chart(fig_local, use_container_width=True)
    st.markdown(f"#### Normalized Matrix for {criterion}")
    st.dataframe(alternative_norms[criterion].round(4), use_container_width=True)

# =========================================================
# 11. LOCAL PRIORITY MATRIX
# =========================================================
st.markdown("## 11. Local Priority Matrix")
st.markdown("""
<div class="card">
<p>The local priority matrix combines all alternative priority vectors. Each column shows how the alternatives perform under one criterion.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(local_priority_matrix.round(4), use_container_width=True)

fig_local_heat = px.imshow(local_priority_matrix, text_auto=".3f", color_continuous_scale=BLUE_SCALE, aspect="auto")
fig_local_heat.update_layout(height=500, coloraxis_colorbar=dict(title="Local Priority"))
fig_local_heat = plotly_blue_layout(fig_local_heat, "Local Priority Heatmap")
st.plotly_chart(fig_local_heat, use_container_width=True)

# =========================================================
# 12. GLOBAL PRIORITY CALCULATION
# =========================================================
st.markdown("## 12. Global Priority Calculation")
st.markdown("""
<div class="card">
<p>The global priority is obtained by multiplying each local priority by the corresponding criterion weight. Then all weighted local priorities are summed for each alternative.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"GlobalPriority_{ij}=LocalPriority_{ij}\times w_j")
st.latex(r"FinalPriority_i=\sum_{j=1}^{n}LocalPriority_{ij}w_j")

st.markdown("### 12.1 Weighted Global Priority Matrix")
st.dataframe(global_priority.round(4), use_container_width=True)

st.markdown("### 12.2 Final AHP Ranking")
st.dataframe(final_result.round(4), use_container_width=True, hide_index=True)

fig_final = px.bar(final_result.sort_values("AHP Final Priority"), x="AHP Final Priority", y="Alternative", orientation="h", text="AHP Final Priority", color="AHP Final Priority", color_continuous_scale=BLUE_SCALE)
fig_final.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_final.update_layout(height=440, coloraxis_showscale=False, xaxis_title="Final Priority", yaxis_title="")
fig_final = plotly_blue_layout(fig_final, "Final AHP Ranking")
st.plotly_chart(fig_final, use_container_width=True)

st.markdown(f"""
<div class="success-note">
<h3>Ranking Interpretation</h3>
<p>The best alternative is <b>{best_alt}</b> with a final AHP priority of <b>{best_score:.4f}</b>. This means it receives the highest overall priority after considering criteria weights and local alternative priorities.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 13. CONTRIBUTION BREAKDOWN
# =========================================================
st.markdown("## 13. Contribution Breakdown by Criterion")
st.markdown("""
<div class="note">
<p>This chart shows where the final score comes from. It is useful for explaining why an alternative wins.</p>
</div>
""", unsafe_allow_html=True)

contrib_df = global_priority.reset_index().melt(id_vars="index", var_name="Criterion", value_name="Contribution")
contrib_df.rename(columns={"index": "Alternative"}, inplace=True)
fig_stack = px.bar(contrib_df, x="Alternative", y="Contribution", color="Criterion", text="Contribution", color_discrete_sequence=BLUE_DISCRETE)
fig_stack.update_traces(texttemplate="%{text:.3f}", textposition="inside")
fig_stack.update_layout(height=500, xaxis_title="Alternative", yaxis_title="Weighted Contribution")
fig_stack = plotly_blue_layout(fig_stack, "Weighted Contribution of Each Criterion")
st.plotly_chart(fig_stack, use_container_width=True)

# =========================================================
# 14. CONSISTENCY SUMMARY FOR ALL MATRICES
# =========================================================
st.markdown("## 14. Consistency Summary for All Pairwise Matrices")
st.markdown("""
<div class="card">
<p>AHP requires consistency checking not only for the criteria matrix, but also for alternative matrices under each criterion.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(summary_df.round(4), use_container_width=True, hide_index=True)

fig_cr = px.bar(summary_df, x="Matrix", y="CR", text="CR", color="CR", color_continuous_scale=BLUE_SCALE)
fig_cr.add_hline(y=0.10, line_dash="dash", line_color="#EA580C", annotation_text="Recommended threshold CR = 0.10")
fig_cr.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_cr.update_layout(height=500, coloraxis_showscale=False, xaxis_title="", yaxis_title="Consistency Ratio")
fig_cr = plotly_blue_layout(fig_cr, "Consistency Ratio Across AHP Matrices")
st.plotly_chart(fig_cr, use_container_width=True)

# =========================================================
# 15. SENSITIVITY ANALYSIS
# =========================================================
st.markdown("## 15. Sensitivity Analysis")
st.markdown("""
<div class="card">
<p>In AHP, sensitivity analysis is used to see whether the final ranking changes when criterion weights are adjusted. This helps determine whether the decision is robust.</p>
</div>
""", unsafe_allow_html=True)

scenario_weights = {
    "Original AHP Weights": criteria_weights,
    "Cost Priority Scenario": pd.Series({"Cost": 0.35, "Usability": 0.20, "Security": 0.20, "Features": 0.15, "Support": 0.10}),
    "Security Priority Scenario": pd.Series({"Cost": 0.15, "Usability": 0.20, "Security": 0.40, "Features": 0.15, "Support": 0.10}),
    "User Experience Scenario": pd.Series({"Cost": 0.15, "Usability": 0.40, "Security": 0.20, "Features": 0.15, "Support": 0.10}),
    "Feature Innovation Scenario": pd.Series({"Cost": 0.15, "Usability": 0.20, "Security": 0.20, "Features": 0.35, "Support": 0.10}),
}

sens_rows = []
rank_rows = []
for scenario, w in scenario_weights.items():
    w = w / w.sum()
    scores = local_priority_matrix.multiply(w, axis=1).sum(axis=1)
    temp = pd.DataFrame({"Alternative": scores.index, "Score": scores.values})
    temp["Rank"] = temp["Score"].rank(ascending=False, method="dense").astype(int)
    for _, row in temp.iterrows():
        sens_rows.append({"Scenario": scenario, "Alternative": row["Alternative"], "AHP Score": row["Score"]})
        rank_rows.append({"Scenario": scenario, "Alternative": row["Alternative"], "Rank": row["Rank"]})

sensitivity_df = pd.DataFrame(sens_rows)
sensitivity_rank_df = pd.DataFrame(rank_rows)
st.markdown("### 15.1 Scenario Meaning")
scenario_explain = pd.DataFrame({
    "Scenario": list(scenario_weights.keys()),
    "Meaning": [
        "Uses the original weights derived from the AHP pairwise criteria matrix.",
        "Tests what happens if affordability becomes the main priority.",
        "Tests what happens if platform security becomes the main priority.",
        "Tests what happens if usability and user friendliness become the main priority.",
        "Tests what happens if digital features and innovation become the main priority."
    ]
})
st.dataframe(scenario_explain, use_container_width=True, hide_index=True)

st.markdown("### 15.2 Sensitivity Score Table")
st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="AHP Score").round(4), use_container_width=True)

fig_sens = px.line(sensitivity_df, x="Scenario", y="AHP Score", color="Alternative", markers=True, color_discrete_sequence=BLUE_DISCRETE)
fig_sens.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens.update_layout(height=520, xaxis_title="Scenario", yaxis_title="AHP Score")
fig_sens = plotly_blue_layout(fig_sens, "AHP Score Across Weight Scenarios")
st.plotly_chart(fig_sens, use_container_width=True)

fig_sens_rank = px.line(sensitivity_rank_df, x="Scenario", y="Rank", color="Alternative", markers=True, color_discrete_sequence=BLUE_DISCRETE)
fig_sens_rank.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens_rank.update_yaxes(autorange="reversed", dtick=1)
fig_sens_rank.update_layout(height=520, xaxis_title="Scenario", yaxis_title="Rank")
fig_sens_rank = plotly_blue_layout(fig_sens_rank, "Ranking Stability Across AHP Scenarios")
st.plotly_chart(fig_sens_rank, use_container_width=True)

# =========================================================
# 16. INTERACTIVE WEIGHT EXPLORER
# =========================================================
st.markdown("## 16. Interactive Weight Explorer")
st.markdown("""
<div class="note">
<p>This section allows students to manually change criteria weights and observe whether the AHP ranking changes. The weights are automatically normalized to sum to 1.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Open Interactive Weight Explorer"):
    sliders = {}
    cols = st.columns(len(criteria))
    for idx, criterion in enumerate(criteria):
        with cols[idx]:
            sliders[criterion] = st.slider(f"{criterion}", 0.01, 0.70, float(criteria_weights[criterion]), 0.01)
    slider_weights = pd.Series(sliders)
    slider_weights = slider_weights / slider_weights.sum()
    interactive_scores = local_priority_matrix.multiply(slider_weights, axis=1).sum(axis=1)
    interactive_result = pd.DataFrame({"Alternative": interactive_scores.index, "Interactive Score": interactive_scores.values})
    interactive_result["Rank"] = interactive_result["Interactive Score"].rank(ascending=False, method="dense").astype(int)
    interactive_result = interactive_result.sort_values("Rank")
    st.markdown("### Normalized Interactive Weights")
    st.dataframe(slider_weights.to_frame("Normalized Weight").round(4), use_container_width=True)
    st.markdown("### Interactive Ranking Result")
    st.dataframe(interactive_result.round(4), use_container_width=True, hide_index=True)
    fig_interactive = px.bar(interactive_result.sort_values("Interactive Score"), x="Interactive Score", y="Alternative", orientation="h", text="Interactive Score", color="Interactive Score", color_continuous_scale=BLUE_SCALE)
    fig_interactive.update_traces(texttemplate="%{text:.4f}", textposition="outside")
    fig_interactive.update_layout(height=420, coloraxis_showscale=False)
    fig_interactive = plotly_blue_layout(fig_interactive, "Interactive AHP Ranking")
    st.plotly_chart(fig_interactive, use_container_width=True)

# =========================================================
# 17. COMPARISON WITH OTHER METHODS
# =========================================================
st.markdown("## 17. Comparison with SAW and TOPSIS")
comparison_df = pd.DataFrame({
    "Aspect": ["Main role", "Input style", "Weight generation", "Consistency check", "Ranking logic", "Best use case"],
    "SAW": ["Ranking", "Original performance data", "Needs predefined weights", "No", "Weighted summation", "Simple transparent scoring"],
    "TOPSIS": ["Ranking", "Original performance data", "Needs predefined weights", "No", "Closest to ideal and farthest from worst", "Distance-based ranking"],
    "AHP": ["Weighting and ranking", "Pairwise judgement", "Can derive weights", "Yes, through CR", "Priority synthesis", "Expert judgement and qualitative criteria"]
})
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# =========================================================
# 18. COMMON MISTAKES
# =========================================================
st.markdown("## 18. Common Mistakes in AHP")
st.markdown("""
<div class="card">
<ol>
<li>Using direct weights without explaining how pairwise comparison was conducted.</li>
<li>Ignoring the reciprocal rule in the pairwise matrix.</li>
<li>Accepting a matrix with high Consistency Ratio without revision.</li>
<li>Using too many criteria, which makes pairwise judgement tiring and inconsistent.</li>
<li>Mixing benefit and cost thinking incorrectly when comparing alternatives.</li>
<li>Assuming AHP is fully objective; AHP still depends on expert judgement.</li>
<li>Reporting final ranking without showing criteria weights.</li>
<li>Reporting weights without showing CR, CI, and RI.</li>
<li>Not explaining the Saaty scale to respondents or experts.</li>
<li>Using average scores from questionnaires as if they were pairwise comparison values.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 19. VIVA / PANEL QUESTIONS
# =========================================================
st.markdown("## 19. Viva and Panel Preparation")
st.markdown("""
<div class="dark-note">
<h3>Question 1: Why use AHP?</h3>
<p>AHP is suitable because the problem involves multiple criteria and expert judgement. It helps transform qualitative comparison into numerical weights and checks judgement consistency using the Consistency Ratio.</p>
</div>
<div class="dark-note">
<h3>Question 2: What does Consistency Ratio mean?</h3>
<p>Consistency Ratio measures whether the pairwise judgements are logically consistent. A CR below or equal to 0.10 is commonly considered acceptable.</p>
</div>
<div class="dark-note">
<h3>Question 3: Is AHP subjective?</h3>
<p>Yes, AHP is judgement-based. However, it improves subjective judgement by using a structured pairwise process and consistency checking.</p>
</div>
<div class="dark-note">
<h3>Question 4: Why not just use SAW?</h3>
<p>SAW needs predefined weights. AHP is useful when the researcher wants to derive weights from expert pairwise judgement before ranking alternatives.</p>
</div>
<div class="dark-note">
<h3>Question 5: What happens if CR is high?</h3>
<p>The decision maker should review the pairwise comparisons because the judgements may contradict each other. The final weights should not be accepted blindly.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 20. DOWNLOAD
# =========================================================
st.markdown("## 20. Download Worked Example")
excel_bytes = to_excel_bytes(
    criteria_matrix, criteria_norm, criteria_weights, criteria_consistency,
    alternative_matrices, alternative_norms, alternative_weights,
    global_priority, final_result, sensitivity_df, summary_df
)
st.download_button(
    label="Download AHP Worked Example Excel",
    data=excel_bytes,
    file_name="AHP_Method_Worked_Example.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# 21. QUIZ
# =========================================================
st.markdown("## 21. Self-Assessment Quiz")
st.markdown("""
<div class="note">
<p>This quiz contains exactly <b>10 questions</b>: 5 True/False and 5 Multiple Choice questions.</p>
</div>
""", unsafe_allow_html=True)

tf_questions = [
    {"question": "AHP uses pairwise comparison to derive priorities.", "answer": "True"},
    {"question": "The diagonal values in an AHP pairwise matrix should be 0.", "answer": "False"},
    {"question": "The reciprocal rule means aij = 1 / aji.", "answer": "True"},
    {"question": "AHP does not have any consistency checking mechanism.", "answer": "False"},
    {"question": "AHP can be used to derive criteria weights from expert judgement.", "answer": "True"},
]

mcq_questions = [
    {"question": "What does AHP stand for?", "options": ["Analytic Hierarchy Process", "Alternative Hybrid Procedure", "Analytical Highest Priority", "Automated Hierarchy Plot"], "answer": "Analytic Hierarchy Process"},
    {"question": "Which scale is commonly used in AHP pairwise comparison?", "options": ["Saaty 1–9 scale", "Binary 0–1 scale", "Likert 1–5 only", "Percentage scale only"], "answer": "Saaty 1–9 scale"},
    {"question": "What is the usual acceptable CR threshold?", "options": ["0.10", "0.50", "1.00", "10.00"], "answer": "0.10"},
    {"question": "What does CI stand for in AHP?", "options": ["Consistency Index", "Criteria Interval", "Comparison Indicator", "Central Importance"], "answer": "Consistency Index"},
    {"question": "What should be done if CR is too high?", "options": ["Revise pairwise judgements", "Ignore the matrix", "Delete all alternatives", "Set all weights to zero"], "answer": "Revise pairwise judgements"},
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
            st.success("Excellent. You understand AHP pairwise comparison and consistency checking.")
        elif percentage >= 70:
            st.info("Good. Review the consistency ratio and priority vector calculation.")
        else:
            st.warning("Please revisit the worked calculation before moving to another method.")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)

# =========================================================
# 22. FINAL SUMMARY
# =========================================================
st.markdown("""
<hr>
<div class="card">
<h2>Final Summary</h2>
<p>AHP is more than a ranking method. It is a structured decision-making framework that builds a hierarchy, compares criteria and alternatives in pairs, derives priority weights, checks consistency, and synthesizes local priorities into a final ranking.</p>
<p>The most important parts to defend are the pairwise comparison logic, the Saaty scale, the reciprocal matrix, the priority vector, and the Consistency Ratio.</p>
</div>
""", unsafe_allow_html=True)
