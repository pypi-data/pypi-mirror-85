"""This module contains the Interpolator object that can be created
from a trained Emulator."""
import warnings

import asdf
import emcee
import george
from george import kernels
import numpy as np
import pyDOE as pd
import scipy.optimize as op
from tqdm import tqdm

from tremulator.util import arrays_to_theta, kernel_to_map, map_to_kernel

import pdb

class Interpolator(object):
    """
    Gaussian process interpolator

    Parameters
    ----------
    bounds : array
        lower and upper bounds for each dimension of the input theta
    theta : array (n_samples, n_dim)
        input coordinates
    y : array (n_samples, )
        function values
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    hyper_parameters : array or None
        vector of hyper parameters
    hyper_bounds : array or None
        only required if hyper_vector is None, bounds for hyper_vector
        optimization
    alpha : array or None, optional
        gp alpha for exact reproduction (default: None)
    n_restarts : int
        number of random initialization positions for hyperparameters
        optimization (default: 5)
    """
    def __init__(
            self,
            bounds=None,
            theta=None,
            y=None,
            kernel=None,
            hyper_parameters=None,
            hyper_bounds=None,
            alpha=None,
            n_restarts=5
    ):
        self.theta = theta
        self.bounds = bounds
        self.y = y
        self.kernel = kernel
        self.hyper_parameters = hyper_parameters
        self.hyper_bounds = hyper_bounds
        self.alpha = alpha
        self.n_restarts = n_restarts

    def _check_theta(self, theta):
        """Check whether theta has right dimensions"""
        theta = np.atleast_2d(theta)
        if len(theta.shape) > 2 or theta.shape[1] != self._n_dim:
            raise TypeError("theta should have shape (n_samples, n_dim)")
        return theta

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        if value is None:
            warnings.warn("theta will need to be loaded", RuntimeWarning)
            self._theta = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2:
                raise TypeError("theta should have shape (n_samples, n_dim)")
            self._n_dim = value.shape[1]
            self._n_samples = value.shape[0]
            self._theta = value

    def _within_bounds(self, theta):
        """Return indices of given theta within the given bounds"""
        # difference between coord and the bounds of its dimension
        diff = (theta.reshape(-1, self._n_dim, 1)
                - self.bounds.reshape(1, self._n_dim, 2))

        # out_of bounds := coord - lower_bound < 0 or coord - upper_bound > 0
        out_of_bounds = ((diff[..., 0] < 0) | (diff[..., 1] > 0)).any(axis=-1)

        return ~out_of_bounds

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        if value is None:
            try:
                value = np.ones((self._n_dim, 2))
                value[:, 0] = -np.inf
                value[:, 1] = np.inf
                self._bounds = value
                warnings.warn("no bounds provided, we might end up extrapolating...",
                              RuntimeWarning)
            except AttributeError:
                warnings.warn("bounds will need to be loaded",
                              RuntimeWarning)
                self._bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2 or value.shape[1] != 2:
                raise TypeError("bounds should have shape (n_dim, 2)")
            if (value[:, 0] >= value[:, 1]).any():
                raise ValueError("cannot have lower bound >= upper bound")
            self._n_dim = value.shape[0]
            self._bounds = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value is None:
            warnings.warn("y will need to be loaded", RuntimeWarning)
            self._y = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("y should have shape (n_samples, )")
            elif value.shape[0] != self._n_samples:
                raise ValueError("y should have same n_samples as theta")
            else:
                self._y = value

    @property
    def kernel(self):
        return self._kernel

    @kernel.setter
    def kernel(self, kernel):
        if kernel is None:
            warnings.warn("kernel will need to be loaded", RuntimeWarning)
            self._kernel = None
        elif isinstance(kernel, kernels.Kernel):
            self._kernel_dim = kernel.ndim
            self._kernel = kernel
        else:
            raise TypeError("kernel needs to be Kernel instance")

    @property
    def n_restarts(self):
        return self._n_restarts

    @n_restarts.setter
    def n_restarts(self, value):
        if type(value) is int:
            self._n_restarts = value
        else:
            raise TypeError("n_restarts has to be int")

    @property
    def hyper_parameters(self):
        return self._hyper_parameters

    @hyper_parameters.setter
    def hyper_parameters(self, value):
        # if hyper_parameters is None, we need to optimize it later
        if value is None:
            self._optimize = True
            self._hyper_parameters = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("hyper_parameters should be 1d")
            elif value.shape[0] != self._kernel_dim + 1:
                raise ValueError("hyper_parameters should have size {}".format(self._kernel_dim + 1))
            else:
                self._optimize = False
                self._hyper_parameters = value

    @property
    def hyper_bounds(self):
        return self._hyper_bounds

    @hyper_bounds.setter
    def hyper_bounds(self, value):
        # if no optimization required, all is well
        # self._optimize is True if no hyper_parameters are given
        if not self._optimize:
            self._hyper_bounds = None

        # need hyper_bounds if optimization required
        elif self._optimize and value is None:
            warnings.warn("hyper_parameters will need to be loaded",
                          RuntimeWarning)
            self._hyper_bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2:
                raise TypeError("hyper_bounds should be 2d")
            elif (value.shape[0] == self._kernel_dim + 1 and
                  value.shape[1] == 2):
                self._hyper_bounds = value
            else:
                raise TypeError("hyper_bounds should have size (n_dim_kernel + 1, 2)")

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if value is None:
            self._alpha = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("alpha should be 1d")
            elif value.shape[0] != self.theta.shape[0]:
                raise ValueError("alpha should have same n_samples as theta")
            else:
                self._alpha = value

    def _gp_init(self):
        self._gp = george.GP(self.kernel)
        self._gp.compute(self.theta)
        if self.alpha is not None:
            self._gp._alpha = self.alpha

        if self._optimize:
            self._optimize_hyper_parameters()
        else:
            self._gp.set_parameter_vector(self.hyper_parameters)

    @property
    def gp(self):
        try:
            # if hyper_parameters or alpha were updated, reload them in the gp
            if not (self._gp.get_parameter_vector()
                    == self.hyper_parameters).all():
                self._gp.set_parameter_vector(self.hyper_parameters)
            if not (self._gp._alpha == self.alpha).all():
                self._gp._alpha = self.alpha
            return self._gp
        except AttributeError:
            self._gp_init()
            return self._gp

    def _optimize_hyper_parameters(self):
        """Optimize the Gaussian process hyperparameters by minimizing the log
        likelihood.

        The optimizations is performed for num_restarts random
        starting points within hyper_bounds and the hyperparameters
        resulting in the highest log_likelihood are chosen.
        """
        # define the negative log likelihood
        def nll(p):
            self._gp.set_parameter_vector(p)
            ll = self._gp.log_likelihood(self.y, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        # And the gradient of the objective function.
        def grad_nll(p):
            self._gp.set_parameter_vector(p)
            return -self._gp.grad_log_likelihood(self.y, quiet=True)

        parameters = []
        results = []
        for _ in range(self.n_restarts):
            # Run the optimization routine.
            p0 = np.random.uniform(low=self.hyper_bounds[:, 0],
                                   high=self.hyper_bounds[:, 1])

            # find optimal parameters
            result = op.minimize(nll, p0, jac=grad_nll, method="L-BFGS-B")
            parameters.append(result.x)

            # now compute the loglikelihood for these parameters
            self._gp.set_parameter_vector(result.x)
            results.append(self._gp.log_likelihood(self.y, quiet=True))

        # the highest value of the loglikelihood corresponds to the
        # wanted hyperparameters
        best_idx = np.argmax(results)

        # Update the kernel
        self._gp.set_parameter_vector(parameters[best_idx])
        self.hyper_parameters = parameters[best_idx]

    def predict(self, theta, var=False, cov=False, **kwargs):
        theta = self._check_theta(theta)

        # check if all values are within the bounds
        out_of_bounds = ~self._within_bounds(theta)
        if out_of_bounds.any():
            warnings.warn("extrapolating for {}".format(theta[out_of_bounds]),
                          RuntimeWarning)
        return self.gp.predict(self.y, theta, return_var=var, return_cov=cov,
                               **kwargs)

    def _from_dict(self, dic):
        """Convert dict to Emulator"""
        self.kernel = map_to_kernel(dic["kernel"][:])
        self.bounds = dic["bounds"][:]
        self.hyper_bounds = dic["hyper_bounds"][:]
        self.theta = dic["theta"][:]
        self.y = dic["y"][:]
        self.hyper_parameters = dic["hyper_parameters"][:]
        self.alpha = dic["alpha"][:]

    def _to_dict(self):
        """Convert Emulator to dict for saving"""
        # if alpha has not been computed, calculate it
        if self.gp._alpha is None:
            self.gp._compute_alpha(self.y, cache=True)
        parameters = {
            "kernel": kernel_to_map(self.kernel),
            "bounds": self.bounds,
            "hyper_bounds": self.hyper_bounds,
            "theta": self.theta,
            "y": self.y,
            "hyper_parameters": self.gp.get_parameter_vector(),
            "alpha": self.gp._alpha,
        }
        return parameters

    def load(self, fname):
        with asdf.open(fname, copy_arrays=True) as af:
            self._from_dict(af)
