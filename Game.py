import pygame, sys, random

pygame.mixer.init()
sound = pygame.mixer.Sound("BOOM sound effect (1).mp3")
sound67 = pygame.mixer.Sound("ssvid.net--doot-doot-6-7-skrilla-shorts.mp3")

highscore = 0

last_speed_increase = 0

show_speed_text = 0
show_speed_text2 = 0

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, show_speed_text

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 7
    if start and ball_speed_x == 0 and ball_speed_y == 0:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((-1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player) and ball_speed_y > 0:
            # TODO Task 2: Fix score to increase by 1
        ball_speed_y *= -1  # Reverse ball's vertical direction
        ball.bottom = player.top

        if score <= 55:
            score += 1
            sound.play()

        elif score == 56:
            score += 1
            sound67.play()

        elif 57 <= score <= 67:
            score += 1

        else:
            score += 1
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
        game_over_screen() # Reset the game

    if difficulty():
        show_speed_text = 60
        show_speed_text2 = 100

def difficulty():
    global ball_speed_x, ball_speed_y, score, last_speed_increase

    if score != 0 and score % 10 == 0 and score < 99 and score != last_speed_increase:
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        last_speed_increase = score
        return True
    return False

    if score != 0 and score == 100:
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        return True
    return False

    if score > 101:
        ball_speed_x *= 1
        ball_speed_y *= 1

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
    global ball_speed_x, ball_speed_y, score, start, player_speed
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = 0, 0
    score = 0
    start = False
    player_speed = 0

    player.centerx = screen_width / 2
    pygame.event.clear()

def game_over_screen():
    global score, highscore, ball_speed_x, ball_speed_y, start

    if score > highscore:
        highscore = score

    ball_speed_x, ball_speed_y = 0, 0

    overlay = pygame.Surface((345, 200))
    overlay.fill(pygame.Color("grey25"))
    overlay_rect = overlay.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(overlay, overlay_rect)

    font = pygame.font.Font("freesansbold.ttf", 28)
    text1 = font.render("Game Over", True, pygame.Color("firebrick4"))
    text2 = font.render(f"Highscore: {highscore}", True, pygame.Color("white"))
    text3 = font.render(f"Score: {score}", True, pygame.Color("white"))
    text4 = font.render("Press SPACE to Restart", True, pygame.Color("yellow"))

    screen.blit(text1, (overlay_rect.centerx - text1.get_width() / 2, overlay_rect.top + 20))
    screen.blit(text2, (overlay_rect.centerx - text2.get_width()/2, overlay_rect.top + 63))
    screen.blit(text3, (overlay_rect.centerx - text3.get_width()/2, overlay_rect.top + 105))
    screen.blit(text4, (overlay_rect.centerx - text4.get_width()/2, overlay_rect.top + 150))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart()
                    waiting = False

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
player.centerx = (screen_width / 2)

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
    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, fire, ball)  # Draw ball
    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    screen.blit(player_text, (screen_width/2 - player_text.get_width() / 2, 10))  # Display score on screen

    if show_speed_text > 0 and show_speed_text <= 90:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_increased = font.render("Speed Increased", True, pygame.Color('gold'))
        screen.blit(text_increased, (screen_width/2 - text_increased.get_width()/2, 50))
        show_speed_text -= 1

    if score == 100:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_increased = font.render("Max Speed", True, pygame.Color('gold'))
        screen.blit(text_increased, (screen_width/2 + 1 - text_increased.get_width()/2, 50))
        show_speed_text -= 1

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second