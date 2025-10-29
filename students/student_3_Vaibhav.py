import os
import math
import json
import time
import requests
import numpy as np
import pandas as pd
import streamlit as st

def xrp_detail_page():
    # ---------- Page setup ----------
    st.set_page_config(page_title="Ripple (XRP) Dashboard", page_icon="💠", layout="wide")

    col1, _ = st.columns([1, 5])
    with col1:
        if st.button("← Back to Landing"):
            st.session_state.page = "landing"
            st.rerun()
    
    st.title("💠 Ripple (XRP) — Investor Dashboard")
    st.caption("Historical analytics + next-day HIGH prediction (via FastAPI).")

    # ---------- Sidebar controls ----------
    st.sidebar.header("Controls")

    # CoinGecko days (used by your FastAPI too)
    days = st.sidebar.slider("History window (days)", min_value=30, max_value=365, value=90, step=10)

    # FastAPI backend URL (try to read from secrets or env first)
    default_api = (
        #st.secrets.get("https://at3-fastapi.onrender.com", None)
        #or os.environ.get("FASTAPI_URL", None)
        #or "http://localhost:8000"
        "https://at3-fastapi.onrender.com"
    )
    api_base = st.sidebar.text_input("FastAPI URL", value=default_api, help="e.g., http://localhost:8000")

    st.sidebar.caption("Make sure your FastAPI is running and reachable from this machine.")

    # ---------- Data fetch (CoinGecko) ----------
    COINGECKO_BASE = "https://api.coingecko.com/api/v3"
    XRP_ID = "ripple"

    @st.cache_data(show_spinner=True, ttl=300)
    def fetch_xrp_coingecko(days: int) -> pd.DataFrame:
        """Return daily XRP df with ['timestamp','close','volume','marketCap'] ascending."""
        url = f"{COINGECKO_BASE}/coins/{XRP_ID}/market_chart"
        params = {"vs_currency": "usd", "days": str(days)}
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        data = r.json()

        prices = pd.DataFrame(data.get("prices", []), columns=["ts", "price"])
        caps   = pd.DataFrame(data.get("market_caps", []), columns=["ts", "marketCap"])
        vols   = pd.DataFrame(data.get("total_volumes", []), columns=["ts", "volume"])

        if prices.empty:
            return pd.DataFrame(columns=["timestamp","close","volume","marketCap"])

        df = prices.merge(caps, on="ts", how="left").merge(vols, on="ts", how="left")
        df["timestamp"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        df = df.set_index("timestamp").sort_index()

        daily = pd.DataFrame({
            "close":     df["price"].resample("1D").last(),
            "volume":    df["volume"].resample("1D").last(),
            "marketCap": df["marketCap"].resample("1D").last(),
        }).dropna(subset=["close"]).reset_index()

        # ensure numeric
        for c in ["close","volume","marketCap"]:
            daily[c] = pd.to_numeric(daily[c], errors="coerce")

        daily = daily.dropna(subset=["timestamp","close"]).sort_values("timestamp").reset_index(drop=True)
        return daily[["timestamp","close","volume","marketCap"]]

    # ---------- Load data ----------
    with st.spinner("Fetching XRP data from CoinGecko..."):
        try:
            df = fetch_xrp_coingecko(days)
        except Exception as e:
            st.error(f"Failed to load data: {e}")
            st.stop()

    if df.empty:
        st.warning("No data returned from CoinGecko. Try a larger window or check network.")
        st.stop()

    # ---------- Derived metrics ----------
    df["return"] = np.log(df["close"]).diff()
    df["vol_30d"] = df["return"].rolling(30).std() * np.sqrt(365)  # ann. vol (approx)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) >= 2 else last_row

    last_close = float(last_row["close"])
    pct_chg_1d = float((last_row["close"] / (prev_row["close"] if prev_row["close"] else last_row["close"]) - 1) * 100)
    mcap = float(last_row["marketCap"]) if not math.isnan(last_row["marketCap"]) else None
    ann_vol = float(last_row["vol_30d"]) if not math.isnan(last_row["vol_30d"]) else None

    # ---------- Top metrics row ----------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Last Close (USD)", f"${last_close:,.4f}", f"{pct_chg_1d:+.2f}% / 1d")
    c2.metric("Market Cap", f"${mcap:,.0f}" if mcap is not None else "—")
    c3.metric("Ann. Vol (30d, log returns)", f"{ann_vol:.2%}" if ann_vol is not None else "—")
    c4.metric("Data as of (UTC)", last_row["timestamp"].strftime("%Y-%m-%d"))

    st.divider()

    # ---------- Charts ----------
    import altair as alt
    alt.data_transformers.disable_max_rows()

    price_chart = (
        alt.Chart(df)
          .mark_line()
          .encode(
              x=alt.X("timestamp:T", title="Date"),
              y=alt.Y("close:Q", title="Close (USD)"),
              tooltip=[alt.Tooltip("timestamp:T", title="Date"), alt.Tooltip("close:Q", format="$.4f")]
          )
          .properties(height=320)
    )

    # Add MAs
    for w in [7, 14]:
        df[f"ma_{w}"] = df["close"].rolling(w).mean()

    ma7 = alt.Chart(df).mark_line(opacity=0.7).encode(x="timestamp:T", y=alt.Y("ma_7:Q", title=""), color=alt.value("#888"))
    ma14 = alt.Chart(df).mark_line(opacity=0.7).encode(x="timestamp:T", y=alt.Y("ma_14:Q", title=""), color=alt.value("#aaa"))

    st.subheader("Price (Close) — with 7/14-day moving averages")
    st.altair_chart(price_chart + ma7 + ma14, use_container_width=True)

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Volume (daily)")
        vol_chart = (
            alt.Chart(df)
              .mark_bar()
              .encode(
                  x=alt.X("timestamp:T", title="Date"),
                  y=alt.Y("volume:Q", title="Volume"),
                  tooltip=[alt.Tooltip("timestamp:T"), alt.Tooltip("volume:Q", format=",.0f")]
              )
              .properties(height=240)
        )
        st.altair_chart(vol_chart, use_container_width=True)

    with colB:
        st.subheader("Market Cap (daily)")
        mcap_chart = (
            alt.Chart(df)
              .mark_line()
              .encode(
                  x=alt.X("timestamp:T", title="Date"),
                  y=alt.Y("marketCap:Q", title="Market Cap (USD)"),
                  tooltip=[alt.Tooltip("timestamp:T"), alt.Tooltip("marketCap:Q", format="$.0f")]
              )
              .properties(height=240)
        )
        st.altair_chart(mcap_chart, use_container_width=True)

    st.divider()

    st.subheader("🔮 Next-Day HIGH Prediction (FastAPI)")

    def _debug_response(resp):
        try:
            st.code(resp.text[:2000], language="json")
        except Exception:
            st.text(resp.text[:2000])

    api_ok = False
    if api_base:
        try:
            # Try both /predict/ and /predict/ripple/, and pass ?days= to match the sidebar
            candidate_urls = [
                f"{api_base.rstrip('/')}/predict/?days={days}",
                f"{api_base.rstrip('/')}/predict/ripple/?days={days}",
            ]
            pred_url = None
            for u in candidate_urls:
                r = requests.get(u, timeout=60)
                if r.status_code not in (404, 405):  # found a usable route
                    pred_url = u
                    break

            if pred_url is None:
                st.error("Prediction endpoint not found (tried /predict/ and /predict/ripple/). Check your FastAPI routes.")
            else:
                if st.button("Get Prediction"):
                    with st.spinner("Calling FastAPI…"):
                        resp = requests.get(pred_url, timeout=45)
                        if resp.ok:
                            payload = resp.json()
                            # Only read the fields we actually want; use .get() to avoid KeyErrors
                            pred_high = payload.get("predicted_high_usd", None)
                            as_of = payload.get("as_of", "")
                            pred_day = payload.get("prediction_day", "")

                            col1, col2, col3 = st.columns(3)
                            col1.metric(
                                "Predicted Next-Day HIGH (USD)",
                                f"${pred_high:,.6f}" if pred_high is not None else "—"
                            )
                            col2.metric("As of (UTC)", as_of.split("T")[0] if as_of else "—")
                            col3.metric("Prediction Day", pred_day.split("T")[0] if pred_day else "—")

                            with st.expander("Raw response"):
                                st.json(payload)
                        else:
                            st.error(f"Prediction failed ({resp.status_code})")
                            _debug_response(resp)
            api_ok = True
        except requests.RequestException as e:
            st.error(f"Could not reach FastAPI: {e}")
        
    st.caption("Data: CoinGecko • Times are UTC • Educational use only, not financial advice.")