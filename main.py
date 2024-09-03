import numpy as np
import test
import manage_data

import Optimizer
from Optimizer import *

from plotly.subplots import make_subplots


def test_speed(speed_arr, plotting: int):
    speed_f_sim = []
    for s in speed_arr:
        f_sim = np.array([])
        for i in range(1, 20):
            OPT = Optimizer(N=i, M=6, tot_time=10000, speed=s)
            OPT.main()
            print('N_AGVs:' + str(i) + '\t Simulation Time:' + str(OPT.t))
            f_sim = np.append(f_sim, OPT.t)

        speed_f_sim.append(f_sim)
    match plotting:
        case 0:
            test.plotting(speed_f_sim, speed_arr)
        case 1:
            try:
                test.plotting1(speed_f_sim, speed_arr)
            except:
                raise 'Use only 5 speed'
        case 2:
            try:
                test.plotting2(speed_f_sim)
            except:
                raise 'Use only 1 speed'


def Gantt(OPT: Optimizer, plot_agv: int, plot_machine: int):
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

    if plot_agv == 1 and plot_machine == 1:
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
    Gantt(opt, 1, 1)
