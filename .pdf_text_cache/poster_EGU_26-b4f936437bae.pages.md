# Extracted PDF Text: poster_EGU_26.pdf

Source: `/home/adrian/PhD/Adrian-Mag.github.io/media/research/posters/poster_EGU_26.pdf`

Backend: `pypdf`

SHA256: `b4f936437bae7f68b5a91cfe63f719675451cfa2cf5932ca40bc234af7da9cea`



---

## Page 1

Formulate First Your Prior
Is Not Just a Matrix
Naive Diagonals
Boundary Conditions
The Elements
Example Problem Setup
Discretization Diagram
Inverse problems should be posed first in function space.
Discretization should approximate the problem, not redefine it.
Fig. 1: Toy inverse problem setup: the true model, the sensitivity kernels of the forward operator, and the corresponding
noisy observations
Fig. 3: Naive discretization becomes increasingly unstable with refinement (variance grows from N=10 to N=50),
whereas the correctly discretized Bessel posterior converges toward the continuous solution with controlled uncertainty.
Fig. 5: Geometry-aware vs naive discretized Bayesian posterior.
pygeoinf: python package for
geophysical inversions and inferences
built on function analytical principles
with discretization agnostic
implementation
Personal website intervalinf: modular extension of
pygeoinf for function spaces defined
over a 1D interval
Fig. 4: Continuous Bessel priors under two boundary conditions: posterior-consistent sample realizations are shown for
Neumann (top) and Dirichlet–Neumann (bottom), with the black curve indicating the zero mean profile across depth.
Table: Summary of symbols
Fig. 2: Diagram showing the replacement of the
original problem defined on     with a discretizatsed
problem in      .
• Starting with a basis is convenient, but it can hide modelling
assumptions.
• Instead we should start by defining the model space 𝓜, data space
𝓓, forward map G, and a description of uncertainty and prior
information (1,2) - not by discretization.
• Covariances in function spaces are operators and may require
boundary conditions (3), which are part of the prior information.
• Discretization must respect this structure.
Not every matrix defines a valid covariance operator in the continuous
limit (3). For example, a scaled identity is not a good choice for a prior
covariance!(3,4) As numerical resolution increases:
• Naive diagonals (σ²I) → diverging variance
• Proper covariances → finite variance
This leads to unstable vs stable posteriors.
Therefore, it is crucial a covariance must come from a valid operator.
Non-orthonormal bases induce a geometry on the discretized model
space. The inner product on the discretized model must be weighted
by the gram matrix of the basis. Adjoints must be defined with respect
to this geometry (5). Ignoring it changes the problem and the
solution.
We thank Sam Scivier and Christophe Zaroli for helpful discussions. PK acknowledges funding from the Royal Society
through a University Research Fellowship (URF\R1\180377 and URF\R\241025). MM acknowledges the funding received
from the UKRI NERC DTP NE/S007474/1.
1 Mag, A.M., Zaroli, C. and Koelemeijer, P., 2025. Bridging the gap between SOLA and deterministic linear inferences in
the context of seismic tomography. Geophysical Journal International, 242(1), p.ggaf131.
2 Al-Attar, D., 2021. Linear inference problems with deterministic constraints. arXiv preprint arXiv:2104.12256
3 Stuart, A.M., 2010. Inverse problems: a Bayesian perspective. Acta numerica, 19, pp.451-559.
4 Valentine, A.P. and Sambridge, M., 2020. Gaussian process models—I. A framework for probabilistic continuous
inverse theory. Geophysical Journal International, 220(3), pp.1632-1647.
5 Bui-Thanh, T., Ghattas, O., Martin, J. and Stadler, G., 2013. A computational framework for infinite-dimensional
Bayesian inverse problems Part I: The linearized case, with application to global seismic inversion. SIAM Journal on
Scientific Computing, 35(6), pp.A2494-A2523.
• Discretization can hide modelling choices.
• Formulate the problem before discretizing it
• Sound workflows make these choices explicit
• These ideas are implemented in the pygeoinf package (scan QR).
We infer a model from indirect, noisy observations.
• We assume the model space to be a function space.
• We place a Gaussian prior on the model space
• We assume Gaussian noise    ~
• We solve for the posterior using Bayesian inversion, which has
the closed form solution (3):
Consistent Geometry
Conclusions
Acknowledgements
Think First, Discretize Later
A.M. Mag¹, D. Al-Attar², P. Koelemeijer¹
¹ University of Oxford, ² University of Cambridge
