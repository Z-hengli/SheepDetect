import numpy as np
 
import os
import tracker
from detector import Detector
import cv2
import time
 
# os.environ["CUDA_VISIBLE_DEVICES"] = " "
 
if __name__ == '__main__':
 
    time_start = time.time()
 
    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
 
    # 初始化2个撞线polygon
    list_pts_blue = [[0, 0], [0, 1080], [400, 1080], [400, 0]]
    # list_pts_blue = [[850, 0], [850, 1080], [880, 1080], [880, 0]]
    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=1)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]
 
    # 填充第二个polygon
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
    list_pts_yellow = [[400, 0], [400, 1080], [800, 1080], [800, 0]]
    # list_pts_yellow = [[900, 0], [900, 1080], [930, 1080], [930, 0]]
    ndarray_pts_yellow = np.array(list_pts_yellow, np.int32)
    polygon_yellow_value_2 = cv2.fillPoly(mask_image_temp, [ndarray_pts_yellow], color=2)
    polygon_yellow_value_2 = polygon_yellow_value_2[:, :, np.newaxis]
 
    # 撞线检测用mask，包含2个polygon，（值范围 0、1、2），供撞线计算使用
    polygon_mask_blue_and_yellow = polygon_blue_value_1 + polygon_yellow_value_2
 
    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (960, 540))
 
    # 蓝 色盘 b,g,r
    blue_color_plate = [15, 0, 0]
    # 蓝 polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)
 
    # 黄 色盘
    yellow_color_plate = [0, 0, 0]
    # 黄 polygon图片
    yellow_image = np.array(polygon_yellow_value_2 * yellow_color_plate, np.uint8)
 
    # 彩色图片（值范围 0-255）
    color_polygons_image = blue_image + yellow_image
    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (960, 540))
 
    # list 与蓝色polygon重叠
    list_overlapping_blue_polygon = []
 
    # list 与黄色polygon重叠
    list_overlapping_yellow_polygon = []
 
    # 进入数量
    down_count = 0
    # 离开数量
    up_count = 0
 
    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))
 
    # 初始化 yolov5
    detector = Detector()
 
    # 打开视频
    # url = "rtsp://admin:*******@192.168.1.64/Streaming/Channels/1"
    # capture = cv2.VideoCapture(url)
    capture = cv2.VideoCapture(r'./video/sheepvideo.mp4')
    # capture = cv2.VideoCapture('TownCentreXVID.avi')
    i = 0
    while True:
       # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break
 
        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))
