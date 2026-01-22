import numpy as np
import pandas as pd
# from pandas_datareader import data as pdr
import yfinance as yf
# from streamlit_pdf_viewer import pdf_viewer
import os
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import streamlit as st
import datetime as dt
# import base64
# import urllib
# Page Setup ##################################################################
sns.set()
plt.style.use('fivethirtyeight')
st.set_page_config(page_title='Ledgr | Valuation & Pricing Models',
                   layout="wide", initial_sidebar_state="expanded")

direc = os.getcwd()
# Declarations ################################################################
logofile = f'{direc}/pages/appdata/imgs/Ledgr_Logo_F2.png'


st.sidebar.image(logofile, use_container_width=True)
st.sidebar.caption("Select a stock, train the algorithm and predict scenarios")
# Icons and Links ###########################
ytube = f'{direc}/pages/appdata/imgs/ytube.svg'
fbook = f'{direc}/pages/appdata/imgs/fbook.svg'
insta = f'{direc}/pages/appdata/imgs/insta.svg'
linkedin = f'{direc}/pages/appdata/imgs/linkedin.svg'
ledgrblog = f'{direc}/pages/appdata/imgs/Ledgr_Logo_F2.png'
tickerfile = f"{direc}/pages/appdata/tickerlist_y.csv"
tickerdb = pd.read_csv(tickerfile)
tickerlist = tickerdb["SYMBOL"]
stock_m_list = ['^BSESN', '^NSEI']
periods = ['1y', '2y', '5y', '10y']
# Inputs #####################################################################
# Part I
start = dt.datetime(2019, 1, 1)
end = dt.datetime.now() 

if not st.user.is_logged_in:
    st.warning("Please LogIn. Go to the Homepage and Hit the button!")
    st.stop()
