import pygame
import random

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroid Platformer")

# Define gravity limits
min_gravity = -1.0
max_gravity = 0.1

# Define initial gravity
gravity = pygame.math.Vector2(0, 0.1)

# Define player velocity and acceleration
player_velocity = pygame.math.Vector2(0, 0)
player_acceleration = pygame.math.Vector2(0, 0)

# Define player position and size
player_size = 20
player_pos = pygame.math.Vector2(width/2, height/2)

# Define dots
dot_list = []

# Center player on screen
player_pos.x = (width / 2) - (player_size / 2)
player_pos.y = (height / 2) - (player_size / 2)

# Define player maximum speed
max_speed = 5

# Define golden squares(astronauts)
golden_square_list = []
for i in range(6):
    x = random.randint(0, width)
    y = random.randint(0, height)
    golden_square_list.append(pygame.Rect(x, y, 10, 10))

# Define star properties
num_stars = 100
star_size = 2
star_color = (255, 255, 255)
star_list = []

# Generate stars
for i in range(num_stars):
    x = random.randint(0, width)
    y = random.randint(0, height)
    twinkle_timer = random.randint(0, 10)
    twinkle_duration = random.randint(80, 2000)
    twinkle_color = (255, 255, 255)
    twinkle_size = 2
    star_list.append({
        "pos": pygame.math.Vector2(x, y),
        "twinkle_timer": twinkle_timer,
        "twinkle_duration": twinkle_duration,
        "twinkle_color": twinkle_color,
        "twinkle_size": twinkle_size
    })

# Define asteroid properties
num_asteroids = 30
asteroid_size = 10
asteroid_color = (255, 255, 255)
asteroid_list = []
asteroid_velocity_list = []

# Generate asteroids
for i in range(num_asteroids):
    x = random.randint(0, width)
    y = random.randint(0, height)
    asteroid_rect = pygame.Rect(x, y, asteroid_size, asteroid_size)
    asteroid_list.append(asteroid_rect)
    asteroid_velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
    asteroid_velocity_list.append(asteroid_velocity)

points = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_acceleration.x = -0.01
    elif keys[pygame.K_RIGHT]:
        player_acceleration.x = 0.01
    else:
        player_acceleration.x = 0

    if keys[pygame.K_UP]:
        player_acceleration.y = -0.01
    elif keys[pygame.K_DOWN]:
        player_acceleration.y = +0.01
    else:
        player_acceleration.y = 0

    # Update player velocity and position
    player_velocity += player_acceleration
    player_velocity.x = max(-max_speed, min(player_velocity.x, max_speed))
    player_velocity.y = max(-max_speed, min(player_velocity.y, max_speed))
    player_pos += player_velocity

    # Update player acceleration
    if player_acceleration.x != 0:
        player_acceleration.y = 0.005

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw stars
    for star in star_list:
        x = int(star["pos"].x)
        y = int(star["pos"].y)
        size = star["twinkle_size"]
        color = star["twinkle_color"]
        pygame.draw.circle(screen, color, (x, y), size)

    # Update stars
    for star in star_list:
        # Update twinkle timer
        star["twinkle_timer"] += 1
        if star["twinkle_timer"] >= star["twinkle_duration"]:
            if random.randint(0, 1):
                star["twinkle_color"] = (255, 255, 255)
            else:
                star["twinkle_color"] = (100, 100, 100)

            if random.randint(0, 1):
                star["twinkle_size"] = 2
            else:
                star["twinkle_size"] = 2

            star["twinkle_timer"] = 0
        
    #Draw golden squares(asronauts)
    for golden_square in golden_square_list:
        pygame.draw.rect(screen, (255, 215, 0), golden_square)

        # Check for collision with player
        for golden_square in golden_square_list:
            if golden_square.colliderect(pygame.Rect(player_pos.x, player_pos.y, player_size, player_size)):
                golden_square_list.remove(golden_square)
                points += 1
    
    # Draw dots
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            pygame.draw.circle(screen, (255, 255, 255), (int(dot.x), int(dot.y)), 2)
            dot_list.append(pygame.Rect(player_pos.x, player_pos.y, 2, 2))
            for dot in dot_list:    
                
                for asteroid in asteroid_list:
                    if dot.colliderect(asteroid):
                        dot_list.remove(dot)
                        asteroid_list.remove(asteroid)

    # Draw asteroids
    for i, asteroid in enumerate(asteroid_list):
        asteroid_velocity = asteroid_velocity_list[i]
        asteroid.x += asteroid_velocity.x
        asteroid.y += asteroid_velocity.y

        # Check for collision with player
        if asteroid.colliderect(pygame.Rect(player_pos.x, player_pos.y, player_size, player_size)):
            print("Game Over")
            running = False

        # Check for collision with screen boundaries
        if asteroid.left < 0 or asteroid.right > width:
            asteroid_velocity.x *= -1
        if asteroid.top < 0 or asteroid.bottom > height:
            asteroid_velocity.y *= -1

        pygame.draw.rect(screen, asteroid_color, asteroid)

        # Check for collision with other asteroids
        for j, other_asteroid in enumerate(asteroid_list):
            if i == j:
                continue

            if asteroid.colliderect(other_asteroid):
                # Split asteroid into smaller ones
                new_size = asteroid_size // 2
                new_velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                new_asteroid1 = pygame.Rect(asteroid.left, asteroid.top, new_size, new_size)
                new_asteroid2 = pygame.Rect(asteroid.right - new_size, asteroid.bottom - new_size, new_size, new_size)
                asteroid_list[i] = new_asteroid1
                asteroid_list[j] = new_asteroid2

        pygame.draw.rect(screen, asteroid_color, asteroid)
    
    

    font = pygame.font.Font(None, 36)
    text = font.render("Points: " + str(points), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Draw player
    pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(player_pos.x, player_pos.y, player_size, player_size))

    # Update screen
    pygame.display.flip()

    # Delay between frames
    pygame.time.delay(10)

# Clean up
pygame.quit()