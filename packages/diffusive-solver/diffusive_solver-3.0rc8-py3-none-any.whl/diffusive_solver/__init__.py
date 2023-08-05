#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Coupled diffusion equation solver
Solves a system of coupled diffusion equations in two spatial dimensions for 
the fields $\phi_\alpha(\bm r)$ in the form

$-\sum_{ij\,\beta}
\partial_i[L_{\alpha\beta\,ij}(\bm r)\partial_j\phi_\beta(\bm r)]
+\sum_{\beta}\Gamma_{\alpha\beta}(\bm r)\phi_\beta(\bm r)
=F_{\alpha}(\bm r)$.

In the above equations greek indices identify different fields and latin 
indices spatial components.
The equations are solved in a domain $\Omega$ with Dirichlet boundary 
conditions on selected regions of the boundary dubbed contacts $C_1$, $C_2$,...

$\phi_\alpha(\bm r) - V^{(\alpha\, n)} = R_{\rm c}^{(\alpha, n)}J_{\alpha\, i}(\bm r) \hat{n}_i(\bm r)$ 

if $\bm r \in C_n$, and homogeneous Neumann boundary conditions on the remaining 
part of the boundary 

$J_{\alpha\, i}(\bm r) \hat{n}_i(\bm r) = 0 $ if 
$\bm r \in \partial\Omega - \cup C_n$.

Here the currents $J_{\alpha\, i}$ are defined by

$J_{\alpha\, i}(\bm r)\equiv -\sum_{j\, \beta}
L_{\alpha\beta\,ij}(\bm r)\partial_j\phi_\beta(\bm r)$,

and R_{\rm c}^{(\alpha, n)} are generalized contact resistances.

The currents respect the continuity equations including a relaxation term ($\Gamma$) and 
source term ($F$)

$\sum_i \partial_iJ_{\alpha\, i}(\bm r)=
-\sum_\beta\Gamma_{\alpha\beta}(\bm r)\phi_\beta(\bm r)+F_{\alpha}(\bm r)$.

The flux of the current $J_{\alpha\, i}$ at the contact m is defined by 

$I^{(\alpha\,m)}\equiv \int_{C_m} \hat{n}_i(\bm r) J_{\alpha\, i}(\bm r)ds$

and is related to the applied biases $V^{(\beta\, n)$ ($\beta$ component of the 
field at the contact n) by the response matrices

$I^{(\alpha\,m)} =G^{(\alpha\,m,\beta\,n)}V^{(\beta\, n)} + S^{(\alpha\,m)}[F]$

where G does not depend on F and S is a linear function of F.

This module allows to solve for the solution for an arbitrary configuration of 
biases and to extract the matrices $G$ and $S$.
'''
__version__ = '3.0rc8'
__author__ = 'Iacopo Torre'
from . diffusive_solver import *