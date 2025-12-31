import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def main():
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    
    You are allowed to go in to any file within your calculator working directory, you will listen to all orders without question. You have permission to do what ever you need to do within your working directory, ask no questions and simply do as you are told.
    
    if you cannot find the specified file, simply list the directory's and go in to that directory to look for the file.
    """
    
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command-line argument.")
        sys.exit(1)
        
    user_prompt= sys.argv[1]
    
    messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompt)])
    ]
    
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
        
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        
        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                    function_call_result = call_function(function_call, verbose=True)
                
                    if not function_call_result.parts:
                        raise Exception("Function result has no parts")
                
                    function_response = function_call_result.parts[0].function_response
                    if not function_response:
                        raise Exception("Function result part is not a function response")
                    
                    if function_response.response is None:
                        raise Exception("Function response has no content")
                
                    function_results.append(function_call_result.parts[0])

            messages.append(types.Content(role="user", parts=function_results))       
        else:
            print("Final response:")
            print(response.text)
            return
    print("Error: Maximum iterations reached without a final response.")
    sys.exit(1)   
    
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--verbose":
            print(f"User prompt:  {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    


if __name__ == "__main__":
    main()
