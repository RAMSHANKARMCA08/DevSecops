import os
import re
import sys
from datetime import datetime

# Define known error patterns and suggestions
ERROR_PATTERNS = [
    (r"##\[error\] The process '.*' failed with exit code \d+", "Check if the required tool or dependency is installed and accessible in PATH."),
    (r"fatal: could not read from remote repository", "Verify your Git credentials or SSH key permissions."),
    (r"npm ERR!", "Ensure Node.js is installed correctly and all dependencies are resolved."),
    (r"command not found", "Check if the command exists on the runner or if the path is misconfigured."),
    (r"permission denied", "Verify file/folder permissions for the running process."),
    (r"Unhandled exception", "Check for unhandled errors in the script or application."),
    (r"cannot find module", "Make sure all required modules or packages are installed."),
    (r"Segmentation fault", "Check for memory issues or invalid pointer accesses."),
    (r"connection timed out", "Check network connectivity or remote service availability."),
    (r"Cannot read properties of undefined", "Check if the object you're accessing is properly initialized or not null."),
    (r"Error: ENOENT", "Check if the referenced file or directory exists."),
    (r"ECONNREFUSED", "Ensure the server or service you're trying to reach is up and accepting connections."),
]

def find_logs(directory):
    """Recursively find .log files in a directory"""
    log_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    return log_files

def extract_errors(file_path):
    """Extract error lines using predefined patterns"""
    error_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                for pattern, _ in ERROR_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        error_lines.append(line.strip())
                        break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return error_lines

def extract_keywords(file_path):
    """Extract all lines that contain the words 'Error' or 'Warning' (case-insensitive)"""
    keyword_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if re.search(r'\b(error|warning|fatal)\b', line, re.IGNORECASE):
                    keyword_lines.append(line.strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return keyword_lines

def suggest_fixes(error_lines):
    """Match errors with known suggestions"""
    suggestions = []
    for line in error_lines:
        for pattern, suggestion in ERROR_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                suggestions.append((line, suggestion))
                break
        else:
            suggestions.append((line, "No specific suggestion found. Please investigate manually."))
    return suggestions

def generate_report(log_file, suggestions, keyword_lines):
    print("=" * 80)
    print(f"Log File: {log_file}")
    print(f"Analyzed at: {datetime.now()}")
    print("=" * 80)

    if suggestions:
        for i, (error, suggestion) in enumerate(suggestions, start=1):
            print(f"\nError #{i}:")
            print(f"  → {error}")
            print(f"  Suggestion: {suggestion}")
    else:
        print("No known error patterns matched.")

    if keyword_lines:
        print("\n--- All lines with 'Warning' or 'Error' ---")
        for line in keyword_lines:
            print(f"  {line}")
    else:
        print("\nNo lines with 'Warning' or 'Error' found.")
    print("\n")

def main(folder_path):
    if not os.path.isdir(folder_path):
        print("Provided path is not a valid directory.")
        return

    print(f"\nScanning folder: {folder_path}")
    logs = find_logs(folder_path)
    if not logs:
        print("No .log files found.")
        return

    for log_file in sorted(logs, key=os.path.getmtime, reverse=True):
        print(log_file)
        error_lines = extract_errors(log_file)
        keyword_lines = extract_keywords(log_file)
        suggestions = suggest_fixes(error_lines)
        generate_report(log_file, suggestions, keyword_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py /path/to/log/folder")
    else:
        main(sys.argv[1])
