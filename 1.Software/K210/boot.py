import sensor
import image
import lcd
import KPU as kpu
import time
from Maix import FPIOA, GPIO
import gc
from fpioa_manager import fm
import utime
import os
import ubinascii
from Maix import utils
from machine import UART


utils.gc_heap_size(1024*256)


Max_Mode_Num = 2
Max_Feature_Num = 5
task_mask = kpu.load("/sd/mask.smodel")
Key_Press = 0
Last_state = 1
feature_index = 0
SD_Storage = 0
feature_flag = 0
Read_Feature_On_Mode = 0
FeatureChange = 1
ModeChange = 1
face_flag = 0
mask_flag = 0
error_temp = 37.3
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
img_lcd = image.Image()
img_face = image.Image(size=(128, 128))
img_face.pix_to_ai()

def Mode_Change(pin_num):
    # 模式切换:  口罩识别/特征识别
    global ModeChange
    global Max_Mode_Num
    global Last_state
    global Key_Press
    utime.sleep_us(100)
    if(key1.value() == 0):
        if ModeChange < Max_Mode_Num:
            ModeChange += 1
        else:
            ModeChange = 1
        Last_state = ModeChange
        Key_Press = 1

def Feature_Change(pin_num):
    # 特征切换
    global FeatureChange
    global Max_Feature_Num
    utime.sleep_us(100)
    if(key2.value() == 0):
        if FeatureChange < Max_Feature_Num:
            FeatureChange += 1
        else:
            FeatureChange = 1


def Read_Feature_Change(pin_num):
    # 特征读取开关模式切换
    global Read_Feature_On_Mode
    utime.sleep_us(100)
    if(key3.value() == 0):
        if Read_Feature_On_Mode == 1:
            Read_Feature_On_Mode = 0
        else:
            Read_Feature_On_Mode = 1


# 变量定义
Mode_number = 1
BOUNCE_PROTECTION = 50
ACCURACY = 80
record_ftr = []
record_ftrs = []
Person_1_record_ftrs = []
Person_2_record_ftrs = []
Person_3_record_ftrs = []
Person_4_record_ftrs = []
Person_5_record_ftrs = []
record = []
class_IDs = ['no_mask', 'mask']
names = ['Person_1', 'Person_2', 'Person_3', 'Person_4', 'Person_5']




# 标志位变量定义
feature_file_exists = 0  #特征是否存在标志

# IO口重映射
# 按键映射
fm.register(6, fm.fpioa.GPIOHS6)
fm.register(7, fm.fpioa.GPIOHS7)
fm.register(8, fm.fpioa.GPIOHS8)

# 串口映射
fm.register(34, fm.fpioa.UART1_TX, force=True)
fm.register(35, fm.fpioa.UART1_RX, force=True)

key1 = GPIO(GPIO.GPIOHS6, GPIO.PULL_UP)
key2 = GPIO(GPIO.GPIOHS7, GPIO.PULL_UP)
key3 = GPIO(GPIO.GPIOHS8, GPIO.PULL_UP)

key1.irq(Mode_Change,GPIO.IRQ_FALLING,GPIO.WAKEUP_NOT_SUPPORT,7)
key2.irq(Feature_Change,GPIO.IRQ_FALLING,GPIO.WAKEUP_NOT_SUPPORT,7)
key3.irq(Read_Feature_Change,GPIO.IRQ_FALLING,GPIO.WAKEUP_NOT_SUPPORT,7)

uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

def save_feature(feat,file_name):
# 保存特征值
    with open('/sd/' + file_name,'a') as f:
        record =ubinascii.b2a_base64(feat)
        f.write(record)





#读取人脸特征值
for v in os.ilistdir('/sd'):#to check key directorys or files in sd card.sd card should be formated to fat32
    if v[0] == 'Person_1_features.txt' and v[1] == 0x8000:#0x8000 is file
        feature_file_exists = 1
        if(feature_file_exists):
            #print("start")
            with open('/sd/Person_1_features.txt','rb') as f:
                s = f.readlines()
                for line in s:
                    #print(ubinascii.a2b_base64(line))
                    Person_1_record_ftrs.append(bytearray(ubinascii.a2b_base64(line)))

