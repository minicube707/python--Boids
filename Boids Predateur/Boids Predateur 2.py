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
BLUE_OCEAN = (0, 50, 200)

# Remplit l'écran avec la couleur blanche
WIN.fill(BLUE_OCEAN)

# Définit le titre de la fenêtre
pygame.display.set_caption("Basic pygame")


""""""""""""""""""""""""""""""""""""""
#Version super optimisé avec le tableau des distances et la révision du code pour augmenter la performance
#Ajout des prédators et révision du code pour plus de réalisme
""""""""""""""""""""""""""""""""""""""

class Animoid():

    tab_norme = np.array([[]])

    def __init__(self,  colour, len, speed_max,  perception, max_force) -> None:
        self.orientation = (np.random.rand(2) -0.5 ) * math.pi
        self.position = np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT])
        self.colour = colour
        self.len = len
        self.perception = perception
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) -0.5 ) * 5
        self.speed_max = speed_max 

    def update_position(self, border):
         
        self.position += self.speed

        #Limit
        if np.linalg.norm(self.speed) > self.speed_max:
            self.speed = self.speed / np.linalg.norm(self.speed) * self.speed_max

        self.orientation = np.arctan2(-self.speed[1], self.speed[0]) 
        
        #Vérifie que les boids ne sorte pas de l'écran
        if border == True:
            if self.position[0] - 2*self.len < 0:
                distance =  np.linalg.norm(np.array([0, self.position[1]] - self.position))
                diff = self.position - np.array([0, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                self.speed += vecteur_directeur

            elif self.position[0] + 2*self.len > WIDTH:
                distance =  np.linalg.norm(np.array([WIDTH, self.position[1]] - self.position))
                diff = self.position - np.array([WIDTH, self.position[1]])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                self.speed += vecteur_directeur

            if self.position[1] - 2*self.len < 0:
                distance =  np.linalg.norm(np.array([self.position[0], 0] - self.position))
                diff = self.position - np.array([self.position[0], 0])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                self.speed += vecteur_directeur

            elif self.position[1] + 2*self.len > HEIGHT:
                distance =  np.linalg.norm(np.array([self.position[0], HEIGHT] - self.position))
                diff = self.position - np.array([self.position[0], HEIGHT])
                diff = diff / distance
                vecteur_directeur = diff - self.speed
                self.speed += vecteur_directeur

        
        #Vérifie que les boids ne sorte pas de l'écran
        if self.position[0] < 0:
            self.position = np.array([WIDTH, self.position[1]])

        elif self.position[0] > WIDTH:
            self.position = np.array([0, self.position[1]])

        if self.position[1] < 0:
            self.position = np.array([self.position[0], HEIGHT])
            
        elif self.position[1] > HEIGHT:
            self.position = np.array([self.position[0], 0])


    def calcul_distance(self, index, list_animoids):

            """"""""""""""""""""""""""""""""""""""
            #Récupératoin des distance
            """"""""""""""""""""""""""""""""""""""
            #Initialisation
            list_norme = np.array([]) 
            
            #Si c'est le premier boid initialisation du tableau des distances communes
            if index == 0:
                Animoid.tab_norme = np.array([])

            #Sinon on recopie les valeurs déjà trouvers
            else:
                list_norme = np.append(list_norme, -1*Animoid.tab_norme[:, index-1])

            #Pour chaque autre boids, calcul des distances        
            for other_boids in list_animoids[index+1:]:

                #Calcul des distances
                norme = other_boids.position - self.position
                list_norme = np.append(list_norme, norme)

            Animoid.tab_norme = np.append(Animoid.tab_norme, list_norme)
            Animoid.tab_norme = Animoid.tab_norme.reshape((index+1, len(list_animoids)-1 , 2))

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
        
        pygame.draw.polygon(WIN, colour, (new_head, new_tail_1, position, new_tail_2))
        
        #pygame.draw.circle(WIN, BLACK, position, self.perception, 2)


class Boids(Animoid):

    
    def comportement(self, index, list_boid,  list_predator, filter):

        #Initialisation  alignement
        vecteur_directeur_1 = np.zeros((2))
        average_vecteur_1 = np.zeros((2)) #Vecteur moyen
        
        #Initialisation cohesion
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction

        #Initialisation
        vecteur_directeur_3 = np.zeros((2))
        average_vecteur_3 = np.zeros((2)) #Vecteur moyen
        
        total_preda = 0
        total_boid = 0
        nb_predator = len(list_predator)
        flew = False

        epsilon = 1e-3
        
        for sub_index, predator in enumerate(list_predator):

            #Si la norme euclidienne est plus petite que la distance de percepetion alors
            distance =  np.linalg.norm(Animoid.tab_norme[index + nb_predator, sub_index, :])
            if distance < self.perception:
                
                #Séparation
                diff = self.position - predator.position
                average_vecteur_3 += diff
                total_preda +=1
                flew = True
            
        if flew == True:
            average_vecteur_3 = average_vecteur_3 / total_preda 
            vecteur_directeur_3 = average_vecteur_3 - self.speed
                    
            #Normalisation du vecteur directeur
            vecteur_directeur_3 = (vecteur_directeur_3 / np.linalg.norm(vecteur_directeur_3)) * self.max_force
            self.speed += vecteur_directeur_3
        

        #Pour tout les autres boids
        for sub_index, boid in enumerate (list_boid[filter]):
            
            #Si la norme euclidienne est plus petite que la distance de percepetion alors 
            distance =  np.linalg.norm(Animoid.tab_norme[index + nb_predator, sub_index  + nb_predator, :])
            if distance < self.perception:
            
                total_boid += 1

                #Séparation
                diff = self.position - boid.position
                average_vecteur_3 += diff
                
                #Random
                rand = random.randint(1, 50)
                rand_speed = (np.random.rand()*2) - 1

                if rand == 1:
                    self.speed[0] += rand_speed

                elif rand == 2:
                    self.speed[1] += rand_speed

                if flew == False:

                    #Alignement
                    average_vecteur_1 += boid.speed
                
                    #Cohesion
                    center_mass += boid.position
    
                    

    
        #'il y a au moins un voisin alors
        if total_boid > 0:
        
            """"""""""""""""""""""""""""""""""""""
            #Séparation
            """"""""""""""""""""""""""""""""""""""
            average_vecteur_3 = average_vecteur_3 / total_boid
            vecteur_directeur_3 = average_vecteur_3 - self.speed
                
            #Normalisation du vecteur directeur
            if np.linalg.norm(vecteur_directeur_3)> self.max_force:
                vecteur_directeur_3 = (vecteur_directeur_3 / np.linalg.norm(vecteur_directeur_3)) * self.max_force

            if flew == False:

                """"""""""""""""""""""""""""""""""""""
                #Alignement
                """"""""""""""""""""""""""""""""""""""
                average_vecteur_1 = average_vecteur_1 / total_boid

                #Normalisation du vecteur moyen et multiplication par la vitesse max
                average_vecteur_1 = (average_vecteur_1 / (np.linalg.norm(average_vecteur_1) + epsilon)) * self.speed_max
                vecteur_directeur_1 = average_vecteur_1 - self.speed


                """"""""""""""""""""""""""""""""""""""
                #Cohesion
                """"""""""""""""""""""""""""""""""""""
                center_mass = center_mass / total_boid
                vecteur_to_com = center_mass - self.position

                #Normalisation du vecteur de direction
                if np.linalg.norm(vecteur_to_com) > 0:
                    vecteur_to_com = (vecteur_to_com / np.linalg.norm(vecteur_to_com)) * self.speed_max
                vecteur_directeur_2 = vecteur_to_com - self.speed

                #Normalisation du vecteur directeur
                if np.linalg.norm(vecteur_directeur_2)> self.max_force:
                    vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force

        self.speed += vecteur_directeur_1  + vecteur_directeur_2 + vecteur_directeur_3


class Predator(Animoid):

    def __init__(self,  colour, len, speed_max,  perception, max_force) -> None:
        
        self.orientation = (np.random.rand(2) -0.5 ) * math.pi
        self.position = np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT])
        self.colour = colour
        self.len = len
        self.perception = perception
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) -0.5 ) * 5
        self.speed_max = speed_max 

    def chasse(self, index, list_boid, nb_predator):
        
        #Initialisation cohesion
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction
        total = 0

        #Pour tout les autres boids
        for sub_index, boid in enumerate (list_boid):
            
            #Si la norme euclidienne est plus petite que la distance de percepetion alors 
            if np.linalg.norm(Animoid.tab_norme[index, sub_index + nb_predator-1, :]) < self.perception:

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

        nb_boids = 45
        nb_predators = 3
        list_boids = np.array([Boids(WHITE, 30, 3, 100, 0.5) for _ in range(nb_boids)])
        list_predator = np.array([Predator(BLACK, 40, 3, 200, 0.5) for _ in range(nb_predators)])

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

            clock.tick(60)
            WIN.fill(BLUE_OCEAN)

            #Press
            key = pygame.key.get_pressed()

            #Border
            if not key[pygame.K_b] and press1 == False:
                press1 = True

            if key[pygame.K_b] and press1 == True:
                border = not border
                press1 = False

            for index, animoid in enumerate(list_animoids):

                #Calcul des normes entres les boids
                animoid.calcul_distance(index, list_animoids)
                #Comportement of boids
                #Filtre pour ne pas tomber sur nous même dans la list_boid
                if index >= len(list_predator):
                    index -= nb_predators
                    filter = np.array([], dtype = int)
                    filter = np.append(filter, np.arange(index))
                    filter = np.append(filter, np.arange(index+1, nb_boids))  

                    animoid.comportement(index, list_boids, list_predator, filter)

                #Comportement of predateur
                else:
                    animoid.chasse(index, list_boids, nb_predators)
             

                #Update position and draw
                animoid.update_position(border)
                animoid.draw()

            # Rafraîchit l'affichage
            pygame.display.flip()

        # Ferme Pygame
        pygame.quit()

    main()