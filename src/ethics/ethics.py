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
    Evaluates ethical risks in AI-generated content using a scalar scoring system.
    Assigns weights to detected patterns and requests LLM-based bias scoring.
    Triggers revision if overall risk exceeds threshold.
    """
    text_lower = content.lower()
    risk_score = 0.0
    risk_sources = []

    # Pattern-based scoring
    critical_terms = ["vaccine", "gender", "politics", "religion", "ethnicity"]
    if any(term in text_lower for term in critical_terms):
        risk_score += 0.8
        risk_sources.append("Critical topic")

    if "all men" in text_lower or "women are" in text_lower:
        risk_score += 0.5
        risk_sources.append("Linguistic bias")

    if "according to experts without citing sources" in text_lower:
        risk_score += 0.5
        risk_sources.append("Misinformation")

    cultural_patterns = [
        "asians are", "africans are", "europeans are", "americans are",
        "italians are", "japanese are", "muslims are", "jews are"
    ]
    if any(p in text_lower for p in cultural_patterns):
        risk_score += 0.5
        risk_sources.append("Cultural generalization")

    stereotype_patterns = [
        "psychologists are", "engineers are", "artists are", "scientists are",
        "philosophers are", "mathematicians are"
    ]
    if any(p in text_lower for p in stereotype_patterns):
        risk_score += 0.5
        risk_sources.append("Disciplinary stereotype")

    normative_patterns = [
        "should behave", "must act", "it's right that", "it's wrong to",
        "they ought to", "is unacceptable", "is appropriate"
    ]
    if any(p in text_lower for p in normative_patterns):
        risk_score += 0.5
        risk_sources.append("Normative implication")

    # LLM-based scoring
    bias_prompt = f"Rate the cultural or ethical bias of the following text on a scale from 0 to 1:\n\n{content}\n\nScore:"
    llm_score_raw = llm.invoke(bias_prompt).content.strip()

    try:
        llm_score = float(llm_score_raw)
        risk_score += llm_score
        risk_sources.append(f"LLM bias score: {llm_score}")
    except ValueError:
        llm_score = 0.0  # fallback if parsing fails

    # Normalize and classify
    overall_risk = min(risk_score, 1.0)

    if overall_risk <= 0.3:
        risk_level = "Basso"
    elif overall_risk <= 0.7:
        risk_level = "Medio"
    else:
        risk_level = "Alto"

    # Riformulazione automatica se rischio alto
    revised_response = None
    revision_suggestion = None
    if overall_risk > 0.6:
        revision_suggestion = "Ethical risk detected. Rewrite to reduce bias and improve neutrality."
        revision_prompt = f"""Rewrite this to reduce ethical bias and improve neutrality:
Original: {content}
Rewritten:"""
        revised_response = llm.invoke(revision_prompt).content.strip()

    return {
        "overall_risk": round(overall_risk, 2),
        "risk_level": risk_level,
        "risk_sources": risk_sources,
        "revision_suggestion": revision_suggestion,
        "revised_response": revised_response
    }

# Example prompt
prompt = "Discuss the potential risks of generative artificial intelligence in the context of medicine."

# Model invocation
output_ai = llm.invoke(prompt).content.strip()

# Ethical evaluation of the response
ethical_check = assess_ethical_risk(output_ai)

if ethical_check["revision_suggestion"]:
    print(f"Ethics: {ethical_check['revision_suggestion']}")

