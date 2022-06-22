# SheepDetect
安装步骤：
!git clone https://github.com/Z-hengli/SheepDetect.git
cd SheepDetect
!python -m pip install --upgrade pip
!pip install -r requirements.txt
!python main.py


修改的代码  功能   位置代码行数
基于https://github.com/dyh/unbox_yolov5_deepsort_counting修改
.idea文件下unbox_yolov5_deepsort_counting.iml文件改名为SheepDetect.iml文件
main.py文件修改
13  list_pts_blue = [[204, 305], [227, 431], [605, 522], [1101, 464], [1900, 601], [1902, 495], [1125, 379], [604, 437],[299, 375], [267, 289]]改为list_pts_blue = [[0, 0], [0, 1080], [400, 1080], [400, 0]]
21   list_pts_yellow = [[181, 305], [207, 442], [603, 544], [1107, 485], [1898, 625], [1893, 701], [1101, 568], [594, 637], [118, 483], [109, 303]]改为list_pts_yellow = [[400, 0], [400, 1080], [800, 1080], [800, 0]]
34    blue_color_plate = [255, 0, 0]改为blue_color_plate = [15, 0, 0]
39    yellow_color_plate = [0, 255, 255]改为yellow_color_plate = [0, 0, 0]
66    capture = cv2.VideoCapture('./video/test.mp4')改为
capture = cv2.VideoCapture(r'./video/sheepvideo.mp4')
121   print(f'类别: {label} | id: {track_id} | 上行撞线 | 上行撞线总数: {up_count} | 上行id列表: {list_overlapping_yellow_polygon}')改为print(f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
143   print(f'类别: {label} | id: {track_id} | 下行撞线 | 下行撞线总数: {down_count} | 下行id列表: {list_overlapping_blue_polygon}')改为print(f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
193    text_draw = 'DOWN: ' + str(down_count) + \' , UP: ' + str(up_count)改为text_draw = 'all: ' + str(up_count)
200     cv2.imshow('demo', output_image_frame)改为cv2.imwrite("./images/{}.png".format(i), output_image_frame)
另加一行i += 1
Pass与capture.release()中间加如下部分代码
time_end = time.time()
    print('totally cost', time_end - time_start)
    filelist = []
    path = './images/'  
    filelist = os.listdir(path)
    fps = 30
    size = (960, 540)
    file_path = "./test/" + str(int(time.time())) + ".avi"
    fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
    video = cv2.VideoWriter( file_path, fourcc, fps, size )
    img_array = []
    for filename in [r'./images/{0}.png'.format(i) for i in range(i)]: 
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)
    for i in range(i): 
        video.write(img_array[i])
    video.release()
print('end!')

