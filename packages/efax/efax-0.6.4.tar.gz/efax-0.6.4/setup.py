# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['efax', 'efax.scipy_replacement']

package_data = \
{'': ['*']}

install_requires = \
['chex>=0.0.2,<0.0.3',
 'ipromise>=1.5,<2.0',
 'jax>=0.2,<0.3',
 'jaxlib>=0.1.55,<0.2.0',
 'numpy>=1.18,<2.0',
 'scipy>=1.4,<2.0',
 'tjax>=0.6,<1.0']

setup_kwargs = {
    'name': 'efax',
    'version': '0.6.4',
    'description': 'Exponential families for JAX',
    'long_description': '=================================\nEFAX: Exponential Families in JAX\n=================================\n.. image:: https://badge.fury.io/py/efax.svg\n    :target: https://badge.fury.io/py/efax\n\n.. role:: bash(code)\n    :language: bash\n\n.. role:: python(code)\n   :language: python\n\nThis library provides a set of tools for working with *exponential family distributions* in the differential programming library `JAX <https://github.com/google/jax/>`_.\nThe *exponential families* are an important class of probability distributions that include the normal, gamma, beta, exponential, Poisson, binomial, and Bernoulli distributions.\nFor an explaination of the fundamental ideas behind this library, see our `overview on exponential families <https://github.com/NeilGirdhar/efax/blob/master/expfam.pdf>`_.\n\nUsage\n=====\nIn SciPy, a distribution is represented by a single object, so a thousand distributions need a thousand objects.  Each object encodes the distribution family, and the parameters of the distribution.\nEFAX has a different representation.  Each :python:`ExponentialFamily` object encodes only the distribution family for many (say, one thousand) distributions.  The parameters of the distributions are passed in to various methods on the object to evaluate various things.  For example,\n\n.. code:: python\n\n    from jax import numpy as jnp\n\n    from efax import Bernoulli\n\n    b = Bernoulli(shape=(3,))\n\n    # p are expectation parameters of Bernoulli distributions having probabilities\n    # 0.4, 0.5, and 0.6.\n    p = jnp.array([[0.4], [0.5], [0.6]])\n\n    # q are natural parameters of Bernoulli distributions having log-odds 0, which\n    # is probability 0.5.\n    q = jnp.zeros((3, 1))\n\n    print(b.cross_entropy(p, q))\n    # [0.6931472 0.6931472 0.6931472]\n\n    # q are natural parameters of Bernoulli distributions having a probability\n    # of 0.3.\n    q = b.exp_to_nat(0.3 * jnp.ones((3, 1)))\n\n    print(b.cross_entropy(p, q))\n    # [0.6955941  0.78032386 0.86505365]\n    # A Bernoulli distribution with probability 0.3 predicts a Bernoulli\n    # observation with probability 0.4 better than the other observations.\n\nWith exponential families, maximum likelihood estimation is just expectation over expectation parameters.  Models that combine independent predictors just sum natural parameters.  When we want to optimize such models, we just want to take the gradient of cross entropy with respect to predictions.\n\nThanks to JAX, any gradient of the cross entropy will automatically be as accurate and numerically stable as possible.  This is because the gradient of the cross entropy involves the gradient of the log-normalizer, which typically has a very nice form.  For example,\n\n.. code:: python\n\n    from jax import grad, jit, lax\n    from jax import numpy as jnp\n\n    from efax import Bernoulli\n\n    b = Bernoulli(shape=())\n\n\n    def cross_entropy_loss(p, q):\n        return b.cross_entropy(p, q)\n\n\n    gce = jit(grad(cross_entropy_loss, 1))\n\n\n    def body_fun(q):\n        return q - gce(some_p, q) * 1e-4\n\n\n    def cond_fun(q):\n        return jnp.sum(gce(some_p, q) ** 2) > 1e-7\n\n\n    # some_p are expectation parameters of a Bernoulli distribution corresponding\n    # to probability 0.4.\n    some_p = jnp.array([0.4])\n\n    # some_q are natural parameters of a Bernoulli distribution corresponding to\n    # log-odds 0, which is probability 0.5.\n    some_q = jnp.array([0.0])\n\n    # Optimize the predictive distribution iteratively.\n    print(lax.while_loop(cond_fun, body_fun, some_q))\n    # Outputs the natural parameters that correspond to 0.4.\n\n    # Compare with the true value.\n    print(b.exp_to_nat(some_p))\n\nContribution guidelines\n=======================\n\n- Conventions: PEP8.\n\n- How to run tests: :bash:`pytest .`\n\n- How to clean the source:\n\n  - :bash:`isort .`\n  - :bash:`pylint efax`\n  - :bash:`flake8 efax`\n  - :bash:`mypy efax`\n',
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NeilGirdhar/efax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
