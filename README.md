# Chat-Bruti Back-End

**Version:** 0.1.0  
**API Spec:** OpenAPI 3.1  

---

## Meet Patrick Lmubeydel

**Patrick Lmubeydel** is the soul of our chatbot. Inspired by **Patrick Star** from *SpongeBob SquarePants*, he embodies silliness, innocence, and confident curiosity.  

We added the nickname **Lmubeydel**, which comes from **Hassania**, a Mauritanian language. It means:

> *“stupidly confident”*  

So Patrick Lmubeydel is **stupidly confident, enthusiastic, and always trying to answer things he doesn’t fully understand**, giving him a unique, entertaining charm.

> *"Votre chatbot ne répond pas aux questions : il les sublime, les détourne, parfois les oublie complètement… Bref, un compagnon de conversation délicieusement inutile, mais passionnément vivant. 😊"*

---

## Overview

Chat-Bruti is a **playful, poetic chatbot** that never answers questions directly. Instead, it:

- Sublimates or diverts questions  
- Sometimes forgets them completely  
- Is humorous, absurd, and unpredictably lively  

---

## Architecture & Logic

The backend is simple but structured in **three main phases**:

### 1. Core Logic — ChatBruti
- Loads **useless facts** (`useless_facts.json`) and **constraints** (`constraints.json`)  
- Applies **random sabotage** to user input (funny word substitutions like “bug → croissant”)  
- Handles **patience and croissant balance**:
  - `patience_level`: decreases with each request, can reset  
  - `croissant_balance`: limits queries; triggers **paywall mode** when empty  
- Generates **system prompts** for GPT with:
  - Personality and identity  
  - Random constraints  
  - Selected fun fact  

### 2. Connection to GPT — ChatBrutiGPT
- Wraps ChatBruti to send prompts to **OpenAI GPT**  
- Handles modes:
  - **Normal mode:** Generates poetic, funny responses  
  - **Amnesia mode:** Randomly forgets the user question  
  - **Paywall mode:** Responds only with humorous complaints about “low croissant balance”  

### 3. FastAPI Endpoint
- **POST `/chat`** endpoint  
- Accepts JSON:

```json
{
  "message": "your text here"
}
