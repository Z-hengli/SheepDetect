# SheepDetect
* 实现羊群的撞线计算。
* 显示检测类别。
* 检测类别可在 detector.py 文件第60行修改。
* 若要检测不同位置和方向，可在 main.py 文件第19行和27行，修改2个polygon的点。
* 检测识别视频存储在test文件夹
## 运行环境<br>
* python 3.6<br>
* pytorch 1.8<br>
* pip install -r requirements.txt<br>
## 如何运行<br>
1.下载代码<br>
```
!git clone https://github.com/Z-hengli/SheepDetect.git
```
2.进入目录<br>
```
cd SheepDetect
```
3.升级pip
```
!python -m pip install --upgrade pip
```
4.安装软件包
```
!pip install -r requirements.txt
```
5.运行程序
```
!python main.py
```


## 修改的代码<br>
基于https://github.com/dyh/unbox_yolov5_deepsort_counting修改<br>
.idea文件下unbox_yolov5_deepsort_counting.iml文件改名为SheepDetect.iml文件<br>
main.py文件修改<br>
```
13行　　list_pts_blue = [[204, 305], [227, 431], [605, 522], [1101, 464], [1900, 601], [1902, 495], [1125, 379], [604, 437],[299, 375], [267, 289]]　　改为　　list_pts_blue = [[0, 0], [0, 1080], [400, 1080], [400, 0]]
```
```
21行　　list_pts_yellow = [[181, 305], [207, 442], [603, 544], [1107, 485], [1898, 625], [1893, 701], [1101, 568], [594, 637], [118, 483], [109, 303]]　　改为　　list_pts_yellow = [[400, 0], [400, 1080], [800, 1080], [800, 0]]
```
```
34行　　blue_color_plate = [255, 0, 0]　　改为　　blue_color_plate = [15, 0, 0]
```
```
39行　　yellow_color_plate = [0, 255, 255]　　改为　　yellow_color_plate = [0, 0, 0]
```
```
66行　　capture = cv2.VideoCapture('./video/test.mp4')　　改为　　capture = cv2.VideoCapture(r'./video/sheepvideo.mp4')
```
```
121行　　print(f'类别: {label} | id: {track_id} | 上行撞线 | 上行撞线总数: {up_count} | 上行id列表: {list_overlapping_yellow_polygon}')　　改为　　print(f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
```
```
143行　　print(f'类别: {label} | id: {track_id} | 下行撞线 | 下行撞线总数: {down_count} | 下行id列表: {list_overlapping_blue_polygon}')　　改为　　print(f'类别: {label} | id: {track_id} | 总数: {up_count} | id列表: {list_overlapping_yellow_polygon}')
```
```
193行　　text_draw = 'DOWN: ' + str(down_count) + \' , UP: ' + str(up_count)　　改为　　text_draw = 'all: ' + str(up_count)
```
```
200行　　cv2.imshow('demo', output_image_frame)　　改为　　cv2.imwrite("./images/{}.png".format(i), output_image_frame)
```
另加一行　
```
i+= 1
```
Pass与capture.release()中间加如下部分代码
```
time_end = time.time()
　　print('totally cost', time_end - time_start)
　　filelist = []
　　path = './images/' 
　　filelist = os.listdir(path)
　　fps = 30
　　size = (960, 540)
　　file_path = "./test/" + str(int(time.time())) + ".avi"
　　print('检测识别后视频地址为：',file_path)
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
```

待检测视频的地址输入main.py文件中的74行<br>
如果需要实时导入相机视频需要利用72、73行根据相机信息更改72行代码
