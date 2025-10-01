import os
import json
from openai import OpenAI
from playwright.sync_api import Page
from .types import TaskMessage, TaskResult
from .prompt import prompt, SYSTEM_PROMPT
from .create_actions import create_actions

def complete_task(page: Page, task: TaskMessage) -> TaskResult:
    """
    Completes a task by interacting with the OpenAI API.
    """
    options = task.get("options") or {}

    openai = OpenAI(
        api_key=options.get("openai_api_key"),
        base_url=options.get("openai_base_url"),
        default_query=options.get("openai_default_query"),
        default_headers=options.get("openai_default_headers"),
    )

    debug = options.get("debug", os.environ.get("AUTO_PLAYWRIGHT_DEBUG") == "true")

    actions = create_actions(page)

    tools_for_api = []
    for name, details in actions.items():
        schema = {k: v for k, v in details.items() if k != 'function'}
        tools_for_api.append({"type": "function", "function": schema})

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt(task)},
    ]

    while True:
        if debug:
            print("> Sending messages to OpenAI:", json.dumps(messages, indent=2))

        response = openai.chat.completions.create(
            model=options.get("model", "gpt-4o"),
            messages=messages,
            tools=tools_for_api,
            tool_choice="auto",
        )

        response_message = response.choices[0].message

        if debug:
            print("< Received response from OpenAI:", response_message)

        tool_calls = response_message.tool_calls

        if not tool_calls:
            raise Exception("Expected a tool call from the model, but none was received.")

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = actions[function_name]["function"]
            function_args_str = tool_call.function.arguments

            if debug:
                print(f"> Calling function: {function_name} with args: {function_args_str}")

            function_response = function_to_call(function_args_str)

            if debug:
                print(f"< Got function response: {function_response}")

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

            if function_name.startswith("result"):
                if debug:
                    print("> Final result received:", function_response)
                return function_response