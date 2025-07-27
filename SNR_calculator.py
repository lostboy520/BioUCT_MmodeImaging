import cv2
import numpy as np

# 初始化变量
highlight_ref_point = []
background_ref_point = []
highlight_cropping = False
background_cropping = False
highlight_selected = False
background_selected = False

def select_highlight_roi(event, x, y, flags, param):
    global highlight_ref_point, highlight_cropping, highlight_selected
    if event == cv2.EVENT_LBUTTONDOWN:
        highlight_ref_point = [(x, y)]
        highlight_cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        highlight_ref_point.append((x, y))
        highlight_cropping = False
        highlight_selected = True
        cv2.rectangle(image_copy, highlight_ref_point[0], highlight_ref_point[1], (255, 0, 0), 2)
        cv2.imshow("image", image_copy)

def select_background_roi(event, x, y, flags, param):
    global background_ref_point, background_cropping, background_selected
    if event == cv2.EVENT_LBUTTONDOWN:
        background_ref_point = [(x, y)]
        background_cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        background_ref_point.append((x, y))
        background_cropping = False
        background_selected = True
        cv2.rectangle(image_copy, background_ref_point[0], background_ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image_copy)

# 读取图像
image = cv2.imread('3.png', cv2.IMREAD_GRAYSCALE)
image_copy = image.copy()

# 显示图像并手动选择高亮区域
cv2.namedWindow("image")
cv2.setMouseCallback("image", select_highlight_roi)
print("请选择高亮区域，然后按任意键继续...")
cv2.imshow("image", image_copy)
cv2.waitKey(0)

# 显示图像并手动选择背景区域
cv2.setMouseCallback("image", select_background_roi)
print("请选择背景区域，然后按任意键继续...")
cv2.imshow("image", image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

if highlight_selected and background_selected:
    highlight_roi = image[highlight_ref_point[0][1]:highlight_ref_point[1][1], 
                          highlight_ref_point[0][0]:highlight_ref_point[1][0]]
    background_roi = image[background_ref_point[0][1]:background_ref_point[1][1], 
                           background_ref_point[0][0]:background_ref_point[1][0]]

    # 在选定的高亮区域进行阈值分割和轮廓检测
    _, thresh = cv2.threshold(highlight_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建掩码并填充高亮区域的轮廓
    highlight_mask = np.zeros_like(highlight_roi)
    for contour in contours:
        cv2.drawContours(highlight_mask, [contour], -1, 255, thickness=cv2.FILLED)

    # 计算高亮区域的平均亮度
    highlight_pixels = highlight_roi[highlight_mask == 255]
    signal_mean = np.mean(highlight_pixels)
    signal_std = np.std(highlight_pixels)
    signal_max = np.max(highlight_pixels)

    # 计算背景区域的平均亮度和标准差
    background_mean = np.mean(background_roi)
    background_std = np.std(background_roi)
    background_min = np.min(background_roi)

    # 计算信噪比
    snr = (signal_mean - background_mean) / background_std

    # 输出结果
    print(f'Background Mean: {background_mean}')
    #print(f'Background Std Dev: {background_std}')
    #print(f'Background Min Value: {background_min}')
    print(f'Signal Mean: {signal_mean}')
    #print(f'Signal Std: {signal_std}')
    #print(f'Signal max: {signal_max}')
    #print(f'Signal-to-Noise Ratio (SNR): {snr}')

    # 可视化结果并保存图像
    result_image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)
    cv2.rectangle(result_image, highlight_ref_point[0], highlight_ref_point[1], (255, 0, 0), 2)
    cv2.rectangle(result_image, background_ref_point[0], background_ref_point[1], (0, 255, 0), 2)
    for contour in contours:
        contour_offset = contour + highlight_ref_point[0]  # 将轮廓坐标转换回原始图像坐标
        cv2.drawContours(result_image, [contour_offset], -1, (0, 0, 255), 2)
    cv2.imshow("Selected Regions with Contours", result_image)
    cv2.imwrite('selected_regions_with_contours.png', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("未选择高亮区域或背景区域")
