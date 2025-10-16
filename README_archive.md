# NornNet

Where the Fates Weave Destiny with a Touch of AI Magic - A private AI ChatBot

## Team Members

- Elizier Lamen
- Owen Osmera
- Christi Pendergraft
- Joe Scott
- Caleb Stewart
- Shawn Noon
- Jens Boerman

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

## AI ChatBot Project (Private AI options)

Python Flask project to create a web chatbot. Private mode: host an open-source model yourself (local server, private cloud, or on-prem) for full control over data and privacy.

### Project Outline: Flask Chatbot (Private AI)

#### 1. Project Goal 🎯

Build a reliable web chatbot. The app should let users exchange messages with an AI model and see streamed responses.

- Privacy-first solution running a private model server (containerized) with secure access and logging controls.

#### 2. Key Technologies

- **Backend**: Python, Flask, Waitress (chat endpoint and API connector)
- **Frontend**: HTML, CSS, JavaScript 
- **Private AI**: local model server (lightweight runtime like llama.cpp / GGML for CPU quantized models)

---

### 3. Architecture & Implementation Plan

High level: Client (browser) -> Flask app -> (Private model server) -> Flask -> browser.

The implementation is split into phases so the team can ship incrementally.

#### Phase 1 — Basic Flask Server & UI

- Create `app.py` with routes for the homepage (`/`) and chat (`/chat`).
- Build `index.html` with a chat history, input, and send button.
- Implement minimal CSS to make the UI usable.

#### Phase 2 — Frontend-Backend Communication

- Use `main.js` to send user messages to `/chat` and append both user and bot messages to the DOM.
- Implement a temporary backend response for testing (hardcoded echo).

#### Phase 3 — Private AI Integration (self-hosted)

- CPU-only machines: prefer quantized models (GGML / llama.cpp) or small transformer models.
- Create a model server and expose an internal HTTP endpoint.
- Secure the private server: mTLS / API key, and run behind an IIS server which runs waitress
- Add support for streaming responses if the model server supports it.

#### Phase 4 — Privacy, Logging & Data Handling

- Decide what to log (timestamps, anonymized session id, message length). Avoid storing PII by default.
- Add a user-facing privacy notice and an opt-out for logging.
- Implement retention policy and a script to sweep/delete logs older than X days.

#### Phase 5 — Deploy & Ops

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

Notes and safety:

- For private hosting, pick a model size that fits your hardware. Quantized CPU models are great for demos and privacy.
- Make privacy decisions explicit in the app UI (logging on/off, data retention).

**Shared Goal**: Create an intuitive and attractive user interface.

#### **Team 2: The Backend Team (Flask Core)** ⚙️

This pair builds the server-side foundation of the application.

- **Team 3 (Server & Routing)**: Set up the `app.py` file, initialize the Flask application, and create the routes for the home page (`/`) and the chat endpoint (`/chat`).
- **Team 4 (Request & Response Handling)**: Implement the logic within the routes to handle incoming `POST` requests from the frontend. Manage the data flow, ensuring that user input is correctly received and that responses are sent back in the proper JSON format.

**Shared Goal**: Build a stable and reliable server that connects the frontend to the AI logic.

#### **Team 3: The AI Integration Team (API Connectors)** 🧠

This pair focuses on the "smart" part of the chatbot.

- **Team 5 (API Research & Logic)**: Research suitable conversational models on the Hugging Face Hub. Write the core Python function that takes a user's message, formats it correctly, and sends it to the Hugging Face Inference API.

## Project Ideas

### 1. Personal To-Do List ✅

A simple, single-user application to keep track of tasks. This avoids the complexity of collaboration and multiple accounts.

- **Key Features**: A user can register and log in. Once logged in, they can add tasks, mark tasks as complete, and delete them.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend)**: Set up the database models for `User` and `Task`. Create the Flask routes to add, update, and delete tasks.
  - **Students 3 & 4 (Authentication & Forms)**: Handle the user registration and login logic. Create the web forms for adding and editing tasks.
  - **Students 5 & 6 (Frontend)**: Design the Jinja2 templates to display the task list and forms. Apply CSS to make it look clean.

---

### 2. Simple Recipe Book 🍲

A website to display a collection of recipes. This project focuses on reading data from a database and presenting it nicely.

