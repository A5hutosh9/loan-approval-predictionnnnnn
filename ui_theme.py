import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --navy: #0b2a4a;
            --blue: #0f56b3;
            --blue2: #1b75d0;
            --gold: #d6a63a;
            --green: #198754;
            --red: #c23b4a;
            --ink: #16314f;
            --muted: #66788f;
            --panel: #ffffff;
            --bg: #eef3f8;
            --line: #d7e1ec;
        }

        .stApp {
            background: linear-gradient(180deg, #f5f8fc 0%, #edf3f8 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(255,255,255,0.96);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #092846 0%, #0b355c 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f7fbff;
        }

        [data-testid="stSidebar"] .stButton button {
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(255,255,255,0.06);
            color: white;
            border-radius: 10px;
        }

        .bank-brand {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 18px 16px;
            margin-bottom: 18px;
        }

        .bank-brand .logo {
            font-size: 28px;
            margin-bottom: 4px;
        }

        .bank-brand .name {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.2px;
        }

        .bank-brand .tagline {
            color: #d9e7f5;
            font-size: 11px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }

        .tricolor {
            height: 4px;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                #ff7a00 0 33%,
                #ffffff 33% 66%,
                #138808 66% 100%
            );
            margin: 10px 0 4px;
        }

        .hero {
            background: linear-gradient(105deg, #082746 0%, #0e4e92 58%, #176db8 100%);
            border-radius: 22px;
            padding: 30px 32px;
            margin: 8px 0 22px 0;
            color: white;
            box-shadow: 0 14px 40px rgba(9,40,70,0.18);
            position: relative;
            overflow: hidden;
        }

        .hero:after {
            content: "🇮🇳";
            position: absolute;
            right: 40px;
            top: 20px;
            font-size: 74px;
            opacity: 0.16;
        }

        .hero-kicker {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.6px;
            color: #dbe9f7;
            margin-bottom: 8px;
        }

        .hero-title {
            font-size: 42px;
            line-height: 1.05;
            font-weight: 800;
            margin: 0;
        }

        .hero-title span {
            color: #f0c45c;
        }

        .hero-subtitle {
            margin-top: 10px;
            font-size: 17px;
            color: #edf6ff;
        }

        .hero-badges {
            display: flex;
            gap: 12px;
            margin-top: 18px;
            flex-wrap: wrap;
        }

        .hero-badge {
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 12px;
        }

        .section-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 8px 24px rgba(15,40,70,0.06);
            margin-bottom: 18px;
        }

        .section-title {
            color: var(--ink);
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .section-subtitle {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 14px;
        }

        .metric-card {
            background: white;
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 8px 20px rgba(15,40,70,0.05);
            min-height: 120px;
        }

        .metric-label {
            font-size: 12px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.7px;
        }

        .metric-value {
            color: var(--ink);
            font-size: 28px;
            font-weight: 800;
            margin-top: 6px;
        }

        .metric-note {
            color: var(--muted);
            font-size: 12px;
            margin-top: 2px;
        }

        .approval-card {
            background: linear-gradient(135deg, #e9f8f0 0%, #f7fffb 100%);
            border: 1px solid #bfe5cd;
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 16px;
        }

        .approval-title {
            color: #116b41;
            font-size: 28px;
            font-weight: 800;
        }

        .rejection-card {
            background: linear-gradient(135deg, #fff0f2 0%, #fff9fa 100%);
            border: 1px solid #efc0c7;
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 16px;
        }

        .rejection-title {
            color: #9d2636;
            font-size: 28px;
            font-weight: 800;
        }

        .ai-card {
            background: linear-gradient(135deg, #f4f0ff 0%, #fbfaff 100%);
            border: 1px solid #ddd4ff;
            border-radius: 18px;
            padding: 22px;
            line-height: 1.75;
        }

        .ai-label {
            display: inline-block;
            background: #ebe4ff;
            color: #5a3fb3;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 10px;
        }

        .workflow {
            display: flex;
            gap: 14px;
            align-items: stretch;
            flex-wrap: wrap;
        }

        .workflow-step {
            flex: 1 1 180px;
            background: white;
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 18px;
        }

        .workflow-num {
            width: 34px;
            height: 34px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            background: var(--blue);
            color: white;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .workflow-title {
            font-weight: 800;
            color: var(--ink);
        }

        .workflow-text {
            color: var(--muted);
            font-size: 12px;
            margin-top: 5px;
        }

        .footer-card {
            background: #092846;
            color: #dbe8f5;
            border-radius: 16px;
            padding: 18px 20px;
            margin-top: 22px;
            font-size: 12px;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: 10px;
            border-color: #c9d7e5;
        }

        .stButton > button {
            border-radius: 11px;
            min-height: 44px;
            font-weight: 700;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #0f56b3, #1b75d0);
            border: none;
        }

        @media (max-width: 900px) {
            .hero-title { font-size: 32px; }
            .hero:after { right: 10px; font-size: 50px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.sidebar.markdown(
        """
        <div class="bank-brand">
            <div class="logo">🏛️</div>
            <div class="name">Bharat Loan AI</div>
            <div class="tagline">Indian banking-style ML project</div>
            <div class="tricolor"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title="Loan Approval Prediction", subtitle="Data-driven decisions for a smarter tomorrow"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">🇮🇳 Empowering a digitally enabled India</div>
            <div class="hero-title">{title.split('Prediction')[0]}<span>Prediction</span></div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-badges">
                <div class="hero-badge">⚡ Faster insights</div>
                <div class="hero-badge">🛡️ Explainable ML</div>
                <div class="hero-badge">📊 Ensemble learning</div>
                <div class="hero-badge">🤖 Gemini AI explanation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
