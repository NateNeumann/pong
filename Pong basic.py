# Basic Pong Program
# Written by Nate Neumann
# Devin Balkcom's CS 1 Class, Dartmouth College
# Lab 1: February 1st, 2017

from cs1lib import *

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
BALL_RADIUS = 5
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
L_UP_KEY = "a"      # Pressing the L_UP_KEY moves the left paddle up, and so on.
L_DOWN_KEY = "z"
R_UP_KEY = "k"
R_DOWN_KEY = "m"
MOVESPEED = 10      # Amount the paddles move per tick
FRAME_RATE = 60
BALL_START_X = 200  # Starting x- and y-coordinates of ball
BALL_START_Y = 10
BALL_START_VELOCITY_X = 1       # Starting horizontal and vertical speeds of ball
BALL_START_VELOCITY_Y = 1


lalt = 0        # Starting height of left paddle: top left corner at standard setup
ralt = (WINDOW_HEIGHT - PADDLE_HEIGHT)      # Starting height of right paddle: 320 at standard setup
ballx = BALL_START_X        # x-coord of ball at given point
bally = BALL_START_Y        # y-coord of ball at given point
ball_vx = BALL_START_VELOCITY_X     # x-velocity of ball at given point
ball_vy = BALL_START_VELOCITY_Y     # y-velocity of ball at given point
playing = True                     # Boolean-- game is running or not (True = Starts game)

# Defines the above values as the game's start state
start_state = [0, (WINDOW_HEIGHT - PADDLE_HEIGHT), BALL_START_X, BALL_START_Y, BALL_START_VELOCITY_X, BALL_START_VELOCITY_Y]


def paddles():  # This function draws the paddles and ball, based on the data from directive(key) and ball_velocity().
    global ballx, bally, ball_vx, ball_vy, playing, lalt, ralt
    if playing:
        set_clear_color(0, 0, 0)       # Black background
        set_fill_color(1, 1, 1)       # White paddles and ball
        set_stroke_color(1, 1, 1)
        clear()
        ball_velocity()
        draw_rectangle(0, lalt, PADDLE_WIDTH, PADDLE_HEIGHT)     # Left paddle
        draw_rectangle((WINDOW_WIDTH - PADDLE_WIDTH), ralt, PADDLE_WIDTH, PADDLE_HEIGHT)   # Right paddle
        draw_circle(ballx, bally, BALL_RADIUS)   # Ball
        ballx += ball_vx    # Ball movement is based on ball_vx and ball_vy
        bally += ball_vy
    if ballx > (WINDOW_WIDTH - BALL_RADIUS) or ballx < BALL_RADIUS:  # Ends game if ball hits vertical wall
        playing = False
    if is_key_pressed(" "):         # Resets game by pressing spacebar
        lalt, ralt, ballx, bally, ball_vx, ball_vy = start_state
        playing = True
    if is_key_pressed("q"):         # Quits game by pressing Q
        cs1_quit()


def directive(key):     # This function changes the height of the paddles based on keyboard inputs.
    global lalt, ralt
    ldown = is_key_pressed(L_DOWN_KEY)
    lup = is_key_pressed(L_UP_KEY)
    rdown = is_key_pressed(R_DOWN_KEY)
    rup = is_key_pressed(R_UP_KEY)

    if ldown and lalt <= (WINDOW_HEIGHT - PADDLE_HEIGHT - MOVESPEED):  # Prevents L paddle from moving down off screen
        lalt += MOVESPEED
    if lup and lalt >= MOVESPEED:   # Prevents L paddle from moving up offscreen
        lalt -= MOVESPEED

    if rdown and ralt <= (WINDOW_HEIGHT - PADDLE_HEIGHT - MOVESPEED):  # Prevents L paddle from moving down off screen
        ralt += MOVESPEED
    if rup and ralt >= MOVESPEED:   # Prevents L paddle from moving up offscreen
        ralt -= MOVESPEED


def ball_velocity():
    global ballx, bally, ball_vx, ball_vy, lalt, ralt

    # Top of ball hits top of screen or bottom hits bottom of screen: Ball's vertical velocity reverses.
    if (bally - BALL_RADIUS) == 0 or (bally + BALL_RADIUS) == WINDOW_HEIGHT:
        ball_vy = (ball_vy * -1)

    # Ball hits paddle (R or L): ball edge has same X-coord as paddle edge, and ball's y-coord is between paddle's ends
    if ((ballx + BALL_RADIUS) == (WINDOW_WIDTH - PADDLE_WIDTH) and (ralt + PADDLE_HEIGHT) >= bally >= ralt) or\
       ((ballx - BALL_RADIUS) == PADDLE_WIDTH and (lalt + PADDLE_HEIGHT) >= bally >= lalt):
            ball_vx = (ball_vx * -1)    # Ball's horizontal velocity reverses

    # Redirect ball (instead of passing through) in cases where it hits the top or bottom sides of the paddles.
        # Right paddle:
    if (WINDOW_WIDTH - PADDLE_WIDTH < ballx < WINDOW_WIDTH) and (bally + BALL_RADIUS == ralt or bally - BALL_RADIUS == ralt + PADDLE_HEIGHT):
        ball_vy = (ball_vy * -1)
        # Left paddle:
    if (0 < ballx < PADDLE_WIDTH) and (bally + BALL_RADIUS == lalt or bally - BALL_RADIUS == lalt + PADDLE_HEIGHT):
        ball_vy = (ball_vy * -1)

print("Controls:")
print("Left moves with A and Z.")
print("Right moves with K and M.")
print("Spacebar starts a new game.")
print("Q quits the program.")

start_graphics(paddles, 400, key_press=directive, framerate=FRAME_RATE)
