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

# Cache available models at module load
AVAILABLE_MODELS = []

def enumerate_models():
    """Enumerate all available Ollama models at startup."""
    global AVAILABLE_MODELS
    try:
        response = ollama.list()
        # response.models is a list of Model objects with .model attribute
        AVAILABLE_MODELS = [model.model for model in response.models]
        print(f"Available Ollama models: {AVAILABLE_MODELS}")
        return AVAILABLE_MODELS
    except Exception as e:
        print(f"Error enumerating models: {e}")
        return []

# Enumerate models at startup
enumerate_models()

# Bill 11/10/2025:
# Created MODEL constant for easier future changes.
# MODEL = "llama3:8b-instruct-q4_K_M"
# MODEL = "gemma3:4b"
# Similar model to gemma3:4b but fine-tuned for instruction following.
# MODEL = "gemma3:4b-it-qat"

# Model: llama3.1:8b-instruct-q4_K_M or llama3.1:8b
# Size: ~4.9-5 GB
# Speed: Similar to current (slightly slower but worth it)
# Accuracy: Much better than Gemma 4B, excellent reasoning
# Why: Llama 3.1 8B is one of the best CPU models for accuracy. The Q4_K_M quantization maintains quality while being CPU-efficient.
# This is the best model for CPU inference.
# Context Window: 128K tokens (huge!)
# Why Best: Specifically designed for RAG with massive context window, excellent at following instructions and not adding information beyond context
MODEL = "llama3.1:8b-instruct-q4_K_M"

# Memory Optimization Notes:
# The ollama.chat() options parameter supports memory-mapped I/O (use_mmap=True)
# which loads the model efficiently without loading the entire model into RAM at once.
# For best performance on systems with adequate RAM, also set use_mlock=True
# to prevent the model from being swapped to disk.


class ai_class():

    def __init__(self, model=None, memory_enabled=True):
        self.ai_response = ""
        self.user_question = ""
        self.ai_prompt = ""
        self.chat_log = ""
        # Use provided model or fall back to default MODEL constant
        self.model = model if model else MODEL

        # MEMORY SETTINGS [set to false if you want to disable chat logging]
        self.memory_enabled = memory_enabled
        self.memory_enabled = True
        self.chat_log = []  # <-- store conversation history

    # === Getters === #
    def get_user_question(self):
        return self.user_question

    def get_ai_response(self):
        try:
            # Get a response from the module with optimized memory settings
            # Options for efficient memory usage:
            # - use_mmap: Enable memory-mapped file I/O for efficient model loading
            # - use_mlock: Lock model in RAM to prevent swapping (set True if enough RAM)
            # - num_ctx: Context window size (reduce if memory constrained)
            # - num_thread: Number of threads (adjust based on CPU cores available)
            
            # JOE SCOTT 11/12/2025: CHAT HISTORY IS LOGGED HERE
            messages = []
            
            messages.append({
                # System prompt to set AI behavior 
                "role": "system",
                "content": "You are an ai teacher that is going to answer questions based on the prompt provided: " + self.ai_prompt
            })

            # Include chat history
            if self.memory_enabled and self.chat_log:
                messages.extend(self.chat_log)

            # User question
            messages.append({
                "role": "user",
                "content": self.user_question
            })

            self.ai_response = ollama.chat(
                model=self.model,  # Use instance model instead of global MODEL
                messages=messages,
                options={
                    "use_mmap": True,     # Enable memory-mapped I/O for efficient loading
                    "use_mlock": True,    # Set to True if you have enough RAM to lock model
                    # Context window (default 2048, reduce if low memory)
                    "num_ctx": 2048,
                    # Streaming response (set to True for real-time streaming)
                    "stream": True,
                    # CPU threads to use (adjust based on your CPU)
                    "num_thread": 8
                }
            )

            # Checks if the AI gave the user output
            if 'message' in self.ai_response:
                content = self.ai_response['message']['content']
            else:
                content = "Sorry, something went wrong."

            content = self.ai_response.get("message", {}).get("content", "Sorry, something went wrong.")

            # Save to chat log
            if self.memory_enabled:
                self.chat_log.append({"role": "user", "content": self.user_question})
                self.chat_log.append({"role": "assistant", "content": content})

            return content
        
        except Exception as e:
            # Log the specific error for debugging
            error_msg = f"Ollama connection error: {str(e)}"
            print(error_msg)  # This will go to waitress_app.log
            return f"Error: Could not connect to NornNet server. ({str(e)})"
        
        

    def get_ai_prompt(self):
        return self.ai_prompt

    # === Setters === #

    def set_user_question(self, user_question):
        self.user_question = user_question

    def set_ai_prompt(self, ai_prompt):
        self.ai_prompt = ai_prompt

    # === Memory Methods === #

    def clear_memory(self):
        """Reset the chat log."""
        self.chat_log = []

    def save_memory(self, filepath="ai_memory.json"):
        """Save chat log to a file."""
        import json
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.chat_log, f, ensure_ascii=False, indent=2)

    def load_memory(self, filepath="ai_memory.json"):
        """Load chat log from a file."""
        import os, json
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self.chat_log = json.load(f)
        else:
            self.chat_log = []


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
