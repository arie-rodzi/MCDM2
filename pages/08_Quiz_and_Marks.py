import streamlit as st
import pandas as pd
import os
import datetime
import random
from style import apply_style, hero

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Quiz and Marks",
    page_icon="📝",
    layout="wide"
)

apply_style()

RESULT = "data/results.csv"

# ==========================================================
# HEADER
# ==========================================================
hero(
    "08 | Student Quiz and Marks",
    "Students complete the MCDM assessment, submit their answers, and check their marks using Student ID."
)

# ==========================================================
# STUDENT DETAILS
# ==========================================================
with st.expander("Student Details", expanded=True):
    name = st.text_input("Full Name")
    student_id = st.text_input("Student ID / Matric No")
    email = st.text_input("Email")

# ==========================================================
# QUESTIONS
# 20 QUESTIONS:
# 10 TRUE/FALSE
# 10 MULTIPLE CHOICE A-D
# NO FILL IN THE BLANK
# ==========================================================
questions = [
    # TRUE / FALSE
    ("MCDM is used when a decision involves more than one criterion.", "tf", True),
    ("A cost criterion means that a higher value is preferred.", "tf", False),
    ("Benefit criteria prefer higher values.", "tf", True),
    ("Sensitivity analysis checks whether ranking changes when weights change.", "tf", True),
    ("SAW uses weighted summation to calculate the final score.", "tf", True),
    ("TOPSIS ranks alternatives based only on expert judgement.", "tf", False),
    ("AHP uses pairwise comparison to determine priority weights.", "tf", True),
    ("CRITIC is an objective weighting method.", "tf", True),
    ("VIKOR focuses on compromise ranking.", "tf", True),
    ("DEMATEL is mainly used for cause-and-effect analysis.", "tf", True),

    # MCQ A-D
    ("Which method is the simplest weighted ranking method?", "mcq", "SAW",
     ["TOPSIS", "SAW", "DEMATEL", "CRITIC"]),

    ("Which method uses Positive Ideal Solution and Negative Ideal Solution?", "mcq", "TOPSIS",
     ["AHP", "VIKOR", "TOPSIS", "SAW"]),

    ("Which method uses pairwise comparison?", "mcq", "AHP",
     ["CRITIC", "AHP", "TOPSIS", "DEMATEL"]),

    ("Which method uses standard deviation and correlation to determine weights?", "mcq", "CRITIC",
     ["VIKOR", "SAW", "CRITIC", "AHP"]),

    ("Which method uses S, R, and Q values?", "mcq", "VIKOR",
     ["DEMATEL", "TOPSIS", "AHP", "VIKOR"]),

    ("Which method is suitable for cause-effect relationships?", "mcq", "DEMATEL",
     ["SAW", "DEMATEL", "CRITIC", "TOPSIS"]),

    ("In AHP, CR refers to:", "mcq", "Consistency Ratio",
     ["Criteria Ranking", "Consistency Ratio", "Correlation Result", "Cost Ratio"]),

    ("In TOPSIS, CC refers to:", "mcq", "Closeness Coefficient",
     ["Criteria Coefficient", "Closeness Coefficient", "Consistency Check", "Cost Calculation"]),

    ("In DEMATEL, D + R represents:", "mcq", "Prominence",
     ["Regret", "Utility", "Prominence", "Consistency"]),

    ("In VIKOR, the best alternative usually has the:", "mcq", "Lowest Q value",
     ["Highest cost value", "Lowest Q value", "Highest CR value", "Lowest weight value"]),
]

# ==========================================================
# RANDOMIZE QUESTIONS ONCE PER SESSION
# ==========================================================
if "quiz_questions" not in st.session_state:
    random.shuffle(questions)
    st.session_state.quiz_questions = questions

questions = st.session_state.quiz_questions

# ==========================================================
# QUIZ INSTRUCTION
# ==========================================================
st.markdown("""
<div style="
    background:linear-gradient(135deg,#101B3D,#241047);
    padding:28px;
    border-radius:24px;
    color:white;
    margin-top:20px;
    margin-bottom:25px;
    border:1px solid rgba(255,255,255,0.18);
    box-shadow:0 16px 45px rgba(0,0,0,0.25);
">
<h2 style="margin-top:0;">MCDM Assessment Quiz</h2>
<p style="font-size:18px;line-height:1.7;">
This assessment contains <b>20 questions</b>: 
<b>10 True/False questions</b> and <b>10 Multiple Choice questions</b>.
Please answer all questions before submitting.
</p>
</div>
""", unsafe_allow_html=True)

answers = []

# ==========================================================
# DISPLAY QUESTIONS
# ==========================================================
for i, q in enumerate(questions, 1):
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,#18254F,#2E185C);
            padding:22px;
            border-radius:20px;
            border:1px solid rgba(255,255,255,0.15);
            margin-top:18px;
            margin-bottom:10px;
            color:white;
            box-shadow:0 12px 35px rgba(0,0,0,0.22);
        ">
            <h3 style="margin:0;">Q{i}. {q[0]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if q[1] == "tf":
        answers.append(
            st.radio(
                "Choose one",
                [True, False],
                format_func=lambda x: "True" if x else "False",
                key=f"q{i}",
                horizontal=True
            )
        )

    elif q[1] == "mcq":
        options = q[3].copy()

        if f"options_{i}" not in st.session_state:
            random.shuffle(options)
            st.session_state[f"options_{i}"] = options

        options = st.session_state[f"options_{i}"]
        labelled_options = [
            f"{chr(65+j)}. {opt}" for j, opt in enumerate(options)
        ]

        selected = st.radio(
            "Choose one",
            labelled_options,
            key=f"q{i}"
        )

        selected_answer = selected.split(". ", 1)[1]
        answers.append(selected_answer)

# ==========================================================
# SUBMIT QUIZ
# ==========================================================
st.markdown("---")

if st.button("Submit Quiz"):
    if not name or not student_id:
        st.error("Please fill in Full Name and Student ID before submitting.")
    else:
        correct = 0
        review_rows = []

        for i, (ans, q) in enumerate(zip(answers, questions), 1):
            is_correct = ans == q[2]
            correct += int(is_correct)

            review_rows.append({
                "Question": f"Q{i}",
                "Your Answer": ans,
                "Correct Answer": q[2],
                "Status": "Correct" if is_correct else "Incorrect"
            })

        total = len(questions)
        score = round(correct / total * 100, 2)

        row = {
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "name": name,
            "student_id": student_id,
            "email": email,
            "score": score,
            "correct": correct,
            "total": total
        }

        os.makedirs("data", exist_ok=True)

        if os.path.exists(RESULT):
            df = pd.read_csv(RESULT)
        else:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(RESULT, index=False)

        st.success(f"Your score: {score}% ({correct}/{total})")

        st.subheader("Answer Review")
        st.dataframe(
            pd.DataFrame(review_rows),
            use_container_width=True,
            hide_index=True
        )

# ==========================================================
# CHECK MARKS
# ==========================================================
st.markdown("---")
st.subheader("Check Your Marks")

check = st.text_input("Enter your Student ID to check marks")

if st.button("Check Marks"):
    if os.path.exists(RESULT):
        df = pd.read_csv(RESULT)
        out = df[df["student_id"].astype(str) == check]

        if len(out):
            st.dataframe(
                out.sort_values("timestamp", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No record found for this Student ID.")
    else:
        st.warning("No marks have been submitted yet.")
