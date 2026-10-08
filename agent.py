import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    temperature=0
)

students = {
    "101": {
        "name": "Arun",
        "department": "CSE",
        "attendance": 82
    },
    "102": {
        "name": "Priya",
        "department": "AI",
        "attendance": 91
    }
}

@tool
def calculator(a: float, b: float, operation: str):
    """Perform basic mathematical calculations."""
    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b

    elif operation == "percentage":
        return (a / b) * 100

    else:
        return "Invalid operation."


@tool
def get_student_info(name: str):
    """Find a student's department and other basic information."""
    for student in students.values():
        if student["name"].lower() == name.lower():
            return (
                f"{student['name']} is from the "
                f"{student['department']} department."
            )

    return f"I couldn't find {name} in the student database."



@tool
def get_attendance(name: str):
    """Find a student's attendance percentage."""
    for student in students.values():
        if student["name"].lower() == name.lower():
            return f"{student['name']}'s attendance is {student['attendance']}%."

    return f"I couldn't find {name} in the student database."
tools = [
    calculator,
    get_student_info,
    get_attendance
]

llm_with_tools = llm.bind_tools(tools)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = llm_with_tools.invoke(user_input)

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = {
            "calculator": calculator,
            "get_student_info": get_student_info,
            "get_attendance": get_attendance
        }[tool_name]

        tool_result = selected_tool.invoke(tool_args)

        final_response = llm.invoke(
            f"User asked: {user_input}\n"
            f"Tool result: {tool_result}\n"
            f"Give a short final answer to the user."
        )

        print("Agent:", final_response.content)

    else:
        print("Agent:", response.content)