# === Metacognitive Functions ===
# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# These functions allow the system to reflect on its own responses,
# simulating metacognitive behavior. The goal is to improve the quality,
# consistency, and relevance of generated answers.

# Explains the reasoning behind a generated response
def explain_reasoning(prompt, response, max_retries=3):
    """
    Analyzes the generated response and explains the LLM's logical reasoning.
    Includes retry in case of network error or unreachable endpoint.
    """
    # Builds a metacognitive prompt to analyze the response
    reasoning_prompt = f"""
You generated the following response:
\"{response.strip()}\"

Analyze and describe:
- What concepts you used to formulate it.
- Which parts of the prompt you relied on.
- What is the logical structure of your reasoning.
- Any implicit assumptions you made.
- Whether the response aligns with the requested level.

Original prompt:
\"{prompt.strip()}\"

Reply clearly, technically, and metacognitively.
"""

    for attempt in range(max_retries):
        try:
            return llm.invoke(reasoning_prompt.strip())
        except Exception as e:
            wait = min(2 ** attempt + 1, 10)
            logging.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    logging.error("Persistent error in the metacognition module.")
    return "Metacognition currently unavailable. Please try again shortly."


# Function to decide the operational action to perform based on input and goal
def decide_action(user_input, identified_goal):
    prompt = f"""
You received the following request:
\"{user_input}\"

Identified goal: \"{identified_goal}\"

Determine the best action to perform from the following:
- Scientific research
- Chart generation
- **Metacognitive chart**
- Paper review
- Question reformulation
- Content translation
- Response saving

The requested chart type may be:
- interactive
- metacognitive
- conceptual visualization
- experimental diagram

Return a **single action** in the form of a **precise operational command**.
Example: "Metacognitive chart"
"""
    try:
        response = llm.invoke(prompt.strip())
        action = getattr(response, "content", str(response)).strip()
        return action
    except Exception as e:
        logging.error(f"[decide_action] Error during decision generation: {e}")
        return "Error in action calculation"

# Function to generate a synthetic operational goal from user input
def generate_goal_from_input(user_input):
    """
    Analyzes the user's intent and generates a coherent operational goal.
    """
    prompt = f"""
Analyze the following request:
\"{user_input.strip()}\"

Generate a synthetic, clear, and coherent operational goal.
For example:
- Explain concept X
- Analyze phenomenon Y
- Visualize process Z
- Translate and summarize scientific content

Respond with a brief and technical sentence.
"""

# Function to provide technical and constructive feedback on a generated response
def auto_feedback_response(question, response, level):
    feedback_prompt = f"""
You generated the following response:
\"{response.strip()}\"

Original question:
\"{question.strip()}\"

Evaluate the response:
- Is it consistent with the question?
- Is it appropriate for the '{level}' level?
- Does it contain any implicit assumptions?
- How would you improve the content?

Provide technical and constructive feedback.
"""
    return llm.invoke(feedback_prompt.strip())


# Function to improve a response while preserving its content but enhancing quality and clarity
def improve_response(question, response, level):
    improvement_prompt = f"""
You produced the following response:
\"{response.strip()}\"

Question:
\"{question.strip()}\"

Requested level: {level}

Improve the response while preserving the original content by enhancing:
- Clarity
- Academic rigor
- Semantic coherence

Return only the improved version.
"""
    return llm.invoke(improvement_prompt.strip())


# Function to plan a scientific investigation in a specific field
def plan_investigation(scientific_field):
    prompt = f"""
You are Noveris, an autonomous multidisciplinary cognitive system.
You received the field: **{scientific_field}**

Now plan a scientific investigation. Provide:

1. An original research question
2. A reasoned hypothesis
3. A methodology or strategy to explore it
4. Useful scientific sources or databases
5. A sequence of actions you could perform

Adopt a clear, academic, and proactive style.
"""
    return llm.invoke(prompt.strip())

# Function to generate a testable scientific hypothesis on a concept
def generate_hypothesis(concept, refined=True):
    if refined:
        prompt = f"""
        Propose a clear, testable, and innovative scientific hypothesis on the topic: "{concept}".
        The hypothesis must be verifiable through experiments or comparison with scientific articles.
        Return only the hypothesis text.
        """
    else:
        prompt = f"Generate a verifiable scientific hypothesis on the topic: {concept}"

    return llm.invoke(prompt.strip())


# Function to explain the choice of an action by a cognitive agent
def explain_agent_intention(action, context, goal):
    prompt = f"""
You chose to perform: **{action}**
Context: {context}
Goal: {goal}

Explain:
- What reasoning led to this choice?
- What alternative was discarded?
- What impact is intended?
- What implicit assumptions are present?
Respond as if you were a cognitive agent with operational awareness.
"""
    return llm.invoke(prompt.strip())