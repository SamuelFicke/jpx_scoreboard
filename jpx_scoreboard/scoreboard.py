import os
import time
import math
import pyttsx3
from sixAxis import *
import RPi.GPIO as GPIO

winning_score = 11

seven_seg_map = [ '1111110', #0
                  '0110000', #1
                  '1101101', #2
                  '1111001', #3
                  '0110011', #4
                  '1011011', #5
                  '1011111', #6
                  '1110000', #7
                  '1111111', #8
                  '1111011'] #9

SRClk       = 12
RClk        = 16
Home_Tens   = 32
Home_Ones   = 36
Away_Tens   = 38
Away_Ones   = 40

GPIO.setmode(GPIO.BOARD)

GPIO.setup(SRClk,GPIO.OUT)
GPIO.setup(RClk,GPIO.OUT)
GPIO.setup(Home_Tens,GPIO.OUT)
GPIO.setup(Home_Ones,GPIO.OUT)
GPIO.setup(Away_Tens,GPIO.OUT)
GPIO.setup(Away_Ones,GPIO.OUT)
                  
def set_seven_segs(away,away_dec,away_enable,home,home_dec,home_enable):
    
    home_tens = (home//10) % 10
    home_ones = home % 10
    away_tens = (away//10) % 10
    away_ones = away % 10
    
    
    if(home_enable):
        home_tens_bits = seven_seg_map[home_tens]
        home_ones_bits = seven_seg_map[home_ones]
    else:
        home_tens_bits = '0000000'
        home_ones_bits = '0000000'
        
    if(away_enable):
        away_tens_bits = seven_seg_map[away_tens]
        away_ones_bits = seven_seg_map[away_ones]
    else:
        away_tens_bits = '0000000'
        away_ones_bits = '0000000'
        
    
    for ii in range(7,-1,-1):
        if(ii == 7):
            home_tens_data = home_dec
            home_ones_data = 0
            away_tens_data = away_dec
            away_ones_data = away_ones_bits[5]#One of my MOSFETS broke...shitty fix because I don't have any more
            
        else:
            home_tens_data = home_tens_bits[ii]
            home_ones_data = home_ones_bits[ii]
            away_tens_data = away_tens_bits[ii]
            away_ones_data = away_ones_bits[ii]

        GPIO.output(Home_Tens,int(home_tens_data))
        GPIO.output(Home_Ones,int(home_ones_data))
        GPIO.output(Away_Tens,int(away_tens_data))
        GPIO.output(Away_Ones,int(away_ones_data))

        GPIO.output(SRClk,1)
        GPIO.output(SRClk,0)
        
    GPIO.output(RClk,1)
    GPIO.output(RClk,0)
            
        

#Blinks winner's score
def blink(team,num_blinks):
    if(team=="home"):
        for ii in range(num_blinks):
            set_seven_segs(away_score,0,1,home_score,0,1)
            time.sleep(0.25)
            set_seven_segs(away_score,0,1,home_score,0,0)
            time.sleep(0.25)
    else:
        for ii in range(num_blinks):
            set_seven_segs(away_score,0,1,home_score,0,1)
            time.sleep(0.25)
            set_seven_segs(away_score,0,0,home_score,0,1)
            time.sleep(0.25)

#Function to run a timer after a button is pressed
def set_timer(seconds,team):
    #Convert seconds to deciseconds to display tenths
    time_left = seconds*10

    #Set timer on side of winner
    if(team == "home"):
        set_seven_segs(away_score,0,1,time_left,1,1)
    else:
        set_seven_segs(time_left,1,1,home_score,0,1)

    #Wait for input to start timer
    events = controller.getEvents() #clear out events queue
    events = []
    print("Waiting on input from controller")
    while(len(events) == 0):
        events = controller.getEvents()
        time.sleep(0.1)

    audio.say("3. 2. 1. GO")
    audio.runAndWait()
    end = time.time() + seconds
    while(time_left > 0):
        time_left = int(math.ceil((end - time.time())*10))
        if(team == "home"):
            set_seven_segs(away_score,0,1,time_left,1,1)
        else:
            set_seven_segs(time_left,1,1,home_score,0,1)
    audio.say("Stop Drinking, Bitch!")
    audio.runAndWait()
    set_seven_segs(away_score,0,1,home_score,0,1)
        
        
        
    



audio = pyttsx3.init()
    
#Main Code Below


home_score      = 0
away_score      = 0
score_checked   = 0
set_seven_segs(away_score,0,1,home_score,0,1)

while(1):
    #Make Sure The Controller is connected (or reconnect if something tragic happens)
    controller = sixAxis()
    while(controller.connected == False):
        audio.say("Waiting To Pair!")
        audio.runAndWait()
        set_seven_segs(99,0,1,99,0,1)
        time.sleep(1)
        controller = sixAxis()

    #Main game loop
    while(controller.connected == True):
        buttons_pressed = controller.getEvents()

        for button in buttons_pressed:
            
            #dpad up and down control away score
            if(button == "dpad_up" and away_score < 99):
                away_score += 1
            elif(button == "dpad_down" and away_score > 0):
                away_score -= 1

            #triangle and x control home score
            elif(button == "triangle" and home_score < 99):
                home_score += 1
            elif(button == "x" and home_score > 0):
                home_score -= 1

            #select button sets two second timer
            elif(button == "select"):
                set_timer(2,"home")
                
            print("Home:" + str(home_score) + " - Away:" + str(away_score))
            set_seven_segs(away_score,0,1,home_score,0,1)
            if(button != "select"):
                score_checked = 0
            
        if(score_checked == 0 and ((home_score == 9 and away_score == 6) or (home_score == 6 and away_score == 9))):
            audio.say("Nice!")
            audio.runAndWait()
            score_checked = 1
        
        if(home_score > winning_score-1 or away_score > winning_score-1):
            if(abs(home_score - away_score) > 1):
                if(home_score > away_score):
                    blink("home",5)
                    set_timer(5,"home")
                else:
                    blink("away",5)
                    set_timer(5,"away")
                home_score = 0
                away_score = 0
                set_seven_segs(away_score,0,1,home_score,0,1)
