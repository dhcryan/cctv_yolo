import json
import cv2

video_name = '2021-08-01_09-12-00_sun_sunny_out_ja-ma_C0041'
path = './data/'
with open(video_name + '.json', "r") as st_json:
    json_obj = json.load(st_json)
width = json_obj["video"]["resolution"][0]
height = json_obj["video"]["resolution"][1]
total_frame = json_obj['video']['total_frame']
# x1,y1 x1,y2
# x2,y1 x2,y2
# x1 = int(bbox[0])
# y1 = int(bbox[1])
# x2 = int(bbox[2])
# y2 = int(bbox[3])

video = cv2.VideoCapture(
    '/Users/park/it2-team-project/' + video_name + '.mp4')

# 동영상에서 프레임 추출
print("caputre start...")
count = 0
while (video.isOpened()):
    if count >= total_frame:
        break
    ret, image = video.read()
    if ret:
        if (int(video.get(1)) % 1 == 0):
            cv2.imwrite('./images/' + video_name +
                        '-' + str(count) + '.jpg', image)
            count += 1
print("caputre end...\n")

print("write class-list start...")
top = ['long_sleeve', 'short_sleeve', 'sleeveless', 'onepice']
pants = ['long_pants', 'short_pants', 'skirt', 'none']
acce = ['carrier', 'umbrella', 'bag', 'hat', 'glasses', 'none']
f = open("class-list.txt", 'w')
dict = {}
i = 0
for t in top:
    for p in pants:
        for ac in acce:
            data = str(i) + ' '
            data2 = ''
            i += 1
            data2 += t + ' ' + p + ' ' + ac
            dict[data2] = i
            f.write(data + data2 + '\n')
f.close()
print("write class-list end...\n")

print("write label start...")
for anno in json_obj["annotations"]:
    file_name = './labels/' + video_name + '-' + str(anno['frame']) + '.txt'
    f = open(file_name, 'a')
    c_key = anno['top_type'] + ' ' + \
        anno['bottom_type'] + ' ' + anno['accessories']
    class_num = dict.get(c_key, -1)
    bbox = anno["bbox"]
    diff_width = (bbox[2] - bbox[0]) / width
    diff_height = (bbox[3] - bbox[1]) / height
    x = ((bbox[0] + bbox[2]) / 2) / width
    y = ((bbox[1] + bbox[3]) / 2) / height
    data = str(class_num) + ' ' + str(x) + ' ' + str(y) + ' ' + \
        str(diff_width) + ' ' + str(diff_height) + '\n'
    f.write(data)
    f.close()
print("write label end...\n")

# 동영상 테스트
# i = 1
# while (video.isOpened()):
#     ret, frame = video.read()
#     if (i == json_obj["annotations"][30]["frame"]):
#         cv2.line(frame, (x1, y1), (x1, y2), (0, 0, 255), 2)
#         cv2.line(frame, (x1, y2), (x2, y2), (0, 0, 255), 2)
#         cv2.line(frame, (x2, y2), (x2, y1), (0, 0, 255), 2)
#         cv2.line(frame, (x2, y1), (x1, y1), (0, 0, 255), 2)
#     print(i)
#     i += 1
#     if ret:
#         cv2.imshow('image', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# print(i)
