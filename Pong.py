# Pong Program
# Written by Nate Neumann
# Devin Balkcom's CS 1 Class, Dartmouth College
# Lab 1: February 1st, 2017

from cs1lib import *
import random

VICTORY_SCORE = 5       # Points needed to win
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
BALL_RADIUS = 5
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
L_UP_KEY = "a"      # Pressing the L_UP_KEY moves the left paddle up one tick, and so on. Change controls here.
L_DOWN_KEY = "z"
R_UP_KEY = "k"
R_DOWN_KEY = "m"
MOVESPEED = 10      # Amount the paddles move per tick
FRAME_RATE = 60
BALL_START_X = 200  # Starting x-coord of ball
BALL_START_Y = 10   # Starting y-coord of ball
BALL_START_VELOCITY_X = 1
BALL_START_VELOCITY_Y = 1
BOOST_PAD_ACCELERATION = .15    # How much boost pads accelerate the ball (while the ball is on them!)

lalt = 0        # Starting height of left paddle: top left corner at standard setup
ralt = (WINDOW_HEIGHT - PADDLE_HEIGHT)      # Starting height of right paddle: 320 at standard setup
ballx = BALL_START_X        # x-coord of ball at given point
bally = BALL_START_Y        # y-coord of ball at given point
ball_vx = BALL_START_VELOCITY_X     # x-velocity of ball at given point
ball_vy = BALL_START_VELOCITY_Y     # y-velocity of ball at given point
# Save this state for future use:
start_state = [0, (WINDOW_HEIGHT - PADDLE_HEIGHT), BALL_START_X, BALL_START_Y, BALL_START_VELOCITY_X, BALL_START_VELOCITY_Y]

lscore = 0  # Score of left player
rscore = 0  # Score of right player
accel_mod = False           # All mods disabled by default.
paddle_zone_mod = False
color_change_mod = False
random_bouncing_mod = False
boost_pads_mod = False
slam_jam_mod = False
bot_mod = False
modcount = 0
randr = 1                   # Various debugging to prevent undefined global errors.
randg = 1
randb = 1
boost_stationary = 0
begin_game = False          # Moves from menu screen to play.
playing = True              # Makes the game continue to run.


def menu_screen():
    global begin_game
    set_clear_color(0, 0, 0)  # Black background
    set_fill_color(1, 1, 1)  # White paddles
    set_stroke_color(1, 1, 1)
    clear()
    set_font("LilyUPC")
    set_font_size(40)
    draw_text("Welcome to Pong!", 70, 45)           # Menu text: Greeting, Mods list, controls details.
    set_font_size(20)
    draw_text("Begin by pressing Space...", 100, 70)
    draw_text("Or try some mods!", 100, 95)
    draw_text("VS AI or Player (V):", 80, 130)
    if bot_mod:
        draw_text("AI", 300, 130)
    if not bot_mod:
        draw_text("Player", 300, 130)
    draw_text("Acceleration (A): ", 80, 160)
    draw_text("Paddle zones (P): ", 80, 190)
    draw_text("Color Change (C): ", 80, 220)
    draw_text("Random Bouncing (R): ", 80, 250)
    draw_text("Boost pads (B): ", 80, 280)
    draw_text("COME ON AND SLAM (J): ", 80, 310)
    slam_jam_menu()
    menu_mod_font()
    draw_text("Controls:", 160, 340)
    draw_text("Player 1: " + L_UP_KEY + ", " + L_DOWN_KEY + "      Player 2: " + R_UP_KEY + ", " + R_DOWN_KEY, 70, 360)
    draw_text("Play: Space       Quit: Q", 84, 385)
    if is_key_pressed(" "):
        begin_game = True
    if begin_game:
        paddles()


