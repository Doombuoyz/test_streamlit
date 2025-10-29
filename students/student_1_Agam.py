import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_btc_data(days):
    # Calculate timestamp for the specified days ago
    target_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
    url = f"https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD&interval=1440&since={target_timestamp}"
    response = requests.get(url)
    data = response.json()
    # Parse OHLC data
    ohlc = data['result']['XXBTZUSD']
    df = pd.DataFrame(ohlc, columns=['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df

def calculate_bollinger_bands(df, window=20):
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper'] = df['SMA'] + (df['STD'] * 2)
    df['Lower'] = df['SMA'] - (df['STD'] * 2)
    return df

def calculate_ema(df, span):
    return df['close'].ewm(span=span, adjust=False).mean()

def bitcoin_detail_page():
    # Layout with back button on top left
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("""
    <style>
    .big-title {
        font-size: 3em;
        text-align: center;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="big-title">BTC Dashboard</h1>', unsafe_allow_html=True)

    # Next Day High Prediction
    st.header("📈 Next Day High Prediction")
    st.markdown("---")
    with st.spinner("Waking up prediction API... Please wait for 2 min."):
        
        health_response = requests.get("https://bitcoin-prediction-api-rrfq.onrender.com/health/")
        
        if health_response.status_code == 200:
            st.success("API is awake and ready!")
            api_awake = True
        else:
            st.error("Failed to wake up API. Prediction may not work.")
            api_awake = False

    if api_awake:
        if st.button("Get Prediction"):
            today = datetime.now().strftime('%Y-%m-%d')
            response = requests.get(f"https://bitcoin-prediction-api-rrfq.onrender.com/predict/Bitcoin?date={today}")
            if response.status_code == 200:
                data = response.json()
                pred_date = data['prediction']['prediction_day_date']
                pred_high = data['prediction']['Predicted_high']
                st.metric(label=f"Predicted High for {pred_date}", value=f"${pred_high}")
            else:
                st.error("Failed to fetch prediction")
    else:
        st.warning("API is not awake. Waking up the API. Please try again in a minute.")
    

    # Data range selector
    data_range = st.selectbox("Select Data Range", ["Daily (7 days)", "6 Months"], index=1)  # Default to 6 Months

    if data_range == "Daily (7 days)":
        days = 7
        title_suffix = "(7 Days)"
        set_zoom = False
    else:
        days = 180
        title_suffix = "(6 Months)"
        set_zoom = True

    df = get_btc_data(days)
    df['EMA9'] = calculate_ema(df, 9)
    df['EMA21'] = calculate_ema(df, 21)

    # Display current price above the chart
    current_price = df['close'].iloc[-1]
    st.write(f"**Current BTC Price: ${current_price:.2f}**")


    # OHLC Section
    st.header("📈 Latest OHLC Values")
    st.markdown("---")
    latest = df.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open", f"${latest['open']:.2f}")
    with col2:
        st.metric("High", f"${latest['high']:.2f}")
    with col3:
        st.metric("Low", f"${latest['low']:.2f}")
    with col4:
        st.metric("Close", f"${latest['close']:.2f}")

    # Charts Section
    st.header("📊 Charts")
    st.markdown("---")

    # Graph 1: Candlestick with Volume
    fig1 = go.Figure()
    fig1.add_trace(go.Candlestick(x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='Candlestick'))
    fig1.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume', yaxis='y2', opacity=0.3))
    fig1.update_layout(
        title=dict(text=f'BTC Candlestick with Volume {title_suffix}', font=dict(size=24)),
        yaxis_title='Price (USD)',
        yaxis2=dict(title='Volume', overlaying='y', side='right'),
        xaxis_title='Date',
        hovermode='x unified'
    )
    if set_zoom:
        # Set default zoom to last 7 days for 6 months data
        end_date = df.index.max()
        start_date = end_date - timedelta(days=7)
        fig1.update_xaxes(range=[start_date, end_date])
    st.plotly_chart(fig1)

    # Graph 2: EMA Cross
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df.index, y=df['EMA9'], mode='lines', name='EMA 9', line=dict(color='red')))
    fig2.add_trace(go.Scatter(x=df.index, y=df['EMA21'], mode='lines', name='EMA 21', line=dict(color='darkblue')))
    fig2.update_layout(title=dict(text='BTC EMA Crossover', font=dict(size=24)), xaxis_title='Date', yaxis_title='Price (USD)', hovermode='x unified')
    st.plotly_chart(fig2)
