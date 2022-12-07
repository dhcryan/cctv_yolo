filepath='/home/dhc4003/cctv_yolo/data_list/foottraffic/dataset.txt'
add_path='foottraffic/ja_ma/'
with open(filepath, 'r') as f:     # load file
    lines = f.read().splitlines()  # read lines
    
with open('./foottraffic/ja_ma.txt', 'w') as f:  # here to add region.txt
    f.write('\n'.join([add_path+line for line in lines]))