- **Key Features**: A public homepage that lists all available recipes. Clicking a recipe shows a detailed view with ingredients and instructions. An admin page allows for adding or editing recipes.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create the `Recipe` model in the database and populate it with a few examples. Write the routes to show all recipes and a single recipe detail page.
  - **Students 3 & 4 (Admin Panel)**: Build a simple admin page (no complex login needed at first) with a form to add new recipes to the database.
  - **Students 5 & 6 (Frontend)**: Design the templates for the recipe list and the detailed recipe view, focusing on readability.

---

### 3. Micro-Blog ✍️

A single-author blog where one person can log in to post updates, and the public can read them. This is a great introduction to content management.

- **Key Features**: A login page for the author. An interface for the author to create, edit, and delete posts. A public-facing page that lists all posts chronologically.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create the `User` and `Post` models. Implement the routes for creating and deleting posts.
  - **Students 3 & 4 (Authentication)**: Implement a simple login/logout system for the single author. Protect the "new post" page so only the author can access it.
  - **Students 5 & 6 (Frontend)**: Design the templates for the main blog feed and the form for creating a new post.

---

### 4. Simple Guestbook 📖

A classic web project where visitors can leave a short message. It's a great way to learn how to handle form submissions.

- **Key Features**: A single page that displays a list of messages. A form where a visitor can enter their name and a message to be added to the list.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create a simple `Message` model (name, content, timestamp). Write the single Flask route that both displays messages and handles the form submission for new ones.
  - **Students 3 & 4 (Form Handling)**: Create the web form for submitting a new message and add basic validation (e.g., name and message cannot be empty).
  - **Students 5 & 6 (Frontend)**: Design the single Jinja2 template that shows the list of messages and the submission form.

---

### 5. URL Shortener (Basic Version) 🔗

A tool that takes a long URL and generates a short link. This is an excellent project for understanding routes and database lookups.

- **Key Features**: A homepage with a form to submit a long URL. The app generates a unique short code, saves both URLs, and displays the new short link. When the short link is visited, the user is redirected to the original URL.
- **Task Breakdown**:
  - **Students 1 & 2 (Core Logic & Database)**: Design the `Link` model. Write the function to generate a random, unique short code.
  - **Students 3 & 4 (Routes)**: Create the main route for the submission form and the dynamic route that captures the short code and performs the redirect.
  - **Students 5 & 6 (Frontend)**: Design the simple HTML form and the result page that shows the user their shortened URL.

---

### 6. Event Calendar 📅

A simple site that lists upcoming events. This project avoids the complexity of ticketing and user roles.

- **Key Features**: A page that lists events with their date, time, and description. An admin area to add, edit, or delete events.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create the `Event` model (title, date, description). Write the public route to display the list of all events.
  - **Students 3 & 4 (Admin Panel)**: Build the forms and routes for the admin to perform CRUD (Create, Read, Update, Delete) operations on events.
  - **Students 5 & 6 (Frontend)**: Design the Jinja2 templates for the public event list and style them to look like a calendar or agenda.

---

### 7. Simple Poll App 📊

An application where an admin can create a single poll and anyone can vote and see the results.

- **Key Features**: An admin page to create a poll with a question and a few options. A public voting page. A results page that shows how many votes each option received.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Design models for `Poll` and `Vote`. Create the route that handles saving a new poll created by the admin.
  - **Students 3 & 4 (Voting & Results)**: Create the routes for the voting page (which records a vote) and the results page (which counts the votes).
  - **Students 5 & 6 (Frontend)**: Design the three pages: the admin creation form, the public voting page, and the results page.

---

### 8. Digital Flashcard App 🧠

A study tool where a user can create decks of flashcards and quiz themselves.

- **Key Features**: A user can create a "deck." Within a deck, they can add "cards," each with a front (question) and a back (answer). A quiz mode displays the front and reveals the back on a button click.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Design the `Deck` and `Card` models. Create routes for viewing decks and the cards within them.
  - **Students 3 & 4 (Forms & Logic)**: Create the forms for adding new decks and new cards. Implement the logic for the "quiz" page.
  - **Students 5 & 6 (Frontend & Interactivity)**: Design the templates. Use a small amount of JavaScript to handle the "flip card" functionality on the quiz page.

---

### 9. Simple Contact Book 📇

