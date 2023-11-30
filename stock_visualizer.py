import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import requests
import spacy


# Streamlit app title
st.title("Interactive Stock Data Viewer")


# User inputs
ticker = st.text_input("Enter the stock ticker symbol (e.g., AAPL):")
start_date = st.date_input("Select the start date:")
end_date = st.date_input("Select the end date:")


# Create four columns for the buttons side by side
col1, col2, col3, col4 = st.columns(4)

with col1:
    fetch_download_csv = st.button("Show Table")

with col2:
    fetch_graph_button = st.button("Graph Data")

with col3:
    fetch_news_button = st.button("Fetch News")

with col4:
    fetch_statistics = st.button("Statistics")

# Check if the "Fetch News" button is clicked
if fetch_graph_button:

    # Check if inputs are provided and fetch data only if all inputs are available
    if ticker and start_date and end_date:
        # Ensure the start date is earlier than the end date
        if start_date > end_date:
            st.error("Error: Start date should be before the end date.")
        else:
            # Fetch historical data
            data = yf.download(ticker, start=start_date, end=end_date)
            
            # Calculate 50-Day SMA
            data['SMA_50'] = data['Close'].rolling(window=50).mean()

            # Calculate 20-Day EMA
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

            # Create an interactive candlestick chart with volume, SMA, and EMA
            candlestick_chart = go.Figure()

            # Add candlestick trace
            candlestick_chart.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                hovertext=data['Close'],  # Display the 'Close' value on hover
                hoverinfo="x+text",  # Show both date and close value on hover
                name="Candlestick"
            ))

            # Add volume trace
            candlestick_chart.add_trace(go.Bar(
                x=data.index,
                y=data['Volume'],
                name="Volume",
                marker_color='rgba(0, 0, 255, 0.5)',
                opacity=0.5,
                yaxis='y2',  # Use the secondary y-axis for volume
                hoverinfo="y"  # Display the volume value on hover
            ))

            # Add 50-Day SMA trace
            candlestick_chart.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_50'],
                mode='lines',
                name="50-Day SMA",
                line=dict(color='orange', width=2),
                yaxis='y',  # Use the primary y-axis for SMA and EMA
                hoverinfo="y"  # Display the SMA value on hover
            ))

            # Add 20-Day EMA trace
            candlestick_chart.add_trace(go.Scatter(
                x=data.index,
                y=data['EMA_20'],
                mode='lines',
                name="20-Day EMA",
                line=dict(color='green', width=2),
                yaxis='y',  # Use the primary y-axis for SMA and EMA
                hoverinfo="y"  # Display the EMA value on hover
            ))

            # Customize the layout of the chart
            candlestick_chart.update_layout(
                title=f'{ticker} Interactive Candlestick Chart with Volume, 50-Day SMA, and 20-Day EMA',
                xaxis_title="Date",
                yaxis_title="Price",
                yaxis2=dict(
                    title="Volume",
                    overlaying='y',
                    side='right',
                ), height = 700, width = 900
            )


            # Display the interactive chart using Streamlit
            st.plotly_chart(candlestick_chart)

    else:
        st.warning("Please enter values for the stock ticker and date range.")


