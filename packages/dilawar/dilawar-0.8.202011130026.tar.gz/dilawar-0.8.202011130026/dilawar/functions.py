# Helpful functions.

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import numpy as np

# This one is from here:
# https://scipy-cookbook.readthedocs.io/items/Matplotlib_SigmoidalFunctions.html
def boltzman(x, xmid, tau):
    """
    evaluate the boltzman function with midpoint xmid and time constant tau
    over x
    """
    return 1. / (1. + np.exp(-(x-xmid)/tau))

def hill(x, n, k=1):
    """hill function.
    """
    return k*(x**n/(1+x**n))

def logistic(x, alpha=1):
    """logistic function.
    """
    return (1+np.exp(-x))**(-alpha)

def sigmoid(x):
    """Sigmoid function.

    """
    return logistic(x, 1)


def test():
    # Plot all functions.
    import matplotlib.pyplot as plt
    x = np.linspace(0, 1, 1000)
    plt.subplot(221)
    for tau in [0.05, 0.1, 0.2, 0.4, 0.8]:
        y = boltzman(x, 0.5, tau)
        plt.plot(x, y, label=f'{tau}')
    plt.title(r'Botzman function: $\frac{1}{1+e^{-(x-x_o)/τ}}$')
    plt.legend()

    plt.subplot(222)
    x = np.logspace(-2, 2, 1000)
    for n in [1,2,3,4]:
        y = hill(x, n)
        plt.semilogx(x, y, label=f'n={n}')
    plt.legend()
    plt.title(r'Hill function: $\frac{x^n}{1+x^n}$')

    plt.subplot(223)
    x = np.linspace(-5, 5, 1000)
    for alpha in [0, 0.1, 0.5, 1, 2, 4, 10, 100]:
        plt.plot(x, logistic(x, alpha), label=fr'$α={alpha}$')
    plt.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
    plt.title(r'Logistic: $(1+e^{-x})^{-α}$')


    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    test()
