import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    # Wrap the entirety of the model-calling logic into a loop so that the agent can 
    # iterate on a task till it is done working
    for _ in range(20):
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        )

        agent_response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config=config,
        )

        if agent_response.candidates:
            for candidate in agent_response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        if agent_response is None or agent_response.usage_metadata is None:
            raise RuntimeError("Either the agent_response or '.usage_metadata' is 'None'")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {agent_response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {agent_response.usage_metadata.candidates_token_count}")

        if agent_response.function_calls is not None:
            all_function_call_results: list = []
            for function_call in agent_response.function_calls:
                function_call_result = call_function(function_call)
                if function_call_result.parts is None:
                    raise Exception(f"The '.parts[0]' of functional call {function_call_result} is None")
                if function_call_result.parts[0].function_response is None:
                    raise Exception(f"The '.function_response' of functional call {function_call_result} is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception(f"The '.function_response.response' of functional call {function_call_result} is None")

                all_function_call_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(agent_response.text)
            return

        messages.append(types.Content(role="user", parts=all_function_call_results))

    sys.exit("The agent was unable to come to a solution after 20 iterations")

if __name__ == "__main__":
    main()

