import plotly.figure_factory as ff
import pandas as pd
from datetime import datetime, timedelta


# import pickle
#
# f = open('store.pckl', 'rb')
# machines = pickle.load(f)
# f.close()
def fig_machine(machines, plot: int):
    machines_new = []
    for i in range(len(machines)):
        name = 'M' + str(i)
        temp = [[], [], []]
        for j in range(len(machines[0])):
            if machines[i][j]['AGV_load'] is not None:
                temp[0].append({'Machine': name, 'AGV': machines[i][j]['AGV_load'].id, 'Task': 'Load'})  # Load
            else:
                temp[0].append({'Machine': name, 'AGV': 'None', 'Task': 'Wait'})

            if machines[i][j]['AGV_unload'] is not None:
                temp[1].append({'Machine': name, 'AGV': machines[i][j]['AGV_unload'].id, 'Task': 'Unload'})  # Unload
            else:
                temp[1].append({'Machine': name, 'AGV': None, 'Task': 'Wait'})

            if machines[i][j]['State']['Work'] == 1:
                temp[2].append({'Machine': name, 'AGV': None, 'Task': 'Work'})  # Unload
            else:
                temp[2].append({'Machine': name, 'AGV': None, 'Task': 'Wait'})
        machines_new.append(temp)
    data = machines_new

    # Funzione per generare una data di partenza
    def generate_date(base_time, task_index):
        return base_time + timedelta(seconds=task_index)

    # Base time per i task
    base_time = datetime(2024, 9, 1, 10, 0, 0)  # Inizio alle 08:00

    # Preparare una lista di dizionari per creare il DataFrame
    tasks = []

    # Definizione delle risorse: una per ogni macchina e task
    resources = ['Load', 'Unload', 'Work']

    # Itera attraverso i dati
    for machine_index, machine_data in enumerate(data):
        machine_name = f"M{machine_index + 1}"  # Identificatore della macchina (M1, M2, ...)

        # Itera attraverso i tre tipi di task: Load, Unload, Process
        for task_type_index, task_type in enumerate(machine_data):
            task_type_name = resources[task_type_index]

            # Iteriamo tra le coppie di task Load-Wait, Unload-Wait, Process-Wait
            for task_index in range(len(task_type)):
                current_task = task_type[task_index]

                # Determina i tempi di inizio e fine per il task
                start_time = generate_date(base_time, task_index)
                end_time = generate_date(base_time, task_index + 1)
                task_desc = f"{current_task['AGV']} -> {machine_name} ({task_type_name})"

                # Aggiungi task per il diagramma di Gantt, specificando l'AGV e il tipo di task
                tasks.append({
                    'Task': f"{machine_name} {task_type_name}",
                    'Start': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Finish': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'Resource': current_task['Task'],  # Il tipo di task (Load, Unload, Process, Wait)
                    'AGV': current_task['AGV'],  # Associa l'AGV se esiste
                    'Description':task_desc
                })

    # Converti la lista di dizionari in un DataFrame
    df = pd.DataFrame(tasks)

    # Mappa dei colori fissi per i task
    colors = {
        'Load': 'rgb(46, 204, 113)',  # Verde
        'Work': 'rgb(52, 152, 219)',  # Blu
        'Unload': 'rgb(231, 76, 60)',  # Rosso
        'Wait': 'rgb(192, 192, 192)'  # Grigio
    }

    # Crea il diagramma di Gantt con plotly.figure_factory
    fig = ff.create_gantt(
        df,
        index_col='Resource',  # Usa la colonna 'Resource' per colorare in base al tipo di task
        show_colorbar=True,
        showgrid_x=True,
        showgrid_y=True,
        title='Gantt Chart of Tasks by Machine',
        group_tasks=True,  # Raggruppa i task per macchina e per tipo
        show_hover_fill=True,
        colors=colors  # Usa la mappa dei colori per i task
    )

    # Mostra il diagramma
    if plot == 1:
        fig.show()
    return fig


def fig_agv(AGVs, plot: int):
    for i in range(len(AGVs[0])):
        for j in range(len(AGVs)):
            AGVs[j][i]['AGV'] = j
            if AGVs[j][i]['Machine'] is not None:
                AGVs[j][i]['Machine'] = 'M' + str(AGVs[j][i]['Machine'].id)
            if AGVs[j][i]['State']['Wait'] == 1:
                AGVs[j][i]['Task'] = 'Wait'

    # Converti i dati in un DataFrame
    df = []
    for i in range(len(AGVs)):
        df.append(pd.DataFrame(AGVs[i]))
    df_agv = pd.concat(df)

    # Definisci il tempo iniziale
    start_time = datetime(2024, 9, 1, 10, 0, 0)

    # Definisci la durata per ogni tipo di task (può essere modificata)
    task_duration_map = {
        'Load': timedelta(minutes=1),
        'Move': timedelta(minutes=1),
        'Unload': timedelta(minutes=1),
        'Wait': timedelta(minutes=1)
    }

    # Crea un dizionario per tenere traccia del tempo corrente di ogni AGV
    agv_time = {agv: start_time for agv in df_agv['AGV'].unique()}

    # Mappa dei colori per i diversi tipi di task
    task_colors = {
        'Load': 'rgb(46, 204, 113)',  # Verde
        'Move': 'rgb(52, 152, 219)',  # Blu
        'Unload': 'rgb(231, 76, 60)',  # Rosso
        'Wait': 'rgb(192, 192, 192)'  # Grigio
    }

    # Lista per i task nel formato che Plotly Gantt può utilizzare
    tasks = []

    # Processa ogni task nel DataFrame
    for idx, row in df_agv.iterrows():
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

    # Crea il Gantt con i colori specifici per i task
    fig = ff.create_gantt(tasks, colors=task_colors, index_col='Resource', show_colorbar=True, group_tasks=True,
                          title='AGV Movement and Tasks')
    if plot == 1:
        fig.show()
    return fig
