import os,time
try:
 import threading,subprocess,base64,cv2,random
 import numpy as np
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
import threading,subprocess,base64,cv2,random
import numpy as np
from datetime import datetime

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")
    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
    def find(self,img='',template_pic_name=False,threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle+'.png'
        else:
            self.screen_capture(template_pic_name)
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data

def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
        
GetDevices()
thread_count = len(GetDevices())

print(GetDevices())

class starts(threading.Thread):
    def __init__(self, nameLD, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
    def run(self):
        device = self.device
        d = Auto(device)

        print('test')

        # def memus():
        #     print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m nhap 1 dê mo Face | Time:", time.ctime(time.time()))
        #     print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
        #     print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
        #     memusn = int(input("Nhap memu can chon: "))
        #     if memusn ==1:
        #         step1(d)
        #     if memusn ==2:
        #         step2(d)
            
        # def step2(d):
        #     while True:
        #         try:
        #             poin  = d.find('2.png')
        #             if poin > [(0, 0)] :
        #                 d.click(poin[0][0],poin[0][1])
        #                 memus()
        #                 print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
        #                 break
        #         except:
        #             return 0
        # def step1(d):
        #     while True:
        #         try:
        #             poin  = d.find('2.png')
        #             if poin > [(0, 0)] :
        #                 d.click(poin[0][0],poin[0][1])
        #                 print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
        #                 break
        #         except:
        #             return 0
        
        # memus()           
        


        
def main(m):
        device = GetDevices()[m]
        for i in range(m, 2, thread_count):
                run = starts(device,device,)
                print(device)
                run.run()

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()

print('thread_count:', thread_count)