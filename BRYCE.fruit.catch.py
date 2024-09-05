#########################################
# Bryce Orchard
# 04/04/2023
# game of Fruit Catch
#########################################

import pygame
import random
import time

# Setup pygame and game objects
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680
TIME_LIMIT = 31
BTN_SIZE = 2
FRUIT_SIZE = 40
BASKET_HEIGHT = (502/600) * 75

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED, vsync=1)
# Vsync works for my laptop, but it may not work on other machines, however it makes the game
# way more smoother
pygame.display.set_caption("Fruit Catch")
background = pygame.Surface(screen.get_size())

def load_image(file, width, height):
    """Loads an image from a file and scales it to the given width and height."""
    image = pygame.image.load(file)
    return pygame.transform.scale(image, (width, height))

FONT = pygame.font.SysFont('Arial', 16, True)
IMAGES = {"Apple": load_image("images/apple.png", FRUIT_SIZE, FRUIT_SIZE),
          "Basket": load_image("images/basket.png", 75, BASKET_HEIGHT),
          "Cherry": load_image("images/cherry.png", FRUIT_SIZE, FRUIT_SIZE),
          "Pear": load_image("images/pear.png", FRUIT_SIZE, FRUIT_SIZE),
          "Background": load_image("images/background.jpeg", SCREEN_WIDTH, SCREEN_HEIGHT)}

class Game():
    def __init__(self):
        self.score = 0
        self.fruits = []
        
    def spawn_fruit(self):
        if len(self.fruits) <= 6:
            # Checks if there are less than or equal to 6 fruits on screen
            random_fruit = random.choice(('Apple', 'Cherry', 'Pear'))
            position = random.randint(5, 1275)
            fruit = Fruit(random_fruit, position)
        
            self.fruits.append(fruit)
        
    def move_fruits(self):
        for fruit in self.fruits:
            if fruit.y < SCREEN_HEIGHT:
                # Checks if the fruit is not off the screen
                fruit.y += fruit.speed * dt
            else:
                self.fruits.remove(fruit)

    def catch(self, basket):
        basket_rect = IMAGES['Basket'].get_rect(topleft = (basket.x, basket.y))
        
        for fruit in self.fruits:
            # Creates a rectangle for the fruit images and basket
            fruit_rect = IMAGES[fruit.kind].get_rect(topleft = (fruit.x, fruit.y))
            
            if fruit_rect.colliderect(basket_rect):
                # Checks collision
                self.score += fruit.points
                self.fruits.remove(fruit)
                # Remove the caught fruit from the list of fruits on screen
                break
    
    def render(self, basket):
        counter = int(abs((time.time() - start_time) - TIME_LIMIT))
        # Counting down from the time limit
        if len(str(counter)) < 2:
            counter = f"0{counter}"
            # Adds a zero in front of a single digit
            
        text_score = FONT.render(f"Score: {self.score} / 100", True, (255,255,255))
        text_timer = FONT.render(f"Timer: {counter}", True, (255,255,255))
        
        screen.blit(IMAGES['Background'], (0, 0))
        
        for fruit in self.fruits:
            image = IMAGES[fruit.kind]
            screen.blit(image, (fruit.x, fruit.y))
        # Render fruits
        screen.blit(IMAGES["Basket"], (basket.x, basket.y))
        # Render basket
        screen.blit(text_score, (10, 10))
        screen.blit(text_timer, (SCREEN_WIDTH - (text_timer.get_rect().width) - 10, 10))
        # Render score and timer
        
class Basket():
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT - (SCREEN_HEIGHT/10)
        # Sets basket height to a tenth from the bottom
    
    def move_basket(self, direction: str):
        """Moves the basket in the specified direction"""
        if self.x > 10:
            if direction == "left":
                self.x = max(0, (self.x-510 * dt))
                # Prevents going past the left edge of the screen
        if self.x < SCREEN_WIDTH - 85:   
            # Width of basket is 75    
            if direction == "right":
                self.x = min((self.x+510 * dt), 1280)
                # Prevents going past the right edge of the screen

class Fruit():
    def __init__(self, kind, x):
        self.kind = kind
        
        if kind == "Apple":
            self.speed = 270
            self.points = 1
        elif kind == "Cherry":
            self.speed = 450
            self.points = 3
        elif kind == "Pear":
            self.speed = 550
            self.points = 7
        # Speeds are large because of dt
        self.x = x
        self.y = 0 - (IMAGES[kind].get_rect().height)
        # Spawns fruits off the screen

