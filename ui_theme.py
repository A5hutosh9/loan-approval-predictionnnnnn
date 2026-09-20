import textwrap
import streamlit as st


# ==========================================================
# APPLY GLOBAL THEME
# ==========================================================

def apply_theme():

    st.markdown(
        textwrap.dedent("""
        <style>

        /* =====================================================
           COLORS
        ===================================================== */

        :root {
            --navy: #082746;
            --navy-light: #0d4e8e;
            --blue: #145db5;
            --blue-light: #2378c9;

            --gold: #e4b84d;
            --saffron: #ff7a00;
            --green: #138808;

            --white: #ffffff;
            --background: #eef4f9;

            --text: #153451;
            --text-light: #637890;

            --border: #d5e1ec;

            --success: #117a46;
            --danger: #a5293c;
        }


        /* =====================================================
           MAIN APP
        ===================================================== */

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #f8fbfd 0%,
                    #eef4f8 55%,
                    #e9f0f6 100%
                );

            color: var(--text);
        }


        /* =====================================================
           REMOVE STREAMLIT DEFAULT ELEMENTS
        ===================================================== */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            background: rgba(255,255,255,0.96);
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #062441 0%,
                    #0a3156 52%,
                    #07253f 100%
                );

            border-right:
                1px solid rgba(255,255,255,0.08);
        }


        [data-testid="stSidebar"] * {
            color: #ffffff;
        }


        [data-testid="stSidebar"] hr {
            border-color:
                rgba(255,255,255,0.16);
        }


        /* =====================================================
           SIDEBAR BRAND
        ===================================================== */

        .bank-brand {
            background:
                rgba(255,255,255,0.07);

            border:
                1px solid
                rgba(255,255,255,0.12);

            border-radius:
                18px;

            padding:
                20px 18px;

            margin-bottom:
                18px;

            box-shadow:
                0 10px 30px
                rgba(0,0,0,0.12);
        }


        .bank-brand .logo {
            font-size:
                31px;

            margin-bottom:
                8px;
        }


        .bank-brand .name {
            color:
                #ffffff;

            font-size:
                21px;

            font-weight:
                800;
        }


        .bank-brand .tagline {
            color:
                #cdddec;

            font-size:
                10px;

            text-transform:
                uppercase;

            letter-spacing:
                1.4px;

            margin-top:
                4px;
        }


        /* =====================================================
           INDIAN TRICOLOUR STRIP
        ===================================================== */

        .tricolor {
            width:
                100%;

            height:
                5px;

            border-radius:
                999px;

            margin-top:
                14px;

            background:
                linear-gradient(
                    90deg,
                    #ff7a00 0%,
                    #ff7a00 33.33%,
                    #ffffff 33.33%,
                    #ffffff 66.66%,
                    #138808 66.66%,
                    #138808 100%
                );
        }


        /* =====================================================
           SIDEBAR BUTTONS
        ===================================================== */

        [data-testid="stSidebar"] .stButton button {

            width:
                100%;

            min-height:
                42px;

            border-radius:
                10px;

            background:
                rgba(255,255,255,0.07);

            border:
                1px solid
                rgba(255,255,255,0.12);

            color:
                #ffffff;

            font-weight:
                600;
        }


        [data-testid="stSidebar"] .stButton button:hover {

            background:
                rgba(255,255,255,0.14);

            transform:
                translateY(-1px);
        }


        /* =====================================================
           HERO
        ===================================================== */

        .hero {

            position:
                relative;

            overflow:
                hidden;

            background:
                linear-gradient(
                    105deg,
                    #082746 0%,
                    #0d4e8e 57%,
                    #2378c9 100%
                );

            border-radius:
                22px;

            padding:
                34px 36px;

            margin:
                8px 0 25px 0;

            box-shadow:
                0 18px 42px
                rgba(8,39,70,0.18);

            color:
                #ffffff;
        }


        /* =====================================================
           TRICOLOUR CIRCLE
        ===================================================== */

        .hero:after {

            content:
                "";

            position:
                absolute;

            right:
                40px;

            top:
                35px;

            width:
                125px;

            height:
                125px;

            border-radius:
                50%;

            background:
                conic-gradient(
                    #ff7a00 0deg 120deg,
                    #ffffff 120deg 240deg,
                    #138808 240deg 360deg
                );

            opacity:
                0.15;
        }


        .hero:before {

            content:
                "✺";

            position:
                absolute;

            right:
                79px;

            top:
                74px;

            z-index:
                2;

            width:
                43px;

            height:
                43px;

            display:
                grid;

            place-items:
                center;

            border-radius:
                50%;

            border:
                2px solid
                rgba(255,255,255,0.30);

            color:
                rgba(255,255,255,0.55);

            font-size:
                22px;
        }


        .hero-kicker {

            position:
                relative;

            z-index:
                3;

            color:
                #dceafa;

            font-size:
                12px;

            text-transform:
                uppercase;

            letter-spacing:
                1.6px;

            margin-bottom:
                8px;
        }


        .hero-title {

            position:
                relative;

            z-index:
                3;

            color:
                #ffffff;

            font-size:
                43px;

            line-height:
                1.08;

            font-weight:
                800;

            margin:
                0;

            max-width:
                800px;
        }


        .hero-title span {
            color:
                #f0c45c;
        }


        .hero-subtitle {

            position:
                relative;

            z-index:
                3;

            color:
                #edf6ff;

            font-size:
                17px;

            margin-top:
                11px;

            max-width:
                760px;
        }


        /* =====================================================
           HERO BADGES
        ===================================================== */

        .hero-badges {

            position:
                relative;

            z-index:
                3;

            display:
                flex;

            flex-wrap:
                wrap;

            gap:
                10px;

            margin-top:
                20px;
        }


        .hero-badge {

            color:
                #ffffff;

            background:
                rgba(255,255,255,0.10);

            border:
                1px solid
                rgba(255,255,255,0.16);

            border-radius:
                999px;

            padding:
                8px 13px;

            font-size:
                12px;

            backdrop-filter:
                blur(4px);
        }


        /* =====================================================
           WHITE SECTION CARD
        ===================================================== */

        .section-card {

            background:
                #ffffff;

            border:
                1px solid
                var(--border);

            border-radius:
                18px;

            padding:
                23px;

            margin-bottom:
                18px;

            box-shadow:
                0 8px 26px
                rgba(20,49,80,0.06);

            color:
                var(--text) !important;
        }


        .section-card,
        .section-card p,
        .section-card div,
        .section-card span,
        .section-card li,
        .section-card ul,
        .section-card ol {

            color:
                var(--text) !important;
        }


        .section-card li {

            margin-bottom:
                8px;

            line-height:
                1.65;
        }


        .section-title {

            color:
                var(--text) !important;

            font-size:
                22px;

            font-weight:
                800;

            margin-bottom:
                5px;
        }


        .section-subtitle {

            color:
                var(--text-light) !important;

            font-size:
                13px;

            line-height:
                1.55;

            margin-bottom:
                14px;
        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        .metric-card {

            background:
                #ffffff;

            border:
                1px solid
                var(--border);

            border-radius:
                16px;

            padding:
                19px;

            min-height:
                120px;

            box-shadow:
                0 8px 22px
                rgba(20,49,80,0.05);
        }


        .metric-label {

            color:
                var(--text-light) !important;

            font-size:
                11px;

            text-transform:
                uppercase;

            letter-spacing:
                0.8px;
        }


        .metric-value {

            color:
                var(--text) !important;

            font-size:
                28px;

            font-weight:
                800;

            margin-top:
                6px;
        }


        .metric-note {

            color:
                var(--text-light) !important;

            font-size:
                12px;

            margin-top:
                3px;
        }


        /* =====================================================
           APPROVAL CARD
        ===================================================== */

        .approval-card {

            background:
                linear-gradient(
                    135deg,
                    #eaf8f0,
                    #f9fffb
                );

            border:
                1px solid
                #b7dfc9;

            border-radius:
                18px;

            padding:
                23px;

            color:
                #20543b !important;
        }


        .approval-card * {
            color:
                #20543b !important;
        }


        .approval-title {

            color:
                #087747 !important;

            font-size:
                28px;

            font-weight:
                800;
        }


        /* =====================================================
           REJECTION CARD
        ===================================================== */

        .rejection-card {

            background:
                linear-gradient(
                    135deg,
                    #fff0f2,
                    #fff9fa
                );

            border:
                1px solid
                #ecc1c8;

            border-radius:
                18px;

            padding:
                23px;

            color:
                #633e48 !important;
        }


        .rejection-card * {
            color:
                #633e48 !important;
        }


        .rejection-title {

            color:
                #a4273b !important;

            font-size:
                28px;

            font-weight:
                800;
        }


        /* =====================================================
           AI EXPLANATION
        ===================================================== */

        .ai-card {

            background:
                linear-gradient(
                    135deg,
                    #f2eeff,
                    #fbfaff
                );

            border:
                1px solid
                #ddd2ff;

            border-radius:
                18px;

            padding:
                23px;

            line-height:
                1.75;

            color:
                #2c3b65 !important;
        }


        .ai-card *,
        .ai-card p,
        .ai-card div,
        .ai-card span {

            color:
                #2c3b65 !important;
        }


        .ai-label {

            display:
                inline-block;

            background:
                #eae2ff;

            color:
                #5d3bb1 !important;

            border-radius:
                999px;

            padding:
                5px 11px;

            font-size:
                11px;

            font-weight:
                700;

            text-transform:
                uppercase;

            letter-spacing:
                0.7px;

            margin-bottom:
                11px;
        }


        /* =====================================================
           WORKFLOW
        ===================================================== */

        .workflow {

            display:
                flex;

            gap:
                14px;

            flex-wrap:
                wrap;
        }


        .workflow-step {

            flex:
                1 1 180px;

            background:
                #ffffff;

            border:
                1px solid
                var(--border);

            border-radius:
                16px;

            padding:
                19px;

            box-shadow:
                0 5px 16px
                rgba(20,49,80,0.04);
        }


        .workflow-num {

            width:
                34px;

            height:
                34px;

            border-radius:
                50%;

            display:
                grid;

            place-items:
                center;

            background:
                var(--blue);

            color:
                #ffffff !important;

            font-weight:
                800;

            margin-bottom:
                10px;
        }


        .workflow-title {

            color:
                var(--text) !important;

            font-weight:
                800;
        }


        .workflow-text {

            color:
                var(--text-light) !important;

            font-size:
                12px;

            line-height:
                1.55;

            margin-top:
                5px;
        }


        /* =====================================================
           INPUT FIELDS
        ===================================================== */

        label {

            color:
                var(--text) !important;

            font-weight:
                600;
        }


        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {

            background:
                #ffffff;

            border:
                1px solid
                #c9d7e5;

            border-radius:
                10px;
        }


        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {

            background:
                #ffffff !important;

            color:
                var(--text) !important;
        }


        div[data-baseweb="select"] * {

            color:
                var(--text) !important;
        }


        /* =====================================================
           BUTTONS AND FORM CONTROL CONTRAST
        ===================================================== */

        .stButton > button {
            min-height: 44px;
            border: 2px solid #145db5 !important;
            border-radius: 11px;
            background: #edf5ff !important;
            color: #082746 !important;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: #dcecff !important;
            border-color: #0d4e8e !important;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #082746, #145db5) !important;
            border-color: #082746 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(8, 39, 70, 0.22);
        }

        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(90deg, #061d35, #0d4e8e) !important;
            border-color: #061d35 !important;
        }

        div.stButton > button[kind="primary"] * {
            color: #ffffff !important;
        }

        /* Streamlit's current number-input and selectbox controls. */
        [data-testid="stNumberInputContainer"],
        .react-aria-ComboBox [role="group"] {
            background: #ffffff !important;
            border: 2px solid #145db5 !important;
            border-radius: 10px !important;
        }

        [data-testid="stNumberInputField"],
        .react-aria-ComboBox input[role="combobox"],
        [data-testid="stNumberInputStepUp"],
        [data-testid="stNumberInputStepDown"],
        .react-aria-ComboBox button[aria-haspopup="listbox"] {
            color: #082746 !important;
        }

        [data-testid="stNumberInputStepUp"],
        [data-testid="stNumberInputStepDown"],
        .react-aria-ComboBox button[aria-haspopup="listbox"] {
            background: #dcecff !important;
            border-left: 1px solid #145db5 !important;
        }

        [data-testid="stNumberInputStepUp"]:hover,
        [data-testid="stNumberInputStepDown"]:hover,
        .react-aria-ComboBox button[aria-haspopup="listbox"]:hover {
            background: #c7e0fa !important;
        }


        /* =====================================================
           EXPANDER
        ===================================================== */

        [data-testid="stExpander"] {

            background:
                #ffffff;

            border:
                1px solid
                var(--border);

            border-radius:
                14px;
        }


        [data-testid="stExpander"] summary {

            color:
                var(--text) !important;

            font-weight:
                700;
        }


        /* =====================================================
           TABS
        ===================================================== */

        button[data-baseweb="tab"] {

            color:
                var(--text-light) !important;

            font-weight:
                700;
        }


        button[data-baseweb="tab"][aria-selected="true"] {

            color:
                var(--blue) !important;
        }


        /* =====================================================
           DATAFRAME
        ===================================================== */

        [data-testid="stDataFrame"] {

            border-radius:
                12px;

            overflow:
                hidden;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 900px) {

            .hero {

                padding:
                    28px 23px;
            }


            .hero-title {

                font-size:
                    32px;
            }


            .hero-subtitle {

                font-size:
                    15px;
            }


            .hero:after {

                width:
                    90px;

                height:
                    90px;

                right:
                    14px;

                top:
                    30px;
            }


            .hero:before {

                right:
                    37px;

                top:
                    55px;
            }
        }


        /* =====================================================
           DARK MODE OVERRIDES
        ===================================================== */

        :root {
            --navy: #06182b;
            --navy-light: #0d355c;
            --blue: #3c8ee6;
            --blue-light: #6aaef2;
            --background: #081522;
            --text: #e8f1fb;
            --text-light: #aec2d8;
            --border: #29445f;
        }

        .stApp {
            background: linear-gradient(180deg, #081522 0%, #0a1b2c 55%, #07131f 100%);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(8, 21, 34, 0.96);
            border-bottom: 1px solid #29445f;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #04101d 0%, #08233d 52%, #061625 100%);
        }

        .section-card,
        .metric-card,
        .workflow-step,
        [data-testid="stExpander"] {
            background: #10243a !important;
            border-color: #29445f !important;
            box-shadow: 0 8px 26px rgba(0, 0, 0, 0.24);
        }

        .section-card,
        .section-card p,
        .section-card div,
        .section-card span,
        .section-card li,
        .section-card ul,
        .section-card ol,
        .section-title,
        .metric-value,
        .workflow-title {
            color: #eef6ff !important;
        }

        .section-subtitle,
        .metric-label,
        .metric-note,
        .workflow-text {
            color: #aec2d8 !important;
        }

        .approval-card {
            background: #0d3328 !important;
            border-color: #2a9d70 !important;
            color: #e8fff5 !important;
        }

        .rejection-card {
            background: #3a1b28 !important;
            border-color: #d95a7a !important;
            color: #ffeef3 !important;
        }

        .ai-card {
            background: #202247 !important;
            border-color: #7268d9 !important;
            color: #f2f0ff !important;
        }

        .ai-label {
            background: #3a367a !important;
            color: #ffffff !important;
        }

        label,
        [data-testid="stWidgetLabel"] p {
            color: #e8f1fb !important;
        }

        [data-testid="stNumberInputContainer"],
        .react-aria-ComboBox [role="group"] {
            background: #0b1b2d !important;
            border-color: #3c8ee6 !important;
        }

        [data-testid="stNumberInputField"],
        .react-aria-ComboBox input[role="combobox"],
        [data-testid="stNumberInputStepUp"],
        [data-testid="stNumberInputStepDown"],
        .react-aria-ComboBox button[aria-haspopup="listbox"] {
            color: #eef6ff !important;
        }

        [data-testid="stNumberInputStepUp"],
        [data-testid="stNumberInputStepDown"],
        .react-aria-ComboBox button[aria-haspopup="listbox"] {
            background: #173a5e !important;
            border-color: #3c8ee6 !important;
        }

        .stButton > button {
            background: #173a5e !important;
            border-color: #4b9df0 !important;
            color: #f4f9ff !important;
        }

        .stButton > button:hover {
            background: #24517f !important;
            border-color: #79b9f6 !important;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #1261b8, #3c8ee6) !important;
            border-color: #6aaef2 !important;
            color: #ffffff !important;
        }

        [data-testid="stAlert"] {
            background: #122c45 !important;
            color: #e8f1fb !important;
            border-color: #315d88 !important;
        }

        button[data-baseweb="tab"],
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #d9eaff !important;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #29445f;
        }

        </style>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# SIDEBAR BRAND
# ==========================================================

def sidebar_brand():
    """Render the sidebar brand as HTML, not Markdown code."""
    html = """
<div class="bank-brand">
    <div class="logo">🏛️</div>
    <div class="name">Bharat Loan AI</div>
    <div class="tagline">Indian Banking-Style ML Project</div>
    <div class="tricolor"></div>
</div>
"""
    with st.sidebar:
        st.html(textwrap.dedent(html))


# ==========================================================
# HERO SECTION
# ==========================================================

def hero(
    title="Loan Approval Prediction",
    subtitle="Data-driven decisions for a smarter tomorrow"
):
    """Render the page hero as HTML, not Markdown code."""
    if "Prediction" in title:
        parts = title.split("Prediction", 1)
        title_html = parts[0] + "<span>Prediction</span>" + parts[1]
    else:
        title_html = title

    html = f"""
<div class="hero">
    <div class="hero-kicker">🇮🇳 Empowering a digitally enabled India</div>
    <div class="hero-title">{title_html}</div>
    <div class="hero-subtitle">{subtitle}</div>
    <div class="hero-badges">
        <div class="hero-badge">⚡ Faster Insights</div>
        <div class="hero-badge">🛡️ Explainable ML</div>
        <div class="hero-badge">📊 Ensemble Learning</div>
        <div class="hero-badge">🤖 Gemini AI Explanation</div>
    </div>
</div>
"""
    st.html(textwrap.dedent(html))


# ==========================================================
# SECTION CARD
# ==========================================================


def section_card(
    title,
    text="",
    items=None
):

    items_html = ""

    if items:

        items_html = "<ul>"

        for item in items:

            items_html += (
                f"<li>{item}</li>"
            )

        items_html += "</ul>"


    html = f"""
<div class="section-card">

    <div class="section-title">
        {title}
    </div>

    <div class="section-subtitle">
        {text}
    </div>

    {items_html}

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(
    label,
    value,
    note=""
):

    html = f"""
<div class="metric-card">

    <div class="metric-label">
        {label}
    </div>

    <div class="metric-value">
        {value}
    </div>

    <div class="metric-note">
        {note}
    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# APPROVAL CARD
# ==========================================================

def approval_card(
    probability,
    risk
):

    html = f"""
<div class="approval-card">

    <div style="font-size:42px;">
        ✓
    </div>

    <div class="approval-title">
        Loan Approved
    </div>

    <div style="margin-top:6px;">
        The model predicts that this loan application
        is likely to be approved.
    </div>

    <div style="
        display:flex;
        gap:30px;
        margin-top:18px;
        flex-wrap:wrap;
    ">

        <div>
            <strong>
                {probability:.1f}%
            </strong>
            <br>
            Approval Probability
        </div>

        <div>
            <strong>
                {risk}
            </strong>
            <br>
            Risk Level
        </div>

    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# REJECTION CARD
# ==========================================================

def rejection_card(
    probability,
    risk
):

    html = f"""
<div class="rejection-card">

    <div style="font-size:42px;">
        ✕
    </div>

    <div class="rejection-title">
        Loan Rejected
    </div>

    <div style="margin-top:6px;">
        The model predicts that this loan application
        is unlikely to be approved.
    </div>

    <div style="
        display:flex;
        gap:30px;
        margin-top:18px;
        flex-wrap:wrap;
    ">

        <div>
            <strong>
                {probability:.1f}%
            </strong>
            <br>
            Approval Probability
        </div>

        <div>
            <strong>
                {risk}
            </strong>
            <br>
            Risk Level
        </div>

    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# AI EXPLANATION CARD
# ==========================================================

def ai_card(
    explanation
):

    html = f"""
<div class="ai-card">

    <div class="ai-label">
        Gemini AI Explanation
    </div>

    <div style="
        font-size:20px;
        font-weight:800;
        margin-bottom:12px;
    ">
        🤖 Explanation of This Prediction
    </div>

    <div>
        {explanation}
    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# WORKFLOW
# ==========================================================

def workflow():

    html = """
<div class="workflow">

    <div class="workflow-step">

        <div class="workflow-num">
            1
        </div>

        <div class="workflow-title">
            Input
        </div>

        <div class="workflow-text">
            Applicant details are entered into
            the application.
        </div>

    </div>


    <div class="workflow-step">

        <div class="workflow-num">
            2
        </div>

        <div class="workflow-title">
            Preprocessing
        </div>

        <div class="workflow-text">
            Numerical and categorical data are
            prepared using the training pipeline.
        </div>

    </div>


    <div class="workflow-step">

        <div class="workflow-num">
            3
        </div>

        <div class="workflow-title">
            ML Prediction
        </div>

        <div class="workflow-text">
            The trained ensemble model calculates
            the loan approval probability.
        </div>

    </div>


    <div class="workflow-step">

        <div class="workflow-num">
            4
        </div>

        <div class="workflow-title">
            AI Explanation
        </div>

        <div class="workflow-text">
            Gemini converts the model result into
            a simple human-readable explanation.
        </div>

    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ==========================================================
# FOOTER
# ==========================================================

def footer():

    html = """
<div class="footer-card">

    <div style="
        display:flex;
        justify-content:space-between;
        gap:20px;
        flex-wrap:wrap;
    ">

        <div>
            <strong>
                🇮🇳 Bharat Loan AI
            </strong>
            <br>
            A Machine Learning Project
        </div>

        <div>
            Developed by
            <strong>
                Ashutosh Paltasingh
            </strong>
            <br>
            B.Tech CSE (AIML)
        </div>

        <div>
            Loan Approval Prediction
            <br>
            Bagging vs Boosting
        </div>

    </div>

</div>
"""

    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )
