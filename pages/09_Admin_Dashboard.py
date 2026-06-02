import streamlit as st
import pandas as pd
import os
from style import apply_style, hero, card

st.set_page_config(page_title="Marks Dashboard", page_icon="🔐", layout="wide")
apply_style()

RESULT = "data/results.csv"
PASSWORD = "ZAHARI"

hero(
    "09 | Marks Dashboard",
    "Restricted marks dashboard for instructor use only."
)

# ==========================================================
# PASSWORD PROTECTION
# ==========================================================
if "marks_access" not in st.session_state:
    st.session_state.marks_access = False

if not st.session_state.marks_access:
    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#111827,#312E81);
        padding:30px;
        border-radius:24px;
        color:white;
        margin-top:25px;
        margin-bottom:25px;
        box-shadow:0 18px 45px rgba(0,0,0,0.25);
    ">
        <h2 style="margin-top:0;">🔐 Instructor Access Required</h2>
        <p style="font-size:17px;line-height:1.7;">
        This page is restricted. Please enter the instructor password to view,
        download, or replace student marks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password == PASSWORD:
            st.session_state.marks_access = True
            st.success("Access granted.")
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()

# ==========================================================
# DASHBOARD CONTENT
# ==========================================================
os.makedirs("data", exist_ok=True)

if os.path.exists(RESULT):
    df = pd.read_csv(RESULT)
else:
    df = pd.DataFrame(
        columns=[
            "timestamp",
            "name",
            "student_id",
            "email",
            "score",
            "correct",
            "total"
        ]
    )

st.success("Instructor access granted.")

# ==========================================================
# KPI SUMMARY
# ==========================================================
st.subheader("Assessment Summary")

if len(df) > 0:
    total_submissions = len(df)
    unique_students = df["student_id"].astype(str).nunique()
    average_score = round(df["score"].mean(), 2)
    highest_score = round(df["score"].max(), 2)
else:
    total_submissions = 0
    unique_students = 0
    average_score = 0
    highest_score = 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Submissions", total_submissions)

with c2:
    st.metric("Unique Students", unique_students)

with c3:
    st.metric("Average Score", f"{average_score}%")

with c4:
    st.metric("Highest Score", f"{highest_score}%")

# ==========================================================
# CURRENT MARKS
# ==========================================================
st.subheader("Current Marks")

st.dataframe(
    df.sort_values("timestamp", ascending=False) if len(df) else df,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇️ Download Marks CSV",
    df.to_csv(index=False),
    "mcdm_marks.csv",
    "text/csv"
)

# ==========================================================
# STUDENT SEARCH
# ==========================================================
st.markdown("---")
st.subheader("Search Student Marks")

search_id = st.text_input("Search by Student ID / Matric No")

if search_id:
    filtered = df[df["student_id"].astype(str).str.contains(search_id, case=False, na=False)]

    if len(filtered):
        st.dataframe(
            filtered.sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No matching student record found.")

# ==========================================================
# UPLOAD MARKS FILE
# ==========================================================
st.markdown("---")

card(
    "Upload Marks File",
    """
    <p>
    Upload a CSV file only if you want to replace the current marks file.
    The uploaded file must contain the required columns:
    timestamp, name, student_id, email, score, correct, and total.
    </p>
    """,
    "blue"
)

upload = st.file_uploader(
    "Upload marks CSV to replace current records",
    type=["csv"]
)

if upload is not None:
    new = pd.read_csv(upload)

    required = {
        "timestamp",
        "name",
        "student_id",
        "email",
        "score",
        "correct",
        "total"
    }

    if required.issubset(set(new.columns)):
        st.warning("This will replace the current marks file.")

        if st.button("Confirm Replace Marks File"):
            new.to_csv(RESULT, index=False)
            st.success("Marks uploaded successfully. Refresh page to view updated records.")
    else:
        st.error(
            "Uploaded CSV must include: timestamp, name, student_id, email, score, correct, and total."
        )

# ==========================================================
# CLEAR MARKS OPTION
# ==========================================================
st.markdown("---")
st.subheader("Danger Zone")

with st.expander("Clear all marks"):
    st.warning("This action will permanently clear all current marks from the CSV file.")

    confirm_text = st.text_input("Type CLEAR to confirm")

    if st.button("Clear All Marks"):
        if confirm_text == "CLEAR":
            empty_df = pd.DataFrame(
                columns=[
                    "timestamp",
                    "name",
                    "student_id",
                    "email",
                    "score",
                    "correct",
                    "total"
                ]
            )
            empty_df.to_csv(RESULT, index=False)
            st.success("All marks have been cleared.")
            st.rerun()
        else:
            st.error("Please type CLEAR exactly to confirm.")

# ==========================================================
# LOGOUT
# ==========================================================
st.markdown("---")

if st.button("Logout"):
    st.session_state.marks_access = False
    st.rerun()
