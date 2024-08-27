import numpy as np
import Machine
import AGV
from Machine import Machine
from AGV import AGV

N = 2
M = 4
tot_time = 100
AGV_l = [AGV(0, 2),
         AGV(1, 2),
         AGV(2, 2),

         ]

Machine_l = [Machine(0, 0, 1, 2, 2, 2, (2, 2)),
             Machine(1, 1, 2, 2, 2, 2, (1, 1)),
             Machine(2, 2, 2, 2, 2, 2, (2, 1)),
             Machine(3, 3, 1, 2, 2, 2, (1, 2)), ]

problem_state = {'AGVs':
    {
        0: {'State': None, 'Task': None, 'Machine': None, 'Position': None},
        1: {'State': None, 'Task': None, 'Machine': None, 'Position': None},
    },

    'Machines':
        {0: {'State': None, 'AGV_load': None, 'AGV_unload': None},
         1: {'State': None, 'AGV_load': None, 'AGV_unload': None},
         }}

for i in range(N):
    problem_state['AGVs'][i]['State'] = AGV_l[i].get_state()
    problem_state['AGVs'][i]['Task'] = AGV_l[i].get_task()
    problem_state['AGVs'][i]['Machine'] = AGV_l[i].get_machine()
    problem_state['AGVs'][i]['Position'] = AGV_l[i].get_position()


# ogni macchina e agv ha variabili che indicano l'inizio e la fine del task. ad ogni instate vanno controllate e
# aggiornate. inoltre va controllato in che stato stanno.

# devo creare una funzione che ad ogni istante di tempo mi faccia un resoconto del problema.
# dopo il recap,mi deve resituire i macchinari liberi per il carico e lo scarico, gli agv liberi
# e deve assegnare i task di carico e scarico in base alla minor tempo di spostamento.

