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
score = 0
liste_obstacles = [(0, 4), (1, 4), (0, 5), (1, 5)]
game = False
game_start = True
game_over = False

    
class Player:
    def __init__(self):
        self.width = 20
        self.height = 31
        self.chest_height = 21
        self.x = screen_width //2
        self.y = screen_height //2
        self.img_x = 26
        self.img_y = 0
        self.speed = 2
        self.health = 25
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
        

    # Fonction detection collision 
    def detection_collisions(self):

        
        # detection collisions à right
        d_x = (self.x + self.width) // 8
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
                pyxel.play(1, 4, 1, False)
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
            
    

    def update(self):
        
        global scroll_x, scroll_y
        self.detection_collisions()
        self.player_move()
        self.scroll_player()
        
        

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
            x_f = 4
            w = - self.width
            
        pyxel.blt(self.x + x_f, self.y + self.chest_height,0, self.f[0], 21, w_f, 10, transparent_color)
        pyxel.blt(self.x, self.y + self.y_r, 0, 32, 0, w, self.chest_height, transparent_color)
        
        pyxel.rect(58 + scroll_x, scroll_y, 42, 9, 0)
        pyxel.text(60 + scroll_x, 2 + scroll_y, "HP|      |", 7)
        pyxel.rect(71 + scroll_x, 2 + scroll_y, self.health, 5, 9)
        pyxel.text(80 + scroll_x, 2 + scroll_y, str(self.health), 7)
        

