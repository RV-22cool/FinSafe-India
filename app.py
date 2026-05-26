import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="FinSafe India",
    page_icon="🏦",
    layout="centered"
)

# =====================================================
# LOAD CSS
# =====================================================

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS CONNECTION
# =====================================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = st.secrets["gcp_service_account"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

sheet = client.open("FinSafe India Responses").sheet1

# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# =====================================================
# PAGE 1 — REGISTRATION
# =====================================================

if st.session_state.page == 1:

    st.title("🏦 FinSafe India")
    st.subheader("Interactive Financial Literacy & Cyber Safety Activity")

    st.info(
        "Learn about digital safety, fraud awareness, budgeting, "
        "financial planning, and smart money habits."
    )

    with st.container():

        name = st.text_input("👤 Full Name")

        mobile = st.text_input("📱 Mobile Number")

        email = st.text_input("📧 Email Address")

        education = st.selectbox(
            "🎓 Education Level",
            [
                "School Student",
                "College Student",
                "Graduate",
                "Professional",
                "Other"
            ]
        )

    st.progress(10)

    if st.button("🚀 Start Activity"):

        if name == "" or mobile == "" or email == "":

            st.warning("Please fill all details.")

        else:

            st.session_state.name = name
            st.session_state.mobile = mobile
            st.session_state.email = email
            st.session_state.education = education

            st.session_state.page = 2

            st.rerun()

# =====================================================
# PAGE 2 — SPOT THE SCAM
# =====================================================

elif st.session_state.page == 2:

    st.title("🕵️ Spot the Scam")

    st.progress(30)

    scam_score = 0

    st.markdown("### 📩 Case 1")

    st.warning(
        "Your bank account will be blocked. "
        "Click this link and update your KYC immediately."
    )

    c1 = st.radio(
        "Is this fraud?",
        ["Yes", "No"],
        key="c1"
    )

    red1 = st.multiselect(
        "Select red flags",
        [
            "Urgent pressure",
            "Unknown link",
            "KYC threat",
            "Official RBI notice"
        ]
    )

    action1 = st.text_area(
        "What should you do?",
        key="action1"
    )

    if c1:
        scam_score += 1

    if len(red1) >= 2:
        scam_score += 1

    if len(action1) > 5:
        scam_score += 1

    # -------------------------------------------------

    st.markdown("### ☎️ Case 2")

    st.warning(
        "You won ₹25 lakh lottery. "
        "Pay ₹5,000 processing fee to claim."
    )

    c2 = st.radio(
        "Is this fraud?",
        ["Yes", "No"],
        key="c2"
    )

    red2 = st.multiselect(
        "Select red flags",
        [
            "Lottery scam",
            "Advance payment request",
            "Unknown caller",
            "Official RBI message"
        ]
    )

    action2 = st.text_area(
        "What should you do?",
        key="action2"
    )

    if c2:
        scam_score += 1

    if len(red2) >= 2:
        scam_score += 1

    if len(action2) > 5:
        scam_score += 1

    # -------------------------------------------------

    if st.button("➡️ Next Section"):

        st.session_state.scam_score = scam_score
        st.session_state.page = 3

        st.rerun()

# =====================================================
# PAGE 3 — BUDGET CHALLENGE
# =====================================================

elif st.session_state.page == 3:

    st.title("💰 Budget Challenge")

    st.progress(50)

    budget_score = 0

    st.info(
        "You earn ₹15,000/month. "
        "Allocate your expenses wisely."
    )

    rent = st.number_input("🏠 Rent / Stay", min_value=0)

    food = st.number_input("🍛 Food", min_value=0)

    entertainment = st.number_input("🎬 Entertainment", min_value=0)

    savings = st.number_input("💸 Savings", min_value=0)

    emergency = st.number_input("🚨 Emergency Fund", min_value=0)

    total = (
        rent
        + food
        + entertainment
        + savings
        + emergency
    )

    st.write(f"### Total Used: ₹{total}")

    if total > 15000:

        st.error("⚠️ Budget exceeded!")

    else:

        st.success("✅ Budget managed well!")

    if savings >= 3000:
        budget_score += 2
        st.success("🏅 Smart Saver Badge Earned!")

    goal = st.text_input(
        "🎯 Write one financial goal"
    )

    if len(goal) > 3:
        budget_score += 1

    if st.button("➡️ Continue"):

        st.session_state.budget_score = budget_score
        st.session_state.page = 4

        st.rerun()

# =====================================================
# PAGE 4 — AWARENESS ACTIVITIES
# =====================================================

