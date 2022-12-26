import modi
from threading import Timer
import pygame
from random import randint
import time
import os
import numpy as np
import pandas as pd
import joblib
from music import jingle_bells,sound2
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn import metrics

global gamepad, clock, msg, background
global here

#custom
global count
here = os.path.dirname(__file__)
WIDTH, HEIGHT = 1920, 1080


class Bulb:
    def __init__(self,bulb_category,mode):
        if mode == 0:
            self.bulb = []
        if mode == 2:
            self.pos_x, self.pos_y = randomize_bulb_all()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 3:
            self.pos_x, self.pos_y = randomize_bulb_left()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 4:
            self.pos_x, self.pos_y = randomize_bulb_right()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 5:
            self.pos_x, self.pos_y = randomize_bulb_bottom()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 6:
            self.pos_x, self.pos_y = randomize_bulb_middle()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 7:
            self.pos_x, self.pos_y = randomize_bulb_top()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 8:
            self.pos_x, self.pos_y = randomize_bulb_all()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]

def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
            
def play_sound(jinglebell_freq,jinglebell_sleep_list,rudolph_freq,rudolph_sleep_list,i):
    """
    argument : jinglebell_freq
                jinglebell_sleep_list
                rudolph_freq
                rudolph_sleep_list
                i
    """
    global mode
    i_for_jinglebell_freq = i % 93
    i_for_jinglebell_list = i % 93
    i_for_rudolph_freq = i % 96
    i_for_rudolph_sleep_list = i % 96
    if mode == 2:
        speaker.tune = jinglebell_freq[i_for_jinglebell_freq], 1000
        time.sleep(jinglebell_sleep_list[i_for_jinglebell_list])
    elif mode == 3:
        speaker.tune = rudolph_freq[i_for_rudolph_freq], 1000
        time.sleep(rudolph_sleep_list[i_for_rudolph_sleep_list])
    else:
        speaker.tune = 0, 0
    


