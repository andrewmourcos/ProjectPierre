import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
from pose_detection import PoseEstimator
import os
from threading import Thread
poser = PoseEstimator(0)

def run_all():
    Thread(target = os.system('python pose_detection.py')).start() 
    Thread(target = os.system('python ugh.py')).start()
    # show_frame()

def show_frame():
    head_queue = []
    r_arm_queue = []

    head_vel_x=[]
    head_vel_y=[]
    last_head_vel_y=0
    last_head_vel_x=0
    head_counter = 0

    r_arm_vel_x=[]
    r_arm_vel_y=[]
    last_r_arm_vel_y=0
    last_r_arm_vel_x=0
    r_arm_counter = 0

    start = time.time()
    r_arm_start = time.time()

    while cv2.waitKey(1) < 0:
        hasFrame, frame = poser.cap.read()

        if not hasFrame:
            cv2.waitKey()
            break

        poser.frameWidth = frame.shape[1]
        poser.frameHeight = frame.shape[0]
        points = poser.GetPose(frame)
        try:
            if len(head_queue) < 10:
                head_queue.append(points[0])
                # print(points[4])
                r_arm_queue.append(points[3])

                try:
                    x, y = zip(*head_queue)
                except:
                    pass

                try:
                    x1, y1 = zip(*r_arm_queue)
                except:
                    pass

                try:
                    head_vel_x.append(list(x)[-1]-list(x)[-2])
                    head_vel_y.append(list(y)[-1]-list(y)[-2])
                except:
                    pass

                try:
                    r_arm_vel_x.append(list(x1)[-1]-list(x1)[-2])
                    r_arm_vel_y.append(list(y1)[-1]-list(y1)[-2])
                except:
                    pass

            else:
                head_queue.pop(0)
                head_queue.append(points[0])
                r_arm_queue.pop(0)
                r_arm_queue.append(points[3])
                # print(points[4])
                try:
                    x, y = zip(*head_queue)
                except:
                    pass
                try:
                    x1, y1 = zip(*r_arm_queue)
                except:
                    pass

                try:
                    head_vel_x.pop(0)
                    head_vel_y.pop(0)
                    head_vel_x.append(list(x)[-1]-list(x)[-2])
                    head_vel_y.append(list(y)[-1]-list(y)[-2])
                except:
                    pass

                try:
                    r_arm_vel_x.pop(0)
                    r_arm_vel_y.pop(0)
                    r_arm_vel_x.append(list(x1)[-1]-list(x1)[-2])
                    r_arm_vel_y.append(list(y1)[-1]-list(y1)[-2])
                except:
                    pass

            ##### Moving Head #####
            if (last_head_vel_x < -2 and list(x)[-1]-list(x)[-2] > 2) or (last_head_vel_x > 2 and list(x)[-1]-list(x)[-2] < -2) or (last_head_vel_y < -2 and list(y)[-1]-list(y)[-2] > 2) or (last_head_vel_y > 2 and list(y)[-1]-list(y)[-2] < -2):
                if time.time() - start < 20:
                    head_counter+=1
                else:
                    start = time.time()
                    head_counter=0

            if head_counter > 5:
                print("STOP MOVING YOUR HEAD!!!")
                head_counter = 0
                start = time.time()
            ##### Moving Head #####


            ##### Moving right arm #####
            if (last_r_arm_vel_x < -2 and list(x1)[-1]-list(x1)[-2] > 2) or (last_r_arm_vel_x > 2 and list(x1)[-1]-list(x1)[-2] < -2) or (last_r_arm_vel_y < -2 and list(y1)[-1]-list(y1)[-2] > 2) or (last_r_arm_vel_y > 2 and list(y1)[-1]-list(y1)[-2] < -2):
                if time.time() - r_arm_start < 20:
                    r_arm_counter+=1
                else:
                    r_arm_start = time.time()
                    r_arm_counter=0

            if r_arm_counter > 5:
                print("STOP MOVING YOUR ARM!!!")
                r_arm_counter = 0
                r_arm_start = time.time()
            ##### Moving right arm #####

            try:
                last_head_vel_x = list(x)[-1]-list(x)[-2]
                last_head_vel_y = list(y)[-1]-list(y)[-2]
            except:
                pass

            try:
                last_r_arm_vel_x = list(x1)[-1]-list(x1)[-2]
                last_r_arm_vel_y = list(y1)[-1]-list(y1)[-2]
            except:
                pass

        except:
            pass


    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    display1.imgtk = imgtk #Shows frame for display 1
    display1.configure(image=imgtk)
    display2.imgtk = imgtk #Shows frame for display 2
    display2.configure(image=imgtk)
    window.after(10, show_frame) 




#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Pierre")
window.config(background="#FFFFFF")

master=window

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)


tk.Label(master, 
         text="Name").grid(row=0)
tk.Label(master, 
         text="Command").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master, 
          text='Quit', 
          command=master.quit).grid(row=3, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(master, 
          text='Begin', command=run_all).grid(row=3, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)



#Capture video frames

cap = cv2.VideoCapture(0)



display1 = tk.Label(imageFrame)
display1.grid(row=1, column=0, padx=10, pady=2)  #Display 1
display2 = tk.Label(imageFrame)
display2.grid(row=0, column=0) #Display 2

#Slider window (slider controls stage position)
sliderFrame = tk.Frame(window, width=600, height=100)
sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

# show_frame() #Display
window.mainloop()  #Starts GUI