for v in os.ilistdir('/sd'):#to check key directorys or files in sd card.sd card should be formated to fat32
    if v[0] == 'Person_2_features.txt' and v[1] == 0x8000:#0x8000 is file
        feature_file_exists = 1
        if(feature_file_exists):
            #print("start")
            with open('/sd/Person_2_features.txt','rb') as f:
                s = f.readlines()
                for line in s:
                    #print(ubinascii.a2b_base64(line))
                    Person_2_record_ftrs.append(bytearray(ubinascii.a2b_base64(line)))

for v in os.ilistdir('/sd'):#to check key directorys or files in sd card.sd card should be formated to fat32
    if v[0] == 'Person_3_features.txt' and v[1] == 0x8000:#0x8000 is file
        feature_file_exists = 1
        if(feature_file_exists):
            #print("start")
            with open('/sd/Person_3_features.txt','rb') as f:
                s = f.readlines()
                for line in s:
                    #print(ubinascii.a2b_base64(line))
                    Person_3_record_ftrs.append(bytearray(ubinascii.a2b_base64(line)))

for v in os.ilistdir('/sd'):#to check key directorys or files in sd card.sd card should be formated to fat32
    if v[0] == 'Person_4_features.txt' and v[1] == 0x8000:#0x8000 is file
        feature_file_exists = 1
        if(feature_file_exists):
            #print("start")
            with open('/sd/Person_4_features.txt','rb') as f:
                s = f.readlines()
                for line in s:
                    #print(ubinascii.a2b_base64(line))
                    Person_4_record_ftrs.append(bytearray(ubinascii.a2b_base64(line)))

for v in os.ilistdir('/sd'):#to check key directorys or files in sd card.sd card should be formated to fat32
    if v[0] == 'Person_5_features.txt' and v[1] == 0x8000:#0x8000 is file
        feature_file_exists = 1
        if(feature_file_exists):
            #print("start")
            with open('/sd/Person_5_features.txt','rb') as f:
                s = f.readlines()
                for line in s:
                    #print(ubinascii.a2b_base64(line))
                    Person_5_record_ftrs.append(bytearray(ubinascii.a2b_base64(line)))


def face_init():
    global task_fd
    global task_ld
    global task_fe
    global feature_anchor
    global dst_point
    global img_face
    global task_mask
    global face_flag
    global mask_flag
    if ModeChange == 1 and mask_flag:
        kpu.deinit(task_mask)
        del task_mask
        gc.collect()
    task_fd = kpu.load("/sd/0x300000_fd.smodel")
    task_ld = kpu.load("/sd/0x400000_fl.smodel")
    task_fe = kpu.load("/sd/0x500000_fe.smodel")
    feature_anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437,6.92275, 6.718375, 9.01025)  # anchor for face detect
    dst_point = [(44, 59), (84, 59), (64, 82), (47, 105),(81, 105)]  # standard face key point position
    kpu.init_yolo2(task_fd, 0.5, 0.3, 5, feature_anchor)
    face_flag = 1
    mask_flag = 0
    #lcd.init()
    #sensor.reset()
    #sensor.set_pixformat(sensor.RGB565)
    #sensor.set_framesize(sensor.QVGA)
    #sensor.set_hmirror(1)
    #sensor.set_vflip(1)
    #sensor.run(1)
    #img_lcd = image.Image()
    #img_face = image.Image(size=(128, 128))
    #img_face.pix_to_ai()

