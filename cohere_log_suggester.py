import cohere
import os
import sys

# Get the API key from environment variable
API_KEY = os.getenv("COHERE_API_KEY")

if not API_KEY:
    print("❌ Error: Please set the COHERE_API_KEY environment variable.")
    sys.exit(1)

co = cohere.Client(API_KEY)

def get_suggestion_from_cohere(error_line):
    prompt = (
        f"I encountered the following log error:\n\n"
        f"\"{error_line}\"\n\n"
        f"What does it mean and how do I fix it? Respond with a short explanation and suggestion."
    )
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=200,
            temperature=0.4
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python cohere_log_suggester.py \"<log error line>\"")
        return

    error_line = sys.argv[1]
    print(f"\n📄 Error: {error_line}")
    print("🤖 Cohere Suggestion:\n")

    suggestion = get_suggestion_from_cohere(error_line)
    print(suggestion)

if __name__ == "__main__":
    main()