def paddles():  # Draws the score, plus paddles and ball, based on the data from directive(key) and ball_velocity().
    global ballx, bally, ball_vx, ball_vy, lscore, rscore, playing, lalt, ralt, boost_stationary
    set_clear_color(0, 0, 0)       # Black background
    set_fill_color(1, 1, 1)       # White paddles and ball
    clear()
    ball_velocity()
    if slam_jam_mod:               # COME ON AND SLAM
        slam_jam_implement()       # AND WELCOME TO THE JAM
    if not slam_jam_mod:
        draw_rectangle(0, lalt, PADDLE_WIDTH, PADDLE_HEIGHT)     # Left paddle
        draw_rectangle((WINDOW_WIDTH - PADDLE_WIDTH), ralt, PADDLE_WIDTH, PADDLE_HEIGHT)   # Right paddle

    if boost_pads_mod:      # Draws boost pads, if mod is enabled. (Drawn before others to appear behind score et al.)
        boost_pads_implement()
    set_stroke_color(1, 1, 1)       # Prints the score on-screen
    set_font("LilyUPC")
    set_font_size(50)
    set_font_bold()
    draw_text(str(lscore), 100, 70)
    draw_text(str(rscore), 270, 70)
    if lscore == VICTORY_SCORE:                 # Prints game winner and ends game when a player reaches 5 points.
        if not slam_jam_mod:
            set_font_size(80)
            draw_text("Left wins!", 40, 200)
        if slam_jam_mod:
            draw_text("Monstars win!", 60, 120)
        set_font_size(50)
        playing = False
    if rscore == VICTORY_SCORE:
        if not slam_jam_mod:
            set_font_size(80)
            draw_text("Right wins!", 40, 200)
        if slam_jam_mod:
            draw_text("Tune Squad wins!", 10, 120)
        set_font_size(50)
        playing = False

    if color_change_mod:    # Colors the ball if mod is enabled, with randcolors changing with each hit.
        set_fill_color(randr, randg, randb)
        set_stroke_color(randr, randg, randb)

    if not slam_jam_mod:
        draw_circle(ballx, bally, BALL_RADIUS)          # Draws the ball-- SJ mod has its own draw function for this.

    if bot_mod:     # Automatically moves the R paddle towards the ball if playing vs computer.
        if ralt + (PADDLE_HEIGHT / 2) > bally and ralt > 0:
            ralt -= 1
        if ralt + (PADDLE_HEIGHT / 2) < bally and ralt < WINDOW_HEIGHT - PADDLE_HEIGHT:
            ralt += 1

    if playing:
        ballx += ball_vx        # Ball moves according to horizontal and vertical velocities
        bally += ball_vy
    if ballx > WINDOW_WIDTH + BALL_RADIUS + 1:      # Adds point, stops and resets the game after Left scores
        lscore += 1
        playing = False
        lalt, ralt, ballx, bally, ball_vx, ball_vy = start_state
        boost_stationary = 0        # Re-randomizes boost pad locations
    if ballx < 0 - BALL_RADIUS - 1:                 # Same as above, for Right player
        rscore += 1
        playing = False
        lalt, ralt, ballx, bally, ball_vx, ball_vy = start_state
        boost_stationary = 0

    if is_key_pressed(" "):         # Game resumed  by pressing spacebar
        playing = True
    if is_key_pressed("q"):         # Quits game by pressing Q
        cs1_quit()


def directive(key):     # This function changes the height of the paddles, and toggles mods, based on keyboard inputs.
    global lalt, ralt, accel_mod, paddle_zone_mod, color_change_mod, random_bouncing_mod, boost_pads_mod, slam_jam_mod, bot_mod
    ldown = is_key_pressed(L_DOWN_KEY)
    lup = is_key_pressed(L_UP_KEY)
    rdown = is_key_pressed(R_DOWN_KEY)
    rup = is_key_pressed(R_UP_KEY)

    # L paddle movement
    if ldown and lalt <= (WINDOW_HEIGHT - PADDLE_HEIGHT - MOVESPEED):  # Prevents L paddle from moving down offscreen
        lalt += MOVESPEED
    if lup and lalt >= MOVESPEED:   # Prevents L paddle from moving up offscreen
        lalt -= MOVESPEED

    # R paddle movement
    if not bot_mod:     # Prevents player from screwing with the AI's movement, when playing vs the computer.
        if rdown and ralt <= (WINDOW_HEIGHT - PADDLE_HEIGHT - MOVESPEED):  # Prevents Rpaddle from moving down offscreen
            ralt += MOVESPEED
        if rup and ralt >= MOVESPEED:   # Prevents R paddle from moving up offscreen
            ralt -= MOVESPEED

    # Keyboard mod toggling on menu screen
    if is_key_pressed("v"):
        bot_mod = not bot_mod
    if is_key_pressed("a"):
        accel_mod = not accel_mod
    if is_key_pressed("p"):
        paddle_zone_mod = not paddle_zone_mod
    if is_key_pressed("c"):
        color_change_mod = not color_change_mod
    if is_key_pressed("r"):
        random_bouncing_mod = not random_bouncing_mod
    if is_key_pressed("b"):
        boost_pads_mod = not boost_pads_mod
    if is_key_pressed("j"):
        slam_jam_mod = not slam_jam_mod


