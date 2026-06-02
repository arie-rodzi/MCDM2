import streamlit as st
from style import apply_style, hero, card

st.set_page_config(
    page_title="MCDM Masterclass",
    page_icon="📊",
    layout="wide"
)

apply_style()

# ==========================================================
# HERO SECTION
# ==========================================================

hero(
    "MCDM Masterclass",
    """
    A comprehensive learning platform for Multi-Criteria Decision-Making (MCDM),
    designed to guide students, researchers, academics, and decision-makers
    through the most widely used decision analysis techniques using
    interactive explanations, real-world examples, mathematical derivations,
    visualization tools, and hands-on calculations.
    """
)

# ==========================================================
# INTRODUCTION
# ==========================================================

card(
    "Welcome to the MCDM Masterclass",
    """
    Multi-Criteria Decision-Making (MCDM) is a collection of analytical methods
    used to evaluate, compare, and rank alternatives when multiple and often
    conflicting criteria must be considered simultaneously.

    In real-world decision environments, selecting the best alternative rarely
    depends on a single factor. Decision makers frequently need to balance
    economic, technical, social, environmental, and operational considerations.

    This platform has been developed as a complete educational environment
    where users can learn, understand, and apply several important MCDM
    techniques through structured learning modules and practical examples.
    """,
    "blue"
)

# ==========================================================
# WHAT YOU WILL LEARN
# ==========================================================

card(
    "What You Will Learn",
    """
    ✔ Weighting Techniques

    • Analytic Hierarchy Process (AHP)

    • CRITIC Method


    ✔ Ranking Techniques

    • Simple Additive Weighting (SAW)

    • Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)

    • VIKOR Method


    ✔ Cause-and-Effect Analysis

    • DEMATEL Method


    Each learning module includes:

    • Conceptual explanations

    • Mathematical foundations

    • Detailed worked examples

    • Interactive calculations

    • Visualization dashboards

    • Sensitivity analysis

    • Assessment quizzes

    • Downloadable calculation workbooks
    """,
    "green"
)

# ==========================================================
# WHY MCDM
# ==========================================================

card(
    "Why Multi-Criteria Decision-Making?",
    """
    Modern decision-making problems often involve multiple objectives
    that cannot be optimized simultaneously.

    Examples include:

    • Selecting the best supplier

    • Choosing a scholarship recipient

    • Evaluating project proposals

    • Ranking investment opportunities

    • Selecting a technology platform

    • Determining strategic priorities

    • Assessing organisational performance

    MCDM methods provide a systematic and transparent mechanism
    for transforming complex decision problems into structured,
    defendable, and reproducible solutions.
    """,
    "purple"
)

# ==========================================================
# LEARNING PATH
# ==========================================================

card(
    "Recommended Learning Path",
    """
    Step 1 → Understand the Fundamentals of MCDM

    Step 2 → Learn AHP and CRITIC for Weight Determination

    Step 3 → Study SAW as the Fundamental Ranking Method

    Step 4 → Explore TOPSIS and VIKOR for Advanced Ranking Analysis

    Step 5 → Learn DEMATEL for Cause-and-Effect Relationships

    Step 6 → Complete Quizzes and Compare Results Across Methods

    Step 7 → Apply the Methods to Real Decision Problems
    """,
    "orange"
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.info(
    """
    This learning platform is intended for educational, research,
    and professional development purposes. Users are encouraged to
    compare different MCDM methods and understand the strengths,
    limitations, and assumptions associated with each technique.
    """
)
