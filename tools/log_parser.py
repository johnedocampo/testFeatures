import re
import argparse
import sys

def parse_logs(log_file, pattern):
    """
    Parses a log file using a regular expression to extract information.

    Args:
        log_file (str): The path to the log file.
        pattern (str): The regular expression pattern to match.
    """
    try:
        compiled_pattern = re.compile(pattern)
    except re.error as e:
        print(f"Error: Invalid regular expression: {e}", file=sys.stderr)
        sys.exit(1)

    values = []
    try:
        with open(log_file, 'r') as f:
            for i, line in enumerate(f, 1):
                match = compiled_pattern.search(line)
                if match:
                    # Assume the first captured group is the value of interest.
                    if match.groups():
                        try:
                            values.append(float(match.group(1)))
                        except (ValueError, IndexError):
                            print(f"Warning: Could not convert value on line {i} to a float.", file=sys.stderr)
                    else:
                        try:
                            values.append(float(match.group(0)))
                        except ValueError:
                            print(f"Warning: Could not convert value on line {i} to a float.", file=sys.stderr)

        if values:
            print("Caught numbers:")
            for v in values:
                print(v)
            print(f"Average: {sum(values) / len(values)}")
        else:
            print("No values found to average.")

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract information from log files and calculate the average.",
        epilog="Example: python log_parser.py /var/log/auth.log 'sshd\[(\d+)\]: Failed password for .+ from ([\d\.]+)'"
    )
    parser.add_argument("logfile", help="The path to the log file to parse.")
    parser.add_argument("pattern", help="The Python-style regular expression to use for matching.")
    
    args = parser.parse_args()
    
    parse_logs(args.logfile, args.pattern)

if __name__ == "__main__":
    main()