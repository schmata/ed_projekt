import MyModule

if __name__ == '__main__':
    # data, header = MyModule.read_csv('klasyfikacja_przykład.csv')
    data, header = MyModule.read_csv('regresja_przykład.csv')
    # data, header = MyModule.read_csv('example.csv')

    data = MyModule.get_data_lists(data, (8, 9, 10))
    data = [list(map(float, x)) for x in data]
    for i in range(len(data)):
        data[i] = data[i][87:]
    model_1_quality_assessment, model_1_error_list = \
        MyModule.regression_model_quality_assessment(list(zip(data[0], data[1])))
    model_2_quality_assessment, model_2_error_list = \
        MyModule.regression_model_quality_assessment(list(zip(data[0], data[2])))

    print(model_1_quality_assessment)
    print(model_2_quality_assessment)
#     prediction_data = MyModule.get_data_lists(data, (0, 1, 3))
#     model_1_probability_data = MyModule.get_data_lists(data, (0, 2))
#     model_2_probability_data = MyModule.get_data_lists(data, (0, 4))
#
#     labels = MyModule.get_unique_values(prediction_data[0], max_len=2)
#     tmp = labels[0]
#     labels[0] = labels[1]
#     labels[1] = tmp
#     positive_label = labels[0]
#
#     # # start_time = time.time()
#     model_1_ROC_points = MyModule.ROC_curve(model_1_probability_data, labels)
#     # # print("Time1: ", time.time() - start_time)
#     # # start_time = time.time()
#     # model_2_ROC_points = MyModule.ROC_curve(model_2_probability_data, labels)
#     # # print("Time2: ", time.time() - start_time)
#
#     model_1_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 1))
#     model_2_confusion_matrix = MyModule.calculate_confusion_matrix(prediction_data, labels, indices=(0, 2))
# #
#     model_1_quality_assessment = MyModule.classification_model_quality_assessment(model_1_confusion_matrix)
#     model_2_quality_assessment = MyModule.classification_model_quality_assessment(model_2_confusion_matrix)
#
#     auc = MyModule.calc_AUC(model_1_ROC_points)
#     print(auc)
#
#     for point in model_1_ROC_points:
#         print(point)
