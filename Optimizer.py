import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Machine
import AGV
import test
import manage_data

from plotly.subplots import make_subplots
from Machine import Machine
from AGV import AGV
from copy import deepcopy


# TODO : IMPORTANTE - RINCONTROLLARE ASSEGNAZIONE UNLOAD TASK , DEVONO INZIARE QUANDO LA LAVORAZIONE FINISCE.
#  Quindi bisogna torare un modo che assegni agli agv il tasj di scarico in base alla differneza tra illoro tempo
#  di arrivo alla macchina e il tempo di fine della macchina
# TODO: Aggiungere feature alle sequence, in quanto lo scarico puo iniziare solo se la macchina ha terminato il carico
# TODO : Insert VERBOSE, 1-2-3, based on what we want to print
# TODO : Comment functions,and classes

# TODO: Quando tutti i macchinari hanno completato le lavorazioni, gli agv possono tornare alla base di partenza
#  ... la simulazione termina quando tutti gli agv sono tornati alla base. I realta potremmo aggiungere il tempo
#  ... di ritorno al termine del completamento di tutte le macchine. L'importante è portare a completamento i
#  ... macchinari fare test con piu agv


# class that manage the task every second
class Optimizer:
    def __init__(self, N, M, tot_time, speed):
        self.state_position = []
        self.N = N  # numero di agv
        self.M = M  # numero di macchine
        self.tot_time = tot_time
        self.speed = speed
        self.AGV_l = [AGV(i, self.speed) for i in range(self.N)]

        self.Machine_l = [Machine(0, 0, 30, 100, 20, 20, (0, 5)),
                          Machine(1, 1, 30, 100, 20, 20, (5, 5)),
                          Machine(2, 2, 30, 100, 20,20, (10, 0)),
                          Machine(3, 3, 30, 100, 20, 20, (20, 20)),
                          Machine(4, 4, 30, 100, 20, 20, (30, 20)),
                          Machine(5, 5, 30, 100, 20, 20, (20, 30)),
                          ]
        self.stock = {'position': (10, 10)}
        self.t = 0
        self.simulation_time = tot_time
        self.state = {
            'AGVs': {i: {'State': None, 'Task': None, 'Machine': None, 'Position': None} for i in range(self.N)},
            'Machines': {i: {'State': None, 'AGV_load': None, 'AGV_unload': None} for i in range(self.M)}
        }
        self.agv_available = []
        self.machine_load_available = []
        self.machine_unload_available = []
        self.sequence = {k: 0 for k in range(self.M)}
        self.states = []

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
            if machine_temp[i]['State']['Complete'] == 0 and machine_temp[i]['State']['Load'] == 0 and machine_temp[i]['State']['Work'] == 0:
                self.machine_load_available.append(self.Machine_l[i])
            if machine_temp[i]['State']['Work'] == 1 or machine_temp[i]['State']['Unload'] == 0:
                self.machine_unload_available.append(self.Machine_l[i])
            if machine_temp[i]['State']['Work'] == 0 and machine_temp[i]['State']['Complete'] == 1 :
                self.machine_unload_available.append(self.Machine_l[i])
                # print(self.sequence)

        # str_load = ''
        # for m in self.machine_load_available:
        #     str_load = ' ' + str_load + '[' + str(m.id) + ']' + ' '
        # str_unload = ''
        # for m in self.machine_unload_available:
        #     str_unload = ' ' + str_unload + '[' + str(m.id) + ']' + ' '
        # print('Load:' + str_load + '\n\r' + 'Unload:' + str_unload + '\n')

    def assign_machine_agv(self):
        """
        In base ai macchiari disponibile assegna l'agv piu vicino alla macchina,
        Aggiornando lo stato della macchina e agv richiamando main
        se gli indici sono -1 vuol dire che l'agv deve aspettare
                """
        machine_position_load = {m.id: m.get_position() for m in self.machine_load_available}
        machine_position_unload = {m.id: m.get_position() for m in self.machine_unload_available}
        agv_position = {a.id: [a.get_position(), a.speed] for a in self.agv_available}
        # print(agv_position)
        index_min_time = 0
        assign_task = {}
        if len(agv_position) >= 1:
            for agv in agv_position:
                while True:
                    # print('T')
                    if len(machine_position_load) > 0:
                        task = 'Load'
                        index_min_time, index_array = self.find_best_machine_to_assign(agv_position[agv],
                                                                                       machine_position_load, task)
                        if index_min_time != -1:
                            if self.sequence[index_min_time] < 1:
                                assign_task[agv] = [index_min_time, 'Load']
                                self.sequence[index_min_time] += 1
                                # self.check_sequence()
                                machine_position_load.pop(index_min_time)
                                # if index_array is not None:
                                    # print('LOAD TASK INDEXS :' + str(index_array))
                                    # print('INDEX:' + str(index_min_time))
                                break
                            elif self.sequence[index_min_time] >= 1:
                                machine_position_load.pop(index_min_time)
                    elif len(machine_position_load) <= 0 and len(machine_position_unload) > 0:
                        task = 'Unload'
                        index_min_time, index_array = self.find_best_machine_to_assign(agv_position[agv],
                                                                                       machine_position_unload,
                                                                                       task)

                        if index_min_time != -1:
                            if self.sequence[index_min_time] == 1:
                                assign_task[agv] = [index_min_time, 'Unload']
                                self.sequence[index_min_time] -= 1
                                machine_position_unload.pop(index_min_time)
                                # if index_array is not None:
                                    # print('UNLOAD TASK INDEXS :' + str(index_array))
                                    # print('INDEX:' + str(index_min_time))
                                break
                            elif self.sequence[index_min_time] != 1:
                                machine_position_unload.pop(index_min_time)
                    elif len(machine_position_unload) == 0:
                        # print('No machine available')
                        break
                    if len(machine_position_unload) > 0 and index_min_time == -1:
                        break

        return assign_task

    def check_sequence(self):
        for key, value in self.sequence.items():
            # if self.Machine_l[key].finish_load_time is not None:
            print('------------------')
            print(f'Time:{self.t} - Sequence value:{value}')
            print(f'Machine:{key} - FinishLoad:{self.Machine_l[key].finish_load_time}')
            # if value == 1 and self.Machine_l[key].finish_load_time >= self.t:
            #     print(2)
            # self.sequence[key] = 2

    def find_best_machine_to_assign(self, agv, machine_position, task):
        if len(machine_position) >= 1:
            time = {}
            if task == 'Load':
                for m in machine_position:
                    time[m] = (self.distance_to_time(agv[0], self.stock['position']) + self.Machine_l[m].load_time +
                               self.distance_to_time(self.stock['position'], machine_position[m]))
            elif task == 'Unload':
                for m in machine_position:
                    if self.Machine_l[m].work_time['end'] is not None:
                        if ((self.t + self.distance_to_time(agv[0], machine_position[m]) + self.Machine_l[
                            m].unload_time) >
                                (self.Machine_l[m].work_time['end'])):
                            time[m] = (self.distance_to_time(agv[0], machine_position[m]) + self.Machine_l[
                                m].unload_time + self.distance_to_time(machine_position[m], self.stock['position']))

                # print(time)
                # valore_minimo = min(time.values())
                # indexs_min = [chiave for chiave, valore in time.items() if valore == valore_minimo]
            # return min(time, key=time.get),indexs_min
            if len(time) == 0:
                return -1, None
            else:
                valore_minimo = min(time.values())
                indexs_min = [chiave for chiave, valore in time.items() if valore == valore_minimo]

                return min(time, key=time.get), indexs_min

        else:
            return -1, None

    def distance_to_time(self, p1: tuple, p2: tuple):
        distance = np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])  # mannathan distance
        # distance = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        if distance <= 0:
            time = 0
        else:
            time = round(distance / self.speed)
        return time

    def update_task(self, tasks: dict):
        # x:y x agv y machine
        # {0: [1, 'Load'], 1: [2, 'Load'], 2: [0, 'Load'], 3: [3, 'Load'], 4: [1, 'Unload']}
        if len(tasks) > 0:
            for a in tasks:
                self.AGV_l[a].set_machine(self.Machine_l[tasks[a][0]])  # Assign Machine to AGV
                self.AGV_l[a].set_task(tasks[a][1])

                # self.AGV_l[a].set_move_duration(self.distance_to_time(self.AGV_l[a].get_position(),
                #                                                       self.AGV_l[a].get_machine().get_position()))
                # self.AGV_l[a].set_time_task(self.t)

                if tasks[a][1] == 'Load':
                    self.AGV_l[a].set_move_duration((self.distance_to_time(self.AGV_l[a].get_position(),
                                                                           self.stock['position']) +
                                                     self.distance_to_time(self.stock['position'],
                                                                           self.AGV_l[a].get_machine().get_position())))
                    self.AGV_l[a].set_time_task(self.t)
                    self.Machine_l[tasks[a][0]].set_load(self.AGV_l[a])
                elif tasks[a][1] == 'Unload':
                    self.AGV_l[a].set_move_duration(self.distance_to_time(self.AGV_l[a].get_position(),
                                                                          self.AGV_l[a].get_machine().get_position()) +
                                                    self.distance_to_time(self.AGV_l[a].get_machine().get_position(),
                                                                          self.stock['position']))
                    self.AGV_l[a].set_time_task(self.t)
                    self.Machine_l[tasks[a][0]].set_unload(self.AGV_l[a])

    def update_all(self):
        for k in range(self.N):
            self.AGV_l[k].main(self.t)
        for j in range(self.M):
            self.Machine_l[j].main(self.t)

    def print_position_agvs(self):
        string = 'Position AGVs:\n'
        for i in range(self.N):
            string += 'AGV' + str(i) + ':' + str(self.state['AGVs'][i]['Position']) + '\r\n'
        print(string)

    def check_status_sim(self):
        machine_complete = 0
        for i in range(self.M):
            if self.state['Machines'][i]['State']['Complete'] == 1:
                machine_complete += 1
        if machine_complete >= self.M:
            return 1

    def set_status(self):
        temp = []
        for i in range(self.N):
            temp.append(self.state['AGVs'][i]['Position'])
        self.state_position.append(temp)
        self.states.append(deepcopy(self.state))

    def get_status(self):
        return self.states

    def main(self):
        self.update_all()
        self.update_state()
        self.set_status()
        for t in range(1, self.simulation_time):
            status = self.check_status_sim()

            self.t = t
            self.agvs_available()
            self.machines_available()
            task = self.assign_machine_agv()
            self.update_task(task)
            self.update_all()
            self.update_state()
            self.set_status()
            # self.print_position_agvs()
            if status is not None and status >= 1:
                # print('Simulation Terminated, Time:' + str(self.t))
                # self.print_position_agvs()
                print(self.state)
                break

            # print(t)
            # print(task)
            # print(self.sequence)

