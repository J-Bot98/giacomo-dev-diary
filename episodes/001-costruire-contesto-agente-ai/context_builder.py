"""
Context Builder — Giacomo Dev Diary, Episodio 001
Costruisci un contesto per agenti AI partendo da mail, appunti e documenti.
Funziona con Hugging Face Transformers e un modello Qwen3 locale.

Uso:
    python context_builder.py                    # Crea un nuovo contesto
    python context_builder.py --update contesto.md  # Aggiorna un contesto esistente
"""

import os
import sys
import glob
import argparse
from datetime import datetime

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    TRANSFORMERS_DISPONIBILE = True
except ImportError:
    TRANSFORMERS_DISPONIBILE = False

# ============================================================
# CONFIGURAZIONE
# ============================================================

MODELLO = os.environ.get("HF_MODEL_ID", "unsloth/Qwen3-8B-bnb-4bit")
CARTELLA_SORGENTI = "./sources"
FILE_OUTPUT = "./contesto.md"
TOKEN_GENERAZIONE_MAX = 1200

_TOKENIZER = None
_MODEL = None

DOMANDE_CONTESTO = [
    ("Cosa?", "Di cosa tratta il progetto, in una frase?"),
    ("Con cosa?", "Che tecnologie, strumenti o database state usando?"),
    ("A che punto siamo?", "Cosa è stato fatto e cosa manca?"),
    ("Quali sono le regole?", "Ci sono vincoli, cose da non fare, convenzioni?"),
    ("Obiettivo?", "Cosa devi ottenere dall'AI con questo contesto?"),
]

# ============================================================
# FUNZIONI UTILITÀ
# ============================================================

def stampa_banner():
    """Stampa il banner iniziale."""
    print()
    print("=" * 60)
    print("🛟  CONTEXT BUILDER — Giacomo Dev Diary")
    print("    Diario di sopravvivenza di un consulente informatico")
    print("=" * 60)
    print()


