# Sistema di Ottimizzazione per multi-AGV nel Processo di Carico-Scarico di Macchine per Sagomatura del Poliuretano Espanso Flessibile

## Descrizione del Progetto

Questo progetto si concentra sullo sviluppo di un sistema automatizzato basato su robot mobili (AGV) in grado di trasportare materiali tra le diverse macchine nel processo produttivo di sagomatura del poliuretano espanso flessibile. L'obiettivo principale è ottimizzare l'assegnazione dei task di carico e scarico per massimizzare l'efficienza operativa e ridurre i tempi di completamento delle lavorazioni.

## Obiettivi

- Sviluppare un sistema di robot mobili (AGV) per il trasporto di blocchi di poliuretano espanso.
- Ottimizzare l'assegnazione dei task per minimizzare il tempo di completamento e massimizzare l'efficienza operativa.
- Creare un sistema di scheduling per la gestione dinamica dei task in tempo reale.

## Componenti Principali

- **AGV**: Robot mobili responsabili del trasporto dei materiali.
- **Macchine**: Entità che eseguono operazioni di carico, lavorazione e scarico.
- **Scheduler**: Componente che gestisce l'assegnazione dei task ad ogni intervallo di tempo, ottimizzando i movimenti degli AGV.
![prova](https://github.com/user-attachments/assets/54627e60-b4f3-46c6-aa27-1ad9bcafb2a6)


## Funzionamento

1. **Raccolta Dati**: Ogni entità (AGV e macchine) raccoglie informazioni sulla propria posizione, stato e task da eseguire a intervalli regolari.
   
2. **Assegnazione dei Task**: Lo Scheduler crea una lista di AGV e macchine disponibili e assegna i task tenendo conto della distanza minima e della sequenza di operazioni (carico, lavorazione, scarico).

3. **Ottimizzazione**: L'algoritmo utilizza un'euristica per migliorare l'assegnazione dei task e ridurre i tempi di inattività.
![prova](https://github.com/user-attachments/assets/b8719c0f-7193-4b93-98f9-8b5cf7840b30)

# Analisi della Velocità Variabile degli AGV

È stata effettuata un'analisi riguardo alla **velocità variabile degli AGV**, che può variare da **1 a 2 m/s**. Sono state studiate le soluzioni al variare della velocità e del numero di AGV, fino a un massimo di **5 unità**. Questa analisi ha permesso di valutare l'impatto della velocità e della quantità di AGV sulla performance complessiva del sistema, identificando i parametri ottimali per migliorare l'efficienza operativa.
![test](https://github.com/user-attachments/assets/6edeec17-b86b-4190-9263-9b062630d51e)
## Installazione

1. Clona questo repository:
   ```bash
   git clone https://github.com/tuo-username/tuo-progetto-agv.git
   cd tuo-progetto-agv
