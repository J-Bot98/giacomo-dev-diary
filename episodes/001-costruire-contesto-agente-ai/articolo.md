# Episodio 001 - Costruire un contesto per un agente AI

### 🛟 Diario di sopravvivenza di un consulente informatico

---

## Il Problema

Ciao a tutti! Benvenuti al primo episodio del diario dello sviluppatore!

Sono Giacomo, lavoro in Deloitte da 5 anni e nella vita ho sempre fatto 
lo sviluppatore: pigro, soprattutto. L'arrivo degli agenti di intelligenza 
artificiale generativa non ha fatto altro che alimentare la mia pigrizia, 
ma anche la mia voglia di sperimentare, creare, studiare e fare. Strano, vero?

Negli ultimi tempi l'IA ci sta travolgendo. Tutti che ci dicono 
*"usatela!", "apri Solaria!", "chiedi agli agenti AI!"*. 
Ma nessuno che ci insegni **come usarla davvero bene**.

In quanti di voi si sono trovati nella situazione di sparare a caso un prompt 
a un chatbot senza sapere dove mettere le mani? Io in primis!

Aprite la chat, scrivete la vostra domanda, e la risposta è **generica**, 
**sbagliata**, o talmente vaga che tanto valeva cercare su Google.

Riprovate. Riformulate. Aggiungete dettagli. 
E l'IA continua a girare intorno al problema senza mai centrarlo.

**Risultato?** Dopo mezz'ora avete perso tempo, pazienza, e quella poca 
fiducia che avevate nello strumento.

Ma il problema non è l'IA. Il problema è che **l'IA non sa niente di voi**, 
del vostro progetto, del vostro mondo.

---

## Una storia vera

Proprio mentre scrivevo questo articolo, un collega mi scrive:

> *"Ho iniziato a usare agenti AI, ma le conversazioni durano pochissimo prima di esaurirsi
> e poi la compressione automatica mi fa perdere dettagli. Come faccio?"*

Ci sono passato anche io. E la risposta che gli ho dato è stata semplice:

**Tieni aggiornato il contesto e, soprattutto, costruiscilo bene: può farti risparmiare tempo e risorse.**

Oggi la piattaforma Solaria permette di costruire contesti grazie al suo 
Context Builder: uno strumento utile per organizzare il lavoro, mantenere il 
filo della conversazione e migliorare la qualità delle risposte.

Ogni volta che apri una nuova conversazione è un po' come se arrivasse un 
nuovo collega su un progetto: la qualità delle risposte dipende anche dalle 
informazioni che gli mettiamo a disposizione. Le conversazioni possono 
superare i limiti di contesto, la compressione automatica può semplificare o 
perdere dettagli e gli allegati potrebbero non essere disponibili in una nuova chat.

Per questo il mio consiglio è: **costruite e condividete il vostro contesto**, 
anche quando usate gli strumenti integrati. Potete partire da un semplice 
file di testo, aggiornarlo quando serve e usarlo all'inizio di una nuova chat.

Lo strumento aiuta a mantenere il filo; un contesto chiaro aiuta l'AI a capire 
meglio il progetto e a darvi risposte più pertinenti.

Ma aspettate: prima di costruirne uno, capiamo bene cos'è un contesto.

---

## Ma cos'è un contesto?

Pensatela così. Immaginate di essere **il nuovo arrivato su un progetto**. 
Il vostro primo giorno: **non sapete nulla**.

Non sapete di cosa tratta il progetto, chi sono i referenti, quali decisioni 
sono state prese o dove trovare i documenti. Siete persi.

Ora immaginate che un collega gentile si sieda accanto a voi e vi dica:

> *"Il progetto è per un cliente bancario e stiamo rifacendo il sistema di 
> reportistica. Marco è il referente lato cliente, Laura prende le decisioni 
> tecniche, i dati arrivano da tre sorgenti e ogni venerdì ci allineiamo col cliente."*

In **30 secondi** avete una mappa. Sapete dove siete, con chi parlare e come 
muovervi. Quello è il **contesto**.

**Per un'AI è uguale identico.** Un modello non conosce automaticamente il 
vostro progetto. Se gli chiedete *"Fammi un riassunto di questo documento"*, 
può darvi una risposta generica. Se gli spiegate che il documento riguarda i 
requisiti di un flusso ETL bancario e chiedete di concentrarsi su regole di 
trasformazione e dipendenze tra tabelle, la risposta sarà più mirata.

