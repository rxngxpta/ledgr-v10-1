# !/usr/bin/env python312
# -*- coding: utf-8 -*-
# __author__ = 'R. Sengupta | r_xn'
# __copyright__ = 'Copyright 2023, Ledgr | www.alphaLedgr.com'
# __credits__ = ['r_xn, s.sengupta,  adasgupta@gmail.com']
# __license__ = 'Ledgr | alphaledgr.com'
# __version__ = '01.02.04'
# __maintainer__ = 'r_xn@alphaledgr.com'
# __emails__ = 'r_xn@alphaledgr.com / response@alphaledgr.com'
# __status__ = 'In active development'
import streamlit_authenticator as stauth

# from yaml.loader import SafeLoader
import os
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
direc = os.getcwd()

##################################################################
logofile = f'{direc}/pages/appdata/imgs/Ledgr_Logo_F2.png'

selected = option_menu(
    menu_title=None,
    options = ["News", "LedgrSite", "Media, Visuals & Posts"],

    default_index=0,
    orientation="Horizontal",
    )

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

url_ytube = "https://www.youtube.com/@LedgrInc"
url_fbook = "https://www.facebook.com/share/1BnXaYvRzV/"
url_insta = 'https://www.instagram.com/alphaledgr/'
url_blog = 'https://www.alphaledgr.com/Blog'
url_linkedin = "https://www.linkedin.com/company/ledgrapp/"


# Authentication 1 #  
st.markdown(''' <div align="center"><h1>Hello! Welcome to Ledgr.</h1></div>''',
                unsafe_allow_html=True)

def login_screen():

    st.markdown(''' <div align="center"><h1>Authenticate via Google to proceed.</h1></div>''',
                unsafe_allow_html=True)
    st.markdown(''' <div align="center"><h1>Proceed into a new ecosystem.</h1></div>''',
                unsafe_allow_html=True)
    # st.subheader()
    st.image(logofile, use_container_width=True)
    v1, v2, v3 = st.columns([2, 1, 2])
    with v1:
        st.write(" ")
    with v2:
        if st.button("Log in with Google"):
            st.login()
    with v3:
        st.write(" ")

if not st.user.is_logged_in:
    login_screen()
else:
    st.user
    st.sidebar.button("Log out", on_click=st.logout)

    st.user.family_name

        # Main Streamlit app starts here

    
    st.markdown('''
                <div align="center">
                <h3>Learn how to get started on the platform!
                See below for details..</h3></div>''',
                unsafe_allow_html=True)
   # st.write(f'{username} Welcome!')
    st.image(f'{direc}/pages/appdata/imgs/The alphaLedgr Web3 Platform.png',
             width="content")
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

        # Use a consistent style for the plot
        style.use('fivethirtyeight')

        # Initialize figure and axis
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        xs = []
        ys = []

        def animate(i):
            # Fetch the latest data (can be replaced with an API call in a real application)
            data = yf.Ticker('^NSEI').info
            current_price = data.get('regularMarketPrice')
            if current_price:
                xs.append(i) # Use an incrementing counter for x-axis time
                ys.append(current_price)
                ax1.clear()
                ax1.plot(xs, ys)
                plt.xlabel("Time")
                plt.ylabel("Nifty Price")
                plt.title("Real-Time Nifty Plot")

        # Set up the animation function to be called every 1000 milliseconds (1 second)
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

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



#if not st.user.is_logged_in:
 #   login_screen()
#else:
 #   st.header(f"Welcome1, {st.user}!")
    




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
    st.image(ledgrblog,  '[Ledgr\'s Blog ](%s)' % url_blog)
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

