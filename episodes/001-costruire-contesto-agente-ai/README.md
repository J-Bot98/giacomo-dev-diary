# Context Builder

Questo progetto contiene lo script Python dell'Episodio 001. L'articolo è in
[articolo.md](articolo.md); qui trovi installazione, modello e istruzioni d'uso.

Il Context Builder legge file `.txt`, `.md`, `.eml` e `.csv` dalla cartella
`sources`, li analizza con un modello locale e genera `contesto.md`. Supporta
anche l'aggiornamento di un contesto esistente e una modalità manuale.

## Modello consigliato per questo PC

Il default è [Qwen3-8B in quantizzazione 4-bit](https://huggingface.co/unsloth/Qwen3-8B-bnb-4bit),
caricato con **Hugging Face Transformers** e `bitsandbytes` su CPU. Il checkpoint
quantizzato occupa circa **6,1 GB da scaricare**.

Con il tuo Ryzen 7 PRO 7840U e 32 GB di RAM è una scelta fattibile. La Radeon
780M è una GPU integrata: questo setup non la usa come una GPU CUDA, quindi la
generazione avviene sulla CPU e sarà più lenta che su una scheda video dedicata.
La memoria effettiva durante l'esecuzione è superiore alla dimensione del
download, ma 32 GB lasciano margine per pesi quantizzati, cache e sistema.

Se preferisci ridurre download e tempi, puoi passare a
[Qwen3-4B 4-bit](https://huggingface.co/unsloth/Qwen3-4B-bnb-4bit), che occupa
circa **2,65 GB**. Per il Context Builder partirei comunque dall'8B: l'estrazione
di informazioni da appunti e documenti trae beneficio dal modello più capace.

## Installazione su Windows

Serve Python 3.10 o superiore a 64 bit e una CPU compatibile AVX2. In questo
ambiente è disponibile Python 3.11; i comandi sotto lo selezionano esplicitamente.
Il primo setup e il download iniziale del modello richiedono una connessione Internet.

Dalla root del repository, entra prima nella cartella dell'episodio e crea lì
un ambiente virtuale dedicato:

```powershell
cd .\episodes\001-costruire-contesto-agente-ai
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installa la build CPU di PyTorch, poi Transformers, Accelerate e bitsandbytes:

```powershell
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

Al primo avvio, Transformers scarica automaticamente il checkpoint quantizzato
da Hugging Face e lo salva nella cache locale dell'utente. Gli avvii successivi
riusano il modello scaricato; l'inferenza avviene sul PC, senza Ollama o LM Studio.

Per usare il modello più piccolo, imposta l'ID prima di avviare lo script:

```powershell
$env:HF_MODEL_ID = "unsloth/Qwen3-4B-bnb-4bit"
python context_builder.py
```

Per tornare al default 8B in quella sessione PowerShell:

```powershell
Remove-Item Env:HF_MODEL_ID
```

## Utilizzo

1. Metti i documenti di progetto in `sources`.
2. Attiva l'ambiente virtuale e avvia:

   ```powershell
   python context_builder.py
   ```

3. Trovi il risultato in `contesto.md`.

### Provare gli esempi inclusi

La cartella `example_sources` contiene appunti, una conversazione email,
requisiti e un verbale su un progetto completamente fittizio. Per usarli senza
copiare o sovrascrivere i tuoi documenti, assicurati che PowerShell sia nella
cartella dell'episodio (`episodes\001-costruire-contesto-agente-ai`) e avvia:

```powershell
python context_builder.py --sources .\example_sources --output .\contesto_demo.md
```

Il primo avvio scarica il modello dalla cache Hugging Face; le esecuzioni
successive riutilizzano i file gia' scaricati. Il risultato demo viene salvato
in `contesto_demo.md`.

Per aggiornare un contesto:

```powershell
python context_builder.py --update contesto.md
```

Per costruirlo senza modello:

```powershell
python context_builder.py --manual
```

Se il modello o Transformers non sono disponibili, lo script propone la
modalità manuale.

## Riferimenti tecnici

- [Qwen3-8B 4-bit su Hugging Face](https://huggingface.co/unsloth/Qwen3-8B-bnb-4bit)
- [Qwen3-4B 4-bit su Hugging Face](https://huggingface.co/unsloth/Qwen3-4B-bnb-4bit)
- [Documentazione Qwen3 in Transformers](https://huggingface.co/docs/transformers/model_doc/qwen3)
- [Installazione Transformers: CPU e PyTorch](https://huggingface.co/docs/transformers/installation)
- [Quantizzazione bitsandbytes e supporto CPU](https://huggingface.co/docs/transformers/quantization/bitsandbytes)