import sys
import pygame
import time
import random

pygame.init()
pygame.font.init()
fontH1 = pygame.font.SysFont("Cambria", 80)
fontH2 = pygame.font.SysFont("Cambria", 50)
fontP = pygame.font.SysFont("Cambria", 28)
fontPmini = pygame.font.SysFont("Cambria", 18)

gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill((0,0,0))
pygame.display.set_caption("TEST WINDOW")
bg = pygame.Surface((800, 600))
bg.fill((0, 0, 0))
bg = pygame.image.load("imgs/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (800, 600))

class Player():
    def __init__(self):
        self.body = [(220, 190), (250, 190), (280, 190), (310, 190)]
        self.shape = pygame.Surface((30, 30))
        self.shape.fill((0, 255, 0))
        self.head = pygame.Surface((30, 30))
        self.head.fill((0, 200, 0))
        self.dir = "RIGHT"
        self.score = 0

    def move(self):
        if self.dir == "RIGHT":
            self.body.append((self.body[len(self.body)-1][0] + 30 , self.body[len(self.body)-1][1]))
        elif self.dir == "UP":
            self.body.append((self.body[len(self.body)-1][0] , self.body[len(self.body)-1][1] - 30))
        elif self.dir == "DOWN":
            self.body.append((self.body[len(self.body)-1][0] , self.body[len(self.body)-1][1] + 30))
        elif self.dir == "LEFT":        
            self.body.append((self.body[len(self.body)-1][0] - 30 , self.body[len(self.body)-1][1]))
        self.body.pop(0)

    def self_collision(self):
        return self.body[-1] in self.body[0:-1]

    def wall_collision(self):
        return (self.body[-1][0] > gameWindow.width - 20 or 
        self.body[-1][0] < 10 or 
        self.body[-1][1] > gameWindow.height - 30 or 
        self.body[-1][1] < 10)

    def get_longer(self):
        self.body.insert(0, self.body[0])

    def apple_collision_detection(self):
        return (self.body[-1][0] <= (apple.x +int(apple.shape.width) + 2) and #snake x smaller than apple x plus it's physical width
            (self.body[-1][0] + self.shape.width + 2) >= apple.x and #snake and his physical width bigger than apple x
            self.body[-1][1] <= (apple.y + apple.shape.height) and #snake y smaller than apple x and it's height + 5
            (self.body[-1][1] + self.shape.height + 2) >= apple.y) #snake y and his physical height bigger than apple y

    def mine_collision(self):
        for i in mine_list:
            if (self.body[-1][0] < i.x + 30 and 
                self.body[-1][0] + 30 > i.x and 
                self.body[-1][1] < i.y + 30 and 
                self.body[-1][1] + 30 > i.y):
                return True
        return False

player = Player()

class Apple():
    def __init__(self):
        self.x = 190
        self.y = 160
        self.old_x = 190
        self.old_y = 160
        self.prev_x = 190
        self.prev_y = 160
        self.vel_x = 0
        self.vel_y = 0
        self.move_time = 0
        self.dir = 0
        self.shape = pygame.Surface((20, 20))
        self.shape.fill((255, 0, 0))

    def getNewPos(self):
        while True:
            self.x = random.randint(1, 24) * 30 + 15
            self.y = random.randint(1, 18) * 30 + 15
            
            collision = False
            for segment in player.body:
                if (self.x < segment[0] + 30 and self.x + 20 > segment[0] and
                    self.y < segment[1] + 30 and self.y + 20 > segment[1]):
                    collision = True
                    break 

            for i in mine_list:
                if (self.x < i.x + 30 and self.x + 20 > i.x and
                    self.y < i.y + 30 and self.y + 20 > i.y):
                    collision = True
                    break 

            if not collision and (self.x != self.old_x or self.y != self.old_y):
                self.old_x = self.x
                self.old_y = self.y
                break

    def moveIt(self):
        self.dir = random.randint(-4, 4)

    def wall_collision(self):
        if self.x < 25:
            if self.dir == -4:
                self.dir = -self.dir
            elif self.dir == -2:
                self.dir = 1
            elif self.dir == -1:
                self.dir = 2
        elif self.x > gameWindow.width - 55:
            if self.dir == 4:
                self.dir = -self.dir
            elif self.dir == 2:
                self.dir = -1
            elif self.dir == 1:
                self.dir = -2
        elif self.y < 25:
            if self.dir == -3:
                self.dir = -self.dir
            elif self.dir == -2:
                self.dir = -1
            elif self.dir == 1:
                self.dir = 2
        elif self.y > gameWindow.height - 65:
            if self.dir == 3:
                self.dir = -self.dir
            elif self.dir == -1:
                self.dir = -2
            elif self.dir == 2:
                self.dir = 1

    def player_collision(self):
        if self.move_time != 5:
            return False

        next_x = self.x
        next_y = self.y

        match self.dir:
            case -4:  # Left
                next_x -= 30
            case -3:  # Up
                next_y -= 30
            case -2:  # Left up
                next_x -= 30
                next_y -= 30
            case -1:  # Left down
                next_x -= 30
                next_y += 30
            case 0:
                pass
            case 1:   # Right up
                next_x += 30
                next_y -= 30
            case 2:   # Right down
                next_x += 30
                next_y += 30
            case 3:   # Down
                next_y += 30
            case 4:   # Right
                next_x += 30

        for segment in player.body[0:-1]:
            segment_x = segment[0]
            segment_y = segment[1]
            
            if (next_x < segment_x + 30 and next_x + 20 > segment_x and 
                next_y < segment_y + 30 and next_y + 20 > segment_y):
                return True
                
        return False

apple = Apple()

class Mine():
    def __init__(self):
        self.x = None
        self.y = None
        self.old_x = None
        self.old_y = None
        self.body = pygame.Surface((30, 30))
        self.ind = pygame.Surface((15, 15))
        self.body.fill((0, 0, 0))
        self.ind.fill((255, 180, 0))
        self.col_switch = 0

    def getNewPos(self):
        while True:
            self.x = random.randint(1, 24) * 30 + 10
            self.y = random.randint(1, 18) * 30 + 10
        
            collision = False
            for segment in player.body:
                if (self.x < segment[0] + 90 and self.x + 90 > segment[0] and
                    self.y < segment[1] + 90 and self.y + 90 > segment[1]):
                    collision = True
                    break 

            if not collision:
                for segment in mine_list:
                    if segment is self:
                        continue
                    if (self.x < segment.x + 30 and self.x + 30 > segment.x and
                        self.y < segment.y + 30 and self.y + 30 > segment.y):
                        collision = True
                        break

                if not collision:
                    if (self.x < apple.x + 20 and self.x + 30 > apple.x and
                        self.y < apple.y + 20 and self.y + 30 > apple.y):
                        collision = True
        
            if not collision and (self.x != self.old_x or self.y != self.old_y):
                self.old_x = self.x
                self.old_y = self.y
                break

mine_list = []

a = 1
b = 0

clock = pygame.time.Clock()

tickCool = 1

x = 0

chaos = "NO"

moveApples = "NO"

spawnMines = "NO"

moveMines = "NO"

alwaysMoveMines = "NO"

alwaysSpawnMines = "NO"

game_state = 0

def spawnNewMine():
        global x
        if alwaysSpawnMines == "YES" and spawnMines == "YES":
            mine = Mine()
            mine.getNewPos()
            mine_list.append(mine)
            if alwaysMoveMines == "YES":
                for i in mine_list:
                    i.getNewPos()
        else:
            if x + 1 == int(player.score/100) and x + 1 > len(mine_list):
                x += 1
                mine = Mine()
                mine.getNewPos()
                mine_list.append(mine)
                if moveMines == "YES":
                    for i in mine_list:
                        i.getNewPos()

while True:
    clock.tick(10)
    match game_state:
        case 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if a == 1:
                            player.body = [(220, 190), (250, 190), (280, 190), (310, 190)]
                            player.dir = "RIGHT"
                            player.score = 0
                            apple.vel_x = 0
                            apple.vel_y = 0
                            apple.getNewPos()
                            mine_list.clear()
                            x = 0
                            game_state = 1
                        elif a == 2:
                            a = 1
                            game_state = 0.1
                        elif a == 3:
                            pygame.quit()
                            sys.exit(0)
                    elif event.key == pygame.K_DOWN:
                        if a == 3:
                            a = 1
                        else:
                            a += 1
                    elif event.key == pygame.K_UP:
                        if a == 1:
                            a = 3
                        else:
                            a -= 1


        case 0.1:
            for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    if a == 1:
                                        if chaos == "YES":
                                            chaos = "NO"
                                            moveApples = "NO"
                                            spawnMines = "NO"
                                            alwaysMoveMines = "NO"
                                            alwaysSpawnMines = "NO"
                                            moveMines = "NO"
                                        elif chaos == "NO":
                                            chaos = "YES"
                                            moveApples = "YES"
                                            spawnMines = "YES"
                                            alwaysMoveMines = "YES"
                                            alwaysSpawnMines = "YES"
                                            moveMines = "YES"
                                    elif a == 2:
                                        if moveApples == "YES":
                                            moveApples = "NO"
                                        elif moveApples == "NO":
                                            moveApples = "YES"
                                    elif a == 3:
                                        if spawnMines == "YES":
                                            spawnMines = "NO"
                                        elif spawnMines == "NO":
                                            spawnMines = "YES"
                                    elif a == 4:
                                        if moveMines == "YES":
                                            moveMines = "NO"
                                        elif moveMines == "NO":
                                            moveMines = "YES"
                                    elif a == 5:
                                        if alwaysSpawnMines == "YES":
                                            alwaysSpawnMines = "NO"
                                        elif alwaysSpawnMines == "NO":
                                            alwaysSpawnMines = "YES"
                                    elif a == 6:
                                        if alwaysMoveMines == "YES":
                                            alwaysMoveMines = "NO"
                                        elif alwaysMoveMines == "NO":
                                            alwaysMoveMines = "YES"
                                    elif a == 7:
                                        a = 1
                                        game_state = 0
                                elif event.key == pygame.K_DOWN:
                                    if a == 7:
                                        a = 1
                                    else:
                                        a += 1
                                elif event.key == pygame.K_UP:
                                    if a == 1:
                                        a = 7
                                    else:
                                        a -= 1


        case 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
    
                elif event.type == pygame.KEYDOWN:
                    if tickCool == 1:
                        if event.key == pygame.K_LEFT:
                            if player.dir != "RIGHT" and player.dir != "LEFT":
                                player.dir = "LEFT"
                                tickCool = -tickCool
                        elif event.key == pygame.K_RIGHT:
                            if player.dir != "LEFT" and player.dir != "RIGHT":
                                player.dir = "RIGHT"
                                tickCool = -tickCool
                        elif event.key == pygame.K_UP:
                            if player.dir != "DOWN" and player.dir != "UP":
                                player.dir = "UP"
                                tickCool = -tickCool
                        elif event.key == pygame.K_DOWN:
                            if player.dir != "UP" and player.dir != "DOWN":
                                player.dir = "DOWN"
                                tickCool = -tickCool

            player.move()
            if tickCool == -1:
                tickCool = -tickCool
            if moveApples == "YES":
                apple.move_time += 1
            
            if player.apple_collision_detection():
                player.score += 10
                player.get_longer()
                apple.getNewPos()
                if alwaysMoveMines == "YES" and spawnMines == "YES":
                    for i in mine_list:
                        i.getNewPos()
                if alwaysSpawnMines == "YES" and spawnMines == "YES":
                    spawnNewMine()
                if moveApples == "YES":
                    apple.moveIt()
                if player.score > 100:
                    if spawnMines == "YES":
                        spawnNewMine()

            if moveApples == "YES":
                apple.wall_collision()
                apple.player_collision()
                if apple.player_collision():
                    apple.dir = -apple.dir

            if player.self_collision():
                time.sleep(1)
                game_state = 2

            if player.wall_collision():
                time.sleep(1)
                game_state = 2

            if player.mine_collision():
                time.sleep(0.1)
                game_state = 2
    
            
        case 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        a = 1
                        b = 0
                        game_state = 0


    #Drawing

    #Main Menu Drawing
    if game_state == 0:
        if chaos == "YES":
            gameWindow.fill((0, 0, 0))
            welcomeText = fontH1.render("CHAOS SNAKE", True, (255, 0, 0))
            madeByText = fontPmini.render("MADE BY MIROSLAV OREL (jbx505)", True, (255, 0, 0))
            playText = fontP.render("PLAY", True, (255, 0, 0))
            optionsText = fontP.render("SETTINGS", True, (255, 0, 0))
            quitText = fontP.render("QUIT", True, (255, 0, 0))
            selectBox = pygame.Surface((50, 20))
            selectBox.fill((0, 0, 0))
        elif chaos == "NO":
            gameWindow.fill((255, 255, 255))
            welcomeText = fontH1.render("CHAOS SNAKE", True, (0, 0, 0))
            madeByText = fontPmini.render("MADE BY MIROSLAV OREL (jbx505)", True, (0, 0, 0))
            playText = fontP.render("PLAY", True, (0, 0, 0))
            optionsText = fontP.render("SETTINGS", True, (0, 0, 0))
            quitText = fontP.render("QUIT", True, (0, 0, 0))
            selectBox = pygame.Surface((50, 20))
            selectBox.fill((0, 0, 0))

        if a == 1:
            playText = fontP.render("PLAY", True, (255, 255, 255))
            selectBox = pygame.Surface((playText.get_width() + 18, 35))
        elif a == 2:
            optionsText = fontP.render("SETTINGS", True, (255, 255, 255))
            selectBox = pygame.Surface((optionsText.get_width() + 18, 35))
        elif a == 3:
            quitText = fontP.render("QUIT", True, (255, 255, 255))
            selectBox = pygame.Surface((quitText.get_width() + 18, 35))

        gameWindow.blit(welcomeText, ((gameWindow.width - welcomeText.get_width()) // 2, 50))
        gameWindow.blit(madeByText, ((gameWindow.width - madeByText.get_width()) // 2, 135))
        if a == 1:
            gameWindow.blit(selectBox, ((gameWindow.width - playText.get_width()) // 2 - 9, 350))
        elif a == 2:
            gameWindow.blit(selectBox, ((gameWindow.width - optionsText.get_width()) // 2 - 9, 400))
        elif a == 3:
            gameWindow.blit(selectBox, ((gameWindow.width - quitText.get_width()) // 2 - 9, 450))
        gameWindow.blit(playText, ((gameWindow.width - playText.get_width()) // 2, 350))
        gameWindow.blit(optionsText, ((gameWindow.width - optionsText.get_width()) // 2, 400))
        gameWindow.blit(quitText, ((gameWindow.width - quitText.get_width()) // 2, 450))

    #Options Menu Drawing
    elif game_state == 0.1:
        if moveApples == "YES" and spawnMines == "YES" and moveMines == "YES" and alwaysMoveMines == "YES" and alwaysSpawnMines == "YES":
            chaos = "YES"
        else:
            chaos = "NO"
        if chaos == "YES":
            gameWindow.fill((0, 0, 0))
            settingsText = fontH1.render("SETTINGS", True, (255, 0, 0))
            chaosText = fontP.render((f"CHAOS: {chaos}"), True, (255, 0, 0))
            option1Text = fontP.render((f"MOVING APPLES: {moveApples}"), True, (255, 0, 0))
            option2Text = fontP.render((f"SPAWN MINES: {spawnMines}"), True, (255, 0, 0))
            option3Text = fontP.render((f"MOVE MINES: {moveMines}"), True, (255, 0, 0))
            option4Text = fontP.render((f"SPAWN NEW MINE AFTER EVERY APPLE: {alwaysSpawnMines}"), True, (255, 0, 0))
            option5Text = fontP.render((f"MOVE MINES AFTER EVERY APPLE: {alwaysMoveMines}"), True, (255, 0, 0))
            returnText = fontP.render(("BACK"), True, (255, 0, 0))
        elif chaos == "NO":
            gameWindow.fill((255, 255, 255))
            settingsText = fontH1.render("SETTINGS", True, (0, 0, 0))
            chaosText = fontP.render((f"CHAOS: {chaos}"), True, (0, 0, 0))
            option1Text = fontP.render((f"MOVING APPLES: {moveApples}"), True, (0, 0, 0))
            option2Text = fontP.render((f"SPAWN MINES: {spawnMines}"), True, (0, 0, 0))
            option3Text = fontP.render((f"MOVE MINES: {moveMines}"), True, (0, 0, 0))
            option4Text = fontP.render((f"SPAWN NEW MINE AFTER EVERY APPLE: {alwaysSpawnMines}"), True, (0, 0, 0))
            option5Text = fontP.render((f"MOVE MINES AFTER EVERY APPLE: {alwaysMoveMines}"), True, (0, 0, 0))
            returnText = fontP.render(("BACK"), True, (0, 0, 0))
        selectBox2 = pygame.Surface((50, 20))
        selectBox2.fill((0, 0, 0))

        match a:
            case 1:
                chaosText = fontP.render((f"CHAOS: {chaos}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((chaosText.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - chaosText.get_width()) // 2  - 9, 200))
            case 2:
                option1Text = fontP.render((f"MOVING APPLES: {moveApples}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((option1Text.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - option1Text.get_width()) // 2  - 9, 250))
            case 3:
                option2Text = fontP.render((f"SPAWN MINES: {spawnMines}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((option2Text.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - option2Text.get_width()) // 2  - 9, 300))
            case 4:
                option3Text = fontP.render((f"MOVE MINES: {moveMines}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((option3Text.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - option3Text.get_width()) // 2 - 9, 350))
            case 5:
                option4Text = fontP.render((f"SPAWN NEW MINE AFTER EVERY APPLE: {alwaysSpawnMines}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((option4Text.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - option4Text.get_width()) // 2 - 9, 400))
            case 6:
                option5Text = fontP.render((f"MOVE MINES AFTER EVERY APPLE: {alwaysMoveMines}"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((option5Text.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - option5Text.get_width()) // 2 - 9, 450))
            case 7:
                returnText = fontP.render(("BACK"), True, (255, 255, 255))
                selectBox2 = pygame.Surface((returnText.get_width() + 18, 35))
                gameWindow.blit(selectBox2, ((gameWindow.width - returnText.get_width()) // 2  - 9, 500))
        
        gameWindow.blit(settingsText, ((gameWindow.width - settingsText.get_width()) // 2, 50))
        gameWindow.blit(chaosText, ((gameWindow.width - chaosText.get_width()) // 2, 200))
        gameWindow.blit(option1Text, ((gameWindow.width - option1Text.get_width()) // 2, 250))
        gameWindow.blit(option2Text, ((gameWindow.width - option2Text.get_width()) // 2, 300))
        gameWindow.blit(option3Text, ((gameWindow.width - option3Text.get_width()) // 2, 350))
        gameWindow.blit(option4Text, ((gameWindow.width - option4Text.get_width()) // 2, 400))
        gameWindow.blit(option5Text, ((gameWindow.width - option5Text.get_width()) // 2, 450))
        gameWindow.blit(returnText, ((gameWindow.width - returnText.get_width()) // 2, 500))

    #Main Game Loop Drawing
    elif game_state == 1:
        gameWindow.fill((0, 0, 0))
        
        gameWindow.blit(bg, (0, 0))

        for i in mine_list:
            gameWindow.blit(i.body, (i.x, i.y))
            if i.col_switch == 5:
                gameWindow.blit(i.ind, (i.x+8, i.y+8))
                i.col_switch = 0
            else:
                i.col_switch += 1

        for i in player.body[0:-1]:
            gameWindow.blit(player.shape, i)
        gameWindow.blit(player.head, player.body[-1])

        if apple.move_time == 5:
            match apple.dir:
                case -4: #Left
                    apple.vel_x = -30
                    apple.vel_y = 0
                case -3: #Up
                    apple.vel_x = 0
                    apple.vel_y = -30
                case -2: #Left up
                    apple.vel_x = -30
                    apple.vel_y = -30
                case -1: #Left down
                    apple.vel_x = -30
                    apple.vel_y = 30
                case 0:
                    apple.vel_x = 0
                    apple.vel_y = 0
                case 1: #Right up
                    apple.vel_x = 30
                    apple.vel_y = -30
                case 2: #Right down
                    apple.vel_x = 30
                    apple.vel_y = 30
                case 3: #Down
                    apple.vel_x = 0
                    apple.vel_y = 30
                case 4: #Right
                    apple.vel_x = 30
                    apple.vel_y = 0
                
        
            apple.move_time = 0
        
        else:
            apple.vel_x = 0
            apple.vel_y = 0
        apple.x += apple.vel_x
        apple.y += apple.vel_y
        gameWindow.blit(apple.shape, (apple.x, apple.y))

        scoreText = fontH1.render(str(player.score), True, (255, 255, 255))
        gameWindow.blit(scoreText, (10, 10))

    #Game Over Screen Drawing
    elif game_state == 2:
        gameWindow.fill((0, 0, 0))

        if chaos == "YES":
            game_over = fontH1.render("GAME OVER", True, (255, 0, 0))
        elif chaos == "NO":
            game_over = fontH1.render("GAME OVER", True, (255, 255, 255))
        gameWindow.blit(game_over, ((gameWindow.width - game_over.get_width()) // 2, 50))

        if player.self_collision():
            if chaos == "YES":
                collisionText = fontH2.render("YOU COLIDED WITH YOURSELF", True, (255, 0, 0))
            elif chaos == "NO":
                collisionText = fontH2.render("YOU COLIDED WITH YOURSELF", True, (255, 255, 255))
            gameWindow.blit(collisionText, ((gameWindow.width - collisionText.get_width()) // 2, 250))

        if player.wall_collision():
            if chaos == "YES":
                collisionText = fontH2.render("YOU COLIDED WITH THE WALL", True, (255, 0, 0))
            elif chaos == "NO":
                collisionText = fontH2.render("YOU COLIDED WITH THE WALL", True, (255, 255, 255))
            gameWindow.blit(collisionText, ((gameWindow.width - collisionText.get_width()) // 2, 250))

        if player.mine_collision():
            if chaos == "YES":
                collisionText = fontH2.render("YOU STEPPED ON A MINE", True, (255, 0, 0))
            elif chaos == "NO":
                collisionText = fontH2.render("YOU STEPPED ON A MINE", True, (255, 255, 255))
            gameWindow.blit(collisionText, ((gameWindow.width - collisionText.get_width()) // 2, 250))

        if a > 0:
            if chaos == "YES":
                backToMenu = fontP.render("PRESS ENTER TO CONTINUE", True, (255, 0, 0))
            elif chaos == "NO":
                backToMenu = fontP.render("PRESS ENTER TO CONTINUE", True, (255, 255, 255))
        elif a < 0:
            backToMenu = fontP.render("PRESS ENTER TO CONTINUE", True, (0, 0, 0))

        b += 1

        if b > 3:
            a = -a
            b = 0

        gameWindow.blit(backToMenu, ((gameWindow.width - backToMenu.get_width()) // 2, 450))


    pygame.display.flip()