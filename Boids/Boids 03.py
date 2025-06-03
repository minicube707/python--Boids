import pygame
import math
import numpy as np
import random

pygame.init()

# Crée une fenêtre de 1_550, 860pixels
WIDTH, HEIGHT = 1_550, 860
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Définit la couleur blanche
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

# Remplit l'écran avec la couleur blanche
WIN.fill(WHITE)

# Définit le titre de la fenêtre
pygame.display.set_caption("Basic pygame")


""""""""""""""""""""""""""""""""""""""
#Version origianl
""""""""""""""""""""""""""""""""""""""

class Boids():

    def __init__(self,  colour, len, speed_max,  perception, max_force) -> None:
        self.orientation = (np.random.rand(2) -0.5 ) * math.pi
        self.position = np.random.rand((2))  * HEIGHT 
        self.colour = colour
        self.len = len
        self.perception = perception
        self.max_force = max_force

        #Vitesse
        self.speed = (np.random.rand(2) -0.5 ) * 5
        self.speed_max = speed_max 

    
    def alignement(self, list_boid):

        #Initialisation
        vecteur_directeur = np.zeros((2))
        total = 0
        average_vecteur = np.zeros((2)) #Vecteur moyen

        for boid in list_boid:
            #Si ce n'est pas nous même et que la norme euclidienne est plus petite que la distance de percepetion alors 
            if self != boid and  np.linalg.norm(boid.position - self.position) < self.perception:
                average_vecteur += boid.speed
                total += 1

        if total > 0:
            average_vecteur = average_vecteur / total
            #Normalisation du vecteur moyen et multiplication par la vitesse max
            average_vecteur = (average_vecteur / np.linalg.norm(average_vecteur)) * self.speed_max
            vecteur_directeur = average_vecteur - self.speed
        self.speed += vecteur_directeur


    def cohesion(self, list_boid):

        #Initialisation
        vecteur_directeur = np.zeros((2))
        total = 0
        center_mass = np.zeros((2)) #Centre d'attraction

        for boid in list_boid:
            
            #Si ce n'est pas nous même et que la norme euclidienne est plus petite que la distance de percepetion alors 
            if self != boid and np.linalg.norm(boid.position - self.position) < self.perception:
                center_mass += boid.position
                total += 1

        if total > 0:
            
            center_mass = center_mass / total
            vecteur_to_com = center_mass - self.position

            if np.linalg.norm(vecteur_to_com) > 0:
                vecteur_to_com = (vecteur_to_com / np.linalg.norm(vecteur_to_com)) * self.speed_max

            vecteur_directeur = vecteur_to_com - self.speed
            
            if np.linalg.norm(vecteur_directeur)> self.max_force:
                vecteur_directeur = (vecteur_directeur / np.linalg.norm(vecteur_directeur)) * self.max_force

        self.speed += vecteur_directeur

    def separaton(self, list_boid):

        #Initialisation
        vecteur_directeur = np.zeros((2))
        total = 0
        average_vecteur = np.zeros((2)) #Vecteur moyen
        
        for boid in list_boid:
            
            distance =  np.linalg.norm(boid.position - self.position)
            if self != boid and distance < self.perception:
                diff = self.position - boid.position
                diff = diff / distance
                average_vecteur += diff
                total +=1

            if total > 0:
                average_vecteur = average_vecteur / total
                vecteur_directeur = average_vecteur - self.speed

                if np.linalg.norm(vecteur_directeur)> self.max_force:
                    vecteur_directeur = (vecteur_directeur / np.linalg.norm(vecteur_directeur)) * self.max_force
        
        self.speed += vecteur_directeur

    def random_mouvement (self):
        rand = random.randint(1, 10)
        rand_speed = (np.random.rand()*2) - 1

        if rand == 1:
            self.speed[0] += rand_speed

        elif rand == 2:
            self.speed[1] += rand_speed


    def update_position(self):
         
        self.position += self.speed

        if np.linalg.norm(self.speed) > self.speed_max:
            self.speed = self.speed / np.linalg.norm(self.speed) * self.speed_max


        self.orientation = np.arctan2(-self.speed[1], self.speed[0]) 
        
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
        
        
        """pygame.draw.circle(WIN, BLACK, position, self.perception, 2)"""

if __name__ == "__main__":
    def main():

        nb_boids = 40
        list_boids = [Boids(BLACK, 10, 3, 100, 0.05) for _ in range(nb_boids)]


        # Boucle principale
        running = True
        clock = pygame.time.Clock()

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
            WIN.fill(WHITE)

            #Update
            for boid in list_boids:
                boid.alignement(list_boids)
                boid.cohesion(list_boids)
                boid.separaton(list_boids)
                boid.random_mouvement()
                boid.update_position()
                boid.draw()

            # Rafraîchit l'affichage
            pygame.display.flip()
        # Ferme Pygame
        pygame.quit()

    main()
