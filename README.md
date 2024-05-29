# TaskForceAI

A desktop application built with PyQt6 and Microsoft Autogen that allows users to customize and configure teams of AI agents who can carry out specialized tasks.

## Installation

```git clone https://github.com/evanbrooks0629/PyGUI.git```

```cd PyGUI```

```pip install PyQt6```

```pip install pyautogen```

```pip install groq```

```python3 app.py```

## Set Up

1. Confuguring your LLMs (Models tab)
   
There are 2 options for this, either to install Ollama or to get a Groq API key. You can download Ollama [here](https://ollama.com/) and you can get a Groq API key [here](https://console.groq.com/keys). There are different reasons to use Ollama / Groq. Ollama gives you the ability to host your own local LLM, while Groq offers free API requests remotely.

You can paste your Groq API key into the textbox if you are using Groq. Then, simply click on a model to select it.

2. Creating your Agents (Agents tab)

Give your agent a role, like "React.js Engineer". 

It's description helps you understand what this agent does, like "Software Engineer proficient in JavaScript and React". 

The Agent's system message is essentially your initial prompt to it; i.e., "You are a JavaScript and React expert, knowledgeable about web development. You are a part of a software engineering team that helps create large-scale web apps."

The Agent's max consecutive auto-reply is the maximum number of times the agent can be involved in a conversation. A normal range is between 1-5.

Create multiple agents. Other ideas include "Front-End Engineer", "Creative Writer", "Research Analyst", etc.

3. Creating a Team (Teams tab)

Each Team is composed of at least 2 Agents. These Teams can include any selection of Agents, ideally the ones that are all relevant for the task you will give them. For example, a Software Development Team can consist of a "Front-End Engineer", a "Back-End Engineer", and a "QA Engineer". Simply give your Team a name and select the Agents from the ones you have created.

4. Start a Chat (Chats tab)

To start a chat, simply select the Team you want to use, then ask it a question! For a Software Development team, a good question can be: "Develop a basic file system in Python" or "Create a Flask app".

Please note that output is nondeterministic, meaning you won't get the same output each time with the same prompt. The quality of your output depends on all factors, including the chosen LLM, the agent configurations, and team member relevance.

## Things to Do

This project is very far from complete. Some things to add include:
- [ ] Conversation flow in chats (respond to a response)
- [ ] Document uploads for agents and chats
- [ ] Adding functions or "Skills" to Autogen Agents (see an example [here](https://microsoft.github.io/autogen/docs/notebooks/agentchat_function_call_currency_calculator))

## Contribution / Help / Support / Questions

Contributors are welcome. Simply submit a PR to help :)

Any questions can be sent to me via email at evanbrooks0629@gmail.com.


