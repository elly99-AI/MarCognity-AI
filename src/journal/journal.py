# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Estrai il contenuto testuale dalla risposta
response_text = getattr(response, "content", str(response)).strip()

# Ora puoi tagliare i primi 1000 caratteri
response_short = response_text[:1000]

reflection_prompt = f"""
You responded to the following prompt:
"{prompt}"

Your answer:
"{response_short}"


Now reflect briefly on how you arrived at this answer.

- What reasoning path led you to this response?
- What criteria guided your choices?
- Were there any risks or ambiguities you considered?
- How does this reflect your cognitive style?

Write a concise reflection in 2–3 paragraphs, using a clear and analytical tone.
"""

reflection = llm.invoke(reflection_prompt).content.strip()

journal = {}

def record_journal(journal_id, prompt, response, reflection):
    journal[journal_id] = {
        "prompt": prompt,
        "response": response,
        "reflection": reflection
    }

record_journal(journal_id=0, prompt=prompt, response=response, reflection=reflection)

def save_journal_markdown(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"# Reflective Journal\n\n")
        f.write(f"## Prompt\n> {data['prompt']}\n\n")
        f.write(f"## Response\n{data['response']}\n\n")
        f.write(f"## Metacognitive Reflection\n{data['reflection']}\n")

filename = f"journal_{datetime.datetime.utcnow().isoformat()}.md"
save_journal_markdown(journal[0], filename)