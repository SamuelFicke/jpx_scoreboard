import math
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

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
            away_ones_data = away_ones_bits[6]#One of my MOSFETS broke...shitty fix because I don't have any more
            
        else:
            print(int(away_tens_bits[ii]))
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
