import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="VIKOR Method", page_icon="💜", layout="wide")

# =========================================================
# ROYAL PURPLE PREMIUM THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(157, 119, 255, 0.28), transparent 30%),
        radial-gradient(circle at bottom right, rgba(80, 32, 130, 0.16), transparent 35%),
        linear-gradient(135deg, #F8F4FF 0%, #EFE7FA 45%, #E6DDF3 100%);
}
.block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1280px;}
.hero {
    padding: 36px 36px 32px 36px;
    border-radius: 32px;
    background: linear-gradient(135deg, #241138 0%, #4A216D 55%, #8E5FD3 100%);
    color: white;
    box-shadow: 0 26px 65px rgba(50, 22, 80, 0.30);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    right: -85px;
    top: -75px;
    width: 285px;
    height: 285px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.14);
}
.hero h1 {font-size: 50px; line-height: 1.04; margin: 0; font-weight: 900; letter-spacing: -1.3px;}
.hero p {font-size: 18px; color: #F2E9FF; margin-top: 13px; max-width: 920px;}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.28);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 12px;
}
.card {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(92, 55, 145, 0.18);
    border-radius: 24px;
    padding: 26px;
    margin: 18px 0;
    box-shadow: 0 14px 40px rgba(50, 22, 80, 0.10);
}
.card h2, .card h3 {color: #32164F;}
.note {
    background: linear-gradient(135deg, #FBF8FF, #EFE6FC);
    border-left: 7px solid #6F3BB7;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #2E2140;
}
.gold-note {
    background: linear-gradient(135deg, #FFF9E7, #F5E4B8);
    border-left: 7px solid #BE943C;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3E3017;
}
.success-note {
    background: linear-gradient(135deg, #F1EAFE, #E2D3FA);
    border-left: 7px solid #4A216D;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #27163A;
}
.danger-note {
    background: linear-gradient(135deg, #FFF1F5, #F8D7E2);
    border-left: 7px solid #B03A69;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #45172A;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF, #F1E9FD);
    border: 1px solid rgba(92,55,145,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(50, 22, 80, 0.09);
    text-align: center;
    min-height: 116px;
}
.metric-card .big {font-size: 34px; font-weight: 900; color: #32164F;}
.metric-card .small {font-size: 14px; color: #695779; font-weight: 800;}
.quiz-box {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(92,55,145,0.18);
    box-shadow: 0 10px 25px rgba(50, 22, 80, 0.06);
    margin: 16px 0 8px 0;
}
.compare-box {
    background: linear-gradient(135deg, #FFFFFF, #F6F0FF);
    border-radius: 20px;
    border: 1px solid rgba(92,55,145,0.18);
    padding: 20px;
    height: 100%;
}
[data-testid="stDataFrame"] {border-radius: 18px; overflow: hidden;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #4A216D, #8E5FD3) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.1rem !important;
    font-weight: 900 !important;
}
hr {border: none; height: 1px; background: rgba(92,55,145,0.22); margin: 26px 0;}
</style>
""", unsafe_allow_html=True)

PURPLE_SCALE = ["#EFE6FC", "#D6C2F2", "#B28DE4", "#8E5FD3", "#6F3BB7", "#4A216D", "#32164F"]
PURPLE_DISCRETE = ["#32164F", "#6F3BB7", "#8E5FD3", "#BE943C", "#B03A69", "#5D4E75"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def vikor_calculation(df, criteria_types, weights, v=0.5):
    matrix = df.set_index("Alternative").astype(float)
    w = pd.Series(weights, dtype=float)
    w = w / w.sum()

    best = pd.Series(index=matrix.columns, dtype=float)
    worst = pd.Series(index=matrix.columns, dtype=float)
    for c in matrix.columns:
        if criteria_types[c] == "Benefit":
            best[c] = matrix[c].max()
            worst[c] = matrix[c].min()
        else:
            best[c] = matrix[c].min()
            worst[c] = matrix[c].max()

    gap = best - worst
    # Formula transformed for both benefit and cost so that 0 is best and 1 is worst.
    normalized_gap = pd.DataFrame(index=matrix.index, columns=matrix.columns, dtype=float)
    for c in matrix.columns:
        denom = abs(best[c] - worst[c])
        if denom == 0:
            normalized_gap[c] = 0.0
        elif criteria_types[c] == "Benefit":
            normalized_gap[c] = (best[c] - matrix[c]) / denom
        else:
            normalized_gap[c] = (matrix[c] - best[c]) / denom

    weighted_gap = normalized_gap * w
    S = weighted_gap.sum(axis=1)
    R = weighted_gap.max(axis=1)

    S_star, S_minus = S.min(), S.max()
    R_star, R_minus = R.min(), R.max()

    if S_minus == S_star:
        S_part = pd.Series(0, index=S.index, dtype=float)
    else:
        S_part = (S - S_star) / (S_minus - S_star)
    if R_minus == R_star:
        R_part = pd.Series(0, index=R.index, dtype=float)
    else:
        R_part = (R - R_star) / (R_minus - R_star)

    Q = v * S_part + (1 - v) * R_part

    result = pd.DataFrame({
        "Alternative": matrix.index,
        "S (Group Utility Gap)": S.values,
        "R (Individual Regret)": R.values,
        "Q (Compromise Index)": Q.values,
    })
    result["Rank by Q"] = result["Q (Compromise Index)"].rank(ascending=True, method="dense").astype(int)
    result = result.sort_values("Rank by Q")

    best_worst_df = pd.DataFrame({
        "Criterion": matrix.columns,
        "Type": [criteria_types[c] for c in matrix.columns],
        "Weight": [w[c] for c in matrix.columns],
        "Best f*": [best[c] for c in matrix.columns],
        "Worst f-": [worst[c] for c in matrix.columns],
    })
    return matrix, best_worst_df, normalized_gap, weighted_gap, result


def acceptable_conditions(result):
    m = len(result)
    dq = 1 / (m - 1) if m > 1 else 0
    sorted_result = result.sort_values("Q (Compromise Index)").reset_index(drop=True)
    if m < 2:
        return dq, True, True, "Only one alternative is available."
    q1 = sorted_result.loc[0, "Q (Compromise Index)"]
    q2 = sorted_result.loc[1, "Q (Compromise Index)"]
    a1 = sorted_result.loc[0, "Alternative"]
    condition_1 = (q2 - q1) >= dq
    rank_s = result.sort_values("S (Group Utility Gap)").iloc[0]["Alternative"]
    rank_r = result.sort_values("R (Individual Regret)").iloc[0]["Alternative"]
    condition_2 = (a1 == rank_s) or (a1 == rank_r)
    text = f"Best by Q is {a1}. Best by S is {rank_s}. Best by R is {rank_r}."
    return dq, condition_1, condition_2, text


def to_excel_bytes(original, best_worst, normalized_gap, weighted_gap, result, sensitivity_df, ranking_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        original.to_excel(writer, sheet_name="Original Data", index=False)
        best_worst.to_excel(writer, sheet_name="Best Worst Values", index=False)
        normalized_gap.to_excel(writer, sheet_name="Normalized Gap")
        weighted_gap.to_excel(writer, sheet_name="Weighted Gap")
        result.to_excel(writer, sheet_name="VIKOR Result", index=False)
        sensitivity_df.to_excel(writer, sheet_name="v Sensitivity", index=False)
        ranking_df.to_excel(writer, sheet_name="Ranking Stability", index=False)
    return output.getvalue()


def purple_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#32164F")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.60)",
        font=dict(color="#2E2140"),
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0.70)", bordercolor="rgba(92,55,145,0.20)", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="rgba(92,55,145,0.13)", zerolinecolor="rgba(92,55,145,0.22)")
    fig.update_yaxes(gridcolor="rgba(92,55,145,0.13)", zerolinecolor="rgba(92,55,145,0.22)")
    return fig

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="pill">MCDM Learning Module • Royal Purple Edition</div>
    <h1>VIKOR Method</h1>
    <p>A premium interactive note for compromise ranking: group utility, individual regret, Q index, acceptable advantage, acceptable stability, sensitivity analysis, downloadable Excel output, and self-assessment quiz.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
default_df = pd.DataFrame({
    "Alternative": ["Platform A", "Platform B", "Platform C", "Platform D"],
    "Cost": [12000, 15000, 10000, 18000],
    "Usability": [80, 90, 75, 85],
    "Security": [78, 88, 70, 92],
    "Features": [70, 85, 65, 95],
    "Support Time": [12, 8, 15, 6]
})
criteria_types = {
    "Cost": "Cost",
    "Usability": "Benefit",
    "Security": "Benefit",
    "Features": "Benefit",
    "Support Time": "Cost"
}
weights = {
    "Cost": 0.25,
    "Usability": 0.25,
    "Security": 0.20,
    "Features": 0.20,
    "Support Time": 0.10
}

# v parameter
st.sidebar.markdown("## VIKOR Control Panel")
st.sidebar.markdown("Adjust the compromise parameter **v** to explore how ranking changes.")
v = st.sidebar.slider("Compromise parameter, v", min_value=0.00, max_value=1.00, value=0.50, step=0.05)
st.sidebar.markdown("""
**Interpretation**
- v = 0.00: regret-focused decision  
- v = 0.50: balanced compromise  
- v = 1.00: group utility-focused decision
""")

matrix, best_worst_df, normalized_gap, weighted_gap, result = vikor_calculation(default_df, criteria_types, weights, v)
best_alt = result.iloc[0]["Alternative"]
best_q = result.iloc[0]["Q (Compromise Index)"]
dq, c1_condition, c2_condition, condition_text = acceptable_conditions(result)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(default_df)}</div><div class='small'>Alternatives</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(weights)}</div><div class='small'>Criteria</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='big'>{v:.2f}</div><div class='small'>Compromise Parameter v</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='big'>{best_alt}</div><div class='small'>Best Alternative • Q {best_q:.4f}</div></div>", unsafe_allow_html=True)

# =========================================================
# 1 CONCEPT OVERVIEW
# =========================================================
st.markdown("""
<div class="card">
<h2>1. Concept Overview</h2>
<p><b>VIKOR</b> is a compromise ranking method in Multi-Criteria Decision-Making. It is useful when decision makers need a solution that is not merely the highest weighted score, but a balanced compromise between overall performance and the worst individual weakness.</p>
<p>The name VIKOR comes from the Serbian phrase <i>VIseKriterijumska Optimizacija I Kompromisno Resenje</i>, which means multi-criteria optimization and compromise solution.</p>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    <div class="success-note">
    <h3>Group Utility, S</h3>
    <p>Measures the total weighted gap from the ideal solution across all criteria. It asks: how good is the alternative overall?</p>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown("""
    <div class="danger-note">
    <h3>Individual Regret, R</h3>
    <p>Measures the worst weighted gap among all criteria. It asks: what is the biggest weakness of the alternative?</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="note">
<h3>Why VIKOR is different</h3>
<p>SAW focuses on weighted summation. TOPSIS focuses on distance from ideal and anti-ideal solutions. VIKOR focuses on a <b>compromise solution</b> by combining two ideas: maximum group utility and minimum individual regret.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 2 HISTORY
# =========================================================
st.markdown("""
<div class="card">
<h2>2. Short Historical Background</h2>
<p>VIKOR is commonly associated with the work of Serafim Opricovic and was developed for multi-criteria optimization problems where decision makers need a compromise ranking among conflicting criteria.</p>
<p>It became popular because many real decision problems do not have one alternative that is best in every criterion. VIKOR helps identify an alternative that is acceptable from both collective and worst-case perspectives.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 3 CASE STUDY
# =========================================================
st.markdown("""
<div class="card">
<h2>3. Real Case Study</h2>
<p>A university wants to select the most suitable digital learning platform. The decision involves cost, usability, security, features, and technical support response time.</p>
<p>This example is suitable for VIKOR because the lowest-cost platform may not be the most secure, while the most feature-rich platform may be expensive. Therefore, a compromise solution is needed.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 4. Original Decision Matrix")
st.dataframe(default_df, use_container_width=True, hide_index=True)

criteria_df = pd.DataFrame({
    "Criterion": list(weights.keys()),
    "Type": [criteria_types[c] for c in weights.keys()],
    "Weight": [weights[c] for c in weights.keys()],
    "Decision Logic": ["Lower is better" if criteria_types[c] == "Cost" else "Higher is better" for c in weights.keys()]
})
st.markdown("## 5. Criteria Type and Weight")
st.dataframe(criteria_df, use_container_width=True, hide_index=True)

# =========================================================
# 6 FORMULATION
# =========================================================
st.markdown("""
<div class="card">
<h2>6. Mathematical Formulation</h2>
<p>The decision matrix contains alternatives as rows and criteria as columns.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"X=[x_{ij}]_{m \times n}")
st.latex(r"A_i=\text{alternative }i, \qquad C_j=\text{criterion }j")

st.markdown("""
<div class="note">
<h3>Best and Worst Values</h3>
<p>VIKOR first identifies the best and worst values for every criterion. For benefit criteria, the best value is the maximum. For cost criteria, the best value is the minimum.</p>
</div>
""", unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.markdown("<div class='success-note'><h3>Benefit Criterion</h3><p>Higher value is better.</p></div>", unsafe_allow_html=True)
    st.latex(r"f_j^* = \max_i f_{ij}")
    st.latex(r"f_j^- = \min_i f_{ij}")
with right:
    st.markdown("<div class='gold-note'><h3>Cost Criterion</h3><p>Lower value is better.</p></div>", unsafe_allow_html=True)
    st.latex(r"f_j^* = \min_i f_{ij}")
    st.latex(r"f_j^- = \max_i f_{ij}")

st.markdown("""
<div class="card">
<h3>Utility Measure, Regret Measure and Q Index</h3>
<p>The weighted normalized gap measures how far an alternative is from the ideal value. Lower gap is better.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"d_{ij}=w_j\frac{f_j^*-f_{ij}}{f_j^*-f_j^-}\quad \text{for benefit criteria}")
st.latex(r"d_{ij}=w_j\frac{f_{ij}-f_j^*}{f_j^- - f_j^*}\quad \text{for cost criteria}")
st.latex(r"S_i=\sum_{j=1}^{n} d_{ij}")
st.latex(r"R_i=\max_j(d_{ij})")
st.latex(r"Q_i=v\frac{S_i-S^*}{S^- - S^*}+(1-v)\frac{R_i-R^*}{R^- - R^*}")
st.latex(r"S^*=\min_i S_i, \quad S^- = \max_i S_i, \quad R^*=\min_i R_i, \quad R^- = \max_i R_i")

st.markdown("""
<div class="note">
<h3>Meaning of v</h3>
<p>The parameter <b>v</b> controls decision preference. A higher v gives more emphasis to group utility S. A lower v gives more emphasis to individual regret R.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# STEP BY STEP
# =========================================================
st.markdown("## 7. Step-by-Step Worked Calculation")

st.markdown("""
<div class="note">
<h3>Step 1: Identify Best and Worst Values</h3>
<p>For each criterion, VIKOR determines the ideal and worst reference values.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(best_worst_df.round(4), use_container_width=True, hide_index=True)

st.markdown("""
<div class="note">
<h3>Step 2: Calculate Normalized Gap</h3>
<p>The normalized gap shows how far each alternative is from the best value. A value close to 0 is better. A value close to 1 is worse.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(normalized_gap.round(4), use_container_width=True)

st.markdown("""
<div class="note">
<h3>Step 3: Apply Criterion Weights</h3>
<p>Each normalized gap is multiplied by its criterion weight. This creates the weighted gap matrix.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(weighted_gap.round(4), use_container_width=True)

st.markdown("""
<div class="note">
<h3>Step 4: Compute S and R</h3>
<p><b>S</b> is the total weighted gap. <b>R</b> is the worst weighted gap. In VIKOR, smaller S and smaller R are better.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(result[["Alternative", "S (Group Utility Gap)", "R (Individual Regret)"]].round(4), use_container_width=True, hide_index=True)

st.markdown("""
<div class="note">
<h3>Step 5: Compute Q and Rank Alternatives</h3>
<p>The Q index combines S and R using the selected v value. The best alternative has the lowest Q value.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(result.round(4), use_container_width=True, hide_index=True)

# =========================================================
# GRAPHS
# =========================================================
st.markdown("## 8. Visual Analysis")
fig_q = px.bar(
    result.sort_values("Q (Compromise Index)", ascending=False),
    x="Q (Compromise Index)",
    y="Alternative",
    orientation="h",
    text="Q (Compromise Index)",
    color="Q (Compromise Index)",
    color_continuous_scale=PURPLE_SCALE,
)
fig_q.update_traces(texttemplate="%{text:.4f}", textposition="outside", marker_line_width=0)
fig_q.update_layout(height=440, showlegend=False, coloraxis_showscale=False, xaxis_title="Q Index (lower is better)", yaxis_title="")
fig_q = purple_layout(fig_q, "VIKOR Q Index Ranking")
st.plotly_chart(fig_q, use_container_width=True)

fig_sr = go.Figure()
fig_sr.add_trace(go.Bar(name="S: Group Utility Gap", x=result["Alternative"], y=result["S (Group Utility Gap)"], marker_color="#6F3BB7"))
fig_sr.add_trace(go.Bar(name="R: Individual Regret", x=result["Alternative"], y=result["R (Individual Regret)"], marker_color="#BE943C"))
fig_sr.update_layout(barmode="group", height=470, xaxis_title="Alternative", yaxis_title="Value (lower is better)")
fig_sr = purple_layout(fig_sr, "S and R Comparison")
st.plotly_chart(fig_sr, use_container_width=True)

heatmap_df = weighted_gap.copy()
fig_heat = px.imshow(
    heatmap_df,
    text_auto=".4f",
    color_continuous_scale=PURPLE_SCALE,
    aspect="auto",
)
fig_heat.update_layout(height=470, coloraxis_colorbar=dict(title="Weighted Gap"))
fig_heat = purple_layout(fig_heat, "Weighted Gap Heatmap")
st.plotly_chart(fig_heat, use_container_width=True)

# =========================================================
# ACCEPTABLE ADVANTAGE AND STABILITY
# =========================================================
st.markdown("## 9. Acceptable Advantage and Acceptable Stability")
st.markdown("""
<div class="card">
<p>VIKOR does not only rank alternatives. It also checks whether the top alternative can be accepted as a compromise solution. Two conditions are usually considered:</p>
<ol>
<li><b>Acceptable Advantage</b>: The difference between the first and second Q values should be large enough.</li>
<li><b>Acceptable Stability</b>: The best Q alternative should also be best by S or best by R.</li>
</ol>
</div>
""", unsafe_allow_html=True)
st.latex(r"DQ=\frac{1}{m-1}")

cc1, cc2, cc3 = st.columns(3)
with cc1:
    st.markdown(f"<div class='metric-card'><div class='big'>{dq:.4f}</div><div class='small'>DQ Threshold</div></div>", unsafe_allow_html=True)
with cc2:
    st.markdown(f"<div class='metric-card'><div class='big'>{'PASS' if c1_condition else 'CHECK'}</div><div class='small'>Acceptable Advantage</div></div>", unsafe_allow_html=True)
with cc3:
    st.markdown(f"<div class='metric-card'><div class='big'>{'PASS' if c2_condition else 'CHECK'}</div><div class='small'>Acceptable Stability</div></div>", unsafe_allow_html=True)

if c1_condition and c2_condition:
    st.markdown(f"<div class='success-note'><h3>Compromise Solution Accepted</h3><p>{condition_text}</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='gold-note'><h3>Compromise Solution Needs Careful Interpretation</h3><p>{condition_text}</p><p>If one of the VIKOR conditions is not satisfied, the decision maker may present a set of compromise alternatives instead of only one winner.</p></div>", unsafe_allow_html=True)

# =========================================================
# SENSITIVITY ANALYSIS BY v
# =========================================================
st.markdown("## 10. Sensitivity Analysis Using v")
st.markdown("""
<div class="card">
<p>For VIKOR, sensitivity analysis is naturally linked to the parameter <b>v</b>. Instead of changing criterion weights only, we can observe how the ranking changes when the decision maker becomes more regret-focused or more utility-focused.</p>
</div>
""", unsafe_allow_html=True)

v_scenarios = {
    "Regret Dominant (v=0.25)": 0.25,
    "Balanced Compromise (v=0.50)": 0.50,
    "Utility Dominant (v=0.75)": 0.75,
    "Pure Utility (v=1.00)": 1.00,
}
sensitivity_rows = []
rank_rows = []
for scenario, vv in v_scenarios.items():
    _, _, _, _, scenario_result = vikor_calculation(default_df, criteria_types, weights, vv)
    for _, row in scenario_result.iterrows():
        sensitivity_rows.append({"Scenario": scenario, "v": vv, "Alternative": row["Alternative"], "Q": row["Q (Compromise Index)"]})
        rank_rows.append({"Scenario": scenario, "v": vv, "Alternative": row["Alternative"], "Rank": row["Rank by Q"]})

sensitivity_df = pd.DataFrame(sensitivity_rows)
ranking_df = pd.DataFrame(rank_rows)
st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="Q").round(4), use_container_width=True)

fig_sens = px.line(
    sensitivity_df,
    x="Scenario",
    y="Q",
    color="Alternative",
    markers=True,
    color_discrete_sequence=PURPLE_DISCRETE,
)
fig_sens.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens.update_layout(height=500, xaxis_title="v Scenario", yaxis_title="Q Index (lower is better)")
fig_sens = purple_layout(fig_sens, "Q Index Across v Scenarios")
st.plotly_chart(fig_sens, use_container_width=True)

fig_rank = px.line(
    ranking_df,
    x="Scenario",
    y="Rank",
    color="Alternative",
    markers=True,
    color_discrete_sequence=PURPLE_DISCRETE,
)
fig_rank.update_traces(line=dict(width=4), marker=dict(size=10))
fig_rank.update_yaxes(autorange="reversed", dtick=1)
fig_rank.update_layout(height=500, xaxis_title="v Scenario", yaxis_title="Rank")
fig_rank = purple_layout(fig_rank, "Ranking Stability Across v Scenarios")
st.plotly_chart(fig_rank, use_container_width=True)

# =========================================================
# COMPARISON
# =========================================================
st.markdown("## 11. Comparison with SAW and TOPSIS")
comparison_df = pd.DataFrame({
    "Feature": ["Main Logic", "Best Value Used", "Worst Value Used", "Distance Concept", "Regret Concept", "Compromise Solution", "Main Output"],
    "SAW": ["Weighted summation", "Through normalization", "Not explicit", "No", "No", "No", "Final weighted score"],
    "TOPSIS": ["Distance to ideal solution", "Positive ideal solution", "Negative ideal solution", "Yes", "No", "No", "Closeness coefficient"],
    "VIKOR": ["Compromise ranking", "Best f*", "Worst f-", "Indirect gap", "Yes", "Yes", "Q compromise index"],
})
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# =========================================================
# VIVA QUESTIONS
# =========================================================
st.markdown("## 12. Possible Viva or Presentation Questions")
st.markdown("""
<div class="card">
<ol>
<li><b>Why use VIKOR instead of SAW?</b><br>Because VIKOR does not only sum performance. It also considers regret, which represents the worst criterion gap for each alternative.</li>
<li><b>Why use VIKOR instead of TOPSIS?</b><br>TOPSIS focuses on distance from ideal and anti-ideal points, while VIKOR focuses on compromise ranking using group utility and individual regret.</li>
<li><b>What does S represent?</b><br>S represents the overall group utility gap. Smaller S means the alternative is closer to the ideal solution across all criteria.</li>
<li><b>What does R represent?</b><br>R represents individual regret, meaning the worst weighted criterion gap for an alternative.</li>
<li><b>What does Q represent?</b><br>Q is the compromise index combining S and R based on the value of v.</li>
<li><b>What is the role of v?</b><br>v controls whether the decision emphasizes group utility or individual regret.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# COMMON MISTAKES
# =========================================================
st.markdown("## 13. Common Mistakes in VIKOR")
st.markdown("""
<div class="card">
<ol>
<li>Assuming the highest Q value is the best. In VIKOR, the lowest Q value is preferred.</li>
<li>Using the benefit formula for cost criteria.</li>
<li>Ignoring the meaning of S and R.</li>
<li>Using v = 0.5 without explaining why.</li>
<li>Not checking acceptable advantage and acceptable stability.</li>
<li>Thinking VIKOR is the same as TOPSIS because both use ideal values.</li>
<li>Forgetting that the VIKOR output may be a set of compromise alternatives.</li>
<li>Using weights that do not sum to 1.</li>
<li>Not conducting sensitivity analysis on v.</li>
<li>Presenting ranking without explaining the compromise logic.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DOWNLOAD
# =========================================================
st.markdown("## 14. Download Worked Example")
excel_bytes = to_excel_bytes(default_df, best_worst_df, normalized_gap, weighted_gap, result, sensitivity_df, ranking_df)
st.download_button(
    label="Download VIKOR Worked Example Excel",
    data=excel_bytes,
    file_name="VIKOR_Method_Worked_Example.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# QUIZ
# =========================================================
st.markdown("## 15. Self-Assessment Quiz")
st.markdown("""
<div class="note">
<p>This quiz contains exactly <b>10 questions</b>: 5 True/False and 5 Multiple Choice questions.</p>
</div>
""", unsafe_allow_html=True)

tf_questions = [
    {"question": "In VIKOR, the lowest Q value is preferred.", "answer": "True"},
    {"question": "S represents the worst individual criterion gap.", "answer": "False"},
    {"question": "R represents individual regret.", "answer": "True"},
    {"question": "The value of v affects the final Q index.", "answer": "True"},
    {"question": "VIKOR is exactly the same as SAW because both only use weighted summation.", "answer": "False"},
]

mcq_questions = [
    {"question": "What is the main idea of VIKOR?", "options": ["Simple weighted sum", "Compromise ranking", "Random ranking", "Only pairwise comparison"], "answer": "Compromise ranking"},
    {"question": "What does S measure?", "options": ["Group utility gap", "Consistency ratio", "Correlation weight", "Cause-effect power"], "answer": "Group utility gap"},
    {"question": "What does R measure?", "options": ["Average score", "Worst weighted gap", "Total distance from negative ideal", "Eigenvalue"], "answer": "Worst weighted gap"},
    {"question": "What does v control?", "options": ["Number of alternatives", "Balance between S and R", "Data type only", "The criterion names"], "answer": "Balance between S and R"},
    {"question": "Which statement is correct?", "options": ["Higher Q is always better", "Lower Q is preferred", "Q is not used in ranking", "Q only works for cost criteria"], "answer": "Lower Q is preferred"},
]

answers = {}
st.markdown("### Part A: True / False")
for i, q in enumerate(tf_questions, start=1):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"tf_{i}"] = st.radio(f"Answer Q{i}", ["Select answer", "True", "False"], key=f"vikor_tf_{i}", label_visibility="collapsed")

st.markdown("### Part B: Multiple Choice")
for i, q in enumerate(mcq_questions, start=6):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"mcq_{i}"] = st.radio(f"Answer Q{i}", ["Select answer"] + q["options"], key=f"vikor_mcq_{i}", label_visibility="collapsed")

if st.button("Submit Quiz"):
    incomplete = any(vv == "Select answer" for vv in answers.values())
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
            st.success("Excellent. You understand the VIKOR compromise ranking concept.")
        elif percentage >= 70:
            st.info("Good. Review S, R, Q and the role of v to improve further.")
        else:
            st.warning("Please revisit the worked calculation before moving to another MCDM method.")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)

st.markdown("""
<hr>
<div class="card">
<h2>Final Summary</h2>
<p>VIKOR is powerful because it does not only identify the alternative with good overall performance. It also checks the worst criterion weakness through regret. Therefore, it is especially useful when the best decision should be a compromise between group utility and individual regret.</p>
</div>
""", unsafe_allow_html=True)
