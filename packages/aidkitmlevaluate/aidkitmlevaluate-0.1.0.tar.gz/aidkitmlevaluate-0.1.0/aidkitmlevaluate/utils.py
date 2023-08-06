import numpy as np
import pandas as pd



def calc_acc(label, prediction, total_batches):
    right_pred = 0
    total_images = 0
    for batch in range(total_batches):
        right_pred = right_pred + (np.sum(label[batch] == prediction[batch]))
        total_images = total_images + len(prediction[batch])

    accuracy = right_pred/total_images

    return accuracy

def plot_conf_matrix(label_list, prediction_list, total_images):
    label_array = np.concatenate(label_list, axis=0)
    pred_array = np.concatenate(prediction_list, axis=0)

    label_array = label_array[:total_images]
    pred_array = pred_array[:total_images]

    actual_label = pd.Series(label_array, name='Actual')
    pred_label = pd.Series(pred_array, name='Predicted')
    df_confusion = pd.crosstab(actual_label, pred_label, rownames=['Actual'], colnames=['Predicted'], margins=True)
    return df_confusion

def plot_roc(label_list, prediction_list, total_images):
    pred_array = []
    label_array = []
    for step in range(len(prediction_list)):
        pred_array.extend(prediction_list[step][0][:,1])
        label_array.extend(label_list[step])

    label_array = label_array[:total_images]
    pred_array = pred_array[:total_images]

    # false positive rate
    fpr = []
    # true positive rate
    tpr = []
    # Iterate thresholds from 0.0, 0.01, ... 1.0
    thresholds = np.arange(-1.0, 1.0, .1)

    # get number of positive and negative examples in the dataset
    Pos = sum(label_array)
    Neg = len(label_array) - Pos

    # iterate through all thresholds and determine fraction of true positives
    # and false positives found at this threshold
    for thresh in thresholds:
        FP = 0
        TP = 0
        for i in range(len(pred_array)):
            if (pred_array[i] > thresh):
                if label_array[i] == 1:
                    TP = TP + 1
                if label_array[i] == 0:
                    FP = FP + 1
        fpr.append(FP / float(Neg))
        tpr.append(TP / float(Pos))

    return fpr, tpr

