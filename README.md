# NornNet

Visit [NornNet](https://lab.wncc.edu/nornnet). Where the Fates Weave Destiny with a Touch of AI Magic - A private AI ChatBot that rocks!



## Team Members

- Eliezer Lamien
- Joe Scott
- Owen Osmera
- Shawn Noon

## Flask Tutorials

- [Chapter.16_Web_Development.pdf](https://itinstructor.github.io/WNCCComputerScience/Python/Web_Development/Chapter.16_Web_Development.pdf)
- [Flask Unit Converter](https://itinstructor.github.io/WNCCComputerScience/Python/Web_Development/Flask_Unit_Converter.pdf)
- [Flask Blog Tutorial](https://itinstructor.github.io/WNCCComputerScience/Python/Web_Development/Python_Flask_Blog_Tutorial.pdf)

## AI Private ChatBot Research

- [LM Studio Tutorial: Run Large Language Models (LLM) on Your Laptop](https://youtu.be/ygUEbCpOOLg?si=udEcraHqxw08DPsN)
- [Network Chuck Private AI](https://www.youtube.com/watch?v=WxYC9-hBM_g)
- [How to Build a Local AI Agent With Python (Ollama, LangChain & RAG)](https://youtu.be/E4l91XKQSgw?si=Q-Unp9DOsImHkXbS)
- [The Ultimate Guide to Local AI and AI Agents (The Future is Here)](https://youtu.be/mNcXue7X8H0?si=uSyVxAVtBBj1cMHZ)
- [Part 1 - Run Ollama with Python in 5 Minutes (Full Setup Guide](https://youtu.be/7uTt5t0B3H0?si=wlLhD5IsrULHp54X)
- [Part 2 - Local Ollama Chatbot in Python](https://youtu.be/CJVR4HE_j-0?si=2_1ByW7LU14GOgZ7)
- [Demo Creating an App Using Ollama OpenAI Python Client](https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Demo-Creating-an-App-Using-Ollama-OpenAI-Python-Client)
- [How to Create Your Own AI Chatbot Like DeepSeek with Ollama in Python Flask](https://www.codewithfaraz.com/python/112/how-to-create-your-own-ai-chatbot-like-deepseek-with-ollama-in-python-flask)
- [Learn Ollama in 15 Minutes - Run LLM Models Locally for FREE](https://youtu.be/UtSSMs6ObqY)

## Personal Research

- Integrate an LLM into flask with python https://github.com/ollama/ollama-python
- Create, read, and write to a PDF file https://github.com/py-pdf/pypdf
- Chat history/Memory/Context https://github.com/digithree/ollama-rag

## Create Pull Request on NornNet Github

1. Fork the NornNet Repository.
2. Pull local copy to your computer.
3. Make code changes.
4. Commit --> then Push to your repository
5. If your repository is not up to date --> Synchronize Changes.
6. Create a Pull Request.

## AI ChatBot Project (Private AI options)

- Please watch: [Video about Guild Project](https://wnccnet-my.sharepoint.com/:v:/g/personal/loringw_wncc_edu/EQc3SGTfIatAkoM0KrAEeMcBv-unJKhR9tElYD93-XLvCA?e=ixGNOO) (10-16-25)

Python Flask project to create a web chatbot. Private mode: host an open-source model yourself (local server, private cloud, or on-prem) for full control over data and privacy.

## Project Outline: Flask Chatbot (Private AI)

## 1. Project Goal 🎯

Build a reliable web chatbot. The app should let users exchange messages with an AI model and see streamed responses.

- Privacy-first solution running a private model server (containerized) with secure access and logging controls.

## 2. Key Technologies

- **Backend**: Python, Flask, Waitress (chat endpoint and API connector)
- **Frontend**: HTML, CSS, JavaScript 
- **Private AI**: local model server (lightweight runtime like llama.cpp / GGML for CPU quantized models)

---

## 3. Architecture & Implementation Plan

High level: Client (browser) -> Flask app -> (Private model server) -> Flask -> browser.

The implementation is split into phases so the team can ship incrementally.

## Phase 1: Setup Flask Server & Ollama Backend

### ✅ Install ollama on Windows 2025 Server

1. Download the latest [Ollama Release](https://github.com/ollama/ollama/releases) (e.g., ollama-windows-amd64.zip)
2. Extract the zip file --> place all files in c:\ollama
3. Add to system environment variables: c:\ollama
4. Verify installation: Open a Command Prompt:
5. Verify that gemma3:4b is installed as the model

   ```ollama --version```

5. Pull a Model to test with:
  
    ```ollama pull gemma3:4b```

### ✅ Set Up Ollama as a Windows Service (using NSSM)

This ensures Ollama starts automatically with the server and restarts if it ever crashes, without requiring a user to be logged in.

Step 1: Download NSSM

1. Go to the [NSSM download page](https://nssm.cc/download).
2. Download the latest release (e.g., nssm-2.24.zip).
3. Extract the ZIP file to a permanent location on your server, like C:\nssm

Step 2: Configure the Ollama Service with NSSM

1. Open an Administrator Command Prompt or Administrator PowerShell.

   ```nssm install Ollama```

This will open the NSSM service installer GUI.

Application Tab:

1. Path: Click the ... button and navigate to your ollama.exe file.
2. Startup directory: This should automatically populate to the correct folder.
3. Arguments: This is the most important part. Enter:

   ```serve```
  
This tells Ollama to run as a server.

4. Log on Tab: For a server, it's best to run this as a Local System account. Select the

 ```Local System account```

 radio button. This allows the service to run even when no user is logged in.
 
 5. Environment Tab: This is critical for allowing your Flask server to access Ollama.
 6. In the Environment variables box, add the following key-value pair:

   ```OLLAMA_HOST=0.0.0.0```

  This tells Ollama to listen for requests on all network interfaces, not just localhost.

  7. Click the ```Install service``` button. You should see a "Service 'Ollama' installed successfully!" message.

Step 3: Start the Service

1. Open the Windows Services app (run services.msc).
2. Find your new service named Ollama.
3. Right-click it and select Start.
4. Verify it's working: Open your server's web browser and navigate to:
  
   ```http://localhost:11434```

5. You should see the message "Ollama is running."

The Ollama server is now running as a persistent service on port 11434, accessible from other machines on your network.

☐ Todo — Draft README
🔄 In progress — Add examples and docs
✅ Complete — Initial release

## Flask Web Server

✅ Complete — Initial release

- Create `main_app.py` with routes for the homepage (`/`) and chat (`/chat`).
  - Dynamic base path support: set `BASE_PATH=/nornnet` in `.env` for production; leave unset locally to serve at root.
- Build `index.html` with a chat history, input, and send button.
- Implement minimal CSS to make the UI usable.
- Download the student handbook onto the server for the AI to reference
- Create virtual environment
  - Install python ollama library:

     ```pip install ollama```

## Phase 2: Frontend-Backend Communication

✅ Complete — Initial release

- Use `main.js` to send user messages to `/chat` and append both user and bot messages to the DOM.

## Phase 3 — Private AI Integration (self-hosted)

✅ Complete — Initial release

- CPU-only machines: prefer quantized models (GGML / llama.cpp) or small transformer models.
- Create a model server and expose an internal HTTP endpoint.
- Secure the private server: mTLS / API key, and run behind an IIS server which runs waitress

# Tasks for the week of 11/10/25 - 11/16/25

- Make the ai function a class for expandability.
  - DO NOT chage the AI function file only make a new file for the class.
  - SetUserQuestion
  - GetUserQuestion
  - GetAIResponse
  - SetAIPrompt
  - GetAIPrompt
- Find a way to get a pdf reader in python and integrate that into the code.
  - How do we add the student handbook as context for the ai?
  - This can be a function for class we just need a way to read the file to create words for prompting the ai.
- Find out if context can be enabled on ollama.
  - Integrate this into the code so the AI can have context
  - Research using CAG or RAG
- Add github repository address to docs page.
- Add responsive design to user interface. The interface should resize for different devices. Look at ChatGPT for an example
- - Add support for streaming responses if the model server supports it. This may provide a faster start to the response and a better user experience.

## Phase 4 — Privacy, Logging & Data Handling

☐ Todo

- Decide what to log (timestamps, anonymized session id, message length). Avoid storing PII by default.
- Add a user-facing privacy notice and an opt-out for logging.
- Implement retention policy and a script to sweep/delete logs older than X days.

## Phase 5 — Deploy & Ops

☐ Todo

- Add health checks, simple metrics (request counts, success/failure), and basic monitoring instructions.

---

### 4. Task Breakdown

This plan maps team roles to implement the privacy-oriented private mode.

#### Frontend (UI/UX)

- Team 1 (HTML & Structure): `index.html` — chat layout, message list, input form.
- Team 2 (CSS & Interactivity): `style.css` and `main.js` — chat bubbles, responsive layout, DOM updates, optimistic UI.

Shared goal: Deliver a clean, usable chat UI with graceful error states.

#### Backend (Flask Core)

- Team 3 (Server & Routing): `app.py` — create routes, session handling, simple persistence for sessions.
- Team 4 (Request & Response Handling): Implement `/chat` logic that validates input, forwards to the connector, and returns JSON or streaming responses.

Shared goal: Reliable, well-documented endpoints and simple persistence for conversation history.

#### AI Integration & Ops

- Team 5 (Private AI & Security): Implement local/private model server wiring and implement logging & retention rules. If hardware allows, tune for streaming and lower-latency inference.

Optional extras for the team:

- Add unit/integration tests for the connector code.
- Add a small evaluation page that replays test prompts and shows model outputs side-by-side.
- Add simple cost/latency telemetry so the team can compare different models.

---
### License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

Copyright (c) 2025 WNCC IT Program