La differenza? **Il contesto.**

### Una definizione

Nel 2025 Andrej Karpathy ha descritto il context engineering come l'arte e la 
scienza di inserire nella finestra di contesto le informazioni giuste per il 
passo successivo.

In parole povere: non conta solo come fai la domanda, ma anche **che cosa fai 
sapere all'AI prima di chiederle qualcosa**.

---

## Perché il contesto fa la differenza

Un modello AI è un software addestrato. Il contesto non lo modifica e non lo 
riaddestra: è l'insieme delle informazioni sul progetto che gli forniamo mentre 
lo usiamo.

La differenza è questa:

```text
CONTESTO: informazioni riutilizzabili del progetto
- Il servizio usa Python e FastAPI.
- Il database è PostgreSQL.
- Ogni endpoint deve avere test automatici.
- Non registrare dati sensibili nei log.

PROMPT: la richiesta di oggi
Scrivi l'endpoint GET /movimenti.
```

Il prompt dice **che cosa fare adesso**. Il contesto spiega **in quale mondo 
stiamo lavorando**. Domani potete riutilizzare lo stesso contesto per scrivere 
un test, diagnosticare un errore o documentare l'endpoint.

Il contesto non garantisce che la risposta sia corretta, ma dà all'AI elementi 
concreti per evitare di dover indovinare tecnologie, vincoli e obiettivi.

---

## Come si scrive un buon contesto?

Pensatelo come una scheda di progetto da consegnare a un collega appena arrivato.
Non serve raccontargli tutta la storia: servono le informazioni per iniziare a 
lavorare senza fare domande ogni cinque minuti.

Per costruirla, partite da queste cinque domande:

1. **Cosa stiamo facendo?** Descrivete il progetto in una frase.
2. **Con quali strumenti?** Indicate tecnologie, database e linguaggi.
3. **A che punto siamo?** Separate ciò che è fatto da ciò che manca.
4. **Quali regole dobbiamo rispettare?** Scrivete vincoli e convenzioni.
5. **Che cosa deve aiutarmi a fare l'AI?** Definite un obiettivo concreto.

Le risposte diventano il contenuto del vostro file `contesto.md`. Non deve 
essere perfetto né lunghissimo: deve essere chiaro e facile da aggiornare.

Se volete una sigla per ricordare gli elementi di una richiesta, potete usare 
**RCTF**: **Ruolo**, **Contesto**, **Task** (il compito) e **Formato** della 
risposta. Non è uno standard ufficiale, solo una checklist utile.

---

### Sì ok, ma io queste risposte NON ce le ho

Lo so. Benvenuti in consulenza.

Arrivi su un progetto e nessuno ti spiega niente. Quello che hai è un thread 
di mail infinito, un documento di requisiti vecchio di sei mesi, appunti presi 
al volo durante una call e, se sei fortunato, il codice.

Da questo caos dovresti costruirti un contesto? A mano? No grazie, sono pigro.

Per questo ho creato uno **script Python** che analizza documenti locali, fa 
qualche domanda per riempire i buchi e genera un file `contesto.md`. Se avete 
già un contesto, può aiutarvi ad aggiornarlo con le nuove informazioni.

**Voi gli date il caos, lui vi restituisce ordine.**

Il codice e la guida per provarlo sono nella cartella dell'episodio, nel file 
[README.md](README.md).

### Supporto e commenti

Avete provato a costruire il vostro contesto? Raccontatemi com'è andata, cosa 
ha funzionato e dove invece l'AI ha deciso di complicare le cose. Potete lasciare 
un commento, aprire una Issue su GitHub o scrivermi direttamente.

Al prossimo episodio!

---

## 📚 Fonti

- [Andrej Karpathy - Context engineering](https://x.com/karpathy/status/1937902205765607626) - riflessione sulla selezione delle informazioni da inserire nel contesto.
- [OpenAI - Prompt engineering best practices](https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt) - indicazioni per richieste chiare e contestualizzate.
- [Anthropic - Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) - approfondimento su come il contesto aiuta a recuperare informazioni rilevanti.
