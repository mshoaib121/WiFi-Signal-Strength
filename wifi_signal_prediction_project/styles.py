import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f8fafc 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1300px;
        }

        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        .hero-card {
            background: linear-gradient(135deg, #111827 0%, #1d4ed8 65%, #2563eb 100%);
            padding: 34px 38px;
            border-radius: 28px;
            color: white;
            box-shadow: 0 22px 60px rgba(30, 58, 138, 0.22);
            margin-bottom: 28px;
        }

        .hero-title {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 10px;
        }

        .hero-subtitle {
            font-size: 16px;
            color: #dbeafe;
            line-height: 1.7;
            max-width: 950px;
        }

        .section-card {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid #e5e7eb;
            border-radius: 24px;
            padding: 26px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
            margin-bottom: 22px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 8px;
        }

        .section-desc {
            color: #64748b;
            font-size: 15px;
            line-height: 1.7;
            margin-bottom: 5px;
        }

        .badge-blue {
            display: inline-block;
            background: #dbeafe;
            color: #1d4ed8;
            font-weight: 800;
            font-size: 13px;
            padding: 7px 13px;
            border-radius: 999px;
            margin-bottom: 12px;
        }

        .badge-green {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            font-weight: 800;
            font-size: 13px;
            padding: 7px 13px;
            border-radius: 999px;
            margin-bottom: 12px;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            padding: 18px 20px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b;
            font-size: 14px;
            font-weight: 700;
        }

        div[data-testid="stMetricValue"] {
            color: #111827;
            font-size: 26px;
            font-weight: 800;
        }

        div[data-testid="stSelectbox"] label {
            font-weight: 700;
            color: #1f2937;
            font-size: 14px;
        }

        div[data-baseweb="select"] > div {
            background: #ffffff;
            border: 1px solid #dbe3ef;
            border-radius: 14px;
            min-height: 48px;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }

        .stButton > button {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 0.78rem 1.35rem;
            font-weight: 800;
            letter-spacing: 0.2px;
            box-shadow: 0 14px 30px rgba(37, 99, 235, 0.28);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 38px rgba(37, 99, 235, 0.34);
            color: white;
        }

        .tip-item {
            background: white;
            padding: 13px 15px;
            border-radius: 14px;
            margin-bottom: 10px;
            border: 1px solid #e5e7eb;
            color: #334155;
            font-weight: 500;
        }

        hr {
            border-color: #e5e7eb;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }

            .hero-card {
                padding: 22px 18px;
                border-radius: 20px;
                margin-bottom: 18px;
            }

            .hero-title {
                font-size: 25px;
                line-height: 1.25;
                letter-spacing: -0.3px;
            }

            .hero-subtitle {
                font-size: 14px;
                line-height: 1.6;
            }

            .section-card {
                padding: 18px 14px;
                border-radius: 18px;
                margin-bottom: 16px;
            }

            .section-title {
                font-size: 21px;
                line-height: 1.3;
            }

            .section-desc {
                font-size: 14px;
                line-height: 1.6;
            }

            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }

            div[data-testid="stMetric"] {
                padding: 14px 14px;
                margin-bottom: 10px;
                border-radius: 16px;
            }

            div[data-testid="stMetricValue"] {
                font-size: 22px;
            }

            .stButton > button {
                width: 100%;
                padding: 0.85rem 1rem;
            }

            .tip-item {
                font-size: 14px;
                padding: 12px 13px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