elif st.session_state.page == 4:

    st.title("🎯 Financial Awareness Activities")

    st.progress(70)

    awareness_score = 0

    # -------------------------------------------------
    # NEED VS WANT
    # -------------------------------------------------

    st.subheader("🛒 Need vs Want")

    rent_q = st.radio(
        "Rent",
        ["Need", "Want"],
        key="rent_q"
    )

    iphone_q = st.radio(
        "New iPhone",
        ["Need", "Want"],
        key="iphone_q"
    )

    groceries_q = st.radio(
        "Groceries",
        ["Need", "Want"],
        key="groceries_q"
    )

    if rent_q:
        awareness_score += 1

    if iphone_q:
        awareness_score += 1

    if groceries_q:
        awareness_score += 1

    # -------------------------------------------------
    # RIGHT OR WRONG
    # -------------------------------------------------

    st.subheader("✅ Right or Wrong")

    otp_q = st.radio(
        "Sharing OTP is safe",
        ["Right", "Wrong"],
        key="otp_q"
    )

    saving_q = st.radio(
        "Saving money is important",
        ["Right", "Wrong"],
        key="saving_q"
    )

    invest_q = st.radio(
        "Investing early is beneficial",
        ["Right", "Wrong"],
        key="invest_q"
    )

    if otp_q:
        awareness_score += 1

    if saving_q:
        awareness_score += 1

    if invest_q:
        awareness_score += 1

    # -------------------------------------------------
    # MATCH THE PAIR
    # -------------------------------------------------

    st.subheader("🔗 Match the Pair")

    sip = st.selectbox(
        "SIP →",
        [
            "Complaint System",
            "Regular Investment",
            "Emergency Expenses"
        ]
    )

    sebi = st.selectbox(
        "SEBI →",
        [
            "Market Regulator",
            "Insurance",
            "UPI Service"
        ]
    )

    if sip:
        awareness_score += 1

    if sebi:
        awareness_score += 1

    # -------------------------------------------------

    if st.button("➡️ Continue to Final Round"):

        st.session_state.awareness_score = awareness_score
        st.session_state.page = 5

        st.rerun()

# =====================================================
# PAGE 5 — RAPID FIRE
# =====================================================

elif st.session_state.page == 5:

    st.title("⚡ Rapid Fire Round")

    st.progress(90)

    rapid_score = 0

    q1 = st.text_input(
        "1. App used for quick payments"
    )

    q2 = st.text_input(
        "2. Fraud using fake links"
    )

    q3 = st.text_input(
        "3. Money saved for future"
    )

    reflection = st.text_area(
        "🧠 What is one step you take to stay safe online?"
    )

    if len(q1) > 1:
        rapid_score += 1

    if len(q2) > 1:
        rapid_score += 1

    if len(q3) > 1:
        rapid_score += 1

    if len(reflection) > 5:
        rapid_score += 2

    # =================================================
    # SUBMIT BUTTON
    # =================================================

    if st.button("✅ Submit Activity"):

        final_score = (
            st.session_state.scam_score
            + st.session_state.budget_score
            + st.session_state.awareness_score
            + rapid_score
        )

        st.session_state.final_score = final_score

        # =============================================
        # TIMESTAMP
        # =============================================

        ist = timezone(timedelta(hours=5, minutes=30))

        timestamp = datetime.now(ist).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # =============================================
        # GOOGLE SHEET DATA
        # =============================================

        data = [
            timestamp,
            st.session_state.name,
            st.session_state.mobile,
            st.session_state.email,
            st.session_state.education,
            st.session_state.scam_score,
            st.session_state.budget_score,
            st.session_state.awareness_score,
            rapid_score,
            final_score,
            reflection
        ]

        sheet.append_row(data)

        st.session_state.page = 6

        st.rerun()

# =====================================================
# PAGE 6 — FINAL RESULT
# =====================================================

elif st.session_state.page == 6:

    st.title("🎉 Activity Completed!")

    st.balloons()

    st.success(
        f"Your Participation Score: "
        f"{st.session_state.final_score}"
    )

    score = st.session_state.final_score

    if score >= 15:

        st.success(
            "🏅 Cyber Safety Champion!"
        )

        st.info(
            "Excellent awareness about "
            "financial safety and fraud prevention."
        )

    elif score >= 10:

        st.info(
            "🎯 Smart Financial Learner!"
        )

        st.write(
            "You have good awareness and practical understanding."
        )

    else:

        st.warning(
            "📘 Finance Explorer!"
        )

        st.write(
            "Keep learning about digital safety and money management."
        )

    st.info(
        "Together we can build a financially aware "
        "and cyber-safe India 🇮🇳"
    )

    if st.button("🔄 Restart Activity"):

        st.session_state.page = 1
        st.session_state.final_score = 0

        st.rerun()
