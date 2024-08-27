import numpy as np
#TODO: bisogna vincolare lo scarico solo quando il work è completato, quindi rendere disponibile il macchinario
# solo alla fine del lavoro, quindi se work : 1 unload : 1


class Machine:
    def __init__(self, id=0, id_work=0, n_works=0, execute_time=0, load_time=0, unload_time=0, position=(0, 0)):
        self.id = id
        self.id_work = id_work
        self.n_works = n_works
        self.execute_time = execute_time
        self.load_time = load_time
        self.unload_time = unload_time
        self.position = position
        self.actual_time = 0
        self.state = {'Load': 0,  # indica carico disponibile:0 , non disponibile:1
                      'Work': 0,  # indica lavoro non sta lavorando: 0, lavorando : 1
                      'Unload': 0, # indica scarico disponibile:0, non disponibile:1
                      'Complete': 0}  # indica completamento , non completo 0, completo :1
        self.work_time = {'start': 0, 'end': 0}  # (start end time)
        self.AGV_load = None
        self.AGV_unload = None

    def get_state_str(self, state: str):
        return self.state[state]

    def get_state(self):
        return self.state

    def update_time(self, time):
        self.actual_time = time

    def check_state(self):
        if self.n_works > 0:
            if self.actual_time == self.work_time['end']:
                self.n_works -= 1

            if self.work_time['start'] <= self.actual_time < self.work_time['end']:
                self.state['Work'] = 1
            else:
                self.state['Work'] = 0
                self.work_time['start'] = 0
                self.work_time['end'] = 0

        elif self.n_works <= 0:
            self.state['Complete'] = 1
            self.AGV_load = None
            self.AGV_unload = None
            print('[M'+str(self.id)+']'+'-- finish')

    def check_overlap(self):
        if self.AGV_load is not None and self.AGV_unload is not None:
            if self.AGV_load.id == self.AGV_unload.id:
                raise f"Error: Same AGV:{self.AGV_unload.id} on the same MACHINE{self.id}"

    def check_load(self):
        if self.AGV_load is not None:
            start_load_time = self.AGV_load.move_task_time['Load']['start']
            finish_load_time = self.AGV_load.move_task_time['Load']['end'] + self.load_time
            if start_load_time <= self.actual_time < finish_load_time:
                self.state['Load'] = 1
            else:
                self.state['Load'] = 0
                self.AGV_load = None

    def check_unload(self):
        if self.AGV_unload is not None:
            start_unload_time = self.AGV_unload.move_task_time['Unload']['start']
            finish_unload_time = self.AGV_unload.move_task_time['Unload']['end'] + self.unload_time
            if start_unload_time <= self.actual_time < finish_unload_time:
                self.state['Unload'] = 1
            else:
                self.state['Unload'] = 0
                self.AGV_unload = None

    def calculate_work_time(self):
        if self.AGV_load is not None:
            self.work_time['start'] = self.AGV_load.move_task_time['Load']['end'] + self.load_time
            self.work_time['end'] = self.work_time['start'] + self.execute_time

    def set_load(self, agv_load):
        self.AGV_load = agv_load

    def get_load(self):
        return self.AGV_load

    def set_unload(self, agv_unload):
        self.AGV_unload = agv_unload

    def get_unload(self):
        return self.AGV_unload

    def get_position(self):
        return self.position

    def main(self, time):
        self.update_time(time)
        self.calculate_work_time()
        self.check_state()
        self.check_load()
        self.check_unload()