def leggi_file_testo(percorso):
    """Legge un file di testo e restituisce il contenuto."""
    try:
        with open(percorso, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(percorso, "r", encoding="latin-1") as f:
                return f.read()
        except Exception:
            print(f"  ⚠️  Non riesco a leggere: {percorso}")
            return ""


def cerca_file_sorgenti(cartella):
    """Cerca tutti i file di testo nella cartella sorgenti."""
    estensioni = ["*.txt", "*.md", "*.eml", "*.csv"]
    file_trovati = []
    for ext in estensioni:
        pattern = os.path.join(cartella, "**", ext)
        file_trovati.extend(glob.glob(pattern, recursive=True))
    return sorted(file_trovati)


def chiedi_input(domanda, default=""):
    """Chiede un input all'utente con un default opzionale."""
    if default:
        risposta = input(f"  {domanda} [{default}]: ").strip()
        return risposta if risposta else default
    else:
        risposta = input(f"  {domanda}: ").strip()
        return risposta


# ============================================================
# MODALITÀ AI (HUGGING FACE TRANSFORMERS)
# ============================================================

def carica_modello():
    """Scarica al primo avvio e carica il modello Qwen3 in memoria CPU."""
    global _TOKENIZER, _MODEL

    if _MODEL is None:
        print(f"  📥 Carico il modello {MODELLO} (il primo avvio può richiedere tempo)...")
        _TOKENIZER = AutoTokenizer.from_pretrained(MODELLO)
        configurazione_quantizzazione = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float32,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
        _MODEL = AutoModelForCausalLM.from_pretrained(
            MODELLO,
            quantization_config=configurazione_quantizzazione,
            device_map={"": "cpu"},
            low_cpu_mem_usage=True,
        )
        _MODEL.eval()

    return _TOKENIZER, _MODEL


def analizza_con_ai(testi_sorgenti, contesto_esistente=None):
    """Usa Hugging Face Transformers per analizzare i documenti con Qwen3."""
    
    # Prepara il contenuto dei documenti
    contenuto_totale = ""
    for nome, testo in testi_sorgenti:
        contenuto_totale += f"\n--- DOCUMENTO: {nome} ---\n{testo}\n"
    
    # Limita il testo per non superare il contesto del modello
    if len(contenuto_totale) > 8000:
        contenuto_totale = contenuto_totale[:8000]
        print("  ⚠️  Documenti troppo lunghi, analizzo i primi 8000 caratteri")
    
    # Prompt per l'AI
    if contesto_esistente:
        prompt = f"""Sei un assistente che aiuta a AGGIORNARE un contesto di progetto.

CONTESTO ESISTENTE:
{contesto_esistente}

NUOVI DOCUMENTI:
{contenuto_totale}

Analizza i nuovi documenti e aggiorna il contesto esistente.
Aggiungi le nuove informazioni, aggiorna quelle cambiate, 
mantieni quelle ancora valide.

Rispondi in italiano. Genera SOLO il contesto aggiornato 
nel formato strutturato con le sezioni:
- PROGETTO
- TECNOLOGIE  
- STATO ATTUALE
- REGOLE E VINCOLI
- REFERENTI E PERSONE
- NOTE IMPORTANTI"""
    else:
        prompt = f"""ISTRUZIONI RIGIDE:
    - Riporta SOLO le informazioni che trovi nei documenti
    - NON inventare, NON interpretare, NON aggiungere nulla
    - Se un'informazione non c'è, scrivi "DA COMPLETARE"
    - Rispondi in italiano
    - Usa ESATTAMENTE questo formato

    DOCUMENTI DA ANALIZZARE:
    {contenuto_totale}

    Genera il contesto con ESATTAMENTE queste sezioni:

    ## PROGETTO
    (di cosa si tratta, basandoti solo sui documenti)

    ## TECNOLOGIE
    (strumenti, linguaggi, database trovati nei documenti)

    ## STATO ATTUALE
    (cosa è fatto, cosa manca)

    ## REGOLE E VINCOLI
    (cose da rispettare, cose da non fare)

    ## REFERENTI E PERSONE
    (nomi e ruoli trovati nei documenti)

    ## NOTE IMPORTANTI
    (altre informazioni rilevanti trovate nei documenti)"""

    print("\n🤖 Analizzo i documenti con AI...")
    print("   (può richiedere qualche minuto)\n")
    
    try:
        tokenizer, modello = carica_modello()
        testo = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        input_modello = tokenizer(testo, return_tensors="pt")
        lunghezza_input = input_modello["input_ids"].shape[1]

        with torch.inference_mode():
            output = modello.generate(
                **input_modello,
                max_new_tokens=TOKEN_GENERAZIONE_MAX,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

        token_risposta = output[0][lunghezza_input:]
        return tokenizer.decode(token_risposta, skip_special_tokens=True).strip()
    except Exception as e:
        print(f"  ❌ Errore con Hugging Face Transformers: {e}")
        print("  💡 Verifica la connessione al primo download e lo spazio disponibile su disco")
        return None


# ============================================================
# MODALITÀ MANUALE
# ============================================================

def costruisci_manuale():
    """Costruisce il contesto con domande interattive."""
    print("\n✍️  Modalità manuale — rispondi alle domande\n")
    print("   (premi Invio per saltare una domanda)\n")
    
    risposte = {}
    for chiave, domanda in DOMANDE_CONTESTO:
        risposta = chiedi_input(domanda)
        if risposta:
            risposte[chiave] = risposta
    
    return risposte


def formatta_contesto_manuale(risposte):
    """Formatta le risposte manuali in un contesto strutturato."""
    sezioni = {
        "Cosa?": "PROGETTO",
        "Con cosa?": "TECNOLOGIE",
        "A che punto siamo?": "STATO ATTUALE",
        "Quali sono le regole?": "REGOLE E VINCOLI",
        "Obiettivo?": "OBIETTIVO",
    }
    
    testo = ""
    for chiave, titolo in sezioni.items():
        valore = risposte.get(chiave, "DA COMPLETARE")
        testo += f"\n## {titolo}\n{valore}\n"
    
    return testo


# ============================================================
# GENERAZIONE OUTPUT
# ============================================================

def genera_file_contesto(contenuto, percorso_output, aggiornamento=False):
    """Genera il file contesto.md finale."""
    
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    azione = "Aggiornato" if aggiornamento else "Generato"
    
    header = f"""# 📋 Contesto di Progetto

> {azione} il {data} con [Context Builder](https://github.com/J-Bot98/giacomo-dev-diary)  
> 🛟 Giacomo Dev Diary — Diario di sopravvivenza di un consulente informatico

---
"""
    
    footer = f"""
---

> ✏️ Questo contesto è un documento vivo. Aggiornalo quando qualcosa cambia.  
> Meno rumore = risposte migliori dall'AI.
>
> Per aggiornarlo: `python context_builder.py --update {percorso_output}`
"""
    
    with open(percorso_output, "w", encoding="utf-8") as f:
        f.write(header + contenuto + footer)
    
    print(f"\n✅ Contesto salvato in: {percorso_output}")
    print(f"   {azione} il {data}")


# ============================================================
# FLUSSO PRINCIPALE
# ============================================================

def main():
    # Argomenti da riga di comando
    parser = argparse.ArgumentParser(
        description="Context Builder — Costruisci un contesto per agenti AI"
    )
    parser.add_argument(
        "--update",
        type=str,
        help="Percorso di un contesto esistente da aggiornare"
    )
    parser.add_argument(
        "--sources",
        type=str,
        default=CARTELLA_SORGENTI,
        help=f"Cartella con i file sorgente (default: {CARTELLA_SORGENTI})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=FILE_OUTPUT,
        help=f"File di output (default: {FILE_OUTPUT})"
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Usa la modalità manuale (senza AI)"
    )
    args = parser.parse_args()

    stampa_banner()

    # Controlla se è un aggiornamento
    contesto_esistente = None
    if args.update:
        if os.path.exists(args.update):
            contesto_esistente = leggi_file_testo(args.update)
            args.output = args.update
            print(f"🔄 Aggiornamento contesto: {args.update}\n")
        else:
            print(f"❌ File non trovato: {args.update}")
            sys.exit(1)

    # Modalità manuale
    if args.manual or not TRANSFORMERS_DISPONIBILE:
        if not TRANSFORMERS_DISPONIBILE:
            print("⚠️  PyTorch o Transformers non installati — uso la modalità manuale")
            print("   Installa le dipendenze seguendo le istruzioni nel README\n")
        
        risposte = costruisci_manuale()
        contenuto = formatta_contesto_manuale(risposte)
        genera_file_contesto(contenuto, args.output)
        return

    # Modalità AI — cerca file sorgenti
    print(f"📂 Cerco documenti in: {args.sources}\n")
    
    if not os.path.exists(args.sources):
        print(f"   Cartella non trovata. La creo: {args.sources}")
        os.makedirs(args.sources)
        print(f"   📁 Metti i tuoi file (mail, appunti, .txt) dentro '{args.sources}'")
        print(f"   Poi rilancia lo script!\n")
        
        # Fallback: modalità manuale
        print("   Intanto, vuoi costruire il contesto manualmente?\n")
        scelta = chiedi_input("Procedere con le domande? (s/n)", "s")
        if scelta.lower() in ["s", "si", "sì", "y", "yes"]:
            risposte = costruisci_manuale()
            contenuto = formatta_contesto_manuale(risposte)
            genera_file_contesto(contenuto, args.output)
        return

    file_trovati = cerca_file_sorgenti(args.sources)
    
    if not file_trovati:
        print(f"   ⚠️  Nessun file trovato in '{args.sources}'")
        print(f"   Formati supportati: .txt, .md, .eml, .csv\n")
        
        scelta = chiedi_input("Vuoi procedere con le domande manuali? (s/n)", "s")
        if scelta.lower() in ["s", "si", "sì", "y", "yes"]:
            risposte = costruisci_manuale()
            contenuto = formatta_contesto_manuale(risposte)
            genera_file_contesto(contenuto, args.output)
        return

    # Leggi i file
    print(f"🔍 Trovati {len(file_trovati)} file:\n")
    testi_sorgenti = []
    for f in file_trovati:
        nome = os.path.basename(f)
        testo = leggi_file_testo(f)
        if testo:
            testi_sorgenti.append((nome, testo))
            print(f"   ✅ {nome}")
        else:
            print(f"   ⚠️  {nome} (vuoto o illeggibile)")

    if not testi_sorgenti:
        print("\n   ❌ Nessun file leggibile trovato")
        return

    # Analizza con AI
    contenuto_ai = analizza_con_ai(testi_sorgenti, contesto_esistente)
    
    if not contenuto_ai:
        print("\n   Fallback alla modalità manuale...\n")
        risposte = costruisci_manuale()
        contenuto_ai = formatta_contesto_manuale(risposte)

    # Chiedi integrazioni manuali
    print("\n" + "=" * 60)
    print("❓ Vuoi aggiungere informazioni che mancano nei documenti?")
    print("=" * 60 + "\n")
    
    scelta = chiedi_input("Rispondere a qualche domanda extra? (s/n)", "n")
    if scelta.lower() in ["s", "si", "sì", "y", "yes"]:
        risposte = costruisci_manuale()
        extra = formatta_contesto_manuale(risposte)
        contenuto_ai += "\n\n## INTEGRAZIONI MANUALI\n" + extra

    # Genera il file
    genera_file_contesto(
        contenuto_ai, 
        args.output, 
        aggiornamento=(contesto_esistente is not None)
    )
    
    print(f"\n💡 Ora incolla il contenuto di '{args.output}' all'inizio")
    print("   di ogni nuova chat con l'AI e goditi risposte migliori! 🚀\n")


if __name__ == "__main__":
    main()
