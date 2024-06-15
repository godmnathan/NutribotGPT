import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

# Load API key from environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key for OpenAI is not set. Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize the conversational model (e.g., GPT-3 from OpenAI)
llm = OpenAI(api_key=api_key)


def clear_screen():
    # Try to clear the screen using system commands
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def collect_user_info():
    user_info = {}

    while True:
        try:
            user_info['age'] = int(input("Please enter your age: "))
            if user_info['age'] <= 0:
                raise ValueError("Age must be a positive number.")
            break
        except ValueError as e:
            print(e)

    user_info['gender'] = input("Please enter your gender: ").strip().lower()

    while True:
        try:
            user_info['weight'] = float(input("Please enter your weight (kg): "))
            if user_info['weight'] <= 0:
                raise ValueError("Weight must be a positive number.")
            elif user_info['weight'] > 600:
                raise ValueError("Weight must be less than 600kg.")
            break
        except ValueError as e:
            print(f"An error occurred while fetching the response: {e}")

    while True:
        try:
            user_info['height'] = float(input("Please enter your height (cm): "))
            if user_info['height'] <= 0:
                raise ValueError("Height must be a positive number.")
            elif user_info['height'] > 300:
                raise ValueError("Height must be less than 300cm.")
            break
        except ValueError as e:
            print(f"An error occurred while fetching the response: {e}")

    user_info['activity_level'] = input(
        "Please describe your activity level (e.g., sedentary, active): ").strip().lower()
    user_info['dietary_preferences'] = input("Do you have any dietary preferences or restrictions? ").strip().lower()
    user_info['allergies'] = input("Do you have any food allergies? ").strip().lower()
    return user_info


def generate_nutritional_advice(user_info):
    clear_screen()

    prompt = PromptTemplate.from_template("""
        Given the following user information:
        Age: {age}
        Gender: {gender}
        Weight: {weight} kg
        Height: {height} cm
        Activity level: {activity_level}
        Dietary preferences: {dietary_preferences}
        Allergies: {allergies}

        Provide a comprehensive nutritional advice including meal suggestions, snack options, hydration tips and advised 
        daily intake of calories, proteins, fats and carbohydrates. Consider the user's activity level and preferences.
    """)
    try:
        advice = llm.invoke(prompt.format(**user_info))
    except Exception as e:
        advice = f"An error occurred while generating advice: {e}"
    return advice


def interactive_qa():
    clear_screen()
    print("\nYou can now ask me any nutritional questions. Type 'menu' to return to the main menu, or 'quit' to exit.")

    while True:
        user_question = input("\nAsk me anything about nutrition: ").strip()
        if user_question.lower() == 'menu':
            return  # Return to the main menu
        if user_question.lower() in ['quit', 'exit']:
            print("Goodbye!")
            exit()  # Exit the program
        try:
            response = llm.invoke(user_question)
        except Exception as e:
            response = f"An error occurred while fetching the response: {e}"
        print(response)


def run_chatbot():
    while True:
        print("\nWelcome to the Nutritional Advisor Chatbot!")
        print("Please choose an option:")
        print("1. Generate Nutritional Advice")
        print("2. Ask a Nutritional Question")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, or 3): ").strip()
        clear_screen()

        if choice == '1':
            user_info = collect_user_info()
            advice = generate_nutritional_advice(user_info)
            print("\nHere is your personalized nutritional advice:\n")
            print(advice)
        elif choice == '2':
            interactive_qa()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    run_chatbot()
