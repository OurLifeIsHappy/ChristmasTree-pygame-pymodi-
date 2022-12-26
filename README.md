# Galaga with PyMODI

<p align="center">
    <img src="https://github.com/OurLifeIsHappy/ChristmasTree-pygame-pymodi-/tree/main/img/Ready.png" width=200 height=300> 
    <img src="https://github.com/OurLifeIsHappy/ChristmasTree-pygame-pymodi-/tree/main/img/btn.png" width=200 height=300> 
    <img src="https://github.com/k2sebeom/pymodi_galaga/blob/master/src/gyro.JPG" width=200 height=300> 
</p>

<p align="center">
    Enjoy your christmas using this system with Luxrobo!!
<p>

--------

PyMODI is an open source library that uses python to control MODI modules developed by LuxRobo.
<https://github.com/LUXROBO/pymodi>

With a custom-made game console which consists of 6 MODI modules, the game, "Galaga with PyMODI," provides a fully immersive gaming experience to all the gamers around the world.

## Introduction

MODI is a technology of integrable robotic modules developed and produced by a Korean venture company, <a href="https://modi.luxrobo.com/">LuxRobo Co., Ltd.<a>. 

<p align="center">
    <img src="https://modi.luxrobo.com/img/main/friends01.jpg" width=300 height=200>    
</p>

There are several different modules such as speaker, gyro, motor, mic, and infrared sensor, all of which can be controlled by MODI compatible softwares. PyMODI is an open source python library designed to control MODI modules. Galaga_with_PyMODI uses the PyMODI library to control a console made by MODI technology.

## Structure

In terms of a backend, PyMODI uses two different open-source python libraries.
<ul>
    <li>PyMODI: https://github.com/LUXROBO/pymodi</li>
    <li>PyGame: https://github.com/pygame/pygame</li>
</ul>

PyGame is used to construct a mainframe of the game, and PyMODI is used to get inputs from a MODI controller.

The controller of the game is a DIY MODI controller that consists of 5 MODI modules.
<ul>
    <li>Network module</li>
    <li>Speaker module</li>
    <li>Mic module</li>
    <li>Gyro module</li>
    <li>Button module</li>
    <li>Dial module</li>
</ul>

Connect all 6 modules like the following image.

<p align="center">
    <img src="https://github.com/OurLifeIsHappy/ChristmasTree-pygame-pymodi-/tree/main/img/hardware.jpg" width=300 height=250> 
</p>


## How to Play

First, clone the repository to your local device.

    $ git clone https://github.com/OurLifeIsHappy/ChristmasTree-pygame-pymodi-

Then, you need to download two python libraries.

    $ pip install pymodi
    $ pip install pygame
 
Once you have all the files, prepare your MODI controller prepared as explained above. Connect the controller to your device, and start the game!

    $ python main.py
    
