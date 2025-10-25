"""Fundamental analysis agent for stock evaluation."""
import json
import os
from src.tools.api import get_financial_metrics


def fundamentals_analyst_agent(tickers: list[str], end_date: str = None) -> dict:
    """Analyzes fundamental data and generates trading signals for multiple tickers.
    
    Args:
        tickers: List of stock ticker symbols
        end_date: End date for analysis (YYYY-MM-DD), defaults to today
        
    Returns:
        Dictionary mapping tickers to their analysis results
    """
    api_key = os.getenv("FINANCIAL_DATASETS_API_KEY")
    fundamental_analysis = {}
    
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        
        # Get financial metrics
        financial_metrics = get_financial_metrics(
            ticker=ticker,
            end_date=end_date,
            period="ttm",
            limit=10,
            api_key=api_key,
        )
        
        if not financial_metrics:
            print(f"Warning: No financial metrics found for {ticker}")
            fundamental_analysis[ticker] = {
                "signal": "neutral",
                "confidence": 0,
                "reasoning": {"error": "No financial data available"}
            }
            continue
        
        # Get the most recent metrics
        metrics = financial_metrics[0]
        
        # Analyze different aspects
        signals = []
        reasoning = {}
        
        # 1. Profitability Analysis
        return_on_equity = metrics.get("return_on_equity")
        net_margin = metrics.get("net_margin")
        operating_margin = metrics.get("operating_margin")
        
        profitability_score = 0
        if return_on_equity and return_on_equity > 0.15:
            profitability_score += 1
        if net_margin and net_margin > 0.20:
            profitability_score += 1
        if operating_margin and operating_margin > 0.15:
            profitability_score += 1
        
        signals.append(
            "bullish" if profitability_score >= 2 else "bearish" if profitability_score == 0 else "neutral"
        )
        reasoning["profitability_signal"] = {
            "signal": signals[0],
            "details": (
                f"ROE: {return_on_equity:.2%}" if return_on_equity else "ROE: N/A"
            ) + ", " + (
                f"Net Margin: {net_margin:.2%}" if net_margin else "Net Margin: N/A"
            ) + ", " + (
                f"Op Margin: {operating_margin:.2%}" if operating_margin else "Op Margin: N/A"
            ),
        }
        
        # 2. Growth Analysis
        revenue_growth = metrics.get("revenue_growth")
        earnings_growth = metrics.get("earnings_growth")
        
        growth_score = 0
        if revenue_growth and revenue_growth > 0.10:
            growth_score += 1
        if earnings_growth and earnings_growth > 0.10:
            growth_score += 1
        
        signals.append(
            "bullish" if growth_score >= 1 else "bearish" if growth_score == 0 else "neutral"
        )
        reasoning["growth_signal"] = {
            "signal": signals[1],
            "details": (
                f"Revenue Growth: {revenue_growth:.2%}" if revenue_growth else "Revenue Growth: N/A"
            ) + ", " + (
                f"Earnings Growth: {earnings_growth:.2%}" if earnings_growth else "Earnings Growth: N/A"
            ),
        }
        
        # 3. Financial Health
        current_ratio = metrics.get("current_ratio")
        debt_to_equity = metrics.get("debt_to_equity")
        
        health_score = 0
        if current_ratio and current_ratio > 1.5:
            health_score += 1
        if debt_to_equity and debt_to_equity < 0.5:
            health_score += 1
        
        signals.append(
            "bullish" if health_score >= 1 else "bearish" if health_score == 0 else "neutral"
        )
        reasoning["financial_health_signal"] = {
            "signal": signals[2],
            "details": (
                f"Current Ratio: {current_ratio:.2f}" if current_ratio else "Current Ratio: N/A"
            ) + ", " + (
                f"D/E: {debt_to_equity:.2f}" if debt_to_equity else "D/E: N/A"
            ),
        }
        
        # 4. Valuation Ratios
        pe_ratio = metrics.get("price_to_earnings_ratio")
        pb_ratio = metrics.get("price_to_book_ratio")
        ps_ratio = metrics.get("price_to_sales_ratio")
        
        price_ratio_score = 0
        if pe_ratio and pe_ratio > 25:
            price_ratio_score += 1
        if pb_ratio and pb_ratio > 3:
            price_ratio_score += 1
        if ps_ratio and ps_ratio > 5:
            price_ratio_score += 1
        
        signals.append(
            "bearish" if price_ratio_score >= 2 else "bullish" if price_ratio_score == 0 else "neutral"
        )
        reasoning["price_ratios_signal"] = {
            "signal": signals[3],
            "details": (
                f"P/E: {pe_ratio:.2f}" if pe_ratio else "P/E: N/A"
            ) + ", " + (
                f"P/B: {pb_ratio:.2f}" if pb_ratio else "P/B: N/A"
            ) + ", " + (
                f"P/S: {ps_ratio:.2f}" if ps_ratio else "P/S: N/A"
            ),
        }
        
        # Determine overall signal
        bullish_signals = signals.count("bullish")
        bearish_signals = signals.count("bearish")
        
        if bullish_signals > bearish_signals:
            overall_signal = "bullish"
        elif bearish_signals > bullish_signals:
            overall_signal = "bearish"
        else:
            overall_signal = "neutral"
        
        # Calculate confidence
        total_signals = len(signals)
        confidence = round(max(bullish_signals, bearish_signals) / total_signals * 100)
        
        fundamental_analysis[ticker] = {
            "signal": overall_signal,
            "confidence": confidence,
            "reasoning": reasoning,
        }
    
    return fundamental_analysis
