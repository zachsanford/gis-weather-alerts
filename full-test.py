# IMPORTS
import argparse
from modtestfuncs import map_alerts

# MAIN
def main():

    # Argument to pass; State
    parser = argparse.ArgumentParser(
        description="Download and map NOAA Weather Alerts."
    )
    parser.add_argument(
        "--state",
        default="OR",
        help="Two-letter state abbreviation (default: OR)"
    )
    args = parser.parse_args()

    # Call mapping function
    map_alerts(args.state)

if __name__ == '__main__':
    main()