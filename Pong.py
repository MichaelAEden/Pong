import random
from pygame import *
import pygame.gfxdraw
import pygame.locals

HORIZONTAL = 0
VERTICAL = 1

UP = 10
DOWN = 11
LEFT = 5
RIGHT = 6

NO_WIN = 2
PLAYER = 3
COMPUTER = 4

EASY = 12
MEDIUM = 13
HARD = 14

DIFFICUlTY = EASY

WHITE = 255,255,255
GREEN = 50,255,50
BLACK = 0,0,0

def main():
        #Initializes window
        width = 800
        height = 400
        window = Window("Pong", width, height)
        table = Table(width, height)
        #Loops until the space bar is pressed
        while (1):
            window.update()
            if (window.getInput().shouldQuit()):
                pygame.display.quit()
                #sys.exit(0)
            table.update(window)
            window.clear()
            table.draw(window)
            window.render()
            pygame.time.delay(5)


class Input:
    def __init__(self):
        pygame.key.set_repeat(15, 15)    #A key held down will generate multiple events
        return

    #Updates the list of events
    def update(self):
        self.events = pygame.event.get()
        
    #Returns true if the given key is down
    def keyDown(self, key):
        keys = pygame.key.get_pressed()
        if (keys[key]):
            return True
        return False
        
    def shouldQuit(self):
        if (self.keyDown(K_q)):
            return True
        for event in self.events:
            if (event.type == QUIT):
                return True
        return False

    #Returns the coordinates of the entry clicked on
    def getMouseEntry(self):
        return



class Window:
    #Creates a window given a title, width, and height
    def __init__(self, title, width, height):
        self.screen = pygame.display.set_mode(width, height)
        pygame.display.set_caption(title)
        pygame.init()
        surface = pygame.Surface((width, height))
        
        self.width = width
        self.height = height
        self.input = Input()
        
    def update(self):
        self.input.update()
    
    #Clears the screen
    def clear(self):
        self.screen.fill(BLACK)
        
    def render(self):
        pygame.display.update()

    #Displays text in the window, centred at given coordinates
    def displayText(self, screen, text, x, y):
        font = pygame.font.Font(None, 35)
        fontImage = font.render(text, 1, WHITE)
        screen.blit(fontImage, (x - fontImage.get_rect().width / 2, y - fontImage.get_rect().height / 2))
 
    def getInput(self):
        return self.input
    def getScreen(self):
        return self.screen
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height



class Ball:
    #Relative to table, not to window
    #Centre of the ball
    def __init__(self, table):
        self.xVel = 7
        self.yVel = 7
        self.radius = 20
        self.centre(table)
 
    #Updates ball movement
    def update(self, table, playerLeft, playerRight):
        #Updates position
        self.x += self.xVel
        self.y += self.yVel
        self.checkCollision(playerLeft)
        self.checkCollision(playerRight)
        #Updates collision for horizontal walls, not vertical walls because the table would have detected that a win has occurred
        if ((self.y + self.radius) >= table.getHeight() or (self.y - self.radius) <= 0):
            self.bounce(VERTICAL, None)

    #Checks if the ball collides with the provided paddle
    def checkCollision(self, player):
        if (self.y >= player.getY() and self.y <= player.getY() + player.getPaddleHeight()):
            if (self.x + self.radius >= player.getX() and
                self.x - self.radius <= player.getX() + player.getPaddleWidth()):
                self.bounce(HORIZONTAL, player)
                self.xVel += player.getXVel()
        if (self.x >= player.getX() and self.x <= player.getX() + player.getPaddleWidth()):
            if (self.y + self.radius >= player.getY() and
                self.y - self.radius <= player.getY() + player.getPaddleHeight()):
                self.bounce(VERTICAL, player)
                self.yVel += player.getYVel()

    #Called when the ball hits any boundary; NOTE: direction indicates direction of bounce
    def bounce(self, direction, player):
        if (player == None):
            if (direction == HORIZONTAL):
                self.xVel *= -1
            elif (direction == VERTICAL):
                self.yVel *= -1
        else:
            if (direction == HORIZONTAL):
                self.xVel = (player.getXVel() - self.xVel)
                if (self.xVel > 0):     #Only possible if the ball bounced off the right side
                    self.x = player.getX() + player.getPaddleWidth() + self.radius
                elif (self.xVel < 0):    #Only possible if the ball bounced off the left side
                    self.x = player.getX() - self.radius
            elif (direction == VERTICAL):
                self.yVel = (player.getYVel() - self.yVel)
                if (self.yVel > 0):
                    self.y = player.getY() + player.getPaddleHeight() + self.radius
                elif (self.yVel < 0):
                    self.y = player.getY() - self.radius

    #Returns the ball to the centre of the table
    def centre(self, table):
        self.x = table.getWidth() / 2
        self.y = table.getHeight() / 2

    #Draws the ball
    def draw(self, screen):
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), self.radius, GREEN)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), self.radius, GREEN)

    def setSpeed(self, xVel, yVel):
        self.xVel = xVel
        self.yVel = yVel
    def getRadius(self):
        return self.radius
    def getX(self):
        return self.x
    def getY(self):
        return self.y



