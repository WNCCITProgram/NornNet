"""
File: AIResponse.py
date: 10/30/25
Purpose: Early version of ai implementation in python for web server
"""


import ollama

# this function gets responses form the ai
def get_response_from_ollama(user_input):
    # get a response from the modle
    ai_response = ollama.chat(model="gemma3:4b", messages=[{"role": "user", "content": user_input}])

    # Checks if the AI gave the user output
    if 'message' in ai_response:
        return ai_response['message']['content']
    else:
        return 'Sorry something went wrong.'
    
def main():
    # variables
    user_input = ""
    ai_response = ""

    # loop for testing the ai
    while(True):
        # Get the user response
        user_input = input("Ask the AI [/bye to exit]: ")

        # See if the user wants to quit
        if user_input == "/bye":
            break

        # Run it through ollama and save the output
        ai_response = get_response_from_ollama(user_input)

        # Return the output to the user
        print(ai_response)

        # print for space and split chats
        print()
        print("---------")
        print()





        
    
    
if __name__ == "__main__":
    main()

    

