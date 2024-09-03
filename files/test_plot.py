import plotly.figure_factory as ff
import pandas as pd

# Dati di esempio
data_load = [
    {'Machine': 'M1', 'AGV': 'AGV1', 'State': {'Load': 1}, 'Task': 'Load'},
    {'Machine': 'M1', 'AGV': 'AGV1', 'State': {'Load': 1}, 'Task': 'Load'},
    {'Machine': 'M1', 'AGV': 'AGV1', 'State': {'Load': 1}, 'Task': 'Load'},
    {'Machine': 'M1', 'AGV': 'AGV1', 'State': {'Load': 1}, 'Task': 'Load'},
    {'Machine': 'M1', 'AGV': 'AGV1', 'State': {'Load': 1}, 'Task': 'Load'}
]

data_unload = [
    {'Machine': 'M1', 'AGV': 'AGV2', 'State': {'Unload': 1}, 'Task': 'Unload'},
    {'Machine': 'M1', 'AGV': 'AGV2', 'State': {'Unload': 1}, 'Task': 'Unload'},
    {'Machine': 'M1', 'AGV': 'AGV2', 'State': {'Unload': 1}, 'Task': 'Unload'},
    {'Machine': 'M1', 'AGV': 'AGV2', 'State': {'Unload': 1}, 'Task': 'Unload'},
    {'Machine': 'M1', 'AGV': 'AGV2', 'State': {'Unload': 1}, 'Task': 'Unload'}
]

data_work = [
    {'Machine': 'M2', 'AGV': None, 'State': {'Work': 1, 'Complete': 0}, 'Task': 'Work'},
    {'Machine': 'M2', 'AGV': None, 'State': {'Work': 1, 'Complete': 0}, 'Task': 'Work'},
    {'Machine': 'M2', 'AGV': None, 'State': {'Work': 1, 'Complete': 0}, 'Task': 'Work'},
    {'Machine': 'M2', 'AGV': None, 'State': {'Work': 1, 'Complete': 0}, 'Task': 'Work'},
    {'Machine': 'M2', 'AGV': None, 'State': {'Work': 1, 'Complete': 0}, 'Task': 'Work'}
]


def create_gantt(data_load, data_unload, data_work):
    """
    Crea un grafico Gantt per visualizzare i task di carico, scarico e lavoro.
    I tempi sono ricavati dalla posizione degli elementi nelle liste.

    Args:
    data_load (list of dict): Dati di carico.
    data_unload (list of dict): Dati di scarico.
    data_work (list of dict): Dati di lavoro.

    Returns:
    plotly.graph_objects.Figure: Grafico Gantt
    """
    # Creiamo una lista per contenere tutti i task
    all_tasks = []

    # Aggiungiamo i dati di carico
    for idx, entry in enumerate(data_load):
        all_tasks.append({
            'Machine': entry['Machine'],
            'AGV': entry['AGV'],
            'Task': entry['Task'],
            'Start': pd.Timestamp('2024-09-02 08:00') + pd.Timedelta(minutes=idx),
            'Finish': pd.Timestamp('2024-09-02 08:00') + pd.Timedelta(minutes=idx + 1)
        })

    # Aggiungiamo i dati di scarico
    for idx, entry in enumerate(data_unload):
        all_tasks.append({
            'Machine': entry['Machine'],
            'AGV': entry['AGV'],
            'Task': entry['Task'],
            'Start': pd.Timestamp('2024-09-02 08:05') + pd.Timedelta(minutes=idx),
            'Finish': pd.Timestamp('2024-09-02 08:05') + pd.Timedelta(minutes=idx + 1)
        })

    # Aggiungiamo i dati di lavoro
    for idx, entry in enumerate(data_work):
        all_tasks.append({
            'Machine': entry['Machine'],
            'AGV': entry['AGV'],
            'Task': entry['Task'],
            'Start': pd.Timestamp('2024-09-02 08:10') + pd.Timedelta(minutes=idx),
            'Finish': pd.Timestamp('2024-09-02 08:10') + pd.Timedelta(minutes=idx + 1)
        })

    # Creiamo il DataFrame dai dati
    df = pd.DataFrame(all_tasks)

    # Verifica i valori unici dei task
    unique_tasks = df['Task'].unique()
    print(f"Unique tasks: {unique_tasks}")

    # Definiamo i colori per i task
    color_map = {
        'Load': 'rgb(46, 204, 113)',  # Verde per Load
        'Unload': 'rgb(231, 76, 60)',  # Rosso per Unload
        'Work': 'rgb(52, 152, 219)'  # Blu per Work
    }

    # Assicuriamoci che tutti i task abbiano un colore definito
    task_colors = {task: color_map.get(task, 'gray') for task in unique_tasks}

    # Creiamo il grafico Gantt
    fig = ff.create_gantt(df, colors=task_colors, index_col='Machine', show_colorbar=True, group_tasks=True,
                          title='Machine Tasks', showgrid_x=True)

    # Aggiorniamo il layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Machine',
        barmode='stack',  # Usa barmode 'stack' per visualizzare le barre come strati sovrapposti
        bargap=0.2,  # Spazio tra le barre
        height=600  # Altezza del grafico
    )

    return fig


# Creiamo il grafico Gantt
fig = create_gantt(data_load, data_unload, data_work)
fig.show()