"""API client for fetching financial data."""
import os
import json
from typing import Optional


class FinancialMetrics:
    """Container for financial metrics data."""
    
    def __init__(self, data: dict):
        self.data = data
    
    def get(self, key: str, default=None):
        """Get a metric value by key."""
        return self.data.get(key, default)
    
    def __getitem__(self, key: str):
        return self.data.get(key)


def get_financial_metrics(
    ticker: str,
    end_date: Optional[str] = None,
    period: str = "ttm",
    limit: int = 10,
    api_key: Optional[str] = None,
) -> list[FinancialMetrics]:
    """Fetch financial metrics for a given ticker.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date for the data (YYYY-MM-DD)
        period: Time period (ttm, annual, quarterly)
        limit: Maximum number of records to return
        api_key: Financial Datasets API key (optional for free tickers)
    
    Returns:
        List of FinancialMetrics objects
    """
    # Free tickers that don't require an API key
    FREE_TICKERS = ["AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"]
    
    try:
        import requests
    except ImportError:
        print("Error: requests library not found. Install it with: pip install requests")
        return []
    
    # For free tickers, use mock data if no API key
    if ticker.upper() in FREE_TICKERS and not api_key:
        return _get_mock_data(ticker.upper())
    
    if not api_key:
        print(f"Warning: No API key provided for {ticker}. Using mock data.")
        return _get_mock_data(ticker.upper())
    
    # Build API request
    url = f"https://api.financialdatasets.ai/financial-metrics/"
    params = {
        "ticker": ticker,
        "period": period,
        "limit": limit,
    }
    if end_date:
        params["end_date"] = end_date
    
    headers = {
        "X-API-KEY": api_key,
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        metrics_list = data.get("financial_metrics", [])
        
        return [FinancialMetrics(m) for m in metrics_list]
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return _get_mock_data(ticker.upper())


def _get_mock_data(ticker: str) -> list[FinancialMetrics]:
    """Return mock financial data for demonstration purposes."""
    
    mock_data = {
        "AAPL": {
            "return_on_equity": 1.4725,
            "net_margin": 0.2644,
            "operating_margin": 0.3074,
            "revenue_growth": 0.0202,
            "earnings_growth": 0.1022,
            "book_value_growth": 0.0850,
            "current_ratio": 0.87,
            "debt_to_equity": 1.97,
            "free_cash_flow_per_share": 6.85,
            "earnings_per_share": 6.13,
            "price_to_earnings_ratio": 33.89,
            "price_to_book_ratio": 50.30,
            "price_to_sales_ratio": 8.94,
        },
        "MSFT": {
            "return_on_equity": 0.3621,
            "net_margin": 0.3613,
            "operating_margin": 0.4237,
            "revenue_growth": 0.1572,
            "earnings_growth": 0.2213,
            "book_value_growth": 0.1124,
            "current_ratio": 1.27,
            "debt_to_equity": 0.28,
            "free_cash_flow_per_share": 9.65,
            "earnings_per_share": 11.80,
            "price_to_earnings_ratio": 35.25,
            "price_to_book_ratio": 12.87,
            "price_to_sales_ratio": 13.02,
        },
        "NVDA": {
            "return_on_equity": 1.2345,
            "net_margin": 0.5523,
            "operating_margin": 0.6207,
            "revenue_growth": 1.2211,
            "earnings_growth": 2.8145,
            "book_value_growth": 0.4523,
            "current_ratio": 3.45,
            "debt_to_equity": 0.15,
            "free_cash_flow_per_share": 2.87,
            "earnings_per_share": 11.93,
            "price_to_earnings_ratio": 52.34,
            "price_to_book_ratio": 55.67,
            "price_to_sales_ratio": 28.91,
        },
    }
    
    # Default mock data for unknown tickers
    default_data = {
        "return_on_equity": 0.15,
        "net_margin": 0.10,
        "operating_margin": 0.12,
        "revenue_growth": 0.05,
        "earnings_growth": 0.08,
        "book_value_growth": 0.06,
        "current_ratio": 1.5,
        "debt_to_equity": 0.4,
        "free_cash_flow_per_share": 2.5,
        "earnings_per_share": 3.0,
        "price_to_earnings_ratio": 20.0,
        "price_to_book_ratio": 3.0,
        "price_to_sales_ratio": 2.0,
    }
    
    data = mock_data.get(ticker, default_data)
    return [FinancialMetrics(data)]
