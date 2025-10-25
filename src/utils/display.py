"""Utilities for displaying analysis results."""
import json
from colorama import Fore, Style


def print_analysis_output(analysis: dict):
    """Print the fundamental analysis output in a formatted way.
    
    Args:
        analysis: Dictionary mapping tickers to their analysis results
    """
    print(f"\n{Fore.GREEN}{'=' * 60}")
    print(f"{Fore.GREEN}Fundamental Analysis Results")
    print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}\n")
    
    for ticker, result in analysis.items():
        signal = result["signal"]
        confidence = result["confidence"]
        
        # Color code the signal
        if signal == "bullish":
            signal_color = Fore.GREEN
        elif signal == "bearish":
            signal_color = Fore.RED
        else:
            signal_color = Fore.YELLOW
        
        print(f"{Fore.CYAN}━━━ {ticker} ━━━{Style.RESET_ALL}")
        print(f"Signal: {signal_color}{signal.upper()}{Style.RESET_ALL}")
        print(f"Confidence: {confidence}%\n")
        
        # Print reasoning
        reasoning = result.get("reasoning", {})
        if reasoning:
            print("Analysis Breakdown:")
            for key, value in reasoning.items():
                signal_name = key.replace("_signal", "").replace("_", " ").title()
                signal_value = value.get("signal", "N/A")
                details = value.get("details", "N/A")
                
                # Color code individual signals
                if signal_value == "bullish":
                    color = Fore.GREEN
                elif signal_value == "bearish":
                    color = Fore.RED
                else:
                    color = Fore.YELLOW
                
                print(f"  • {signal_name}: {color}{signal_value}{Style.RESET_ALL}")
                print(f"    {details}")
        
        print()
    
    print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}\n")


def print_json(data: dict, title: str = None):
    """Print formatted JSON output.
    
    Args:
        data: Dictionary to print as JSON
        title: Optional title to display above the JSON
    """
    if title:
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.CYAN}{title.center(60)}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    print(json.dumps(data, indent=2))
    
    if title:
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
