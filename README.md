# Stock Visualizer App

## Overview

Ever wondered how to turn your fascination with stocks into an interactive data exploration adventure? Look no further! Introducing the Stock Visualizer App, where finance meets interactivity. Whether you're a seasoned investor or just curious about stock trends, this app has something for everyone.

In a market full of data analysis projects, this one stands out by combining financial insights with an intuitive user interface. No more boring charts; we're talking about candlestick charts, moving averages, and news updates. Dive into the world of stock data, make informed decisions, and maybe even impress your friends with your newfound financial wizardry.

Ready to embark on a financial journey? Explore the Stock Visualizer App live [here](https://tamara-stock-visualizer.streamlit.app/).

## Project Details

I sourced stock data using the `yfinance` library, and additional insights are fetched from a news API for a comprehensive experience.

### Features

- **Interactive Candlestick Chart:** Visualize historical stock data with candlestick patterns, 50-Day SMA, and 20-Day EMA.
- **Latest News Feed:** Stay informed with the latest news related to the stock you're exploring.
- **Data Download:** Download historical stock data as a CSV for your analysis.
- **Comprehensive Statistics:** Fetch key statistics about a stock for a quick overview.

### How to Use

Getting started with the Stock Visualizer App is as easy as placing a market order:

1. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```
   
2. Run the app:

   ```bash
   streamlit run stock_visualizer.py
   ```

And there you have it — your personal Stock Visualizer App is ready to enlighten you on the intricacies of the stock market!

## Yahoo Finance Integration
The Stock Visualizer App seamlessly integrates with Yahoo Finance, leveraging data from their extensive financial database. The statistics section is crafted to mirror the key metrics available on Yahoo Finance, providing users with a familiar and comprehensive view of a stock's performance.
