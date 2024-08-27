import numpy as np


class AGV:
    def __init__(self, id=0, speed=0):
        self.id = id
        self.speed = speed
        self.time_task = None  # set from optimizer # time when start task
        self.task = None  # set from optimizer
        self.move_duration = None  # based set from optimizer # based on position calculate time
        self.machine = None
        self.machine_state = None
        self.state = {'Move': 0,
                      'Load': 0,
                      'Unload': 0,
                      'Wait': 1}  # [Attesa]
        self.actual_time = None  # simulation real time
        self.move_task_time = {'Load': {'start': 0, 'end': 0},
                               'Unload': {'start': 0, 'end': 0}}
        self.position = (
            0, 0)  # initial position

    def update_machine_state(self):
        if self.machine is not None:
            self.machine_state = self.machine.get_state()

    def check_state(self):
        self.update_machine_state()
        if self.machine_state is not None:
            if self.machine_state[self.task] == 1:
                self.state[self.task] = 1
                self.state['Move'] = 1
            else:
                self.state[self.task] = 0
                self.state['Move'] = 0
                self.move_task_time[self.task] = {'start': 0, 'end': 0}
                # self.machine = None

    def check_task(self):
        if self.machine is not None:
            start_task_time = self.time_task
            finish_task_time = 0
            if self.task is not None and self.task == 'Load':
                finish_task_time = start_task_time + self.move_duration + self.machine.load_time

            if self.task is not None and self.task == 'Unload':
                finish_task_time = start_task_time + self.move_duration + self.machine.load_time

            self.move_task_time[self.task]['start'] = self.time_task
            self.move_task_time[self.task]['end'] = self.time_task + self.move_duration

            if start_task_time <= self.actual_time < finish_task_time:
                self.state['Wait'] = 0
            else:
                self.state['Wait'] = 1
                self.set_position(self.machine.position)
                self.machine = None

    def update_time(self, time):
        self.actual_time = time

    def set_machine(self, machine):
        self.machine = machine

    def get_state(self):
        return self.state

    def get_task(self):
        return self.task

    def set_task(self, task: str):
        self.task = task

    def set_move_duration(self, move_duration: int):
        self.move_duration = move_duration

    def get_machine(self):
        return self.machine

    def set_time_task(self, time):
        self.time_task = time

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def main(self, time):
        self.update_time(time)
        self.check_state()
        self.check_task()
