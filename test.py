import MyModule

data, header = MyModule.read_csv('regresja_przykład.csv')
data = MyModule.get_data_lists(data, (8, 9, 10))
data = [list(map(float, x)) for x in data]
for i in range(len(data)):
    data[i] = data[i][87:]
model_1_quality_assessment, model_1_error_list = \
    MyModule.regression_model_quality_assessment(list(zip(data[0], data[1])))
model_2_quality_assessment, model_2_error_list = \
    MyModule.regression_model_quality_assessment(list(zip(data[0], data[2])))

hist = MyModule.calc_histogram(model_1_error_list, 20)

copy_list = model_1_error_list
bins = 20
min_val = min(copy_list)
copy_list = [x + abs(min_val) for x in copy_list]
norm = [float(i)/max(copy_list) for i in copy_list]
histogram = []
for i in range(bins):
    histogram.append(0)
step = 1/bins
for i in range(bins):
    temp = []
    for val in norm:
        lower_boundary = i*step
        upper_boundary = (i+1)*step
        if lower_boundary <= val <= upper_boundary:
            histogram[i] += 1
            temp.append(val)
    for val in temp:
        norm.remove(val)
pass