# class that manage the task every second
class Optimizer:
    def __init__(self, N, M, tot_time):
        self.N = N  # numero di agv
        self.M = M  # numero di macchine
        self.AGV_l = AGV_l  # liste o array di agv
        self.Machine_l = Machine_l  # liste o array di agv
        self.t = 0
        self.simulation_time = tot_time
        self.state = {'AGVs':
                          {0: {'State': None, 'Task': None, 'Machine': None, 'Position': None},
                           1: {'State': None, 'Task': None, 'Machine': None, 'Position': None},
                           2: {'State': None, 'Task': None, 'Machine': None, 'Position': None},
                           },
                      'Machines':
                          {0: {'State': None, 'AGV_load': None, 'AGV_unload': None},
                           1: {'State': None, 'AGV_load': None, 'AGV_unload': None},
                           2: {'State': None, 'AGV_load': None, 'AGV_unload': None},
                           3: {'State': None, 'AGV_load': None, 'AGV_unload': None},
                           }}
        self.agv_available = []
        self.machine_load_available = []
        self.machine_unload_available = []
        self.sequence = {0: 0,  # 0 (machine): 1 load 2 unload
                         1: 0,  # 1 (machine): 1 load 2 unload
                         2: 0,
                         3: 0}

    def update_state(self):
        for i in range(self.N):
            agv = self.state['AGVs'][i]
            agv['State'] = self.AGV_l[i].get_state()
            agv['Task'] = self.AGV_l[i].get_task()
            agv['Machine'] = self.AGV_l[i].get_machine()
            agv['Position'] = self.AGV_l[i].get_position()

        for j in range(self.M):
            machine = self.state['Machines'][j]
            machine['State'] = self.Machine_l[j].get_state()
            machine['AGV_load'] = self.Machine_l[j].get_load()
            machine['AGV_unload'] = self.Machine_l[j].get_unload()

    def agvs_available(self):
        """ Funzione Ritorna AGV liberi indicando la loro posizione"""
        agv_temp = self.state['AGVs']
        self.agv_available = []
        for i in range(self.N):
            if agv_temp[i]['State']['Wait'] == 1:
                self.agv_available.append(self.AGV_l[i])
            else:
                if self.AGV_l[i] in self.agv_available:
                    self.agv_available.remove(self.AGV_l[i])

    def machines_available(self):
        """ Ritona Macchine Libere Per Carico o Scarico  indicando la posizione delle macchiane"""
        machine_temp = self.state['Machines']
        self.machine_load_available = []
        self.machine_unload_available = []
        for i in range(self.M):
            if machine_temp[i]['State']['Complete'] == 0 and machine_temp[i]['State']['Load'] == 0 and machine_temp[i][
                'AGV_load'] is None:
                self.machine_load_available.append(self.Machine_l[i])
            if machine_temp[i]['State']['Work'] == 0 and machine_temp[i]['State']['Unload'] == 0 and machine_temp[i][
                'AGV_unload'] is None:
                self.machine_unload_available.append(self.Machine_l[i])
        str_load = ''
        for m in self.machine_load_available:
            str_load = ' ' + str_load + '[' + str(m.id) + ']' + ' '
        str_unload = ''
        for m in self.machine_unload_available:
            str_unload = ' ' + str_unload + '[' + str(m.id) + ']' + ' '
        print('Load:' + str_load + '\n\r' + 'Unload:' + str_unload + '\n')

    def assign_machine_agv(self):
        """
        In base ai macchiari disponibile assegna l'agv piu vicino alla macchina,
        Aggiornando lo stato della macchina e agv richiamando main
        se gli indici sono -1 vuol dire che l'agv deve aspettare
                """
        machine_position_load = {m.id: m.get_position() for m in self.machine_load_available}
        machine_position_unload = {m.id: m.get_position() for m in self.machine_unload_available}
        agv_position = {a.id: [a.get_position(), a.speed] for a in self.agv_available}

        assign_task = {}
        if len(agv_position) >= 1:
            for agv in agv_position:
                while True:
                    if len(machine_position_load) > 0:
                        index_min_time = self.find_best_machine_to_assign(agv_position[agv], machine_position_load)
                        if index_min_time != -1:
                            if self.sequence[index_min_time] < 1:
                                assign_task[agv] = [index_min_time, 'Load']
                                self.sequence[index_min_time] += 1
                                machine_position_load.pop(index_min_time)
                                break
                            elif self.sequence[index_min_time] >= 1:
                                machine_position_load.pop(index_min_time)
                    if len(machine_position_load) <= 0 and len(machine_position_unload)>0:
                        index_min_time = self.find_best_machine_to_assign(agv_position[agv], machine_position_unload)
                        if index_min_time != -1:
                            if self.sequence[index_min_time] == 1:
                                assign_task[agv] = [index_min_time, 'Unload']
                                self.sequence[index_min_time] -= 1
                                machine_position_unload.pop(index_min_time)
                                break
                            elif self.sequence[index_min_time] != 1:
                                machine_position_unload.pop(index_min_time)
                    if len(machine_position_unload) == 0:
                        print('No machine available')
                        break

        return assign_task

    def find_best_machine_to_assign(self, agv, machine_position):
        if len(machine_position) >= 1:
            time = {}
            for m in machine_position:
                time[m] = self.distance_to_time(agv[0], machine_position[m], agv[1])
            return min(time, key=time.get)
        else:
            return -1

    @staticmethod
    def distance_to_time(p1: tuple, p2: tuple, speed):
        distance = np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])  # mannathan distance
        if distance <= 0:
            time = 0
        else:
            time = round(distance / speed)
        return time

    def update_task(self, tasks: dict):
        # x:y x agv y machine
        # {0: [1, 'Load'], 1: [2, 'Load'], 2: [0, 'Load'], 3: [3, 'Load'], 4: [1, 'Unload']}
        if len(tasks) > 0:
            for a in tasks:
                self.AGV_l[a].set_machine(self.Machine_l[tasks[a][0]])  # Assign Machine to AGV
                self.AGV_l[a].set_task(tasks[a][1])

                self.AGV_l[a].set_move_duration(self.distance_to_time(self.AGV_l[a].get_position(),
                                                                      self.AGV_l[a].get_machine().get_position(),
                                                                      self.AGV_l[a].speed))
                self.AGV_l[a].set_time_task(self.t)

                if tasks[a][1] == 'Load':
                    self.Machine_l[tasks[a][0]].set_load(self.AGV_l[a])

                elif tasks[a][1] == 'Unload':
                    self.Machine_l[tasks[a][0]].set_unload(self.AGV_l[a])

    def update_all(self):
        for k in range(N):
            self.AGV_l[k].main(self.t)
        for j in range(M):
            self.Machine_l[j].main(self.t)

    def main(self):
        self.update_state()
        for t in range(1, self.simulation_time):
            self.t = t
            print(t)
            self.agvs_available()
            self.machines_available()
            task = self.assign_machine_agv()
            print(task)
            print(self.sequence)
            self.update_task(task)
            self.update_state()
            print(self.state)
            self.update_all()


opt = Optimizer(N=3, M=4, tot_time=40)
# TODO: Quando tutti i macchinari hanno completato le lavorazioni, gli agv possono tornare alla base di partenza ...
# ... la simulazione termina quando tutti gli agv sono tornati alla base. I realta potremmo aggiungere il tempo ...
# ... di ritorno al termine del completamento di tutte le macchine. L'importante è portare a completamento i macchinari.
# fare test con piu agv
opt.main()
