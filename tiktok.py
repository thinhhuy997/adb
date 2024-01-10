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
        
class EmulatorWorker(threading.Thread):
    def __init__(self, nameLD, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
    def run(self):
        try:
            device = self.device
            d = Auto(device)
            print('--------------------')
            print(f"Device {device} started")

            while True:
                try:
                    anh1=d.find("./images./app-store.png")
                    if anh1 > [(0,0)]:
                        d.click(anh1[0][0], anh1[0][1])
                        break
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    
def start_workers(worker_index, thread_count):
    device = GetDevices()[worker_index]    
    worker = EmulatorWorker(device, device)
    worker.run()

def main():
    devices = GetDevices()
    # print('devices:', devices)
    thread_count = len(GetDevices())

    print('thread_count', thread_count)

    for i in range(thread_count):
        # print('i', i)
        threading.Thread(target=start_workers, args=(i, thread_count)).start()

if __name__=="__main__": 
    main()