else:
    st.sidebar.button("Log out", on_click=st.logout)
    st.title("Evaluate your assets")


 # ###################################################
    mx1, mx2, mx3 = st.columns([2, 4, 2])
    with mx1:
        st.write(' ')
    with mx2:
        st.title(":ValuationModels:")
        st.markdown("""**Find out how much an asset is worth or if a transaction is
                    profitable compared to its peers.**""")
    with mx3:
        st.write(' ')


    with st.form(key="Input Assset Info", enter_to_submit=True, border=True):
        stock = st.selectbox("Choose Stock Ticker", tickerlist)
        stock_m = st.selectbox('Choose the Base Index', stock_m_list)
        slider_val = st.slider("Expected Volatility")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if not submitted:
            st.stop()
        if submitted:
            stock_a = stock + ".NS"
            pass


    @st.cache_resource
    def CAPM(stock_a, stock_m):
        stock_a1 = yf.Ticker(stock_a)
        stock_m1 = yf.Ticker(stock_m)
        data_a = stock_a1.history(period='max')['Close']
        data_m = stock_m1.history(period='max')['Close']

        ME_stock_a = data_a.resample('ME').last()
        ME_stock_m = data_m.resample('ME').last()
        data = pd.DataFrame({'Inv_Close': ME_stock_a,
                             'Markt_Close': ME_stock_m})
        data[['Inv_Ret', 'Markt_Ret']] = np.log(
            data[['Inv_Close',
                  'Markt_Close']]/data[['Inv_Close',
                                        'Markt_Close']].shift(1))
        data.dropna(inplace=True)
        beta_reg, alpha = np.polyfit(x=data['Markt_Ret'],
                                     y=data['Inv_Ret'], deg=1)
        st.write('\n')
        al0 = alpha.round(4)
        alpha_m = 100*al0
        st.write(25*'==')
        st.metric('Calculated Beta - Linear Regression: ',
                  beta_reg.round(4))
        st.metric('Calculated Alpha: ', alpha_m)
        st.write(25*'==')
        plt.figure(figsize=(13, 9))
        plt.axvline(0, color='grey', alpha=0.5)
        plt.axhline(0, color='grey', alpha=0.5)
        sns.scatterplot(y='Inv_Ret', x='Markt_Ret',
                        data=data, label='Returns')
        sns.lineplot(x=data['Markt_Ret'],
                     y=alpha + data['Markt_Ret']*beta_reg,
                     color='red', label='CAPM Line')
        plt.xlabel('Market Monthly Return: {}'.format(stock_m[0]))
        plt.ylabel('Investment Monthly Return: {}'.format(stock_a[0]))
        plt.legend(bbox_to_anchor=(1.01, 0.8), loc=2, borderaxespad=0.)
        st.pyplot(plt)

    #        CAPM(stock_a, stock_m)


    @st.cache_resource
    def CAPM_daily(stock_a, stock_m):
        stock_a1 = yf.Ticker(stock_a)
        stock_m1 = yf.Ticker(stock_m)
        data_a = stock_a1.history(period='max')['Close']
        data_m = stock_m1.history(period='max')['Close']
        # ME_stock_a = data_a.resample('ME').last()
        # ME_stock_m = data_m.resample('ME').last()
        data = pd.DataFrame({'Inv_Close': data_a, 'Markt_Close': data_m})
        data[['Inv_Ret', 'Markt_Ret']] = np.log(
            data[['Inv_Close',
                  'Markt_Close']]/data[['Inv_Close',
                                        'Markt_Close']].shift(1))
        data.dropna(inplace=True)

        beta_reg, alpha = np.polyfit(x=data['Markt_Ret'],
                                     y=data['Inv_Ret'], deg=1)
        st.write('\n')
        al = alpha.round(4)
        alpha_d = al*100
        st.write(20*'==')
        st.metric('Beta - Linear Regression: ', beta_reg.round(4))
        st.metric('Alpha: ', alpha_d.round(4))
        st.write(20*'==')
        plt.figure(figsize=(13, 9))
        plt.axvline(0, color='grey', alpha=0.5)
        plt.axhline(0, color='grey', alpha=0.5)

        sns.scatterplot(y='Inv_Ret',
                        x='Markt_Ret',
                        data=data, label='Returns')
        sns.lineplot(x=data['Markt_Ret'],
                     y=alpha + data['Markt_Ret']*beta_reg,
                     color='red', label='CAPM Line')

        plt.xlabel('Market Monthly Return: {}'.format(stock_m[0]))
        plt.ylabel('Investment Monthly Return: {}'.format(stock_a[0]))
        plt.legend(bbox_to_anchor=(1.01, 0.8), loc=2, borderaxespad=0.25)
        st.pyplot(plt)


    #        CAPM_daily(stock_a, stock_m)
        pass


    st.header("Part1: Critical Asset Pricing Model")

    v11, v12 = st.columns([1, 1])
    with v11:
        st.subheader('1A. CAPM Plot: Monthly')
        CAPM(stock_a, stock_m)
    with v12:
        st.subheader('1B. CAPM Plot: Daily')
        CAPM_daily(stock_a, stock_m)

    st.write('------------------------------------------------------------------')
    # Part II #####################################################################
    ticker = yf.Ticker(stock_a)
    stock_price = ticker.history(period='1y')['Close'][1]
    # stock_price = stock_price.last()
    st.write("Stock Price", stock_price)

    info = ticker.info
    info = pd.DataFrame([info])
    info = info.rename(columns={0: 'Items', 1: 'Description'})
    info.reset_index()
    # info = info.set_index(['Items'])
    pnl = ticker.financials
    bsheet = ticker.balancesheet
    cflow = ticker.cashflow
    df_pnl = pd.DataFrame.from_dict(pnl)
    df_cflow = pd.DataFrame.from_dict(cflow)
    df_bsheet = pd.DataFrame.from_dict(bsheet)
    ##############################################################################
    pnl2 = df_pnl.reset_index(level=None, drop=False, inplace=False, col_level=0)
    cflow2 = df_cflow.reset_index(level=None, drop=False, inplace=False,
                                  col_level=0, col_fill="")
    bsheet2 = df_bsheet.reset_index(level=None, drop=False, inplace=False,
                                    col_level=0, col_fill="")
    pnl2 = pnl2.set_index('index')
    bsheet2 = bsheet2.set_index('index')
    cflow2 = cflow2.set_index('index')
    ###############################################################################
    with st.container(border=True):
        st.header("Part2: Firm's Financial Statements")
        st.write('------------------------------------------')
        t1, t2, t3 = st.tabs(["Income Statement", "Balance Sheet",
                              "Cash Flow Statement"])
        with t1:
            st.caption(f'{stock}\'s Income Statement')
            st.dataframe(pnl2)
        with t2:
            st.caption(f"{stock}\'s Balance Sheet")
            st.dataframe(bsheet2)
        with t3:
            st.caption(f'{stock}\'s Cash Flow Statement')
            st.dataframe(cflow2)


    ##############################################################################
    st.write('------------------------------------------------------------------')
    try:
        accounts_receivable = bsheet2.loc["Accounts Receivable"][0]
    except Exception:
        pass

    try:
        accounts_payable = bsheet2.loc["Accounts Payable"][0]
    except Exception:
        accounts_payable = 0
        pass

    try:
        inventory = bsheet2.loc["Inventory"][0]
    except Exception:
        inventory = 1
        pass

    try:
        taxes_payable = bsheet2.loc["Total Tax Payable"][0]
    except Exception:
        pass

    try:
        current_liabilities = bsheet2.loc["Current Liabilities"][0]
    except Exception:
        current_liabilities = bsheet2.loc['Current Liabilities'][1]
    else:
        pass
    try:
        cash = bsheet2.loc["Cash Financial"][0]
    except Exception:
        pass
    try:
        cost_of_rev = pnl2.iloc["Cost of Revenue"]
    except Exception:
        cost_of_rev = "Insufficient Data"
        pass


    try:
        current_assets = bsheet2.loc['Current Assets'][0]
    except Exception:
        current_assets = cash + accounts_receivable + inventory
        pass


    try:
        book_value = bsheet2.loc['Tangible Book Value'][0]
    except Exception:
        book_value = 'Insufficient Data'
        pass


    try:
        equity = bsheet2.loc['Stockholders Equity'][0]
    except Exception:
        equity = 'Data Unreported'
        pass

    try:
        shares_outstanding = bsheet2.loc['Share Issued'][0]
    except Exception:
        shares_outstanding = 'Data Unreported'
        pass


    try:
        book_value_per_share = book_value/shares_outstanding
    except Exception:
        book_value_per_share = 1

    try:
        cash_flow_from_operations = cflow2.loc['Operating Cash Flow'][0]
    except Exception:
        cash_flow_from_operations = st.warning("In the works")
        pass

    try:
        OPEX = pnl2.loc['Operating Expense'][0]
    except Exception:
        OPEX = "In the works"
        pass

    try:
        sga = pnl2.loc['Selling General And Administration'][0]
    # COGS =
    except Exception:
        sga = "Data Unreported"
        pass


    try:
        total_rev = pnl2.loc['Total Revenue'][0]
    except Exception:
        total_rev = "Data Unreported"
        pass
    try:
        net_income = pnl2.loc['Net Income'][0]
    except Exception:
        net_income = "Data Unreported"
        pass
    try:
        net_revenues = pnl2.loc['EBITDA'][0]
    except Exception:
        net_revenues = pnl2.loc['Normalized EBITDA'][0]
    else:
        pass

    try:
        op_rev = pnl2.loc['Operating Revenue'][0]
    except Exception:
        op_rev = "Data Unreported"
        pass

    try:
        total_assets = pnl2.loc['Operating Revenue'][0]  # ??
    except Exception:
        total_assets = pnl2.loc['Operating Revenue'][1]  # ??
    else:
        total_assets = "Data Unreported"
        pass


    try:
        shareholders_equity = bsheet2.loc['Stockholders Equity'][0]
    except Exception:
        shareholders_equity = "Data Unreported"
        pass
    try:
        cash_eqv = bsheet2.loc['Cash And Cash Equivalents'][0]
    except Exception:
        cash_eqv = "Data Unreported"
        pass

    try:
        eps = pnl2.loc['Basic EPS'][0]
    except Exception:
        eps = 'Data Unreported'


    try:
        cash_eqv2 = bsheet2.loc['Cash Cash Equivalents & Short Term Investments'][0]
    except Exception:
        pass


    try:
        working_capital = bsheet2.loc['Working Capital'][0]
    except Exception:
        working_capital = "Data Unreported"
        pass

    try:
        gross_profit = pnl2.loc['Gross Profit'][0]
    except Exception:
        gross_profit = "Data Unreported"
        pass

    try:
        total_debt = bsheet2.loc['Total Debt'][0]
    except Exception:
        total_debt = "Data Unreported"
        pass

    try:
        total_liabilities = bsheet2.loc['Total Liabilities'][0]
    except Exception:
        total_liabilities = bsheet2.loc['Total Liabilities Net Minority Interest'][0]
    else:
        pass


    try:
        interest_expenses = pnl2.loc['Interest Expense Non Operating'][0]
    except Exception:
        interest_expenses = "Data Unreported"
        pass

    try:
        ebitda = pnl2.loc['EBITDA'][0]
    except Exception:
        ebitda = "Data Unreported"
        pass

    try:
        current_debt = bsheet2.loc['Current Debt'][0]
    except Exception:
        current_debt = "Data Unreported"
        pass

    try:
        ebit = pnl2.loc["EBIT"][0]
    except Exception:
        ebit = "Data Unreported"
        pass

    try:
        cost_of_revenue = pnl2.loc['Cost Of Revenue'][0]
    except Exception:
        cost_of_revenue = "Data Unreported"
        pass

    try:
        dividends = bsheet2.loc['Dividends Payable'][0]
    except Exception:
        dividends = 0
        pass

    try:
        net_sales = total_rev - cost_of_revenue
    except Exception:
        net_sales = "Data Insufficient"
        pass

    try:
        op_profits = op_rev - OPEX
        op_profits = op_profits.round(4)
    except Exception:
        op_profits = "Data Unreported"
        pass

    try:
        net_profit = 0.7*gross_profit
    except Exception:
        net_profit = "Data Unreported"
        pass

    try:
        cr = current_assets/current_liabilities
    except Exception:
        cr = st.warning("Data Unreported")
        pass


    try:
        acr = (cash + accounts_receivable)/current_liabilities
        acr = acr.round(4)
    except Exception:
        acr = (cash_eqv2/current_liabilities)
        acr = acr.round(4)
        pass


    try:
        c_ratio1 = cash_eqv/current_liabilities
    except Exception:
        c_ratio1 = 'In the Works'
    try:
        c_ratio2 = cash_eqv2/current_liabilities
    except Exception:
        c_ratio2 = 'In the Works'
        pass

    try:
        ocfr = cash_flow_from_operations/current_liabilities
        ocfr = ocfr.round(3)
    except Exception:
        ocfr = 'In the Works'
        pass


    try:
        cogs = total_rev - gross_profit
        cogs = cogs.round(3)
    except Exception:
        cogs = 'In the Works'
        pass

    try:
        der = total_liabilities/shareholders_equity
    except Exception:
        der = 'In the Works'
        pass

    try:
        icr = ebit/interest_expenses
        icr = icr.round(4)
    except Exception:
        icr = 'In the Works'
        pass


    try:
        atr = net_sales/total_rev
        atr = atr.round(3)
    except Exception:
        atr = 'In the Works'
        pass

    try:
        itr = cogs/inventory
    except Exception:
        itr = 'In the Works'
        pass

    try:
        dsi = (inventory*365)/cogs
    except Exception:
        dsi = 'In the Works'
        pass

    try:
        gmr = (total_rev - cogs)/net_revenues
    except Exception:
        gmr = 'Absent Data'
        pass

    try:
        omr = 100*op_profits/op_rev
    except Exception:
        omr = 'Absent Record'
        pass

    try:
        roe = 100*net_profit/shareholders_equity
    except Exception:
        roe = 'Absent Record'
        pass

    bvps = book_value/shares_outstanding
    pbr = stock_price/bvps
    # pbr = round(pbr, 3)

    try:
        p_s = (stock_price*shares_outstanding)/total_rev
    except Exception:
        p_s = 'Insufficient Data'
        pass

    try:
        bvps = book_value/shares_outstanding
        mbr = stock_price/bvps
        mbr = mbr.round(4)
    except Exception:
        mbr = 'In the Works'
        pass

    try:
        ceps = net_income/shares_outstanding
        ceps = ceps.round(3)
    except Exception:
        ceps = 'Invalid Outputs'
        pass

    try:
        dps = dividends/shares_outstanding
        dps = dps.round(3)
    except Exception:
        dps = 'In the Works'
        pass

    try:
        dpr = dividends/net_income
        dpr = dpr.round(3)
    except Exception:
        dpr = 'In the Works'
        pass

    pe = shares_outstanding*stock_price/net_income
    pe = pe.round(3)


    #####################################################################
    with st.container(border=True):
        u1, u2, u3, u4, u5 = st.columns([1, 1, 1, 1, 1])
        with u1:
            st.metric("Net Income (Cr.)", net_income/10000000)
        with u2:
            st.metric("Current Assets (Cr.)", current_assets/10000000)
        with u3:
            st.metric("Operating Profits (Cr.)", op_profits/10000000)
        with u4:
            st.metric("Operating Cash Flow", cash_flow_from_operations/10000000)
        with u5:
            st.metric("Gross Profit in (Cr.)", gross_profit/10000000)
    ###########################################################################

    # Pagework 2
    st.write('-------------------------------------------------------------------')
    st.title("Part 3: Financial Metrics")
    with st.container(border=True):
        st.header("1. Liquidity ratios.")
        st.info('''Compute the availability of a company’s underlying short-term
                assets, such as account receivables, to cover current liabilities,
                such as account payables.''')
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        g2, g3 = st.columns(2)
        with g2:
            st.metric("Current Assets in Cr.", current_assets/10000000)
        with g3:
            st.metric("Current Liabilities in Cr.", current_liabilities/10000000)

    with st.container(border=True):
        st.subheader("1A. Current-Ratio")
        st.info("""It tells investors and analysts how a company can maximize the
                current assets on its balance sheet to satisfy its current debt and
                other payables.
                A current ratio that is in line with the industry average or
                slightly higher is generally considered acceptable.""")
        st.metric("Current Ratio", cr)
        st.markdown("""A Firm with a CR less than one means that its Equity heavy
                    and shall not be able to manage its short term payouts""")

    with st.container(border=True):
        st.subheader("1B. Acid-Test-Ratio")
        st.info('''The acid-test ratio (or quick ratio) is calculated by dividing a
        company\'s quick assets by its current liabilities.''')
        g4, g5 = st.columns(2)
        with g4:
            st.metric("=>ACR=Quick assets(cash+accounts_rcv)/current liabilities",
                      acr)
        with g5:
            st.info("""A Firm with a CR less than one means that its Equity heavy
                     and shall not be able to manage its short term payouts""")


    with st.container(border=True):
        st.subheader("1C. Cash-Ratio")
        st.info('''Benchmark being around the value of 1, a higher Cash Ratio
                indicates that the firm is in good health, being able to deal
                with short and long term payments''')
        g6, g7 = st.columns(2)
        with g6:
            st.info("**=>Cash Ratio=(Cash + Cash Equivalents)÷Current Liabilities")
        with g7:
            st.metric("Cash Ratio)", c_ratio1)
        st.write("""If a Firm's cash ratio is around 0.6, it means that for every
                 dollar borrowed, it has only 0.6 dollars to pay back.""")

    with st.container(border=True):
        st.subheader("1D. Operating-Cash-Flow-Ratio")
        g8, g9 = st.columns(2)
        with g8:
            st.info('Measure how much a company earns against its borrowings.')
        with g9:
            st.metric("**=>OCFR = Total Revenue - (COGS -+OPEX)**", ocfr)
        st.write("=>OCFR = Cash Flow from Operations/Current Liabilities")

    st.write('-------------------------------------------------------------------')
    #################################################
    with st.container(border=True):
        st.header("2. Leverage or Debt Ratios.")
        st.success('''Leverage ratios help fathom whether a firm positioned
                   in terms of its short-term and long-term obligations.''')
        with st.container(border=True):
            g10, g11 = st.columns(2)
            with g10:
                st.metric("Total Debt in Cr.", total_debt/10000000)
            with g11:
                st.info('''Measure the level of debt the company takes on to
                        finance its operations, against the level of capital,
                        or available equity''')

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("2.1 Debt-to-Equity-Ratio")
        g12, g13 = st.columns(2)
        with g12:
            st.info('''The debt-to-equity ratio indicates how much portion of the
                    capital is borrowed and how much is invested in equity.''')
        st.write("""=>Debt-to-Equity:=(Total Liabilities)÷(Shareholders Equity)""")
        st.info('''If a company has a higher debt-to-equity ratio,
            it means it is leveraging more,
            and it is more vulnerable to interest rates.''')
        with g13:
            st.metric("Debt-to-Equity Ratio", der)

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("2.2 Interest-Coverage-Ratio")
        h14, h15 = st.columns(2)
        with h14:
            st.info('Gauge whether a firm can pay interest on its overall debt')
            st.write(
                '''A High ICR i.e. above 2.00 exhibits a firm\'s capacity to
                pay off all interests of short term debts''')
        with h15:
            st.metric("Interest Coverage Ratio", icr)

    st.write('-------------------------------------------------------------------')
    # ################################################
    with st.container(border=True):
        st.header("3. Efficiency ratios.")
        st.info("""Measure a firm's ability to use its assets to generate income.
                It often looks at various aspects of the company,
                such as the time it takes to collect cash from customers or,
                to convert inventory to cash.
                Improvements in efficiency ratio translates to profitability.""")
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("3.1 Asset-Turnover-Ratio")
        g16, g17 = st.columns(2)
        with g16:
            st.info('Measure how a company uses its assets to generate revenue.')
        with g17:
            st.metric("**=> ATR = Net Sales/Total Revenues**", atr.round(4))

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("3.2 Inventory-Turnover-Ratio")
        h17, h18 = st.columns(2)
        with h17:
            st.info('''Inventory turnover is the rate that inventory stock is sold,
                    or used, and replaced''')
        with h18:
            st.metric('**=>COGS/Avg. Value of Inventory**', itr.round(4))
        st.write('''Measures how many times a Firm\'s Inventory is used and
                 sold over a period''')

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("3.3 Day-Sales-in-Inventory-Ratio")
        g18, g19 = st.columns(2)
        with g18:
            st.info('Mark the avg days it takes to turn inventory into sales')
        with g19:
            st.metric("=>DSI = (Avg. Value of Inventory/COGS)X365: DSI",
                      dsi.round(4))
    st.write('-------------------------------------------------------------------')
    # ################################################
    with st.container(border=True):
        st.header("4. Profitability ratios.")
        st.info('''Measure and evaluate the ability of a company to generate
                income (profit) relative to revenue, balance sheet assets,
                operating costs, and shareholders’ equity during a specific period.
                They show how well a company utilizes its assets to produce profit
                and deliver value to shareholders.''')
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader("4.1 Gross-Margin-Ratio")
        g20, g21 = st.columns(2)
        with g20:
            st.info('''The gross margin ratio is a percentage that quantify gains
                    a company makes for each dollar of revenue.''')
        with g21:
            st.metric("**=>GMR = (Revenues - COGS)/Revenues**", gmr.round(4))
        st.write("""A higher ratio indicates that a company is efficiently managing
                 its costs and pricing""")
    st.write('-------------------------------------------------------------------')

    with st.container(border=True):
        st.subheader("4.2 Operating-Margin-Ratio")
        g22, g23 = st.columns(2)
        with g22:
            st.info('Measure a company\'s operating profit against its revenues')
        with g23:
            st.metric("**Operating Profits Margin**", omr.round(4))

    st.write('-------------------------------------------------------------------')
    #####
    with st.container(border=True):
        st.subheader("4.3 Return-on-Equity")
        g24, g25 = st.columns(2)
        with g24:
            st.info('Assess company’s net profit w,r.t its equity capital')
        with g25:
            st.metric("ROE = (Net Profit)÷Shareholder’s Equity", roe.round(4))
            # roe = net_profit/Average_Shareholders_Equity
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.header("5. Market value ratios. ")
        st.info("""Measure, analyze and compare stock prices against market prices,
                competitors accounting in other relevant writes.""")
        st.write("""Mark out the optimal price levels
                 at which a security's stock should be bought or sold. """)
    st.write("-------------------------------------------------------------------")
    with st.container(border=True):
        st.subheader('5.1 Book-Value')
        g42, g43 = st.columns(2)
        with g42:
            st.info("Gauge if the stock is worth buying.")
        with g43:
            st.metric("=>BV=Total Stockholders' Equity/Total Outstanding Shares",
                      book_value/10000000)
        st.write("""This is the valuation as reflected in the audited books
                 of the company.""")
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.2 Price-to-Book-Ratio')
        g28, g29 = st.columns(2)
        with g28:
            st.info("""Accounts in the firm's market value,
                    book value and Shares Outstanding. Firms with Low P-BV,
                    in certain scenarios, indicate a 'Buy',
                    given that one has considered other relevant factors.""")
        with g29:
            st.metric("P-B Ratio:", pbr.round(4))
        st.write("=>P-BV = (Market Price Per Share)÷(Book Value per share)")
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.3 Price-to-Sales-Ratio')
        h1, h2 = st.columns(2)
        with h1:
            st.info('Gauge a security\'s price vs its Sales Turnover')
            st.caption("P/S = (Price per Share) ÷ (Annual Sales Per Share)")
        with h2:
            st.metric("Price-to-Sales", p_s)
    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.4 Market-to-Book-Ratio')
        g32, g33 = st.columns(2)
        with g32:
            st.info('Market Value here refers to the stock price')
        with g33:
            st.metric("Market-to-Book Ratio:", mbr)


    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.6 Earnings-per-Share')
        g36, g37 = st.columns(2)
        with g36:
            st.info("EPS represents the earnings on every unit of stock you own.")
        with g37:
            st.metric("=>Calculated EPS = [Net Income]/(Outstanding Shares)", ceps)
        st.write(
            "=>EPS = [Net Profit-Preferred_Shares_Dividend]/(Shares_Outstanding)")

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.7 Dividend-per-Share')
        g38, g39 = st.columns(2)
        with g38:
            st.info('''Accounts for the sum of declared dividends issued by a firm
                    for every share outstanding.''')
        with g39:
            st.metric("Dividends Payable", dividends)
            st.write("Dividend-per-Share:", dps)

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.8 Price-to-Earnings-Ratio')
        g40, g41 = st.columns(2)
        with g40:
            st.info("Gauge if the stock is Over/Undervalued")
        with g41:
            st.metric("=>Calculated PE=(Price Per Share)÷(Earnings Per Share)", pe)
        st.write("""A PE ratio of 42 means that investors are willing to pay for
                 every ₹1 of the company's earnings per share(EPS)""")

    st.write('-------------------------------------------------------------------')
    with st.container(border=True):
        st.subheader('5.9 Dividend-Payout-Ratio')
        g44, g45 = st.columns(2)
        with g44:
            st.info('''(DPR) is the amount of dividends paid to shareholders
                    accounting in the total net income the company generates''')
        with g45:
            st.metric("**=>DPR = Total Dividends/Net Income**", dpr)
        st.write("**=>DPR = Dividends per share/Earnings per share**")
