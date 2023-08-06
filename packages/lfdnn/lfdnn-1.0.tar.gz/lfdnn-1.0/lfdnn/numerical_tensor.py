from lfdnn.tensor import tensor
from lfdnn.operator import accuracy
from lfdnn.utils import one_hot

def numerical_accuracy(y_predict_prob, y_true):
    '''accuracy value computed from two probability vectors

    Parameters
    ----------
    y_predict_prob: array-like, number of samples x the probability vector at each sample
    y_true: array-like, number of samples x the embedded true class vector

    Returns
    -------
    acc: a numerical accuracy value
    '''
    input_dim = y_predict_prob.shape[0]
    output_dim = y_predict_prob.shape[1]
    y_predict_prob_tensor = tensor([input_dim, output_dim], 'predict')
    y_true_tensor = tensor([input_dim, output_dim], 'label')
    feed = {'predict': y_predict_prob, 'label': one_hot(y_true, output_dim)}
    return accuracy(y_predict_prob_tensor, y_true_tensor).eval(feed)