import pygame
import math
import numpy as np
import random

pygame.init()

# Crée une fenêtre de 800x600 pixels
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Définit la couleur blanche
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

# Remplit l'écran avec la couleur blanche
WIN.fill(WHITE)

# Définit le titre de la fenêtre
pygame.display.set_caption("Basic pygame")


class Boids():

    tab_distance_x = np.array([[]])
    tab_distance_y = np.array([[]])

    def __init__(self, orientation, position, colour, len, speed, speed_rotation, distance_cohesion, distance_separation) -> None:
        self.orientation = orientation
        self.position = position
        self.colour = colour
        self.len = len
        self.speed = speed
        self.speed_rotation= speed_rotation
        self.distance_cohension = distance_cohesion
        self.distance_separation = distance_separation

    def get_position(self):
        return self.position
    
    def get_orientation (self):
        return self.orientation
    
    def update(self, index, list_boids):
        
        """"""""""""""""""""""""""""""""""""""
        #Récupératoin des distance
        """"""""""""""""""""""""""""""""""""""
        #Initialisation
        distance_cohesion = self.distance_cohension
        distance_separation = self.distance_separation

        list_distance_x = np.array([])    
        list_distance_y = np.array([])  

        #Vérifie s'il y a plusieur boids
        if len(list_boids) > 1:

            #Si c'est le premier boid initialisation du tableau des distances communes
            if index == 0:
                Boids.tab_distance_x = np.array([])
                Boids.tab_distance_y = np.array([])

            #Sinon on recopie les valeurs déjà trouvers
            else:
                list_distance_x = np.append(list_distance_x, -1 * Boids.tab_distance_x[:, index -1])
                list_distance_y = np.append(list_distance_y, -1 * Boids.tab_distance_y[:, index -1])

            #Pour chaque autre boids, calcul des distances        
            for other_boids in list_boids[index:]:

                #On retire la distance avec nous même
                if self == other_boids:
                    continue

                else:
                    #Calcul des distances
                    distance_x = other_boids.get_position()[0] - self.get_position()[0]
                    distance_y = other_boids.get_position()[1] - self.get_position()[1]
                    list_distance_x = np.append(list_distance_x, distance_x)
                    list_distance_y = np.append(list_distance_y, distance_y)

            #On ajoute les distances au tableau de toutes les distances
            #X
            Boids.tab_distance_x = np.append(Boids.tab_distance_x, list_distance_x)
            Boids.tab_distance_x = Boids.tab_distance_x.reshape((index+1, len(list_boids) -1))

            #Y
            Boids.tab_distance_y = np.append(Boids.tab_distance_y, list_distance_y)
            Boids.tab_distance_y = Boids.tab_distance_y.reshape((index+1, len(list_boids) -1))

            shape = Boids.tab_distance_y.shape

            tab_distance = np.sqrt(Boids.tab_distance_x**2 + Boids.tab_distance_y**2)
            tab_distance = tab_distance.reshape(shape)

            nearest_neighbor_index = np.argmin(tab_distance[index, :])
            nearest_neighbor_distance = np.min(tab_distance)
            nearest_neighbor_distance_x = (Boids.tab_distance_x[index, nearest_neighbor_index])
            nearest_neighbor_distance_y = (Boids.tab_distance_y[index, nearest_neighbor_index])
        

            """"""""""""""""""""""""""""""""""""""
            #Update des états du boids
            """"""""""""""""""""""""""""""""""""""
            #Cohesion
            if nearest_neighbor_distance > distance_cohesion:
                angle_to_nearest_boids = np.arctan2(nearest_neighbor_distance_y, nearest_neighbor_distance_x)

                if angle_to_nearest_boids < 0:
                    self.orientation -= self.speed_rotation * math.pi/180

                else:
                    self.orientation += self.speed_rotation * math.pi/180

            #Séparation 
            elif nearest_neighbor_distance < distance_separation:
                angle_to_nearest_boids = np.arctan2(nearest_neighbor_distance_y, nearest_neighbor_distance_x)

                if angle_to_nearest_boids < 0:
                    self.orientation += self.speed_rotation * math.pi/180

                else:
                    self.orientation -= self.speed_rotation * math.pi/180

            #Alignement
            else:
                nb_neighbor = 0
                all_orienetatoin = 0
                for index_ali, distance_ali in enumerate (tab_distance[index,:]):
                    if (distance_ali < distance_cohesion) and (distance_ali > distance_separation):
                        nb_neighbor += 1

                        if index_ali > index:
                            index_ali += 1

                        all_orienetatoin += list_boids[index_ali].get_orientation()

                if nb_neighbor == 0:
                    nb_neighbor = 1

                if all_orienetatoin / nb_neighbor < self.orientation:
                    self.orientation -= self.speed_rotation * math.pi/180
                
                else:
                    self.orientation += self.speed_rotation * math.pi/180

                  
        """"""""""""""""""""""""""""""""""""""
        #Ajout de l'aléatoire pour le mouvement
        """""""""""""""""""""""""""""""""""""" 
        rand = random.randint(1, 20)
        if rand == 1:
            self.orientation -= self.speed_rotation * math.pi/180

        elif rand == 2:
            self.orientation += self.speed_rotation * math.pi/180

        
        """"""""""""""""""""""""""""""""""""""
        #Update position
        """"""""""""""""""""""""""""""""""""""    
        self.position = self.position + np.array([self.speed * np.cos(-self.orientation), self.speed * np.sin(-self.orientation)])   
        
        #Vérifie que les boids ne sorte pas de l'écran
        if self.position[0] < 0:
            self.position = np.array([WIDTH, self.position[1]])
        
        elif self.position[0] > WIDTH:
            self.position = np.array([0, self.position[1]])

        if self.position[1] < 0:
            self.position = np.array([self.position[0], HEIGHT])
        
        elif self.position[1] > HEIGHT:
            self.position = np.array([self.position[0], 0])
        

    def draw(self):
        
        angle_orientation = self.orientation
        width = self.len
        colour = self.colour
        position = self.position

        #Head
        head_distance = np.array([2*width/3, 0])

        #Tail
        tails_1_distance = np.array([-width/3,  width/3])
        tails_2_distance = np.array([-width/3, -width/3])

        #Orientation 
        matrice_orientation = np.array([[np.cos(angle_orientation), -np.sin(angle_orientation)], 
                                        [np.sin(angle_orientation),  np.cos(angle_orientation)]])
        
        new_head = position + head_distance.dot(matrice_orientation)
        new_tail_1 = position + tails_1_distance.dot(matrice_orientation)
        new_tail_2 = position + tails_2_distance.dot(matrice_orientation)

        pygame.draw.circle(WIN, colour, new_head, 2)
        pygame.draw.circle(WIN, colour, new_tail_1, 2)
        pygame.draw.circle(WIN, colour, new_tail_2, 2)

        pygame.draw.line(WIN, colour, new_head, new_tail_1, 2)
        pygame.draw.line(WIN, colour, new_head, new_tail_2, 2)
        pygame.draw.line(WIN, colour, position, new_tail_1, 2)
        pygame.draw.line(WIN, colour, position, new_tail_2, 2)
        
        #pygame.draw.circle(WIN, BLACK, position, self.distance_separation, 2)  Draw circle to distance of separation
        #pygame.draw.circle(WIN, BLACK, position, self.distance_cohension, 2)   Draw circle to distance of cohension
        

