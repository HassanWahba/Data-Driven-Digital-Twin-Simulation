import logging
import numpy as np
from time import sleep
import time


def simulate(logger):
    transporter_1 = Transporter("1", logger)

    track_warehouse_to_cell_1 = AssemblyTrack("1", logger)
    cell_1 = RobotArm("1", logger)

    track_warehouse_to_cell_2 = AssemblyTrack("2", logger)
    cell_2 = RobotArm("2", logger)

    transporter_2 = Transporter("2", logger)

    transporter_1.transport_to_track()

    track_warehouse_to_cell_1.transport_to_cell()
    cell_1.operate()

    track_warehouse_to_cell_2.transport_to_cell()
    cell_2.operate()

    transporter_2.transport_to_track()


class Transporter:
    def __init__(self, id, logger):
        self.id = id
        self.logger = logger.info

    def transport_to_track(self):
        self.logger("transport_to_track_" + self.id + ',start')
        sleep(np.random.poisson() * 5)
        self.logger("transport_to_track_" + self.id + ',end')


class AssemblyTrack:
    def __init__(self, id, logger):
        self.id = id
        self.logger = logger.info

    def transport_to_cell(self):
        self.logger("transport_to_cell_" + self.id + ',start')
        sleep(np.random.poisson() * 5)
        self.logger("transport_to_cell_" + self.id + ',end')
        return True


class RobotArm:
    def __init__(self, id, logger):
        self.id = id
        self.logger = logger.info

    def operate(self):
        self.logger("operation_on_cell_" + self.id + ',start')
        sleep(np.random.poisson() * 5)
        self.logger("operation_on_cell_" + self.id + ',end')
        return True


if __name__ == '__main__':
    logging.basicConfig(filename="event_log.csv",
                        filemode='a',
                        format='%(name)s,%(message)s,%(asctime)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    start = time.time()
    for i in range(100, 101):
        logger = logging.getLogger(str(i))
        simulate(logger)

    print(time.time() - start)
