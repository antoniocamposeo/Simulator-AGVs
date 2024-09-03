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
        self.AGV_l = [AGV(i, speed) for i in range(self.N)]
        self.Machine_l = [Machine(0, 0, 10, 100, 10, 9, (10, 10)),
                          Machine(1, 1, 10, 90, 11, 8, (20, 10)),
                          Machine(2, 2, 10, 80, 12, 7, (10, 20)),
                          Machine(3, 3, 10, 70, 13, 6, (20, 20)),
                          Machine(4, 4, 10, 60, 14, 5, (30, 20)),
                          Machine(5, 5, 10, 50, 15, 4, (20, 30)),
                          ]
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
            if machine_temp[i]['State']['Complete'] == 0 and machine_temp[i]['State']['Load'] == 0 and machine_temp[i][
                'AGV_load'] is None and machine_temp[i]['State']['Work'] == 0:
                self.machine_load_available.append(self.Machine_l[i])
            if machine_temp[i]['State']['Work'] == 0 and machine_temp[i]['State']['Unload'] == 0 and machine_temp[i][
                'AGV_unload'] is None:
                self.machine_unload_available.append(self.Machine_l[i])

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
                    elif len(machine_position_load) <= 0 and len(machine_position_unload) > 0:
                        index_min_time = self.find_best_machine_to_assign(agv_position[agv], machine_position_unload)
                        if index_min_time != -1:
                            if self.sequence[index_min_time] == 1:
                                assign_task[agv] = [index_min_time, 'Unload']
                                self.sequence[index_min_time] -= 1
                                machine_position_unload.pop(index_min_time)
                                break
                            elif self.sequence[index_min_time] != 1:
                                machine_position_unload.pop(index_min_time)
                    elif len(machine_position_unload) == 0:
                        # print('No machine available')
                        break

        return assign_task

    def find_best_machine_to_assign(self, agv, machine_position):
        if len(machine_position) >= 1:
            time = {}
            for m in machine_position:
                time[m] = self.distance_to_time(agv[0], machine_position[m], agv[1])

            # Trova il valore minimo nel dizionario
            valore_minimo = min(time.values())

            # Trova gli indici (le chiavi) che hanno quel valore minimo
            indici_minimo = [chiave for chiave, valore in time.items() if valore == valore_minimo]
            # print(indici_minimo + 'indice scelto' +str(min(time, key=time.get)))
            min_index = 0
            if len(indici_minimo) == 3:
                print(str(indici_minimo) + 'indice scelto' + str(indici_minimo[0]))
                min_index = indici_minimo[1]
            elif len(indici_minimo) == 2:
                min_index = indici_minimo[1]
                print(str(indici_minimo) + 'indice scelto' + str(indici_minimo[0]))
            else:
                min_index = indici_minimo[0]
                print(str(indici_minimo) + 'indice scelto' + str(indici_minimo[0]))

            return min(time, key=time.get)
            # return min_index

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
                break

            # print(t)
            # print(task)
            # print(self.sequence)
            # print(self.state)


opt = Optimizer(N=6, M=6, tot_time=2000, speed=4)
opt.main()
print('N_AGVs:' + str(opt.N) + '\t Simulation Time:' + str(opt.t))


def test_speed(speed_arr,plotting:int):
    speed_f_sim = []
    for s in speed_arr:
        f_sim = np.array([])
        for i in range(1, 20):
            opt = Optimizer(N=i, M=6, tot_time=10000, speed=s)
            opt.main()
            print('N_AGVs:' + str(i) + '\t Simulation Time:' + str(opt.t))
            f_sim = np.append(f_sim, opt.t)

        speed_f_sim.append(f_sim)
    match plotting:
        case 0:
            test.plotting(speed_f_sim, speed_arr)
        case 1:
            try:
                test.plotting1(speed_f_sim,speed_arr)
            except:
                raise 'Use only 5 speed'
        case 2:
            try:
                test.plotting2(speed_f_sim)
            except:
                raise 'Use only 1 speed'



def Gantt(OPT: Optimizer,plot_agv:int,plot_machine:int):
    temp = OPT.get_status()
    # Dividere per ogni AGV e Macchina quello che fanno in un arco temporale
    AGVs = [[] for i in range(OPT.N)]
    Machines = [[] for i in range(OPT.M)]
    for i in range(len(temp)):
        for n in range(OPT.N):
            AGVs[n].append(temp[i]['AGVs'][n])
        for m in range(OPT.M):
            Machines[m].append(temp[i]['Machines'][m])

    figure_agv = manage_data.fig_agv(AGVs, plot_agv)
    figure_machine = manage_data.fig_machine(Machines, plot_machine)

    if plot_agv==1 and plot_machine==1:
        # Creiamo una figura con due sottotrame
        fig_tot = make_subplots(rows=2, cols=1, subplot_titles=['Machine Operations', 'AGV Operations'])

        # Aggiungiamo il primo grafico Gantt alla prima sottotrama
        for trace in figure_machine.data:
            fig_tot.add_trace(trace, row=1, col=1)

        # Aggiungiamo il secondo grafico Gantt alla seconda sottotrama
        for trace in figure_agv.data:
            fig_tot.add_trace(trace, row=2, col=1)

        # Aggiorniamo il layout per migliorare la visualizzazione
        fig_tot.update_layout(
            title_text='Gantt Charts ',
            height=1000,  # Altezza della figura complessiva
            showlegend=True
        )

        # Mostriamo la figura
        fig_tot.show()


if __name__ == '__main__':
    # Single Test
    opt = Optimizer(N=2, M=4, tot_time=5000, speed=2)
    opt.main()
    print('N_AGVs:' + str(opt.N) + '\t Simulation Time:' + str(opt.t))

    # Multi Test - Speed
    # Create a numpy vector with speed
    # speed_arr = np.arange(0.2, 5) / 2
    # test_speed(speed_arr=speed_arr)

    # Gant With Single Simulation
    Gantt(opt,1,1)
