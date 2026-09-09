import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

try: 
    api_key = os.environ.get("OPENROUTER_API_KEY")
except: 
    raise RuntimeError("OPENROUTER_API_KEY not found in environment variables. Please set it in your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

function_name = next(
    (
        tool["function"]["name"]
        for tool in available_functions
        if tool["function"]["name"] in args.user_prompt
    ),
    None,
)

for request_number in range(20):
    tool_choice = "auto"
    if request_number == 0 and function_name is not None:
        tool_choice = {
            "type": "function",
            "function": {"name": function_name},
        }

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
        tool_choice=tool_choice,
    )
    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump(exclude_none=True))

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if assistant_message.tool_calls is None:
        print(assistant_message.content)
        break

    for tool_call in assistant_message.tool_calls:
        result_message = call_function(tool_call, args.verbose)
        messages.append(result_message)
        print(f"Tool call result: {result_message['content']}")