class Button():
    def __init__(self, dimensions: tuple, font, text, antialiasing, colour):
        """Creates a button with the given dimensions, font, text, and colour \n
           Generates a rectangle with a white border and centers the text within"""
        self.x = 0
        self.y = 0
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])
        self.font = font
        self.text = text
        
        rendered_text = self.font.render(self.text, antialiasing, colour)
        
        text_box = pygame.Surface((self.width, self.height))
        # Create surface
        text_box.fill("black")
        
        outer_border = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(text_box, 'white', outer_border, width=int(self.height/10))
        # Draw border
        
        text_rect = pygame.Rect(rendered_text.get_rect(center = outer_border.center))
        text_box.blit(rendered_text, text_rect)
        # Adds text to surface in the center of the rectangle
        
        self.text_box = text_box
        
    @staticmethod
    def div(btn1, btn2, width):
        """Takes two buttons and a width and puts them on the end of a rectangle of the
           specified width"""
           
        div = pygame.Surface((width, btn1.height))
        div.blit(btn1.text_box, (0, 0))
        # Add leftmost button
        div.blit(btn2.text_box, ((width - btn2.width), 0))
        # Add rightmost button
        return div
    
def gameplay():
    game = Game()
    basket = Basket()
    # I'm using the time module since this function is called multiple times
    # and pygame.get_ticks doesn't work since it starts at pygame.init()
    global dt 
    global start_time
    start_time = time.time()
    # Start game loop
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # UPDATE YOUR GAME HERE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            basket.move_basket("left")
        if keys[pygame.K_d]:
            basket.move_basket("right")
            
        game.move_fruits()
        
        game.catch(basket)
        
        if random.randint(0, 28) == 1:
            game.spawn_fruit() 
        
        # RENDER YOUR GAME HERE

        game.render(basket)

        # flip() the display to update your work on screen
        pygame.display.flip()

        dt = clock.tick(60) / 1000 # limits FPS to 60
        
        if (time.time() - start_time) >= TIME_LIMIT:
            # Switch to end screen after the time limit has passed
            return end_screen(game)
            # If the quit button is pressed, exits the function
        
class End_Screen():
    """Defines the properties of the end screen"""
    
    def __init__(self, game):
        result_font = pygame.font.SysFont('Arial', 40, True)
        btn_font = pygame.font.SysFont('Arial', 20, True)
        
        if game.score < 100:
            self.result_text = result_font.render("You lost :(", True, (255,255,255))
        else:
            self.result_text = result_font.render("You win :)", True, (255,255,255))
        
        btn_quit_size = (btn_font.size('Quit')[0] * BTN_SIZE, btn_font.size('Quit')[1] * BTN_SIZE)
        btn_retry_size = (btn_font.size('Retry')[0] * BTN_SIZE, btn_font.size('Retry')[1] * BTN_SIZE)
        
        self.btn_quit = Button(btn_quit_size, btn_font, 'Quit', True, (255,255,255))
        self.btn_retry = Button(btn_retry_size, btn_font, 'Retry', True, (255,255,255))
        # Create buttons
        
        self.div = Button.div(self.btn_quit, self.btn_retry, 125 * BTN_SIZE)
        # Create div with buttons so as to center them horizontally
        
        self.div_rect = self.div.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        self.btn_quit.x = self.div_rect.left
        self.btn_quit.y = self.div_rect.top
        self.btn_retry.x = self.div_rect.right - self.btn_retry.width
        self.btn_retry.y = self.div_rect.top
        # Updates the button positions according to the div placement
        
    def mouse_pressed(self, button):
        """Checks to see if mouse cursor is within a given button rectangle"""
        
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button.x, button.y, button.width, button.height)

        if pygame.Rect.collidepoint(button_rect, mouse_pos):
            return button.text
        
def end_screen(game):
    """Function to manage the end screen which consists of some text and two buttons"""
    
    end_screen = End_Screen(game)
    running = True
    while running:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # UPDATE YOUR GAME HERE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in (end_screen.btn_quit, end_screen.btn_retry):
                    if end_screen.mouse_pressed(button) == 'Quit':
                        return False
                    # Exits function and quits the main game loop
                    elif end_screen.mouse_pressed(button) == 'Retry':
                        return True
                    # Starts the main game loop again
                    
        # RENDER YOUR GAME HERE
        
        result_center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - (40 * BTN_SIZE)) # 40*BTN_SIZE above the middle of the screen
        screen.blit(end_screen.result_text, end_screen.result_text.get_rect(center = result_center))
        # Display win/loss status
        
        screen.blit(end_screen.div, end_screen.div_rect)
        # Display buttons
        
        # flip() the display to update your work on screen
        pygame.display.flip()

def game():
    """Main game loop which manages the playable game and the final screen"""
    running = True
    while running:
        running = gameplay()
        # gameplay() is false when the quit button is pressed
    pygame.quit()
    
if __name__ == "__main__":
    game()