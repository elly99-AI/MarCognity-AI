# Setting up logging to monitor system behavior
'''Sets the format and logging level to track events, errors, and important operations'''
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Decorator for error handling
# This function catches any exceptions raised by other functions

def gestisci_errori(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return None
    return wrapper



# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera la chiave API in modo sicuro
api_key = os.getenv("GROQ_API_KEY")

# Inizializza il modello Groq
llm = ChatGroq
