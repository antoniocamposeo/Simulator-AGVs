import plotly.figure_factory as ff
import pandas as pd
from datetime import datetime, timedelta

# Creiamo un DataFrame Pandas con i dati delle macchine
machine_data = pd.DataFrame([
    {'Machine': 'M1', 'Task': 'Load', 'AGV': 'AGV1', 'Start': datetime(2024, 9, 2, 10, 0, 0),
     'Finish': datetime(2024, 9, 2, 10, 5, 0)},
    {'Machine': 'M1', 'Task': 'Unload', 'AGV': 'AGV2', 'Start': datetime(2024, 9, 2, 10, 3, 0),
     'Finish': datetime(2024, 9, 2, 10, 8, 0)},
    {'Machine': 'M1', 'Task': 'Work', 'AGV': 'AGV2', 'Start': datetime(2024, 9, 2, 10, 3, 0),
     'Finish': datetime(2024, 9, 2, 10, 8, 0)},
    {'Machine': 'M2', 'Task': 'Load', 'AGV': 'AGV1', 'Start': datetime(2024, 9, 2, 10, 10, 0),
     'Finish': datetime(2024, 9, 2, 10, 15, 0)},
])
# Creiamo un DataFrame Pandas con i dati degli AGV
data = pd.DataFrame([
    {'AGV': 'AGV1', 'Machine': 'M1', 'Position': (0, 0), 'State': {'Load': 1, 'Move': 1, 'Unload': 0, 'Wait': 0},
     'Task': 'Load'},
    {'AGV': 'AGV1', 'Machine': 'M2', 'Position': (1, 0), 'State': {'Load': 0, 'Move': 1, 'Unload': 1, 'Wait': 0},
     'Task': 'Move'},
    {'AGV': 'AGV1', 'Machine': 'M1', 'Position': (0, 0), 'State': {'Load': 1, 'Move': 1, 'Unload': 0, 'Wait': 0},
     'Task': 'Unload'},
    {'AGV': 'AGV2', 'Machine': 'M1', 'Position': (0, 1), 'State': {'Load': 1, 'Move': 0, 'Unload': 0, 'Wait': 1},
     'Task': 'Wait'},
    {'AGV': 'AGV2', 'Machine': 'M2', 'Position': (1, 1), 'State': {'Load': 0, 'Move': 0, 'Unload': 1, 'Wait': 0},
     'Task': 'Move'},
    {'AGV': 'AGV2', 'Machine': 'M1', 'Position': (0, 1), 'State': {'Load': 0, 'Move': 1, 'Unload': 0, 'Wait': 1},
     'Task': 'Unload'},
])

# Definisci il tempo iniziale
start_time = datetime(2024, 9, 2, 10, 0, 0)

# Definisci la durata per ogni tipo di task (può essere modificata)
task_duration_map = {
    'Load': timedelta(minutes=4),
    'Move': timedelta(minutes=4),
    'Unload': timedelta(minutes=2),
    'Wait': timedelta(minutes=1),
    'Work': timedelta(minutes=100),
}

# Crea un dizionario per tenere traccia del tempo corrente di ogni AGV
agv_time = {agv: start_time for agv in data['AGV'].unique()}

# Mappa dei colori per i diversi tipi di task
task_colors = {
    'Load': 'rgb(46, 204, 113)',  # Verde
    'Move': 'rgb(52, 152, 219)',  # Blu
    'Unload': 'rgb(231, 76, 60)',  # Rosso
    'Wait': 'rgb(241, 196, 15)',  # Giallo
    'Work': 'rgb(241, 230, 15)'}

# Lista per i task nel formato che Plotly Gantt può utilizzare (Macchine)
machine_tasks = []