def ball_velocity():        # Adjusts ball's location, velocity, et al in regards to collision with paddles and walls.
    global ballx, bally, ball_vx, ball_vy, lalt, ralt, randr, randg, randb

    # Top of ball hits top of screen or bottom hits bottom of screen: Ball's vertical velocity reverses.
    if (bally - BALL_RADIUS) <= 0 or (bally + BALL_RADIUS) >= WINDOW_HEIGHT:
        ball_vy = (ball_vy * -1)

    # Ball hits paddle (R or L): ball edge has same X-coord as paddle edge, and ball's y-coord is between paddle's ends
    # Formula slightly modified to account for refresh delay at greater acceleration causing giltching through paddles.
    if ((ballx + BALL_RADIUS) == (WINDOW_WIDTH - PADDLE_WIDTH) and (ralt + PADDLE_HEIGHT) >= bally >= ralt) or\
       ((ballx - BALL_RADIUS) == PADDLE_WIDTH and (lalt + PADDLE_HEIGHT) >= bally >= lalt):
            ball_vx = (ball_vx * -1)    # Ball's horizontal velocity reverses

            if accel_mod:                       # Accelerates ball based on paddle's movement on hit.
                accel_implement()
            if paddle_zone_mod:                 # Accelerates ball based on where on the paddle it hits.
                paddle_zone_implement()
            if color_change_mod:  # Randomly changes the ball's color on hit.
                color_change_implement()
            if random_bouncing_mod:             # Randomizes ball velocity on hit.
                random_bouncing_implement()

    # Redirect ball (instead of passing through) in cases where it hits the top or bottom sides of the R paddle.
    if (WINDOW_WIDTH - PADDLE_WIDTH < ballx < WINDOW_WIDTH) and (bally + BALL_RADIUS == ralt or bally - BALL_RADIUS == ralt + PADDLE_HEIGHT):
        ball_vy = (ball_vy * -1)
    if (0 < ballx < PADDLE_WIDTH) and (bally + BALL_RADIUS == lalt or bally - BALL_RADIUS == lalt + PADDLE_HEIGHT):
        ball_vy = (ball_vy * -1)


# Mods down below

def menu_mod_font():        # Sets up the visuals for mod toggling on menu screen.
    global accel_mod, paddle_zone_mod, color_change_mod, boost_pads_mod
    modlist = [accel_mod, paddle_zone_mod, color_change_mod, random_bouncing_mod, boost_pads_mod]
    modcount = 0
    while modcount < len(modlist):
        if modlist[modcount]:
            set_stroke_color(0, 1, 0)
            # Unicode help from http://stackoverflow.com/questions/10569438/how-to-print-unicode-character-in-python
            draw_text(u'\u2713', 300, 160 + (30 * modcount))    # Green check mark
        if not modlist[modcount]:
            set_stroke_color(1, 0, 0)
            draw_text(u"\u2717", 300, 160 + (30 * modcount))    # Red X mark
        set_stroke_color(1, 1, 1)
        modcount += 1


def accel_implement():      # Accelerates ball based on paddle directional input on hit.
    global ball_vy
    if not bot_mod:
        if is_key_pressed("a") or is_key_pressed("k"):
            ball_vy -= (MOVESPEED / 10)
        if is_key_pressed("z") or is_key_pressed("m"):
            ball_vy += (MOVESPEED / 10)
    if bot_mod:         # Mod does not apply to Right pad if played by AI, because it is constantly accelerating.
        if is_key_pressed("a") and ballx < 200:
            ball_vy -= (MOVESPEED / 10)
        if is_key_pressed("z") and ballx < 200:
            ball_vy += (MOVESPEED / 10)