def face_check(img):
    global task_fd
    global task_ld
    global task_fe
    global feature_anchor
    global dst_point
    global feature_flag
    global Read_Feature_On_Mode
    global code
    try:
        code = kpu.run_yolo2(task_fd, img)
        if code:
            for i in code:
                # Cut face and resize to 128x128
                a = img.draw_rectangle(i.rect())
                face_cut = img.cut(i.x(), i.y(), i.w(), i.h())
                face_cut_128 = face_cut.resize(128, 128)
                a = face_cut_128.pix_to_ai()
                # a = img.draw_image(face_cut_128, (0,0))
                # Landmark for face 5 points
                fmap = kpu.forward(task_ld, face_cut_128)
                plist = fmap[:]
                le = (i.x() + int(plist[0] * i.w() - 10), i.y() + int(plist[1] * i.h()))
                re = (i.x() + int(plist[2] * i.w()), i.y() + int(plist[3] * i.h()))
                nose = (i.x() + int(plist[4] * i.w()), i.y() + int(plist[5] * i.h()))
                lm = (i.x() + int(plist[6] * i.w()), i.y() + int(plist[7] * i.h()))
                rm = (i.x() + int(plist[8] * i.w()), i.y() + int(plist[9] * i.h()))

                #绘制人脸五点特征

                #a = img.draw_circle(le[0], le[1], 4)
                #a = img.draw_circle(re[0], re[1], 4)
                #a = img.draw_circle(nose[0], nose[1], 4)
                #a = img.draw_circle(lm[0], lm[1], 4)
                #a = img.draw_circle(rm[0], rm[1], 4)

                # align face to standard position
                src_point = [le, re, nose, lm, rm]
                T = image.get_affine_transform(src_point, dst_point)
                a = image.warp_affine_ai(img, img_face, T)
                a = img_face.ai_to_pix()
                # a = img.draw_image(img_face, (128,0))
                del (face_cut_128)
                # calculate face feature vector
                fmap = kpu.forward(task_fe, img_face)
                feature = kpu.face_encode(fmap[:])

                max_score = 0
                index = 0
                scores = []
                for j in range(len(Person_1_record_ftrs)):
                    score = kpu.face_compare(Person_1_record_ftrs[j], feature)
                    scores.append(score)
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        feature_index = index

                index = 1
                scores = []
                for j in range(len(Person_2_record_ftrs)):
                    score = kpu.face_compare(Person_2_record_ftrs[j], feature)
                    scores.append(score)
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        feature_index = index


                index = 2
                scores = []
                for j in range(len(Person_3_record_ftrs)):
                    score = kpu.face_compare(Person_3_record_ftrs[j], feature)
                    scores.append(score)
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        feature_index = index

                index = 3
                scores = []
                for j in range(len(Person_4_record_ftrs)):
                    score = kpu.face_compare(Person_4_record_ftrs[j], feature)
                    scores.append(score)
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        feature_index = index

                index = 4
                scores = []
                for j in range(len(Person_5_record_ftrs)):
                    score = kpu.face_compare(Person_5_record_ftrs[j], feature)
                    scores.append(score)
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        feature_index = index

                if max_score > ACCURACY:
                    a = img.draw_string(i.x(), i.y(), ("%s :%2.1f" % (
                        names[feature_index], max_score)), color=(0, 255, 0), scale=2)
                else:
                    a = img.draw_string(i.x(), i.y(), ("X :%2.1f" % (
                        max_score)), color=(255, 0, 0), scale=2)
                if Read_Feature_On_Mode == 1:
                    Read_Feature_On_Mode = 0
                    record_ftr = feature
                    if FeatureChange == 1:
                        Person_1_record_ftrs.append(record_ftr) #将当前特征添加到已知特征列表
                    elif FeatureChange == 2:
                        Person_2_record_ftrs.append(record_ftr) #将当前特征添加到已知特征列表
                    elif FeatureChange == 3:
                        Person_3_record_ftrs.append(record_ftr) #将当前特征添加到已知特征列表
                    elif FeatureChange == 4:
                        Person_4_record_ftrs.append(record_ftr) #将当前特征添加到已知特征列表
                    elif FeatureChange == 5:
                        Person_5_record_ftrs.append(record_ftr) #将当前特征添加到已知特征列表

                    a = img.draw_string(100,100, "Storage successful", color=(0,255,0),scale=2)
                    #time.sleep(1)
                    if FeatureChange == 1:
                        save_feature(record_ftr,"Person_1_features.txt")
                    elif FeatureChange == 2:
                        save_feature(record_ftr,"Person_2_features.txt")
                    elif FeatureChange == 3:
                        save_feature(record_ftr,"Person_3_features.txt")
                    elif FeatureChange == 4:
                        save_feature(record_ftr,"Person_4_features.txt")
                    elif FeatureChange == 5:
                        save_feature(record_ftr,"Person_5_features.txt")
    finally:
        utime.sleep_ms(10)
