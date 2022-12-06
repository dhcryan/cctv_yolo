filepath='/home/dhc4003/cctv_yolo/data_list/foottraffic/ye_ma.txt'
add_path='foottraffic/ye_ma/'
with open(filepath, 'r') as f:     # load file
    lines = f.read().splitlines()  # read lines
with open('./foottraffic/dataset.txt', 'w') as f: 
    f.write('\n'.join([add_path+line for line in lines]))