def paddle_zone_implement():    # Accelerates ball based on where on the paddle it hits (higher = upwards acceleration)
    global ball_vy
    if ballx > (WINDOW_WIDTH / 2):  # Right paddle
        if ralt < bally < ralt + (PADDLE_HEIGHT / 3):
            ball_vy -= .4
        if (ralt + PADDLE_HEIGHT * 2 / 3) < bally < (ralt + PADDLE_HEIGHT):
            ball_vy += .4
    if ballx < (WINDOW_WIDTH / 2):  # Left paddle
        if lalt < bally < lalt + (PADDLE_HEIGHT / 3):
            ball_vy -= .4
        if (lalt + PADDLE_HEIGHT * 2 / 3) < bally < (lalt + PADDLE_HEIGHT):
            ball_vy += .4


def color_change_implement():           # Randomizes ball color on paddle hit.
    global randr, randg, randb
    randr = random.randint(10, 100)     # Lowest values are set to .1 so the ball is never too dark
    randg = random.randint(10, 100)
    randb = random.randint(10, 100)
    randr = (float(randr)) / 100
    randg = (float(randg)) / 100
    randb = (float(randb)) / 100


def random_bouncing_implement():        # Some randomization of ball velocity on paddle hit.
    global ball_vx, ball_vy             # Faster speed can occasionally glitch through paddles due to refresh rate.
    ball_vy = float(random.uniform(-3, 3))
    if ball_vx > 0:
        ball_vx = float(random.randint(1, 2))
    if ball_vx < 0:
        ball_vx = float(random.randint(-2, -1))


def boost_pads_implement():             # Adds boost pads to the table, which accelerate the ball when hit.
    global boost_up_x, boost_up_y, boost_down_x, boost_down_y, boost_stationary, ball_vy
    boost_up = load_image("boost.png")
    boost_down = load_image("boost2.png")
    if boost_stationary < 1:            # Sets random location for each booster with each point.
        boost_up_x = random.randint(100, 300)
        boost_up_y = random.randint(200, 300)   # Upwards booster appears in bottom half of screen.
        boost_down_x = random.randint(100, 300)
        boost_down_y = random.randint(50, 150)  # Downwards booster appears in upper half of screen.
        boost_stationary += 1
    draw_image(boost_up, boost_up_x, boost_up_y)
    if (boost_up_x <= ballx <= boost_up_x + 42) and (boost_up_y <= bally <= boost_up_y + 66):   # Accelerates ball.
        ball_vy -= BOOST_PAD_ACCELERATION
    draw_image(boost_down, boost_down_x, boost_down_y)
    if (boost_down_x <= ballx <= boost_down_x + 42) and (boost_down_y <= bally <= boost_down_y + 66):
        ball_vy += BOOST_PAD_ACCELERATION


def slam_jam_menu():        # Sets the Slam Jam mod's special menu screen text.
    if slam_jam_mod:
        set_font_size(15)
        set_stroke_color(0, 1, 0)
        draw_text("AND WELCOME", 295, 303)
        draw_text("TO THE JAM", 300, 314)
        set_font_size(20)
        set_stroke_color(1, 1, 1,)
    if not slam_jam_mod:
        set_stroke_color(1, 0, 0)
        draw_text(u"\u2717", 300, 310)
        set_stroke_color(1, 1, 1)


def slam_jam_implement():                                                   # Everybody get up
    court = load_image("resize court.jpg")                                  # It's time to slam now
    court_center = load_image("resize court center.png")                    # We got a real jam goin' down
    left_monstar_paddle = load_image("resize monstar.png")                  # Welcome to the Space Jam
    right_mj_paddle = load_image("resize mj.png")                           # Here's your chance
    bball = load_image("resize bball.png")                                  # Do your dance
    draw_image(court, 0, 0)                                                 # At the Space Jam,
    draw_image(court_center, 175, 150)                                      # Alright.
    draw_image(left_monstar_paddle, 0, lalt)                                # Come on and slam
    draw_image(right_mj_paddle, WINDOW_WIDTH - PADDLE_WIDTH, ralt)          # And welcome to the jam
    draw_image(bball, ballx, bally)                                         # Come on and slam
                                                                            #  If you wanna jam


start_graphics(menu_screen, 400, key_press=directive, framerate=FRAME_RATE)
