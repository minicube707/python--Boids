import pygame
import math
import numpy as np
import random

import multiprocessing as mp

def Processing1(WIDTH, HEIGHT, list_chuck, border):

    list_animoid_update = []

    #Add the animoid in the eight neighbors cell, plus the cell himself
    for i in range(WIDTH//200):
        for j in range(HEIGHT//100):
            list_update = list_chuck[i + j*WIDTH//100]

            list_neighbors = []
            for dx in [-1, 0, 1]:
                if i + dx >= WIDTH//100 or i + dx < 0:
                    continue

                for dy in [-1, 0, 1]:
                    if j + dy >= HEIGHT//100 or j + dy < 0:
                        continue
                    
                    list_neighbors.extend(list_chuck[i + dx + (j + dy)*WIDTH//100])

            for animoid in list_update:
                flew = False
                list_distance_boid = np.array([])
                list_distance_pred = np.array([])
                list_class_boid = np.array([])
                list_class_pred = np.array([])

                #For all the animoid, calcul the distante betteew us
                for other in list_neighbors:
                            
                    if other is animoid:
                        continue
                            
                    elif isinstance(other, Boids):
                        list_distance_boid = np.append(list_distance_boid, np.linalg.norm(other.position - animoid.position))
                        list_class_boid = np.append(list_class_boid, other)

                    else:
                        list_distance_pred = np.append(list_distance_pred, np.linalg.norm(other.position - animoid.position))
                        list_class_pred = np.append(list_class_pred, other)
        
                #Comportement of boids
                if isinstance(animoid, Boids):
                    flew = animoid.comportement(list_distance_boid, list_distance_pred, list_class_boid, list_class_pred)

                #Comportement of predateur
                else:
                    animoid.chasse(list_distance_boid, list_distance_pred, list_class_boid, list_class_pred)
        
                #Update position and draw
                animoid.update_position(border, flew)
                list_animoid_update.append(animoid)

    return list_animoid_update


def Processing2(WIDTH, HEIGHT, list_chuck, border):

    list_animoid_update = []

    #Add the animoid in the eight neighbors cell, plus the cell himself
    for i in range(WIDTH//200):
        i += WIDTH//200

        for j in range(HEIGHT//100):
            list_update = list_chuck[i + j*WIDTH//100]

            list_neighbors = []
            for dx in [-1, 0, 1]:
                if i + dx >= WIDTH//100 or i + dx < 0:
                    continue

                for dy in [-1, 0, 1]:
                    if j + dy >= HEIGHT//100 or j + dy < 0:
                        continue
                            
                    list_neighbors.extend(list_chuck[i + dx + (j + dy)*WIDTH//100])

            for animoid in list_update:
                flew = False
                list_distance_boid = np.array([])
                list_distance_pred = np.array([])
                list_class_boid = np.array([])
                list_class_pred = np.array([])

                #For all the animoid, calcul the distante betteew us
                for other in list_neighbors:
                            
                    if other is animoid:
                        continue
                            
                    elif isinstance(other, Boids):
                        list_distance_boid = np.append(list_distance_boid, np.linalg.norm(other.position - animoid.position))
                        list_class_boid = np.append(list_class_boid, other)

                    else:
                        list_distance_pred = np.append(list_distance_pred, np.linalg.norm(other.position - animoid.position))
                        list_class_pred = np.append(list_class_pred, other)
        
                #Comportement of boids
                if isinstance(animoid, Boids):
                    flew = animoid.comportement(list_distance_boid, list_distance_pred, list_class_boid, list_class_pred)

                #Comportement of predateur
                else:
                    animoid.chasse(list_distance_boid, list_distance_pred, list_class_boid, list_class_pred)
        
                #Update position and draw
                animoid.update_position(border, flew)
                list_animoid_update.append(animoid)

    return list_animoid_update



""""""""""""""""""""""""""""""""""""""
#Version super optimisé avec le tableau des distances et la révision du code pour augmenter la performance
#Ajout des prédators et révision du code pour plus de réalisme
#Aujout des différentes distances pour la séparation, alignement et cohesion
#Tranformation du tableau commun des distances en tableau commun des normes
#Ajout d'un vecteur pour plus de réalsime lorsque les boids sont proche de la bordure
#Ajout de la règle des 6 voisins
#Ajout de la condition de fuite
#Ajout de la séparation pour les prédateur pour plus de réalisme
""""""""""""""""""""""""""""""""""""""

class Animoid():

    def __init__(self, WIDTH, HEIGHT, colour, len, speed_max, max_force, distance_separation) -> None:
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.orientation = (np.random.rand() - 0.5 ) * math.pi
        self.position = np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT])
        self.colour = colour
        self.len = len
        self.distance_separation = distance_separation
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) - 0.5 ) * 5
        self.speed_max = speed_max 


    def update_position(self, border, flew):
         
        curent_speed = self.speed
        near_border = False
        add_speed = 0
        
        if flew == True:
            speed_max = self.speed_max_flew
        else:
            speed_max = self.speed_max

        #Vérifie que les boids ne sorte pas de l'écran
        if border == True:
            if self.position[0] - 3 * self.len < 0:
                distance =  np.linalg.norm(np.array([0, self.position[1]] - self.position))
                diff = self.position - np.array([0, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([0, 1])
                near_border = True

            elif self.position[0] + 3 * self.len > self.WIDTH:
                distance =  np.linalg.norm(np.array([self.WIDTH, self.position[1]] - self.position))
                diff = self.position - np.array([self.WIDTH, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([0, - 1])
                near_border = True

            if self.position[1] - 3 * self.len < 0:
                distance =  np.linalg.norm(np.array([self.position[0], 0] - self.position))
                diff = self.position - np.array([self.position[0], 0])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([-1, 0])
                near_border = True

            elif self.position[1] + 3 * self.len > self.HEIGHT:
                distance =  np.linalg.norm(np.array([self.position[0], self.HEIGHT] - self.position))
                diff = self.position - np.array([self.position[0], self.HEIGHT])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([1, 0])
                near_border = True

        
        #Vérifie que les boids ne sorte pas de l'écran
        else:
            if self.position[0] < 0:
                self.position = np.array([self.WIDTH, self.position[1]])

            elif self.position[0] > self.WIDTH:
                self.position = np.array([0, self.position[1]])

            if self.position[1] < 0:
                self.position = np.array([self.position[0], self.HEIGHT])

            elif self.position[1] > self.HEIGHT:
                self.position = np.array([self.position[0], 0])
        
        #Ajout des vitesse en fonction de la proximité du bords
        if near_border == False:
            self.speed += curent_speed

        else:
            self.speed += add_speed

       #Limit
        if np.linalg.norm(self.speed) > speed_max:
            self.speed = self.speed / np.linalg.norm(self.speed) * speed_max  
        
        #Orientatin
        self.orientation = np.arctan2(-self.speed[1], self.speed[0]) 

        #Update position
        self.position += self.speed

    def draw(self, WIN):
        
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

        """pygame.draw.circle(WIN, colour, new_head, 2)
        pygame.draw.circle(WIN, colour, new_tail_1, 2)
        pygame.draw.circle(WIN, colour, new_tail_2, 2)"""

        pygame.draw.line(WIN, colour, new_head, new_tail_1, 2)
        pygame.draw.line(WIN, colour, new_head, new_tail_2, 2)
        pygame.draw.line(WIN, colour, position, new_tail_1, 2)
        pygame.draw.line(WIN, colour, position, new_tail_2, 2)
        
        pygame.draw.polygon(WIN, colour, (new_head, new_tail_1, position, new_tail_2))
        #pygame.draw.circle(WIN, BLACK, position, 100, 2)


class Boids(Animoid):
    
    def __init__(self, WIDTH, HEIGHT, colour, len, speed_max, max_force, speed_max_flew, max_force_flew, distance_separation, distance_alignement, distance_cohesion) -> None:
        super().__init__(WIDTH, HEIGHT, colour, len, speed_max, max_force, distance_separation)

        #Flew
        self.speed_max_flew = speed_max_flew
        self.max_force_flew = max_force_flew

        #Disatance
        self.distance_alignement = distance_alignement
        self.distance_cohesion = distance_cohesion

    def comportement(self, list_distance_boid, list_distance_pred, list_class_boid, list_class_pred):
        
        #Initialisation  alignement
        #Alignement
        vecteur_directeur_1 = np.zeros((2))
        average_vecteur_1 = np.zeros((2)) #Vecteur moyen
        total_alignement = 0
        
        #Initialisation cohesion
        #Cohesion
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction
        total_cohesion = 0

        #Initialisation
        #Séparation
        vecteur_directeur_3 = np.zeros((2))
        average_vecteur_3 = np.zeros((2)) #Vecteur moyen
        total_separation = 0
        
        total_preda = 0
        epsilon = 1e-3
        flew = False
        
        #In cherche à savoir quelle sont les boids les plus proches
        index_nearest_neighbords = np.argsort(list_distance_boid)
        list_distance_boid = list_distance_boid[index_nearest_neighbords]
        list_class_boid = list_class_boid[index_nearest_neighbords]

        #Pour chaque prédateur
        for index, distance in enumerate (list_distance_pred):

            #Si la norme euclidienne est plus petite que la distance  alors
            if distance < self.distance_cohesion:
                
                #Evite le
                diff = self.position - list_class_pred[index].position
                average_vecteur_3 += diff
                total_preda += 1
                flew = True

        #S'il y a un prédateur
        if flew == True:
            average_vecteur_3 = average_vecteur_3 / total_preda 
            vecteur_directeur_3 = average_vecteur_3 - self.speed
                    
            #Normalisation du vecteur directeur
            vecteur_directeur_3 *= self.max_force_flew
            self.speed += vecteur_directeur_3
        
        #Sinon
        else:
            #Pour tout les autres boids
            for index, distance in enumerate (list_distance_boid[:6]):
                
                #Si la norme euclidienne est plus petite que la distance alors 
                #Séparation
                if distance < self.distance_separation:
                    diff = self.position - list_class_boid[index].position
                    diff = diff / (distance**2 + epsilon)
                    average_vecteur_3 += diff
                    total_separation += 1
                
                #Alignement
                elif distance < self.distance_alignement:
                    average_vecteur_1 += list_class_boid[index].speed
                    total_alignement += 1

                #Cohesion
                elif distance < self.distance_cohesion :
                    center_mass += list_class_boid[index].position
                    total_cohesion += 1
    
                else:
                    #Random
                    rand = random.randint(1, 50)
                    rand_speed = (np.random.rand()*2) - 1
    
                    if rand == 1:
                        self.speed[0] += rand_speed
    
                    elif rand == 2:
                        self.speed[1] += rand_speed
    
            #S'il y a au moins un voisin alors
            if total_separation > 0:
                """"""""""""""""""""""""""""""""""""""
                #Séparation
                """"""""""""""""""""""""""""""""""""""
                average_vecteur_3 = average_vecteur_3 / total_separation
                vecteur_directeur_3 = average_vecteur_3 - self.speed
                    
                #Normalisation du vecteur directeur
                if np.linalg.norm(vecteur_directeur_3)> self.max_force:
                    vecteur_directeur_3 = (vecteur_directeur_3 /(np.linalg.norm(vecteur_directeur_3) + epsilon)) * self.max_force

            elif total_alignement > 0:
            
                """"""""""""""""""""""""""""""""""""""
                #Alignement
                """"""""""""""""""""""""""""""""""""""
                average_vecteur_1 = average_vecteur_1 / total_alignement
    
                #Normalisation du vecteur moyen et multiplication par la vitesse max
                average_vecteur_1 = (average_vecteur_1 / (np.linalg.norm(average_vecteur_1) + epsilon)) * self.speed_max
                vecteur_directeur_1 = average_vecteur_1 - self.speed
            
            
            elif total_cohesion > 0:
                """"""""""""""""""""""""""""""""""""""
                #Cohesion
                """"""""""""""""""""""""""""""""""""""
                center_mass = center_mass / total_cohesion
                vecteur_to_com = center_mass - self.position
    
                #Normalisation du vecteur de direction
                if np.linalg.norm(vecteur_to_com) > 0:
                    vecteur_to_com = (vecteur_to_com / np.linalg.norm(vecteur_to_com)) * self.max_force
    
                vecteur_directeur_2 = vecteur_to_com - self.speed
                
                #Normalisation du vecteur directeur
                if np.linalg.norm(vecteur_directeur_2) > self.max_force:
                    vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force

            self.speed += vecteur_directeur_1 + vecteur_directeur_2 + vecteur_directeur_3

        return flew

class Predator(Animoid):

    def __init__(self, WIDTH, HEIGHT, colour, len, speed_max, max_force, distance_chasse, distance_separation) -> None:
        super().__init__(WIDTH, HEIGHT, colour, len, speed_max, max_force, distance_separation)

        self.distance_chasse = distance_chasse

    def chasse(self, list_distance_boid, list_distance_pred, list_class_boid, list_class_pred):
        
        #Initialisation chasse
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction

        #Initialisation
        #Séparation
        vecteur_directeur_3 = np.zeros((2))
        average_vecteur_3 = np.zeros((2)) #Vecteur moyen

        total = 0
        total_preda = 0

        #Pour chaque prédateur
        for index, distance in enumerate(list_distance_pred):

            #Si la norme euclidienne est plus petite que la distance  alors
            if distance < self.distance_separation:
                
                #Séparation
                diff = self.position - list_class_pred[index].position
                average_vecteur_3 += diff
                total_preda += 1

        #S'il y a un prédateur, on s'éloingne un peu
        if total_preda > 0:
            average_vecteur_3 = average_vecteur_3 / total_preda 
            vecteur_directeur_3 = average_vecteur_3 - self.speed

            #Normalisation du vecteur directeur
            vecteur_directeur_3 = (vecteur_directeur_3 / np.linalg.norm(vecteur_directeur_3)) * self.max_force
            self.speed += vecteur_directeur_3

        #Pour tout les autres boids
        for index, distance in enumerate (list_distance_boid):
            
            #Si la norme euclidienne est plus petite que la distance alors 
            if distance < self.distance_chasse:

                #Chasse
                center_mass += list_class_boid[index].position
                total += 1

        #Random
        rand = random.randint(1, 50)
        rand_speed = (np.random.rand()*2) - 1

        if rand == 1:
            self.speed[0] += rand_speed

        elif rand == 2:
            self.speed[1] += rand_speed

        #'il y a au moins un voisin alors
        if total > 0:
            
            center_mass = center_mass / total
            vecteur_to_com = center_mass - self.position

            #Normalisation du vecteur de direction
            if np.linalg.norm(vecteur_to_com) > 0:
                vecteur_to_com = (vecteur_to_com / np.linalg.norm(vecteur_to_com)) * self.speed_max

            vecteur_directeur_2 = vecteur_to_com - self.speed
            
            #Normalisation du vecteur directeur
            if np.linalg.norm(vecteur_directeur_2) > self.max_force:
                vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force

        self.speed += vecteur_directeur_2    


def initialisatoin_chuck(WIDTH, HEIGHT, list_animoids):

    list_chuck = []
    for i in range(WIDTH//100):
        for j in range(HEIGHT//100):

            chuck = []
            for animoids in list_animoids:
                    
                #Top Left
                if i == 0 and j == 0:
                    if -100 < animoids.position[0] <= 100 and -100 < animoids.position[1] <= 100:
                        chuck.append(animoids)

                #Top Right
                elif i == (WIDTH//100)-1 and j == 0:
                    if ((WIDTH//100)-1) * 100 < animoids.position[0] <= ((WIDTH//100)+1)*100 and -100 < animoids.position[1] <= 100:
                        chuck.append(animoids)

                #Botom Left
                elif i == 0 and j == (HEIGHT//100)-1:
                    if -100 < animoids.position[0] <= 100 and ((HEIGHT//100)-1)*100 < animoids.position[1] <= ((HEIGHT//100)+1)*100:
                        chuck.append(animoids)

                #Botom Right
                elif i == (WIDTH//100)-1 and j == (HEIGHT//100)-1:
                    if ((WIDTH//100)-1) * 100 < animoids.position[0] <= ((WIDTH//100)+1)*100 and ((HEIGHT//100)-1)*100 < animoids.position[1] <= ((HEIGHT//100)+1)*100:
                        chuck.append(animoids)

                #Left
                elif i == 0:
                    if -100 < animoids.position[0] <= 100 and j * 100 < animoids.position[1] < (j+1) * 100:
                        chuck.append(animoids)

                #Top
                elif j == 0:
                    if i * 100 < animoids.position[0] <= (i+1) * 100 and - 100 < animoids.position[1] <= 100:
                        chuck.append(animoids)
                    
                #Right
                elif i == (WIDTH//100)-1:
                    if ((WIDTH//100)-1) * 100 < animoids.position[0] <= ((WIDTH//100)+1)*100 and j * 100 < animoids.position[1] < (j+1) * 100:
                        chuck.append(animoids)

                #Bottom
                elif j == (HEIGHT//100)-1:
                    if i * 100 < animoids.position[0] <= (i+1) * 100 and ((HEIGHT//100)-1)*100 < animoids.position[1] <= ((HEIGHT//100)+1)*100:
                        chuck.append(animoids)

                #Else              
                elif i * 100 < animoids.position[0] <= (i+1) * 100 and j * 100 < animoids.position[1] <= (j+1) * 100:
                    chuck.append(animoids)

            list_chuck.append(chuck)

    return list_chuck

def calcul_animation(WIDTH, HEIGHT, list_chuck, border):
    # Create copies of the original list for each process
    list_chuck1 = list(list_chuck)
    list_chuck2 = list(list_chuck)

    # Launch async tasks for both processes
    result_1 = Processing1(WIDTH, HEIGHT, list_chuck1, border)
    result_2 = Processing2(WIDTH, HEIGHT, list_chuck2, border)

     
def main():

    pygame.init()

    # Crée une fenêtre de 1_550, 860 pixels
    WIDTH, HEIGHT = 800, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Définit la couleur blanche
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE_OCEAN = (0, 200, 255)
    
    # Remplit l'écran avec la couleur blanche
    WIN.fill(BLUE_OCEAN)
    
    # Définit le titre de la fenêtre
    pygame.display.set_caption("Basic pygame")



    nb_boids = 100
    nb_predators = 4

    #colour, len, speed_max, max_force, speed_max_flew, max_force_flew, distance_separation, distance_alignement, distance_cohesion
    list_boids = np.array([Boids(WIDTH, HEIGHT, WHITE, 10, 2, 0.5, 4, 0.5, 20, 40, 70) for _ in range(nb_boids)])

    #colour, len, speed_max, max_force, distance_chasse, distance_separation
    list_predator = np.array([Predator(WIDTH, HEIGHT, BLACK, 40, 4, 0.5, 100, 55) for _ in range(nb_predators)])

    list_animoids =  np.array([])
    list_animoids = np.append(list_animoids, list_predator)
    list_animoids = np.append(list_animoids, list_boids)


    border = True
    press1 = True

    #Boucle principale
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
        WIN.fill(BLUE_OCEAN)

        #Activation de la bordure
        key = pygame.key.get_pressed()

        #Border
        if not key[pygame.K_b] and press1 == False:
            press1 = True

        if key[pygame.K_b] and press1 == True:
            border = not border
            press1 = False

        #Initilalise the grid
        list_chuck = initialisatoin_chuck(WIDTH, HEIGHT, list_animoids)
        calcul_animation(WIDTH, HEIGHT, list_chuck, border)

        for animoid in list_animoids:
            animoid.draw(WIN)
            
        # Rafraîchit l'affichage
        pygame.display.flip()

    # Ferme Pygame
    pygame.quit()


if __name__ == "__main__":
    mp.freeze_support()
    main()