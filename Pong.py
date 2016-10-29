from pygame import *
import pygame.gfxdraw
import pygame.locals

HORIZONTAL = 0
VERTICAL = 1

LEFT = 5
RIGHT = 6

NO_WIN = 2
PLAYER = 3
COMPUTER = 4

GREEN = 50,255,50
BLACK = 0,0,0

def main():
        #Initializes window
        window = Window("Pong", 800, 400)
        table = Table(800, 400)
        
        #Loops until the player quits
        while (1):
            window.update()
            
            if (window.getInput().shouldQuit()):
                pygame.display.quit()
                sys.exit(0)
            
            table.update(window)
            
            window.clear()
            table.draw(window)
            window.render()
            
            pygame.time.delay(5)



#Handles all player input
class Input:
    def __init__(self):
        pygame.key.set_repeat(15, 15)    #A key held down will generate multiple events
        return
    
    #Updates the list of events
    def update(self):
        self.events = pygame.event.get()
    
    #Returns true if the given key is down
    def keyDown(self, key):
        for event in self.events:
            if (event.type == KEYDOWN and event.key == key):
                return True
        return False
    
    #Returns true if the game should quit (if the space bar has been pressed or the window has been closed)
    def shouldQuit(self):
        for event in self.events:
            if (event.type == QUIT or self.keyDown(K_SPACE)):
                return True
        return False



class Window:
    #Creates a window given a title, width, and height
    def __init__(self, title, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        pygame.init
        surface = pygame.Surface((width, height))
        
        self.width = width
        self.height = height
        self.input = Input()
    
    #Updates the input object
    def update(self):
        self.input.update()
        
    #Fills the screen with background colour
    def clear(self):
        self.screen.fill(BLACK)
        
    #Renders everything drawn to the screen
    def render(self):
        pygame.display.update()
    
    #Displays text at given coordinates (NOT CURRENTLY WORKING)
    def displayText(self, text, x, y):
        return
        #font = pygame.font.Font(None, 35)
        #fontImage = font.render("Test", 1, GREEN)
        #screen.blit(fontImage(x, y))
    
    def getInput(self):
        return self.input
    def getScreen(self):
        return self.screen
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height



class Ball:
    def __init__(self, table):
        self.radius = 10
        self.xVelocity = 7
        self.yVelocity = 7
        self.centre(table)
    
    #Updates ball movement
    def update(self, table, playerLeft, playerRight):
        #Updates position
        self.x += self.xVelocity
        self.y += self.yVelocity
        
        #Updates collision with walls and paddles
        if ((self.y + self.radius) >= table.getHeight() or (self.y - self.radius) <= 0):
            self.bounce(VERTICAL)
        if (self.x + self.radius >= table.getWidth() - table.getGoalIndent() and self.y >= playerRight.getY() and self.y <= (playerRight.getY() + playerRight.getPaddleHeight())):
            self.bounce(HORIZONTAL)
        if (self.x - self.radius <= table.getGoalIndent() and self.y >= playerLeft.getY() and self.y <= (playerLeft.getY() + playerLeft.getPaddleHeight())):
            self.bounce(HORIZONTAL)
    
    #Draws the ball
    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), self.radius, GREEN)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), self.radius, GREEN)
    
    #Called when the ball hits any boundary, where direction indicates direction of bounce
    def bounce(self, direction):
        if (direction == HORIZONTAL):
            self.xVelocity *= -1
        if (direction == VERTICAL):
            self.yVelocity *= -1
    
    #Sets the ball in the centre of the table
    def centre(self, table):
        self.x = table.getWidth() / 2
        self.y = table.getHeight() / 2
    
    def getRadius(self):
        return self.radius
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    #NOT CURRENTLY WORKING
    def setSpeed(self, speed):
        return



#Players, including paddle and score
#Note this class is used by both the user and the AI
class Player:
    #Initializes the paddle on the left or right side of the table
    def __init__(self, table, side):
        self.score = 0
        
        self.paddleWidth = 20
        self.paddleHeight = 75
        
        #Positions paddle
        if (side == LEFT):
            self.x = table.getGoalIndent() - self.paddleWidth
        else:
            self.x = table.getWidth() - table.getGoalIndent()
        self.y = table.getHeight() / 2 + self.paddleHeight / 2;
        
    #Draws the paddle
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.paddleWidth, self.paddleHeight), 0)
        
    #Keeps the paddle within the confines of the table
    def checkBounds(self, table):
        if (self.y + self.paddleHeight > table.getHeight()):
            self.y = table.getHeight() - self.paddleHeight
        if (self.y < 0):
            self.y = 0
    
    #Sets the height of the paddle
    def setPosition(self, y, table):
        self.y = y
        self.checkBounds(table)
    
    #Moves the paddle up or down
    def movePaddle(self, height, table):
        self.y += height
        self.checkBounds(table)

    #Called when a goal is scored
    def incrementScore(self, amount):
        self.score += amount
    
    def getScore(self):
        return self.score
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getPaddleWidth(self):
        return self.paddleWidth
    def getPaddleHeight(self):
        return self.paddleHeight



#The AI class
class Opponent:
    #Moves the paddle to track the ball, NEEDS MORE WORK
    def movePaddle(self, player, table, ball):
        player.setPosition(ball.getY() - player.getPaddleHeight() / 2, table)



class Table:
    #Initializes a table of given width and height
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.goalIndent = 50      #Distance from each paddle's farthest side to the adjacent wall
        self.paddleMovement = 10  #Amount paddle moves when a player moves it
        
        self.ball = Ball(self)
        self.playerLeft = Player(self, LEFT)   #Paddle controlled by the user
        self.playerRight = Player(self, RIGHT) #Paddle controlled by the computer
        self.computer = Opponent()             #AI which controls the right paddle
        
    #Updates the table, including ball motion and paddle movement
    def update(self, window):
        #Updates user input
        if (window.getInput().keyDown(K_w)):
            self.playerLeft.movePaddle(-self.paddleMovement, self)
        elif (window.getInput().keyDown(K_s)):
            self.playerLeft.movePaddle(self.paddleMovement, self)
        
        #If a player won, reset the ball in the middle
        if (self.checkForWin()):    
            self.ball.centre(self)
            self.ball.setSpeed(0)
        else:
            self.ball.update(self, self.playerLeft, self.playerRight)
        
        self.computer.movePaddle(self.playerRight, self, self.ball)
        
    #Draws all elements of the table (paddles, ball, score)
    def draw(self, window):
        self.ball.draw(window.getScreen())
        self.playerLeft.draw(window.getScreen())
        self.playerRight.draw(window.getScreen())
        window.displayText(str(self.playerLeft.getScore()) + " - " +
                           str(self.playerRight.getScore()),
                           int(window.getWidth() / 2), int(window.getHeight() / 5))
        
    #Checks if any player has scored a point, and awards a point to that player
    #Returns true if a point has been scored
    def checkForWin(self):
        if ((self.ball.getX() + self.ball.getRadius()) < 0):
            self.playerLeft.incrementScore(1)
            return True
        if ((self.ball.getX() - self.ball.getRadius()) > self.width):
            self.playerRight.incrementScore(1)
            return True
        return False
    
    def getGoalIndent(self):
        return self.goalIndent
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height



main()
