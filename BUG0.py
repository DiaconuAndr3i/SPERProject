import numpy as np
import matplotlib.pyplot as plt

# Clasa in care mapam atat universul cat si functionalitatea
# in care isi desfasoara activitatea robotul in urma aplicarii algoritmului
class Bug:
    def __init__(self, start_point_x, start_point_y, goal_point_x,
                 goal_point_y, obstacle_x, obstacle_y):
        # initializam punctul de sosire
        self.goal_point_x = goal_point_x
        self.goal_point_y = goal_point_y

        # initializam obstacolele
        self.obstacle_x = obstacle_x
        self.obstacle_y = obstacle_y

        # initializam drumul pe care il va parcurge robotul
        self.road_x = [start_point_x]
        self.road_y = [start_point_y]

        # initializam frontiera obstacolelor
        self.boundaryOfObstacle_x = []
        self.boundaryOfObstacle_y = []


        # stabilim frontiera pentru fiecare obstacol furnizat
        for item_obstacle, jtem_obstacle in zip(obstacle_x, obstacle_y):
            """
                  1
            -1    0    1
                 -1
            """
            for add_direction_x, add_direction_y in zip([-1, -1, -1, 0, 0, 1, 1, 1],
                                                        [-1, 0, 1, -1, 1, -1, 0, 1]):
                poz_x = item_obstacle + add_direction_x # alegem un posibil punct de pe frontiera in raport cu x
                poz_y = jtem_obstacle + add_direction_y # similar pentru y
                ok = True
                for item_obstacle_2, jtem_obstacle_2 in zip(obstacle_x, obstacle_y):
                    if poz_x == item_obstacle_2 and poz_y == jtem_obstacle_2:
                        ok = False
                        break
                if ok:
                    self.boundaryOfObstacle_x.append(poz_x)  # daca punctul chiar se gaseste
                                                            # pe frontiera il adaugam in vectorul corespunzator
                    self.boundaryOfObstacle_y.append(poz_y)


    # Realizam o miscare simpla spre punctul de sosire in conditiile in care nu suntem ingraditi de vreun obstacol
    # de care ne-am putea lovi in imediata apropiere
    def simpleMove(self):
        return self.road_x[-1] + np.sign(self.goal_point_x - self.road_x[-1]), \
               self.road_y[-1] + np.sign(self.goal_point_y - self.road_y[-1])

    # Realizam o miscare pe frontiera obstacolului in punctele inca nevizitate
    # daca este posibila
    def moveToNextObstacle(self, visited_x, visited_y):
        """
        runCase3 - Poate genera probleme de gasire a destinatiei:
            - Pentru cazul de mai jos din for va gasi destinatia fara probleme
            - Pentru urmatorul caz,
                [-1, 0, 1, 0]
                [0, 1, 0, -1],
            de parcurgere a frontierei obstacolului, algoritmul se va bloca ajungand in starea de unde a pornit
            OBS: Limitare a BUG0
        """
        for on_axes_move_x, on_axes_move_y in zip([-1, 0, 1, 0],  # Facem o miscare ori pe orizontala ori pe verticala datorita
                                                                  # naturii obstacolelor
                                                  [0, -1, 0, 1]):
            move_x = self.road_x[-1] + on_axes_move_x
            move_y = self.road_y[-1] + on_axes_move_y

            for x, y in zip(self.boundaryOfObstacle_x, self.boundaryOfObstacle_y):
                pct_ok = True
                if move_x == x and move_y == y:  # Incercam sa gasim un nou punct de pe frontiera nevizitat daca exista
                    for item, jtem in zip(visited_x, visited_y):
                        if move_x == item and move_y == jtem:
                            pct_ok = False
                            break
                    if pct_ok:
                        return move_x, move_y # Returnam punctul nevizitat
                if not pct_ok:
                    break

        return self.road_x[-1], self.road_y[-1] # Daca nu exista punct nevizitat ramanem in punctul curent al robotului

    def bug0(self):
        # Presupunem ca pornim cu o miscare simpla ( Nu avem obstacole in imediata vecinatate a punctului de miscare )
        move_dir = 'simpleMove'

        move_x, move_y = -np.inf, -np.inf

        # Plotam mapa la momentul initial de timp
        plt.plot(self.obstacle_x, self.obstacle_y, ".k")
        plt.plot(self.road_x[-1], self.road_y[-1], "o")
        plt.plot(self.goal_point_x, self.goal_point_y, "x")
        plt.plot(self.boundaryOfObstacle_x, self.boundaryOfObstacle_y, ".")
        plt.grid(True)

        # Daca robotul porneste din vecinatatea unui obstacol ( se afla pe frontiera ) schimbam tipul de deplasare
        for ob_x, ob_y in zip(self.boundaryOfObstacle_x, self.boundaryOfObstacle_y):
            if self.road_x[-1] == ob_x and self.road_y[-1] == ob_y:
                move_dir = "moveToNextObstacle"
                break

        visited_x = []
        visited_y = []

        while True:
            # Daca ajungem la destinatie
            if self.road_x[-1] == self.goal_point_x and self.road_y[-1] == self.goal_point_y:
                print('I have reached my destination')
                break

            if move_dir == "simpleMove":
                # Ne pozitionam in noul punct rezultat dintr-o miscare simpla
                move_x, move_y = self.simpleMove()
            if move_dir == "moveToNextObstacle":
                # Ne pozitionam in noul punct rezultat dintr-o miscare pe frontiera
                move_x, move_y = self.moveToNextObstacle(visited_x, visited_y)
            if move_dir == "simpleMove":
                boundary = False
                # Daca venim dintr-o miscare simpla iar noul punct este pe frontiera semnalam acest lucru
                for ob_x, ob_y in zip(self.boundaryOfObstacle_x, self.boundaryOfObstacle_y):
                    if move_x == ob_x and move_y == ob_y:
                        self.road_x.append(move_x)
                        self.road_y.append(move_y)
                        visited_x[:] = []
                        visited_y[:] = []
                        visited_x.append(move_x)
                        visited_y.append(move_y)
                        # Schimbam tipul de miscare in miscare pe frontiera
                        move_dir = "moveToNextObstacle"
                        boundary = True
                        break
                # Altfel, continuam cu miscarea simpla si stabilim ca punctul este din drumul spre sosire
                if not boundary:
                    self.road_x.append(move_x)
                    self.road_y.append(move_y)
            # Altfel, avem o deplasare pe frontiera
            elif move_dir == "moveToNextObstacle":
                # Incercam o miscare simpla din acel punct (urmam scopul, acela de a ajunge la goal)
                normal_move = True
                for ob_x, ob_y in zip(self.obstacle_x, self.obstacle_y):
                    simpleMoveRet = self.simpleMove()
                    # Daca lovim un punct din obstacol, continuam ocolirea acestuia
                    if simpleMoveRet[0] == ob_x and simpleMoveRet[1] == ob_y:
                        normal_move = False
                        break
                # Daca punctul rezultat din deplasarea printr-o miscare simpla nu intersecteaza un obstacol marcam ca putem
                # face o astfel de miscare
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

