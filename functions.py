from os import system as syst
import os
from time import sleep


def layout():
    syst('cls')
    print("*"*97)
    print("* "*20+" M I N I G R A M "+' *'*20)
    print('*'*97+'\n')

def loading(Start,Text,Time):
    sleep(Start)
    for i in range(Time):
        layout()
        print(Text+' in '+str(Time-i)+' seconds....')
        sleep(1)


if __name__ == '__main__':

    layout()
    loading(1,"Just for sampling",1)

    path = "C:\\Users\\User\\Desktop\\MiniGram\\my_image.jpg"
    



