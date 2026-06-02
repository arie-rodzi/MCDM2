import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="TOPSIS Method", page_icon="❤️", layout="wide")

# =========================================================
# PREMIUM RED THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(190, 49, 68, 0.22), transparent 34%),
        radial-gradient(circle at bottom right, rgba(120, 18, 32, 0.16), transparent 30%),
        linear-gradient(135deg, #FFF6F4 0%, #F8E7E4 44%, #F2D7D5 100%);
}
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1280px;}

.hero {
    padding: 36px 36px 32px 36px;
    border-radius: 30px;
    background: linear-gradient(135deg, #3B0A12 0%, #7A1F2B 52%, #C94C5C 100%);
    color: white;
    box-shadow: 0 24px 62px rgba(122, 31, 43, 0.30);
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
    left: -80px;
    bottom: -90px;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
}
.hero h1 {font-size: 50px; line-height: 1.05; margin: 0; font-weight: 900; letter-spacing: -1.3px;}
.hero p {font-size: 18px; color: #FFE6E3; margin-top: 12px; max-width: 900px;}
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
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(158, 48, 61, 0.18);
    border-radius: 24px;
    padding: 26px;
    margin: 18px 0;
    box-shadow: 0 14px 38px rgba(92, 24, 34, 0.10);
}
.card h2, .card h3 {color: #5B1420;}
.note {
    background: linear-gradient(135deg, #FFF8F7, #FBE6E3);
    border-left: 7px solid #B53345;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3D1D22;
}
.dark-note {
    background: linear-gradient(135deg, #53111C, #7A1F2B);
    border-left: 7px solid #F0B6B9;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #FFF5F3;
}
.gold-note {
    background: linear-gradient(135deg, #FFF6DE, #F4DFA4);
    border-left: 7px solid #B88928;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3C2E17;
}
.success-note {
    background: linear-gradient(135deg, #F6FFF8, #DFF3E6);
    border-left: 7px solid #2D7A4B;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #173C2D;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF, #FBEAE8);
    border: 1px solid rgba(158,48,61,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(92, 24, 34, 0.09);
    text-align: center;
}
.metric-card .big {font-size: 32px; font-weight: 900; color: #5B1420;}
.metric-card .small {font-size: 14px; color: #7A5054; font-weight: 800;}
.quiz-box {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(158,48,61,0.18);
    box-shadow: 0 10px 25px rgba(92, 24, 34, 0.06);
    margin: 16px 0 8px 0;
}
.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7A1F2B, #C94C5C);
    color: white;
    border-radius: 999px;
    padding: 7px 13px;
    font-weight: 900;
    font-size: 13px;
    margin-bottom: 8px;
}
[data-testid="stDataFrame"] {border-radius: 18px; overflow: hidden;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7A1F2B, #C94C5C) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.1rem !important;
    font-weight: 900 !important;
}
hr {border: none; height: 1px; background: rgba(158,48,61,0.22); margin: 26px 0;}
</style>
""", unsafe_allow_html=True)

RED_SCALE = ["#F9D8D6", "#F1A7A8", "#D65C6B", "#B53345", "#7A1F2B", "#3B0A12"]
RED_DISCRETE = ["#3B0A12", "#7A1F2B", "#B53345", "#D65C6B", "#B88928", "#2D7A4B"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def topsis_calculation(df, criteria_types, weights):
    matrix = df.set_index("Alternative").astype(float)
    weight_series = pd.Series(weights).astype(float)
    weight_series = weight_series / weight_series.sum()

    denominator = np.sqrt((matrix ** 2).sum(axis=0))
    denominator = denominator.replace(0, np.nan)
    normalized = matrix / denominator
    normalized = normalized.replace([np.inf, -np.inf], np.nan).fillna(0)

    weighted = normalized * weight_series

    pis = {}
    nis = {}
    for c in matrix.columns:
        if criteria_types[c] == "Benefit":
            pis[c] = weighted[c].max()
            nis[c] = weighted[c].min()
        else:
            pis[c] = weighted[c].min()
            nis[c] = weighted[c].max()

    pis_series = pd.Series(pis, name="Positive Ideal Solution")
    nis_series = pd.Series(nis, name="Negative Ideal Solution")

    d_plus = np.sqrt(((weighted - pis_series) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted - nis_series) ** 2).sum(axis=1))
    closeness = d_minus / (d_plus + d_minus).replace(0, np.nan)
    closeness = closeness.fillna(0)

    result = pd.DataFrame({
        "Alternative": closeness.index,
        "D+ Distance to Ideal": d_plus.values,
        "D- Distance from Worst": d_minus.values,
        "Closeness Coefficient": closeness.values,
    })
    result["Rank"] = result["Closeness Coefficient"].rank(ascending=False, method="dense").astype(int)
    result = result.sort_values("Rank")
    return normalized, weighted, pis_series, nis_series, result


def to_excel_bytes(original, normalized, weighted, ideal_df, distance_result, sensitivity_df=None, rank_df=None):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        original.to_excel(writer, sheet_name="Original Data", index=False)
        normalized.to_excel(writer, sheet_name="Vector Normalized Matrix")
        weighted.to_excel(writer, sheet_name="Weighted Normalized Matrix")
        ideal_df.to_excel(writer, sheet_name="Ideal Solutions")
        distance_result.to_excel(writer, sheet_name="TOPSIS Result", index=False)
        if sensitivity_df is not None:
            sensitivity_df.to_excel(writer, sheet_name="Sensitivity Scores", index=False)
        if rank_df is not None:
            rank_df.to_excel(writer, sheet_name="Sensitivity Ranks", index=False)
    return output.getvalue()


def plotly_red_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#5B1420")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.62)",
        font=dict(color="#3D1D22"),
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0.70)", bordercolor="rgba(158,48,61,0.20)", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="rgba(158,48,61,0.13)", zerolinecolor="rgba(158,48,61,0.2)")
    fig.update_yaxes(gridcolor="rgba(158,48,61,0.13)", zerolinecolor="rgba(158,48,61,0.2)")
    return fig


def scenario_explanation_table():
    return pd.DataFrame({
        "Scenario": [
            "Balanced Decision",
            "Cost-Control Decision",
            "User Experience Decision",
            "Innovation Decision",
            "Fast Support Decision",
        ],
        "Meaning": [
            "All criteria follow the original balanced weight structure.",
            "Decision maker gives stronger priority to lower cost.",
            "Decision maker gives stronger priority to usability and user acceptance.",
            "Decision maker gives stronger priority to available platform features.",
            "Decision maker gives stronger priority to quick technical support.",
        ],
        "Learning Purpose": [
            "Baseline result for comparison.",
            "Shows what happens if budget pressure becomes dominant.",
            "Shows what happens if the system must be easy for users.",
            "Shows what happens if advanced functions are more important.",
            "Shows what happens if service response is critical.",
        ]
    })

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="pill">MCDM Learning Module • Premium Red Edition</div>
    <h1>TOPSIS Method</h1>
    <p>A detailed interactive note on ranking alternatives using distance from the positive ideal solution and negative ideal solution, complete with real mathematical equations, manual calculations, visual interpretation, sensitivity analysis, downloadable Excel output, and a self-assessment quiz.</p>
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
normalized, weighted, pis, nis, result = topsis_calculation(default_df, criteria_types, weights)
ideal_df = pd.DataFrame([pis, nis])
best_alt = result.iloc[0]["Alternative"]
best_score = result.iloc[0]["Closeness Coefficient"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(default_df)}</div><div class='small'>Alternatives</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(weights)}</div><div class='small'>Criteria</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='big'>{best_alt}</div><div class='small'>Best Alternative</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='big'>{best_score:.4f}</div><div class='small'>Best Closeness</div></div>", unsafe_allow_html=True)

# =========================================================
# INTRODUCTION
# =========================================================
st.markdown("""
<div class="card">
<h2>1. Concept Overview</h2>
<p><b>TOPSIS</b> stands for <b>Technique for Order Preference by Similarity to Ideal Solution</b>. The main idea is very intuitive: the best alternative should be <b>closest to the ideal solution</b> and <b>farthest from the worst solution</b>.</p>
<p>Unlike a simple weighted-sum approach, TOPSIS compares every alternative against two reference points. The first reference point is the <b>Positive Ideal Solution</b>, which represents the best possible performance. The second reference point is the <b>Negative Ideal Solution</b>, which represents the worst possible performance.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<h3>Real Case Study</h3>
<p>A university wants to select the most suitable digital learning platform. Four platforms are assessed using annual cost, usability, number of features, and support response time. TOPSIS is useful here because the decision maker does not only want a high weighted score; they want the platform that is nearest to the ideal profile and farthest from the weakest profile.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dark-note">
<h3>Why TOPSIS is More Detailed Than SAW</h3>
<p>SAW ends after weighted summation. TOPSIS continues further by constructing ideal solutions, calculating distances, and computing a closeness coefficient. Because of that, TOPSIS usually provides richer interpretation for ranking problems.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ORIGINAL MATRIX
# =========================================================
st.markdown("## 2. Original Decision Matrix")
st.dataframe(default_df, use_container_width=True, hide_index=True)

criteria_df = pd.DataFrame({
    "Criterion": list(weights.keys()),
    "Type": [criteria_types[c] for c in weights.keys()],
    "Weight": [weights[c] for c in weights.keys()],
    "Decision Logic": ["Lower is better", "Higher is better", "Higher is better", "Lower is better"]
})
st.markdown("## 3. Criteria Type and Weight Structure")
st.dataframe(criteria_df, use_container_width=True, hide_index=True)

# =========================================================
# MATHEMATICAL FORMULATION
# =========================================================
st.markdown("""
<div class="card">
<h2>4. Mathematical Foundation</h2>
<p>TOPSIS begins with a decision matrix. Each value is denoted as <b>x<sub>ij</sub></b>, where alternative <b>i</b> is evaluated under criterion <b>j</b>.</p>
</div>
""", unsafe_allow_html=True)

st.latex(r"X=[x_{ij}]_{m \times n}")
st.latex(r"A_i = \text{alternative } i, \qquad C_j = \text{criterion } j")

st.markdown("""
<div class="note">
<h3>Step 1: Vector Normalization</h3>
<p>TOPSIS commonly uses vector normalization. This converts the original criteria into comparable scale values.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"r_{ij}=\frac{x_{ij}}{\sqrt{\sum_{i=1}^{m}x_{ij}^{2}}}")

st.markdown("""
<div class="note">
<h3>Step 2: Weighted Normalized Matrix</h3>
<p>Each normalized value is multiplied by its criterion weight.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"v_{ij}=w_j r_{ij}")
st.latex(r"\sum_{j=1}^{n}w_j=1")

left, right = st.columns(2)
with left:
    st.markdown("""
    <div class="success-note">
    <h3>Positive Ideal Solution</h3>
    <p>The best reference profile. For benefit criteria, it takes the maximum value. For cost criteria, it takes the minimum value.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"A^{+}=\{v_1^{+},v_2^{+},\ldots,v_n^{+}\}")
    st.latex(r"v_j^{+}=\max_i(v_{ij}) \quad \text{for benefit criteria}")
    st.latex(r"v_j^{+}=\min_i(v_{ij}) \quad \text{for cost criteria}")
with right:
    st.markdown("""
    <div class="gold-note">
    <h3>Negative Ideal Solution</h3>
    <p>The worst reference profile. For benefit criteria, it takes the minimum value. For cost criteria, it takes the maximum value.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"A^{-}=\{v_1^{-},v_2^{-},\ldots,v_n^{-}\}")
    st.latex(r"v_j^{-}=\min_i(v_{ij}) \quad \text{for benefit criteria}")
    st.latex(r"v_j^{-}=\max_i(v_{ij}) \quad \text{for cost criteria}")

st.markdown("""
<div class="card">
<h3>Distance and Closeness Coefficient</h3>
<p>The distance from each alternative to the positive ideal and negative ideal is calculated using Euclidean distance. The final TOPSIS score is called the closeness coefficient.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"D_i^{+}=\sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^{+})^2}")
st.latex(r"D_i^{-}=\sqrt{\sum_{j=1}^{n}(v_{ij}-v_j^{-})^2}")
st.latex(r"CC_i=\frac{D_i^{-}}{D_i^{+}+D_i^{-}}")

# =========================================================
# STEP BY STEP CALCULATION
# =========================================================
st.markdown("## 5. Step-by-Step Worked Calculation")

st.markdown("""
<div class="note">
<span class="step-badge">STEP 1</span>
<h3>Calculate the Vector Normalization Denominator</h3>
<p>For every criterion, square all values, sum them, and take the square root. This denominator is used to normalize the original values.</p>
</div>
""", unsafe_allow_html=True)

matrix = default_df.set_index("Alternative").astype(float)
denom = np.sqrt((matrix ** 2).sum(axis=0))
denom_df = pd.DataFrame({"Criterion": denom.index, "Vector Denominator": denom.values})
st.dataframe(denom_df.round(4), use_container_width=True, hide_index=True)

st.latex(r"\sqrt{12000^2+15000^2+10000^2+18000^2}=27640.5499")
st.latex(r"\sqrt{80^2+90^2+75^2+85^2}=165.5295")

st.markdown("""
<div class="note">
<span class="step-badge">STEP 2</span>
<h3>Normalize the Decision Matrix</h3>
<p>Every original value is divided by its vector denominator. For example, Platform A cost is divided by the cost denominator.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"r_{A,Cost}=\frac{12000}{27640.5499}=0.4341")
st.latex(r"r_{B,Usability}=\frac{90}{165.5295}=0.5437")
st.dataframe(normalized.round(4), use_container_width=True)

st.markdown("""
<div class="note">
<span class="step-badge">STEP 3</span>
<h3>Apply Criterion Weights</h3>
<p>The normalized matrix is multiplied by the weight vector. This creates the weighted normalized matrix.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"v_{A,Cost}=0.4341\times0.30=0.1302")
st.latex(r"v_{B,Usability}=0.5437\times0.30=0.1631")
st.dataframe(weighted.round(4), use_container_width=True)

st.markdown("""
<div class="note">
<span class="step-badge">STEP 4</span>
<h3>Identify Positive and Negative Ideal Solutions</h3>
<p>For benefit criteria, the positive ideal is the highest weighted value. For cost criteria, the positive ideal is the lowest weighted value.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(ideal_df.round(4), use_container_width=True)

st.markdown("""
<div class="note">
<span class="step-badge">STEP 5</span>
<h3>Calculate Distance to Ideal and Distance from Worst</h3>
<p>A strong alternative should have a small distance to the positive ideal and a large distance from the negative ideal.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"D_i^{+}=\sqrt{(v_{i1}-v_1^{+})^2+(v_{i2}-v_2^{+})^2+\cdots+(v_{in}-v_n^{+})^2}")
st.latex(r"D_i^{-}=\sqrt{(v_{i1}-v_1^{-})^2+(v_{i2}-v_2^{-})^2+\cdots+(v_{in}-v_n^{-})^2}")

st.markdown("""
<div class="note">
<span class="step-badge">STEP 6</span>
<h3>Calculate the Closeness Coefficient and Rank Alternatives</h3>
<p>The closeness coefficient ranges from 0 to 1. A higher value means the alternative is closer to the ideal solution.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"0 \leq CC_i \leq 1")
st.dataframe(result.round(4), use_container_width=True, hide_index=True)

# =========================================================
# VISUALIZATION
# =========================================================
st.markdown("## 6. Visual Interpretation")

fig_score = px.bar(
    result.sort_values("Closeness Coefficient", ascending=True),
    x="Closeness Coefficient",
    y="Alternative",
    orientation="h",
    text="Closeness Coefficient",
    color="Closeness Coefficient",
    color_continuous_scale=RED_SCALE,
)
fig_score.update_traces(texttemplate="%{text:.4f}", textposition="outside", marker_line_width=0)
fig_score.update_layout(height=450, showlegend=False, coloraxis_showscale=False, xaxis_title="Closeness Coefficient", yaxis_title="")
fig_score = plotly_red_layout(fig_score, "TOPSIS Final Ranking by Closeness Coefficient")
st.plotly_chart(fig_score, use_container_width=True)

fig_distance = go.Figure()
fig_distance.add_trace(go.Bar(x=result["Alternative"], y=result["D+ Distance to Ideal"], name="D+ Distance to Ideal", marker_color="#B53345"))
fig_distance.add_trace(go.Bar(x=result["Alternative"], y=result["D- Distance from Worst"], name="D- Distance from Worst", marker_color="#3B0A12"))
fig_distance.update_layout(barmode="group", height=480, xaxis_title="Alternative", yaxis_title="Distance")
fig_distance = plotly_red_layout(fig_distance, "Distance Comparison: Near to Ideal and Far from Worst")
st.plotly_chart(fig_distance, use_container_width=True)

st.markdown("""
<div class="success-note">
<h3>How to Read the Distance Graph</h3>
<p>The preferred alternative should have a <b>low D+</b> because it is near to the ideal solution, and a <b>high D−</b> because it is far from the worst solution. The closeness coefficient combines both distances into one final ranking value.</p>
</div>
""", unsafe_allow_html=True)

# Heatmap of weighted normalized matrix
st.markdown("## 7. Weighted Matrix Heatmap")
fig_heat = px.imshow(
    weighted.round(4),
    text_auto=True,
    aspect="auto",
    color_continuous_scale=RED_SCALE,
    title="Weighted Normalized Matrix Heatmap"
)
fig_heat.update_layout(height=460, coloraxis_colorbar=dict(title="Weighted Value"))
fig_heat = plotly_red_layout(fig_heat, "Weighted Normalized Matrix Heatmap")
st.plotly_chart(fig_heat, use_container_width=True)

# Ideal profile comparison
st.markdown("## 8. Ideal Solution Profile")
ideal_long = ideal_df.reset_index().rename(columns={"index": "Ideal Type"}).melt(id_vars="Ideal Type", var_name="Criterion", value_name="Weighted Value")
fig_ideal = px.line(
    ideal_long,
    x="Criterion",
    y="Weighted Value",
    color="Ideal Type",
    markers=True,
    color_discrete_sequence=["#2D7A4B", "#B53345"],
)
fig_ideal.update_traces(line=dict(width=4), marker=dict(size=11))
fig_ideal.update_layout(height=460, xaxis_title="Criterion", yaxis_title="Weighted Ideal Value")
fig_ideal = plotly_red_layout(fig_ideal, "Positive and Negative Ideal Solution Profiles")
st.plotly_chart(fig_ideal, use_container_width=True)

# =========================================================
# SENSITIVITY ANALYSIS
# =========================================================
st.markdown("## 9. Sensitivity Analysis")
st.markdown("""
<div class="card">
<p>Sensitivity analysis checks whether the final ranking remains stable when the weights are changed. In this learning module, the scenario names are written in plain decision language so students can understand the purpose of each scenario.</p>
</div>
""", unsafe_allow_html=True)

st.dataframe(scenario_explanation_table(), use_container_width=True, hide_index=True)

scenarios = {
    "Balanced Decision": {"Cost": 0.30, "Usability": 0.30, "Features": 0.25, "Support Time": 0.15},
    "Cost-Control Decision": {"Cost": 0.45, "Usability": 0.20, "Features": 0.20, "Support Time": 0.15},
    "User Experience Decision": {"Cost": 0.20, "Usability": 0.45, "Features": 0.20, "Support Time": 0.15},
    "Innovation Decision": {"Cost": 0.20, "Usability": 0.20, "Features": 0.45, "Support Time": 0.15},
    "Fast Support Decision": {"Cost": 0.20, "Usability": 0.25, "Features": 0.20, "Support Time": 0.35},
}

sensitivity_rows, rank_rows = [], []
for scenario_name, scenario_weights in scenarios.items():
    _, _, _, _, scenario_result = topsis_calculation(default_df, criteria_types, scenario_weights)
    for _, row in scenario_result.iterrows():
        sensitivity_rows.append({
            "Scenario": scenario_name,
            "Alternative": row["Alternative"],
            "Closeness Coefficient": row["Closeness Coefficient"],
        })
        rank_rows.append({
            "Scenario": scenario_name,
            "Alternative": row["Alternative"],
            "Rank": row["Rank"],
        })

sensitivity_df = pd.DataFrame(sensitivity_rows)
rank_df = pd.DataFrame(rank_rows)
st.markdown("### Sensitivity Score Table")
st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="Closeness Coefficient").round(4), use_container_width=True)

fig_sens = px.line(
    sensitivity_df,
    x="Scenario",
    y="Closeness Coefficient",
    color="Alternative",
    markers=True,
    color_discrete_sequence=RED_DISCRETE,
)
fig_sens.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens.update_layout(height=520, xaxis_title="Decision Scenario", yaxis_title="Closeness Coefficient")
fig_sens = plotly_red_layout(fig_sens, "Sensitivity Analysis: Closeness Coefficient Across Scenarios")
st.plotly_chart(fig_sens, use_container_width=True)

fig_rank = px.line(
    rank_df,
    x="Scenario",
    y="Rank",
    color="Alternative",
    markers=True,
    color_discrete_sequence=RED_DISCRETE,
)
fig_rank.update_traces(line=dict(width=4), marker=dict(size=10))
fig_rank.update_yaxes(autorange="reversed", dtick=1)
fig_rank.update_layout(height=520, xaxis_title="Decision Scenario", yaxis_title="Rank")
fig_rank = plotly_red_layout(fig_rank, "Ranking Stability Across Decision Scenarios")
st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("""
<div class="gold-note">
<h3>Interpretation of Sensitivity Analysis</h3>
<p>If the best alternative remains the same across most scenarios, the ranking is relatively robust. If the best alternative changes when one criterion becomes more important, the decision maker must explain why the selected weight structure is acceptable.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# INTERACTIVE MINI CALCULATOR
# =========================================================
st.markdown("## 10. Interactive Weight Experiment")
st.markdown("""
<div class="card">
<p>Use the sliders below to test how the ranking changes when weights are modified. The system automatically normalizes the weights so that the total equals 1.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Open interactive TOPSIS weight experiment", expanded=False):
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        w_cost = st.slider("Cost Weight", 0.05, 0.70, 0.30, 0.05)
    with col_b:
        w_usability = st.slider("Usability Weight", 0.05, 0.70, 0.30, 0.05)
    with col_c:
        w_features = st.slider("Features Weight", 0.05, 0.70, 0.25, 0.05)
    with col_d:
        w_support = st.slider("Support Time Weight", 0.05, 0.70, 0.15, 0.05)

    raw_weights = pd.Series({"Cost": w_cost, "Usability": w_usability, "Features": w_features, "Support Time": w_support})
    interactive_weights = (raw_weights / raw_weights.sum()).to_dict()
    st.write("Normalized weights used in calculation:")
    st.dataframe(pd.DataFrame({"Criterion": list(interactive_weights.keys()), "Normalized Weight": list(interactive_weights.values())}).round(4), use_container_width=True, hide_index=True)

    _, _, _, _, interactive_result = topsis_calculation(default_df, criteria_types, interactive_weights)
    st.dataframe(interactive_result.round(4), use_container_width=True, hide_index=True)

    fig_interactive = px.bar(
        interactive_result.sort_values("Closeness Coefficient", ascending=True),
        x="Closeness Coefficient",
        y="Alternative",
        orientation="h",
        text="Closeness Coefficient",
        color="Closeness Coefficient",
        color_continuous_scale=RED_SCALE,
    )
    fig_interactive.update_traces(texttemplate="%{text:.4f}", textposition="outside")
    fig_interactive.update_layout(height=430, coloraxis_showscale=False, xaxis_title="Closeness Coefficient", yaxis_title="")
    fig_interactive = plotly_red_layout(fig_interactive, "Interactive TOPSIS Ranking")
    st.plotly_chart(fig_interactive, use_container_width=True)

# =========================================================
# COMPARISON WITH SAW
# =========================================================
st.markdown("## 11. TOPSIS Compared with SAW")
comparison_df = pd.DataFrame({
    "Aspect": ["Main logic", "Final score", "Ideal solution", "Distance calculation", "Interpretation", "Complexity"],
    "SAW": ["Weighted summation", "Total weighted normalized score", "Not used", "Not used", "Higher score is better", "Simple"],
    "TOPSIS": ["Similarity to ideal solution", "Closeness coefficient", "Used", "Used", "Closer to ideal and farther from worst", "Moderate"]
})
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="dark-note">
<h3>Teaching Point</h3>
<p>SAW is usually easier for beginners. TOPSIS is more powerful for explanation because it shows how alternatives behave relative to the best possible and worst possible reference points.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# COMMON MISTAKES
# =========================================================
st.markdown("## 12. Common Mistakes in TOPSIS")
st.markdown("""
<div class="card">
<ol>
<li>Forgetting to distinguish between benefit and cost criteria when constructing ideal solutions.</li>
<li>Using simple max-min normalization when the selected TOPSIS procedure requires vector normalization.</li>
<li>Assuming that the highest original value is always ideal even for cost criteria.</li>
<li>Reporting only the final ranking without showing D+, D−, and closeness coefficient.</li>
<li>Using weights that do not sum to 1 without explaining normalization.</li>
<li>Ignoring sensitivity analysis even though TOPSIS results may change under different weights.</li>
<li>Misinterpreting D+ as a positive score. In fact, smaller D+ is better.</li>
<li>Misinterpreting D− as a negative score. In fact, larger D− is better.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DOWNLOAD
# =========================================================
st.markdown("## 13. Download Worked Example")
excel_bytes = to_excel_bytes(default_df, normalized, weighted, ideal_df, result, sensitivity_df, rank_df)
st.download_button(
    label="Download TOPSIS Worked Example Excel",
    data=excel_bytes,
    file_name="TOPSIS_Method_Worked_Example.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# QUIZ
# =========================================================
st.markdown("## 14. Self-Assessment Quiz")
st.markdown("""
<div class="note">
<p>This quiz contains exactly <b>10 questions</b>: 5 True/False and 5 Multiple Choice questions.</p>
</div>
""", unsafe_allow_html=True)

tf_questions = [
    {"question": "TOPSIS ranks alternatives using similarity to ideal solution.", "answer": "True"},
    {"question": "In TOPSIS, a larger D+ is always better.", "answer": "False"},
    {"question": "For benefit criteria, the positive ideal solution uses the maximum weighted normalized value.", "answer": "True"},
    {"question": "For cost criteria, the positive ideal solution uses the maximum weighted normalized value.", "answer": "False"},
    {"question": "A higher closeness coefficient indicates a better alternative.", "answer": "True"},
]

mcq_questions = [
    {"question": "What does TOPSIS compare each alternative against?", "options": ["Only the average value", "Positive and negative ideal solutions", "Only the lowest cost", "Only the highest benefit criterion"], "answer": "Positive and negative ideal solutions"},
    {"question": "Which value should be smaller for a good alternative?", "options": ["D+ distance to ideal", "D- distance from worst", "Closeness coefficient", "Criterion weight"], "answer": "D+ distance to ideal"},
    {"question": "Which value should be larger for a good alternative?", "options": ["D+ distance to ideal", "D- distance from worst", "Normalization denominator", "Cost criterion value"], "answer": "D- distance from worst"},
    {"question": "What is the TOPSIS final ranking value usually called?", "options": ["Consistency Ratio", "Closeness Coefficient", "Regret Measure", "Information Content"], "answer": "Closeness Coefficient"},
    {"question": "Why is sensitivity analysis useful in TOPSIS?", "options": ["To remove all criteria", "To avoid normalization", "To check ranking stability when weights change", "To force all alternatives to become equal"], "answer": "To check ranking stability when weights change"},
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
            st.success("Excellent. You understand the TOPSIS concept, ideal solutions, distances, and closeness coefficient.")
        elif percentage >= 70:
            st.info("Good. Review the ideal solution and distance interpretation to improve further.")
        else:
            st.warning("Please revisit the step-by-step TOPSIS calculation before moving to another method.")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)

# =========================================================
# FINAL SUMMARY
# =========================================================
st.markdown("""
<hr>
<div class="card">
<h2>Final Summary</h2>
<p>TOPSIS is a distance-based MCDM method. The best alternative should be close to the positive ideal solution and far from the negative ideal solution. The most important parts are vector normalization, correct treatment of benefit and cost criteria, construction of ideal solutions, distance calculation, closeness coefficient, and sensitivity analysis.</p>
</div>
""", unsafe_allow_html=True)
