import random 
 
fin = open("./dataset.txt", 'rb') 
f60out = open("./FOOTTRAFFIC_train_list.txt", 'wb') 
f40out = open("./FOOTTRAFFIC_test_list.txt", 'wb') 
for line in fin: 
    r = random.random() 
    if r < 0.60: 
        f60out.write(line) 
    else: 
        f40out.write(line) 
fin.close() 
f60out.close() 
f40out.close() 