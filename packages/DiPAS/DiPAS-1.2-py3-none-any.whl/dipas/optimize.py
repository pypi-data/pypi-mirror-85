from collections import deque, namedtuple

import torch
from torch.autograd.functional import jacobian

from .utils import numpy_compatible


class JacobianAdapter:
    """This class allows combination with external optimizers which require the Jacobian.
    
    Can be used together with ``scipy.optimize.least_squares`` for example.

    Parameters
    ----------
    f_compute : callable
        This function should compute the desired quantity, given a tensor of inputs.
        It will be called with a single argument, a tensor of shape ``(N,)`` and must output
        a single tensor of shape ``(M,)``.
    ref_data : torch.Tensor, shape (M,)
        The reference data to compute the residuals w.r.t. the output of `f_compute`.
        Must have the same shape as the output of `f_compute`.
    verbose : bool, optional
        If True then at every iteration the current mean squared error is printed to ``sys.stdout``.
    history : bool, optional
        If True then at every iteration the current estimate and residuals are saved in the `history` attribute.

    Attributes
    ----------
    step : int
        The current step during the optimization. This attribute is incremented by one
        for each ``__call__`` of the adapter.
    history : list
        If the `history` parameter is set to true then this list is appended the current parameter estimate and
        residuals as a tuple on every iteration.
    """

    Progress = namedtuple('Progress', 'estimate residual')
    
    def __init__(self, f_compute, *, ref_data, verbose=False, history=False):
        self.f_compute = f_compute
        self.ref_data = ref_data
        self._verbose = verbose
        self._save_history = history
        self.history = []
        self.step = 0
        self._jac_cache = deque(maxlen=1)
        self._res_cache = deque(maxlen=1)

    @numpy_compatible
    def __call__(self, estimate):
        """Compute the residuals and Jacobian for the given estimate.
        
        Parameters
        ----------
        estimate : torch.Tensor or np.ndarray, shape (N,)

        Returns
        -------
        residuals : torch.Tensor, shape (M,)
        """
        self.step += 1
        jac = jacobian(self._compute, estimate)
        self._jac_cache.append(jac)
        res = self._res_cache.pop().detach()
        if self._verbose:
            print(f'[{self.step:03d}] mse = {torch.mean(res**2):.3e}')
        if self._save_history:
            self.history.append(self.Progress(estimate, res))
        return res

    def jacobian(self, _):
        """Return the Jacobian corresponding to the last estimate."""
        return self._jac_cache.pop()
        
    def _compute(self, estimate):
        """Compute the residuals via ``self.f_compute`` and store in ``self._res_cache``."""
        res = self.f_compute(estimate) - self.ref_data
        self._res_cache.append(res)
        return res