A private, single-user address book to store contact information.

- **Key Features**: A user can log in. They can add contacts with a name, phone number, and email. They can view, edit, and delete their contacts.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create `User` and `Contact` models. Write the routes for adding, editing, and deleting contacts.
  - **Students 3 & 4 (Authentication & Forms)**: Handle user login. Create the form for adding/editing a contact.
  - **Students 5 & 6 (Frontend)**: Design the main dashboard that lists all contacts and the form pages.

---

### 10. "Quote of the Day" Website 💬

A very simple website that displays a new, random quote each day.

- **Key Features**: A database of quotes. The homepage displays one random quote. An admin page allows adding new quotes to the database.
- **Task Breakdown**:
  - **Students 1 & 2 (Backend & Database)**: Create a `Quote` model (text, author). Write the main route that selects a random quote from the database and passes it to the template.
  - **Students 3 & 4 (Admin Panel)**: Build a simple form and route for an admin to add new quotes.
  - **Students 5 & 6 (Frontend)**: Design a visually appealing homepage to display the quote of the day.


## Project Names for Future Projects

- OdinChat – wise and all-seeing.
- LokiTalk – mischievous and clever, perfect for a witty assistant.
- FenrirBot – fierce and untamed, for a bold AI.
- ValhallaTalk – epic and heroic, for a grand assistant.
- NornNet – named after the fates who weave destiny.
- AsgardAI – the realm of the gods, lofty and powerful. 

Project Ragnarok: While Ragnarok is the "end of the world," in a project context it can signify the final, ultimate version of a build or a stress-testing application designed to push a system to its limits.

1. OdinCode- All-seeing god meets all-seeing code.
2. ThorByte - Hammering out powerful code and projects.
3. LokiLogic - Clever, unpredictable algorithms and coding.
4. ValhallaDev - A heaven for developers and their code.
5. AsgardianTech - Divine tech from the realm of the gods.
6. FreyaStack - Beauty and brains in full-stack development.
7. MjolnirLabs - Where code hits like a thunderbolt.
8. YggdrasilNet - The tree that connects all systems—like your project architecture.
9. HeimdallHub - The guardian of gateways (perfect for network-related projects).
10. TyrScripts - Justice in clean, efficient scripting.
11. RunicCode - Ancient runes meet modern syntax.
12. NorseNode - A network or idea node with mythic roots.
13. BifrostBridge - Bridging users and data like the rainbow bridge.
14. OdinWare - Software that sees all, like the Allfather.
15. FrostGiant.dev - Big ideas, colder execution. Great for back-end-heavy projects.
16. SagaSys - Every project tells a saga. Ideal for system design.
17. RagnarokAI - Where machine learning meets the end of the old world.
18. NornNet - The Norns wove fate; you weave networks.
19. SkadiSoft - Precision and cold beauty in user interface.
20. FenrirCode - Unleashing wild and powerful code—best for disruptive apps.
21. AsgardOps – "Where All Systems Ascend."
22. ValkyrieVision – "Guiding Your Code to Glory."
23. RuneLogic – "Decoding the Secrets of Smart Systems."
24. MjolnirBuild – "Hammer Out Powerful Deployments."
25. BifrostBridge – "Connecting Worlds of Data and Code."
26. FenrirGuard – "Unleash Security That Bites Back."
27. JotunCompute – "Giant Power for Massive Processing."
28. SleipnirSpeed – "Ride Eight-Legged Fast to Delivery."
29. HodrShadow – "Silent Strength for Dark Ops."
30. VanaheimVault – "Store Your Secrets Like the Gods."
31. EinherjarTest – "Battle-Tested for Ultimate Reliability."
32. GjallarhornAlert – "Sound the Alarm Before Chaos Strikes."
33. NornPredict – "Fate-Driven Forecasting for Your Data."
34. SurtrFire – "Ignite Performance with Relentless Heat."
35. HrimfaxiSync – "Night-Rider Speed for Data Sync."
36. AlfheimUI – "Light-Elf Elegance for Your Interfaces."
37. VíðarrSilent – "Quiet Power for Background Tasks."
38. RatatoskrLink – "Fast Messaging Across the Tree of Life."
39. GungnirDeploy – "Strike True with Precision Deployments."
40. DraupnirScale – "Infinite Replication, Just Like the Ring."