def main():

    boid_1 = Boids(math.pi, np.array([WIDTH//2, HEIGHT//2]),        BLACK, 20, 3, 5, 120, 20)
    boid_2 = Boids(math.pi, np.array([2*WIDTH//3, HEIGHT//2]),      BLACK, 20, 3, 5, 120, 20)
    boid_3 = Boids(math.pi, np.array([WIDTH//3, HEIGHT//2]),        BLACK, 20, 3, 5, 120, 20)
    boid_3 = Boids(math.pi, np.array([WIDTH//2, 2*HEIGHT//3]),      BLACK, 20, 3, 5, 120, 20)
    boid_4 = Boids(math.pi/3, np.array([WIDTH//2, HEIGHT//3]),      BLACK, 20, 3, 5, 120, 20)
    boid_5 = Boids(math.pi/3, np.array([WIDTH//2, 2*HEIGHT//3]),    BLACK, 20, 3, 5, 120, 20)
    boid_6 = Boids(math.pi/2, np.array([WIDTH//2, 2*HEIGHT//3]),    BLACK, 20, 3, 5, 120, 20)
    boid_7 = Boids(math.pi/2, np.array([WIDTH//2, 2*HEIGHT//3]),    BLACK, 20, 3, 5, 120, 20)
    boid_8 = Boids(math.pi/2, np.array([WIDTH//2, 2*HEIGHT//3]),    BLACK, 20, 3, 5, 120, 20)
    boid_9 = Boids(math.pi/2, np.array([WIDTH//2, 2*HEIGHT//3]),    BLACK, 20, 3, 5, 120, 20)


    list_boids =np.array([boid_1, boid_2, boid_3, boid_4, boid_5, boid_6, boid_7, boid_8, boid_9])

    # Boucle principale
    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)
        WIN.fill(WHITE)

        #Update
        for index, boids in enumerate (list_boids):
            boids.update(index, list_boids)

        #Draw
        for boids in list_boids:
            boids.draw()

        # Rafraîchit l'affichage
        pygame.display.flip()

    # Ferme Pygame
    pygame.quit()

main()
