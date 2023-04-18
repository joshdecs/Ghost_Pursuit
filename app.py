import pyxel

"""variables démarrage"""
# Dimensions de la fenêtre de jeu
screen_width = 640
screen_height = 320

#Hauteur de l'image du personnage
perso_height = 69

# Largeur de l'image du personnage
perso_width = 32

# Couleur de la banque d'image qui n'apparaît pas à l'écran
transparent_color = 2

# Couleur de l'arrière-plan nombre entre 0 et 16
background_color = 1

# Ordonnée du sol
floor_y = screen_height - 10

tile_mur_x = 10
avancee_max_droite = 320
avancee_max_gauche = 100
    
def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)


def detect_collision(x, y, dy):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= tile_mur_x:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) == tile_sol:
                return True
    return False  


class Personnage:
    
    def __init__(self):
        
        """Méthode du personnage"""
        
        # Apparence du Personnage
        self.height = perso_height
        self.width = perso_width
        self.color = 9
        
        # Position du Personnage
        self.x = screen_width/2
        self.y_min = floor_y - self.height
        self.y = self.y_min
        self.scroll_x = 0
        
        """Déplacements horizontaux du Personnage"""
        # Direction du personnage égale à -1 lorsqu'il est tourné vers la gauche et 1 vers la droite
        self.direction = 1
        # Vitesse du personnage en pixels/frame
        self.speed = 5
        
        """Utilisation du jetpack"""
        # Quantité de carburant initiale du jetpack du personnage (fixe) A NE PAS CHANGER
        self.fuel_init = 9 #A NE PAS CHANGER
        # Quantité de carburant variable du jetpack du personnage (variable)
        self.fuel = self.fuel_init
        # Quantité de carburant consommée chaque frame lors d'un saut
        self.fuel_variations = 0.05
        # taille de la jauge de carburant proportionnelle à la quantité de carburant restante
        self.fuel_bar = self.fuel
        # Coordonnées initiales en x et y de la jauge de carburant (en partant en haut à gauche de la fenêtre de jeu)
        self.fuel_bar_x_init = 22
        self.fuel_bar_y_init = 10
        
        self.health_bar_x_init = 4
        self.health_bar_y_init = 10
        self.health_bar_x = self.health_bar_x_init
        self.health_bar_y = self.health_bar_y_init
        # Coordonnées variables en x et y de la jauge de carburant (en partant en haut à gauche de la fenêtre de jeu)
        self.fuel_bar_x = self.fuel_bar_x_init
        self.fuel_bar_y = self.fuel_bar_y_init
        # Couleur de la jauge de carburant qui varie en fonction du carburant consommé
        self.fuel_bar_color = 10
        
        # Déplacements verticaux du Personnage / gravité
        self.gy = 0
        self.jump = 12
        self.jumping = False
        self.gravity = 1
        
        # Variables relatives aux tirs du Personnage
        self.tir_liste = []
        self.tir = False
        self.tir_x = self.x + self.width
        self.tir_y = self.y + 30
        self.tir_speed = 10
        self.tir_direction = self.direction
        
        # variables relatives à la dague
        self.dague_x = 50
        self.dague_y = 50
        self.map_dague_x = 64
        self.map_dague_y = 88
        self.dague_width = 16
        self.dague_height = 16

  
    def deplacement_gauche_Personnage(self):
        
        # Déplacement vers la gauche
        if pyxel.btn(pyxel.KEY_Q) :
            self.x -= self.speed
            self.direction = -1
 
    def deplacement_droite_Personnage(self):
        
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
            self.direction = 1
 
    def deplacement_vertical_Personnage(self):    
        # Dépolacement vers le haut / saut
        if pyxel.btn(pyxel.KEY_SPACE) and self.y == self.y_min and self.fuel > 0:
            self.jumping = True
            self.gy -= self.jump
        
        # Déplacement vers le bas 
        if pyxel.btn(pyxel.KEY_S) and self.y < self.y_min:
            self.y += 10
        
        # Gravité en fin de saut    
        if self.gy < 0:
            self.y += self.gy
            self.gy += self.gravity
        
        # Gravité lorsque la flèche du haut n'est plus pressée    
        if not pyxel.btn(pyxel.KEY_SPACE) or self.fuel <= 0:
            self.y += self.gy
            self.gy += self.gravity
        
        # Le personnage arrête de tomber lorsqu'il touche le sol
        if self.y > self.y_min:
            self.jumping = False
            self.y = self.y_min
            self.gy = 0
    
    def scroll_player(self):
        if self.x > (self.scroll_x + avancee_max_droite) and self.scroll_x < 1402:
            self.scroll_x = self.x - avancee_max_droite
        if self.x < (self.scroll_x + avancee_max_gauche) and self.scroll_x > 0:
            self.scroll_x = self.x - avancee_max_gauche
            
    def tir_creation(self):
        
        #création d'un tir avec la barre d'espace
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 0, 5):
            self.tir_x = (self.x + self.width) if self.direction == 1 else self.x
            self.tir_y = self.y + 30
            self.tir_liste.append([self.tir_x, self.tir_y, self.direction])
            self.tir = True
            
        else:
            self.tir = False
            
    def consume_fuel(self):
        
        if self.jumping == True and self.fuel > 0:
            self.fuel -= self.fuel_variations
            self.fuel_bar_y += self.fuel_variations * 8
        if self.jumping == False and self.fuel < self.fuel_init :
            self.fuel += self.fuel_variations
            self.fuel_bar_y -= self.fuel_variations * 8
            
        
    def tir_deplacement(self):
        
        #déplacement des tirs vers la droite ou la gauche et suppression s'ils sortent du cadre
        for tir in self.tir_liste:
            tir[0] += self.tir_speed*tir[2]
            if  tir[0]<0 or tir[0]>screen_width:
                self.tir_liste.remove(tir)
    
    
    
    def fuel_bar_color_change(self):
        if self.fuel <= 9 and self.fuel >=6:
            self.fuel_bar_color = 10
            
        elif self.fuel < 6 and self.fuel >= 3: 
            self.fuel_bar_color = 9
            
        elif self.fuel < 3 and self.fuel >= 0:
            self.fuel_bar_color = 4
            
            
    
    def update(self):
        # Mise à jour des fonctions du personnage
        self.deplacement_gauche_Personnage()
        self.deplacement_droite_Personnage()
        self.deplacement_vertical_Personnage()   
        self.tir_creation()
        self.tir_deplacement()
        self.scroll_player()
        self.consume_fuel()
        self.fuel_bar_color_change()

    
    def draw(self):
        # Affichage du personnage
        # Chargement du fichier ressources
        
        
        # Variable w permettant d'orienter le personnage vers la droite ou la gauche selon si elle est positive ou non
        w = self.width if self.direction > 0 else -self.width
        
        # Affichage du personnage lorsqu'il n'est pas en train de tirer
        if not self.tir:
            pyxel.blt(self.x, self.y, 0, 16, 0, w, self.height, transparent_color)
        
        # Affichage du personnage en position de tir
        elif self.tir:
            pyxel.blt(self.x, self.y, 0, 48, 0, w, self.height, transparent_color)
        
        # Afichage des flammes sous la planche
        if(pyxel.frame_count % 3 == 0):
            pyxel.blt(self.x + 8, self.y + 69, 0, 29, 69, self.width - 3, 3, transparent_color)
        if self.jumping is True:
            pyxel.blt(self.x, self.y + 16, 0, 8, 72, w, 32, transparent_color)
        
        # Affichage des tirs    
        for tir in self.tir_liste:
            pyxel.rect(tir[0], tir[1], 4, 1, 10)    
            
        self.fuel_bar_height = self.fuel
        pyxel.rect(self.fuel_bar_x_init - 2 + self.scroll_x, self.fuel_bar_y_init-2, 14, self.fuel_init*8 + 4, 0)
        pyxel.rect(self.fuel_bar_x + self.scroll_x, self.fuel_bar_y, 10, self.fuel_bar_height*8, self.fuel_bar_color)
        pyxel.rect(self.health_bar_x-2 + self.scroll_x,self.health_bar_y-2,14,9*8+4,0)
        pyxel.rect(self.health_bar_x + self.scroll_x,self.health_bar_y,10,9*8,3)
        
        
        
        
        # Affichage de la Dague
        pyxel.blt(self.x + 25, self.y + 20, 0, self.map_dague_x, self.map_dague_y, self.dague_width, self.dague_height, transparent_color)
        
        pyxel.mouse(True) 
     
    
class App:
    
    def __init__(self):
        pyxel.init(screen_width, screen_height)
        pyxel.load("resourcesfinal.pyxres")
        self.personnage = Personnage()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.personnage.update()
        
    
    def draw(self):
        pyxel.cls(0)
        # Remplissage arrière-plan
        pyxel.camera()
        
        for i in range(0, 1792, 256):
            pyxel.bltm(i - self.personnage.scroll_x//3, 0, 0, 0, 1920, 256, 70, transparent_color)
            pyxel.bltm(i - self.personnage.scroll_x//3, 70, 0, 0, 1920, 256, 128, transparent_color)
            pyxel.bltm(i - self.personnage.scroll_x//3, 198, 0, 0, 1952, 256, 128, transparent_color)
            pyxel.bltm(i - self.personnage.scroll_x//3, 224, 0, 0, 1952, 256, 96, transparent_color)
        
        
        pyxel.bltm(0, 0, 0, self.personnage.scroll_x, 0, screen_width, screen_height, transparent_color)
        pyxel.camera(self.personnage.scroll_x, 0)
        self.personnage.draw()
        
        
        

        
App()