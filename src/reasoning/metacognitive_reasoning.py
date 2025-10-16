# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# This function simulates an intentional decision-making process by the AI agent.
# It analyzes the proposed action in relation to the goal, available alternatives, and context.
# Metacognition functions that adapt to the system
def execute_intentional_choice(action, goal, alternatives, context):
    ai_explanation = choice_with_intention(action, goal, alternatives, context)
    explanation_content = getattr(ai_explanation, "content", str(ai_explanation)).strip()

    intentional_log.append({
        "action": action,
        "reason": explanation_content,
        "impact": f"Expected outcome for goal: {goal}",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

    return explanation_content

# Generates a response with intentionality by combining reasoning, AI response, and extracted text
def generate_response_with_intention(prompt, action, goal, alternatives, context):
    reasoning = execute_intentional_choice(action, goal, alternatives, context)
    ai_response = llm.invoke(prompt)
    response_text = getattr(ai_response, "content", str(ai_response)).strip()

    return f"{response_text}\n\n*Agent's intentional explanation:*\n{reasoning}"