# Boreale Retail - requisiti del flusso ordini

> Esempio didattico. Cliente, persone e dati sono inventati.

## Obiettivo

Caricare nel datamart gli ordini giornalieri provenienti da e-commerce e POS,
per consentire report interni per data, canale e valuta.

## Campi in uscita

- `order_id`: identificativo assegnato dalla sorgente
- `channel`: `ECOMMERCE` oppure `POS`
- `business_date`: data di competenza dell'ordine
- `amount`: importo dell'ordine
- `currency`: valuta in formato ISO
- `status`: stato funzionale dell'ordine
- `modified_at`: timestamp tecnico usato per il caricamento incrementale

Email e numeri di telefono non sono richiesti nel datamart e non devono essere
copiati nei log.

## Regole di caricamento

- Chiave di deduplicazione: `channel` + `order_id`.
- Caricamento incrementale basato su `modified_at`.
- Le riesecuzioni devono essere idempotenti.
- Gli annullamenti restano nel datamart con il relativo stato; il mapping dei
  codici POS e' in attesa di conferma funzionale.
- I report devono usare `business_date`, non `created_at`.

## Criteri di verifica

- Confrontare conteggi e importi per data, canale e valuta.
- Ogni differenza deve essere tracciabile tramite `batch_id`.
- Il rilascio e' bloccato finche' il mapping degli stati POS non e' validato.