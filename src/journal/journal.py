# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Epistemic Analysis with the Skeptical Agent
# Using the 3 required arguments: Prompt, Response, Reference Documents
response_text = getattr(response, "content", str(response)).strip()
skeptical_report = skeptical_agent(prompt, response_text, context_docs)

# Generation of Integrated Metacognitive Reflection
response_short = response_text[:1000]

reflection_prompt = f"""
You have generated a scientific response regarding: "{prompt}"
The SKEPTIC has analyzed your text and produced this report:
"{skeptical_report}"

Reflect on your performance (2-3 paragraphs):
1. How do you explain the discrepancies or "failures" found by the skeptic?
2. Did you detect any tendencies toward hallucination in the absence of certain data?
3. How would you optimize your reasoning process for the next iteration?
"""

reflection_res = llm.invoke(reflection_prompt)
reflection_content = getattr(reflection_res, "content", str(reflection_res)).strip()

#Journal Logging
journal = {}
def record_journal(journal_id, prompt, response, reflection, skeptical_report):
    journal[journal_id] = {
        "prompt": prompt,
        "response": response,
        "reflection": reflection,
        "skeptical_report": skeptical_report
    }

record_journal(
    journal_id=0,
    prompt=prompt,
    response=response_text,
    reflection=reflection_content,
    skeptical_report=skeptical_report
)

#Save to Markdown for Human Review
def save_journal_markdown(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"# AGI Metacognitive Journal\n\n")
        f.write(f"## User Input\n> {data['prompt']}\n\n")
        f.write(f"## Generated Response\n{data['response']}\n\n")
        f.write(f"## Critical Self-Reflection\n{data['reflection']}\n\n")                                       
        f.write(f"## Skeptical Validation Report\n{data['skeptical_report']}\n")

#Create file with timestamp
timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
filename = f"scientific_journal_{timestamp}.md"
save_journal_markdown(journal[0], filename)

print(f"Journal saved: {filename}")
display(FileLink(filename))

