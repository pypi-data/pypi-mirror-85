"""This module contains utility functions to convert george.Kernel
objects to dictionaries with a mapping that preserves the composition
properties of the given Kernel.

"""
from george import kernels
from george import metrics
import numpy as np


# since metric parameters are the log of the given parameter, we need to
# pass the metric instead of the parameters to instantiate the kernel.
# Only works for kernels that take only a metric:
only_metric = [
    'ExpKernel',
    'ExpSquaredKernel',
    'Matern32Kernel',
    'Matern52Kernel'
]

# kernel operators are identified by integer values
operator_types = [kernels.Sum, kernels.Product]


def is_metric_type(kernel_name):
    """Check whether kernel_name requires only metric argument."""
    return kernel_name in only_metric


def metric_to_dict(metric):
    """Convert george.metrics.Metric object to dict for asdf serialization."""
    m_dict = {}
    m_dict["metric_type"] = metric.metric_type
    m_dict["ndim"] = metric.ndim
    m_dict["parameter_names"] = metric.parameter_names
    m_dict["parameter_bounds"] = metric.parameter_bounds
    m_dict["unfrozen_mask"] = metric.unfrozen_mask
    m_dict["parameter_vector"] = metric.parameter_vector
    m_dict["axes"] = metric.axes

    return m_dict


def dict_to_metric(m_dict):
    """
    Convert dict with metric keywords to george.metrics.Metric object
    for asdf serialization.
    """
    # instantiate dummy metric type
    m = metrics.Metric(1, ndim=m_dict["ndim"])

    # now set the metric parameters
    m.metric_type = m_dict["metric_type"]
    # need to create a view of the arrays so that they will be loaded from asdf
    m.parameter_names = m_dict["parameter_names"][:]
    m.unfrozen_mask = m_dict["unfrozen_mask"][:]
    m.parameter_vector = m_dict["parameter_vector"][:]
    m.parameter_bounds = m_dict["parameter_bounds"][:]
    m.axes = m_dict["axes"][:]
    return m


def kernel_to_dict(kernel):
    """
    Convert george.kernels.Kernel object to dict for asdf serialization.
    """
    if isinstance(kernel, kernels.Kernel):
        if kernel.kernel_type == -1:
            raise ValueError("need a basic Kernel object")
        else:
            k_dict = {
                "name": type(kernel).__name__,
                "parameters": (
                    kernel.get_parameter_vector()
                    if not is_metric_type(type(kernel).__name__)
                    else metric_to_dict(kernel.metric)
                ),
                "ndim": kernel.ndim
            }
        return k_dict

    if isinstance(kernel, dict):
        if (
                "name" in kernel.keys() and
                "parameters" in kernel.keys() and
                "ndim" in kernel.keys()
        ):
            return kernel
        raise ValueError("kernel_dict needs 'name', 'parameters' and 'ndim' keys")

    raise TypeError("kernel should be kernels.Kernel or dict")


def dict_to_kernel(k_dict):
    """
    Convert dict with kernel parameters to george.kernels.Kernel object,
    hands back the same object if it already is a Kernel, necessary for
    map_to_kernel recursion. Used in asdf serialization.
    """
    if isinstance(k_dict, dict):
        if (
                "name" in k_dict.keys() and
                "parameters" in k_dict.keys() and
                "ndim" in k_dict.keys()
        ):
            # get kernel type from class name
            k = getattr(kernels, k_dict["name"])(
                k_dict["parameters"]
                if not is_metric_type(k_dict["name"])
                else dict_to_metric(k_dict["parameters"]),
                ndim=k_dict["ndim"]
            )
            return k
        else:
            raise ValueError("kernel_dict needs 'name', 'parameters' and 'ndim' keys")

    elif isinstance(k_dict, kernels.Kernel):
        return k_dict
    else:
        raise TypeError("kernel should be kernels.Kernel or dict")


def kernel_to_map(kernel):
    """
    Extract map of all constituent kernels as dictionaries with their
    operations.

    Parameters
    ----------
    kernel : george.kernels.Kernel object
        possible sum and product of kernels

    Returns
    -------
    kernel_map : list
        list of building blocks [operation, kernel1, kernel2]
        where kernel1 or kernel2 is either a dict or another
        building block.
    """
    # kernel is still composed of multiple kernels
    if kernel.kernel_type == -1:
        operator = operator_types[kernel.operator_type].__name__
        kernel_1 = kernel.models["k1"]
        kernel_2 = kernel.models["k2"]
        return [operator, kernel_to_map(kernel_1), kernel_to_map(kernel_2)]

    # kernel is a single building block -> convert to dict
    else:
        return kernel_to_dict(kernel)


def map_to_kernel(kernel_map):
    """
    Convert a kernel_map to the george.kernels.Kernel object
    with correct operations order.

    Parameters
    ----------
    kernel_map : list
        list of building blocks [operation, kernel1, kernel2]
        where kernel1 or kernel2 is either a dict or another
        building block.

    Returns
    -------
    kernel : george.kernels.Kernel object
        kernel resulting from all the correct operations on kernel_map
    """
    # whichever of the two kernels is not reduced, needs to be reduced
    if isinstance(kernel_map[1], list):
        kernel_map[1] = map_to_kernel(kernel_map[1])
    elif isinstance(kernel_map[2], list):
        kernel_map[2] = map_to_kernel(kernel_map[2])
    # if both kernels are reduced, we can add them and send them up the stack
    else:
        k1 = dict_to_kernel(kernel_map[1])
        k2 = dict_to_kernel(kernel_map[2])
        return getattr(kernels, kernel_map[0])(k1, k2)

    # now we need to add up the final objects
    k1 = dict_to_kernel(kernel_map[1])
    k2 = dict_to_kernel(kernel_map[2])
    return getattr(kernels, kernel_map[0])(k1, k2)


def arrays_to_theta(*xi):
    '''
    Convert a set of N 1-D coordinate arrays to a regular coordinate grid of
    dimension (npoints, N) for the interpolator
    '''
    # the meshgrid matches each of the *xi to all the other *xj
    Xi = np.meshgrid(*xi, indexing='ij')

    # now we create a column vector of all the coordinates
    theta = np.concatenate([X.reshape(X.shape + (1,)) for X in Xi], axis=-1)

    return theta.reshape(-1, len(xi))
