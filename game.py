import pygame # type: ignore
from sys import exit
from random import randint, choice

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score : {current_time}', True, 'Black')
    score_rect = score_surf.get_rect(center = (490, 100))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(samurai.sprite, obstacle_group, False):
        obstacle_group.empty()
        hit_sound = pygame.mixer.Sound('assets/sfx/hit.wav')
        hit_sound.play()
        return False
    else:
        return True

class Samurai(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.samurai_run = [pygame.image.load('assets/images/samurai/run/01.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/02.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/03.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/04.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/05.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/06.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/07.png').convert_alpha(),
            pygame.image.load('assets/images/samurai/run/08.png').convert_alpha()]
        self.samurai_index = 0
        self.samurai_jump = pygame.image.load('assets/images/samurai/jump/01.png').convert_alpha()
        
        self.image = self.samurai_run[self.samurai_index]
        self.rect = self.image.get_rect(midbottom = (200, 450))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('assets/sfx/jump.wav')
        self.jump_sound.set_volume(0.2)

    def samurai_input(self):
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP])and self.rect.bottom >= 450:
            self.gravity = -20
            self.jump_sound.play()
        if(keys_pressed[pygame.K_LEFT]) and self.rect.left >= 0:
            self.rect.x -= 5
        if(keys_pressed[pygame.K_RIGHT]) and self.rect.right <= SCREEN_SIZE[0] - 100:
            self.rect.x += 5

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 450 : self.rect.bottom = 450
    
    def samurai_animation(self):
        if self.rect.bottom < 450:
            self.image = self.samurai_jump
        else:
            self.samurai_index += 0.25
            if self.samurai_index >= len(self.samurai_run):
                self.samurai_index = 0
            self.image = self.samurai_run[int(self.samurai_index)]
    def update(self):
        self.samurai_input()
        self.apply_gravity()
        self.samurai_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'bird':
            bird_frame1 = pygame.image.load('assets/images/bird/01.png').convert_alpha()
            bird_frame1 = pygame.transform.rotozoom(bird_frame1, 0, 2.5)
            bird_frame2 = pygame.image.load('assets/images/bird/02.png').convert_alpha()
            bird_frame2 = pygame.transform.rotozoom(bird_frame2, 0, 2.5)
            self.frames = [bird_frame1, bird_frame2]
            y_pos = 280
        else:
            self.enemy_walk = [pygame.image.load('assets/images/enemy/walk/01.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/02.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/03.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/04.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/05.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/06.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/07.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/08.png').convert_alpha(),
                pygame.image.load('assets/images/enemy/walk/09.png').convert_alpha()]
            self.frames = self.enemy_walk
            y_pos = 450
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1200, 1600), y_pos) )
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

pygame.init()
#display
SCREEN_SIZE = (980, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Samurai Runner")
clock = pygame.time.Clock()
font = pygame.font.Font('assets/font/Font.ttf', 40)
running = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('assets/music.mp3')
bg_music.set_volume(0.4)
bg_music.play(loops = -1)

#Groups
samurai = pygame.sprite.GroupSingle()
samurai.add(Samurai())
obstacle_group = pygame.sprite.Group()

#bg display and ground
background_surf = pygame.image.load('assets/bg.png').convert()
background_surf = pygame.transform.scale(background_surf, SCREEN_SIZE)
game_over_surf = pygame.image.load('assets/gameoverbg.png').convert()
game_over_surf = pygame.transform.scale(game_over_surf, SCREEN_SIZE)
ground_surf = pygame.image.load('assets/ground.png').convert()
tile_surf = pygame.image.load('assets/gamestart_tile.png').convert_alpha()
tile_rect = tile_surf.get_rect(center = (SCREEN_SIZE[0] //2 - 3, 470))

#intro screen
samurai_idle_surf = pygame.image.load('assets/images/samurai/idle/01.png').convert_alpha()
samurai_idle_surf_rect = samurai_idle_surf.get_rect(center = (SCREEN_SIZE[0] //2 - 25, SCREEN_SIZE[1] //2))
samurai_idle_surf_scaled = pygame.transform.rotozoom(samurai_idle_surf,0, 2)
samurai_dead_surf = pygame.image.load('assets/images/samurai/dead/02.png').convert_alpha()
samurai_dead_surf = pygame.transform.rotozoom(samurai_dead_surf,0, 2)
samurai_dead_surf_rect = samurai_dead_surf.get_rect(center = (SCREEN_SIZE[0] //2 - 15, SCREEN_SIZE[1] //2 + 65))
game_name = font.render('Samurai Runner',False, 'Black')
game_name_rect = game_name.get_rect(center = (SCREEN_SIZE[0] //2, 100))
game_message = font.render('Press enter to run',False,'Black')
game_message_rect = game_message.get_rect(center = (SCREEN_SIZE[0] //2, 150))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  #trigger this timer every 900 milisecond

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 150)

bird_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bird_animation_timer, 200)

while True:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if running : 
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird', 'enemy', 'enemy', 'enemy'])))
        else:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN ):
                running = True
                start_time = int(pygame.time.get_ticks()/1000)
                # if randint(0,2):    #gives 0/1 as output -> if 1 : enemy
                #     obstacle_rect_list.append(enemy_surf.get_rect(bottomright = (randint(1200, 1600), 450)))
                # else:   #if 0 : bird
                #     obstacle_rect_list.append(bird_surf.get_rect(bottomright = (randint(1200, 1600), 280)))
            
            # if event.type == enemy_animation_timer:
            #     enemy_index += 1
            #     if enemy_index >= len(enemy_walk): enemy_index = 0
            #     enemy_surf = enemy_walk[enemy_index]
            # if event.type == bird_animation_timer:
            #     if bird_index == 0 : bird_index = 1
            #     else: bird_index = 0
            #     bird_surf = bird_fly[bird_index]


    #logic        
    if running :
        screen.blit(background_surf, (0,0))
        screen.blit(ground_surf, (0,450))
        score = display_score()

        samurai.draw(screen)
        samurai.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        running = collision_sprite()
        
        #enemy
        # enemy_rect.x -=6
        # if enemy_rect.right < 0: enemy_rect.left = 980
        # screen.blit(enemy_surf,enemy_rect)
        
        #obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)  
        # if event.type == obstacle_timer:
            # obstacle_rect_list.append(enemy_surf.get_rect(bottomright = (randint(900, 1100), 450)))
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        #player
        # samurai_gravity += 1
        # samurai_rect.y += samurai_gravity
        # if samurai_rect.bottom >= 450 : samurai_rect.bottom = 450
        # samurai_animation()
        # screen.blit(samurai_surf,samurai_rect)

        # running = collisions(samurai_rect, obstacle_rect_list)

        
    #after game over
    else:
        screen.blit(game_over_surf, (0,0))
        screen.blit(samurai_dead_surf, samurai_dead_surf_rect)
        screen.blit(tile_surf, tile_rect)
        score_message = font.render(f'Your Score was: {score}', True, 'Black')
        score_message_rect = score_message.get_rect(center = (SCREEN_SIZE[0] //2, 100))
        screen.blit(game_message, game_message_rect)
        if score == 0:  #starting screen
            start_bg = pygame.image.load('assets/gamestartbg.png').convert_alpha()
            start_bg = pygame.transform.scale(start_bg, SCREEN_SIZE)
            screen.blit(start_bg, (0,0))
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(tile_surf, tile_rect)
            screen.blit(samurai_idle_surf_scaled, samurai_idle_surf_rect)
        else:
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)

#quit
pygame.quit()
exit()