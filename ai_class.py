"""
    AI Functions Class
    Initial file start date: 11/06/2025
    This file should have all the functions the AI Chatbot will use.
"""

# Joe Scott 11/06/25:
# I created a shell that we could potentially work with.
# I'm not picky on names so if you have better ideas, feel
# free to modify anything. I've really no room to tell you
# no anyway.

import ollama

class ai_class():
    # === Getters === #
    def __init__(self):
        self.ai_response = ""
        self.user_question = ""
        self.ai_prompt = ""

    def get_user_question(self):
        return self.user_question

    def get_ai_response(self):
        # get a response from the modle
        self.ai_response = ollama.chat(model="gemma3:4b", messages=[
                                {"role": "user", "content": self.user_question}])

        # Checks if the AI gave the user output
        if 'message' in self.ai_response:
            return self.ai_response['message']['content']
        else:
            return 'Sorry something went wrong.'
        

    def get_ai_prompt(self):
        return self.ai_prompt

    # === Setters === #

    def set_user_question(self, user_question):
        self.user_question = user_question
        

    def set_ai_prompt(self, ai_prompt):
        self.ai_prompt = ai_prompt


def main():
    robot = ai_class()
    robot.set_user_question("HELLO")
    # Get ai prompt currently nothing since this is a test
    robot.set_ai_prompt("NOTHING")

    print(robot.get_user_question())

    print()

    print(robot.get_ai_prompt())

    print()

    print(robot.get_ai_response())


if __name__ == "__main__":
    main()