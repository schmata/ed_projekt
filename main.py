import MyModule

data, header = MyModule.read_csv('klasyfikacja_przykład.csv')

prediction_data = MyModule.get_data_lists(data, (0, 1, 3))
model_1_probability_data = MyModule.get_data_lists(data, (0, 2))
model_2_probability_data = MyModule.get_data_lists(data, (0, 4))

# sorted1 = [[x, y] for y, x in sorted(zip(model_1_probability_data[1], model_1_probability_data[0]),
#                                      key=lambda pair: pair[0],
#                                      reverse=True)]
# [model_1_probability_data[0], model_1_probability_data[1]] = map(list, zip(*sorted1))
# pass

labels = MyModule.get_unique_values(prediction_data[0], max_len=2)
positive_label = labels[0]

model_1_probability_data[0] = list(map(lambda x: x.replace(labels[0], '1'), model_1_probability_data[0]))
model_1_probability_data[0] = list(map(lambda x: x.replace(labels[1], '0'), model_1_probability_data[0]))
model_1_thresholds = MyModule.get_unique_values(model_1_probability_data[1])
model_1_thresholds.sort(reverse=True)

for threshold in model_1_thresholds:
    tmp = []
    for value in model_1_probability_data[1]:
        if value > threshold:
            tmp.append('1')
        else:
            tmp.append('0')
    model_1_probability_data.append(tmp)

matrices = []
for i in range(2, len(model_1_probability_data)):
    tp = tn = fp = fn = 0
    for true_value, predicted_value in zip(model_1_probability_data[0], model_1_probability_data[i]):
        if true_value == predicted_value == '1':
            tp += 1
        elif true_value == predicted_value == '0':
            tn += 1
        elif true_value == '0' and predicted_value == '1':
            fp += 1
        elif true_value == '1' and predicted_value == '0':
            fn += 1
    matrices.append({
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    })

calculations = []
for matrix in matrices:
    calculations.append(MyModule.calc_sens_and_spec(matrix))
pass

# model1_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 1))
# model2_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 2))
#
# model1_quality_assessment = MyModule.model_quality_assessment(model1_confusion_matrix)
# model2_quality_assessment = MyModule.model_quality_assessment(model2_confusion_matrix)

# confusion_matrices = []
# quality_assessments = []
# for model in prepared_data:
#     confusion_matrix = MyModule.calculate_confusion_matrix(model, labels)
#     confusion_matrices.app
#     end(confusion_matrix)
#
#     quality_assessment = MyModule.model_quality_assessment(confusion_matrix)
#     quality_assessments.append(quality_assessment)
#
# for quality_assessment in quality_assessments:
#     print(quality_assessment)
# print(data)
# for line in data[:][:]:
#     print(line)
# labels = MyModule.get_unique_values(data)

# MyModule.calculate_confusion_matrix(data)