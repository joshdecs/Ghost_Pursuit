import pyxel
import random
# variables pour le jeu
transparent_color = 2
background_color = 1
screen_width = 256
screen_height = 128
walking_max_right = 100
walking_max_left = 100
scroll_x = 0
scroll_y = 0
liste_obstacles = [(0, 4), (1, 4), (0, 5), (1, 5)]
game = False

    
class Player:
    def __init__(self):
        self.width = 28
        self.height = 31
        self.chest_height = 21
        self.x = screen_width //2
        self.y = screen_height //2
        self.img_x = 26
        self.img_y = 0
        self.speed = 2
        self.direction = 1
        self.scroll_x = 0
        self.is_walking = False
        # variables de collisions
        self.collision_right = False
        self.collision_left = False
        self.collision_up = False
        self.collision_down = False
        # leg frames fn =[u, v, w, d_x]
        self.f_1 = [32, 21, 16, 0]
        self.f_2 = [56, 21, 16, 0]
        self.f_3 = [72, 21, 16, 0]
        self.f_4 = [88, 21, 16, 0]
        self.f_5 = [104, 21, 16, 0]
        self.f_6 = [128, 21, 16, 0]
        self.f_not_walking = [144, 21, 16, 0]
        self.f =  self.f_1
        self.f_jump = [167, 21, 18, 0]
        self.y_r = 0
        

        
        # Déplacements verticaux du Personnage / gravité
        self.gy = 0
        self.jump_strength = 12
        self.is_jumping = False
        self.gravity = 1
        self.floor_y = screen_height
        self.max_y_down = screen_height
        self.max_y_up = 0
        
        # variables de tirs
        self.gunshots_list = []
        self.gunshooting = False
        self.gunshot_speed = 5
        self.gunshot_y_position = 18
        
        self.shot_init = 25 #A NE PAS CHANGER
        self.shot = self.shot_init
        self.shot_variations = 1
        self.shot_bar_x_init = 5
        self.shot_bar_y_init = 5
        self.shot_bar = self.shot
        self.shot_bar_color = 7
        self.shot_bar_x = 5
        self.shot_bar_y = 5
        self.shot_bar_height = self.shot_init
        self.shot_bar_width = 5

    
    
    # Fonction detection collision 
    def detection_collisions(self):

        
        # detection collisions à right
        d_x = (self.x-12 + self.width) // 8
        d_y1 = (self.y)//8
        d_y2 = (self.y + self.height - 1)//8
        for d_yi in range(d_y1, d_y2 + 1):
            if pyxel.tilemap(0).pget(d_x, d_yi) in liste_obstacles:
                self.collision_right = True
                break
            else:
                self.collision_right = False
    
    
        # detection collision à left
        g_x = (self.x-1)//8
        g_y1 = (self.y)//8 
        g_y2 = (self.y + self.height - 1)//8
        for g_yi in range(g_y1, g_y2 + 1):
            if pyxel.tilemap(0).pget(g_x, g_yi) in liste_obstacles:
                self.collision_left = True
                break
            else:
                self.collision_left = False
            
    
        # detection collision en up
        h_x1 = (self.x)//8
        h_x2 = (self.x + self.width - 1)//8 
        h_y = (self.y - 1)//8
        for h_xi in range(h_x1, h_x2 + 1):
            if pyxel.tilemap(0).pget(h_xi, h_y) in liste_obstacles :
                self.collision_up = True
                break
            else:
                self.collision_up = False
    
        # detection collision en down
        b_x1 = (self.x)//8
        b_x2 = (self.x + self.width - 1)//8 
        b_y = (self.y + self.height + self.gy - 1)//8
        for b_xi in range(b_x1, b_x2 + 1):
            if pyxel.tilemap(0).pget(b_xi, b_y) in liste_obstacles :
                self.collision_down = True
                self.floor_y = b_y * 8
                break
            else:
                self.collision_down = False
        
    
    # Fonction de déplacement du joueur
    def player_move(self):
        if pyxel.btn(pyxel.KEY_D):
            self.is_walking = True
            self.direction = 1
            if self.collision_right == False:
                self.x += self.speed
            
            
            
        elif pyxel.btn(pyxel.KEY_Q):
            self.direction = -1
            self.is_walking = True
            if self.collision_left == False:
                self.x -= self.speed
            
        
        else:
            self.is_walking = False
        
        
        if self.collision_down:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.gy -= self.jump_strength
                self.is_jumping = True
            else:
                self.gy = 0
                self.is_jumping = False
                
        if self.collision_up:
            self.gy = self.gravity
        
                
        
        self.y += self.gy
        self.gy += self.gravity

        if pyxel.btn(pyxel.KEY_S):
            deplacement_down = True
            if self.collision_down == False:
                self.y += self.speed


    def scroll_player(self):
        global scroll_x, scroll_y
        if self.x > (scroll_x + walking_max_right) and scroll_x < 1790:
            scroll_x = self.x - walking_max_right
        if self.x < (scroll_x + walking_max_left) and scroll_x > 0:
            scroll_x = self.x - walking_max_left
            
        if self.y > 0 and self.y <= screen_height:
            scroll_y = 0
        elif self.y > screen_height and self.y < 2*screen_height:
            scroll_y = screen_height
        elif self.y > 2*screen_height and self.y < 3*screen_height:
            scroll_y = 2*screen_height
        elif self.y >= 3*screen_height and self.y < 4*screen_height:
            scroll_y = 3*screen_height
            
    def player_gunshots(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.shot > 0:
            self.gunshot_y_position = 18 if self.y_r == 1 else 17
            self.gunshot_x_position = 20 if self.direction == 1 else 3
            self.gunshots_list.append([self.x, self.y, self.direction, self.gunshot_y_position, self.gunshot_x_position])
            self.shot -= 1
        else :
            self.gunshooting = False
            
        for gunshot in self.gunshots_list:
            gunshot[0] += self.gunshot_speed * gunshot[2]
        if pyxel.btnr(pyxel.KEY_R):
            self.shot = 9
            self.shot_bar_height += 9
            
    def consume_shot(self):
        
        if self.gunshooting == True and self.shot > 0:
            self.shot -= self.shot_variations
            self.shot_bar_height -= self.shot_variations
        if self.gunshooting == False and self.shot < self.shot_init :
            self.shot += self.shot_variations
            

    def update(self):
        
        global scroll_x, scroll_y
        self.detection_collisions()
        self.player_move()
        self.scroll_player()
        self.player_gunshots()
        self.consume_shot()

    def draw(self):
        n = 5 if self.is_walking else 15
        if (pyxel.frame_count % n == 0):
            self.y_r = 1 if self.y_r == 0 else 0
        # défilement images de marche 
        if (pyxel.frame_count % (4//self.speed) == 0) and self.is_walking == True:
            if self.f == self.f_1:
                self.f = self.f_2
            elif self.f == self.f_2:
                self.f = self.f_3
            elif self.f == self.f_3:
                self.f = self.f_4
            elif self.f == self.f_4:
                self.f = self.f_5
            elif self.f == self.f_5:
                self.f = self.f_6
            else:
                self.f = self.f_1
        if self.is_walking == False:
            self.f = self.f_not_walking
        if self.is_jumping == True:
            self.f = self.f_jump 
        # Variable w_f et variable x_f de compensation permettant d'orienter les jambes du personnage vers la right ou la left selon si elle est positive ou non + pareil avec w mais pour le buste      
        if self.direction > 0:
            w_f = self.f[2]
            x_f = 0
            w = self.width
        else:
            w_f = - self.f[2]
            x_f = 12
            w = - self.width
            
        pyxel.blt(self.x + x_f, self.y + self.chest_height,0, self.f[0], 21, w_f, 10, transparent_color)
        pyxel.blt(self.x, self.y + self.y_r, 0, 32, 0, w, self.chest_height, transparent_color)
        
        for gunshot in self.gunshots_list:
            pyxel.rect(gunshot[0] + gunshot[4], gunshot[1] + gunshot[3], 4, 1, 9)
            
        pyxel.rect(self.shot_bar_x_init - 2 + scroll_x, self.shot_bar_y_init-2, 14, self.shot_init + 4, 0)
        pyxel.rect(self.shot_bar_x + scroll_x, self.shot_bar_y, 10, self.shot_bar_height, self.shot_bar_color)
        
        
        
class Ennemi_1:
    def __init__(self):
        self.player = Player()
        self.img_x = 192
        self.img_y = 0
        self.width = 20
        self.height = 21
        self.speed = 2
        
        
        
        
    #def update(self):
        
        
        
    #def draw(self):
        
        
class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height)
        pyxel.load("new.pyxres")
        
        self.player = Player()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        global game
        if game == True:
            self.player.update()
    
        if pyxel.btn(pyxel.KEY_G):
            game = True
    
    def draw(self):
        pyxel.cls(0)
        if game == True:
            pyxel.camera()
            for i in range(0, 1792, 256):
                pyxel.bltm(i - scroll_x//3, 0, 0, 0, 1920, 256, 128, transparent_color)
                
            pyxel.bltm(0, 0, 0, scroll_x, scroll_y, 296, 128, transparent_color)
            
            pyxel.camera(scroll_x, scroll_y)
            self.player.draw()
    
        
        else:
            pyxel.rect(0,0,screen_width, screen_height, 9)

App()
 
