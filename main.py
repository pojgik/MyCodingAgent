import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MAX_ITERATIONS = 20


def main():
    prompt = ""
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
    
    
def generate_content(client, messages, verbose):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
        )
            
    except Exception as e:
        print(f"Error sending request to Gemini: {e}")
        sys.exit(1)
    
    if (verbose):
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(candidate.content)
    
    if not response.function_calls:
        return response.text
    
    function_responses = [] 
    if not response.function_calls:
        print("Response:")
        print(response.text)
    else:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Function call did not return a response.")
            else:
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting")
    
    if function_responses:
        messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()