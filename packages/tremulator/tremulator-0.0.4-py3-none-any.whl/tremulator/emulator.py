"""This module contains the Emulator object and its base that uses
Gaussian process regression to fit a model to the output of a given
function.

"""
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


class EmulatorBase(object):
    """
    Base Gaussian process emulator of y(theta)

    Parameters
    ----------
    n_init : int
        number of points in the initial Latin hypercube (default: 10)
    f : callable f(theta)
        function to be emulated f(theta, *args, **kwargs) -> float
    bounds : (n_dim, 2) array
        lower and upper bounds for each dimension of the input theta to f
    f_args : tuple, optional
        positional arguments for f
    f_kwargs : dict, optional
        keyword arguments for f
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    hyper_bounds: array
        lower and upper bounds for each hyperparameter in the given kernel
    n_restarts : int
        number of random initialization positions for hyperparameters
        optimization (default: 5)
    """
    def __init__(
            self,
            n_init=10,
            f=None,
            kernel=None,
            bounds=None,
            args=(),
            kwargs={},
            hyper_bounds=None,
            n_restarts=5,
            pool=None,
            fname=None,
    ):
        if fname is not None:
            self.load(fname=fname)

        else:
            self.n_init = n_init
            self.bounds = bounds
            # in case we are not initializing an empty Emulator to read in theta
            # later, we need to get the n_init values of theta
            if self.bounds is not None:
                self._reset()
            self.f = f
            self.kernel = kernel
            self.args = args
            self.kwargs = kwargs
            self.hyper_bounds = hyper_bounds
            self.n_restarts = n_restarts
            self.pool = pool

    @property
    def n_init(self):
        return self._n_init

    @n_init.setter
    def n_init(self, value):
        if type(value) is int:
            self._n_init = value
        else:
            raise TypeError("n_init has to be int")

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

            # set initial guess for theta
            self.theta_center = 0.5 * (self.bounds[:, 1] + self.bounds[:, 0])
            self.theta_range = self.bounds[:, 1] - self.bounds[:, 0]
            self.theta_init = ((pd.lhs(self._n_dim,
                                       self.n_init,
                                       criterion="maximin") - 0.5)
                               * self.theta_range + self.theta_center)
            # and load test values
            self.theta_test = None

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
        value = self._check_theta(value)
        self._n_samples = value.shape[0]
        self._theta = value

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        if value is None:
            warnings.warn("f will need to be loaded", RuntimeWarning)
            self._f = None
        elif not callable(value):
            raise TypeError("f should be callable")
        else:
            self._f = value

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if value is None:
            self._args = ()
        else:
            self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if value is None:
            self._kwargs = {}
        elif not isinstance(value, dict):
            raise TypeError("kwargs should be dict")
        else:
            self._kwargs = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        value = np.atleast_1d(value)
        if len(value.shape) > 1:
            raise TypeError("y should have shape (n_samples, )")
        elif value.shape[0] != self._n_samples:
            raise TypeError("y should have same n_samples as theta")
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
    def hyper_bounds(self):
        return self._hyper_bounds

    @hyper_bounds.setter
    def hyper_bounds(self, value):
        if value is None:
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
    def n_restarts(self):
        return self._n_restarts

    @n_restarts.setter
    def n_restarts(self, value):
        if type(value) is int:
            self._n_restarts = value
        else:
            raise TypeError("n_restarts has to be int")

    def _reset(self):
        """Reset theta to a Latin hypercube with n_init points"""
        # theta_init is set when loading bounds
        self.theta = self.theta_init
        # set theta_test to None to automatically load the test points
        # can be updated later
        self.theta_test = None

    @property
    def theta_test(self):
        return self._theta_test

    @theta_test.setter
    def theta_test(self, value):
        """Create theta grid spanning parameter space for testing"""
        if value is None:
            # for low-dimensional data, sample regular grid
            if self._n_dim <= 4:
                self._theta_test = arrays_to_theta(*np.linspace(self.bounds[:, 0],
                                                                self.bounds[:, 1],
                                                                5).T)
            # otherwise, hypercube with fixed number of points
            else:
                self._theta_test = ((pd.lhs(self._n_dim, 512, criterion="maximin") - 0.5)
                                    * self.theta_range + self.theta_center)

        else:
            self._theta_test = self._check_theta(value)

    def _optimize_hyper_parameters(self, verbose=False):
        """Optimize the Gaussian process hyperparameters by minimizing the log
        likelihood.

        The optimizations is performed for n_restarts random
        starting points within hyper_bounds and the hyperparameters
        resulting in the highest log_likelihood are chosen.
        """
        # define the negative log likelihood
        def nll(p):
            self.gp.set_parameter_vector(p)
            ll = self.gp.log_likelihood(self.y, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        # And the gradient of the objective function.
        def grad_nll(p):
            self.gp.set_parameter_vector(p)
            return -self.gp.grad_log_likelihood(self.y, quiet=True)

        if verbose:
            # Print the initial ln-likelihood.
            print("Initial log likelihood: "
                  "{}".format(self.gp.log_likelihood(self.y)))

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
            self.gp.set_parameter_vector(result.x)
            results.append(self.gp.log_likelihood(self.y, quiet=True))

        # the highest value of the loglikelihood corresponds to the
        # wanted hyperparameters
        best_idx = np.argmax(results)

        # Update the kernel
        self.gp.set_parameter_vector(parameters[best_idx])

        if verbose:
            # print the final log-likelihood.
            print("Final log likelihood: "
                  "{}".format(self.gp.log_likelihood(self.y)))

    def _gp_init(self):
        self._gp = george.GP(self.kernel)
        self._gp.compute(self.theta)
        try:
            # if y has already been loaded, we don't need to recompute it
            # but it should have the same shape is y
            if self.y.shape[0] != self.theta.shape[0]:
                raise TypeError("y should have same n_samples as theta")
        except AttributeError:
            if self.pool is not None:
                map_fn = self.pool.map
            else:
                map_fn = map

            # create dummy function that already has args and kwargs passed
            def f(theta): return self.f(theta, *self.args, **self.kwargs)

            self.y = list(map_fn(f, self.theta.tolist()))

    @property
    def gp(self):
        try:
            return self._gp
        except AttributeError:
            self._gp_init()
            return self._gp

    def predict(self, theta, var=False, cov=False, **kwargs):
        """
        Predict f(theta) using the GP emulator
        """
        theta = self._check_theta(theta)
        return self.gp.predict(self.y, theta, return_var=var, return_cov=cov,
                               **kwargs)

    def add(self, theta):
        """Add observations theta to the emulator"""
        theta = self._check_theta(theta)

        # check if we are actually adding new coordinates
        if theta.size == 0:
            pass
        else:
            # create dummy function that already has args and kwargs passed
            def f(theta): return self.f(theta, *self.args, **self.kwargs)

            if self.pool is not None:
                map_fn = self.pool.map
            else:
                map_fn = map

            y = list(map_fn(f, theta.tolist()))

            is_nan = np.isnan(y)
            if is_nan.any():
                warnings.warn("NaNs in function, dropping theta = {}".format(theta[is_nan]),
                              RuntimeWarning)
                theta = theta[~is_nan]
                y = y[~is_nan]
            # update the coordinates and function values
            self.theta = np.vstack([self.theta, theta])
            self.y = np.concatenate([self.y, y])

            # now get the new Gaussian process
            self.gp.compute(self.theta)

    def _to_dict(self):
        """Convert Emulator to dict for saving"""
        # if alpha has not been computed, calculate it
        if self.gp._alpha is None:
            self.gp._compute_alpha(self.y, cache=True)
        parameters = {
            "n_init": self.n_init,
            # # cannot save functions to asdf...
            # "f": self.f,
            # # if args or kwargs are None, or not built-in,
            # # asdf does not transfer them correctly
            # "args": self.args,
            # "kwargs": self.kwargs,
            "kernel": kernel_to_map(self.kernel),
            "bounds": self.bounds,
            "hyper_bounds": self.hyper_bounds,
            "n_restarts": self.n_restarts,
            "theta": self.theta,
            "y": self.y,
            "hyper_parameters": self.gp.get_parameter_vector(),
            "alpha": self.gp._alpha,
        }
        return parameters

    def _from_dict(self, dic):
        """Convert dict to Emulator"""
        self.n_init = dic["n_init"]
        self.kernel = map_to_kernel(dic["kernel"][:])
        self.bounds = dic["bounds"][:]
        self.hyper_bounds = dic["hyper_bounds"][:]
        self.n_restarts = dic["n_restarts"]
        self.theta = dic["theta"][:]
        self.y = dic["y"][:]
        self.hyper_parameters = dic["hyper_parameters"][:]
        self.alpha = dic["alpha"][:]

        warnings.warn(
            "f, args and kwargs will need to be loaded for Emulator()",
            RuntimeWarning
        )

    def save(self, fname, extra={}):
        """Save the trained GP parameters to fname

        Parameters
        ----------
        fname : str
            path for savefile, asdf format
        extra : dict
            extra information to be saved
        """
        parameters = self._to_dict()
        # python 2 compatible
        parameters = parameters.copy()
        parameters.update(extra)
        with asdf.AsdfFile(parameters) as ff:
            ff.write_to(fname)

    def load(self, fname):
        with asdf.open(fname, copy_arrays=True) as af:
            self._from_dict(af)

    def _check_converged(self, *args, **kwargs):
        """Convergence check for the emulator"""
        raise NotImplementedError("overloaded by subclasses")

    def acquisition(self, *args, **kwargs):
        """Acquisition function for new emulator training points"""
        raise NotImplementedError("overloaded by subclasses")

    def train(self, *args, **kwargs):
        """Train the emulator"""
        raise NotImplementedError("overloaded by subclasses")


class Emulator(EmulatorBase):
    """
    Gaussian process emulator of y(theta) trained by sampling acquisition.

    Parameters
    ----------
    n_init : int
        number of points in the initial Latin hypercube (default: 10)
    f : callable f(theta)
        function to be emulated f(theta, *args, **kwargs) -> float
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    bounds : array
        lower and upper bounds for each dimension of the input theta to f
t    args : tuple, optional
        positional arguments for f
    kwargs : dict, optional
        keyword arguments for f
    hyper_bounds: array
        lower and upper bounds for each hyperparameter in the given kernel
    n_restarts : int
        number of random initialization positions for hyperparameters
        optimization (default: 25)
    """
    def __init__(
            self,
            n_init=10,
            f=None,
            kernel=None,
            bounds=None,
            args=(),
            kwargs={},
            hyper_bounds=None,
            n_restarts=5,
            pool=None,
            fname=None,
    ):
        super(Emulator, self).__init__(
            n_init=n_init,
            f=f,
            kernel=kernel,
            bounds=bounds,
            args=args,
            kwargs=kwargs,
            hyper_bounds=hyper_bounds,
            n_restarts=n_restarts,
            pool=pool,
            fname=fname,
        )
        # cannot be converged at initialization
        self.converged = False

    def _check_converged(self, var_tol=1e-3):
        """Check convergence of the process by requiring var_max < var_tol for
        the minimum variance of the GP when sampled multiple times"""
        def neg_var(theta):
            y, var = self.predict(theta, var=True)
            return -var

        parameters = []
        results = []

        # sample Latin hypercube to ensure coverage of parameter space
        p0s = ((pd.lhs(self._n_dim,
                       self.n_restarts,
                       criterion="maximin") - 0.5)
               * self.theta_range + self.theta_center)
        for p0 in p0s:
            # find optimal parameters
            result = op.minimize(neg_var, p0, method="L-BFGS-B",
                                 bounds=self.bounds)
            parameters.append(result.x)
            results.append(-neg_var(result.x))

        parameters = np.array(parameters)
        results = np.array(results)

        # set convergence status
        self.converged = np.max(results) < var_tol
        self.theta_max_var = parameters[np.argmax(results)]

    def acquisition(self, theta, a, b):
        """Acquisition function returns linear combination of function value
        and GP variance"""
        within_bounds = self._within_bounds(theta)
        if within_bounds.all():
            pred, pred_var = self.predict(theta, var=True)
            return np.squeeze(a * pred + b * pred_var)
        else:
            return -np.inf

    def train(
            self,
            n_steps=50,
            a=1,
            b=1,
            n_add=5,
            n_walkers=32,
            var_tol=1e-3,
            epsilon=0.05
    ):
        """Train the emulator by drawing points from the function sampled from
        the acquisition function. Training is stopped after n_steps or
        when converged.

        Parameters
        ----------
        n_steps : int
            number of steps to iterate
        a : float
            relative weight of func in acquisition
        b : float
            relative weight of variance in acquisition
        n_add : int
            number of points to add, better to keep this value low (< 10)
        n_walkers : int
            number of walkers to use to sample acquisition function
        var_tol : float
            maximum allowed variance of GP
        epsilon : float
            minimum fractional distance between new and previous theta
        """
        def acquire_theta(a, b, n_add, n_walkers):
            """Draw n_add samples from acquisition"""
            p0 = (np.ones((n_walkers, self._n_dim))
                  * self.theta_center.reshape(1, -1))
            p0 += ((np.random.rand(n_walkers, self._n_dim) - 0.5)
                   * self.theta_range)
            # set up the sampler for the acquisition function
            sampler = emcee.EnsembleSampler(
                n_walkers, self._n_dim,
                self.acquisition,
                args=(a, b),
                # # somehow, this starts using all the CPU available on the threads
                # # and is not faster than running serially... Must be some issue here.
                # pool=self.pool
            )

            # run the chain
            sampler.run_mcmc(p0, 600)
            # get the samples with burn-in removed
            samples = sampler.chain[:, 100:, :].reshape(-1, self._n_dim)

            # get random theta from the drawn samples
            indices = np.random.randint(0, samples.shape[0], n_add)

            close = np.zeros(len(samples[indices]), dtype=bool)
            theta_temp = self.theta * 1.
            for idx, theta in enumerate(samples[indices]):
                # for each coordinate compare the distance to the data points
                # to the minimum length scale of the domain
                # do not include points which are less than epsilon of that scale
                norms = np.linalg.norm(theta_temp - theta, axis=-1)
                scale = np.min(self.theta_range)
                too_close = (norms / scale < epsilon)
                close[idx] = too_close.any()

                # add new coordinate to comparison
                theta_temp = np.vstack([theta_temp, theta])

            return samples[indices][~close]

        self.a = a
        self.b = b
        # run the training
        for i in tqdm(range(n_steps), desc="Training", position=0):
            theta_new = acquire_theta(a=self.a, b=self.b, n_add=n_add,
                                      n_walkers=n_walkers)
            self.add(theta_new)

            # rescale a and b by the median of y and var to preserve relative
            # importance of both
            y_test, var_test = self.predict(self.theta_test, var=True)
            self.a = a / np.median(y_test)
            self.b = b / np.median(var_test)

            # only check convergence for every 50 added coordinates
            if self.theta.shape[0] % 50:
                continue

            # first optimize hyper parameters
            self._optimize_hyper_parameters()
            self._check_converged(var_tol=var_tol)
            if self.converged:
                print("Convergence reached")
                break

        # if stopped before convergence, warn the user
        # but also optimize hyper parameters to be sure
        if not self.converged:
            warnings.warn("Convergence criterion not reached, run some more steps...",
                          RuntimeWarning)
            self._optimize_hyper_parameters()
