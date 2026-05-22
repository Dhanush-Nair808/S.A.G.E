import streamlit as st
import requests
import os

os.makedirs(".streamlit", exist_ok=True)

with open(".streamlit/config.toml", "w") as f:
    f.write("""
[theme]
base="light"

primaryColor="#FF9900"

backgroundColor="#EAEDED"

secondaryBackgroundColor="#FFFFFF"

textColor="#111111"

font="sans serif"
""")

st.set_page_config(layout="wide", page_title="S.A.G.E - Support And Guidance Expert")

# ====================== THEME (clean white) ======================
THEME_CSS = """
<style>

/* =========================================================
   AMAZON INSPIRED THEME
========================================================= */

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #EAEDED !important;
    color: #111111 !important;
    font-family: "Amazon Ember", "Segoe UI", sans-serif !important;
}

/* Hide Streamlit defaults */
[data-testid="stSidebarNav"] {
    display: none !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: #131921 !important;
    border-right: 1px solid #232F3E !important;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] > div {
    padding-top: 1rem !important;
}

/* =========================================================
   AMAZON BRANDING
========================================================= */

.sage-header-text {
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #131921 !important;
    letter-spacing: -1px !important;
    margin-bottom: 2px !important;
}

.sage-logo-gold {
    color: #FF9900 !important;
}

.sage-sub {
    font-size: 13px !important;
    color: #565959 !important;
    margin-bottom: 24px !important;
}

/* =========================================================
   MAIN CARD
========================================================= */

.sage-card {
    background-color: #FFFFFF !important;

    padding: 30px !important;

    border-radius: 12px !important;

    border: 1px solid #D5D9D9 !important;

    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;

    margin-bottom: 20px !important;
}

/* =========================================================
   SIDEBAR NAV BUTTONS
========================================================= */

section[data-testid="stSidebar"] div.stButton > button {
    width: 100% !important;

    text-align: left !important;

    padding: 12px 16px !important;

    background: #232F3E !important;

    color: #FFFFFF !important;

    border: 1px solid #37475A !important;

    border-radius: 8px !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    margin-bottom: 10px !important;

    transition: all 0.2s ease !important;
}

/* Hover */
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #37475A !important;

    border-color: #FF9900 !important;

    transform: translateX(4px) !important;
}

/* Active */
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #FF9900 !important;

    color: #111111 !important;

    border-color: #FF9900 !important;

    font-weight: 700 !important;
}

/* =========================================================
   CENTER NAV
========================================================= */

.center-nav-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;

    min-height: 45vh;
}

/* =========================================================
   MINI BADGES
========================================================= */

.mini-badge-container {
    display: flex;
    gap: 16px;
    margin: 14px 0;
}

.mini-badge {
    flex: 1;

    background-color: #FFFFFF !important;

    border-left: 5px solid #FF9900 !important;

    padding: 14px !important;

    border-radius: 8px !important;

    border: 1px solid #D5D9D9 !important;
}

.mini-badge-blue {
    border-left-color: #146EB4 !important;
}

.mini-label {
    font-size: 10px !important;

    text-transform: uppercase !important;

    color: #565959 !important;

    font-weight: 700 !important;

    margin-bottom: 4px !important;

    letter-spacing: 0.5px;
}

.mini-value {
    font-size: 18px !important;

    font-weight: 800 !important;

    color: #111111 !important;
}

/* =========================================================
   BADGES
========================================================= */

.sage-star-badge {
    background: #FFF3E0 !important;

    border: 1px solid #FF9900 !important;

    color: #B12704 !important;

    font-size: 10px !important;

    font-weight: 700 !important;

    padding: 4px 10px !important;

    border-radius: 5px !important;

    display: inline-block !important;

    text-transform: uppercase !important;

    letter-spacing: 0.5px;
}

/* =========================================================
   ANALYTICS CARDS
========================================================= */

.analytics-card {
    background: #FFFFFF;

    border: 1px solid #D5D9D9;

    border-radius: 10px;

    padding: 22px;

    text-align: center;

    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.analytics-card .ac-label {
    font-size: 11px;

    text-transform: uppercase;

    color: #565959;

    font-weight: 700;

    letter-spacing: 0.5px;
}

.analytics-card .ac-value {
    font-size: 38px;

    font-weight: 800;

    color: #131921;

    margin-top: 6px;
}

/* =========================================================
   INPUTS
========================================================= */

textarea,
input {
    border-radius: 8px !important;

    border: 1px solid #A6A6A6 !important;
}

/* Focus effect */
textarea:focus,
input:focus {
    border-color: #FF9900 !important;

    box-shadow: 0 0 0 2px rgba(255,153,0,0.25) !important;
}

/* =========================================================
   STREAMLIT BUTTONS
========================================================= */

.stButton > button {
    border-radius: 8px !important;
}

/* =========================================================
   EXPANDERS
========================================================= */

.streamlit-expanderHeader {
    font-weight: 700 !important;

    color: #131921 !important;
}

/* =========================================================
   SUCCESS / INFO / ERROR
========================================================= */

.stAlert {
    border-radius: 10px !important;
}

/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #879596;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #5F6B6D;
}

</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:8000"

# ---- Session state init ----
for key, default in [
    ("logged_in", False), ("username", ""), ("menu", "Analytics"),
    ("active_review_id", None), ("active_review_text", ""), ("active_category", ""),
    ("active_sentiment", ""), ("active_reply", ""), ("feedback_submitted", False),
    ("show_disappointment_form", False), ("chat_history", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ====================== BRAND HEADER ======================
st.markdown("""
<div class="sage-header-text">S.A.G.E<span class="sage-logo-gold">.</span></div>
<div class="sage-sub">Support And Guidance Expert &bull; Feedback &amp; Retraining Console</div>
""", unsafe_allow_html=True)

# ====================== AUTH WALL ======================
if not st.session_state.logged_in:
    st.sidebar.markdown("""
    <div style='text-align:center;padding:25px 0;'>
        <div style='background:#F59E0B;color:#fff;font-weight:900;padding:6px 18px;
                    border-radius:6px;font-size:24px;display:inline-block;'>S.A.G.E.</div>
        <div style='font-size:13px;margin-top:12px;font-weight:600;color:#374151;'>Control Center</div>
        <p style='font-size:11px;color:#9CA3AF;margin-top:4px;'>Sign in to unlock dashboards.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])

    with tab1:
        st.subheader("Sign In")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In", type="primary"):
            if username and password:
                with st.spinner("Authenticating..."):
                    try:
                        res = requests.post(f"{BASE_URL}/login",
                                            json={"username": username, "password": password})
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.logged_in = True
                            st.session_state.username = data.get("username", username)
                            st.session_state.menu = "Analytics"
                            st.rerun()
                        else:
                            try:
                                err = res.json().get("detail", res.text[:200])
                            except Exception:
                                err = f"Status {res.status_code}"
                            st.error(f"❌ {err}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

    with tab2:
        st.subheader("Create Account")
        new_username = st.text_input("Choose Username", key="reg_user")
        new_email = st.text_input("Email Address", key="reg_email")
        new_password = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        if st.button("Create Account", type="primary"):
            if not new_username or not new_email or not new_password:
                st.error("All fields are required!")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating profile..."):
                    try:
                        res = requests.post(f"{BASE_URL}/register",
                                            json={"username": new_username,
                                                  "email": new_email,
                                                  "password": new_password})
                        if res.status_code == 200:
                            st.success("✅ Account created! Please sign in.")
                        else:
                            try:
                                err = res.json().get("detail", res.text)
                            except Exception:
                                err = res.text[:300]
                            st.error(f"❌ {err}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

# ====================== LOGGED-IN PORTAL ======================
else:
    # ---------- SIDEBAR ----------
    st.sidebar.markdown(f"""
    <div style='text-align:center;padding:14px 0 10px;'>
        <div style='background:#F59E0B;color:#fff;font-weight:900;padding:5px 16px;
                    border-radius:6px;font-size:22px;display:inline-block;'>S.A.G.E.</div>
        <p style='font-size:10px;margin-top:6px;font-weight:700;letter-spacing:2px;
                  color:#6B7280;text-transform:uppercase;'>Portal Active</p>
    </div>
    <div style='padding:8px 14px;border-radius:6px;margin-bottom:16px;
                border:1px solid #E5E7EB;border-left:3px solid #F59E0B;
                background:#FFFBEB;text-align:center;'>
        <span style='font-size:12px;color:#374151;'>Welcome, <b>{st.session_state.username}</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("##### 🧭 Navigation")

    NAV = [
        
        ("📝 Submit Review",  "Submit Review"),
        ("📋 Public Reviews", "Public Reviews"),
        ("💬 S.A.G.E Chat",  "Chatbot"),
        ("📊 Analytics",      "Analytics"),
    ]
    for label, key in NAV:
        btn_type = "primary" if st.session_state.menu == key else "secondary"
        if st.sidebar.button(label, use_container_width=True, type=btn_type, key=f"nav_{key}"):
            st.session_state.menu = key
            st.rerun()

    # Past reviews in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 📦 My Past Reviews")
    try:
        ur_res = requests.get(f"{BASE_URL}/user-reviews/{st.session_state.username}")
        if ur_res.status_code == 200:
            user_reviews = ur_res.json()
            if user_reviews:
                for ur in user_reviews[:5]:
                    icon = "👍" if ur.get("satisfaction") == "YES" else ("👎" if ur.get("satisfaction") == "NO" else "⏳")
                    with st.sidebar.expander(f"{icon} {ur.get('category')} ({ur.get('sentiment')})"):
                        st.markdown(
                            f"<span style='font-size:11px;'><b>Review:</b> <i>{ur.get('review','')[:80]}…</i></span>",
                            unsafe_allow_html=True)
                        st.markdown(
                            f"<span style='font-size:11px;color:#B45309;'><b>S.A.G.E:</b> <i>{ur.get('reply','')[:80]}…</i></span>",
                            unsafe_allow_html=True)
            else:
                st.sidebar.caption("No reviews yet.")
    except Exception as e:
        st.sidebar.caption(f"Could not load reviews: {e}")

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        for k in ["logged_in", "username", "active_review_id", "active_review_text",
                  "active_category", "active_sentiment", "active_reply",
                  "feedback_submitted", "show_disappointment_form", "chat_history"]:
            st.session_state[k] = False if k == "logged_in" else ([] if k == "chat_history" else ("" if k != "active_review_id" else None))
        st.rerun()

    # ---------- MAIN CONTENT ----------
    st.markdown("<div class='sage-card'>", unsafe_allow_html=True)

    # ---- ANALYTICS ----
    if st.session_state.menu == "Analytics":
        st.markdown("<h3 style='margin-top:0;'>📊 ML Analytics</h3>", unsafe_allow_html=True)
        st.write("Live statistics derived from all submitted reviews and closed-loop feedback.")
        try:
            res = requests.get(f"{BASE_URL}/public-reviews")
            data = res.json()
            total = len(data)
            satisfied = sum(1 for r in data if r.get("satisfaction") == "YES")
            dissatisfied = sum(1 for r in data if r.get("satisfaction") == "NO")
            pending = total - satisfied - dissatisfied

            # Category breakdown
            from collections import Counter
            categories = Counter(r.get("category", "Unknown") for r in data)
            sentiments = Counter(r.get("sentiment", "Unknown") for r in data)

            c1, c2, c3, c4 = st.columns(4)
            metrics = [
                (c1, "Total Reviews", total, "#3B82F6"),
                (c2, "✅ Satisfied", satisfied, "#10B981"),
                (c3, "❌ Dissatisfied", dissatisfied, "#EF4444"),
                (c4, "⏳ Pending", pending, "#F59E0B"),
            ]
            for col, label, val, color in metrics:
                col.markdown(f"""
                <div class='analytics-card'>
                    <div class='ac-label'>{label}</div>
                    <div class='ac-value' style='color:{color};'>{val}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("---")
            col_cat, col_sent = st.columns(2)
            with col_cat:
                st.markdown("**Category Breakdown**")
                for cat, count in categories.most_common():
                    pct = int(count / total * 100) if total else 0
                    st.markdown(f"`{cat}` — **{count}** ({pct}%)")
                    st.progress(pct / 100)
            with col_sent:
                st.markdown("**Sentiment Breakdown**")
                for sent, count in sentiments.most_common():
                    pct = int(count / total * 100) if total else 0
                    st.markdown(f"`{sent}` — **{count}** ({pct}%)")
                    st.progress(pct / 100)
        except Exception as e:
            st.error(f"Error loading analytics: {e}")

    # ---- SUBMIT REVIEW ----
    elif st.session_state.menu == "Submit Review":
        st.markdown("<h3 style='margin-top:0;'>📝 Submit Product Review</h3>", unsafe_allow_html=True)
        

        review = st.text_area("Write review details below:", height=130,
                               placeholder="Type review content here…")

        if st.button("Analyze & Generate Response", type="primary"):
            if review.strip():
                with st.spinner("Analyzing with ML Engine…"):
                    try:
                        res = requests.post(f"{BASE_URL}/submit-review",
                                            json={"review": review,
                                                  "username": st.session_state.username})
                        if res.status_code == 200:
                            d = res.json()
                            st.session_state.active_review_id = d.get("id")
                            st.session_state.active_review_text = review
                            st.session_state.active_category = d.get("category", "")
                            st.session_state.active_sentiment = d.get("sentiment", "")
                            st.session_state.active_reply = d.get("reply", "")
                            st.session_state.feedback_submitted = False
                            st.session_state.show_disappointment_form = False
                        else:
                            try:
                                err = res.json().get("detail", res.text[:200])
                            except Exception:
                                err = res.text[:200]
                            st.error(f"Error: {err}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
            else:
                st.warning("Please enter a review before submitting.")

        if st.session_state.active_review_id is not None:
            st.markdown("---")
            st.markdown("<div class='sage-star-badge'>S.A.G.E Classifier Result</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="mini-badge-container">
                <div class="mini-badge">
                    <div class="mini-label">Predicted Category</div>
                    <div class="mini-value">{st.session_state.active_category}</div>
                </div>
                <div class="mini-badge mini-badge-blue">
                    <div class="mini-label">Detected Sentiment</div>
                    <div class="mini-value">{st.session_state.active_sentiment}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h5 style='margin-bottom:6px;'>S.A.G.E Response:</h5>", unsafe_allow_html=True)
            st.info(st.session_state.active_reply)

            if not st.session_state.feedback_submitted:
                st.markdown("#### Are you satisfied with S.A.G.E's response?")
                fc1, fc2, _ = st.columns([1, 1, 4])
                with fc1:
                    if st.button("👍 Yes", key="thumbs_up"):
                        try:
                            res = requests.post(f"{BASE_URL}/feedback",
                                                json={"review_id": st.session_state.active_review_id,
                                                      "satisfaction": "YES"})
                            if res.status_code == 200:
                                st.session_state.feedback_submitted = True
                                st.rerun()
                            else:
                                st.error("Failed to submit feedback.")
                        except Exception as e:
                            st.error(f"Error: {e}")
                with fc2:
                    if st.button("👎 No", key="thumbs_down"):
                        st.session_state.show_disappointment_form = True
                        st.rerun()

                if st.session_state.show_disappointment_form:
                    st.markdown("---")
                    st.markdown("<h5 style='color:#B91C1C;'>🔍 Help us improve — why are you dissatisfied?</h5>",
                                unsafe_allow_html=True)
                    reason = st.selectbox("Primary reason:",
                                          ["Incorrect Category", "Incorrect Sentiment", "Unhelpful LLM Reply"])
                    corrected_cat = None
                    if reason == "Incorrect Category":
                        corrected_cat = st.selectbox(
                            "Correct category:",
                            ["account_access", "billing", "bug_report", "refund_request", "shipping_delivery"])
                    if st.button("Submit & Retrain", type="primary"):
                        try:
                            res = requests.post(f"{BASE_URL}/feedback",
                                                json={"review_id": st.session_state.active_review_id,
                                                      "satisfaction": "NO",
                                                      "reason": reason,
                                                      "corrected_category": corrected_cat})
                            if res.status_code == 200:
                                st.session_state.feedback_submitted = True
                                st.session_state.show_disappointment_form = False
                                st.session_state.active_review_id = None
                                st.success("Feedback recorded & model retrained! 🚀")
                                st.rerun()
                            else:
                                st.error("Failed to submit dissatisfaction.")
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.success("🎉 Feedback recorded! Model fine-tuned in real time.")
                if st.button("Submit New Review"):
                    st.session_state.active_review_id = None
                    st.session_state.feedback_submitted = False
                    st.rerun()

    # ---- PUBLIC REVIEWS ----
    elif st.session_state.menu == "Public Reviews":
        st.markdown("<h3 style='margin-top:0;'>📋 Public Reviews Log</h3>", unsafe_allow_html=True)
        st.write("Browse feedback logs submitted by users, along with satisfaction ratings.")
        try:
            res = requests.get(f"{BASE_URL}/public-reviews")
            reviews = res.json()
            if not reviews:
                st.info("No reviews submitted yet.")
            for r in reviews:
                sat = r.get("satisfaction")
                badge = "👍 Satisfied" if sat == "YES" else ("👎 Dissatisfied" if sat == "NO" else "⏳ Pending")
                with st.expander(f"**{r.get('category','')}** • {r.get('sentiment','')} • {badge}"):
                    st.markdown(f"**Submitted by:** `{r.get('username', 'anonymous')}`")
                    st.markdown(f"**Review:** *{r.get('review','')}*")
                    st.info(r.get("reply", ""))
        except Exception as e:
            st.error(f"Could not load public reviews: {e}")

    # ---- CHATBOT ----
    elif st.session_state.menu == "Chatbot":
        st.markdown("<h3 style='margin-top:0;'>💬 S.A.G.E Chatbot</h3>", unsafe_allow_html=True)
        st.write("Chat with S.A.G.E — powered by Mistral AI. Ask anything about orders, policies, or support.")

        for speaker, msg in st.session_state.chat_history:
            if speaker == "You":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.info(f"🤖 **S.A.G.E:** {msg}")

        user_msg = st.text_input("Type your message:", key="chat_input",
                                  placeholder="e.g. What is your refund policy?")
        if st.button("Send", type="primary"):
            if user_msg.strip():
                st.session_state.chat_history.append(("You", user_msg))
                with st.spinner("S.A.G.E is thinking…"):
                    try:
                        res = requests.post(f"{BASE_URL}/chat",
                                            json={"message": user_msg}, timeout=30)
                        reply = res.json().get("reply", "No response.") if res.status_code == 200 \
                            else f"Backend error {res.status_code}"
                    except Exception as e:
                        reply = f"Connection error: {e}"
                st.session_state.chat_history.append(("S.A.G.E", reply))
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)