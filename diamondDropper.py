import pygame
import keyboard
from main import gamedef
pygame.mixer.init()
pygame.init()

    # Arrays
colours = [(155, 0, 150), (105, 0, 100), (255, 255, 255), (0,0,0)]
btnSizes = [170, 100]

# Load images
startImage = pygame.image.load('PlayButtonAsset.jpg')
exitImage = pygame.image.load('ExitButtonAsset.jpg')
bgImage = pygame.image.load('resizedbg.png')
lvl1Image = pygame.image.load('Level 1 Demo.jpg')

# Setting game window dimensions
imageW = bgImage.get_width()
imageH = bgImage.get_height()

screenW = imageW
screenH = imageH
startScreen = pygame.display.set_mode((screenW, screenH))

startImageSize = (screenW//7, screenH //7 + 10)
exitImageSize = startImageSize

# Resize images
startImage = pygame.transform.scale(startImage, startImageSize)
exitImage = pygame.transform.scale(exitImage, exitImageSize)
lvl1Image = pygame.transform.scale(lvl1Image, (screenW, screenH))
pygame.display.set_caption('Minion Dash')

textFont = pygame.font.SysFont('Arial Bold', 90)
titleText = textFont.render('Title', True, colours[2])
titleTextRect = titleText.get_rect(center=(screenW // 2, 100))

# Button Variables
startBtnPos = (screenW//2 - 400 , screenH - startImage.get_height() - 50)
exitBtnPos = (screenW//2 +200, screenH - exitImage.get_height() - 50)

playsound = pygame.mixer.Sound('buttonPressed.mp3')
bgmusic = pygame.mixer.music.load('bgmusic.mp3')
# Button Function
def startGame():
    print("Start button pressed!")
    pygame.mixer.Sound.play(playsound)
    #pygame.mixer.music.play
    #level1Screen.blit(lvl1Image, (0, 0))
    game1 = Game1()
    game1.run()


def exitButtonPressed():
    print("Exit button pressed!")
    pygame.quit()

backgroundimg = pygame.image.load('greenbg.png')
playerImg = pygame.image.load('MinionCharacter.png')
scoreSFX = pygame.mixer.Sound('caching.mp3')
class Game1:
    def __init__(self):
        self.level1Screen = pygame.display.set_mode((screenW, screenH))
        pygame.display.set_caption("Level 1")
        self.backgroundimg = pygame.image.load('plinko.png')
        self.backgroundimg = pygame.transform.scale(backgroundimg, (screenW, screenH))
        pygame.display.set_caption('Minion Dash')
        playersize = [50]
        self.playerImg = pygame.image.load('minionballplayer.png')
        self.playerImg = pygame.transform.scale(playerImg, (playersize[0], playersize[0]))
        self.playerX = (screenW//2)
        self.playerY = 10
        self.playerX_chng = 0
        self.playerY_chng = 0

        self.score = 0

        #text
        self.font = pygame.font.SysFont('Arial Bold', 50)  # Font size can be adjusted
        self.textColor = colours[3] # White color

    def updateScore(self):
        self.text = self.font.render(f'Score:  {self.score}', True, self.textColor)
        self.textRect = self.text.get_rect(topleft=(20, 20))  # Position at top-left corner


    def player(self, x, y):
        self.level1Screen.blit(self.playerImg, (x, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if keyboard.is_pressed('esc'):
                    running = False

                speed = 2

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.playerX_chng = -speed
                        print("left")
                    if event.key == pygame.K_d:
                        self.playerX_chng = speed
                        print("right")
                    if event.key == pygame.K_w:
                        self.playerY_chng = -speed
                        print("up")
                    if event.key == pygame.K_s:
                        self.playerY_chng = speed
                        print("down")
                    if event.key == pygame.K_p:
                        self.score += 1  # Increase the score
                        print(f"Score updated: {self.score}")
                        pygame.mixer.Sound.play(scoreSFX)


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        self.playerX_chng = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.playerY_chng = 0

            # Player movement
            self.playerX += self.playerX_chng
            if self.playerX <= 0:
                self.playerX = 0
            elif self.playerX >= 768:
                self.playerX = 768
            self.playerY += self.playerY_chng
            if self.playerY <= 0:
                self.playerY = 0
            elif self.playerY >= 768:
                self.playerY = 768

            self.updateScore()

                        # Drawing everything
            self.level1Screen.fill((130, 100, 20))
            self.level1Screen.blit(self.backgroundimg, (0, 0))
            self.player(self.playerX, self.playerY)
            self.level1Screen.blit(self.text, self.textRect)
            pygame.display.update()

        pygame.quit()

# Main game loop
running = True
while running:
    # Mouse positions
    mPos = pygame.mouse.get_pos()
    mClick = pygame.mouse.get_pressed()

    pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Drawing everything
    startScreen.blit(bgImage, (0, 0))  # Draw the background image first
    #startScreen.blit(titleText, titleTextRect)  # Draw the title text on top
    startScreen.blit(startImage, startBtnPos)  # Draw the start button image
    startScreen.blit(exitImage, exitBtnPos)  # Draw the exit button image

    #M clicks are within the button images
    startBtnRect = pygame.Rect(startBtnPos, (startImage.get_width(), startImage.get_height()))
    exitBtnRect = pygame.Rect(exitBtnPos, (exitImage.get_width(), exitImage.get_height()))

    if startBtnRect.collidepoint(mPos):
        startBtnPos = (screenW // 2 - 400, screenH - startImage.get_height() - 45)
        if mClick[0]:
            gamedef()
    else:
        startBtnPos = (screenW // 2 - 400, screenH - startImage.get_height() - 50)

    if exitBtnRect.collidepoint(mPos):
        exitBtnPos = (screenW // 2 + 200, screenH - exitImage.get_height() - 45)
        if mClick[0]:
            exitButtonPressed()
    else:
        exitBtnPos = (screenW // 2 + 200, screenH - exitImage.get_height() -50)


    # Update the display
    pygame.display.update()

    if keyboard.is_pressed('esc'):
        running = False

pygame.quit()