def mask_init():
    global task_fd
    global task_ld
    global task_fe
    global mask_anchor
    global task_mask
    global face_flag
    global mask_flag
    if ModeChange == 2 and face_flag:
        kpu.deinit(task_fd)
        kpu.deinit(task_ld)
        kpu.deinit(task_fe)
        del task_fd
        del task_ld
        del task_fe
        gc.collect()
    task_mask = kpu.load("/sd/mask.smodel")
    mask_anchor = (0.1606, 0.3562, 0.4712, 0.9568, 0.9877, 1.9108, 1.8761, 3.5310, 3.4423, 5.6823)
    kpu.init_yolo2(task_mask, 0.5, 0.3, 5, mask_anchor)
    face_flag = 0
    mask_flag = 1
    #lcd.init()
    #sensor.reset()
    #sensor.set_pixformat(sensor.RGB565)
    #sensor.set_framesize(sensor.QVGA)
    #sensor.set_hmirror(1)
    #sensor.set_vflip(1)
    #sensor.run(1)
    #img_lcd = image.Image()

def mask_check(img):
    global task_mask
    global code
    try:
        code = kpu.run_yolo2(task_mask, img)
        if code:
            for item in code:
                confidence = float(item.value())
                classID = int(item.classid())
                if classID == 1 and confidence > 0.8:
                    img.draw_rectangle(item.rect(), (0, 255, 0), tickness=5)
                    img.draw_string(item.x(), item.y(), 'mask:{:.2f}'.format(confidence), color=(0, 255, 0) , scale=1.5)
                elif classID == 0 and confidence > 0.65                                                                                                                                                        :
                    img.draw_rectangle(item.rect(), color=(255, 0, 0), tickness=5)
                    img.draw_string(item.x(), item.y(), 'no mask:{:.2f}'.format(confidence) , color=(255, 0, 0) , scale=1.5)
    finally:
        utime.sleep_ms(10)
def display_draw_flash(img):
    if ModeChange == 1:
        img.draw_string(160,200, "Mode:Feature", color=(0,255,0),scale=1.5)
    elif ModeChange == 2:
        img.draw_string(160,200, "Mode:Mask", color=(0,0,255),scale=1.5)

    if FeatureChange == 1:
        img.draw_string(160,220, "Feature:Person_1", color=(0,255,0),scale=1.5)
    elif FeatureChange == 2:
        img.draw_string(160,220, "Feature:Person_2", color=(0,255,0),scale=1.5)
    elif FeatureChange == 3:
        img.draw_string(160,220, "Feature:Person_3", color=(0,255,0),scale=1.5)
    elif FeatureChange == 4:
        img.draw_string(160,220, "Feature:Person_4", color=(0,255,0),scale=1.5)
    elif FeatureChange == 5:
        img.draw_string(160,220, "Feature:Person_5", color=(0,255,0),scale=1.5)
    else:
        img.draw_string(160,220, "Feature:%d" %(FeatureChange), color=(0,255,0),scale=1.5)


gc.collect()
face_init()
while (1):

    img = sensor.snapshot()

    if Key_Press == 1:
        Key_Press = 0
        if ModeChange == 1:
            face_init()
        elif ModeChange == 2:
            mask_init()
        utime.sleep_ms(100)
    if ModeChange == 1 and face_flag:
        face_check(img)
    elif ModeChange == 2 and mask_flag:
        mask_check(img)

    read_data = uart_A.readline()
    if read_data:
        read_str = read_data.decode('utf-8').strip()

    if float(read_str) > error_temp:
        img.draw_string(0,220, "Temp:" + read_str, color=(255,0,0),scale=1.5)
    else:
        img.draw_string(0,220, "Temp:" + read_str, color=(0,255,0),scale=1.5)

    display_draw_flash(img)

    lcd.display(img)
    gc.collect()
    #kpu.memtest()

# a = kpu.deinit(task_fe)
# a = kpu.deinit(task_ld)
# a = kpu.deinit(task_fd)
