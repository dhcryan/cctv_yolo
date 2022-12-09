import json
import cv2
import splitfolders
import shutil
import os
import glob

file_list = os.listdir('./data')

video_name_list = []
for i in range(len(file_list)):
    video_name_list.append(os.path.splitext(file_list[i])[0])
video_name_list = set(video_name_list)

for video_name in video_name_list:
    print('video_name = ', video_name)
    with open('./data/' + video_name + '.json', "r") as st_json:
        json_obj = json.load(st_json)
    width = json_obj["video"]["resolution"][0]
    height = json_obj["video"]["resolution"][1]
    total_frame = json_obj['video']['total_frame']

    video = cv2.VideoCapture('./data/' + video_name + '.mp4')

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
                data2 += t + ' ' + p + ' ' + ac
                dict[data2] = i
                i += 1
                f.write(data + data2 + '\n')
    f.close()
    print("write class-list end...")

    chk = [0 for i in range(540)]
    print("write label start...")
    for anno in json_obj["annotations"]:
        chk[anno['frame']] = 1
        file_name = './preprocessed-data/images/' + \
            video_name + '-' + str(anno['frame']) + '.txt'
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

    print("caputre start...")
    count = 0
    while (video.isOpened()):
        if count >= total_frame:
            break
        ret, image = video.read()
        if ret and chk[count]:
            if (int(video.get(1)) % 1 == 0):
            cv2.imwrite('./preprocessed-data/images/' + video_name +
                        '-' + str(count) + '.jpg', image)
        count += 1
    print("caputre end...")
print("write label end...\n\n")
os.mkdir('./output')
os.mkdir('./output/train')
os.mkdir('./output/val')
os.mkdir('./output/train/labels')
os.mkdir('./output/val/labels')

print("start split data...")
splitfolders.ratio("./preprocessed-data", output="./output",
                   seed=1337, ratio=(.8, .2), group_prefix=2)
print("end split data...\n")

print("start move .txt files...")
os.chdir("./output/train/images")
for file in glob.glob("*.txt"):
    shutil.move(file, '../labels')
os.chdir("../../val/images")
for file in glob.glob("*.txt"):
    shutil.move(file, '../labels')
print("end move .txt files...\n")
