import numpy as np
import matplotlib.pyplot as plt


class Bug:
    def __init__(self, start_point_x, start_point_y, goal_point_x,
                 goal_point_y, obstacle_x, obstacle_y):
        self.goal_point_x = goal_point_x
        self.goal_point_y = goal_point_y
        self.obstacle_x = obstacle_x
        self.obstacle_y = obstacle_y
        self.road_x = [start_point_x]
        self.road_y = [start_point_y]
        self.out_x = []
        self.out_y = []

        for item_obstacle, jtem_obstacle in zip(obstacle_x, obstacle_y):
            """
                  1
            -1    0    1
                 -1
            """
            for add_direction_x, add_direction_y in zip([-1, -1, -1, 0, 0, 1, 1, 1],
                                                        [-1, 0, 1, -1, 1, -1, 0, 1]):
                poz_x = item_obstacle + add_direction_x
                poz_y = jtem_obstacle + add_direction_y
                ok = True
                for item_obstacle_2, jtem_obstacle_2 in zip(obstacle_x, obstacle_y):
                    if poz_x == item_obstacle_2 and poz_y == jtem_obstacle_2:
                        ok = False
                        break
                if ok:
                    self.out_x.append(poz_x)
                    self.out_y.append(poz_y)

    def simpleMove(self):
        return self.road_x[-1] + np.sign(self.goal_point_x - self.road_x[-1]), \
               self.road_y[-1] + np.sign(self.goal_point_y - self.road_y[-1])

    def moveToNextObstacle(self, visited_x, visited_y):
        for on_axes_move_x, on_axes_move_y in zip([1, 0, -1, 0],
                                                  [0, 1, 0, -1]):
            move_x = self.road_x[-1] + on_axes_move_x
            move_y = self.road_y[-1] + on_axes_move_y

            for x, y in zip(self.out_x, self.out_y):
                pct_ok = True
                if move_x == x and move_y == y:
                    for item, jtem in zip(visited_x, visited_y):
                        if move_x == item and move_y == jtem:
                            pct_ok = False
                            break
                    if pct_ok:
                        return move_x, move_y
                if not pct_ok:
                    break

        return self.road_x[-1], self.road_y[-1]

    def bug0(self):
        move_dir = 'simpleMove'

        move_x, move_y = -np.inf, -np.inf

        plt.plot(self.obstacle_x, self.obstacle_y, ".k")
        plt.plot(self.road_x[-1], self.road_y[-1], "o")
        plt.plot(self.goal_point_x, self.goal_point_y, "x")
        plt.plot(self.out_x, self.out_y, ".")
        plt.grid(True)

        for ob_x, ob_y in zip(self.out_x, self.out_y):
            if self.road_x[-1] == ob_x and self.road_y[-1] == ob_y:
                move_dir = "moveToNextObstacle"
                break

        visited_x = []
        visited_y = []

        while True:
            if self.road_x[-1] == self.goal_point_x and self.road_y[-1] == self.goal_point_y:
                print('I have reached my destination')
                break

            if move_dir == "simpleMove":
                move_x, move_y = self.simpleMove()
            if move_dir == "moveToNextObstacle":
                move_x, move_y = self.moveToNextObstacle(visited_x, visited_y)
            if move_dir == "simpleMove":
                boundary = False
                for ob_x, ob_y in zip(self.out_x, self.out_y):
                    if move_x == ob_x and move_y == ob_y:
                        self.road_x.append(move_x)
                        self.road_y.append(move_y)
                        visited_x[:] = []
                        visited_y[:] = []
                        visited_x.append(move_x)
                        visited_y.append(move_y)
                        move_dir = "moveToNextObstacle"
                        boundary = True
                        break
                if not boundary:
                    self.road_x.append(move_x)
                    self.road_y.append(move_y)
            elif move_dir == "moveToNextObstacle":
                normal_move = True
                for ob_x, ob_y in zip(self.obstacle_x, self.obstacle_y):
                    simpleMoveRet = self.simpleMove()
                    if simpleMoveRet[0] == ob_x and simpleMoveRet[1] == ob_y:
                        normal_move = False
                        break
                if normal_move:
                    move_dir = "simpleMove"
                else:
                    self.road_x.append(move_x)
                    self.road_y.append(move_y)
                    visited_x.append(move_x)
                    visited_y.append(move_y)

            plt.plot(self.road_x, self.road_y, "-r")
            plt.pause(0.001)

        plt.show()


def constructObstacles(limit_obstacle_x, limit_obstacle_y):
    obstacle_x = []
    obstacle_y = []
    for limit_x, limit_y in zip(limit_obstacle_x, limit_obstacle_y):

        for ob_x in range(limit_x[0], limit_x[1]):
            for ob_y in range(limit_y[0], limit_y[1]):
                obstacle_x.append(ob_x)
                obstacle_y.append(ob_y)

    return obstacle_x, obstacle_y


def runCase1():
    start_point_x = 0.0
    start_point_y = 190.0

    goal_point_x = 190
    goal_point_y = 50.0

    limit_obstacle_x = [[10, 40], [40, 70], [70, 100], [130, 170], [130, 150], [130, 180], [70, 120], [0, 60], [0, 20]]
    limit_obstacle_y = [[130, 180], [150, 180], [170, 180], [40, 80], [80, 130], [130, 190], [50, 100], [0, 30], [30, 60]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y


def runCase2():
    start_point_x = 170.0
    start_point_y = 40.0

    goal_point_x = 10
    goal_point_y = 170.0

    limit_obstacle_x = [[100, 140], [140, 190], [30, 70]]
    limit_obstacle_y = [[20, 100], [60, 100], [30, 190]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y


def runCase3():
    start_point_x = 20.0
    start_point_y = 140.0

    goal_point_x = 150.0
    goal_point_y = 120.0

    limit_obstacle_x = [[30, 50], [50, 190], [170, 190], [100, 170], [100, 120]]
    limit_obstacle_y = [[20, 160], [20, 50], [50, 180], [160, 180], [100, 160]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y


if __name__ == "__main__":
    start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y = runCase3()

    obstacle_x, obstacle_y = constructObstacles(limit_obstacle_x, limit_obstacle_y)

    instance = Bug(start_point_x, start_point_y, goal_point_x, goal_point_y, obstacle_x, obstacle_y)
    instance.bug0()