def randomize_bulb_all():
    """divide tree in rectangle central +15"""
    random_position = randint(0,3)
    if random_position == 0:
        # Bottom rectangle
        pos_x = randint(WIDTH // 2 - 335, WIDTH // 2 + 365)
        pos_y = randint(750,800)
    if random_position == 1:
        # Middle 1 rectangle
        pos_x = randint(WIDTH // 2 - 235, WIDTH // 2 + 265)
        pos_y = randint(450,600)
    if random_position == 2:
        # Middle 2 rectangle
        pos_x = randint(WIDTH // 2 - 85, WIDTH // 2 + 115)
        pos_y = randint(300,400)
    if random_position == 3:
        # Top rectangle
        pos_x = randint(WIDTH // 2 - 35, WIDTH // 2 + 65)
        pos_y = randint(150,250)
    return pos_x, pos_y


def randomize_bulb_left():
    """divide tree in rectangle central +15"""
    random_position = randint(0,3)
    if random_position == 0:
        # Bottom rectangle
        pos_x = randint(WIDTH // 2 - 335, WIDTH // 2 + 15)
        pos_y = randint(750,800)
    if random_position == 1:
        # Middle 1 rectangle
        pos_x = randint(WIDTH // 2 - 235, WIDTH // 2 + 15)
        pos_y = randint(450,600)
    if random_position == 2:
        # Middle 2 rectangle
        pos_x = randint(WIDTH // 2 - 85, WIDTH // 2 + 15)
        pos_y = randint(300,400)
    if random_position == 3:
        # Top rectangle
        pos_x = randint(WIDTH // 2 - 35, WIDTH // 2 + 15)
        pos_y = randint(150,250)
    return pos_x, pos_y


def randomize_bulb_right():
    """divide tree in rectangle central +15"""
    random_position = randint(0,3)
    if random_position == 0:
        # Bottom rectangle
        pos_x = randint(WIDTH // 2 + 15, WIDTH // 2 + 365)
        pos_y = randint(750,800)
    if random_position == 1:
        # Middle 1 rectangle
        pos_x = randint(WIDTH // 2 + 15, WIDTH // 2 + 265)
        pos_y = randint(450,600)
    if random_position == 2:
        # Middle 2 rectangle
        pos_x = randint(WIDTH // 2 + 15, WIDTH // 2 + 115)
        pos_y = randint(300,400)
    if random_position == 3:
        # Top rectangle
        pos_x = randint(WIDTH // 2 + 15, WIDTH // 2 + 65)
        pos_y = randint(150,250)
    return pos_x, pos_y


def randomize_bulb_bottom():
    """divide tree in rectangle central +15"""
    # Bottom rectangle
    pos_x = randint(WIDTH // 2 - 335, WIDTH // 2 + 365)
    pos_y = randint(750,800)
    return pos_x, pos_y


def randomize_bulb_middle():
    """divide tree in rectangle central +15"""
    # Bottom rectangle
    pos_x = randint(WIDTH // 2 - 235, WIDTH // 2 + 265)
    pos_y = randint(450,600)
    return pos_x, pos_y


def randomize_bulb_top():
    """divide tree in rectangle central +15"""
    # Bottom rectangle
    pos_x = randint(WIDTH // 2 - 35, WIDTH // 2 + 65)
    pos_y = randint(150,250)
    return pos_x, pos_y


#Tree action
def btn_action(gamepad,font,button):
    global count, msg, speaker, mode
    """버튼 누를 때 Tree action
        한번 누르면 전구 다 끄기
        한번 더 누르면 전구 다 켜고 스피커 음악 출력 & 카운트 0"""
    
    if button.pressed:
        if count == 0:
            count = 1
            mode = 0
            msg = "Button Clear!"
        elif count == 1:
            count = 0
            msg = "Button All!"
            mode = 2


def gyro_act_left(gamepad,font,pred):
    global mode, msg
    """자이로 왼쪽으로 휘두르면
        왼쪽 전구 켜기"""
    if pred == 'L':
        #왼쪽 전구 켜기
        msg = "Gyro : left side!"
        mode = 3


def gyro_act_right(gamepad,font,pred):
    global mode, msg
    """자이로 오른쪽으로 휘두르면
        오른쪽 전구 켜기"""
    if pred == 'R':
        #오른쪽 전구 켜기
        msg = "Gyro : right side!"
        mode = 4


def mic_action(gamepad,font,vol):
    global mode, msg
    """mic 1단계 : 아래 전구 점등
    2단계 : 중간 전구 점등
    3단계 : 상단 전구 점등
    4단계 : 노란 별 전구 점등 노란 별 깜빡깜빡 & 스피커 노래 """
    if vol <= 10:
        #아래 전구 점등
        msg = "Low Level"
        mode = 5

    elif 10 < vol <= 20:
        #중간 전구 점등
        msg = "Middle Level"
        mode = 6

    elif 20 < vol <= 30:
        #상단 전구 점등
        msg = "High Level"
        mode = 7

    elif 30 < vol :
        #노란 별 전구 점등 & 스피커
        msg = "Super Level"
        mode = 8


def recv_gyro(gyro):
    realX = gyro.acceleration_x
    realY = gyro.acceleration_y
    realZ = gyro.acceleration_z
    real_data_dict = {
        "AX" : [realX],
        "AY" : [realY],
        "AZ" : [realZ]
    }
    real_data = pd.DataFrame(data=real_data_dict)    
    return real_data


def predict_model(real_data):
    """
    predict class of pose L or R
    """
    model_load = joblib.load('save_model.pkl') 
    value = model_load.predict(real_data)
    print(value)
    return value



def run_game(bundle):
    global gamepad, clock, background, msg, speaker,mode
    global count


    #MODI MODULE
    gyro = bundle.gyros[0]
    button = bundle.buttons[0]
    mic = bundle.mics[0]
    dial = bundle.dials[0]
    display = bundle.displays[0]
    speaker = bundle.speakers[0]


    mode = 0
    crashed = False
    count = 0
    msg = "Merry Christmas : Ready"
    font = pygame.font.Font(os.path.join(here, 'src/8bit.ttf'), 32)
    
    g = infinite_sequence()

    while not crashed:
        for event in pygame.event.get(): # 창 닫기 버튼 누르면 끝남 USEREVENT	사용자 설정 이벤트	code
            if event.type == pygame.QUIT:
                crashed = True
        gamepad.fill((255, 255, 255))
        gamepad.blit(background, (0, 0)) # 트리 띄우기
        gamepad.blit(font.render(str(msg), False,
                                    (0, 0, 0)), (WIDTH // 2 - 700, 130))
        #Mode 1
        if dial.degree <10:
            #text 띄우기  현재 action 띄우자
            display.text = "Ready"
            mode = 0

        #Mode 2
        if 10<dial.degree <30:
            #Tree btn action
            display.text = "Button Mode"
            btn_action(gamepad,font,button)
        

        #Mode 3
        if 30<dial.degree <55:
            #Tree gyro action
            display.text = "Gyroscope Mode"
            gyro_data = recv_gyro(gyro)
            pred = predict_model(gyro_data)
            gyro_act_left(gamepad,font,pred)
            gyro_act_right(gamepad,font,pred)
        
        
        #Mode 4
        if dial.degree > 60:
            #Tree mic action
            display.text = "Micro Phone Mode"
            mic_action(gamepad,font,mic.volume)


        #create msg and bulbs
        jinglebell_freq = [ 392,659,587,523,392
         ,392,659,587,523,440
         ,440,698,659,587,493
         ,783,783,698,587,659,523
         ,392,659,587,523,392
         ,392,659,587,523,440
         ,440,698,659,587,783,783,783,783
         ,880,783,698,587,523
         ,659,659,659,659,659,659
         ,659,783,523,587,659
         ,698,698,698,698,698,659,659,659
         ,659,587,587,523,587,783
         ,659,659,659,659,659,659
         ,659,783,523,587,659
         ,698,698,698,698,698,659,659,659
         ,783,783,698,587,523 ]
        jinglebell_sleep_list = [ 0.25,0.25,0.25,0.25,1
                  ,0.25,0.25,0.25,0.25,1
                  ,0.25,0.25,0.25,0.25,1
                  ,0.25,0.25,0.25,0.25,0.25,0.5
                  ,0.25,0.25,0.25,0.25,1
                  ,0.25,0.25,0.25,0.25,1
                  ,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25
                  ,0.25,0.25,0.25,0.25,0.5
                  ,0.25,0.25,0.5,0.25,0.25,0.5
                  ,0.25,0.25,0.375,0.125,1
                  ,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25
                  ,0.25,0.25,0.25,0.25,0.5,0.5
                  ,0.25,0.25,0.5,0.25,0.25,0.5
                  ,0.25,0.25,0.375,0.125,1
                  ,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25
                  ,0.25,0.25,0.25,0.25,0.25 ]
        rudolph_freq = [ 392,440,392,329,523
         ,440,392
         ,392,440,392,440,392,523
         ,493
         ,349,392,349,293,493
         ,440,392
         ,392,440,392,440,392,440
         ,329
         ,392,440,392,329,523
         ,440,392
         ,392,440,392,440,392,587
         ,523
         ,440,440,523,440
         ,392,329,392
         ,349,440,392,349,329
         ,293,329,392,440
         ,493,493,493
         ,523,523,493,440
         ,392,349,293
         ,392,440,392,329,523
         ,440,392
         ,392,440,392,440,392,1046
         ,987
         ,392,440,392,587,493
         ,440,392
         ,392,440,392,440,392,587
         ,523 ]
        rudolph_sleep_list = [0.25,0.5,0.25,0.5,0.5
                ,0.5,1.5
                ,0.25,0.25,0.25,0.25,0.5,0.5
                ,1.5
                ,0.25,0.5,0.25,0.5,0.5
                ,0.5,1.5
                ,0.25,0.25,0.25,0.25,0.5,0.5
                ,1.5
                ,0.25,0.5,0.25,0.5,0.5
                ,0.5,1.5
                ,0.25,0.25,0.25,0.25,0.5,0.5
                ,1.5
                ,0.5,0.5,0.5,0.5
                ,0.5,0.5,1.0
                ,0.5,0.5,0.5,0.5,1.5
                ,0.5,0.5,0.5,0.5
                ,0.5,0.5,1.0
                ,0.5,0.5,0.5,0.5
                ,0.5,0.5,1.0
                ,0.25,0.5,0.25,0.5,0.5
                ,0.5,1.5
                ,0.25,0.25,0.25,0.25,0.5,0.5
                ,1.0
                ,0.25,0.5,0.25,0.5,0.5
                ,0.5,1.5
                ,0.25,0.25,0.25,0.25,0.5,0.5
                ,1.5]

        
        print(f"jinglebell_freq : {len(jinglebell_freq)} \n jinglebell_sleep_list : {len(jinglebell_sleep_list)} \n rudolph_freq : {len(rudolph_freq)} \n rudolph_sleep_list : {len(rudolph_sleep_list)}")
        
        ########빛나고 소리
        iterator_generated = next(g)
        print(f"iterator_generated : {iterator_generated}")
        play_sound(jinglebell_freq,jinglebell_sleep_list,rudolph_freq,rudolph_sleep_list,iterator_generated)
        bulb_list = [Bulb(bulbs,mode) for _ in range(20)]
        if len(bulb_list[0].bulb) != 0:
            for bulb in bulb_list:
                    gamepad.blit(bulb.bulb[0],bulb.bulb[1])
        pygame.display.update()
        clock.tick(5)

    time.sleep(2)


    #pygame, pymodi 종료
    display.clear()
    time.sleep(0.1)
    pygame.quit()
    bundle._com_proc.terminate()


def init_game():
    global gamepad, clock, jet, background, bulbs, targets, star
    #MODI
    # bundle = modi.MODI()
    bundle = modi.MODI(conn_type='ble', network_uuid="6987F89E")
    #PYGAME
    pygame.init()
    gamepad = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Marry Cristmas")
    # jet = pygame.image.load(os.path.join(here, 'img/jet.png'))
    bulbs, targets, star = [], [], []
    bulbs.append(pygame.image.load(os.path.join(here, 'img/bluebulb.png')))
    bulbs.append(pygame.image.load(os.path.join(here, 'img/greenbulb.png')))
    bulbs.append(pygame.image.load(os.path.join(here, 'img/redbulb.png')))
    background = pygame.image.load(os.path.join(here, 'img/background.png'))
    clock = pygame.time.Clock()

    pygame.display.update()
    run_game(bundle)


if __name__ == "__main__":
    init_game()
