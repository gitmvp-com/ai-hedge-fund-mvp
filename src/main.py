"""Main entry point for the AI Hedge Fund MVP."""
import argparse
import json
from dotenv import load_dotenv
from colorama import init, Fore, Style

from src.agents.fundamentals import fundamentals_analyst_agent
from src.utils.display import print_analysis_output

# Load environment variables
load_dotenv()

# Initialize colorama
init(autoreset=True)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the AI Hedge Fund MVP - Fundamental Analysis Agent"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        required=True,
        help="Comma-separated list of stock tickers (e.g., AAPL,MSFT,NVDA)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="End date for analysis (YYYY-MM-DD). Defaults to today."
    )
    return parser.parse_args()


def main():
    """Main function to run the fundamental analysis."""
    args = parse_arguments()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    end_date = args.end_date
    
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}AI Hedge Fund MVP - Fundamental Analysis Agent")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    print(f"Analyzing tickers: {', '.join(tickers)}\n")
    
    # Run the fundamental analysis agent
    try:
        analysis_result = fundamentals_analyst_agent(
            tickers=tickers,
            end_date=end_date
        )
        
        # Display results
        print_analysis_output(analysis_result)
        
    except Exception as e:
        print(f"{Fore.RED}Error running analysis: {str(e)}{Style.RESET_ALL}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
