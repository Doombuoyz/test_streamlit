import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
from crypto_data import get_crypto_data, get_price_history, MAIN_CRYPTOS
from st_theme import show_callout

def landing_page():
    """Main landing page with our four cryptocurrencies"""
    
    st.markdown('<h1 class="main-header">🚀 Crypto Dashboard</h1>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    ">
        <h2 style="color: #2d3748; margin-bottom: 1rem;">Welcome to the Crypto Dashboard!</h2>
        <p style="color: #4a5568; font-size: 1.1rem; line-height: 1.6;">
            Track live prices for Bitcoin, Ethereum, XRP, and Solana - the top cryptocurrencies in the market.
        </p>
        <p style="color: #2d3748; font-weight: bold; margin-top: 1rem;">
            <strong>Click on any cryptocurrency below to view detailed analysis and predictions!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get crypto data
    with st.spinner("Loading cryptocurrency data..."):
        crypto_data = get_crypto_data()
    
    # Display crypto overview
    st.subheader("📊 Top 4 Cryptocurrencies")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_market_cap = sum([coin.get('market_cap', 0) for coin in crypto_data])
        st.metric("Total Market Cap", f"${total_market_cap/1e12:.2f}T")
    
    with col2:
        avg_change = sum([coin.get('price_change_percentage_24h', 0) for coin in crypto_data]) / len(crypto_data)
        st.metric("Avg 24h Change", f"{avg_change:.2f}%")
    
    with col3:
        st.metric("Cryptocurrencies", "4")
    
    with col4:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    # Crypto selection grid - 2x2 layout
    st.subheader("🎯 Select a Cryptocurrency")
    
    # Create a 2x2 grid
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    cols = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    for idx, coin in enumerate(crypto_data):
        col = cols[idx]
        
        with col:
            # Create crypto card
            price_change = coin.get('price_change_percentage_24h', 0)
            change_color = "green" if price_change >= 0 else "red"
            change_symbol = "↗️" if price_change >= 0 else "↘️"
            
            # Use the coin's actual color for the border and better styling
            card_html = f"""
            <div style="
                background: rgba(255, 255, 255, 0.9);
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 6px solid {coin['color']};
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <h3 style="color: {coin['color']}; margin-bottom: 0.5rem;">
                    {coin['icon']} {coin['name']} ({coin['symbol']})
                </h3>
                <h4 style="color: #2d3748; font-weight: bold; margin: 0.5rem 0;">
                    ${coin.get('current_price', 0):,.2f}
                </h4>
                <p style="color: {change_color}; font-weight: bold; margin: 0.5rem 0;">
                    {change_symbol} {price_change:.2f}%
                </p>
                <p style="color: #4a5568; font-size: 0.9em; margin: 0;">
                    Market Cap: ${coin.get('market_cap', 0)/1e9:.1f}B
                </p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(f"View {coin['name']}", key=f"btn_{coin['id']}", use_container_width=True, type="primary"):
                st.session_state.selected_crypto = coin
                st.session_state.page = "crypto_detail"
                st.rerun()

def crypto_detail_page():
    """Detailed page for selected cryptocurrency"""
    
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
        st.markdown(f'<h1 class="main-header">{crypto["icon"]} {crypto["name"]} ({crypto["symbol"]}) Analytics</h1>', 
                   unsafe_allow_html=True)
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${crypto.get('current_price', 'N/A'):,.2f}",
            delta=f"{crypto.get('price_change_percentage_24h', 0):.2f}%"
        )
    
    with col2:
        market_cap = crypto.get('market_cap', 0)
        st.metric("Market Cap", f"${market_cap/1e9:.2f}B" if market_cap > 1e9 else f"${market_cap/1e6:.2f}M")
    
    with col3:
        st.metric("Symbol", crypto['symbol'])
    
    with col4:
        st.metric("24h Change", f"{crypto.get('price_change_percentage_24h', 0):+.2f}%")
    
    # Add Ethereum prediction section if ETH is selected
    if crypto['symbol'] == 'ETH':
        st.markdown("---")
        st.subheader("🔮 Ethereum Price Prediction")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            show_callout("""
            **🤖 AI-Powered ETH Prediction Available!**
            
            Our machine learning model can predict Ethereum's next-day HIGH price using:
            - 📈 Price momentum analysis
            - 📊 Volume patterns  
            - 🔄 Technical indicators
            - 🧠 Advanced feature engineering
            
            **Model Performance:** 99.14% R² Score
            """)
        
        with col2:
            if st.button("🤖 Get ETH Prediction", type="primary", use_container_width=True):
                with st.spinner("🔮 Generating prediction..."):
                    try:
                        response = requests.get("http://localhost:8000/predict/ETH", timeout=10)
                        
                        if response.status_code == 200:
                            prediction = response.json()
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
                                <h3>🎯 Next-Day HIGH Prediction</h3>
                                <h2>${pred_high:,.2f}</h2>
                                <p>Expected change: {change_pct:+.2f}%</p>
                                <small>Current Close: ${latest_close:,.2f}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show additional details
                            with st.expander("📊 Prediction Details"):
                                st.json(prediction)
                                
                        else:
                            st.error("❌ Prediction API not available")
                            st.info("💡 **Start the API:** `uvicorn app.main:app --reload --port 8000`")
                            
                    except Exception as e:
                        st.error(f"❌ Could not connect to prediction API")
                        st.info("💡 **Make sure your FastAPI server is running on port 8000**")
    
    # Price chart
    st.markdown("---")
    st.subheader("📈 Price History")
    
    # Time period selector
    period = st.selectbox(
        "Select Time Period",
        ["7d", "30d", "90d", "1y"],
        format_func=lambda x: {"7d": "7 Days", "30d": "30 Days", "90d": "90 Days", "1y": "1 Year"}[x]
    )
    
    # Get and display price history
    with st.spinner("Loading price history..."):
        yf_symbol = MAIN_CRYPTOS[crypto['id']]['yf_symbol']
        price_data = get_price_history(yf_symbol, period)
    
    if price_data is not None and not price_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=price_data['Close'],
            mode='lines',
            name='Price',
            line=dict(color=crypto['color'], width=3)
        ))
        
        fig.update_layout(
            title=f"{crypto['name']} Price History ({period})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode='x unified',
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Unable to load price history data.")
    
    # Crypto information section
    st.markdown("---")
    st.subheader("ℹ️ About " + crypto['name'])
    
    # Display information about each crypto
    crypto_info = {
        'bitcoin': {
            'description': 'Bitcoin (BTC) is the world\'s first cryptocurrency, created by the pseudonymous Satoshi Nakamoto. It operates on a decentralized peer-to-peer network and serves as digital gold.',
            'features': ['Digital Gold', 'Store of Value', 'Peer-to-Peer', 'Limited Supply (21M)']
        },
        'ethereum': {
            'description': 'Ethereum (ETH) is a decentralized platform that enables smart contracts and decentralized applications (DApps). It\'s the second-largest cryptocurrency by market cap.',
            'features': ['Smart Contracts', 'DApps Platform', 'DeFi Ecosystem', 'NFT Marketplace']
        },
        'ripple': {
            'description': 'XRP is a digital asset designed for payments and created by Ripple Labs. It aims to enable fast, low-cost international money transfers.',
            'features': ['Fast Payments', 'Low Fees', 'Bank Partnerships', 'Cross-border Transfers']
        },
        'solana': {
            'description': 'Solana (SOL) is a high-performance blockchain supporting crypto apps and marketplaces. Known for fast transactions and low fees.',
            'features': ['High Speed', 'Low Fees', 'Web3 Apps', 'NFT Ecosystem']
        }
    }
    
    if crypto['id'] in crypto_info:
        info = crypto_info[crypto['id']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.9);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                border-left: 4px solid {crypto['color']};
            ">
                <h4 style="color: {crypto['color']}; margin-bottom: 1rem;">📖 Description</h4>
                <p style="color: #2d3748; line-height: 1.6; font-size: 1rem;">
                    {info['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            features_html = ""
            for feature in info['features']:
                features_html += f'<li style="color: #4a5568; margin: 0.5rem 0; font-size: 1rem;">✨ {feature}</li>'
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.9);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                border-left: 4px solid {crypto['color']};
            ">
                <h4 style="color: {crypto['color']}; margin-bottom: 1rem;">⭐ Key Features</h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    {features_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Current Price",
            f"${crypto.get('current_price', 0):,.4f}",
            help="Live price from CoinGecko API"
        )
    
    with col2:
        market_cap = crypto.get('market_cap', 0)
        st.metric(
            "Market Cap Rank",
            f"#{['bitcoin', 'ethereum', 'ripple', 'solana'].index(crypto['id']) + 1}",
            help="Rank among our tracked cryptocurrencies"
        )
    
    with col3:
        change_24h = crypto.get('price_change_percentage_24h', 0)
        st.metric(
            "24h Performance",
            "Bullish" if change_24h > 0 else "Bearish",
            f"{change_24h:+.2f}%"
        )