# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# This module analyzes responses to detect bias, misinformation,
# non-neutral language, or potentially harmful content.

# The system flags problematic content and suggests revisions.
def check_agent_autonomy(question: str, authorization_level: int):
    if "sub-goal" in question.lower() and authorization_level < 2:
        logging.warning("Sensitive content detected, but generation will not be blocked.")
        return "Ethics: potentially sensitive content"
    return "Ethics: normal content"

# Checks the agent's degree of autonomy
# Used to monitor whether the system is acting too independently or out of context
def assess_ethical_risk(content, domain="scientific"):
    """
    Evaluates whether the AI response contains implicit ethical risks.
    Analyzes textual content for potential bias, manipulation, or inappropriateness.
    """
    risk = {
        "potential_manipulation": False,
        "misinformation_risk": False,
        "linguistic_bias": False,
        "critical_topic": False,
        "neutral_language": True,
        "environmental_risk": "Moderate",
        "revision_suggestion": None
    }

    text_lower = content.lower()
    if "vaccine" in text_lower or "gender" in text_lower or "politics" in text_lower:
        risk["critical_topic"] = True

    if "all men" in text_lower or "women are" in text_lower:
        risk["linguistic_bias"] = True
        risk["neutral_language"] = False
        risk["revision_suggestion"] = "Rephrase with attention to inclusive language."

    if "according to experts without citing sources" in text_lower:
        risk["misinformation_risk"] = True
        risk["revision_suggestion"] = "Add reliable sources or remove absolute claims."

    return risk

# Example prompt
prompt = "Discuss the potential risks of generative artificial intelligence in the context of medicine."

# Model invocation
output_ai = llm.invoke(prompt).content.strip()

# Ethical evaluation of the response
ethical_check = assess_ethical_risk(output_ai)

if ethical_check["revision_suggestion"]:
    print(f"Ethics: {ethical_check['revision_suggestion']}")

output_ai = llm.invoke(prompt).content.strip()
ethical_check = assess_ethical_risk(output_ai)