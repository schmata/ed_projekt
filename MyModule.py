import numpy as np


def classification_model_quality_assessment(confusion_matrix):
    tn, fp, fn, tp = confusion_matrix['tn'], confusion_matrix['fp'], confusion_matrix['fn'], confusion_matrix['tp'],
    accuracy = (tn + tp) / (tn + fp + fn + tp)
    overall_error_rate = 1 - accuracy
    sensitivity = tp / (fn + tp)
    fnr = fn / (fn + tp)
    specificity = tn / (tn + fp)
    fpr = fp / (tn + fp)
    precision = tp / (fp + tp)
    f1 = (2 * sensitivity * precision) / (sensitivity + precision)
    return {
        "accuracy": accuracy,
        "overall_error_rate": overall_error_rate,
        "sensitivity": sensitivity,
        "fnr": fnr,
        "specificity": specificity,
        "fpr": fpr,
        "precision": precision,
        "f1": f1
    }


def regression_model_quality_assessment(data):
    error_list = calc_quantitative_variable_error(data)
    mae = regression_MAE(error_list)
    mape = regression_MAPE(error_list, [x[0] for x in data])
    mse = regression_MSE(error_list)
    rmse = pow(mse, 1/2)
    return {
        "mae": mae,
        "mape": mape,
        "mse": mse,
        "rmse": rmse
    }, error_list


def calc_quantitative_variable_error(data):
    error_list = []
    for line in data:
        error_list.append(line[0] - line[1])
    return error_list


def regression_MAE(error_list):
    n = len(error_list)
    total = 0
    for value in error_list:
        total += abs(value)
    return total/n


def regression_MAPE(error_list, true_list):
    n = len(error_list)
    total = 0
    for error_value, true_value in zip(error_list, true_list):
        total += abs(error_value)/true_value
    return (total/n) * 100


def regression_MSE(error_list):
    n = len(error_list)
    total = 0
    for value in error_list:
        total += value*value
    return total/n


def read_csv(file, heading=True, sep=',', decimal='.'):
    f = open(file, "r")
    if heading:
        header = f.readline()
        header = header.strip().split(sep)
    else:
        header = None
    data = []
    lines = f.readlines()
    for line in lines:
        line = line.strip().split(sep)
        # print(line)
        data.append(line)
        # for value in line:
        #     if unique_values.count(value) == 0:
        #         unique_values.append(value)
        # if len(unique_values) == 2:
        #     break
    # print(data)
    return data, header


def get_data_lists(data, indices: (int, int)):
    prepared_data = []
    for i in indices:
        temp = []
        for line in data:
            temp.append(line[i])
        prepared_data.append(temp)
    return prepared_data


def get_data_single(data, indices: (int, int)):
    prepared_data = []
    for line in data:
        temp = []
        for i in indices:
            temp.append(line[i])
        prepared_data.append(temp)
    return prepared_data


def get_unique_values(data, positive_label: str = None, max_len=None):
    unique_values = []
    for value in data:
        if unique_values.count(value) == 0:
            unique_values.append(value)
            if len(unique_values) == max_len:
                break
    if positive_label is not None:
        try:
            unique_values.remove(positive_label)
        except ValueError:
            print("positive_label is not present in data")
        else:
            unique_values.insert(0, positive_label)
    return unique_values


def get_thresholds(probability_data, labels=None):
    tmp = probability_data
    tmp.sort(reverse=True, key=lambda x: x[1])
    thresholds = get_unique_values(tmp)
    for label in labels:
        thresholds.remove(label)
    thresholds = list(map(float, thresholds))

    return thresholds


def calculate_confusion_matrix(data, labels: list = None, positive_label: str = None, indices: (int, int) = None):
    if labels is not None:
        unique_values = labels
    else:
        unique_values = get_unique_values(data, positive_label)
    tp = tn = fp = fn = 0
    if indices is not None and len(indices) == 2:
        indice0, indice1 = indices
    else:
        indice0, indice1 = 0, 1
    for true_value, predicted_value in zip(data[indice0], data[indice1]):
        if true_value == predicted_value == unique_values[0]:
            tp += 1
        elif true_value == predicted_value == unique_values[1]:
            tn += 1
        elif true_value == unique_values[1] and predicted_value == unique_values[0]:
            fp += 1
        elif true_value == unique_values[0] and predicted_value == unique_values[1]:
            fn += 1
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }


def calc_ROC_points(confusion_matrix):
    tn, fp, fn, tp = confusion_matrix['tn'], confusion_matrix['fp'], confusion_matrix['fn'], confusion_matrix['tp'],
    sensitivity = tp / (fn + tp)
    specificity = 1 - (tn / (tn + fp))
    return specificity, sensitivity


def confusion_matrix_thresholds(predictions_by_threshold, probability_data, labels):
    tp = tn = fp = fn = 0
    for true_value, predicted_value in zip(probability_data[0], predictions_by_threshold):
        if true_value == predicted_value == labels[0]:
            tp += 1
        elif true_value == predicted_value == labels[1]:
            tn += 1
        elif true_value == labels[1] and predicted_value == labels[0]:
            fp += 1
        elif true_value == labels[0] and predicted_value == labels[1]:
            fn += 1
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }


def ROC_curve(probability_data, labels):
    import multiprocessing as mp
    # tmp = []
    # tmp[0] = list(map(lambda x: x.replace(labels[0], '1'), probability_data[0]))
    # tmp[0] = list(map(lambda x: x.replace(labels[1], '0'), probability_data[0]))
    thresholds = get_unique_values(probability_data[1])
    # thresholds.append('.0')
    thresholds.sort(reverse=True)
    predictions_by_thresholds = []
    for threshold in thresholds:
        tmp = []
        for value in probability_data[1]:
            if value > threshold:
                tmp.append(labels[0])
            else:
                tmp.append(labels[1])
        predictions_by_thresholds.append(tmp)

    pool = mp.Pool()
    # matrices = [pool.apply(confusion_matrix_thresholds,
    #                        args=(predictions_by_threshold,
    #                              probability_data,
    #                              labels))
    #             for predictions_by_threshold in predictions_by_thresholds]
    matrices = pool.starmap(confusion_matrix_thresholds, [(predictions_by_threshold, probability_data, labels)
                                                          for predictions_by_threshold in predictions_by_thresholds])
    pool.close()

    points = []
    for matrix in matrices:
        points.append(calc_ROC_points(matrix))
    points.append((1.0, 1.0))

    return points


def calc_AUC(points):
    auc = 0.0
    for i in range(0, len(points) - 1):
        a = points[i][1]
        b = points[i + 1][1]
        h = points[i + 1][0] - points[i][0]
        auc += ((a + b) / 2) * h
    return auc
