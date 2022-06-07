#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT


GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)# countdown_timer button to GPIO20 
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)# clock_stop button to GPIO21 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)# stopwatch_stop button to GPIO23
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)# start_stopwatch button to GPIO24


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=90)
device.contrast(16)
virtual = viewport(device, width=32, height=16)


def minute_change(device):
    '''When we reach a minute change, animate it.'''
    hours = datetime.now().strftime('%H')
    minutes = datetime.now().strftime('%M')

    def helper(current_y):
        with canvas(device) as draw:
            text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (17, current_y), minutes, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
    for current_y in range(1, 9):
        helper(current_y)
    minutes = datetime.now().strftime('%M')
    for current_y in range(9, 1, -1):
        helper(current_y)


def animation(device, from_y, to_y):
    
    '''Animate the whole thing, moving it into/out of the abyss.'''
    hourstime = datetime.now().strftime('%H')
    mintime = datetime.now().strftime('%M')
    current_y = from_y
    while current_y != to_y:
        with canvas(device) as draw:
            text(draw, (0, current_y), hourstime, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, current_y), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (17, current_y), mintime, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
        current_y += 1 if to_y > from_y else -1



def countdown_timer(channel):
           
    print ("Timer is started")

    loop = 11

    for i in range(1,11):
    
        loop -= 1
        count = str(loop)
        lowerlimit = 8
        upperlimit = -1
        currentlimit = lowerlimit
    
        while currentlimit != upperlimit:
        
            with canvas(device) as draw:
                if (loop>9):
                    text(draw, (0,0), chr(i+200), fill="white")
                    text(draw, (9,currentlimit), count, fill="white")
                    text(draw, (24,0), chr(i+200), fill="white")
                elif (loop<10 and loop>3):                    
                    text(draw, (0,0), chr(i+200), fill="white")
                    text(draw, (13,currentlimit), count, fill="white")
                    text(draw, (25,0), chr(i+200), fill="white")
                elif(loop<4):
                    text(draw, (0,0), chr(3), fill="white")
                    text(draw, (13,currentlimit), count, fill="white")
                    text(draw, (25,0), chr(3), fill="white")
                                                
            currentlimit +=1 if upperlimit > lowerlimit else -1
            sleep(0.05)
            status = False
        sleep(0.5)
        status = False
   
    show_message(device, 'Happy New Year', fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
    sleep(2)
    clock()
    
    
def stop_watch(channel):
        
    print ("stopwatch is started")
    Second = 0
    sec = 0
    sec1 = '0'
    Second1 ='0'
    toggle = True
    
    while True:
        toggle = not toggle
        secc = datetime.now().second
        sec = sec+1
        if sec == 59:
            # When we change minutes, animate the minute change
            Second= Second+1
            sec = 0
        with canvas(device) as draw:
            Second1 = str(Second)
            sec1 = str(sec)
            if(Second >9):
                text(draw, (0, 1), Second1, fill="white", font=proportional(CP437_FONT))
                text(draw, (15, 1), ":" , fill="white", font=proportional(TINY_FONT))
                text(draw, (17, 1), sec1, fill="white", font=proportional(CP437_FONT))
            else:    
                text(draw, (7, 1), Second1, fill="white", font=proportional(CP437_FONT))
                text(draw, (15, 1), ":" , fill="white", font=proportional(TINY_FONT))
                text(draw, (17, 1), sec1, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.01)
        button_state1 = 1
        button_state1 = GPIO.input(20)
        if (button_state1 == False):
        
            print('stopwatch stop Button Pressed...')
            break;
        
    with canvas(device) as draw:
        
        Second1 = str(Second)
        sec1 = str(sec)
        if(Second >9):
            text(draw, (0, 1), Second1, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, 1), ":" , fill="white", font=proportional(TINY_FONT))
            text(draw, (17, 1), sec1, fill="white", font=proportional(CP437_FONT))
        else:    
            text(draw, (7, 1), Second1, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, 1), ":" , fill="white", font=proportional(TINY_FONT))
            text(draw, (17, 1), sec1, fill="white", font=proportional(CP437_FONT))
    sleep(2)
     
    clock()

    
def clock():
    
    print ("clock is started")
    # The time ascends from the abyss...
    animation(device, 8, 1)
    button_state2 = True
    toggle = True # Toggle the second indicator every second
    
    while True:
        
        button_state2 = GPIO.input(24)
        if button_state2 == False:
             print('Stop Button Pressed...')
             break;
        toggle = not toggle
        sec = datetime.now().second
        if sec == 59:
            # When we change minutes, animate the minute change
            minute_change(device)
        elif sec == 30:

            full_msg = time.ctime()
            animation(device, 1, 8)
            show_message(device, full_msg, fill="white", font=proportional(CP437_FONT))
            animation(device, 8, 1)
        else:

            hours = datetime.now().strftime('%H')
            minutes = datetime.now().strftime('%M')
            with canvas(device) as draw:
                text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
                text(draw, (15, 1), ":" if toggle else " ", fill="white", font=proportional(TINY_FONT))
                text(draw, (17, 1), minutes, fill="white", font=proportional(CP437_FONT))
            time.sleep(0.5)
     


def main():
         
    clock()
    
    GPIO.add_event_detect(23, GPIO.RISING, callback=countdown_timer, bouncetime=300)
    
    GPIO.add_event_detect(21, GPIO.RISING, callback=stop_watch, bouncetime=300)
        

if __name__ == "__main__":
    main()
