from maix import camera, display, image, gpio, pinmap,time,app

# 设置 GPIO 引脚功能
pinmap.set_pin_function("A29", "GPIOA29")
pinmap.set_pin_function("A28", "GPIOA28")
pinmap.set_pin_function("A18", "GPIOA18")

# 初始化 LED
led1 = gpio.GPIO("GPIOA29", gpio.Mode.OUT)
led2 = gpio.GPIO("GPIOA28", gpio.Mode.OUT)
key = gpio.GPIO("GPIOA18",gpio.Mode.IN)
led1.value(1)  # 初始状态为灭
led2.value(1)  # 初始状态为灭

# 初始化摄像头和显示
cam = camera.Camera(320, 240)
disp = display.Display()

# 定义颜色阈值（红色和绿色）
red_thresholds = [[30, 100, 15, 127, 15, 127]]  # 红色的 LAB 阈值
green_thresholds = [[0, 80, -120, -10, 0, 30]]  # 绿色的 LAB 阈值

# 定义大面积检测的色块面积阈值
MIN_BLOB_AREA = 1000  # 色块的最小面积

while not app.need_exit():
    img = cam.read()
    if key.value():
        print('ok')
    # 查找红色色块
        red_blobs = img.find_blobs(red_thresholds, area_threshold=MIN_BLOB_AREA, pixels_threshold=MIN_BLOB_AREA)
        if red_blobs:
            for b in red_blobs:
                # 绘制红色矩形框
                corners = b.corners()
                for i in range(4):
                    img.draw_line(corners[i][0], corners[i][1], corners[(i + 1) % 4][0], corners[(i + 1) % 4][1], image.COLOR_RED)
            led2.value(0)  # 熄灭 LED2
        else:
            led2.value(1)  # 如果没有红色色块，熄灭 LED1

        # 查找绿色色块
        green_blobs = img.find_blobs(green_thresholds, area_threshold=MIN_BLOB_AREA, pixels_threshold=MIN_BLOB_AREA)
        if green_blobs:
            for b in green_blobs:
                # 绘制绿色矩形框
                corners = b.corners()
                for i in range(4):
                    img.draw_line(corners[i][0], corners[i][1], corners[(i + 1) % 4][0], corners[(i + 1) % 4][1], image.COLOR_GREEN)
            led1.value(0)  # 熄灭 LED1
        else:
            led1.value(1)  # 如果没有绿色色块，熄灭 LED2
        
        if green_blobs or red_blobs:
            time.sleep_ms(3000)
            led1.value(1)
            led2.value(1)

    # 显示图像
    disp.show(img)
