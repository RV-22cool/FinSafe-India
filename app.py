import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

def generate_certificate(name, score):
    img = Image.new('RGB', (1000, 700), color=(245, 250, 255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    draw.rectangle([(20, 20), (980, 680)], outline="black", width=3)

    draw.text((380, 80), "CERTIFICATE", fill="black", font=font)
    draw.text((300, 180), "This is to certify that", fill="black", font=font)
    draw.text((380, 260), str(name), fill="blue", font=font)
    draw.text((200, 340), "has successfully completed the FinSafe Quiz", fill="black", font=font)
    draw.text((400, 420), f"Score: {score}", fill="green", font=font)
    draw.text((300, 550), "FinSafe India", fill="gray", font=font)

    return img

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FinSafe India",
    page_icon="🏦",
    layout="centered"
)

# ---------------- LOAD CSS ----------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- GOOGLE SHEETS CONNECTION ----------------
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

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "score" not in st.session_state:
    st.session_state.score = 0

# =========================================================
# PAGE 1 - REGISTRATION
# =========================================================

if st.session_state.page == 1:

    st.title("🏦 FinSafe India")
    st.subheader("Financial Literacy & Cyber Fraud Awareness Quiz")

    st.info(
        "Test your awareness about digital payments, cyber safety, "
        "online frauds, and smart financial habits."
    )

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

    if st.button("🚀 Start Quiz"):

        if name == "" or mobile == "" or email == "":
            st.warning("Please fill all details before proceeding.")

        else:
            st.session_state.name = name
            st.session_state.mobile = mobile
            st.session_state.email = email
            st.session_state.education = education

            st.session_state.page = 2
            st.rerun()

# =========================================================
# PAGE 2 - QUIZ
# =========================================================

elif st.session_state.page == 2:

    st.title("🧠 FinSafe Awareness Quiz")

    st.progress(0.5)

    score = 0

    # -----------------------------------------------------
    # SECTION 1 - MCQs
    # -----------------------------------------------------

    st.header("📘 Section 1: Multiple Choice Questions")

    q1 = st.radio(
        "1. What does OTP stand for?",
        [
            "One Time Password",
            "Online Transaction Process",
            "Official Transfer Password"
        ]
    )

    if q1 == "One Time Password":
        score += 1

    q2 = st.radio(
        "2. Which organization regulates banks in India?",
        [
            "SEBI",
            "RBI",
            "IRCTC"
        ]
    )

    if q2 == "RBI":
        score += 1

    q3 = st.radio(
        "3. Which of the following passwords is strongest?",
        [
            "india123",
            "password@123",
            "R@8mL#29x!"
        ]
    )

    if q3 == "R@8mL#29x!":
        score += 1

    q4 = st.radio(
        "4. What should you do if you receive a suspicious banking link?",
        [
            "Click immediately",
            "Ignore/report it",
            "Forward to friends"
        ]
    )

    if q4 == "Ignore/report it":
        score += 1

    q5 = st.radio(
        "5. UPI PIN should be shared with:",
        [
            "Nobody",
            "Bank manager",
            "Friends"
        ]
    )

    if q5 == "Nobody":
        score += 1

    q6 = st.radio(
        "6. Which of these is a sign of online fraud?",
        [
            "Urgent request for OTP",
            "Official RBI poster",
            "Bank passbook update"
        ]
    )

    if q6 == "Urgent request for OTP":
        score += 1

    # -----------------------------------------------------
    # SECTION 2 - MATCH THE COLUMNS
    # -----------------------------------------------------

    st.header("🔗 Section 2: Match the Columns")

    st.write("Match Column A with the correct option from Column B.")

    match1 = st.selectbox(
        "7. RBI →",
        [
            "Digital Payment",
            "Central Bank",
            "Security Code"
        ]
    )

    if match1 == "Central Bank":
        score += 1

    match2 = st.selectbox(
        "8. OTP →",
        [
            "Security Code",
            "Shopping App",
            "Bank Branch"
        ]
    )

    if match2 == "Security Code":
        score += 1

    match3 = st.selectbox(
        "9. UPI →",
        [
            "Digital Payment",
            "Insurance Policy",
            "Email Fraud"
        ]
    )

    if match3 == "Digital Payment":
        score += 1

    # -----------------------------------------------------
    # SECTION 3 - JUMBLED WORDS
    # -----------------------------------------------------

    st.header("🔤 Section 3: Jumbled Words")

    q10 = st.text_input(
        "10. Unscramble: PHSIHING"
    )

    if q10.lower() == "phishing":
        score += 1

    q11 = st.text_input(
        "11. Unscramble: RDUAF"
    )

    if q11.lower() == "fraud":
        score += 1

    q12 = st.text_input(
        "12. Unscramble: CEURTSIY"
    )

    if q12.lower() == "security":
        score += 1

    # -----------------------------------------------------
    # SECTION 4 - CONCEPTUAL QUESTIONS
    # -----------------------------------------------------

    st.header("🛡 Section 4: Conceptual Awareness")

    q13 = st.radio(
        "13. A caller says your KYC will expire today unless you share OTP immediately. What should you do?",
        [
            "Share OTP immediately",
            "Disconnect and report fraud",
            "Share only last digits"
        ]
    )

    if q13 == "Disconnect and report fraud":
        score += 1

    q14 = st.radio(
        "14. Why is financial literacy important?",
        [
            "To avoid scams and manage money wisely",
            "Only for bankers",
            "Only for businesses"
        ]
    )

    if q14 == "To avoid scams and manage money wisely":
        score += 1

    # -----------------------------------------------------
    # SECTION 5 - USER RESPONSE
    # -----------------------------------------------------

    st.header("✍ Awareness Response")

    q15 = st.text_area(
        "15. What is one important step you take to stay safe from cyber fraud?"
    )

    if len(q15) > 5:
        score += 1

    # -----------------------------------------------------
    # SUBMIT BUTTON
    # -----------------------------------------------------

    if st.button("✅ Submit Quiz"):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = [
            st.session_state.name,
            st.session_state.mobile,
            st.session_state.email,
            st.session_state.education,
            score,
            timestamp
        ]

        sheet.append_row(data)

        st.session_state.score = score
        st.session_state.page = 3

        st.rerun()

# =========================================================
# PAGE 3 - THANK YOU PAGE
# =========================================================

elif st.session_state.page == 3:

    st.title("🎉 Thank You for Participating!")

    st.success(
        f"Your Score: {st.session_state.score} / 15"
    )
    if st.button("🎓 Generate Certificate"):
       cert_img = generate_certificate(
        st.session_state.name,
        st.session_state.score
    )

    buf = io.BytesIO()
    cert_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        "📥 Download Certificate",
        data=byte_im,
        file_name="FinSafe_Certificate.png",
        mime="image/png"
    )
    

    if st.session_state.score >= 13:

        st.balloons()

        st.success(
            "Excellent awareness! You are highly informed "
            "about cyber safety and financial literacy. 🌟"
        )

    elif st.session_state.score >= 8:

        st.info(
            "Good job! You have decent awareness, "
            "but keep learning about cyber safety."
        )

    else:

        st.warning(
            "You should improve your awareness about "
            "financial literacy and cyber fraud prevention."
        )
        

    st.info(
        "Together we can build a financially aware "
        "and cyber-safe India 🇮🇳"
    )

    if st.button("🔄 Restart Quiz"):

        st.session_state.page = 1
        st.rerun()
