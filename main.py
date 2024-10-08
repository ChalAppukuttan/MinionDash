def gamedef():
    import pygame
    import os
    import random
    import tkinter as tk
    pygame.init()

    # Global Constants
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 1100
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minion Dash')
    RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
               pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
    JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
    DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
               pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

    SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
    LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

    BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
            pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

    CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

    BG = pygame.image.load(os.path.join("Assets/Other", "grasstrack.jpg"))

    scoreSFX = pygame.mixer.Sound('caching.mp3')
    class Dinosaur:
        X_POS = 80
        Y_POS = 310
        Y_POS_DUCK = 340
        JUMP_VEL = 8.5

        def __init__(self):
            self.duck_img = DUCKING
            self.run_img = RUNNING
            self.jump_img = JUMPING

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

            self.step_index = 0
            self.jump_vel = self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS

        def update(self, userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index += 1

        def run(self):
            self.image = self.run_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index += 1

        def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            if self.jump_vel < - self.JUMP_VEL:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


    class Cloud:
        def __init__(self):
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = SCREEN_WIDTH + random.randint(2500, 3000)
                self.y = random.randint(50, 100)

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.x, self.y))


    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = SCREEN_WIDTH

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], self.rect)


    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 325


    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 300


    class Bird(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 200
            self.index = 0

        def draw(self, SCREEN):
            if self.index >= 9:
                self.index = 0
            SCREEN.blit(self.image[self.index//5], self.rect)
            self.index += 1

    def show_quiz():
        def check_answer(event=None):
            user_answer = entry.get()
            try:
                user_answer = int(user_answer)
                if user_answer == answer:
                    feedback_label.config(text="Correct!", fg="green")
                    root.after(500, root.destroy)  # Correct answer, close the Tkinter window after 500ms
                    global quiz_result
                    pygame.mixer.Sound.play(scoreSFX)
                    quiz_result = True
                else:
                    feedback_label.config(text="Wrong :(", fg="red")
                    root.after(500, root.destroy)  # Wrong answer, close the Tkinter window after 500ms
                    quiz_result = False
            except ValueError:
                feedback_label.config(text="Please enter a valid number", fg="orange")

        def new_question():
            global num1, num2, answer
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            answer = num1 + num2
            question_label.config(text=f"What does {num1} + {num2} = ?")
            entry.delete(0, tk.END)

        # Initialize Tkinter window
        root = tk.Tk()
        root.title("Math Quiz")

        # Create question label
        question_label = tk.Label(root, text="", font=("Arial", 16))
        question_label.pack(pady=20)

        # Create input field
        entry = tk.Entry(root, font=("Arial", 16))
        entry.pack(pady=10)
        entry.bind('<Return>', check_answer)

        # Feedback label
        feedback_label = tk.Label(root, text="", font=("Arial", 16))
        feedback_label.pack(pady=10)

        # Generate first question
        new_question()

        # Start Tkinter event loop
        root.mainloop()

    def main():
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles, quiz_result
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        font = pygame.font.Font('freesansbold.ttf', 20)
        obstacles = []
        death_count = 0
        quiz_result = True  # Track if quiz is passed

        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1
            if points % 500 == 0 and quiz_result:  # Every 500 points, show quiz
                pygame.time.delay(500)  # Slight delay before pausing
                pygame.display.update()
                show_quiz()  # Show the Tkinter quiz
                if not quiz_result:  # If player failed quiz, reset the game
                    pygame.quit()
                    menu(1)
                    return

            text = font.render("Points: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            SCREEN.fill((255, 255, 230))
            userInput = pygame.key.get_pressed()

            player.draw(SCREEN)
            player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

            background()

            cloud.draw(SCREEN)
            cloud.update()

            score()

            clock.tick(30)
            pygame.display.update()


    def menu(death_count):
        global points
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)

            if death_count == 0:
                text = font.render("Press Space to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press Space to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    main()


    menu(death_count=0)

