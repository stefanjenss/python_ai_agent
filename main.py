import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The API KEY was not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # --- Regerate and return the model's response ---
    
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    )

    agent_response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages,
        config=config,
    )

    if agent_response is None or agent_response.usage_metadata is None:
        raise RuntimeError("Either the agent_response or '.usage_metadata' is 'None'")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {agent_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {agent_response.usage_metadata.candidates_token_count}")

    if agent_response.function_calls is not None:
        for function_call in agent_response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(agent_response.text)

if __name__ == "__main__":
    main()

