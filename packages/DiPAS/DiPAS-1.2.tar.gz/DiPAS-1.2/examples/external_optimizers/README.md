# Using external optimizers

The PyTorch package ships already with a [number of optimizers](https://pytorch.org/docs/stable/optim.html). These however are typically suited for problems with large parameter spaces (several hundred or more). For smaller problems other optimizers, e.g. the [Levenberg-Marquardt algorithm](https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm), are more efficient. The Scipy package offers various other optimizers at their [`scipy.optimize.least_squares`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) function. This notebook shows how to use such external optimizers together with the DiPAS framework.

In PyTorch the job of the optimizer is to update the parameters of the simulation, given their gradients with respect to some cost function. That is it performs the following steps:

1. Compute the new parameter values (based on the current values and gradients),
2. Apply these new values, i.e. make the changes effective.

We use the external optimizer to perform step (1) and then we apply the changes manually (which is easy).
