from datetime import datetime
import time
import RPi.GPIO as GPIO

import requests

# インターバル
INTERVAL = 1
# スリープタイム
SLEEPTIME = 2
# リセットタイム
RESETTIME = 10
# 使用するGPIO
GPIO_PIN = 18
#トイレに人がいるかどうか(in = 1, out = 0)
PEOPLE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

def ifttt_line(eventid1):
    payload = {'value1':"human toilet!!",'value2':"http://www.yahoo.co.jp",'value3':str("Use Time:{0:.2f}, {1}, {2}".format(time.time(), "YEAH!", "HEY!!"))}   
    url = "https://maker.ifttt.com/trigger/" + eventid1 + "/with/key/iv0CKAyFDavdwqCpJpxladqDQzf7ueSCarIlk70n1tq"
    response = requests.post(url, data=payload)

def ifttt_spred(eventid2):
    payload = {'value1':"human toilet!!",'value2':PEOPLE,'value3':str("Use Time:{0:.2f}, {1}, {2}".format(time.time(), "YEAH!", "HEY!!"))}   
    url = "https://maker.ifttt.com/trigger/" + eventid2 + "/with/key/iv0CKAyFDavdwqCpJpxladqDQzf7ueSCarIlk70n1tq"
    response = requests.post(url, data=payload)

if __name__ == '__main__':
    try:
        print ("処理キャンセル：CTRL+C")
        cnt = 1   #Toilet Count
        #t1 = time.time()
        NoActionTime = 0
        
        while True:
            
            # センサー感知
            if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
                print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') +
                    "：" + str("{0:05d}".format(cnt)) + "回目の人感知")

                if(PEOPLE == 0):   #センサー反応時人がいない場合
                     PEOPLE = 1    #いることにする
                     cnt = cnt + 1
                     print("うんこ IN!!")
                     NoActionTime = 0
                     time.sleep(SLEEPTIME)
                else:              #センサー反応時人がいる場合
                     PEOPLE = 0    #いないことにする
                     print("うんこ OUT!!")
                     NoActionTime = 0
                     time.sleep(SLEEPTIME)

                # IFTTT_Webhook
                ifttt_line("line_event")
                ifttt_spred("spred-event")
                  
            if (PEOPLE == 1) and (NoActionTime >= 600):   #人がいない状態で10分間リアクションがない時
                PEOPLE = 0
                print("そして誰もいなくなった...")
                NoActionTime = 0




            NoActionTime = NoActionTime + 1   #NoActionTme increment
            time.sleep(INTERVAL)

            print(str(GPIO.input(GPIO_PIN)) + " : " + str(NoActionTime) + " ; PEOPLE:" + str(PEOPLE))


    except KeyboardInterrupt:
        print("終了処理中...")  
        
    finally:
        GPIO.cleanup()
        print("GPIO clean完了")
