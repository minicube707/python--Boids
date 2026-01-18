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
BLUE_OCEAN = (0, 5, 100)

# Remplit l'écran avec la couleur blanche
WIN.fill(BLUE_OCEAN)

# Définit le titre de la fenêtre
pygame.display.set_caption("Basic pygame")


""""""""""""""""""""""""""""""""""""""
#Version super optimisé avec le tableau des distances et la révision du code pour augmenter la performance
#Tranformation du tableau commun des distances en tableau commun des normes
#Ajout d'un vecteur pour plus de réalsime lorsque les boids sont proche de la bordure
""""""""""""""""""""""""""""""""""""""

class Boids():

    tab_norme = np.array([[]], dtype=np.int32)

    def __init__(self,  colour, len, speed_max,  perception, max_force) -> None:
        self.orientation = (np.random.rand(2) - 0.5 ) * math.pi
        self.position = np.array([np.random.rand() * WIDTH, np.random.rand() * HEIGHT])
        self.colour = colour
        self.len = len
        self.perception = perception
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) - 0.5 ) * 5
        self.speed_max = speed_max 

    def calcul_distance(self, index, list_boids):

        """"""""""""""""""""""""""""""""""""""
        #Récupératoin des distance
        """"""""""""""""""""""""""""""""""""""
        #Initialisation
        list_norme = np.array([],dtype=np.int32) 
         
        #Si c'est le premier boid initialisation du tableau des distances communes
        if index == 0:
            Boids.tab_norme = np.array([], dtype=np.int32)

        #Sinon on recopie les valeurs déjà trouvers
        else:
            list_norme = np.append(list_norme, Boids.tab_norme[:, index -1])

        #Pour chaque autre boids, calcul des distances        
        for other_boids in list_boids[index +1:]:

            #Calcul de la norme euclidienne
            norme = np.int32(np.linalg.norm(other_boids.position - self.position))
            list_norme = np.append(list_norme, norme)

        Boids.tab_norme = np.append(Boids.tab_norme, list_norme)
        Boids.tab_norme = Boids.tab_norme.reshape((index +1, len(list_boids) -1))

    def comportement(self, index, list_boid, filter):

        #Initialisation  alignement
        vecteur_directeur_1 = np.zeros((2))
        average_vecteur_1 = np.zeros((2)) #Vecteur moyen
        
        #Initialisation cohesion
        vecteur_directeur_2 = np.zeros((2))
        center_mass = np.zeros((2)) #Centre d'attraction

        #Initialisation
        vecteur_directeur_3 = np.zeros((2))
        average_vecteur_3 = np.zeros((2)) #Vecteur moyen
        
        total = 0
        epsilon = 1e-3
        
        #Pour tout les autres boids
        for sub_index, boid in enumerate (list_boid[filter]):
            
            #Si la norme euclidienne est plus petite que la distance de percepetion alors 
            distance = Boids.tab_norme[index, sub_index]
            if distance < self.perception:

                total += 1

                #Alignement
                average_vecteur_1 += boid.speed
                
                #Cohesion
                center_mass += boid.position

                #Séparation
                diff = self.position - boid.position
                diff = diff / distance**2
                average_vecteur_3 += diff


        #Random
        rand = random.randint(1, 50)
        rand_speed = (np.random.rand()*2) - 1

        if rand == 1:
            self.speed[0] += rand_speed

        elif rand == 2:
            self.speed[1] += rand_speed

        #'il y a au moins un voisin alors
        if total > 0:

            """"""""""""""""""""""""""""""""""""""
            #Alignement
            """"""""""""""""""""""""""""""""""""""
            average_vecteur_1 = average_vecteur_1 / total

            #Normalisation du vecteur moyen et multiplication par la vitesse max
            average_vecteur_1 = (average_vecteur_1 / (np.linalg.norm(average_vecteur_1) + epsilon)) * self.speed_max
            vecteur_directeur_1 = average_vecteur_1 - self.speed
        

            """"""""""""""""""""""""""""""""""""""
            #Cohesion
            """"""""""""""""""""""""""""""""""""""
            center_mass = center_mass / total
            vecteur_to_com = center_mass - self.position

            #Normalisation du vecteur de direction
            if np.linalg.norm(vecteur_to_com) > 0:
                vecteur_to_com = (vecteur_to_com / np.linalg.norm(vecteur_to_com)) * self.speed_max

            vecteur_directeur_2 = vecteur_to_com - self.speed
            
            #Normalisation du vecteur directeur
            if np.linalg.norm(vecteur_directeur_2) > self.max_force:
                vecteur_directeur_2 = (vecteur_directeur_2 / np.linalg.norm(vecteur_directeur_2)) * self.max_force

      
            """"""""""""""""""""""""""""""""""""""
            #Séparation
            """"""""""""""""""""""""""""""""""""""
            average_vecteur_3 = average_vecteur_3 / total
            vecteur_directeur_3 = average_vecteur_3 - self.speed
                
            #Normalisation du vecteur directeur
            if np.linalg.norm(vecteur_directeur_3) > self.max_force:
                vecteur_directeur_3 = (vecteur_directeur_3 / np.linalg.norm(vecteur_directeur_3)) * self.max_force
        
        self.speed += vecteur_directeur_1 + vecteur_directeur_2 + vecteur_directeur_3



    def update_position(self):
         
        self.position += self.speed

        #Limit
        if np.linalg.norm(self.speed) > self.speed_max:
            self.speed = self.speed / np.linalg.norm(self.speed) * self.speed_max

        self.orientation = np.arctan2(-self.speed[1], self.speed[0]) 
        
        #Vérifie que les boids ne sorte pas de l'écran
        if self.position[0] - self.perception < 0:
            distance = np.linalg.norm(np.array([0, self.position[1]] - self.position))
            diff = self.position - np.array([0, self.position[1]])
            diff = diff / distance
            vecteur_directeur = diff - self.speed
            vecteur_directeur += np.array([0, 1])
            self.speed += vecteur_directeur

        elif self.position[0] + self.perception > WIDTH:
            distance = np.linalg.norm(np.array([WIDTH, self.position[1]] - self.position))
            diff = self.position - np.array([WIDTH, self.position[1]])
            diff = diff / distance
            vecteur_directeur = diff - self.speed
            vecteur_directeur += np.array([0, - 1])
            self.speed += vecteur_directeur

        if self.position[1] - self.perception < 0:
            distance = np.linalg.norm(np.array([self.position[0], 0] - self.position))
            diff = self.position - np.array([self.position[0], 0])
            diff = diff / distance
            vecteur_directeur = diff - self.speed
            vecteur_directeur += np.array([-1, 0])
            self.speed += vecteur_directeur

        elif self.position[1] + self.perception > HEIGHT:
            distance = np.linalg.norm(np.array([self.position[0], HEIGHT] - self.position))
            diff = self.position - np.array([self.position[0], HEIGHT])
            diff = diff / distance
            vecteur_directeur = diff - self.speed
            vecteur_directeur += np.array([1, 0])
            self.speed += vecteur_directeur
        

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
        
        """pygame.draw.circle(WIN, BLACK, position, self.perception, 2)"""

if __name__ == "__main__":

    def main():

        nb_boids = 100
        list_boids = np.array([Boids(RED, 10, 5, 60, 0.01) for _ in range(nb_boids)])


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

            for index, boid in enumerate(list_boids):

                #Calcul des normes entres les boids
                boid.calcul_distance(index, list_boids)

                #Comportement of bird

                #Filtre pour ne pas tomber sur nous même dans la list_boid
                filter = np.array([], dtype = int)
                filter = np.append(filter, np.arange(index))
                filter = np.append(filter, np.arange(index+1, nb_boids))  

                boid.comportement(index, list_boids, filter)
 
                #Update position and draw
                boid.update_position()
                boid.draw()

            # Rafraîchit l'affichage
            pygame.display.flip()

        # Ferme Pygame
        pygame.quit()

    main()
