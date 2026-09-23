from google import genai
from pydantic import ValidationError
from dotenv import load_dotenv

from app.tools import tools, tool_functions, tool_validators

load_dotenv()
client = genai.Client()


def ask_agent(question: str):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=question,
        tools=tools
    )

    max_rounds = 5
    round_count = 0

    while round_count < max_rounds:
        round_count += 1

        function_results = []

        for step in interaction.steps:
            if step.type == "function_call":
                print("Tool requested:", step.name)
                print("Arguments:", step.arguments)

                if step.name not in tool_functions:
                    print("Unknown tool:", step.name)
                    continue

                try:
                    validator = tool_validators[step.name]
                    validated_args = validator.model_validate(step.arguments)

                except ValidationError as error:
                    print("Invalid arguments:", error)
                    continue

                function = tool_functions[step.name]

                result = function(**validated_args.model_dump())

                print("Tool result:", result)

                function_results.append({
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": {
                        "value": result
                    }
                })

        if not function_results:
            return interaction.output_text

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=tools
        )

    return "Agent stopped: maximum number of rounds reached."