#         im = cv2.transpose(im)
#         im = cv2.flip(im, 0)
#         cv2.imwrite("./raw.png", im)
 
        list_bboxs = []
        bboxes = detector.detect(im)
        # print(bboxes)
 
        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)
 
            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass
 
        # 输出图片
        output_image_frame = cv2.add(output_image_frame, color_polygons_image)
 
        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, label, track_id = item_bbox
 
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                y1_offset = int(y1 + ((y2 - y1) * 0.6))
 
                # 撞线的点
                y = y1_offset
                x = x1
 
                if polygon_mask_blue_and_yellow[y, x] == 1:
                    # 如果撞 蓝polygon
                    if track_id not in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.append(track_id)
                    pass
 
                    # 判断 黄polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 外出方向
                    if track_id in list_overlapping_yellow_polygon:
                        # 外出+1
                        up_count += 1
 
                        # print(
                        #     f'类别: {label} | id: {track_id} | 上行撞线 | 上行撞线总数: {up_count} | 上行id列表: {list_overlapping_yellow_polygon}')
                        print(
                            f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
                        # 删除 黄polygon list 中的此id
                        list_overlapping_yellow_polygon.remove(track_id)
 
                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass
 
                elif polygon_mask_blue_and_yellow[y, x] == 2:
                    # 如果撞 黄polygon
                    if track_id not in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.append(track_id)
                    pass
 
                    # 判断 蓝polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 进入方向
                    if track_id in list_overlapping_blue_polygon:
                        # 进入+1
                        # down_count += 1
                        up_count += 1
 
                        # print(
                        #     f'类别: {label} | id: {track_id} | 下行撞线 | 下行撞线总数: {down_count} | 下行id列表: {list_overlapping_blue_polygon}')
                        print(
                            f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
                        # 删除 蓝polygon list 中的此id
                        list_overlapping_blue_polygon.remove(track_id)
 
                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass
                    pass
                else:
                    pass
                pass
 
            pass
 
            # ----------------------清除无用id----------------------
            list_overlapping_all = list_overlapping_yellow_polygon + list_overlapping_blue_polygon
            for id1 in list_overlapping_all:
                is_found = False
                for _, _, _, _, _, bbox_id in list_bboxs:
                    if bbox_id == id1:
                        is_found = True
                        break
                    pass
                pass
 
                if not is_found:
                    # 如果没找到，删除id
                    if id1 in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.remove(id1)
                    pass
                    if id1 in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.remove(id1)
                    pass
                pass
            list_overlapping_all.clear()
            pass
 
            # 清空list
            list_bboxs.clear()
 
            pass
        else:
            # 如果图像中没有任何的bbox，则清空list
            list_overlapping_blue_polygon.clear()
            list_overlapping_yellow_polygon.clear()
            pass
        pass
 
        text_draw = 'all: ' + str(up_count)
            # 'DOWN: ' + str(down_count) + \
            #         ' , UP: ' + str(up_count)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion,
                                         fontFace=font_draw_number,
                                         fontScale=1, color=(255, 255, 255), thickness=2)
        
 
 
        # cv2.imshow('demo', output_image_frame)
        #cv2.imwrite('./res.png', output_image_frame)
        cv2.imwrite("./images/{}.png".format(i), output_image_frame)
        i += 1
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # out = cv2.VideoWriter('out.avi', fourcc, 20.0, (960, 540))
        # cv2.imwrite("..//images//output_image_frame.jpg", output_image_frame);
 
 
 
        cv2.waitKey(1)
 
 
        pass
    pass
 
    time_end = time.time()
    print('totally cost', time_end - time_start)
 
    #size = (960, 540)  # 这个是图片的尺寸，一定要和要用的图片size一致
    # 完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     videowrite = cv2.VideoWriter(r'./test.mp4', fourcc, 20, size)  # 20是帧数，size是图片尺寸

    filelist = []
    path = './images/'  
    filelist = os.listdir(path)
    fps = 30
    size = (960, 540)
    file_path = "./test/" + str(int(time.time())) + ".avi"
    fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
    video = cv2.VideoWriter( file_path, fourcc, fps, size )
#     for item in filelist:
#         if item.endswith('.png'):   
#             item = path + '/' + item  # 全路径地址(c:/../scence/haha.jpg)
#             img = cv2.imread(item)  #使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
#             video.write(img)        #把图片写进视频

#     video.release() #释放
#     cv2.destroyAllWindows()    #关闭图片窗口
    
    img_array = []
    for filename in [r'./images/{0}.png'.format(i) for i in range(i)]:  # 这个循环是为了读取所有要用的图片文件
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)
    for i in range(i):  # 把读取的图片文件写进去
        video.write(img_array[i])
    video.release()
    print('end!')
 
    capture.release()
    cv2.destroyAllWindows()    
    
    
#     videowrite = cv2.VideoWriter(r'./test.mp4', -1, 30, size)  # 20是帧数，size是图片尺寸
#     img_array = []
#     for filename in [r'./images/{0}.png'.format(i) for i in range(i)]:  # 这个循环是为了读取所有要用的图片文件
#         img = cv2.imread(filename)
#         if img is None:
#             print(filename + " is error!")
#             continue
#         img_array.append(img)
#     for i in range(i):  # 把读取的图片文件写进去
#         videowrite.write(img_array[i])
#     videowrite.release()
#     print('end!')
 
#     capture.release()
#     cv2.destroyAllWindows()