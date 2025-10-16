#Visualizzazione risposta
risposta = None
try:
    risposta = llm.invoke(prompt.strip())
except Exception as e:
    logging.error(f"Errore nella generazione della risposta: {e}")

if risposta:
    print("\nRisultato:\n")
    print(getattr(risposta, "content", str(risposta)))
else:
    print("Nessuna risposta disponibile.")