# Processa i task nel DataFrame delle macchine
for idx, row in machine_data.iterrows():
    machine = row['Machine']
    task = row['Task']

    # Descrizione del task della macchina
    task_desc = f"{machine} ({task} by {row['AGV']})"

    # Aggiungi il task alla lista delle macchine
    machine_tasks.append(dict(Task=f"{task} ({machine})",  # Usa task e macchina come combinazione
                              Start=row['Start'],
                              Finish=row['Finish'],
                              Resource=f"{task} ({machine})",  # Usa task e macchina per colori
                              Description=task_desc))

# Trova tutti i task unici
unique_tasks = machine_data['Task'].unique()
unique_machines = machine_data['Machine'].unique()

# Crea una mappa dei colori che copre tutte le combinazioni task-macchina
combined_colors = {}
for task in unique_tasks:
    for machine in unique_machines:
        combined_colors[f"{task} ({machine})"] = task_colors.get(task,
                                                                 'grey')  # Imposta colore di default per task non trovato

# Crea il Gantt per le macchine
fig_machines = ff.create_gantt(machine_tasks, colors=combined_colors, index_col='Resource', show_colorbar=True,
                               group_tasks=True, title='Machine Operations')

# Lista per i task nel formato che Plotly Gantt può utilizzare
tasks = []

# Processa ogni task nel DataFrame
for idx, row in data.iterrows():
    agv = row['AGV']
    task = row['Task']
    machine = row['Machine']

    # Calcola il tempo di inizio e fine per l'AGV specifico
    start = agv_time[agv]
    end = start + task_duration_map[task]

    # Aggiorna il tempo corrente per l'AGV
    agv_time[agv] = end

    # Descrizione del task (AGV -> Macchina)
    task_desc = f"{agv} -> {machine} ({task})"

    # Aggiungi il task alla lista
    tasks.append(dict(Task=agv,
                      Start=start,
                      Finish=end,
                      Resource=task,  # Usa solo il task per i colori
                      Description=task_desc))  # Descrizione completa


# Aggiungi annotazioni per il Gantt delle macchine
for task in machine_tasks:
    fig_machines.add_annotation(
        x=task['Start'] + (task['Finish'] - task['Start']) / 2,
        y=task['Resource'],  # Usa Resource per posizionare verticalmente
        text=task['Description'],
        showarrow=False,
        font=dict(size=10, color='black'),
        bgcolor='rgba(255, 255, 255, 0.7)'
    )

# Configura il layout per migliorare la visualizzazione delle sovrapposizioni
fig_machines.update_layout(
    xaxis_title='Time',
    yaxis_title='Machine',
    barmode='stack',  # Usato per visualizzare le barre come strati sovrapposti
    bargap=0.2,  # Spazio tra le barre
    height=600  # Altezza del grafico
)

# Crea il Gantt con i colori specifici per i task
fig = ff.create_gantt(tasks, colors=task_colors, index_col='Resource', show_colorbar=True, group_tasks=True,
                      title='AGV Movement and Tasks')

# Aggiungi annotazioni per descrizione completa (AGV -> Machine -> Task)
for task in tasks:
    fig.add_annotation(
        x=task['Start'] + (task['Finish'] - task['Start']) / 2,
        y=task['Task'],
        text=task['Description'],
        showarrow=False,
        font=dict(size=10)
    )


from plotly.subplots import make_subplots

# Creiamo una figura con due sottotrame
fig_tot = make_subplots(rows=2, cols=1, subplot_titles=['Machine Operations', 'Machine Activities'])

# Aggiungiamo il primo grafico Gantt alla prima sottotrama
for trace in fig_machines.data:
    fig_tot.add_trace(trace, row=1, col=1)

# Aggiungiamo il secondo grafico Gantt alla seconda sottotrama
for trace in fig.data:
    fig_tot.add_trace(trace, row=2, col=1)

# Aggiorniamo il layout per migliorare la visualizzazione
fig_tot.update_layout(
    title_text='Gantt Charts for Machines',
    height=800,  # Altezza della figura complessiva
    showlegend=True
)

# Mostriamo la figura
fig_tot.show()