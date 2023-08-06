'''
Contains examples of standard likelihood functions for usage in the package.
'''
import numpy as np

def isotropic_gaussian(q):
    '''
    An isotropic Gaussian likelihood function.

    Parameters
    ----------
    q : numpy array
        Position parameter


    Returns
    -------
    r : dictionary
        returns the log likelihood under the ``llh`` key, and the gradient under the ``grad`` key.
    '''

    llh = -np.sum(q * q) / 2
    grad = -q

    return {"llh": llh, "grad": grad}


def ica( q, data, idxs=None, alpha=1 ):
    '''
    Independent Component Analysis likelihood with a Gaussian prior.

    Parameters
    ----------
    q : numpy array
        An (N,1) numpy array of the position parameter
    data : numpy array
        A (N,d) array, where the d datapoints have dimensionality N.
    idxs : list or iterable, optional
        A list of data indexes to use in the calculation, default is to use all of them
    alpha : float, optional
        The variance of the Gaussian prior, default 1.


    Returns
    -------
    r : dictionary
        returns the log likelihood under the ``llh`` key, the gradient under the ``grad`` key and the gradients for each data point are given in ``grad_data``.
    '''

    if (idxs is None):
        X = data
    else:
        X = data[:,idxs]

    # Prior

    Vprior = -0.5*np.sum(q**2) / alpha
    Fprior = -q / alpha

    # LLH

    D,N = data.shape

    W = np.reshape( q , (D,D) ).T
    Winv = np.linalg.inv(W)
    Wdet = np.linalg.det(W)

    WX2 = -0.5 * np.dot( W, X )

    em2x = np.exp(2*WX2 )
    tanhx = (1.0 - em2x) / (1.0 + em2x )
    logcoshx = np.log1p( em2x ) - WX2 - 0.69314718

    V = N * np.log( np.abs( Wdet ) ) - 2*np.sum( logcoshx )

    F = -np.einsum('ij,kj->kij',tanhx,X).reshape( (D*D,-1 ) )
    F = F + np.reshape( Winv.flatten(), q.shape )

    TotalV = V + Vprior
    TotalF = (N * np.mean(F, 1, keepdims=True) + Fprior)

    return {"llh": TotalV  , "grad": TotalF, "grad_data": F}


def blr(q, data, t, idxs=None, alpha=100 ):
    '''
    Bayesian Logistic Regression with a Gaussian prior.

    Parameters
    ----------
    q : numpy array
        A (N,1) array of the N-dimensional position parameter
    data : numpy array
        A (N,d) array, where the d datapoints have dimensionality N.
    t : numpy array
        A (1,d) binary array of indicator values
    idxs : list or iterable, optional
        A list of indexes to use in the BLR calculation
    alpha : float, optional
        The variance of the Gaussian prior, default 100.


    Returns
    -------
    r : dictionary
        returns the log likelihood under the ``llh`` key, the gradient under the ``grad`` key and the gradients for each data point are given in ``grad_data``.
    '''

    Ndata = data.shape[1]

    if idxs is None:
        idxs = np.arange(Ndata)

    X = data[:, idxs].T
    t = t[:, idxs].T

    # Prior
    Vprior = -0.5 * np.sum(q ** 2) / alpha
    Fprior = -q / alpha

    # Posterior
    tv = np.dot(X, q)
    exptv = np.exp(-tv)

    VV = tv * t - np.log(1 + exptv) - tv

    #V = np.sum(tv * t) - np.sum(np.log(1 + exptv)) - np.sum(tv)
    F = X * (t - 1.0 / (1.0 + exptv))

    TotalV = (np.sum(VV) + Vprior)

    TotalF = (Ndata * np.mean(F, 0, keepdims=True) + Fprior.T).T

    return {"llh": TotalV, "llh_data":VV , "grad": TotalF, "grad_data": F.T}