if fetch_news_button:
    # Check if inputs are provided and fetch graph data only if all inputs are available
    if ticker and start_date and end_date:
        # Ensure the start date is earlier than the end date
        if start_date > end_date:
            st.error("Error: Start date should be before the end date.")
        else:
            # Fetch historical data and display the graph
            # Get the name of the ticker using yfinance
            ticker_info = yf.Ticker(ticker)
            ticker_name = ticker_info.info['longName']

            # Add a section for displaying news articles
            st.header("Latest News")
            
            # Integrate a news API (replace with your chosen news API and API key)
            news_api_url = "https://newsapi.org/v2/everything"
            news_api_key = "514db7ff47ff47af80fa780fb822fc76"
            
            # Customize your news query based on the stock symbol and name
            news_query = {
                "q": f"{ticker} {ticker_name}",  # Include both symbol and name
                "apiKey": news_api_key,
                "language": "en",  # Filter by English language
                "sortBy": "publishedAt",  # Sort by publication date
            }


            # Make a request to the news API and display the news articles
            response = requests.get(news_api_url, params=news_query)
            news_data = response.json()

            # Initialize a list to store articles and sort them by date
            articles = sorted(news_data.get("articles", []), key=lambda x: x['publishedAt'], reverse=True)

            # Initialize a set to track unique article titles
            unique_titles = set()

            # Initialize a counter for displayed articles
            displayed_count = 0
            
            nlp = spacy.load("en_core_web_sm")

            for article in articles:
                # Check if the article title is unique
                if article['title'] not in unique_titles:
                    # Check if the article is in English
                    article_content = article.get("content", "")
                    if article_content:
            # Use spacy for language detection
                        doc = nlp(article_content)

            # Check if the detected language is English
                        if doc.lang_ == 'en':
                    
                            # Display the article
                            st.write(f"**{article['title']}**")
                            st.write(f"Source: {article['source']['name']}")
                            st.write(f"Published: {article['publishedAt']}")
                            st.write(article['description'])
                            st.write(f"[Read more]({article['url']})")

                            unique_titles.add(article['title'])
                            displayed_count += 1

                        # Break when 15 unique articles are displayed
                        if displayed_count == 15:
                            break

    else:
        st.warning("Please enter values for the stock ticker and date range.")    

# Check if the "Download CSV" button is clicked
if fetch_download_csv:    # Check if there's data available to download
    if ticker and start_date and end_date:
        # Fetch historical data and create a DataFrame
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # Prepare the data for download
        csv_data = data.to_csv(index=False)
        csv_bytes = csv_data.encode()

        # Display the data table
        st.dataframe(data)
        
        # Create a button to download the CSV file
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"{ticker}_data.csv",
            key="download_button"
        )
    else:
        st.warning("Please enter values for the stock ticker and date range.")