class Player_gunshots():
    def __init__(self):
        self.player = Player()
        self.gunshots_list = []
        self.gunshot_speed = 4
        
        self.munitions_init = 25 #A NE PAS CHANGER
        self.munitions = 25

        
    def gunshots_creation(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.munitions > 0:
            self.munitions -= 1
            self.gunshot_y_position = 18 if self.player.y_r == 1 else 17
            self.gunshot_x_position = 20 if self.player.direction == 1 else 3
            self.gunshots_list.append([self.player.x + self.gunshot_x_position, self.player.y + self.gunshot_y_position, self.player.direction])
            pyxel.play(2, 1, 1, False)
            
    def fill_munitions(self):
        if pyxel.btnr(pyxel.KEY_R) and self.munitions <= 0:
            self.munitions = self.munitions_init

        
    def gunshots_move(self):
        for gunshot in self.gunshots_list:
            gunshot[0] += gunshot[2] * self.gunshot_speed
            
    def gunshots_collisions_wall(self):
        for gunshot in self.gunshots_list:
            if pyxel.tilemap(0).pget((gunshot[0])//8, (gunshot[1])//8) in liste_obstacles:
                self.gunshots_list.remove(gunshot)
            
  
    def update(self):
        self.player.update()
        self.fill_munitions()
        self.gunshots_creation()
        self.gunshots_move()
        self.gunshots_collisions_wall()
        
    def draw(self):
        self.player.draw()
        for gunshot in self.gunshots_list:
            pyxel.rect(gunshot[0], gunshot[1], 4, 1, 9)
        
        pyxel.rect(scroll_x, scroll_y, 55, 9, 0)
        pyxel.text(2 + scroll_x, 2 + scroll_y, "MUNITIONS:", 7)
        pyxel.text(42 + scroll_x, 2 + scroll_y, str(self.munitions), 7)
        
class Ghosts:
    def __init__(self):
        self.player = Player()
        
        # coordonnées dans la banque d'images
        self.img_x = 194
        self.img_y = 4
        
        self.width = 18
        self.height = 17
        self.speed = 2
        self.health = 10
        
        # liste qui va acceullir les données de chaque fantôme
        self.ghosts_list = []
        
        # -1 => gauche et 1 => droite
        self.direction_list = [-1, 1]
        
        # 4 étages possibles lors de leur apparition
        self.ghosts_y = [90, 215, 345, 475]
        
        # première crétion de fantôme [nombre de fantômes créés, True ou False] si False alors déja effectuée
        self.number = 25
        
        for i in range(self.number):  
            self.ghosts_list.append([random.randint(10, 2040), self.ghosts_y[random.randint(0, 3)], self.health, self.direction_list[random.randint(0, 1)]])
        
        
            
    def ghosts_move(self):
        for ghost in self.ghosts_list:
            
            if ghost[0] < 2042 and ghost[0] > -11:
                ghost[0] += self.speed * ghost[3]
                
            elif ghost[0] > 2038:
                ghost[0] -= self.speed
                ghost[3] = -1
                
            elif ghost[0] < - 10:
                ghost[0] += self.speed
                ghost[3] = 1
                
    def ghosts_collisions(self):
        for ghost in self.ghosts_list:

            if ghost[1] <= (self.player.y + self.player.height) and (ghost[1] + self.height) >= self.player.y and ghost[0] <= (self.player.x + self.player.width) and (ghost[0] + self.width) >= self.player.x:
                ghost[0] += 50 * ghost[3]
                if self.player.health > 0:
                    self.player.health -= 1
                
    
                    
    def ghosts_remove(self):
        global score
        for ghost in self.ghosts_list:
            if ghost[2] <= 0:
                self.ghosts_list.remove(ghost)
                score += 10
                
                
    def update(self):
        self.player.update()
        self.ghosts_move()
        self.ghosts_collisions()
        self.ghosts_remove()
        

    def draw(self):
        self.player.draw()
        for ghost in self.ghosts_list:
            w = self.width if ghost[3] == -1 else -self.width
            pyxel.blt(ghost[0], ghost[1], 0, self.img_x, self.img_y, w, self.height, transparent_color)
            x_variation = 0 if ghost[3] == -1 else 7
            pyxel.rect(ghost[0] - 1 + x_variation, ghost[1] - 4, self.health + 2, 3, 0)
            pyxel.rect(ghost[0] + x_variation, ghost[1] - 3, ghost[2], 1, 10)
        
        
        
class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height)
        pyxel.load("res.pyxres")
        #pyxel.playm(0, 120, True)
        self.player = Player()
        self.player_gunshots = Player_gunshots()
        self.ghosts = Ghosts()
        pyxel.run(self.update, self.draw)
        
    def collisions_ghosts_gunshots(self):
        for ghost in self.ghosts.ghosts_list:
            for gunshot in self.player_gunshots.gunshots_list:
                if gunshot[0] > ghost[0] and gunshot[0] < (ghost[0] + self.ghosts.width) and gunshot[1] > ghost[1] and gunshot[1] < (ghost[1] + self.ghosts.height):
                    self.player_gunshots.gunshots_list.remove(gunshot)
                    ghost[2] -= 1
                    
        
    def update(self):
        global game
        if game == True:
            self.player.update()
            self.player_gunshots.update()
            self.ghosts.update()
            self.collisions_ghosts_gunshots()
    
        if pyxel.btn(pyxel.KEY_G):
            game = True
    
    def draw(self):
        pyxel.cls(0)
        pyxel.mouse(True) 
        if game == True:
            pyxel.camera()
            for i in range(0, 1792, 256):
                pyxel.bltm(i - scroll_x//3, 0, 0, 0, 1920, 256, 128, transparent_color)
                
            pyxel.bltm(0, 0, 0, scroll_x, scroll_y, 296, 128, transparent_color)
            
            pyxel.camera(scroll_x, scroll_y)
            self.player.draw()
            self.player_gunshots.draw()
            self.ghosts.draw()
            pyxel.rect(screen_width - 52 + scroll_x, scroll_y, 52, 9, 0)
            pyxel.text(screen_width - 50 + scroll_x, 2 + scroll_y, "SCORE:", 7)
            pyxel.text(screen_width - 25 + scroll_x, 2 + scroll_y, str(score), 7)
            pyxel.rect(screen_width - 94 + scroll_x, scroll_y, 40, 9, 0)
            pyxel.text(screen_width - 92 + scroll_x, 2 + scroll_y, "GHOSTS:", 7)
            pyxel.text(screen_width - 64 + scroll_x, 2 + scroll_y, str(len(self.ghosts.ghosts_list)), 7)
            
    
        
        else:
            pyxel.rect(0,0,screen_width, screen_height, 9)

App() 

