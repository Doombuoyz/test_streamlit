import streamlit as st
import requests
import plotly.graph_objects as go
import sys
import os

# Add the parent directory to Python path to enable imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path: 
    sys.path.append(parent_dir)

# Now import from app directory
from app.crypto_data import get_price_history, MAIN_CRYPTOS
from app.st_theme import show_callout

def ethereum_detail_page():
    """Ethereum detailed page with ML prediction"""
    
    if 'selected_crypto' not in st.session_state:
        st.error("No cryptocurrency selected. Please go back to the landing page.")
        if st.button("← Back to Landing Page"):
            st.session_state.page = "landing"
            st.rerun()
        return
    
    crypto = st.session_state.selected_crypto
    
    # Header with back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Landing"):
            st.session_state.page = "landing"
            st.rerun()
    
    with col2:
        st.markdown(f'<h1 class="main-header">Ξ Ethereum (ETH) - Smart Contract Platform</h1>', 
                   unsafe_allow_html=True)
    
    # Ethereum-specific metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${crypto.get('current_price', 0):,.2f}", delta=f"{crypto.get('price_change_percentage_24h', 0):.2f}%"
        )
    
    with col2:
        market_cap = crypto.get('market_cap', 0)
        st.metric(
            "Market Cap", 
            f"${market_cap/1e9:.2f}B",
            delta="+3,247%"
        )
    
    with col3:
        st.metric(
            "Gas Price", 
            "~25 Gwei", 
            delta="-15%",
            help="Current network fee"
        )
    
    with col4:
        st.metric(
            "Total Supply", 
            "120M+ ETH", 
            delta="+0.05%",
            help="Current circulating supply"
        )


    # Price Chart
    st.markdown("---")
    st.subheader("Ethereum Price History")
    
    period = st.selectbox(
        "Select Time Period",
        ["7d", "30d", "90d", "1y"],
        format_func=lambda x: {"7d": "7 Days", "30d": "30 Days", "90d": "90 Days", "1y": "1 Year"}[x]
    )
    
    with st.spinner("Loading Ethereum price history..."):
        price_data = get_price_history("ETH-USD", period)
    
    if price_data is not None and not price_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=price_data['Close'],
            mode='lines',
            name='ETH Price',
            line=dict(color='#627EEA', width=3)
        ))
        
        fig.update_layout(
            title=f"Ethereum Price History ({period})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode='x unified',
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # AI PREDICTION SECTION
    st.markdown("---")
    st.subheader("Ethereum AI Price Prediction")
    
    # Single line prediction button
    if st.button("Get ETH Prediction", type="primary", use_container_width=True):
        with st.spinner("Generating prediction..."):
            try:
                st.info("Connecting to: SUPER AI PREDICTION API")
                response = requests.get("https://student-api-25156985.onrender.com/predict/ETH", timeout=60)
                
                st.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    prediction = response.json()
                    st.success("API Response received successfully!")
                    pred_high = prediction.get('pred_high_next', 0)
                    latest_close = prediction.get('latest_close', 0)
                    change_pct = ((pred_high - latest_close) / latest_close * 100)
                    
                    # Display prediction in a nice box
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #4CAF50, #45a049);
                        color: white;
                        padding: 1.5rem;
                        border-radius: 15px;
                        text-align: center;
                        margin: 1rem 0;
                        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
                    ">
                        <h3>Next-Day HIGH Prediction</h3>
                        <h2>${pred_high:,.2f}</h2>
                        <p>Expected change: {change_pct:+.2f}%</p>
                        <small>Current Close: ${latest_close:,.2f}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show additional details
                    with st.expander("Prediction Details"):
                        st.json(prediction)
                        
                else:
                    st.error(f"API returned status code: {response.status_code}")
                    st.error(f"Response text: {response.text}")
                    st.info("**Start the API:** `uvicorn app.main:app --reload --port 8000`")
                    
            except requests.exceptions.Timeout:
                st.error("Request timed out - API is taking too long to respond")
                st.info("**Your Render service might be sleeping. Try again in a few seconds.**")
            except requests.exceptions.ConnectionError:
                st.error("Connection error - Cannot reach the API server")
                st.info("**Check if your Render deployment is running**")
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.error(f"Error type: {type(e).__name__}")
                st.info("**Make sure your FastAPI server is running on port 8000**")

    # Ethereum Ecosystem
    st.markdown("---")
    st.subheader("Ethereum Ecosystem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #627EEA, #4A67D6);
            color: white;
            padding: 1.8rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(98, 126, 234, 0.3);
        ">
            <h4 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.2rem;">DeFi Protocols</h4>
            <p style="margin-bottom: 0; font-size: 1rem; line-height: 1.5;">Uniswap, Aave, Compound</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #627EEA, #4A67D6);
            color: white;
            padding: 1.8rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(98, 126, 234, 0.3);
        ">
            <h4 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.2rem;">NFT Markets</h4>
            <p style="margin-bottom: 0; font-size: 1rem; line-height: 1.5;">OpenSea, SuperRare</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #627EEA, #4A67D6);
            color: white;
            padding: 1.8rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(98, 126, 234, 0.3);
        ">
            <h4 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.2rem;">Layer 2 Solutions</h4>
            <p style="margin-bottom: 0; font-size: 1rem; line-height: 1.5;">Polygon, Arbitrum</p>
        </div>
        """, unsafe_allow_html=True)