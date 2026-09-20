import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL COLORS
        ===================================================== */

        :root {
            --navy: #092846;
            --navy2: #0d3f70;
            --blue: #0f56b3;
            --blue2: #1d73c9;
            --gold: #d8a83e;
            --orange: #ff7a00;
            --green: #138808;

            --ink: #16314f;
            --ink2: #234a70;
            --muted: #61758d;

            --bg: #eef4f9;
            --white: #ffffff;
            --line: #d6e1ec;

            --success: #11814a;
            --success-bg: #edf9f2;

            --danger: #a7283b;
            --danger-bg: #fff1f3;
        }


        /* =====================================================
           APP BACKGROUND
        ===================================================== */

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #f8fafc 0%,
                    #edf3f8 55%,
                    #e9f0f6 100%
                );
            color: var(--ink);
        }


        /* =====================================================
           STREAMLIT TOP BAR
        ===================================================== */

        [data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.95);
            height: 55px;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #072844 0%,
                    #0a3157 50%,
                    #082744 100%
                );

            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f5f9fd;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15);
        }


        /* =====================================================
           SIDEBAR BRAND
        ===================================================== */

        .bank-brand {
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 20px 18px;
            margin-bottom: 18px;
            box-shadow:
                0 8px 25px rgba(0,0,0,0.10);
        }

        .bank-brand .logo {
            font-size: 30px;
            line-height: 1;
            margin-bottom: 8px;
        }

        .bank-brand .name {
            color: #ffffff;
            font-size: 21px;
            font-weight: 800;
            letter-spacing: 0.2px;
        }

        .bank-brand .tagline {
            color: #d7e6f4;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1.3px;
            margin-top: 4px;
        }


        /* =====================================================
           INDIA TRICOLOR
        ===================================================== */

        .tricolor {
            height: 5px;
            width: 100%;
            border-radius: 999px;

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

            margin-top: 14px;
            box-shadow:
                0 1px 5px rgba(0,0,0,0.15);
        }


        /* =====================================================
           SIDEBAR BUTTONS
        ===================================================== */

        [data-testid="stSidebar"] .stButton button {
            width: 100%;
            min-height: 42px;

            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.13);
            color: #ffffff;

            border-radius: 10px;

            font-weight: 600;

            transition:
                background 0.2s ease,
                transform 0.2s ease;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: rgba(255,255,255,0.14);
            transform: translateY(-1px);
        }


        /* =====================================================
           MAIN HERO
        ===================================================== */

        .hero {
            position: relative;
            overflow: hidden;

            background:
                linear-gradient(
                    105deg,
                    #082746 0%,
                    #0d4e8e 56%,
                    #1d73bd 100%
                );

            border-radius: 22px;

            padding: 34px 36px;

            margin:
                8px 0 25px 0;

            color: white;

            box-shadow:
                0 16px 42px rgba(9,40,70,0.18);
        }


        /* Decorative Indian tricolor element */
        .hero:after {
            content: "";
            position: absolute;

            right: 38px;
            top: 34px;

            width: 125px;
            height: 125px;

            border-radius: 50%;

            background:
                conic-gradient(
                    #ff7a00 0deg 120deg,
                    #ffffff 120deg 240deg,
                    #138808 240deg 360deg
                );

            opacity: 0.16;

            box-shadow:
                inset 0 0 0 2px rgba(255,255,255,0.25);
        }


        /* Ashoka Chakra-style centre */
        .hero:before {
            content: "✺";

            position: absolute;

            right: 77px;
            top: 59px;

            z-index: 2;

            width: 48px;
            height: 48px;

            display: grid;
            place-items: center;

            border-radius: 50%;

            color: rgba(255,255,255,0.55);

            font-size: 24px;
            font-weight: 700;

            border:
                2px solid
                rgba(255,255,255,0.30);
        }


        .hero-kicker {
            position: relative;
            z-index: 3;

            color: #d8e8f7;

            font-size: 12px;

            text-transform: uppercase;

            letter-spacing: 1.7px;

            margin-bottom: 8px;
        }


        .hero-title {
            position: relative;
            z-index: 3;

            color: #ffffff;

            font-size: 43px;

            line-height: 1.08;

            font-weight: 800;

            margin: 0;

            max-width: 800px;
        }

        .hero-title span {
            color: #f0c45c;
        }


        .hero-subtitle {
            position: relative;
            z-index: 3;

            margin-top: 11px;

            color: #eef6ff;

            font-size: 17px;

            max-width: 750px;
        }


        /* =====================================================
           HERO BADGES
        ===================================================== */

        .hero-badges {
            position: relative;
            z-index: 3;

            display: flex;

            gap: 10px;

            margin-top: 20px;

            flex-wrap: wrap;
        }


        .hero-badge {
            background:
                rgba(255,255,255,0.10);

            border:
                1px solid
                rgba(255,255,255,0.17);

            color: #ffffff;

            padding:
                8px 13px;

            border-radius:
                999px;

            font-size:
                12px;

            backdrop-filter:
                blur(4px);
        }


        /* =====================================================
           SECTION CARD
        ===================================================== */

        .section-card {
            background: #ffffff;

            border:
                1px solid
                var(--line);

            border-radius: 18px;

            padding: 23px;

            margin-bottom: 18px;

            box-shadow:
                0 8px 25px
                rgba(15,40,70,0.06);

            color: var(--ink) !important;
        }


        /* FORCE ALL CARD TEXT TO BE DARK */

        .section-card,
        .section-card p,
        .section-card span,
        .section-card div,
        .section-card li,
        .section-card ul,
        .section-card ol {
            color: var(--ink) !important;
        }


        .section-card li {
            margin-bottom: 8px;

            line-height: 1.65;
        }


        .section-title {
            color: var(--ink) !important;

            font-size: 22px;

            font-weight: 800;

            margin-bottom: 5px;
        }


        .section-subtitle {
            color: var(--muted) !important;

            font-size: 13px;

            margin-bottom: 14px;

            line-height: 1.55;
        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        .metric-card {
            background: #ffffff;

            border:
                1px solid
                var(--line);

            border-radius: 16px;

            padding: 19px;

            min-height: 120px;

            box-shadow:
                0 8px 22px
                rgba(15,40,70,0.05);

            color: var(--ink);
        }


        .metric-label {
            color: var(--muted) !important;

            font-size: 11px;

            text-transform:
                uppercase;

            letter-spacing:
                0.8px;
        }


        .metric-value {
            color: var(--ink) !important;

            font-size: 28px;

            font-weight: 800;

            margin-top: 6px;
        }


        .metric-note {
            color: var(--muted) !important;

            font-size: 12px;

            margin-top: 3px;
        }


        /* =====================================================
           APPROVAL CARD
        ===================================================== */

        .approval-card {
            background:
                linear-gradient(
                    135deg,
                    #e8f8ef 0%,
                    #f8fffb 100%
                );

            border:
                1px solid
                #b9e2ca;

            border-radius:
                18px;

            padding:
                23px;

            margin-bottom:
                16px;

            color:
                #24543c !important;
        }


        .approval-card * {
            color: #24543c !important;
        }


        .approval-title {
            color:
                #0f7446 !important;

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
                    #fff0f2 0%,
                    #fff9fa 100%
                );

            border:
                1px solid
                #edc0c7;

            border-radius:
                18px;

            padding:
                23px;

            margin-bottom:
                16px;

            color:
                #65404a !important;
        }


        .rejection-card * {
            color:
                #65404a !important;
        }


        .rejection-title {
            color:
                #a22739 !important;

            font-size:
                28px;

            font-weight:
                800;
        }


        /* =====================================================
           AI CARD
        ===================================================== */

        .ai-card {
            background:
                linear-gradient(
                    135deg,
                    #f3efff 0%,
                    #fbfaff 100%
                );

            border:
                1px solid
                #ddd3ff;

            border-radius:
                18px;

            padding:
                23px;

            line-height:
                1.75;

            color:
                #27365e !important;
        }


        .ai-card p,
        .ai-card div,
        .ai-card span {
            color:
                #27365e !important;
        }


        .ai-label {
            display:
                inline-block;

            background:
                #e9e1ff;

            color:
                #5b3db0 !important;

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

            align-items:
                stretch;

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
                var(--line);

            border-radius:
                16px;

            padding:
                19px;

            box-shadow:
                0 5px 16px
                rgba(15,40,70,0.04);
        }


        .workflow-num {
            width:
                34px;

            height:
                34px;

            display:
                grid;

            place-items:
                center;

            border-radius:
                50%;

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
            font-weight:
                800;

            color:
                var(--ink) !important;
        }


        .workflow-text {
            color:
                var(--muted) !important;

            font-size:
                12px;

            line-height:
                1.55;

            margin-top:
                5px;
        }


        /* =====================================================
           FOOTER
        ===================================================== */

        .footer-card {
            background:
                linear-gradient(
                    90deg,
                    #082746,
                    #0d3b66
                );

            color:
                #dbe8f5 !important;

            border-radius:
                16px;

            padding:
                18px 20px;

            margin-top:
                22px;

            font-size:
                12px;

            line-height:
                1.6;
        }


        .footer-card * {
            color:
                #dbe8f5 !important;
        }


        /* =====================================================
           INPUT FIELDS
        ===================================================== */

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {
            background:
                #ffffff;

            border-radius:
                10px;

            border:
                1px solid
                #c8d6e5;

            color:
                var(--ink);
        }


        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            color:
                var(--ink) !important;

            background:
                #ffffff !important;
        }


        label {
            color:
                var(--ink) !important;

            font-weight:
                600;
        }


        /* =====================================================
           SELECTBOX TEXT
        ===================================================== */

        div[data-baseweb="select"] * {
            color:
                var(--ink) !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            border-radius:
                11px;

            min-height:
                44px;

            font-weight:
                700;

            border:
                1px solid
                #cbd9e7;
        }


        .stButton > button:hover {
            border-color:
                var(--blue);

            transform:
                translateY(-1px);
        }


        div.stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    90deg,
                    #0f56b3,
                    #1d73c9
                );

            color:
                #ffffff;

            border:
                none;
        }


        div.stButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    90deg,
                    #0d4ca0,
                    #1767b8
                );
        }


        /* =====================================================
           EXPANDER
        ===================================================== */

        [data-testid="stExpander"] {
            background:
                #ffffff;

            border:
                1px solid
                var(--line);

            border-radius:
                14px;
        }


        [data-testid="stExpander"] summary {
            color:
                var(--ink) !important;

            font-weight:
                700;
        }


        /* =====================================================
           TABS
        ===================================================== */

        button[data-baseweb="tab"] {
            color:
                var(--muted) !important;

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
           ALERTS
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius:
                12px;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 900px) {

            .hero {
                padding:
                    27px 24px;
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
                    15px;

                top:
                    28px;
            }

            .hero:before {
                right:
                    36px;

                top:
                    49px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():

    st.sidebar.markdown(
        """
        <div class="bank-brand">

            <div class="logo">
                🏛️
            </div>

            <div class="name">
                Bharat Loan AI
            </div>

            <div class="tagline">
                Indian Banking-Style ML Project
            </div>

            <div class="tricolor"></div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(
    title="Loan Approval Prediction",
    subtitle="Data-driven decisions for a smarter tomorrow"
):

    if "Prediction" in title:

        first_part, second_part = title.split(
            "Prediction",
            1
        )

        title_html = (
            f"{first_part}"
            f"<span>Prediction</span>"
            f"{second_part}"
        )

    else:

        title_html = title


    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-kicker">
                🇮🇳 Empowering a digitally enabled India
            </div>

            <div class="hero-title">
                {title_html}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

            <div class="hero-badges">

                <div class="hero-badge">
                    ⚡ Faster Insights
                </div>

                <div class="hero-badge">
                    🛡️ Explainable ML
                </div>

                <div class="hero-badge">
                    📊 Ensemble Learning
                </div>

                <div class="hero-badge">
                    🤖 Gemini AI Explanation
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )
