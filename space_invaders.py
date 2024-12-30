# Andrew Nguyen, Computing ID: fru4yr
# Derek Song, Computing ID: xrr4td
import uvage
import random

screenwidth = 800
screenheight = 600
camera = uvage.Camera(screenwidth, screenheight)
p1 = uvage.from_image(400, 570, "player.png")
walls = [uvage.from_color(0, screenheight / 2, 'black', 1, screenheight),
         uvage.from_color(800, screenheight / 2, "black", 1, screenheight)]
bulletlist = []
enemy_bullet_list = []
gameon = False
bullet_on_screen = False
game_time = 0
enemies = []
ycoord = 0
row = 0
move_x = False
times_played = 0
score = 0
health = 100
health_bar_box = [uvage.from_color(50, 10, 'white', 50, 2),
                  uvage.from_color(50, 110, 'white', 50, 2),
                  uvage.from_color(25, 60, 'white', 2, 100),
                  uvage.from_color(75, 60, 'white', 2, 100)]
# this is the array that contains the outline of the health bar

hundred = uvage.from_color(50, 20, 'red', 50, 20)
eighty = uvage.from_color(50, 40, 'red', 50, 20)
sixty = uvage.from_color(50, 60, 'red', 50, 20)
forty = uvage.from_color(50, 80, 'red', 50, 20)
twenty = uvage.from_color(50, 100, 'red', 50, 20)
health_bar1 = [hundred, eighty, sixty, forty, twenty]
# each of the hundred, eighty, sixty, forty, and twenty variables are 5 bars in the health bar. as the health
# depletes, each value is removed form the array
poses = uvage.load_sprite_sheet('enemyposes.png', 1, 2)
pose = 0
for i in range(5):
    ycoord += 45
    xcoord = 80

    for j in range(11):
        xcoord += 45
        enemies.append(uvage.from_circle(xcoord, ycoord, 'green', 15, 15))
# this nested for loop creates the rows and columns for the enemies in the game and stores it into an array called
# enemies.
barriers = []
barriers.append(uvage.from_color(200, 450, "green", 100, 40))
barriers.append(uvage.from_color(600, 450, "green", 100, 40))
leftbarrierhealth = 10
rightbarrierhealth = 10


# creates barrier objects


def enemy_hit():  # removes enemies from the enemies array if they are hit by the player's bullet
    global bullet_on_screen
    if gameon:
        for each in enemies:
            if bullet_on_screen and bulletlist[-1].touches(each):
                bullet_on_screen = False
                bulletlist.pop(-1)
                enemies.remove(each)
                return True
        return False


def barrier():  # creates barriers that break after being hit 10 times, either by the player's bullets, or enemy bullets
    global bullet_on_screen
    global leftbarrierhealth
    global rightbarrierhealth
    if gameon == True:
        for bar in barriers:
            camera.draw(bar)
            if leftbarrierhealth == 0:
                del barriers[0]
                leftbarrierhealth -= 1
            if rightbarrierhealth == 0:
                if leftbarrierhealth > 0:
                    del barriers[1]
                else:
                    del barriers[0]
                rightbarrierhealth -= 1

        for bar in barriers:
            if bullet_on_screen and bulletlist[-1].touches(bar):
                bullet_on_screen = False
                bulletlist.pop(-1)
                index = barriers.index(bar)
                if index == 0 and leftbarrierhealth > 0:
                    leftbarrierhealth -= 1
                if index == 1 or (index == 0 and leftbarrierhealth < 0):
                    rightbarrierhealth -= 1
        for bar in barriers:
            for bullet in enemy_bullet_list:
                if bullet.touches(bar):
                    enemy_bullet_list.remove(bullet)
                    index = barriers.index(bar)
                    if index == 0 and leftbarrierhealth > 0:
                        leftbarrierhealth -= 1
                    if index == 1 or (index == 0 and leftbarrierhealth < 0):
                        rightbarrierhealth -= 1


def start_game():  # shows text on the screen telling player how to start the game. once the player clicks the button the game starts.
    global gameon
    if not gameon and times_played == 0:
        camera.draw(uvage.from_text(400, 300, "Press 'enter' to start game", 40, 'white', True, False))
        if uvage.is_pressing('return'):
            gameon = True
    if gameon:
        for each in enemies:
            camera.draw(each)


def enemypose():  # makes enemies randomly change pose
    global enemies
    global pose
    global poses
    global game_time
    global gameon
    if game_time % 25 == 0:
        for each in enemies:
            rand = random.randint(0, 1)
            each.image = poses[rand]


def enemy_move():  # moves the enemies in the same style as the original retro space invaders
    global game_time, row, pose, poses
    if gameon:
        enemy_at_right = False
        enemy_at_left = False
        game_time += 1
        global move_x
        if game_time % 30 == 0 or game_time == 0:
            for each in enemies:
                if each.x + 80 >= 800:
                    enemy_at_right = True
                if each.x - 80 <= 0:
                    enemy_at_left = True
            for each in enemies:
                if enemy_at_left:
                    each.y += 30
                    move_x = False
                elif enemy_at_right:
                    each.y += 30
                    move_x = True
                if move_x:
                    each.x -= 10
                elif not move_x:
                    each.x += 10


def win():  # checks if the player won or lost the game. Turns the game off if won or lost, and displays text corresponding to each scenario.
    global gameon
    global times_played
    if len(enemies) == 0:
        camera.draw(uvage.from_text(400, 300, 'You Win!', 60, 'Green', True, True))
        gameon = False
        times_played += 1
        return True
    else:
        for each in enemies:
            if p1.touches(each) or health == 0:
                camera.draw(uvage.from_text(400, 300, 'You Lose!', 60, 'red', True, True))
                gameon = False
                times_played += 1
                return False


def move_player():  # gives the user the ability to move the shooting entity in the game using the right or left arrow keys.
    if gameon:
        if uvage.is_pressing('left arrow'):
            p1.x -= 8
        if uvage.is_pressing('right arrow'):
            p1.x += 8
        for wall in walls:
            if p1.touches(wall):
                p1.move_to_stop_overlapping(wall)
        camera.draw(p1)


def shoot():  # allows the player to shoot their gun in the game at the aliens using the space bar
    global bulletlist, bullet_on_screen
    if gameon:
        if uvage.is_pressing("space") and not bullet_on_screen:
            bulletlist.append(uvage.from_color(p1.x, p1.y, "red", 5, 10))
            bullet_on_screen = True
        if len(bulletlist) >= 1:
            if bulletlist[-1].y < 0:
                bullet_on_screen = False
        for bullet in bulletlist:
            bullet.y -= 15
        for bullet in bulletlist:
            camera.draw(bullet)


def enemy_shoot():  # makes the enemies shoot bullets back at the player to try and kill the player.
    global enemy_bullet_list, gameon
    enemy_bullet_on_screen = False
    if gameon:
        for each in enemies:
            rng = random.randint(1, 1000)  # if the enemies shoot or not is determined by a random number generator
            if rng < 2 and not enemy_bullet_on_screen:
                enemy_bullet_list.append(uvage.from_color(each.x, each.y, 'green', 5, 10))
                enemy_bullet_on_screen = True
            if len(enemy_bullet_list) > 0 > enemy_bullet_list[-1].y:
                enemy_bullet_on_screen = False
        for bullet in enemy_bullet_list:
            bullet.y += 15
        for bullet in enemy_bullet_list:
            camera.draw(bullet)


def player_take_damage():  # depletes the health of the player if they are hit by any bullet by the invaders.
    global health
    if len(enemy_bullet_list):
        for each in enemy_bullet_list:
            if each.touches(p1) and health > 0:
                health -= 10
                enemy_bullet_list.remove(each)


def restart():  # resets all the variables of the game to their original value
    global gameon, times_played, health, enemies, enemy_bullet_list, health_bar1, pose, poses, move_x, score, leftbarrierhealth, rightbarrierhealth
    if not gameon and times_played > 0:
        camera.draw(uvage.from_text(400, 500, "Press R to restart", 40, 'white', True, False))
        if uvage.is_pressing('r'):
            enemy_bullet_list = []
            ycoord = 0
            times_played = 0
            health = 100
            enemies = []
            pose = 0
            score = 0
            for i in range(5):
                ycoord += 45
                xcoord = 80

                for j in range(11):
                    xcoord += 45
                    enemies.append(uvage.from_circle(xcoord, ycoord, 'green', 15, 15))
            for each in enemies:
                each.image = poses[pose]
            health_bar1 = [hundred, eighty, sixty, forty, twenty]
            leftbarrierhealth = 10
            rightbarrierhealth = 10
            barriers.append(uvage.from_color(200, 450, "green", 100, 40))
            barriers.append(uvage.from_color(600, 450, "green", 100, 40))
            gameon = True
            move_x = False


def health_bar():  # the health bar function. tracks the health of the player to see if the player is losing enough
    # health for there to be visible changes to the in-game health bar.
    global health_bar1
    if health == 80:  # checks for each health level and sets the health bar to its appropriate level
        health_bar1 = [eighty, sixty, forty, twenty]
    elif health == 60:
        health_bar1 = [sixty, forty, twenty]
    elif health == 40:
        health_bar1 = [forty, twenty]
    elif health == 20:
        health_bar1 = [twenty]
    elif health == 0:
        health_bar1 = []
    if gameon:  # draws the health bar
        for j in health_bar_box:
            camera.draw(j)
        for i in health_bar1:
            camera.draw(i)


def display_score(): # calculates the score of the player based on how many enemies were killed and displays it in the top right
    global score
    score = (55 - len(enemies)) * 30
    if score != 0 and gameon:
        camera.draw(uvage.from_text(700, 15, 'Score: ' + str(score), 40, 'white', True, False))


def tick():
    camera.clear('black')
    start_game()
    health_bar()
    move_player()
    enemy_shoot()
    shoot()
    player_take_damage()
    enemy_hit()
    win()
    barrier()
    enemy_move()
    display_score()
    enemypose()
    restart()
    camera.display()


uvage.timer_loop(30, tick)
