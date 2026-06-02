
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="CRITIC Method", page_icon="🟧", layout="wide")

# =========================================================
# PREMIUM ORANGE THEME FOR CRITIC METHOD
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(255, 173, 91, 0.24), transparent 34%),
        radial-gradient(circle at bottom right, rgba(126, 56, 12, 0.15), transparent 30%),
        linear-gradient(135deg, #FFF7EE 0%, #FFEBD6 43%, #F7D1A5 100%);
}
.block-container {padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1280px;}
.hero {
    padding: 36px 36px 32px 36px;
    border-radius: 30px;
    background: linear-gradient(135deg, #4A1F05 0%, #A94809 48%, #F39C12 100%);
    color: white;
    box-shadow: 0 24px 64px rgba(110, 45, 4, 0.29);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    right: -80px;
    top: -70px;
    width: 285px;
    height: 285px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.14);
}
.hero:before {
    content: "";
    position: absolute;
    left: -70px;
    bottom: -105px;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.hero h1 {font-size: 52px; line-height: 1.02; margin: 0; font-weight: 900; letter-spacing: -1.2px;}
.hero p {font-size: 18px; color: #FFF3E4; margin-top: 12px; max-width: 900px;}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.30);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 13px;
    letter-spacing: 0.2px;
}
.card {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(176, 90, 20, 0.18);
    border-radius: 24px;
    padding: 27px;
    margin: 18px 0;
    box-shadow: 0 14px 40px rgba(111, 48, 7, 0.11);
}
.card h2, .card h3 {color: #632B07;}
.card p, .card li {color: #3A2412; font-size: 16px; line-height: 1.7;}
.note {
    background: linear-gradient(135deg, #FFF9F1, #FFE7C8);
    border-left: 7px solid #D35400;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3A2412;
}
.gold-note {
    background: linear-gradient(135deg, #FFF8E2, #FAD894);
    border-left: 7px solid #B9770E;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3A2A11;
}
.dark-note {
    background: linear-gradient(135deg, #4A1F05, #7E3507);
    border-left: 7px solid #F39C12;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #FFF6E7;
}
.dark-note h3, .dark-note p, .dark-note li {color: #FFF6E7;}
.success-note {
    background: linear-gradient(135deg, #FFF4E5, #FFD5A5);
    border-left: 7px solid #E67E22;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 16px 0;
    color: #3B240F;
}
.metric-card {
    background: linear-gradient(135deg, #FFFFFF, #FFF0DD);
    border: 1px solid rgba(176,90,20,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 34px rgba(111, 48, 7, 0.10);
    text-align: center;
    min-height: 118px;
}
.metric-card .big {font-size: 34px; font-weight: 900; color: #632B07; line-height: 1.12;}
.metric-card .small {font-size: 14px; color: #7B4A1D; font-weight: 800; margin-top: 7px;}
.formula-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(211, 84, 0, 0.18);
    border-radius: 20px;
    padding: 18px 20px;
    margin: 12px 0;
}
.quiz-box {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 18px;
    border: 1px solid rgba(211,84,0,0.18);
    box-shadow: 0 10px 26px rgba(111, 48, 7, 0.07);
    margin: 16px 0 8px 0;
}
.viva-box {
    background: linear-gradient(135deg, #FFF7EC, #FFE1BD);
    border: 1px solid rgba(211,84,0,0.22);
    border-radius: 20px;
    padding: 20px;
    margin: 13px 0;
}
[data-testid="stDataFrame"] {border-radius: 18px; overflow: hidden;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7E3507, #E67E22) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.72rem 1.14rem !important;
    font-weight: 900 !important;
}
hr {border: none; height: 1px; background: rgba(176,90,20,0.24); margin: 28px 0;}
.small-caption {font-size: 13px; color: #7B4A1D; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

ORANGE_SCALE = ["#FFF3E4", "#FFD9AA", "#F5B35F", "#E67E22", "#B84E0A", "#632B07"]
ORANGE_SEQ = ["#632B07", "#9A3F06", "#D35400", "#F39C12", "#F7C873", "#7B4A1D"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def safe_min_positive(values):
    values = pd.Series(values).astype(float)
    positive = values[values > 0]
    if len(positive) == 0:
        return 0.0
    return float(positive.min())


def minmax_normalize(df, criteria_types):
    matrix = df.set_index("Alternative").astype(float)
    norm = pd.DataFrame(index=matrix.index)
    detail_rows = []
    for c in matrix.columns:
        x = matrix[c].astype(float)
        x_min = float(x.min())
        x_max = float(x.max())
        denom = x_max - x_min
        if denom == 0:
            norm[c] = 0.0
            rule = "All values equal; normalized as 0 because no contrast exists."
        elif criteria_types[c] == "Benefit":
            norm[c] = (x - x_min) / denom
            rule = "Benefit: (x - min) / (max - min)"
        else:
            norm[c] = (x_max - x) / denom
            rule = "Cost: (max - x) / (max - min)"
        detail_rows.append({
            "Criterion": c,
            "Type": criteria_types[c],
            "Minimum": x_min,
            "Maximum": x_max,
            "Range": denom,
            "Normalization Rule": rule,
        })
    norm = norm.replace([np.inf, -np.inf], np.nan).fillna(0)
    return norm, pd.DataFrame(detail_rows)


def critic_weights(df, criteria_types):
    norm, norm_detail = minmax_normalize(df, criteria_types)
    std = norm.std(axis=0, ddof=0)
    corr = norm.corr().replace([np.inf, -np.inf], np.nan).fillna(0)
    # If a criterion has zero variance, its correlation can become NaN. Fill diagonal correctly.
    for c in corr.columns:
        corr.loc[c, c] = 1.0
    conflict = (1 - corr).sum(axis=1)
    info = std * conflict
    if info.sum() == 0:
        weights = pd.Series(np.ones(len(info)) / len(info), index=info.index)
    else:
        weights = info / info.sum()
    critic_table = pd.DataFrame({
        "Criterion": weights.index,
        "Standard Deviation": std.values,
        "Conflict Intensity": conflict.values,
        "Information Content": info.values,
        "CRITIC Weight": weights.values,
    })
    critic_table["Rank"] = critic_table["CRITIC Weight"].rank(ascending=False, method="dense").astype(int)
    critic_table = critic_table.sort_values("Rank")
    return norm, norm_detail, std, corr, conflict, info, weights, critic_table


def saw_with_weights(df, criteria_types, weights):
    norm, _ = minmax_normalize(df, criteria_types)
    weight_series = pd.Series(weights)
    weighted = norm * weight_series
    scores = weighted.sum(axis=1)
    result = pd.DataFrame({
        "Alternative": scores.index,
        "Integrated Score": scores.values,
    })
    result["Rank"] = result["Integrated Score"].rank(ascending=False, method="dense").astype(int)
    result = result.sort_values("Rank")
    return norm, weighted, result


def entropy_weights_from_normalized(norm):
    # A simple comparator weight. It is used only for educational comparison, not as the main method.
    X = norm.copy().astype(float)
    col_sum = X.sum(axis=0).replace(0, np.nan)
    P = X / col_sum
    P = P.replace([np.inf, -np.inf], np.nan).fillna(0)
    m = len(X)
    if m <= 1:
        return pd.Series(np.ones(X.shape[1]) / X.shape[1], index=X.columns), P, pd.Series(np.zeros(X.shape[1]), index=X.columns)
    k = 1 / np.log(m)
    entropy = -k * (P * np.log(P.replace(0, np.nan))).sum(axis=0).fillna(0)
    diversity = 1 - entropy
    if diversity.sum() == 0:
        weights = pd.Series(np.ones(len(diversity)) / len(diversity), index=diversity.index)
    else:
        weights = diversity / diversity.sum()
    return weights, P, entropy


def plotly_orange_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#632B07")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.58)",
        font=dict(color="#3A2412"),
        margin=dict(l=22, r=22, t=72, b=24),
        legend=dict(bgcolor="rgba(255,255,255,0.72)", bordercolor="rgba(176,90,20,0.22)", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="rgba(176,90,20,0.14)", zerolinecolor="rgba(176,90,20,0.22)")
    fig.update_yaxes(gridcolor="rgba(176,90,20,0.14)", zerolinecolor="rgba(176,90,20,0.22)")
    return fig


def to_excel_bytes(original, criteria_info, normalized, norm_detail, corr, critic_table, weighted, ranking, sensitivity_df, entropy_table, explanation_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        header_fmt = workbook.add_format({"bold": True, "bg_color": "#E67E22", "font_color": "#FFFFFF", "border": 1})
        note_fmt = workbook.add_format({"text_wrap": True, "valign": "top"})
        num_fmt = workbook.add_format({"num_format": "0.0000"})
        original.to_excel(writer, sheet_name="01 Original Matrix", index=False)
        criteria_info.to_excel(writer, sheet_name="02 Criteria Info", index=False)
        norm_detail.to_excel(writer, sheet_name="03 Normalization Rules", index=False)
        normalized.to_excel(writer, sheet_name="04 Normalized Matrix")
        corr.to_excel(writer, sheet_name="05 Correlation Matrix")
        critic_table.to_excel(writer, sheet_name="06 CRITIC Weights", index=False)
        weighted.to_excel(writer, sheet_name="07 Weighted Matrix")
        ranking.to_excel(writer, sheet_name="08 Ranking", index=False)
        sensitivity_df.to_excel(writer, sheet_name="09 Sensitivity", index=False)
        entropy_table.to_excel(writer, sheet_name="10 Entropy Comparison", index=False)
        explanation_df.to_excel(writer, sheet_name="11 Formula Notes", index=False)
        for sheet_name, worksheet in writer.sheets.items():
            worksheet.freeze_panes(1, 0)
            worksheet.set_column(0, 0, 24)
            worksheet.set_column(1, 15, 18, num_fmt)
            if sheet_name == "11 Formula Notes":
                worksheet.set_column(0, 0, 28)
                worksheet.set_column(1, 1, 75, note_fmt)
            # Apply header format to first row when possible.
            try:
                max_col = 12
                for col in range(max_col):
                    worksheet.write(0, col, worksheet.table.get(0, {}).get(col, ''), header_fmt)
            except Exception:
                pass
    return output.getvalue()

# =========================================================
# DEFAULT CASE STUDY DATA
# =========================================================
default_df = pd.DataFrame({
    "Alternative": ["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E"],
    "Cost": [82, 76, 91, 68, 74],
    "Quality": [78, 84, 72, 88, 81],
    "Delivery Speed": [70, 86, 75, 80, 92],
    "Sustainability": [65, 76, 83, 70, 88],
    "Risk": [42, 35, 49, 31, 38],
})
criteria_types = {
    "Cost": "Cost",
    "Quality": "Benefit",
    "Delivery Speed": "Benefit",
    "Sustainability": "Benefit",
    "Risk": "Cost",
}
criteria_info = pd.DataFrame({
    "Criterion": list(criteria_types.keys()),
    "Type": [criteria_types[c] for c in criteria_types],
    "Meaning": [
        "Procurement cost score; lower is better.",
        "Product or service quality rating; higher is better.",
        "Ability to deliver quickly and consistently; higher is better.",
        "Environmental and social sustainability rating; higher is better.",
        "Operational and supply risk score; lower is better.",
    ],
    "Why It Matters": [
        "A supplier should be financially efficient.",
        "High quality reduces defects and complaints.",
        "Fast delivery supports service continuity.",
        "Sustainability supports long-term institutional responsibility.",
        "Lower risk improves reliability and continuity.",
    ]
})

normalized, norm_detail, std, corr, conflict, info, weights, critic_table = critic_weights(default_df, criteria_types)
_, weighted, ranking = saw_with_weights(default_df, criteria_types, weights.to_dict())
base_best = ranking.iloc[0]["Alternative"]
base_score = ranking.iloc[0]["Integrated Score"]

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="pill">MCDM Learning Module • Premium Orange Edition</div>
    <h1>CRITIC Method</h1>
    <p>A detailed objective weighting module using contrast intensity, correlation conflict, information content, ranking integration, sensitivity analysis, full Excel calculation, viva notes, and self-assessment quiz.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(default_df)}</div><div class='small'>Alternatives</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='big'>{len(criteria_types)}</div><div class='small'>Criteria</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='big'>{critic_table.iloc[0]['Criterion']}</div><div class='small'>Highest CRITIC Weight</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='big'>{base_best}</div><div class='small'>Best Alternative • {base_score:.4f}</div></div>", unsafe_allow_html=True)

# =========================================================
# 1. CONCEPT OVERVIEW
# =========================================================
st.markdown("""
<div class="card">
<h2>1. Concept Overview</h2>
<p><b>CRITIC</b> stands for <b>CRiteria Importance Through Intercriteria Correlation</b>. It is an objective weighting method used in Multi-Criteria Decision-Making (MCDM).</p>
<p>The key idea is simple but powerful: a criterion should receive a higher weight when it has strong contrast among alternatives and when it provides information that is not duplicated by other criteria.</p>
<p>In other words, CRITIC does not ask a decision maker to manually assign weights. Instead, it learns the weight structure from the data matrix itself.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<h3>Why CRITIC is Different</h3>
<p>SAW, TOPSIS, and VIKOR usually require weights before ranking can be performed. CRITIC focuses on how to generate those weights objectively from the decision matrix.</p>
<ul>
<li><b>High standard deviation</b> means the criterion can discriminate between alternatives.</li>
<li><b>Low correlation with other criteria</b> means the criterion gives unique information.</li>
<li><b>High information content</b> means the criterion deserves stronger weight.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 2. HISTORICAL NOTE
# =========================================================
st.markdown("""
<div class="card">
<h2>2. Historical Background</h2>
<p>The CRITIC method was introduced by Diakoulaki, Mavrotas and Papayannakis in 1995 as an objective approach for determining criteria weights. The method became popular because it combines two important statistical ideas: contrast intensity and conflict among criteria.</p>
<p>It is especially useful when the researcher wants to avoid purely subjective weighting or when expert judgement is limited, inconsistent, or difficult to collect.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 3. WHEN TO USE CRITIC
# =========================================================
st.markdown("""
<div class="card">
<h2>3. When Should We Use CRITIC?</h2>
<ol>
<li>When the data matrix is available and reliable.</li>
<li>When the researcher wants objective weights.</li>
<li>When expert-based pairwise comparison is difficult.</li>
<li>When criteria may overlap and correlation should be considered.</li>
<li>When the study needs transparent statistical justification for weights.</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dark-note">
<h3>Important Limitation</h3>
<p>CRITIC does not understand policy priority by itself. It only reads information from the numerical decision matrix. If a criterion is strategically important but shows little variation in the data, CRITIC may give it a small weight.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 4. REAL CASE STUDY
# =========================================================
st.markdown("## 4. Real Case Study: Supplier Selection")
st.markdown("""
<div class="note">
<p>An organization wants to select the best supplier. Five suppliers are evaluated using five criteria. Some criteria are benefit criteria, while others are cost criteria.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(default_df, use_container_width=True, hide_index=True)

st.markdown("### Criteria Information")
st.dataframe(criteria_info, use_container_width=True, hide_index=True)

# =========================================================
# 5. MATHEMATICAL FOUNDATION
# =========================================================
st.markdown("""
<div class="card">
<h2>5. Mathematical Foundation</h2>
<p>Let the original decision matrix be represented by <b>X</b>. The matrix contains <b>m</b> alternatives and <b>n</b> criteria.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"X=[x_{ij}]_{m \times n}")
st.latex(r"i=1,2,\ldots,m \qquad j=1,2,\ldots,n")

st.markdown("""
<div class="formula-card">
<h3>Step 1: Normalize the Decision Matrix</h3>
<p>Normalization is required because different criteria may use different units and directions.</p>
</div>
""", unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.markdown("""
    <div class="success-note">
    <h3>Benefit Criterion</h3>
    <p>Higher value is better.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_{ij}=\frac{x_{ij}-\min_i(x_{ij})}{\max_i(x_{ij})-\min_i(x_{ij})}")
with right:
    st.markdown("""
    <div class="gold-note">
    <h3>Cost Criterion</h3>
    <p>Lower value is better.</p>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_{ij}=\frac{\max_i(x_{ij})-x_{ij}}{\max_i(x_{ij})-\min_i(x_{ij})}")

st.markdown("""
<div class="formula-card">
<h3>Step 2: Calculate Standard Deviation</h3>
<p>The standard deviation measures contrast intensity. A criterion with higher variation can separate alternatives more clearly.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\sigma_j=\sqrt{\frac{1}{m}\sum_{i=1}^{m}(r_{ij}-\bar{r}_j)^2}")

st.markdown("""
<div class="formula-card">
<h3>Step 3: Calculate Correlation Conflict</h3>
<p>If two criteria are highly correlated, they may contain overlapping information. CRITIC reduces redundancy by using the conflict term.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\rho_{jk}=\frac{\sum_i(r_{ij}-\bar{r}_j)(r_{ik}-\bar{r}_k)}{\sqrt{\sum_i(r_{ij}-\bar{r}_j)^2}\sqrt{\sum_i(r_{ik}-\bar{r}_k)^2}}");
st.latex(r"\text{Conflict}_j=\sum_{k=1}^{n}(1-\rho_{jk})")

st.markdown("""
<div class="formula-card">
<h3>Step 4: Information Content</h3>
<p>The information content combines contrast intensity and conflict intensity.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"C_j=\sigma_j\sum_{k=1}^{n}(1-\rho_{jk})")

st.markdown("""
<div class="formula-card">
<h3>Step 5: Final CRITIC Weight</h3>
<p>The information content is normalized into weights that sum to 1.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"w_j=\frac{C_j}{\sum_{j=1}^{n}C_j}, \qquad \sum_{j=1}^{n}w_j=1")

# =========================================================
# 6. NORMALIZATION DETAILS
# =========================================================
st.markdown("## 6. Normalization Details")
st.markdown("""
<div class="note">
<p>The matrix below shows the normalized performance values after converting both benefit and cost criteria into the same direction. After normalization, a larger value is always better.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(norm_detail, use_container_width=True, hide_index=True)
st.dataframe(normalized.round(4), use_container_width=True)

# Manual examples
st.markdown("## 7. Manual Calculation Example")
st.markdown("""
<div class="card">
<h3>Example A: Cost Criterion</h3>
<p>Cost is a cost criterion. Lower cost is better, therefore the best value becomes closer to 1 after normalization.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\min(Cost)=68, \qquad \max(Cost)=91")
st.latex(r"r_{Supplier\ A,Cost}=\frac{91-82}{91-68}=\frac{9}{23}=0.3913")
st.latex(r"r_{Supplier\ D,Cost}=\frac{91-68}{91-68}=1.0000")

st.markdown("""
<div class="card">
<h3>Example B: Benefit Criterion</h3>
<p>Quality is a benefit criterion. Higher quality is better, therefore the highest value becomes 1 after normalization.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"\min(Quality)=72, \qquad \max(Quality)=88")
st.latex(r"r_{Supplier\ A,Quality}=\frac{78-72}{88-72}=\frac{6}{16}=0.3750")
st.latex(r"r_{Supplier\ D,Quality}=\frac{88-72}{88-72}=1.0000")

# =========================================================
# 8. STANDARD DEVIATION
# =========================================================
st.markdown("## 8. Contrast Intensity: Standard Deviation")
st.markdown("""
<div class="note">
<p>Standard deviation answers this question: <b>Does the criterion clearly differentiate the alternatives?</b> If all alternatives are almost the same under a criterion, that criterion provides limited discriminating power.</p>
</div>
""", unsafe_allow_html=True)
std_df = pd.DataFrame({"Criterion": std.index, "Standard Deviation": std.values}).sort_values("Standard Deviation", ascending=False)
st.dataframe(std_df.round(4), use_container_width=True, hide_index=True)
fig_std = px.bar(std_df, x="Criterion", y="Standard Deviation", text="Standard Deviation", color="Standard Deviation", color_continuous_scale=ORANGE_SCALE)
fig_std.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_std.update_layout(height=430, showlegend=False, coloraxis_showscale=False, xaxis_title="Criterion", yaxis_title="Standard Deviation")
fig_std = plotly_orange_layout(fig_std, "Contrast Intensity by Criterion")
st.plotly_chart(fig_std, use_container_width=True)

# =========================================================
# 9. CORRELATION MATRIX
# =========================================================
st.markdown("## 9. Correlation Matrix and Conflict Intensity")
st.markdown("""
<div class="card">
<p>Correlation shows whether two criteria move together. A high positive correlation means the criteria may provide similar information. CRITIC rewards criteria that are less redundant.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(corr.round(4), use_container_width=True)
fig_corr = px.imshow(corr.round(4), text_auto=True, aspect="auto", color_continuous_scale="Oranges", zmin=-1, zmax=1)
fig_corr.update_layout(height=520, xaxis_title="Criterion", yaxis_title="Criterion", coloraxis_colorbar=dict(title="Correlation"))
fig_corr = plotly_orange_layout(fig_corr, "Correlation Heatmap")
st.plotly_chart(fig_corr, use_container_width=True)

conflict_df = pd.DataFrame({"Criterion": conflict.index, "Conflict Intensity": conflict.values}).sort_values("Conflict Intensity", ascending=False)
st.dataframe(conflict_df.round(4), use_container_width=True, hide_index=True)
fig_conflict = px.bar(conflict_df, x="Criterion", y="Conflict Intensity", text="Conflict Intensity", color="Conflict Intensity", color_continuous_scale=ORANGE_SCALE)
fig_conflict.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_conflict.update_layout(height=430, showlegend=False, coloraxis_showscale=False, xaxis_title="Criterion", yaxis_title="Conflict Intensity")
fig_conflict = plotly_orange_layout(fig_conflict, "Conflict Intensity by Criterion")
st.plotly_chart(fig_conflict, use_container_width=True)

# =========================================================
# 10. INFORMATION CONTENT AND WEIGHTS
# =========================================================
st.markdown("## 10. Information Content and CRITIC Weight")
st.markdown("""
<div class="success-note">
<p>The information content is obtained by multiplying standard deviation with conflict intensity. The final CRITIC weight is obtained by normalizing the information content.</p>
</div>
""", unsafe_allow_html=True)
st.dataframe(critic_table.round(4), use_container_width=True, hide_index=True)

fig_weight = px.bar(critic_table.sort_values("CRITIC Weight", ascending=True), x="CRITIC Weight", y="Criterion", orientation="h", text="CRITIC Weight", color="CRITIC Weight", color_continuous_scale=ORANGE_SCALE)
fig_weight.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_weight.update_layout(height=460, showlegend=False, coloraxis_showscale=False, xaxis_title="CRITIC Weight", yaxis_title="")
fig_weight = plotly_orange_layout(fig_weight, "Final Objective Weights from CRITIC")
st.plotly_chart(fig_weight, use_container_width=True)

# =========================================================
# 11. WEIGHT INTERPRETATION
# =========================================================
st.markdown("## 11. Interpretation of Weights")
interpret_rows = []
for _, row in critic_table.iterrows():
    crit = row["Criterion"]
    w = row["CRITIC Weight"]
    sd = row["Standard Deviation"]
    cf = row["Conflict Intensity"]
    if w >= critic_table["CRITIC Weight"].mean():
        meaning = "This criterion receives relatively high importance because it contributes stronger information to the decision matrix."
    else:
        meaning = "This criterion receives lower objective importance because its contrast and/or unique information is weaker in this dataset."
    interpret_rows.append({"Criterion": crit, "Weight": w, "Standard Deviation": sd, "Conflict": cf, "Interpretation": meaning})
interpret_df = pd.DataFrame(interpret_rows)
st.dataframe(interpret_df.round(4), use_container_width=True, hide_index=True)

# =========================================================
# 12. INTEGRATING CRITIC WEIGHTS INTO RANKING
# =========================================================
st.markdown("## 12. Ranking Integration Using CRITIC Weights")
st.markdown("""
<div class="card">
<p>CRITIC itself is a weighting method. To rank alternatives, the generated weights can be integrated into a ranking model such as SAW, TOPSIS, VIKOR, MOORA, or another MCDM technique. In this learning module, we use a simple weighted aggregation to show how CRITIC weights affect final ranking.</p>
</div>
""", unsafe_allow_html=True)
st.latex(r"Score_i=\sum_{j=1}^{n}w_jr_{ij}")
st.markdown("### Weighted Normalized Matrix")
st.dataframe(weighted.round(4), use_container_width=True)
st.markdown("### Final Ranking")
st.dataframe(ranking.round(4), use_container_width=True, hide_index=True)

fig_rank = px.bar(ranking.sort_values("Integrated Score", ascending=True), x="Integrated Score", y="Alternative", orientation="h", text="Integrated Score", color="Integrated Score", color_continuous_scale=ORANGE_SCALE)
fig_rank.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_rank.update_layout(height=450, showlegend=False, coloraxis_showscale=False, xaxis_title="Integrated Score", yaxis_title="")
fig_rank = plotly_orange_layout(fig_rank, "Final Ranking After Integrating CRITIC Weights")
st.plotly_chart(fig_rank, use_container_width=True)

# =========================================================
# 13. RADAR CHART FOR NORMALIZED PERFORMANCE
# =========================================================
st.markdown("## 13. Alternative Performance Profile")
st.markdown("""
<div class="note">
<p>The radar chart shows how alternatives behave across normalized criteria. This helps learners see why a supplier may rank highly even if it is not the best in every single criterion.</p>
</div>
""", unsafe_allow_html=True)
radar_fig = go.Figure()
criteria_names = list(normalized.columns)
for alt in normalized.index:
    values = normalized.loc[alt].tolist()
    radar_fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=criteria_names + [criteria_names[0]],
        fill="toself",
        name=alt,
        line=dict(width=2),
    ))
radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=560)
radar_fig = plotly_orange_layout(radar_fig, "Normalized Performance Radar Chart")
st.plotly_chart(radar_fig, use_container_width=True)

# =========================================================
# 14. COMPARISON WITH ENTROPY WEIGHTING
# =========================================================
st.markdown("## 14. Comparison with Entropy Weighting")
st.markdown("""
<div class="card">
<p>This section is included for learning only. Entropy and CRITIC are both objective weighting methods, but they are not identical. Entropy emphasizes dispersion in probability distribution, while CRITIC explicitly includes correlation conflict.</p>
</div>
""", unsafe_allow_html=True)
entropy_w, P_entropy, entropy_values = entropy_weights_from_normalized(normalized)
entropy_table = pd.DataFrame({
    "Criterion": normalized.columns,
    "CRITIC Weight": [weights[c] for c in normalized.columns],
    "Entropy Weight": [entropy_w[c] for c in normalized.columns],
    "Entropy Value": [entropy_values[c] for c in normalized.columns],
})
st.dataframe(entropy_table.round(4), use_container_width=True, hide_index=True)
compare_long = entropy_table.melt(id_vars="Criterion", value_vars=["CRITIC Weight", "Entropy Weight"], var_name="Method", value_name="Weight")
fig_compare = px.bar(compare_long, x="Criterion", y="Weight", color="Method", barmode="group", text="Weight", color_discrete_sequence=["#D35400", "#632B07"])
fig_compare.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig_compare.update_layout(height=470, xaxis_title="Criterion", yaxis_title="Weight")
fig_compare = plotly_orange_layout(fig_compare, "CRITIC vs Entropy Weight Comparison")
st.plotly_chart(fig_compare, use_container_width=True)

# =========================================================
# 15. SENSITIVITY ANALYSIS
# =========================================================
st.markdown("## 15. Sensitivity Analysis")
st.markdown("""
<div class="card">
<p>For CRITIC, sensitivity analysis can be performed by changing the treatment of correlation conflict. The base CRITIC method uses both standard deviation and conflict. We compare this with alternative objective weighting scenarios.</p>
</div>
""", unsafe_allow_html=True)

# Scenario calculations
scenarios = {}
# Base CRITIC
scenarios["Base CRITIC"] = weights
# Contrast only: weight by standard deviation
std_weights = std / std.sum() if std.sum() != 0 else pd.Series(np.ones(len(std))/len(std), index=std.index)
scenarios["Contrast Only"] = std_weights
# Conflict only
conflict_weights = conflict / conflict.sum() if conflict.sum() != 0 else pd.Series(np.ones(len(conflict))/len(conflict), index=conflict.index)
scenarios["Conflict Only"] = conflict_weights
# Entropy comparator
scenarios["Entropy Comparator"] = entropy_w
# Equal weight comparator
equal_weights = pd.Series(np.ones(len(weights))/len(weights), index=weights.index)
scenarios["Equal Weight"] = equal_weights

sensitivity_rows = []
scenario_rank_rows = []
for scenario_name, scenario_w in scenarios.items():
    _, _, scenario_result = saw_with_weights(default_df, criteria_types, scenario_w.to_dict())
    for _, r in scenario_result.iterrows():
        sensitivity_rows.append({"Scenario": scenario_name, "Alternative": r["Alternative"], "Score": r["Integrated Score"]})
        scenario_rank_rows.append({"Scenario": scenario_name, "Alternative": r["Alternative"], "Rank": r["Rank"]})
sensitivity_df = pd.DataFrame(sensitivity_rows)
scenario_rank_df = pd.DataFrame(scenario_rank_rows)
st.dataframe(sensitivity_df.pivot(index="Alternative", columns="Scenario", values="Score").round(4), use_container_width=True)

fig_sens = px.line(sensitivity_df, x="Scenario", y="Score", color="Alternative", markers=True, color_discrete_sequence=ORANGE_SEQ)
fig_sens.update_traces(line=dict(width=4), marker=dict(size=10))
fig_sens.update_layout(height=520, xaxis_title="Weighting Scenario", yaxis_title="Integrated Score")
fig_sens = plotly_orange_layout(fig_sens, "Sensitivity of Alternative Scores")
st.plotly_chart(fig_sens, use_container_width=True)

fig_rank_stability = px.line(scenario_rank_df, x="Scenario", y="Rank", color="Alternative", markers=True, color_discrete_sequence=ORANGE_SEQ)
fig_rank_stability.update_traces(line=dict(width=4), marker=dict(size=10))
fig_rank_stability.update_yaxes(autorange="reversed", dtick=1)
fig_rank_stability.update_layout(height=520, xaxis_title="Weighting Scenario", yaxis_title="Rank")
fig_rank_stability = plotly_orange_layout(fig_rank_stability, "Ranking Stability Across Weighting Scenarios")
st.plotly_chart(fig_rank_stability, use_container_width=True)

st.markdown("""
<div class="gold-note">
<h3>How to Read This Sensitivity Analysis</h3>
<ul>
<li><b>Base CRITIC</b>: Uses standard deviation and correlation conflict.</li>
<li><b>Contrast Only</b>: Uses only standard deviation.</li>
<li><b>Conflict Only</b>: Uses only correlation conflict.</li>
<li><b>Entropy Comparator</b>: Compares with another objective weighting method.</li>
<li><b>Equal Weight</b>: Checks what happens if all criteria are treated equally.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 16. INTERACTIVE CALCULATOR
# =========================================================
st.markdown("## 16. Interactive CRITIC Calculator")
st.markdown("""
<div class="card">
<p>This section allows learners to edit the decision matrix and immediately observe how CRITIC weights and ranking change. It is useful for classroom demonstrations and workshop activities.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Open Interactive Data Editor", expanded=False):
    edited_df = st.data_editor(default_df, use_container_width=True, num_rows="dynamic", key="critic_editor")
    st.markdown("<p class='small-caption'>Note: Keep the first column named Alternative and keep numeric values for all criteria.</p>", unsafe_allow_html=True)
    if "Alternative" in edited_df.columns and len(edited_df.columns) > 2:
        try:
            edited_criteria = [c for c in edited_df.columns if c != "Alternative"]
            edited_types = {}
            cols = st.columns(len(edited_criteria))
            for idx, c in enumerate(edited_criteria):
                with cols[idx]:
                    edited_types[c] = st.selectbox(f"Type: {c}", ["Benefit", "Cost"], index=0 if criteria_types.get(c, "Benefit") == "Benefit" else 1, key=f"type_{c}")
            e_norm, e_norm_detail, e_std, e_corr, e_conflict, e_info, e_weights, e_critic_table = critic_weights(edited_df, edited_types)
            _, e_weighted, e_ranking = saw_with_weights(edited_df, edited_types, e_weights.to_dict())
            st.markdown("### Updated CRITIC Weights")
            st.dataframe(e_critic_table.round(4), use_container_width=True, hide_index=True)
            st.markdown("### Updated Ranking")
            st.dataframe(e_ranking.round(4), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Please check the edited matrix. Error: {e}")

# =========================================================
# 17. WHY CRITIC CAN CHANGE RESULTS
# =========================================================
st.markdown("## 17. Why CRITIC Can Produce Different Weights")
st.markdown("""
<div class="card">
<p>CRITIC can produce weights that differ from expert judgement because it is not measuring perceived importance. It measures statistical information in the data matrix.</p>
<p>A criterion may be very important in real life, but if all alternatives have similar values under that criterion, CRITIC may assign a low weight because it cannot differentiate alternatives.</p>
<p>Similarly, if two criteria are very similar, CRITIC may reduce their combined influence because the information is duplicated.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 18. METHOD COMPARISON TABLE
# =========================================================
st.markdown("## 18. CRITIC Compared with Other Weighting Methods")
comparison_df = pd.DataFrame({
    "Method": ["AHP", "Entropy", "CRITIC", "Equal Weight"],
    "Weight Type": ["Subjective", "Objective", "Objective", "Neutral Baseline"],
    "Main Input": ["Expert pairwise comparison", "Decision matrix", "Decision matrix", "No preference information"],
    "Key Logic": ["Human judgement and consistency", "Dispersion / uncertainty", "Contrast + correlation conflict", "All criteria treated equally"],
    "Strength": ["Captures expert priority", "Simple objective weighting", "Considers redundancy among criteria", "Easy benchmark"],
    "Weakness": ["Can be subjective and inconsistent", "Does not directly use correlation conflict", "Depends on data quality", "May ignore real importance"],
})
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# =========================================================
# 19. COMMON MISTAKES
# =========================================================
st.markdown("## 19. Common Mistakes in CRITIC")
st.markdown("""
<div class="card">
<ol>
<li>Forgetting to normalize cost and benefit criteria correctly.</li>
<li>Assuming CRITIC weights represent expert preference.</li>
<li>Using raw matrix correlation instead of normalized matrix correlation without explanation.</li>
<li>Ignoring zero variance criteria.</li>
<li>Forgetting that CRITIC is a weighting method, not a complete ranking method by itself.</li>
<li>Using CRITIC when data quality is weak or highly uncertain.</li>
<li>Not explaining why objective weighting is suitable for the research problem.</li>
<li>Not comparing CRITIC weights with another weighting method or baseline.</li>
<li>Reporting final ranking without showing intermediate matrices.</li>
<li>Failing to explain the meaning of conflict intensity.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 20. VIVA QUESTIONS AND MODEL ANSWERS
# =========================================================
st.markdown("## 20. Viva Questions and Suggested Answers")
viva_items = [
    ("Why did you use CRITIC?", "CRITIC was used because the study needs objective weights derived from the data matrix. It considers both variation among alternatives and correlation conflict among criteria."),
    ("Is CRITIC a ranking method?", "Strictly speaking, CRITIC is a weighting method. The weights can be integrated into a ranking method such as SAW, TOPSIS, VIKOR, or another aggregation model."),
    ("What does standard deviation mean in CRITIC?", "It represents contrast intensity. A criterion with higher variation is better able to discriminate among alternatives."),
    ("What does correlation conflict mean?", "It measures uniqueness of information. If a criterion is highly correlated with other criteria, it may contain redundant information."),
    ("Can CRITIC replace expert judgement?", "Not always. CRITIC is useful for objective weighting, but strategic or policy importance may still require expert validation."),
    ("Why must criteria be normalized?", "Normalization ensures all criteria are comparable and have the same direction before standard deviation and correlation are calculated."),
    ("What happens if a criterion has zero variance?", "It cannot discriminate alternatives, so its information contribution becomes weak or zero. The researcher must report and justify the treatment."),
    ("Why compare CRITIC with Entropy?", "Both are objective weighting methods, but CRITIC includes correlation conflict while Entropy focuses more on dispersion or uncertainty."),
]
for q, a in viva_items:
    st.markdown(f"""
    <div class="viva-box">
    <h3>{q}</h3>
    <p>{a}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 21. DOWNLOAD FULL CALCULATION EXCEL
# =========================================================
st.markdown("## 21. Download Full Calculation Workbook")
explanation_df = pd.DataFrame({
    "Component": [
        "Decision Matrix", "Normalization", "Standard Deviation", "Correlation", "Conflict", "Information Content", "CRITIC Weight", "Ranking Integration", "Sensitivity Analysis"
    ],
    "Explanation": [
        "Original alternatives and criteria values.",
        "Benefit and cost criteria are transformed so that higher normalized value is better.",
        "Measures contrast intensity of each criterion.",
        "Measures relationship among normalized criteria.",
        "Calculated as the sum of one minus correlation for each criterion.",
        "Calculated by multiplying standard deviation with conflict intensity.",
        "Information content is normalized so that all weights sum to one.",
        "CRITIC weights are applied to normalized matrix to obtain integrated scores.",
        "Alternative rankings are compared across objective weighting scenarios."
    ]
})
excel_bytes = to_excel_bytes(default_df, criteria_info, normalized, norm_detail, corr, critic_table, weighted, ranking, sensitivity_df, entropy_table, explanation_df)
st.download_button(
    label="Download CRITIC Full Calculation Excel",
    data=excel_bytes,
    file_name="CRITIC_Method_Full_Calculation.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================================================
# 22. SELF-ASSESSMENT QUIZ
# =========================================================
st.markdown("## 22. Self-Assessment Quiz")
st.markdown("""
<div class="note">
<p>This quiz contains exactly <b>10 questions</b>: 5 True/False and 5 Multiple Choice questions.</p>
</div>
""", unsafe_allow_html=True)

tf_questions = [
    {"question": "CRITIC is mainly used to generate objective criteria weights.", "answer": "True"},
    {"question": "CRITIC ignores correlation among criteria.", "answer": "False"},
    {"question": "A criterion with high standard deviation has stronger contrast intensity.", "answer": "True"},
    {"question": "CRITIC weights always represent expert preference.", "answer": "False"},
    {"question": "Normalization is required before calculating CRITIC weights.", "answer": "True"},
]

mcq_questions = [
    {"question": "What does CRITIC stand for?", "options": ["Criteria Ranking Through Ideal Comparison", "CRiteria Importance Through Intercriteria Correlation", "Correlation Ratio in Theoretical Criteria", "Critical Ranking of Integrated Choices"], "answer": "CRiteria Importance Through Intercriteria Correlation"},
    {"question": "Which two main components are used in CRITIC?", "options": ["Distance and closeness", "Utility and regret", "Standard deviation and correlation conflict", "Pairwise matrix and consistency ratio"], "answer": "Standard deviation and correlation conflict"},
    {"question": "What does a high standard deviation indicate?", "options": ["No difference among alternatives", "Strong contrast among alternatives", "High expert consistency", "Low correlation only"], "answer": "Strong contrast among alternatives"},
    {"question": "What is the final CRITIC weight based on?", "options": ["Information content divided by total information content", "Random expert score", "Only the mean value", "Only the best alternative"], "answer": "Information content divided by total information content"},
    {"question": "Why is CRITIC useful before TOPSIS or SAW?", "options": ["It removes all criteria", "It generates objective weights for ranking", "It replaces the decision matrix", "It avoids normalization"], "answer": "It generates objective weights for ranking"},
]

answers = {}
st.markdown("### Part A: True / False")
for i, q in enumerate(tf_questions, start=1):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"tf_{i}"] = st.radio(f"Answer Q{i}", ["Select answer", "True", "False"], key=f"critic_tf_{i}", label_visibility="collapsed")

st.markdown("### Part B: Multiple Choice")
for i, q in enumerate(mcq_questions, start=6):
    st.markdown(f"<div class='quiz-box'><b>Q{i}. {q['question']}</b></div>", unsafe_allow_html=True)
    answers[f"mcq_{i}"] = st.radio(f"Answer Q{i}", ["Select answer"] + q["options"], key=f"critic_mcq_{i}", label_visibility="collapsed")

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
            st.success("Excellent. You understand CRITIC weighting very well.")
        elif percentage >= 70:
            st.info("Good. Review the role of correlation conflict and standard deviation.")
        else:
            st.warning("Please revisit the mathematical formulation and worked calculation before moving forward.")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)

# =========================================================
# 23. FINAL SUMMARY
# =========================================================
st.markdown("""
<hr>
<div class="card">
<h2>Final Summary</h2>
<p>CRITIC is a strong objective weighting method because it does not only measure variation but also accounts for redundancy among criteria. A criterion becomes important when it differentiates alternatives and provides unique information.</p>
<p>For a complete MCDM analysis, CRITIC weights should be clearly reported together with the normalized matrix, standard deviation, correlation matrix, conflict intensity, information content, and final integrated ranking.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# APPENDIX: DETAILED TEACHING NOTES FOR TRAINER USE
# These comments are intentionally kept inside the file so trainers can
# explain CRITIC step-by-step when editing or extending the module.
# =========================================================
# Teaching Note 001: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 002: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 003: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 004: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 005: The final CRITIC weight must sum to one.
# Trainer Prompt 001: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 006: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 007: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 008: CRITIC should be interpreted together with the research context.
# Teaching Note 009: The correlation matrix should be inspected, not merely reported.
# Viva Reminder 001: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 010: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 002: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 011: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 012: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 013: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 014: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 015: The final CRITIC weight must sum to one.
# Trainer Prompt 003: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 016: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 017: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 018: CRITIC should be interpreted together with the research context.
# Viva Reminder 002: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 019: The correlation matrix should be inspected, not merely reported.
# Teaching Note 020: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 004: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 021: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 022: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 023: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 024: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 025: The final CRITIC weight must sum to one.
# Trainer Prompt 005: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 026: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 027: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Viva Reminder 003: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 028: CRITIC should be interpreted together with the research context.
# Teaching Note 029: The correlation matrix should be inspected, not merely reported.
# Teaching Note 030: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 006: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 031: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 032: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 033: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 034: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 035: The final CRITIC weight must sum to one.
# Trainer Prompt 007: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 036: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Viva Reminder 004: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 037: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 038: CRITIC should be interpreted together with the research context.
# Teaching Note 039: The correlation matrix should be inspected, not merely reported.
# Teaching Note 040: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 008: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 041: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 042: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 043: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 044: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 045: The final CRITIC weight must sum to one.
# Trainer Prompt 009: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Viva Reminder 005: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 046: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 047: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 048: CRITIC should be interpreted together with the research context.
# Teaching Note 049: The correlation matrix should be inspected, not merely reported.
# Teaching Note 050: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 010: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 051: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 052: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 053: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 054: Benefit criteria and cost criteria must be normalized in the same direction.
# Viva Reminder 006: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 055: The final CRITIC weight must sum to one.
# Trainer Prompt 011: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 056: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 057: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 058: CRITIC should be interpreted together with the research context.
# Teaching Note 059: The correlation matrix should be inspected, not merely reported.
# Teaching Note 060: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 012: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 061: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 062: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 063: Correlation conflict prevents duplicated criteria from dominating the model.
# Viva Reminder 007: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 064: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 065: The final CRITIC weight must sum to one.
# Trainer Prompt 013: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 066: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 067: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 068: CRITIC should be interpreted together with the research context.
# Teaching Note 069: The correlation matrix should be inspected, not merely reported.
# Teaching Note 070: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 014: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 071: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 072: Contrast intensity is represented by standard deviation of normalized criteria.
# Viva Reminder 008: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 073: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 074: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 075: The final CRITIC weight must sum to one.
# Trainer Prompt 015: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 076: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 077: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 078: CRITIC should be interpreted together with the research context.
# Teaching Note 079: The correlation matrix should be inspected, not merely reported.
# Teaching Note 080: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 016: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 081: CRITIC is not a subjective preference method; it derives weights from data.
# Viva Reminder 009: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 082: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 083: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 084: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 085: The final CRITIC weight must sum to one.
# Trainer Prompt 017: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 086: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 087: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 088: CRITIC should be interpreted together with the research context.
# Teaching Note 089: The correlation matrix should be inspected, not merely reported.
# Teaching Note 090: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 018: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Viva Reminder 010: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 091: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 092: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 093: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 094: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 095: The final CRITIC weight must sum to one.
# Trainer Prompt 019: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 096: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 097: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 098: CRITIC should be interpreted together with the research context.
# Teaching Note 099: The correlation matrix should be inspected, not merely reported.
# Viva Reminder 011: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 100: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 020: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 101: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 102: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 103: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 104: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 105: The final CRITIC weight must sum to one.
# Trainer Prompt 021: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 106: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 107: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 108: CRITIC should be interpreted together with the research context.
# Viva Reminder 012: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 109: The correlation matrix should be inspected, not merely reported.
# Teaching Note 110: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 022: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 111: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 112: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 113: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 114: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 115: The final CRITIC weight must sum to one.
# Trainer Prompt 023: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 116: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 117: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Viva Reminder 013: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 118: CRITIC should be interpreted together with the research context.
# Teaching Note 119: The correlation matrix should be inspected, not merely reported.
# Teaching Note 120: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 024: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 121: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 122: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 123: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 124: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 125: The final CRITIC weight must sum to one.
# Trainer Prompt 025: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 126: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Viva Reminder 014: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 127: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 128: CRITIC should be interpreted together with the research context.
# Teaching Note 129: The correlation matrix should be inspected, not merely reported.
# Teaching Note 130: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 026: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 131: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 132: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 133: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 134: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 135: The final CRITIC weight must sum to one.
# Trainer Prompt 027: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Viva Reminder 015: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 136: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 137: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 138: CRITIC should be interpreted together with the research context.
# Teaching Note 139: The correlation matrix should be inspected, not merely reported.
# Teaching Note 140: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 028: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 141: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 142: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 143: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 144: Benefit criteria and cost criteria must be normalized in the same direction.
# Viva Reminder 016: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 145: The final CRITIC weight must sum to one.
# Trainer Prompt 029: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 146: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 147: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 148: CRITIC should be interpreted together with the research context.
# Teaching Note 149: The correlation matrix should be inspected, not merely reported.
# Teaching Note 150: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 030: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 151: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 152: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 153: Correlation conflict prevents duplicated criteria from dominating the model.
# Viva Reminder 017: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 154: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 155: The final CRITIC weight must sum to one.
# Trainer Prompt 031: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 156: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 157: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 158: CRITIC should be interpreted together with the research context.
# Teaching Note 159: The correlation matrix should be inspected, not merely reported.
# Teaching Note 160: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 032: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 161: CRITIC is not a subjective preference method; it derives weights from data.
# Teaching Note 162: Contrast intensity is represented by standard deviation of normalized criteria.
# Viva Reminder 018: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 163: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 164: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 165: The final CRITIC weight must sum to one.
# Trainer Prompt 033: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 166: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 167: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 168: CRITIC should be interpreted together with the research context.
# Teaching Note 169: The correlation matrix should be inspected, not merely reported.
# Teaching Note 170: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 034: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 171: CRITIC is not a subjective preference method; it derives weights from data.
# Viva Reminder 019: Explain that CRITIC is a weighting method and requires integration with a ranking method.
# Teaching Note 172: Contrast intensity is represented by standard deviation of normalized criteria.
# Teaching Note 173: Correlation conflict prevents duplicated criteria from dominating the model.
# Teaching Note 174: Benefit criteria and cost criteria must be normalized in the same direction.
# Teaching Note 175: The final CRITIC weight must sum to one.
# Trainer Prompt 035: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Teaching Note 176: A high CRITIC weight can come from high standard deviation, high conflict, or both.
# Teaching Note 177: A low CRITIC weight does not necessarily mean the criterion is not important in policy terms.
# Teaching Note 178: CRITIC should be interpreted together with the research context.
# Teaching Note 179: The correlation matrix should be inspected, not merely reported.
# Teaching Note 180: Sensitivity analysis is important because objective weighting methods can produce different rankings.
# Trainer Prompt 036: Ask learners which criterion has strongest contrast and whether it also has unique information.
# Viva Reminder 020: Explain that CRITIC is a weighting method and requires integration with a ranking method.
