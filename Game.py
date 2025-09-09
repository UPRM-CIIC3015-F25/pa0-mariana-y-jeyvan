import pygame, sys, random

# Background Music
pygame.mixer.init()
pygame.mixer.music.load("Castle-Infiltration.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Sound Effects
sound = pygame.mixer.Sound("pop.mp3")
sound_game_over = pygame.mixer.Sound("game_over2.mp3")

# Game Variables
highscore = 0
level = 0

# Control Variables (Prevents infinite increases of speed, coins and level when the last number is 0)
last_speed_increase = 0
last_coins_increase = 0
last_level_increase = 0

# Show Speed Text (Frames for the Speed Message)
show_speed_text = 0

# Shop Variables
coins = 0
bronze = 25
silver = 50
gold = 75
platinum = 100
diamond = 150

# Ball Inventory
inventory = {
    "Bronze Ball": False,
    "Silver Ball": False,
    "Gold Ball": False,
    "Platinum Ball": False,
    "Diamond Ball": False}
selected_ball = "normal"

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, show_speed_text, level, coins, \
        last_level_increase, last_coins_increase

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 10
    if start and ball_speed_x == 0 and ball_speed_y == 0:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((-1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player) and ball_speed_y > 0:
            # TODO Task 2: Fix score to increase by 1
        score += 1
        ball_speed_y *= -1  # Reverse ball's vertical direction
        ball.bottom = player.top
        ball_speed_x += random.choice((-1, 0, 1)) # Randomize the Ball's Direction
        sound.play()


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction
        ball.top = 0

    # Ball collision with left and right boundaries
    if ball.left <= 0:
        ball_speed_x *= -1
        ball.left = 0

    if ball.right >= screen_width:
        ball_speed_x *= -1
        ball.right = screen_width

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        pygame.mixer.music.stop()
        sound_game_over.play()
        game_over_screen() # Opens Game Over Screen

    # Increases 5 Coins every 10 points
    if score != 0 and score % 10 == 0 and score != last_coins_increase:
        coins += 5
        last_coins_increase = score

    # Increases level every 10 points
    if score != 0 and score % 10 == 0 and score != last_level_increase and score != 100:
        level +=1
        last_level_increase = score

    # Sets the Max Level to 10 when Score reaches 100 or more
    if score >= 100:
        level = 10

    # When difficulty() returns True, the speed message shows up
    if difficulty():
        show_speed_text = 60

def difficulty():
    global ball_speed_x, ball_speed_y, score, last_speed_increase

    # Multiplies the ball speed by 1.1 every 10 points
    if score != 0 and score % 10 == 0 and score < 99 and score != last_speed_increase:
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        last_speed_increase = score
        return True

    # Sets the Max Speed at 100 points
    if score != 0 and score == 100 and score != last_speed_increase:
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        last_speed_increase = score
        return True

    # Returns False when the score is greater than 100
    if score > 100:
        return False

    return False

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets all game variables and positions to prepare for a new game.
    """

    global ball_speed_x, ball_speed_y, score, start, player_speed, level, \
        last_coins_increase, last_speed_increase, last_level_increase

    ball.center = (screen_width // 2, screen_height // 2)
    ball_speed_x, ball_speed_y = 0, 0
    score = 0
    start = False
    player_speed = 0

    # Reset variables to 0
    level = 0
    last_speed_increase = 0
    last_coins_increase = 0
    last_level_increase = 0

    player.centerx = screen_width // 2 # The paddle resets to center
    pygame.event.clear()

def game_over_screen():
    """
    Displays the Game Over screen, updates highscore, and handles restart or shop selection.
    """

    global score, highscore, ball_speed_x, ball_speed_y, start

    # Saves the Highscore
    if score > highscore:
        highscore = score

    ball_speed_x, ball_speed_y = 0, 0

    # Overlay Screen for the Game Over
    overlay = pygame.Surface((345, 240))
    overlay.fill(pygame.Color("grey25"))
    overlay_rect = overlay.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(overlay, overlay_rect)

    # Texts for the Game Over Screen
    game_over_font = pygame.font.Font("freesansbold.ttf", 28)
    text1 = game_over_font.render("Game Over", True, pygame.Color("firebrick4"))
    text2 = game_over_font.render(f"Highscore: {highscore}", True, pygame.Color("white"))
    text3 = game_over_font.render(f"Score: {score}", True, pygame.Color("white"))
    text4 = game_over_font.render("Press SPACE to Restart", True, pygame.Color("yellow"))
    text5 = game_over_font.render("Press S to Shop", True, pygame.Color("khaki"))

    screen.blit(text1, (overlay_rect.centerx - text1.get_width() / 2, overlay_rect.top + 20))
    screen.blit(text2, (overlay_rect.centerx - text2.get_width()/2, overlay_rect.top + 63))
    screen.blit(text3, (overlay_rect.centerx - text3.get_width()/2, overlay_rect.top + 105))
    screen.blit(text4, (overlay_rect.centerx - text4.get_width()/2, overlay_rect.top + 150))
    screen.blit(text5, (overlay_rect.centerx - text5.get_width() / 2, overlay_rect.top + 190))

    pygame.display.flip()

    # Event Handling for Options on the Game Over Screen
    waiting = True
    while waiting:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_SPACE:
                    restart()
                    pygame.mixer.music.play()
                    waiting = False
                if event2.key == pygame.K_s:
                    shop_screen()
                    waiting = False

def shop_screen():
    """
    Displays the shop menu where players can buy or select balls using coins.
    """

    global selected_ball, bronze, silver, gold, platinum, diamond, coins, inventory

    # Event Handling for the Shop Screen
    running = True
    while running:
        for event3 in pygame.event.get():
            if event3.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event3.type == pygame.KEYDOWN:
                if event3.key == pygame.K_ESCAPE:
                    running = False
                if event3.key == pygame.K_1:
                    if not inventory["Bronze Ball"] and coins >= bronze:
                        coins -= bronze
                        selected_ball = "Bronze Ball"
                        inventory["Bronze Ball"] = True
                    if inventory["Bronze Ball"]:
                        selected_ball = "Bronze Ball"
                if event3.key == pygame.K_2:
                    if not inventory["Silver Ball"] and coins >= silver:
                        coins -= silver
                        selected_ball = "Silver Ball"
                        inventory["Silver Ball"] = True
                    if inventory["Silver Ball"]:
                        selected_ball = "Silver Ball"
                if event3.key == pygame.K_3:
                    if not inventory["Gold Ball"] and coins >= gold:
                        coins -= gold
                        selected_ball = "Gold Ball"
                        inventory["Gold Ball"] = True
                    if inventory["Gold Ball"]:
                        selected_ball = "Gold Ball"
                if event3.key == pygame.K_4:
                    if not inventory["Platinum Ball"] and coins >= platinum:
                        coins -= platinum
                        selected_ball = "Platinum Ball"
                        inventory["Platinum Ball"] = True
                    if inventory["Platinum Ball"]:
                        selected_ball = "Platinum Ball"
                if event3.key == pygame.K_5:
                    if not inventory["Diamond Ball"] and coins >= diamond:
                        coins -= diamond
                        selected_ball = "Diamond Ball"
                        inventory["Diamond Ball"] = True
                    if inventory["Diamond Ball"]:
                        selected_ball = "Diamond Ball"

        # Shop Screen
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(pygame.Color("grey12"))
        overlay_rect = overlay.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(overlay, overlay_rect)

        # Texts for the Shop Screen
        shop_screen_font = pygame.font.Font("freesansbold.ttf", 28)
        coins_font = pygame.font.Font("freesansbold.ttf", 24)
        text_shop = shop_screen_font.render("Shop", True, pygame.Color("white"))
        text_select = shop_screen_font.render("Select Number", True, pygame.Color("khaki"))
        text1_shop = shop_screen_font.render("1. Bronze Ball - 25 coins", True, pygame.Color("sienna"))
        text2_shop = shop_screen_font.render("2. Silver Ball - 50 coins", True, pygame.Color("silver"))
        text3_shop = shop_screen_font.render("3. Gold Ball - 75 coins", True, pygame.Color("gold"))
        text4_shop = shop_screen_font.render("4. Platinum Ball - 100 coins", True, pygame.Color("slategray1"))
        text5_shop = shop_screen_font.render("5. Diamond Ball - 150 coins", True, pygame.Color("paleturquoise3"))
        text_escape = shop_screen_font.render("Press ESC to Exit", True, pygame.Color("yellow"))
        text_coins = coins_font.render(f'Coins: {coins}', True, pygame.Color("yellow"))

        screen.blit(text_shop, (overlay_rect.centerx - text_shop.get_width() / 2, overlay_rect.top + 20))
        screen.blit(text_select, (overlay_rect.centerx - text_select.get_width() / 2, overlay_rect.top + 65))
        screen.blit(text1_shop, (overlay_rect.centerx - text1_shop.get_width() / 2, overlay_rect.top + 120))
        screen.blit(text2_shop, (overlay_rect.centerx - text2_shop.get_width() / 2, overlay_rect.top + 165))
        screen.blit(text3_shop, (overlay_rect.centerx - text3_shop.get_width() / 2, overlay_rect.top + 210))
        screen.blit(text4_shop, (overlay_rect.centerx - text4_shop.get_width() / 2, overlay_rect.top + 255))
        screen.blit(text5_shop, (overlay_rect.centerx - text5_shop.get_width() / 2, overlay_rect.top + 300))
        screen.blit(text_coins, (370, 10))
        screen.blit(text_escape, (overlay_rect.centerx - text_escape.get_width() / 2, overlay_rect.top + 370))

        pygame.display.flip()

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height) # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Score Text setup
score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name

    name = "Jeyvan"
    name2 = "Mariana"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    light_grey = pygame.Color('grey83')
    fire = pygame.Color('firebrick4')
    screen.fill(bg_color)  # Clear screen with background color

    # Background Image
    image_bg = pygame.image.load('download.gif').convert_alpha()
    image_bg.set_alpha(150)
    screen.blit(image_bg, (0, 0))

    pygame.draw.rect(screen, light_grey, player)# Draw player paddle
    # TODO Task 3: Change the Ball Color

    # Ball Colors for the Shop and In-Game
    if selected_ball == "normal":
        pygame.draw.ellipse(screen, fire, ball)  # Draw ball

    if selected_ball == "Bronze Ball":
        pygame.draw.ellipse(screen, pygame.Color('sienna'), ball)

    if selected_ball == "Silver Ball":
        pygame.draw.ellipse(screen, pygame.Color('silver'), ball)

    if selected_ball == "Gold Ball":
        pygame.draw.ellipse(screen, pygame.Color('gold'), ball)

    if selected_ball == "Platinum Ball":
        pygame.draw.ellipse(screen, pygame.Color('slategray1'), ball)

    if selected_ball == "Diamond Ball":
        pygame.draw.ellipse(screen, pygame.Color('paleturquoise3'), ball)

    # Score Points
    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    screen.blit(player_text, (screen_width/2 - player_text.get_width() / 2, 10))  # Display score on screen

    # Player's Coins
    font = pygame.font.Font('freesansbold.ttf', 24)
    coins_text = font.render(f'Coins: {coins}', True, pygame.Color("yellow"))
    screen.blit(coins_text, (370, 10))

    # Displays Speed Increased Message
    if 0 < show_speed_text <= 90:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_increased = font.render("Speed Increased", True, pygame.Color('gold'))
        screen.blit(text_increased, (screen_width/2 - text_increased.get_width()/2, 50))
        show_speed_text -= 1

    # Displays Max Speed Message
    if score == 100:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_increased = font.render("Max Speed", True, pygame.Color('gold'))
        screen.blit(text_increased, (screen_width/2 + 1 - text_increased.get_width()/2, 50))
        show_speed_text -= 1

    # Displays the current Game Level
    if level == 0:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level0 = font.render("Level 0", True, pygame.Color('blue'))
        screen.blit(text_level0, (15, 10))
    if level == 1:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level1 = font.render("Level 1", True, pygame.Color('blue'))
        screen.blit(text_level1, (15,10))
    if level == 2:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level2 = font.render("Level 2", True, pygame.Color('blue'))
        screen.blit(text_level2, (15, 10))
    if level == 3:
       font = pygame.font.Font('freesansbold.ttf', 24)
       text_level3 = font.render("Level 3", True, pygame.Color('blue'))
       screen.blit(text_level3, (15, 10))
    if level == 4:
       font = pygame.font.Font('freesansbold.ttf', 24)
       text_level4 = font.render("Level 4", True, pygame.Color('blue'))
       screen.blit(text_level4, (15, 10))
    if level == 5:
       font = pygame.font.Font('freesansbold.ttf', 24)
       text_level5 = font.render("Level 5", True, pygame.Color('blue'))
       screen.blit(text_level5, (15, 10))
    if level == 6:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level6 = font.render("Level 6", True, pygame.Color('blue'))
        screen.blit(text_level6, (15, 10))
    if level == 7:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level7 = font.render("Level 7", True, pygame.Color('blue'))
        screen.blit(text_level7, (15, 10))
    if level == 8:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level8 = font.render("Level 8", True, pygame.Color('blue'))
        screen.blit(text_level8, (15, 10))
    if level == 9:
            font = pygame.font.Font('freesansbold.ttf', 24)
            text_level9 = font.render("Level 9", True, pygame.Color('blue'))
            screen.blit(text_level9, (15, 10))
    if level == 10:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_level10 = font.render("Level 10", True, pygame.Color('blue'))
        screen.blit(text_level10, (15, 10))

                    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second