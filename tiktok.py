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
from com.dtmilano.android.viewclient import ViewClient


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
    def sendText(self, text: str) -> None:
        os.system(f"adb -s {self.handle} shell input text '{text}'")
    def enter(self) -> None:
        os.system(f"adb -s {self.handle} shell input keyevent 66")

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

    def startApp(self, adb_auto: Auto, app_img_path: str) -> None:
        while True:
            try:
                img_point = adb_auto.find(app_img_path)
                if img_point > [(0,0)]:
                    adb_auto.click(img_point[0][0], img_point[0][1])
                    print('1')
                    time.sleep(5)
                    device, serialno = ViewClient.connectToDeviceOrExit()
                    device.takeSnapshot().crop((100, 50, 500, 600)).save('./images/myscreencap.png', 'PNG')
                    print('2')

                    break
            except Exception as e:
                print("Err", e)

    def searchLiveStream(self, adb_auto: Auto, search_img_path: str, page_name: str, live_tag_img_path_1: str, live_tag_img_path_2: str) -> bool:
        while True:
            try:
                img_point = adb_auto.find(search_img_path)
                print('img_point', img_point)
                print(search_img_path)
                if img_point > [(0,0)]:
                    adb_auto.click(img_point[0][0], img_point[0][1])

                    time.sleep(2)
                    adb_auto.sendText(page_name)
                    adb_auto.enter()

                    time.sleep(2)
                    live_img_point_1 = adb_auto.find(live_tag_img_path_1)
                    live_img_point_2 = adb_auto.find(live_tag_img_path_2)
                    print('live_img_point_1', live_img_point_1)
                    print('live_img_point_2', live_img_point_2)

                    # Because There are 2 live-image tags, need to check twice
                    if live_img_point_1 > [(0, 0)]:
                        adb_auto.click(live_img_point_1[0][0], live_img_point_1[0][1])
                        return True # Search livestream successfully!
                    if live_img_point_2 > [(0, 0)]:
                        adb_auto.click(live_img_point_2[0][0], live_img_point_2[0][1])
                        return True # Search livestream successfully!

            except Exception as e:
                print(e)
                return False
            
            return False
        
    def interactLiveStream(self, adb_auto: Auto, captcha_img_path: str) -> None:

        device, serialno = ViewClient.connectToDeviceOrExit()
        device.takeSnapshot().crop((100, 50, 500, 600)).save('./myscreencap.png', 'PNG')


        # count = 0
        # while True:
        #     captcha_img_point = adb_auto.find(captcha_img_path)
        #     if captcha_img_point > [(0, 0)]:
        #         print(f'Captcha xuất hiện khi count = {count}')
        #     count+=1


            

        #     # Check captcha appear every 10 seconds
        #     time.sleep(10)

    def run(self):
        try:
            device = self.device
            adb_auto = Auto(device)

            app_img_path = "./images/tiktok-1.png"

            search_img_path = "./images/search-1.png"
            page_name = "xuong jogger"
            live_tag_img_path_1 = "./images/live-tag-1.png"
            live_tag_img_path_2 = "./images/live-tag-2.png"

            captcha_img_path = "./images/captcha-1.png"

            print('--------------------')
            print(f"Device {device} started")

            # Start the application that needs the operation
            self.startApp(adb_auto, app_img_path)
            time.sleep(2)

            # Search the tiktok livestream that needs the operation
            live_check = self.searchLiveStream(adb_auto, search_img_path, page_name, live_tag_img_path_1, live_tag_img_path_2)
            time.sleep(2)

            # Interact with the livestream if it is found
            if live_check:
                self.interactLiveStream(adb_auto, captcha_img_path)
                
            else:
                print(f'Livestream "{page_name}" không được tìm thấy')

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