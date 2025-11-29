"""
File: ai_cli_response.py
date: 10/30/25
Purpose: Early version of ai implementation in python for web server
"""

# Joe Scott
# 11/28/2025
# Added early AI context here

import ollama
import pdf_reader

chat_log = 'CONVERSATION LOGS: "'

# this function gets responses form the ai
def get_response_from_ollama(user_input):
    # get a response from the modle
    ai_response = ollama.chat(model="gemma3:4b", messages=[
                              {"role": "user", "content": user_input}])

    # Checks if the AI gave the user output
    if 'message' in ai_response:
        return ai_response['message']['content']
    else:
        return 'Sorry something went wrong.'


def main():
    # variables
    user_input = ""
    ai_response = ""
    global chat_log

    # loop for testing the ai
    while (True):
        
        # Get the user response
        user_input = input("Ask the AI [/bye to exit]: ")

        # See if the user wants to quit
        if user_input == "/bye":
            break

        # Store user input in a chat log for context
        chat_log += user_input + '", "' # Context separator

        # Run it through ollama and save the output
        ai_response = get_response_from_ollama(chat_log + '" QUESTION: ' + user_input)

        # Return the output to the user
        print(ai_response)

        # Store AI response in the chat log for context
        chat_log += ai_response + '", "' # Context Separator

        # print for space and split chats
        print()
        print("---------")
        print()


if __name__ == "__main__":
    main()
