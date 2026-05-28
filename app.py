from pathlib import Path

import streamlit as st

from src.detector import (
    find_suspicious_terms,
    highlight_suspicious_terms,
    load_model,
    predict_message,
    risk_level,
)


st.set_page_config(
    page_title="AI Phishing Email Detector",
    layout="wide",
)


CUSTOM_CSS = """
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    .risk-safe {
        color: #0f7b45;
        font-weight: 700;
    }
    .risk-warning {
        color: #9a6400;
        font-weight: 700;
    }
    .risk-danger {
        color: #b42318;
        font-weight: 700;
    }
    mark {
        background: #ffe08a;
        color: #241a00;
        border-radius: 4px;
        padding: 0.08rem 0.22rem;
    }
    .email-preview {
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 1rem;
        background: #ffffff;
        min-height: 220px;
        line-height: 1.6;
    }
</style>
"""


EXAMPLE_EMAIL = """Subject: Urgent account verification required

Dear customer,

We detected unusual activity on your account. Your account will be suspended unless you verify your password immediately.

Click the secure login link below to update your information:
http://example-security-check.com/login
"""


def read_uploaded_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")


@st.cache_resource
def cached_model():
    return load_model()


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("AI Phishing Email Detector")
st.caption("Machine learning dashboard for detecting suspicious emails and messages.")

try:
    model = cached_model()
except FileNotFoundError as error:
    st.error(str(error))
    st.info("Open a terminal in this project and run: python train_model.py")
    st.stop()

left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.subheader("Analyze an Email")
    uploaded_file = st.file_uploader("Upload a .txt email file", type=["txt"])
    uploaded_text = read_uploaded_file(uploaded_file)

    message = st.text_area(
        "Email or message text",
        value=uploaded_text or EXAMPLE_EMAIL,
        height=330,
    )

    analyze = st.button("Analyze Message", type="primary", use_container_width=True)

with right:
    st.subheader("Prediction")

    if analyze or message.strip():
        result = predict_message(model, message)
        probability = result["phishing_probability"]
        level, style = risk_level(probability)
        suspicious_terms = find_suspicious_terms(message)

        st.metric("Phishing Probability", f"{probability * 100:.1f}%")
        st.progress(probability)
        st.markdown(f"Risk Level: <span class='risk-{style}'>{level}</span>", unsafe_allow_html=True)

        if result["label"] == "phishing":
            st.error("This message looks suspicious. Do not click links or share credentials.")
        else:
            st.success("This message appears safer, but still review links and sender details.")

        st.write("Suspicious terms found:")
        if suspicious_terms:
            st.write(", ".join(sorted(set(suspicious_terms))))
        else:
            st.write("No common suspicious terms found.")

st.divider()

preview_col, tips_col = st.columns([1.2, 0.8], gap="large")

with preview_col:
    st.subheader("Highlighted Email")
    st.markdown(
        f"<div class='email-preview'>{highlight_suspicious_terms(message)}</div>",
        unsafe_allow_html=True,
    )

with tips_col:
    st.subheader("Security Checklist")
    st.checkbox("Sender address matches the real organization")
    st.checkbox("Links point to official domains")
    st.checkbox("No request for passwords or one-time codes")
    st.checkbox("No urgent threat or pressure tactic")
    st.checkbox("Attachments are expected and verified")

    st.info(
        "Phishing models are decision-support tools. Always combine the score with sender, link, and attachment checks."
    )

st.caption(f"Model file: {Path('models/phishing_detector.joblib')}")
