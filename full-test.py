import argparse
from modtestfuncs import full_test

def main():
    parser = argparse.ArgumentParser(description="Download and map NOAA Weather Alerts.")
    parser.add_argument("--state", default="OR",help="Two-letter state abbreviation (default: OR)")
    args = parser.parse_args()
    full_test(args.state)

if __name__ == '__main__':
    main()