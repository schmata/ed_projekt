import numpy as np


def model_quality_assessment(confusion_matrix):
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


def calc_sens_and_spec(confusion_matrix):
    tn, fp, fn, tp = confusion_matrix['tn'], confusion_matrix['fp'], confusion_matrix['fn'], confusion_matrix['tp'],
    sensitivity = tp / (fn + tp)
    specificity = tn / (tn + fp)
    return [sensitivity, specificity]


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
    for line in data:
        if line[indice0] == line[indice1] == unique_values[0]:
            tp += 1
        elif line[indice0] == line[indice1] == unique_values[1]:
            tn += 1
        elif line[indice0] == unique_values[1] and line[indice1] == unique_values[0]:
            fp += 1
        elif line[indice0] == unique_values[0] and line[indice1] == unique_values[1]:
            fn += 1
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }
    # print(unique_values)
    # f.seek()


def ROC_curve(data):
    pass