# Construim obstacolele prin furnizarea limitelor de intindere
def constructObstacles(limit_obstacle_x, limit_obstacle_y):
    obstacle_x = []
    obstacle_y = []
    for limit_x, limit_y in zip(limit_obstacle_x, limit_obstacle_y):

        for ob_x in range(limit_x[0], limit_x[1]):
            for ob_y in range(limit_y[0], limit_y[1]):
                obstacle_x.append(ob_x)
                obstacle_y.append(ob_y)

    return obstacle_x, obstacle_y

# Configuratie mapa 1
def runCase1():
    start_point_x = 0.0
    start_point_y = 190.0

    goal_point_x = 190
    goal_point_y = 50.0

    limit_obstacle_x = [[10, 40], [40, 70], [70, 100], [130, 170], [130, 150], [130, 180], [70, 120], [0, 60], [0, 20]]
    limit_obstacle_y = [[130, 180], [150, 180], [170, 180], [40, 80], [80, 130], [130, 190], [50, 100], [0, 30], [30, 60]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y

# Configuratie mapa 2
def runCase2():
    start_point_x = 170.0
    start_point_y = 40.0

    goal_point_x = 10
    goal_point_y = 170.0

    limit_obstacle_x = [[100, 140], [140, 190], [30, 70]]
    limit_obstacle_y = [[20, 100], [60, 100], [30, 190]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y

# Configuratie mapa 3
def runCase3():
    start_point_x = 20.0
    start_point_y = 140.0

    goal_point_x = 150.0
    goal_point_y = 120.0

    limit_obstacle_x = [[30, 50], [50, 190], [170, 190], [100, 170], [100, 120]]
    limit_obstacle_y = [[20, 160], [20, 50], [50, 180], [160, 180], [100, 160]]

    return start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y


if __name__ == "__main__":
    start_point_x, start_point_y, goal_point_x, goal_point_y, limit_obstacle_x, limit_obstacle_y = runCase2()

    obstacle_x, obstacle_y = constructObstacles(limit_obstacle_x, limit_obstacle_y)

    instance = Bug(start_point_x, start_point_y, goal_point_x, goal_point_y, obstacle_x, obstacle_y)
    instance.bug0()
