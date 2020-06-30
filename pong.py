import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
width = 600
height = 400       
ball_radius = 20
pad_width = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True
ball_vel=[0,0]
paddle1_pos=paddle2_pos=200
paddle1_vel=paddle2_vel=[0,0]
a=b=0
single_player = True
started_now = 500
# initialize ball_pos and ball_vel for new bal in middle of table

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[width/2,height/2]
    if direction==RIGHT:
        ball_vel[0]= random.randrange(2,4)
        ball_vel[1]= random.randrange(-3,-2)
    if direction==LEFT:
        ball_vel[0]= random.randrange(-4,-2)
        ball_vel[1]= random.randrange(-3,-2)

# define event handlers
def new_game():
    spawn_ball(RIGHT)
    global a,b,paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos=paddle2_pos=200
    a=b=0
def draw(canvas):
    global a,b,score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, started_now
    c=str(a)
    d=str(b)

    #ask for number of players before starting
    if started_now >= 0 :
        canvas.draw_text("Press 1 for single player, 2 for two players",[60,70],30,'White')
        canvas.draw_text(str(started_now),[290,200],40,'White')
        started_now = started_now - 1
    else :
        # draw mid line and gutters
        canvas.draw_line([width / 2, 0],[width / 2, height], 1, "White")
        canvas.draw_line([pad_width, 0],[pad_width, height], 1, "White")
        canvas.draw_line([width - pad_width, 0],[width - pad_width, height], 1, "White")
        canvas.draw_text(c,[70,70],30,'White')
        canvas.draw_text(d,[510,70],30,'White')
        # update ball
        if ball_vel[0]>0:
            ball_vel[0]=ball_vel[0]+0.005
        if ball_vel[0]<0:
            ball_vel[0]=ball_vel[0]-0.005
        ball_pos[0] +=ball_vel[0]
        ball_pos[1] +=ball_vel[1]
        if ball_pos[1]<=ball_radius:
            ball_vel[1]=-ball_vel[1]
        elif ball_pos[1]>=400-ball_radius:
            ball_vel[1]=-ball_vel[1]
        if ball_pos[1]>=(paddle1_pos-47) and ball_pos[1]<=(paddle1_pos+47) and ball_pos[0]<=(8+ball_radius):
            ball_vel[0]=-ball_vel[0]
        if ball_pos[1]>=(paddle2_pos-47) and ball_pos[1]<=(paddle2_pos+47) and ball_pos[0]>=(600-8-ball_radius):
            ball_vel[0]=-ball_vel[0]
        if ball_pos[0]<=ball_radius:
            b=b+1
            spawn_ball(RIGHT)
        elif ball_pos[0]>=(600-ball_radius):
            a=a+1
            spawn_ball(LEFT)
        # draw ball
        canvas.draw_circle(ball_pos,ball_radius,2,"RED","WHITE")
        # update paddle's vertical position, keep paddle on the screen
        if paddle1_pos>=40 and paddle1_pos<=360 :
            paddle1_pos=paddle1_pos+paddle1_vel[1]
        if paddle2_pos>=40 and paddle2_pos<=360:    
            paddle2_pos=paddle2_pos+paddle2_vel[1]
        if paddle1_pos<40 and paddle1_vel[1]>0:
            paddle1_pos=paddle1_pos+paddle1_vel[1]
        if paddle2_pos<40 and paddle2_vel[1]>0:
            paddle2_pos=paddle2_pos+paddle2_vel[1]
        if paddle1_pos>360 and paddle1_vel[1]<0:
            paddle1_pos=paddle1_pos+paddle1_vel[1]
        if paddle2_pos>360 and paddle2_vel[1]<0:
            paddle2_pos=paddle2_pos+paddle2_vel[1]
        
        #check for players
        if single_player == True :
            paddle2_pos = ball_pos[1]
        # draw paddles
        canvas.draw_polygon([[0,paddle1_pos-40],[8,paddle1_pos-40],[8,paddle1_pos+40],[0,paddle1_pos+40]],1,"WHITE","WHITW")
        canvas.draw_polygon([[592,paddle2_pos-40],[600,paddle2_pos-40],[600,paddle2_pos+40],[592,paddle2_pos+40]],1,"WHITE","WHITW")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, single_player
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel=[0,5.5]
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel=[0,-5.5]
    if key==simplegui.KEY_MAP['w']:
        paddle1_vel=[0,-5.5]
    if key==simplegui.KEY_MAP['s']:
        paddle1_vel=[0,5.5]
    if key==simplegui.KEY_MAP['space']:
        new_game()
    if key==simplegui.KEY_MAP['1']:
        single_player = True
    if key==simplegui.KEY_MAP['2']:
        single_player = False
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"] or key==simplegui.KEY_MAP["up"]:
        paddle2_vel=[0,0]
    if key==simplegui.KEY_MAP['w'] or key==simplegui.KEY_MAP['S']:
        paddle1_vel=[0,0]
# create frame
frame = simplegui.create_frame("Pong", width, height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
frame.start()
new_game()