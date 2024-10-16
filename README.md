# Sistema di Ottimizzazione per multi-AGV nel Processo di Carico-Scarico di Macchine per Sagomatura del Poliuretano Espanso Flessibile
## Descrizione del problema

In questo progetto, affrontiamo un problema di ottimizzazione relativo alla gestione degli **AGV** (Automated Guided Vehicles) all'interno di un magazzino. L'obiettivo è minimizzare il **makespan**, ovvero il tempo massimo entro il quale tutti gli AGV completano le loro operazioni e ritornano alla base.

### Componenti del problema

- **N AGV** che si spostano nel magazzino eseguendo compiti di carico, scarico, movimentazione e attesa.
- **M macchinari** che richiedono un numero specifico di lavorazioni.
- **Base di partenza** e **base di stoccaggio** come punti di riferimento per i movimenti degli AGV.
- Ogni AGV deve completare un ciclo di: **Carico -> Lavorazione -> Scarico** per ogni macchinario.

Il problema è formulato come un modello di **Programmazione Lineare Intera Mista (MILP)**.

## Modello MILP

### Variabili di Decisione

1. **\( x_{a,m}(t) \)**: Variabile binaria che indica se l'AGV \( a \) è assegnato al macchinario \( m \) per un task di lavorazione al tempo \( t \).
2. **\( z_{a,m}(t) \)**: Variabile binaria che indica se l'AGV \( a \) sta caricando o scaricando presso il macchinario \( m \) al tempo \( t \).
3. **\( y_{a}(t) \)**: Variabile binaria che indica se l'AGV \( a \) è in attesa al tempo \( t \).
4. **\( t_{makespan} \)**: Variabile continua che rappresenta il tempo massimo entro cui tutte le operazioni sono completate.

### Funzione Obiettivo

Minimizzare il **makespan** \( t_{makespan} \):

\[
\min t_{makespan}
\]

### Vincoli

1. **Sequenza operativa dei task**: Ogni macchinario deve seguire la sequenza **carico -> lavorazione -> scarico**.
2. **Capacità dei macchinari**: Ogni macchinario può essere servito da un solo AGV alla volta:
   \[
   \sum_{a=1}^N x_{a,m}(t) \leq 1 \quad \forall m, t
   \]
3. **Esclusività dei task per ogni AGV**: Ogni AGV può eseguire un solo task alla volta:
   \[
   \sum_{m=1}^M z_{a,m}(t) + y_{a}(t) \leq 1 \quad \forall a, t
   \]
4. **Tempi di movimentazione**: Un AGV può iniziare un task di carico solo dopo aver raggiunto lo stoccaggio e il macchinario:
   \[
   \text{Inizio Task}_{m} \geq \text{Partenza} + T_{mov}(\text{Base}, m)
   \]
5. **Tempi di esecuzione**: Il tempo totale del ciclo operativo (carico, lavorazione, scarico) per ogni macchinario è dato da:
   \[
   T_{load}(m) + T_{process}(m) + T_{unload}(m)
   \]
6. **Ritorno alla base**: Dopo aver completato tutte le lavorazioni, ogni AGV deve ritornare alla base entro il makespan:
   \[
   T_{return}(a) \leq t_{makespan}
   \]
7. **Completamento delle lavorazioni**: Ogni macchinario deve completare il numero assegnato di lavorazioni:
   \[
   \sum_{t=0}^{t_{makespan}} x_{a,m}(t) = W_m \quad \forall m
   \]


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
