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
        if mode == 1:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 2:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 3:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 4:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 5:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 6:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 7:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        if mode == 7:
            self.pos_x, self.pos_y = randomize_bulb()
            self.bulb = [bulb_category[randint(0,2)],(self.pos_x,self.pos_y)]
        
            

def randomize_bulb():
    """divide tree in rectangle"""
    random_position = randint(0,3)
    if random_position == 0:
        # Bottom rectangle
        pos_x = randint(WIDTH // 2 - 400, WIDTH // 2 + 400)
        pos_y = randint(500,600)
    if random_position == 1:
        # Middle 1 rectangle
        pos_x = randint(WIDTH // 2 - 300, WIDTH // 2 + 300)
        pos_y = randint(300,400)
    if random_position == 2:
        # Middle 2 rectangle
        pos_x = randint(WIDTH // 2 - 200, WIDTH // 2 + 200)
        pos_y = randint(200,300)
    if random_position == 3:
        # Top rectangle
        pos_x = randint(WIDTH // 2 - 100, WIDTH // 2 + 100)
        pos_y = randint(100,200)
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
            gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
            #전구 다 끄기
        elif count == 1:
            count = 0
            msg = "Button All!"
            gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
            mode = 2


def gyro_act_left(gamepad,font,pred):
    global mode
    """자이로 왼쪽으로 휘두르면
        왼쪽 전구 켜기"""
    if pred == 'L':
        #왼쪽 전구 켜기
        msg = "Gyro : left side!"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 3


def gyro_act_right(gamepad,font,pred):
    global mode
    """자이로 오른쪽으로 휘두르면
        오른쪽 전구 켜기"""
    if pred == 'R':
        #오른쪽 전구 켜기
        msg = "Gyro : right side!"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 4


def mic_action(gamepad,font,freq):
    global mode
    """mic 1단계 : 아래 전구 점등
    2단계 : 중간 전구 점등
    3단계 : 상단 전구 점등
    4단계 : 노란 별 전구 점등 노란 별 깜빡깜빡 & 스피커 노래 """
    if freq <= 100:
        #아래 전구 점등
        msg = "Low Level"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 5

    elif 100 < freq <= 200:
        #중간 전구 점등
        msg = "Middle Level"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 6

    elif 200 < freq <= 300:
        #상단 전구 점등
        msg = "High Level"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 7

    elif 300 < freq :
        #노란 별 전구 점등 & 스피커
        msg = "Super Level"
        gamepad.blit(font.render(str(msg), False,
                        (0, 0, 0)), (WIDTH // 2 - 700, 130))
        mode = 8
    sound2(speaker)


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
            mic_action(gamepad,font,mic.frequency)


        #create msg and bulbs
        
        
        bulb_list = [Bulb(bulbs,mode) for _ in range(10)]
        print(f"bulb_list : {bulb_list}")
        if len(bulb_list[0].bulb) != 0:
            for bulb in bulb_list:
                # print(f"mode{mode}")
                print(bulb.bulb)
                gamepad.blit(bulb.bulb[0],bulb.bulb[1])
                if dial.degree<10:
                    break

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
    bundle = modi.MODI(conn_type='ble',network_uuid="6987F89E")
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