#Note this class is used by both the user and the AI
class Player:
    #Initializes the paddle on the given side
    def __init__(self, table, side):
        self.score = 0
        self.paddleWidth = 20
        self.paddleHeight = 75
        self.accel = 1.75         #Amount paddle accelerates when a key is pressed
        self.decelConst = 0.85    #Rate at which player decelerates
        self.xVel = 0
        self.yVel = 0
        self.side = side
        
        #Establishes boundaries which the paddle cannot cross
        if (side == LEFT):
            self.xConstraint = table.getGoalIndent() - self.paddleWidth
        else:
            self.xConstraint = table.getWidth() - table.getGoalIndent()
        
        self.x = self.xConstraint
        self.y = table.getHeight() / 2 + self.paddleHeight / 2;
 
    #Updates paddle movement
    def update(self, table):
        #Updates position
        self.x += self.xVel
        self.y += self.yVel
        self.xVel *= self.decelConst
        self.yVel *= self.decelConst
        self.checkBounds(table)
        
    #Called when a goal is scored
    def incrementScore(self, amount):
        self.score += amount
        
    #Sets the height of the paddle
    def setPosition(self, y, table):
        self.y = y
        self.checkBounds(table)
        
    #accels the paddle in the given direction
    def accelPaddle(self, direction, table):
        if (direction == UP):
            self.yVel -= self.accel
        elif (direction == DOWN):
            self.yVel += self.accel
        elif (direction == LEFT):
            self.xVel -= self.accel
        elif (direction == RIGHT):
            self.xVel += self.accel
        self.checkBounds(table)
        
    #Keeps the paddle within the confines of the table
    def checkBounds(self, table):
        if (self.y + self.paddleHeight > table.getHeight()):
            self.y = table.getHeight() - self.paddleHeight
        if (self.y < 0):
            self.y = 0
        if (self.side == LEFT):
            if (self.x < 0):
                self.x = 0
            if (self.x > self.xConstraint):
                self.x = self.xConstraint

    #Draws the paddle
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.paddleWidth, self.paddleHeight), 0)

    def getScore(self):
        return self.score
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getXVel(self):
        return self.xVel
    def getYVel(self):
        return self.yVel
    def getPaddleWidth(self):
        return self.paddleWidth
    def getPaddleHeight(self):
        return self.paddleHeight



#The AI class
class Opponent:
    #Moves the paddle to track the ball
    def movePaddle(self, player, table, ball):
        #As ball gets farther from paddle, paddle becomes more likely to track ball
        if (abs(player.getY() + player.getPaddleHeight() / 2 - ball.getY()) > random.randrange(0, 10)):
            if (player.getY() - ball.getY() > 0):
                player.accelPaddle(UP, table)
            elif (player.getY() - ball.getY() < 0):
                player.accelPaddle(DOWN, table)



class Table:
    #Initializes a table of given width and height
    def __init__(self, width, height):
        self.pointWon = False
        self.width = width
        self.height = height
        self.goalIndent = 180     #Distance from each paddle's farthest side to the adjacent wall
        self.ball = Ball(self)
        self.playerLeft = Player(self, LEFT)   #Paddle controlled by the user
        self.playerRight = Player(self, RIGHT) #Paddle controlled by the computer
        self.computer = Opponent()   #AI which controls the paddle
   
    #Updates the table, including
    # - ball motion
    # - computer paddle movement
    # - player paddle movement
    def update(self, window):
        #Updates user input
        if (window.getInput().keyDown(K_w)):
            self.playerLeft.accelPaddle(UP, self)
        if (window.getInput().keyDown(K_s)):
            self.playerLeft.accelPaddle(DOWN, self)
        if (window.getInput().keyDown(K_a)):
            self.playerLeft.accelPaddle(LEFT, self)
        if (window.getInput().keyDown(K_d)):
            self.playerLeft.accelPaddle(RIGHT, self)
        
        self.computer.movePaddle(self.playerRight, self, self.ball)
        self.playerLeft.update(self)
        self.playerRight.update(self)
        
        if (window.getInput().keyDown(K_SPACE) and self.pointWon):
            self.ball.setSpeed(7, 7)
            self.pointWon = False
        if (self.checkForWin()):    #If a player won, reset the ball in the middle
            self.ball.centre(self)
            self.ball.setSpeed(0, 0)
            self.pointWon = True
        else:
            self.ball.update(self, self.playerLeft, self.playerRight)

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

    #Draws all elements of the table (paddles, ball, score)
    def draw(self, window):
        self.ball.draw(window.getScreen())
        self.playerLeft.draw(window.getScreen())
        self.playerRight.draw(window.getScreen())
        self.drawBoundaryLine(window, window.getWidth() / 2)
        self.drawBoundaryLine(window, self.goalIndent)
        self.drawBoundaryLine(window, window.getWidth() - self.goalIndent)
        window.displayText(window.getScreen(),
                           str(self.playerLeft.getScore()) + " - " +
                           str(self.playerRight.getScore()),
                           window.getWidth() / 2, window.getHeight() / 5)
        
    #Draws dotted line at given x-position which marks some boundary (i.e., goal line or centre line)
    def drawBoundaryLine(self, window, position):
        segments = 20
        for y in range (0, segments, 2):
            pygame.draw.line(window.getScreen(), GREEN, (position, y * window.getHeight() / segments), (position, (y + 1) * window.getHeight() / segments), 5)

    def getGoalIndent(self):
        return self.goalIndent
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height



main()
