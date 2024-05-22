#coding: UTF-8
#By Hudson Huang 24/5/22

import sys
sys.path.append("/root/mindplus/.lib/thirdExtension/liao-soruxgpt_01-thirdex")
import time
from unihiker import GUI
from unihiker import Audio
from pinpong.board import Board
from df_xfyun_speech import XfIat
from pinpong.board import Board,Pin
from pinpong.extension.unihiker import *
import requests
import json
from PIL import Image
from pinpong.libs.dfrobot_huskylens import Huskylens
from pinpong.libs.dfrobot_speech_synthesis import DFRobot_SpeechSynthesis_I2C

# 自定义函数
def ZhuYe():
    while True:
        if p_huskylens.is_appear_direct("blocks"):
            u_gui.clear()
            u_gui.draw_text(text="按下P24返回主页",x=0,y=0,font_size=15, color="#0000FF")
            u_gui.draw_text(text="按下P21开始画图交互",x=0,y=20,font_size=15, color="#0000FF")
            u_gui.draw_image(image="chatgpt.png",x=95,y=145)
            u_gui.draw_text(text="P22重新画",x=0,y=290,font_size=15, color="#FF0000")
            p_gravitysynthesis.set_voice(9)
            p_gravitysynthesis.set_speed(4)
            p_gravitysynthesis.set_tone(5)
            p_gravitysynthesis.set_sound_type(p_gravitysynthesis.DONALDDUCK)
            p_gravitysynthesis.speak("你好，请问我吧")
            break
        else:
            u_gui.draw_text(text="请人脸解锁！",x=0,y=0,font_size=20, color="#0000FF")
            u_gui.draw_image(image="chatgpt.png",x=95,y=145)
def ShengChengTuPian():
    u_gui.clear()
    u_gui.draw_text(text="正在冥想，请稍等...",x=0,y=0,font_size=15, color="#0000FF")
    u_gui.draw_image(image="chatgpt.png",x=95,y=145)
    u_gui.draw_text(text=((str("你：")) + ShiBieFuZhi),x=0,y=35,font_size=15, color="#FF6600")
    YuYinBoBao()
    headers = {
                'Content-Type': 'application/json', # 根据需要设置其他header信息
                'Authorization': 'Bearer sk-juTnWeq8jOpCsRTGLyw1q29bUSJ9OZOnaWAQR52kMR5wq1Gl' # 在这里设置Authorization头部的值
        }
    data2={
                "model":"dall-e-3",
                "prompt":((str("请帮我生成英文艺术字图片")) + ShiBieFuZhi),
                "n":1
            }
    json_str2 = json.dumps(data2)
    url2='https://gpt.soruxgpt.com/api/api/v1/images/generations'

    SoruxGPT_wst("local_image.jpg",240,320)
    u_gui.draw_image(image="local_image.jpg",x=0,y=0)
    u_gui.draw_text(text="按B重新进行交互",x=0,y=0,font_size=15, color="#FF0000")
    u_gui.draw_text(text="P22引脚重新画",x=0,y=290,font_size=15, color="#0000FF")
def YuYinBoBao():
    p_gravitysynthesis.set_voice(9)
    p_gravitysynthesis.set_speed(5)
    p_gravitysynthesis.set_tone(5)
    p_gravitysynthesis.set_sound_type(p_gravitysynthesis.FEMALE)
    p_gravitysynthesis.speak(ShiBieFuZhi)


Board().begin()
appId = "6ad8c5ba"
apiKey ="5ef55f835720ffe1d70a14853f876a85"
apiSecret = "MzdmY2Q2OTgwN2UyZjExYjU4N2ZkZjRh"
u_gui=GUI()
u_audio = Audio()
options = {}
p_p24_in=Pin(Pin.P24, Pin.IN)
p_p21_in=Pin(Pin.P21, Pin.IN)
iat = XfIat(appId, apiKey, apiSecret)
p_p22_in=Pin(Pin.P22, Pin.IN)
p_gravitysynthesis = DFRobot_SpeechSynthesis_I2C()
p_gravitysynthesis.begin(p_gravitysynthesis.V1)
p_huskylens = Huskylens()
p_huskylens.command_request_algorthim("ALGORITHM_FACE_RECOGNITION")
def SoruxGPT_txt():
    try:
    # 发送POST请求
        response = requests.post(url=url,headers=headers, data=json_str)
        json_data = response.json()
        #print(json_data)
        txt=json_data['choices'][0]['message']['content']
        return txt # 打印返回的报文内容
    except Exception as e:
        return('Error occurred: ', str(e))
def SoruxGPT_wst(filename,new_width,new_height):
    # 发送POST请求
    response = requests.post(url=url2,headers=headers, data=json_str2)
    json_data2 = response.json()
    image_url=json_data2['data'][0]['url']
    response = requests.get(image_url)
    with open(filename, 'wb') as file:# 打开本地文件进行写入操作
        file.write(response.content)# 将图片内容写入本地文件
    image = Image.open(filename)
    resized_image = image.resize((new_width, new_height))
    # 保存修改后的图片
    resized_image.save(filename)

ZhuYe()

while True:
    if p_p24_in.read_digital():
        u_gui.clear()
        ZhuYe()
    if p_p21_in.read_digital():
        u_gui.clear()
        u_gui.draw_image(image="chatgpt.png",x=95,y=145)
        u_gui.draw_text(text="正在录制 3s",x=0,y=0,font_size=15, color="#FF0000")
        u_audio.start_record("record.wav")
        time.sleep(3)
        u_audio.stop_record()
        u_gui.clear()
        time.sleep(2)
        u_gui.draw_text(text="正在冥想，请稍等...",x=0,y=0,font_size=15, color="#0000FF")
        u_gui.draw_image(image="chatgpt.png",x=95,y=145)
        ShiBieFuZhi = iat.recognition("record.wav")
        u_gui.draw_text(text=((str("你：")) + ShiBieFuZhi),x=0,y=35,font_size=15, color="#FF6600")
        YuYinBoBao()
        headers = {
                    'Content-Type': 'application/json', # 根据需要设置其他header信息
                    'Authorization': 'Bearer sk-juTnWeq8jOpCsRTGLyw1q29bUSJ9OZOnaWAQR52kMR5wq1Gl' # 在这里设置Authorization头部的值
            }
        data2={
                    "model":"dall-e-3",
                    "prompt":((str("请帮我生成英文艺术字图片")) + ShiBieFuZhi),
                    "n":1
                }
        json_str2 = json.dumps(data2)
        url2='https://gpt.soruxgpt.com/api/api/v1/images/generations'

        SoruxGPT_wst("local_image.jpg",240,320)
        u_gui.draw_image(image="local_image.jpg",x=0,y=0)
        u_gui.draw_text(text="按B重新进行交互",x=0,y=0,font_size=15, color="#FF0000")
        u_gui.draw_text(text="P22引脚重新画",x=0,y=290,font_size=15, color="#0000FF")
    if p_p22_in.read_digital():
        ShengChengTuPian()
