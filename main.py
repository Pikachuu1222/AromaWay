from maix import camera, display, image, nn, app, gpio, pinmap, time

# 设置 GPIO 引脚功能
pinmap.set_pin_function("A29", "GPIOA29")
pinmap.set_pin_function("A28", "GPIOA28")
pinmap.set_pin_function("A18", "GPIOA18")

# 初始化 LED
led1 = gpio.GPIO("GPIOA29", gpio.Mode.OUT)
led2 = gpio.GPIO("GPIOA28", gpio.Mode.OUT)
key = gpio.GPIO("GPIOA18", gpio.Mode.IN)
led1.value(1)  # 初始状态为灭
led2.value(1)  # 初始状态为灭

# 初始化YOLOv5检测器
detector = nn.YOLOv5(model="/root/models/maixhub/192643/model_192643.mud")
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()

while not app.need_exit():
    img = cam.read()
    
    if key.value():
        print('ok')
        # 检测物体
        objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
        
        # 重置LED状态
        red_detected = False
        green_detected = False
        
        for obj in objs:
            # 绘制检测框和信息
            img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
            msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
            img.draw_string(obj.x, obj.y, msg, color=image.COLOR_RED)
            
            # 根据标签控制LED
            label = detector.labels[obj.class_id].lower()
            if 'red' in label:
                red_detected = True
            elif 'green' in label:
                green_detected = True
        
        # 控制LED
        if red_detected:
            led2.value(0)  # 点亮LED2表示红色检测
        else:
            led2.value(1)  # 熄灭LED2
            
        if green_detected:
            led1.value(0)  # 点亮LED1表示绿色检测
        else:
            led1.value(1)  # 熄灭LED1
        
        # 如果检测到任何颜色，保持3秒后熄灭
        if red_detected or green_detected:
            time.sleep_ms(3000)
            led1.value(1)
            led2.value(1)
    
    # 显示图像
    dis.show(img)
