# AI Hedge Fund MVP

A simplified version of an AI-powered hedge fund that uses a fundamental analyst agent to analyze stocks and generate trading signals.

## Features

- **Fundamental Analysis Agent**: Analyzes key financial metrics (profitability, growth, financial health, valuation)
- **Trading Signals**: Generates buy/sell/hold recommendations with confidence scores
- **Multiple Stock Support**: Analyze multiple tickers in a single run
- **CLI Interface**: Simple command-line interface for quick analysis

## Disclaimer

This project is for **educational purposes only**. Not intended for real trading or investment. No investment advice or guarantees provided. Always consult a financial advisor.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gitmvp-com/ai-hedge-fund-mvp.git
cd ai-hedge-fund-mvp
```

### 2. Install Dependencies

Make sure you have Python 3.11+ installed.

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### 3. Set up API Keys

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Required: OpenAI API key for AI analysis
OPENAI_API_KEY=your-openai-api-key

# Optional: Financial data API key (free for AAPL, GOOGL, MSFT, NVDA, TSLA)
FINANCIAL_DATASETS_API_KEY=your-api-key
```

**Note**: Data for AAPL, GOOGL, MSFT, NVDA, and TSLA is free and doesn't require a `FINANCIAL_DATASETS_API_KEY`.

## Usage

### Run the Analyst

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

### Example Output

```
================================================
  Fundamental Analysis Agent  
================================================
{
  "AAPL": {
    "signal": "bullish",
    "confidence": 75,
    "reasoning": {
      "profitability_signal": {
        "signal": "bullish",
        "details": "ROE: 147.25%, Net Margin: 26.44%, Op Margin: 30.74%"
      },
      "growth_signal": {
        "signal": "neutral",
        "details": "Revenue Growth: 2.02%, Earnings Growth: 10.22%"
      },
      "financial_health_signal": {
        "signal": "bullish",
        "details": "Current Ratio: 0.87, D/E: 1.97"
      },
      "price_ratios_signal": {
        "signal": "neutral",
        "details": "P/E: 33.89, P/B: 50.30, P/S: 8.94"
      }
    }
  }
}
```

## Project Structure

```
ai-hedge-fund-mvp/
├── src/
│   ├── agents/
│   │   └── fundamentals.py    # Fundamental analysis agent
│   ├── tools/
│   │   └── api.py             # Financial data API client
│   ├── utils/
│   │   └── display.py         # Output formatting
│   └── main.py                # Entry point
├── pyproject.toml             # Poetry dependencies
├── .env.example               # Environment variables template
└── README.md
```

## How It Works

1. **Data Fetching**: Retrieves financial metrics (TTM) for specified tickers
2. **Analysis**: Evaluates 4 key areas:
   - **Profitability**: ROE, net margin, operating margin
   - **Growth**: Revenue and earnings growth
   - **Financial Health**: Current ratio, debt-to-equity, free cash flow
   - **Valuation**: P/E, P/B, P/S ratios
3. **Signal Generation**: Combines individual signals into overall recommendation
4. **Confidence Score**: Calculates confidence based on signal agreement

## Configuration

All dependencies use the same versions as the parent repository for compatibility.

## Contributing

This is an MVP. For the full-featured version with 18+ agents, visit the [original repository](https://github.com/virattt/ai-hedge-fund).

## License

MIT License - see LICENSE file for details.
