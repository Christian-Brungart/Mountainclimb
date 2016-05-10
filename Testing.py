# Christian Brungart
# Testing.py
# 4-20-16

import pygame
import random 
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (133, 109, 84)
 
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((150,50))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((81, 255, 0))
class small_gem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 20
        height = 20 
        self.image = pygame.image.load("smallgem.xcf").convert()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
class Gem(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            width = 20
            height = 20
            self.image = pygame.image.load("gem.xcf").convert()
            self.image.set_colorkey(BLACK)
            
            self.rect = self.image.get_rect()
            
            self.change_x = 0
            self.change_y = 0  
        
class Vine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 20
        height = 20
        self.image = pygame.image.load("vine.xcf").convert()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        
        self.change_x = 0
        self.change_y = 0    
    
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        width = 20
        height = 20
        self.image = pygame.image.load("heart.xcf").convert()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
#class for cave
class Cave(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            width = 40
            height = 60
            self.image = pygame.image.load("cave.xcf").convert()
            self.image.set_colorkey(BLACK)
            
            self.rect = self.image.get_rect()
            
            self.change_x = 0
            self.change_y = 0    
            
            self.level = None
class Croc(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 40
        height = 60
        self.image = pygame.image.load("croc.xcf").convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        
        self.change_x = 0
        self.change_y = 0
        
        self.level = None
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 40
        height = 60
        self.image = pygame.image.load("scorpion.xcf").convert()
        self.image.set_colorkey(BLACK)
 
        # Get's a reference of the image.
        self.rect = self.image.get_rect()
 
        self.change_x = -2
        self.change_y = 0
 
        # List of sprites it can bump against
        self.level = None        
class Player(pygame.sprite.Sprite):
    """ This class handles how the player
    controls."""
 
    # -- Methods
    def __init__(self):
        """ Constructor """
 
        # Calls the parent
        super().__init__()
 
        # This is where the hero image is loaded
        width = 40
        height = 60
        self.image = pygame.image.load("hero.xcf").convert()
        self.image.set_colorkey(BLACK)
 
        # Set a image reference.
        self.rect = self.image.get_rect()
 
        # Set speed of the player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites the player can bump against
        self.level = None
 
    def update(self):
        """ Moves the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if the player hits anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit.
            
            # Makes sure the player doesn't get stuck on blocks
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if the player hits anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the block.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Creates the effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if the sprite is on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down and see if there's a platform below us.
        # Move down 2 pixels because it doesn't work well if you only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set the speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player movement:
    def go_left(self):
        """ Called when the user hits the left button. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right button. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user takes their hand off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an list of 5 numbers like what's defined at the top of the
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(BROWN)
 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    """ This is a class used to define a level.
        Child class's can be made for new levels with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player, if they are implemented in. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        
         
        # Background image
        self.background = None
    def enemy(self, enemy):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.enemy = enemy
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Background drawing code can be put here
        
        
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # List with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 [210, 70, 100, 150]]
 
        # Go through the list above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Mountainclimb")
    
    life_list = []
 
    # Create the player
    player = Player()
    enemy = Enemy()
    croc = Croc()
    cave = Cave()
    smallgem = small_gem()
    croc2 = Croc()
    
    x = 850
    y = SCREEN_HEIGHT - 600
    for i in range(3):
        heart = Heart(x, y)
        x += 50
        life_list.append(heart)
    print(life_list)
    lives = pygame.sprite.Group()
    lives.add(life_list)
    
    gem2 = []
    
    
    vine = Vine()
    gem = Gem()
    
    gem2.append(gem)
    gems = pygame.sprite.Group()
    gems.add(gem2)
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
    level_list.append( Level_01(enemy) )
    level_list.append( Level_01(croc) )
    level_list.append( Level_01(cave) )
    level_list.append( Level_01(heart) )
    level_list.append( Level_01(vine) )
    level_list.append( Level_01(gem)  )
    level_list.append( Level_01(smallgem) )
    level_list.append( Level_01(croc2) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    small_gem_list = pygame.sprite.Group()
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 500
    player.rect.y = SCREEN_HEIGHT - 100
    
    enemy.rect.x = 200
    enemy.rect.y = SCREEN_HEIGHT - 290
    active_sprite_list.add(player)
    active_sprite_list.add(enemy)
     
    croc.rect.x = 100
    croc.rect.y = SCREEN_HEIGHT - 75
    active_sprite_list.add(croc)
    
    croc2.rect.x = 600
    croc2.rect.y = SCREEN_HEIGHT - 75
    active_sprite_list.add(croc2)
    
    cave.rect.x = 605
    cave.rect.y = SCREEN_HEIGHT - 450
    active_sprite_list.add(cave)
    
    vine.rect.x = 280
    vine.rect.y = SCREEN_HEIGHT - 450
    active_sprite_list.add(vine)
    
    gem.rect.x = 155
    gem.rect.y = SCREEN_HEIGHT - 570
    active_sprite_list.add(gem)
    
    smallgem.rect.x = 800
    smallgem.rect.y = SCREEN_HEIGHT - 600  
    # Close button loop.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    background_image = pygame.image.load("tropical.jpg").convert()
    # --- Main Program Loop ---
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()           
 
        # Update the player.
        active_sprite_list.update()
        small_gem_list.update()

 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        # This keeps the player from going off screen
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, do the same
        if player.rect.left < 0:
            player.rect.left = 0
 
        # All drawing code should go BELOW THIS
        screen.blit(background_image, [0,0])
        active_sprite_list.draw(screen)
        current_level.draw(screen)
        lives.draw(screen)
        small_gem_list.draw(screen) 
        #scorpion movement
        enemy.rect.left += 0
        if enemy.rect.right > 0:
            enemy.rect.x += enemy.change_x
            if enemy.rect.x > 370:
                enemy.change_x = -(enemy.change_x)
            if enemy.rect.x < 180:
                enemy.change_x = 2
        
        # croc movement
        croc.rect.left += 0
        if croc.rect.right > 0:
            croc.rect.x += 5
            if croc.rect.x > SCREEN_WIDTH:
                croc.rect.x = -20
                
        croc2.rect.left += 0
        if croc2.rect.right > 0:
            croc2.rect.x += 5
            if croc2.rect.x > SCREEN_WIDTH:
                croc2.rect.x = -20        
                
        # the player collecting the gem
        
        collect = pygame.sprite.spritecollide(player, gems, True)
        if collect:
            gems.remove(gem2)
            gem2.pop()
            gems.add(gem2)
            gems.update()       
            small_gem_list.add(smallgem)
        
        
            
        vine_list = pygame.sprite.Group()
        vine_list.add(vine)
        if pygame.sprite.spritecollide(player, vine_list, False):
            player.change_y = -4
            player.rect.y += player.change_y  
            
        # If the player is hit        
        enemy_list = pygame.sprite.Group()
        enemy_list.add(croc)
        enemy_list.add(enemy)
        enemy_list.add(croc2)
        if pygame.sprite.spritecollide(player, enemy_list, False):
            lives.remove(life_list)
            life_list.pop()
            lives.add(life_list)
            player.rect.x = 500
            player.rect.y = 425
            lives.update()
            if len(lives) == 0:
                done = True
        
        #If the player reaches the goal
        cave_list = pygame.sprite.Group()
        cave_list.add(cave)
        victory = pygame.sprite.spritecollide(player, cave_list, False)       
    
        if victory:
            font = pygame.font.Font(None,36)
            text = font.render("You Win", 0, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            background.blit(text, textpos)
            screen.blit(background, (450, 300))
            player.change_x = 0
            player.change_y = 0    

        # All drawing code should go ABOVE THIS
 
        # Limit to 60 fps
        clock.tick(60)
 
        # Updates and draws the screen.
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()