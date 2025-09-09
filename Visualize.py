import streamlit as st
import pandas as pd
from nsepython import equity_history
import mplfinance as mpf

st.title("NSE Equity Data (OHLCV Ready)")

ticker = st.text_input("Enter NSE symbol", "RELIANCE")
start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
end_date   = st.date_input("End date",   pd.to_datetime("2025-01-01"))

if st.button("Fetch Data"):
    data = equity_history(
        symbol=ticker,
        series="EQ",
        start_date=start_date.strftime("%d-%m-%Y"),
        end_date=end_date.strftime("%d-%m-%Y")
    )

    df = pd.DataFrame(data)

    if not df.empty:
        # Rename NSE column names -> mplfinance OHLCV
        rename_map = {
            "mTIMESTAMP": "Date",
            "CH_OPENING_PRICE": "Open",
            "CH_TRADE_HIGH_PRICE": "High",
            "CH_TRADE_LOW_PRICE": "Low",
            "CH_CLOSING_PRICE": "Close",
            "CH_TOT_TRADED_QTY": "Volume"
        }
        df = df.rename(columns=rename_map)

        # Convert Date to datetime and set as index
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df.set_index("Date", inplace=True)

        # Show renamed OHLCV table
        st.subheader("Renamed OHLCV Table")
        st.dataframe(df[["Open", "High", "Low", "Close", "Volume"]])

        # Plot candlestick chart
        st.subheader("Candlestick Chart")
        fig, ax = mpf.plot(
            df,
            type="candle",
            style="yahoo",
            volume=True,
            figsize=(10, 6),
            returnfig=True
        )
        st.pyplot(fig)
    else:
        st.warning("No data returned from NSE.")
