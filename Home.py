# !/usr/bin/env python310
# -*- coding: utf-8 -*-
# __author__ = 'R. Sengupta | r_xn'
# __copyright__ = 'Copyright 2023, Ledgr | www.alphaLedgr.com'
# __credits__ = ['r_xn, s.sengupta,  adasgupta@gmail.com']
# __license__ = 'Ledgr | alphaledgr.com'
# __version__ = '01.02.04'
# __maintainer__ = 'r_xn@alphaledgr.com'
# __emails__ = 'r_xn@alphaledgr.com / response@alphaledgr.com'
# __status__ = 'In active development'
#  streamlit_authenticator as stauth

# from yaml.loader import SafeLoader
import os
import streamlit as st

direc = os.getcwd()

import pandas as pd
from datetime import datetime, timedelta
from authlib.integrations.requests_client import OAuth2Session

st.write(f'{direc}')
USERS_FILE = f'{direc}//pages/appdata/u_info/users.csv'

# ---------------------------
# Utility Functions
# ---------------------------

def load_users():
    try:
        return pd.read_csv(USERS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["email", "subscription_type", "subscription_expiry"])

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def is_subscription_active(expiry_date):
    return datetime.utcnow() < datetime.fromisoformat(expiry_date)

def subscription_expiry(period):
    if period == "daily":
        return datetime.utcnow() + timedelta(days=1)
    if period == "weekly":
        return datetime.utcnow() + timedelta(days=7)
    if period == "monthly":
        return datetime.utcnow() + timedelta(days=30)

# ---------------------------
# OAuth Configuration
# ---------------------------

CLIENT_ID = "880801167829-cqhehbl71j9i5mp0noirndoqg6f5ap9i.apps.googleusercontent.com"
CLIENT_SECRET = "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"

oauth = OAuth2Session(
    CLIENT_ID,
    CLIENT_SECRET,
    scope="openid email profile",
    redirect_uri=st.secrets.get("redirect_uri", "")
)

# ---------------------------
# Session Initialization
# ---------------------------

if "email" not in st.session_state:
    st.session_state.email = None

# ---------------------------
# Authentication
# ---------------------------

st.title("Welcome to alphaLedgr")

if not st.session_state.email:
    auth_url, _ = oauth.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )

    st.markdown(f"[Sign in with Google]({auth_url})")
    st.stop()

# ---------------------------
# Load User Record
# ---------------------------

users = load_users()
user = users[users.email == st.session_state.email]

# ---------------------------
# Registration
# ---------------------------

if user.empty:
    st.subheader("Complete Registration")

    if st.button("Register Account"):
        new_user = pd.DataFrame([{
            "email": st.session_state.email,
            "subscription_type": "none",
            "subscription_expiry": ""
        }])
        users = pd.concat([users, new_user])
        save_users(users)
        st.experimental_rerun()

    st.stop()

# ---------------------------
# Subscription Validation
# ---------------------------

subscription_type = user.iloc[0]["subscription_type"]
expiry = user.iloc[0]["subscription_expiry"]

if subscription_type == "none" or not expiry or not is_subscription_active(expiry):
    st.subheader("Subscription Required")

    option = st.selectbox(
        "Choose a plan",
        ["daily", "weekly", "monthly"]
    )

    if st.button("Activate Subscription"):
        users.loc[users.email == st.session_state.email, "subscription_type"] = option
        users.loc[users.email == st.session_state.email, "subscription_expiry"] = (
            subscription_expiry(option).isoformat()
        )
        save_users(users)
        st.experimental_rerun()

    st.stop()

# ---------------------------
# Authorized Content
# ---------------------------

st.success("Access granted. Subscription active.")
st.write("You may now access all other pages.")

##################################################################
logofile = f'{direc}/pages/appdata/imgs/Ledgr_Logo_F2.png'

with st.sidebar:
    st.image(logofile)
    st.caption("Your unified Fintelligence Portal!")

# #######################################
# Icons and Links ###########################
ytube = f'{direc}/pages/appdata/imgs/ytube.svg'
fbook = f'{direc}/pages/appdata/imgs/fbook.svg'
insta = f'{direc}/pages/appdata/imgs/insta.svg'
linkedin = f'{direc}/pages/appdata/imgs/linkedin.svg'
ledgrblog = f'{direc}/pages/appdata/imgs/Ledgr_Logo_F2.png'
icon_size = 100

