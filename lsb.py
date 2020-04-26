#!/usr/bin/env Python3
import PySimpleGUI as sg
from PIL import Image
from PIL import ImageFile
#Require PySimpleGUI and Pillow packages

ImageFile.LOAD_TRUNCATED_IMAGES = True

# GUI Styles
sg.ChangeLookAndFeel('GreenTan')

layout = [[sg.Text('通过LSB图片隐写实现的文本加解密')],
          [sg.Text('选择照片:', size=(8, 1)), sg.Input(), sg.FileBrowse()],
          [sg.Text('加密文本:', size=(8, 1)), sg.InputText()],
          [sg.Button('加密'), sg.Button('解密'), sg.Button('退出')]]

window = sg.Window('LSB图片隐写', layout)


# LSB main
def full_eight(str):
    return str.zfill(8)


def get_text_bin(str):
    string = ""
    s_text = str.encode()
    for i in range(len(s_text)):
        string = string + full_eight(bin(s_text[i]).replace('0b', ''))
    return string


def mod(x, y):
    return x % y


def encrypt(str1, str2, str3):
    im = Image.open(str1)
    width = im.size[0]
    height = im.size[1]
    count = 0
    key = get_text_bin(str2)
    keylen = len(key)
    for h in range(0, height):
        for w in range(0, width):
            pixel = im.getpixel((w, h))
            a = pixel[0]
            b = pixel[1]
            c = pixel[2]
            if count == keylen:
                break
            a = a - mod(a, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            b = b - mod(b, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            c = c - mod(c, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            if count % 3 == 0:
                im.putpixel((w, h), (a, b, c))
    im.save(str3)


def decrypt(le, str1):
    a = ""
    b = ""
    im = Image.open(str1)
    lenth = le * 8
    width = im.size[0]
    height = im.size[1]
    count = 0
    for h in range(0, height):
        for w in range(0, width):
            pixel = im.getpixel((w, h))
            if count % 3 == 0:
                count += 1
                b = b + str((mod(int(pixel[0]), 2)))
                if count == lenth:
                    break
            if count % 3 == 1:
                count += 1
                b = b + str((mod(int(pixel[1]), 2)))
                if count == lenth:
                    break
            if count % 3 == 2:
                count += 1
                b = b + str((mod(int(pixel[2]), 2)))
                if count == lenth:
                    break
        if count == lenth:
            break
    st = ""
    for i in range(0, len(b), 8):
        stra = int(b[i:i + 8], 2)
        st += chr(stra)
    return st


while True:
    event, values = window.read()
    if event in (None, '退出'):
        break
    elif event == '加密':
        print(f'You clicked {event}')
        print(f'You chose filenames {values[0]} and {values[1]}')
        try:
            old = values[0]
            print(old)
            keywords = values[1]
            keywords = keywords + "#"
            print(keywords)
            new = values[0][:-4] + "new.png"
            print(new)
            encrypt(old, keywords, new)
            print("Fun Picture done!")
            sg.popup("成功!", "图片加密后保存在:" + new)
        except:
            sg.popup("错误!", "运行错误，请检查图片格式（PNG）或图片路径是否正确")
    elif event == '解密':
        print(f'You clicked {event}')
        print(f'You chose filenames {values[0]} and {values[1]}')
        le = 30
        try:
            new = values[0]
            word = decrypt(le, new).split('#')
            sg.popup("成功!", "解密的文本为:" + word[0])
        except:
            sg.popup("错误!", "运行错误，请检查图片格式（PNG）或图片路径是否正确")
