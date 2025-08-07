import openai
import os
import sys

def chatgpt_suggest_fix(error_line):
    """Ask ChatGPT for a suggestion for a log error"""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return "Error: OPENAI_API_KEY environment variable is not set."

        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" if you're on free tier
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a DevOps assistant who helps interpret log errors "
                        "and suggest actionable solutions for them."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Here's a log error:\n\n{error_line}\n\n"
                        "Please explain what this error likely means and how to resolve it."
                    ),
                },
            ],
            max_tokens=150,
            temperature=0.3,
        )

        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: Failed to fetch suggestion from ChatGPT: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_chatgpt_suggestion.py \"<log error line>\"")
        return

    error_line = sys.argv[1]
    print(f"\n📄 Error: {error_line}")
    print("🤖 ChatGPT Suggestion:\n")

    suggestion = chatgpt_suggest_fix(error_line)
    print(suggestion)

if __name__ == "__main__":
    main()
