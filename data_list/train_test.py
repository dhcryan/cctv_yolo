import random 
# add region name
fin = open("./foottraffic/ja_ma.txt", 'rb') 
f60out = open("./foottraffic/FOOTTRAFFICc_train_list.txt", 'wb') 
f40out = open("./foottraffic/FOOTTRAFFICc_test_list.txt", 'wb') 
for line in fin: 
    r = random.random() 
    if r < 0.60: 
        f60out.write(line) 
    else: 
        f40out.write(line) 
fin.close() 
f60out.close() 
f40out.close() 