if fetch_statistics: 
    # Fetch additional statistics data using yfinance
    if ticker:
        stock = yf.Ticker(ticker)
        statistics = stock.info

        st.write("")  # Insert a space


        # Increase the font size of the subheader using CSS
        st.write(
    f'<span style="font-size: 34px;">Statistics for {ticker}</span>',
    unsafe_allow_html=True)

        stock_price_hist = {
            "Beta (5Y Monthly)": statistics.get("beta"),
            "52-Week Change": statistics.get("52WeekChange"),
            "S&P500 52-Week Change": statistics.get("SandP52WeekChange"),
            "52 Week High": statistics.get("fiftyTwoWeekHigh"),
            "52 Week Low": statistics.get("fiftyTwoWeekLow"),
            "50-Day Moving Average": statistics.get("fiftyDayAverage"),
            "200-Day Moving Average": statistics.get("twoHundredDayAverage"),
        }

        # Additional statistics
        profitability = {
            "Profit Margin": statistics.get("profitMargins"),
            "Operating Margin (ttm)": statistics.get("operatingMargins"),
        }

        management_effectiveness = {
            "Return on Assets (ttm)": statistics.get("returnOnAssets"),
            "Return on Equity (ttm)": statistics.get("returnOnEquity"),
        }

        income_statement = {
            "Revenue (ttm)": statistics.get("totalRevenue"),
            "Revenue Per Share (ttm)": statistics.get("revenuePerShare"),
            "Quarterly Revenue Growth (yoy)": statistics.get("revenueGrowth"),
            "Gross Profit (ttm)": statistics.get("grossProfits"),
            "EBITDA": statistics.get("ebitda"),
            "Net Income Avi to Common (ttm)": statistics.get("netIncomeToCommon"),
            "Diluted EPS (ttm)": statistics.get("trailingEps"),
            "Quarterly Earnings Growth (yoy)": statistics.get("earningsQuarterlyGrowth"),
        }

        balance_sheet = {
            "Total Cash (mrq)": statistics.get("totalCash"),
            "Total Cash Per Share (mrq)": statistics.get("totalCashPerShare"),
            "Total Debt (mrq)": statistics.get("totalDebt"),
            "Total Debt/Equity (mrq)": statistics.get("debtToEquity"),
            "Current Ratio (mrq)": statistics.get("currentRatio"),
            "Book Value Per Share (mrq)": statistics.get("bookValue"),
        }

        cash_flow_statement = {
            "Operating Cash Flow (ttm)": statistics.get("operatingCashflow"),
            "Levered Free Cash Flow (ttm)": statistics.get("freeCashflow"),
        }

        valuation_measures = {
            "Market Cap (intraday)": statistics.get("marketCap"),
            "Enterprise Value": statistics.get("enterpriseValue"),
            "Trailing P/E": statistics.get("trailingPE"),
            "Forward P/E": statistics.get("forwardPE"),
            "PEG Ratio (5 yr expected)": statistics.get("pegRatio"),
            "Price/Sales (ttm)": statistics.get("priceToSalesTrailing12Months"),
            "Price/Book (mrq)": statistics.get("priceToBook"),
            "Enterprise Value/Revenue": statistics.get("enterpriseToRevenue"),
            "Enterprise Value/EBITDA": statistics.get("enterpriseToEbitda"),
        }

        share_statistics = {
            "Avg Vol (3 month)": statistics.get("averageVolume3Month"),
            "Avg Vol (10 day)": statistics.get("averageVolume10days"),
            "Shares Outstanding": statistics.get("sharesOutstanding"),
            "Implied Shares Outstanding": statistics.get("impliedSharesOutstanding"),
            "Float": statistics.get("floatShares"),
            "% Held by Insiders": statistics.get("heldPercentInsiders"),
            "% Held by Institutions": statistics.get("heldPercentInstitutions"),
            "Shares Short (Sep 14, 2023)": statistics.get("sharesShort"),
            "Short Ratio (Sep 14, 2023)": statistics.get("shortRatio"),
            "Short % of Float (Sep 14, 2023)": statistics.get("shortPercentOfFloat"),
            "Short % of Shares Outstanding (Sep 14, 2023)": statistics.get("shortPercentOfSharesOutstanding"),
            "Shares Short (prior month Aug 14, 2023)": statistics.get("sharesShortPriorMonth"),
        }

        dividends_splits = {
            "Forward Annual Dividend Rate": statistics.get("forwardEps"),
            "Forward Annual Dividend Yield": statistics.get("forwardDividendYield"),
            "Trailing Annual Dividend Rate": statistics.get("trailingEps"),
            "Trailing Annual Dividend Yield": statistics.get("trailingDividendYield"),
            "5 Year Average Dividend Yield": statistics.get("averageDividendYield5Years"),
            "Payout Ratio": statistics.get("payoutRatio"),
            "Last Split Factor": statistics.get("lastSplitFactor"),
        }

        # Financial Highlights
        fiscal_year_ends = statistics.get("lastFiscalYearEnd")
        most_recent_quarter = statistics.get("mostRecentQuarter")

        col1, col2 = st.columns(2)

        with col1:
        
            st.subheader("Valuation Measures")
            for key, value in valuation_measures.items():
                st.write(f"{key}: {value}")
            
            st.subheader("Financial Highlights")
            st.write(f"Fiscal Year Ends: {fiscal_year_ends}")
            st.write(f"Most Recent Quarter (mrq): {most_recent_quarter}")



            # Display the additional statistics
            st.subheader("Profitability")
            for key, value in profitability.items():
                st.write(f"{key}: {value}")

            st.subheader("Management Effectiveness")
            for key, value in management_effectiveness.items():
                st.write(f"{key}: {value}")

            st.subheader("Income Statement")
            for key, value in income_statement.items():
                st.write(f"{key}: {value}")

            st.subheader("Balance Sheet")
            for key, value in balance_sheet.items():
                st.write(f"{key}: {value}")

            st.subheader("Cash Flow Statement")
            for key, value in cash_flow_statement.items():
                st.write(f"{key}: {value}")

        with col2:

                # Display the statistics using st.write
            st.subheader("Trading Information")
            st.subheader("Stock Price History")
            for key, value in stock_price_hist.items():
                st.write(f"{key}: {value}")

            st.subheader("Share Statistics")
            for key, value in share_statistics.items():
                st.write(f"{key}: {value}")

            st.subheader("Dividends & Splits")
            for key, value in dividends_splits.items():
                st.write(f"{key}: {value}")


    else:
        st.warning("Please enter a stock ticker to fetch statistics.")

