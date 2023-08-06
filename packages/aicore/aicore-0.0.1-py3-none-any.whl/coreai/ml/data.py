import numpy as np
import matplotlib.pyplot as plt

import sklearn.datasets
import numpy as np
import matplotlib.pyplot as plt

_COLORS = [
 '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000'
]

def classification(sd=3, m=10, n_features=2, n_clusters=2, variant='blobs', noise=0.4, factor=0.1):
    if variant == 'circles':
        return sklearn.datasets.make_circles(n_samples=m, factor=factor, noise=noise)
    if variant == 'blobs':
        return sklearn.datasets.make_blobs(n_samples=m, n_features=n_features, centers=n_clusters, cluster_std=sd)

def regression(m=20): 
    ground_truth_w = 2.3 # slope
    ground_truth_b = -8 #intercept
    X = np.random.uniform(0, 1, size=(m, 1))*2
    idxs = np.argsort(X, axis=0)
    idxs = np.squeeze(idxs)
    X = X[idxs]
    Y = ground_truth_w*X + ground_truth_b + 0.2*np.random.randn(m, 1)
    return X, Y

def show_regression_data(X, Y):
    plt.figure()
    plt.scatter(X, Y, c='r')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def visualise_regression_data(X, Y, H=None):
    ordered_idxs = np.argsort(X, axis=0)
    X = X[ordered_idxs]
    Y = Y[ordered_idxs]
    plt.figure()
    plt.scatter(X, Y, c='r', label='Label')
    if H is not None:
        domain = np.linspace(np.min(X.squeeze()), np.max(X.squeeze()))
        domain = np.expand_dims(domain, axis=1)
        y_hat = H(domain)
        plt.plot(domain, y_hat, label='Hypothesis')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def visualise_predictions(H, X, Y=None, n=50):
    xmin, xmax, ymin, ymax = min(X[:, 0]), max(X[:, 0]), min(X[:, 1]), max(X[:, 1])
    meshgrid = np.zeros((n, n))
    for x1_idx, x1 in enumerate(np.linspace(xmin, xmax, n)): # for each column
        for x2_idx, x2 in enumerate(np.linspace(ymin, ymax, n)): # for each row
            h = H(np.array([[x1, x2]]))[0]
            meshgrid[n-1-x2_idx, x1_idx] = h # axis 0 is the vertical direction starting from the top and increasing downward
    if Y is not None:
        for idx in list(set(Y)):
            plt.scatter(X[Y == idx][:, 0], X[Y== idx][:, 1], c=_COLORS[idx])
    else:
        plt.scatter(X[:,0], X[:, 1])
    plt.imshow(meshgrid, extent=(xmin, xmax, ymin, ymax), cmap='winter')
    plt.show()


def show(X, Y, predictions=None):
    for i in range(min(Y), max(Y)+1):
        y = Y == i
        x = X[y]
        plt.scatter(x[:, 0], x[:, 1], c=_COLORS[i])
        if predictions is not None:
            y = predictions == i
            x = X[y]
            plt.scatter(x[:, 0], x[:, 1], c=_COLORS[i], marker='x', s=100)
    plt.show()
