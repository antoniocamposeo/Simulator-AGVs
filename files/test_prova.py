import random
import numpy as np
import plotly.figure_factory as ff

# Parametri
num_machines = 3
num_agv = 2
num_jobs_per_machine = 1

# Dati di esempio (tempi di lavorazione, carico, scarico per ogni macchina)
processing_times = [10, 15, 20]  # Tempi di lavorazione per ogni macchina
load_times = [3, 3, 4]  # Tempo di carico per ogni macchina
unload_times = [2, 2, 3]  # Tempo di scarico per ogni macchina


# Funzione per generare un cromosoma casuale (soluzione iniziale)
def generate_random_schedule(num_machines, num_agv):
    schedule = []
    for i in range(num_machines):
        agv_id = random.randint(0, num_agv - 1)
        schedule.append((agv_id, i))  # (AGV assegnato, macchina)
    return schedule


# Simulazione per calcolare il tempo totale per una sequenza di operazioni
def simulate(schedule, processing_times, load_times, unload_times):
    agv_times = [0] * num_agv
    machine_times = [0] * num_machines
    machine_status = [False] * num_machines  # False: macchina non in uso, True: macchina in uso
    total_schedule = []

    for operation in schedule:
        agv_id, machine_id = operation

        # L'AGV deve attendere che la macchina sia disponibile (non in uso)
        if machine_status[machine_id]:  # Macchina occupata, attendi che sia libera
            load_start = machine_times[machine_id]
        else:
            load_start = max(agv_times[agv_id], machine_times[machine_id])

        load_end = load_start + load_times[machine_id]

        # La macchina ora è occupata, inizia la lavorazione
        machine_status[machine_id] = True
        process_start = load_end
        process_end = process_start + processing_times[machine_id]

        # Dopo che la lavorazione è completata, la macchina può essere scaricata
        unload_start = process_end
        unload_end = unload_start + unload_times[machine_id]

        # Aggiorna i tempi per AGV e macchina
        agv_times[agv_id] = unload_end
        machine_times[machine_id] = unload_end

        # Rendi la macchina disponibile dopo lo scarico
        machine_status[machine_id] = False

        # Salva gli eventi nel Gantt
        total_schedule.append(('Carico', f'AGV{agv_id + 1}', load_start, load_end, machine_id))
        total_schedule.append(('Lavorazione', f'Macchina{machine_id + 1}', process_start, process_end, machine_id))
        total_schedule.append(('Scarico', f'AGV{agv_id + 1}', unload_start, unload_end, machine_id))

    return max(agv_times), total_schedule




# Operatori genetici
def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)


def crossover(parent1, parent2):
    cut_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:cut_point] + parent2[cut_point:]
    child2 = parent2[:cut_point] + parent1[cut_point:]
    return child1, child2


def mutate(individual):
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual


# Funzione di fitness (minimizza il tempo totale)
def fitness(individual, processing_times, load_times, unload_times):
    total_time, _ = simulate(individual, processing_times, load_times, unload_times)
    return -total_time  # Minimizzare il tempo totale


# Algoritmo genetico modificato per normalizzare i pesi
def genetic_algorithm(pop_size, num_generations, processing_times, load_times, unload_times):
    population = [generate_random_schedule(num_machines, num_agv) for _ in range(pop_size)]
    for generation in range(num_generations):
        fitness_scores = [fitness(ind, processing_times, load_times, unload_times) for ind in population]

        # Normalizzare i punteggi di fitness
        min_fitness = min(fitness_scores)
        fitness_scores = [score - min_fitness + 1 for score in fitness_scores]  # Offset per renderli positivi

        new_population = []
        for _ in range(pop_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population

    # Trova la soluzione migliore
    best_individual = min(population, key=lambda ind: fitness(ind, processing_times, load_times, unload_times))
    _, best_schedule = simulate(best_individual, processing_times, load_times, unload_times)
    return best_individual, best_schedule


# Esecuzione dell'algoritmo genetico
best_individual, best_schedule = genetic_algorithm(
    pop_size=50,
    num_generations=100,
    processing_times=processing_times,
    load_times=load_times,
    unload_times=unload_times
)


# Funzione per generare un diagramma di Gantt con Plotly
def plot_gantt(schedule):
    df = []
    colors = {
        "Carico": 'rgb(46, 137, 205)',
        "Lavorazione": 'rgb(114, 44, 121)',
        "Scarico": 'rgb(198, 47, 105)'
    }
    for task, resource, start, finish, machine_id in schedule:
        df.append(dict(Task=resource, Start=start, Finish=finish, Resource=task))

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True)
    fig.show()


# Mostra il Gantt per la soluzione migliore
plot_gantt(best_schedule)