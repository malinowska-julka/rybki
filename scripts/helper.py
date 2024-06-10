import re
import statistics
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def mean_temp(temp_str):
    l = re.findall(r"\d+", temp_str)
    return statistics.mean(map(int, l))


def strip_length(length_str):
    l = re.findall(r"\d+", length_str)
    if len(l) > 1:
        return math.ceil(statistics.mean(map(int, l)))
    else:
        return l[0]

def plot_regression(y_test,test_predictions,title):
    error = mean_squared_error(y_test, test_predictions)
    j = y_test.to_frame()
    j["predictions"] = test_predictions

    plt.scatter(y_test,test_predictions)
    plt.xlim(0, 10)
    plt.ylim(0,10)
    plt.xlabel("true")
    plt.ylabel("prediction")
    plt.text(6,8.5, 'MSE: ' + str(round(error,4)), fontsize = 20)
    plt.savefig("model_accuracy/" + title +".png")