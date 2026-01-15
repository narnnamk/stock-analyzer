# Stock Analyzer Project

## Overview
Stock Analyzer is a CLI Python program that lets the user enter a stock ticker and a time period, then generates a PDF stock analysis report. The report uses technical indicators such as moving averages (50/200 MA), on-balance volume (OBV), and annualized volatility, along with price and volume data. It includes a quick overview, technical analysis (trend, momentum, volume confirmation), visual charts, and a closing summary with a signal score, outlook, and confidence level.

## Project Motivation
I have a strong interest in investing and I have had a brokerage account for almost two years. During winter break, I had extra time and wanted to build something useful with my current programming and investing knowledge. This project helped me practice working with real financial data, building a clean output layout, and creating an automated report.

## Features
- CLI input for ticker and period (`1mo`, `3mo`, `6mo`, `1y`)
- Pulls stock data using the `yfinance` library
- Calculates indicators:
  - 50-day and 200-day moving averages
  - OBV (On-Balance Volume)
  - Average volume and volume confirmation
  - Annualized volatility (based on log returns)
- Technical analysis output:
  - Trend, momentum, volume confirmation, and MA cross signals
- Generates a PDF report with:
  - Quick overview table
  - Technical analysis text
  - Charts/graphs (matplotlib)
  - Final summary with signal score, outlook, and confidence

## Screenshots
<img width="911" height="392" alt="Image" src="https://github.com/user-attachments/assets/e28a2958-69fa-4bb3-b008-381aef0132ae" />
<img width="776" height="610" alt="Image" src="https://github.com/user-attachments/assets/8f6dc2a4-12f5-47f8-9f92-7cc0cc980f98" />
<img width="837" height="573" alt="Image" src="https://github.com/user-attachments/assets/6115f526-f56c-47f1-a7bb-05bae580456c" />
<img width="773" height="297" alt="Image" src="https://github.com/user-attachments/assets/593a418d-2e6a-4f7e-a0d9-cc71fdd15277" />

## Skills Demonstrated
- Python (functions, modules, clean project structure)
- Data handling with pandas
- Financial data collection with yfinance
- Technical indicator calculations (MA, OBV, volatility, momentum logic)
- Matplotlib charting and subplot layout
- PDF report generation (ReportLab)
- CLI program design and user-friendly output formatting

## How to Run
1. Clone this repository
2. Install dependencies:
   pip install yfinance pandas numpy matplotlib reportlab
3. Run the program: 
   python main.py
4. Enter a ticker and a period when prompted and the program will generate a PDF report in the current directory.

## Files
- input.py - ticker and period input handling
- data.py - retrieve raw stock data from yfinance library
- indicators.py - calculates indicators (moving averages, volatility, price changes, OBV, etc.)
- analysis.py - analysis logic based on indicators values (trend, momentum, volume confirmation, crosses, score)
- plots.py - plots charts and graphs (matplotlib)
- output.py - console output messages and PDF report generation
- main.py - main program that calls and executes functions

## Notes / Limitations
- Some tickers may return missing data depending on yfinance availability.
- This is a technical analysis tool and does not use company fundamentals or news.
- This project is for learning purposes and is not financial advice.


## Contact
Handshake: https://sau.joinhandshake.com/profiles/nnk
LinkedIn: https://www.linkedin.com/in/narnnam-kongsappaisal-3b688232a/