url_ytube = "https://www.youtube.com/@LedgrInc"
url_fbook = "https://www.facebook.com/share/1BnXaYvRzV/"
url_insta = 'https://www.instagram.com/alphaledgr/'
url_blog = 'https://www.alphaledgr.com/Blog'
url_linkedin = "https://www.linkedin.com/company/ledgrapp/"











# Main Streamlit app starts here

st.markdown(''' <div align="center"><h1>Hello! Welcome to Ledgr.</h1></div>''',
            unsafe_allow_html=True)
st.markdown('''
            <div align="center">
            <h3>Learn how to get started on the platform!
            See below for details..</h3></div>''',
            unsafe_allow_html=True)

st.image(f'{direc}/pages/appdata/imgs/The alphaLedgr Web3 Platform.png',
         use_container_width=True)
with st.container():
    a1, a2a, a2, a3 = st.columns([1, 1, 4, 1])
    with a1:
        st.image(f'{direc}/pages/appdata/imgs/LedgrBase.svg',
                 caption='Your Unified Wealth Dashboard')
    with a2a:
        st.write(" ")
    with a2:
        st.subheader("Part I: Ledgrbase")
        st.write("Map your existing asset holdings and portfolios.")
        st.write("Review and note their overall performance till date.")
        st.subheader("Part II: MarketBoard")
        st.write("Calculate Returns from SIPs, Explore ETFs and Mutual Funds.")
    with a3:
        st.image(f'{direc}/pages/appdata/imgs/MarketBoard.png',
                 caption='Market Profiles, Plots and Instruments')
st.write("-------------------------------------------------------------------")
with st.container():
    c1, c2a, c2 = st.columns([1, 1, 3])
    with c1:
        st.image(f'{direc}/pages/appdata/imgs/AnalyticsBox.png',
                 caption='Analytics and Information')
    with c2a:
        st.write(" ")
    with c2:
        st.subheader("AnalyticsBox")
        st.write("Analyze a Security In-Depth. Visualize Metrics & Indicators")
        st.write("Gather comprehensive knowhow on a selected Security.")
st.write("-------------------------------------------------------------------")
with st.container():
    d1, d2a, d2 = st.columns([3, 1, 1])
    with d1:
        st.subheader("InvestmentLab")
        st.write("Optimize Investment Allocations.")
        st.write("Generate Efficient Portfolios to Maximize Returns.")
        st.write("""Input assets and amount to proceed.
                 Select any from 5 Optimized portfolios presented.""")

    with d2a:
        st.write(" ")
    with d2:
        st.image(f'{direc}/pages/appdata/imgs/InvestmentLab.png',
                 caption='Generate Optimal Portfolios',
                 use_container_width=True)
st.write("-------------------------------------------------------------------")
with st.container():
    e1, e2a, e2 = st.columns([1, 1, 3])

    with e1:
        st.image(f'{direc}/pages/appdata/imgs/ForecastEngine.png',
                 'Forecast Price Ranges using your own inputs.')
    with e2a:
        st.write(" ")
    with e2:
        st.subheader("ForecastEngine")
        st.write("Train Ledgr's AI")
        st.markdown("""Generate price forecasts for any security."
                    Observe overall trend plots over specific timescales""")
        st.markdown("""Use the docs and the posts on our Blog to commence!
                 Please do not forget to drop in your feedback""")
st.write("-------------------------------------------------------------------")
column1, column2, column3, column4, column5 = st.columns([1, 1, 1, 2, 1])
with column1:
    st.image(ytube, '[Ledgr\'s YouTube Channel](%s)' % url_ytube, width=60)
with column2:
    st.image(fbook, '[Ledgr\'s FaceBook Page ](%s)' % url_fbook, width=60)
with column3:
    st.image(linkedin,  '[Our LinkedIn Page ](%s)' % url_linkedin, width=60)
with column4:
    st.write(" ")
    st.image(ledgrblog,  '[Ledgr\'s Blog ](%s)' % url_blog, width=85)
    st.write(" ")
with column5:
    st.image(insta,  '[Ledgr\'s @ Instagram ](%s)' % url_insta, width=60)
# # ###################################################################
with st.container():
    f9, f10, f11 = st.columns([1, 5, 1])
    with f9:
        st.write(" ")
    with f10:
        st.caption(""":|2025 - 2026|All Rights Resrved © Ledgr Inc.|alphaLedgr:
                   """)
    with f11:
        st.write(" ")