st.write('------------------------------------------------------------------')
url_ytube = "https://www.youtube.com/@LedgrInc"
url_fb = "https://www.facebook.com/share/1BnXaYvRzV/"
url_insta = 'https://www.instagram.com/alphaledgr/'
url_blog = 'https://www.alphaledgr.com/Blog'
url_linkedin = "https://www.linkedin.com/company/ledgrapp/"
st.write('------------------------------------------------------------------')
column1, column2, column3, column4, column5 = st.columns([1, 1, 1, 2, 1])
with column1:
    st.image(ytube, '[Ledgr\'s YouTube Channel](%s)' % url_ytube)
with column2:
    st.image(fbook, '[Ledgr\'s FaceBook Page ](%s)' % url_fb)
with column3:
    st.image(linkedin,  '[Our LinkedIn Page ](%s)' % url_linkedin)
with column4:
    st.write(" ")
    st.image(ledgrblog,  '[Ledgr\'s Blog ](%s)' % url_blog)
    st.write(" ")
with column5:
    st.image(insta,  '[Ledgr\'s @ Instagram ](%s)' % url_insta)
# # ###################################################################
with st.container():
    f9, f10, f11 = st.columns([1, 5, 1])
    with f9:
        st.write(" ")
    with f10:
        st.caption(
            ":2025:2026 - All Rights Reserved © Ledgr - www.alphaLedgr.com:")
    with f11:
        st.write(" ")
