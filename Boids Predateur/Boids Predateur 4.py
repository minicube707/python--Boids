import pygame
import math
import numpy as np
import random

pygame.init()

# Crée une fenêtre de 1_550, 860 pixels
WIDTH, HEIGHT = 1_550, 860
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Définit la couleur blanche
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_OCEAN = (0, 200, 255)

# Remplit l'écran avec la couleur blanche
WIN.fill(BLUE_OCEAN)

# Définit le titre de la fenêtre
pygame.display.set_caption("Basic pygame")


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

    tab_norme = np.array([[]])

    def __init__(self,  colour, len, speed_max, max_force, distance_separation) -> None:
        self.orientation = (np.random.rand(2) -0.5 ) * math.pi
        self.position = np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT])
        self.colour = colour
        self.len = len
        self.distance_separation = distance_separation
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) -0.5 ) * 5
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
            if self.position[0] - 3*self.len < 0:
                distance =  np.linalg.norm(np.array([0, self.position[1]] - self.position))
                diff = self.position - np.array([0, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([0, 1])
                near_border = True

            elif self.position[0] + 3*self.len > WIDTH:
                distance =  np.linalg.norm(np.array([WIDTH, self.position[1]] - self.position))
                diff = self.position - np.array([WIDTH, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([0, - 1])
                near_border = True

            if self.position[1] - 3*self.len < 0:
                distance =  np.linalg.norm(np.array([self.position[0], 0] - self.position))
                diff = self.position - np.array([self.position[0], 0])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([-1, 0])
                near_border = True

            elif self.position[1] + 3*self.len > HEIGHT:
                distance =  np.linalg.norm(np.array([self.position[0], HEIGHT] - self.position))
                diff = self.position - np.array([self.position[0], HEIGHT])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                add_speed += vecteur_directeur
                add_speed += np.array([1, 0])
                near_border = True

        
        #Vérifie que les boids ne sorte pas de l'écran
        if self.position[0] < 0:
            self.position = np.array([WIDTH, self.position[1]])

        elif self.position[0] > WIDTH:
            self.position = np.array([0, self.position[1]])

        if self.position[1] < 0:
            self.position = np.array([self.position[0], HEIGHT])
            
        elif self.position[1] > HEIGHT:
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


    def calcul_distance(self, index, list_animoids):

            #Initialisation
            list_norme = np.array([]) 
            
            #Si c'est le premier boid initialisation du tableau des normes communes
            if index == 0:
                Animoid.tab_norme = np.array([])

            #Sinon on recopie les valeurs déjà trouvers
            else:
                list_norme = np.append(list_norme, Animoid.tab_norme[:, index-1])

            #Pour chaque autre boids, calcul des distances        
            for other_boids in list_animoids[index+1:]:

                #Calcul des distances
                norme = np.int32(np.linalg.norm(other_boids.position - self.position))
                list_norme = np.append(list_norme, norme)

            Animoid.tab_norme = np.append(Animoid.tab_norme, list_norme)
            Animoid.tab_norme = Animoid.tab_norme.reshape((index+1, len(list_animoids)-1))

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
    
    def __init__(self, colour, len, speed_max, max_force, speed_max_flew, max_force_flew, distance_separation, distance_alignement, distance_cohesion) -> None:
        super().__init__(colour, len, speed_max, max_force, distance_separation)

        #Flew
        self.speed_max_flew = speed_max_flew
        self.max_force_flew = max_force_flew

        #Disatance
        self.distance_alignement = distance_alignement
        self.distance_cohesion = distance_cohesion

    def comportement(self, index, list_boid,  list_predator, filter):

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
        nb_predator = len(list_predator)
        epsilon = 1e-3
        flew = False
        
        #In cherche à savoir quelle sont les boids les plus proches
        index_nearest_neighbords = np.argsort(Animoid.tab_norme[index + nb_predator, nb_predator:])

        #On se retire de la list list_boid
        list_boid_without_self = list_boid[filter]

        #Pour chaque prédateur
        for sub_index, predator in enumerate(list_predator):

            #Si la norme euclidienne est plus petite que la distance  alors
            distance =  Animoid.tab_norme[index + nb_predator, sub_index]
            if distance < self.distance_cohesion:
                
                #Evite le
                diff = self.position - predator.position
                average_vecteur_3 += diff
                total_preda +=1
                flew = True

        #S'il y a un prédateur
        if flew == True:
            average_vecteur_3 = average_vecteur_3 / total_preda 
            vecteur_directeur_3 = average_vecteur_3 - self.speed
                    
            #Normalisation du vecteur directeur
            vecteur_directeur_3  *= self.max_force_flew
            self.speed += vecteur_directeur_3
        
        #Sinon
        else:
            #Pour tout les autres boids
            for sub_index, boid in enumerate (list_boid_without_self[index_nearest_neighbords[:6]]):
                
                #Si la norme euclidienne est plus petite que la distance alors 
                distance = Animoid.tab_norme[index + nb_predator, index_nearest_neighbords[sub_index] + nb_predator]

                #Séparation
                if distance < self.distance_separation:
                    diff = self.position - boid.position
                    diff = diff / (distance**2 + epsilon)
                    average_vecteur_3 += diff
                    total_separation += 1
                
                #Alignement
                elif distance < self.distance_alignement:
                    average_vecteur_1 += boid.speed
                    total_alignement += 1

                #Cohesion
                elif distance < self.distance_cohesion :
                    center_mass += boid.position
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
            if total_alignement > 0:
            
                """"""""""""""""""""""""""""""""""""""
                #Alignement
                """"""""""""""""""""""""""""""""""""""
                average_vecteur_1 = average_vecteur_1 / total_alignement
    
                #Normalisation du vecteur moyen et multiplication par la vitesse max
                average_vecteur_1 = (average_vecteur_1 / (np.linalg.norm(average_vecteur_1) + epsilon)) * self.speed_max
                vecteur_directeur_1 = average_vecteur_1 - self.speed
            
            
            if total_cohesion > 0:
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
                if np.linalg.norm(vecteur_directeur_2)> self.max_force:
                    vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force
    
            if total_separation > 0:
                """"""""""""""""""""""""""""""""""""""
                #Séparation
                """"""""""""""""""""""""""""""""""""""
                average_vecteur_3 = average_vecteur_3 / total_separation
                vecteur_directeur_3 = average_vecteur_3 - self.speed
                    
                #Normalisation du vecteur directeur
                if np.linalg.norm(vecteur_directeur_3)> self.max_force:
                    vecteur_directeur_3 = (vecteur_directeur_3 /(np.linalg.norm(vecteur_directeur_3) + epsilon)) * self.max_force
            
            self.speed += vecteur_directeur_1  + vecteur_directeur_2 + vecteur_directeur_3

        return flew


class Predator(Animoid):

    def __init__(self,  colour, len, speed_max, max_force, distance_chasse, distance_separation) -> None:
        super().__init__(colour, len, speed_max, max_force, distance_separation)

        self.distance_chasse = distance_chasse

    def chasse(self, index, list_boid, list_predator):
        
        #Initialisation chasse
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction

        #Initialisation
        #Séparation
        vecteur_directeur_3 = np.zeros((2))
        average_vecteur_3 = np.zeros((2)) #Vecteur moyen

        total = 0
        total_preda = 0
        nb_predator = len(list_predator)

        #Pour chaque prédateur
        for sub_index, predator in enumerate(list_predator):

            #Si la norme euclidienne est plus petite que la distance  alors
            distance =  Animoid.tab_norme[index, sub_index]
            if distance < self.distance_separation:
                
                #Séparation
                diff = self.position - predator.position
                average_vecteur_3 += diff
                total_preda +=1

        #S'il y a un prédateurn, on s'éloingne un peu
        if total_preda > 0:
            average_vecteur_3 = average_vecteur_3 / total_preda 
            vecteur_directeur_3 = average_vecteur_3 - self.speed

            #Normalisation du vecteur directeur
            vecteur_directeur_3 = (vecteur_directeur_3 / np.linalg.norm(vecteur_directeur_3)) * self.max_force
            self.speed += vecteur_directeur_3

        #Pour tout les autres boids
        for sub_index, boid in enumerate (list_boid):
            
            #Si la norme euclidienne est plus petite que la distance alors 
            if Animoid.tab_norme[index, sub_index + nb_predator-1] < self.distance_chasse:

                #Chasse
                center_mass += boid.position
                total +=1

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
            if np.linalg.norm(vecteur_directeur_2)> self.max_force:
                vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force

        self.speed += vecteur_directeur_2    

if __name__ == "__main__":

    def main():

        nb_boids = 100
        nb_predators = 4

        #colour, len, speed_max, max_force, speed_max_flew, max_force_flew, distance_separation, distance_alignement, distance_cohesion
        list_boids = np.array([Boids(WHITE, 10, 2, 0.5, 4, 0.5, 20, 40, 70) for _ in range(nb_boids)])

        #colour, len, speed_max, max_force, distance_chasse, distance_separation
        list_predator = np.array([Predator(BLACK, 40, 4, 0.5, 100, 55) for _ in range(nb_predators)])

        list_animoids =  np.array([])
        list_animoids = np.append(list_animoids, list_predator)
        list_animoids = np.append(list_animoids, list_boids)

        border = True
        press1 = True

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
            WIN.fill(BLUE_OCEAN)

            #Activation de la bordure
            key = pygame.key.get_pressed()

            #Border
            if not key[pygame.K_b] and press1 == False:
                press1 = True

            if key[pygame.K_b] and press1 == True:
                border = not border
                press1 = False

            for index, animoid in enumerate(list_animoids):
                
                flew = False

                #Calcul des normes entres les boids
                animoid.calcul_distance(index, list_animoids)

                #Comportement of boids
                #Filtre pour ne pas tomber sur nous même dans la list_boid
                if index >= len(list_predator):

                    index -= nb_predators
                    filter = np.array([], dtype = int)
                    filter = np.append(filter, np.arange(index))
                    filter = np.append(filter, np.arange(index+1, nb_boids))  

                    flew = animoid.comportement(index, list_boids, list_predator, filter)

                #Comportement of predateur
                else:
                    animoid.chasse(index, list_boids, list_predator)
             
                #Update position and draw
                animoid.update_position(border, flew)
                animoid.draw()

            # Rafraîchit l'affichage
            pygame.display.flip()

        # Ferme Pygame
        pygame.quit()

    main()