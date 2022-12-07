# 상의 긴팔 long_sleeve
# 상의 반팔 short_sleeve
# 상의 민소매 sleeveless
# 상의 원피스 onepice
# 하의 긴바지 long_pants
# 하의 반바지 short_pants
# 하의 치마 skirt
# 하의 해당없음 none
# 캐리어 carrier
# 우산 umbrella
# 가방 bag
# 모자 hat
# 안경 glasses
# 해당없음 none
top = ['long_sleeve', 'short_sleeve', 'sleeveless', 'onepice']
pants = ['long_pants', 'short_pants', 'skirt', 'none']
acce = ['carrier', 'umbrella', 'bag', 'hat', 'glasses', 'none']
f = open("class-list.txt", 'a')
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
