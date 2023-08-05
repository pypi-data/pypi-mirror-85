#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Solves a system of coupled diffusion equations'''
########### Import modules ####################################################
import os
import numpy as np
import matplotlib.pyplot as plt
from warnings import warn
import mshr
from .fenics_cookbook import *
dol.LogLevel(30)
########### Class for sample geometry #########################################
class Geometry():
    """Class that holds all the geometrical information of the domain
    -------
    Attributes
    -------
    mesh
    n_contacts
    contacts_marker
    subdomain_marker
    dx
    ds
    dS
    -------
    Properties 
    -------
    coordinates
    cells
    cells_centers
    -------
    Methods
    -------
    __init__
    plot
    plot_subdomains
    check_dimensions
    -------
    Constructors
    -------
    from_points
    from_txt_file
    from_msh_file
    """    
    def __init__(self, mesh, contacts_marker, n_contacts, subdomain_marker = None):
        """Initialize an instance of the class

        Parameters
        ----------
        mesh : dolfin Mesh object
            Mesh for the geometry
        contacts_marker : dolfin MeshFunctionSizet
            Facet function that marks the contacts ranging from 1 to n_contacts
        n_contacts : int 
            Number of contacts
        subdomain_marker : dolfin MeshFunctionSizet, optional
            Marker for subdomains of the sample, by default None
        """        
        assert isinstance(mesh, dol.cpp.mesh.Mesh)
        self.mesh = mesh
        assert isinstance(contacts_marker, dol.cpp.mesh.MeshFunctionSizet)
        self.contacts_marker = contacts_marker
        assert isinstance(n_contacts, (int, np.integer))
        self.n_contacts = n_contacts
        if not (subdomain_marker is None):
            assert isinstance(contacts_marker, dol.cpp.mesh.MeshFunctionSizet)
        self.subdomain_marker = subdomain_marker
        if not (subdomain_marker is None):
            self.dx = dol.Measure('dx', domain = mesh, subdomain_data = subdomain_marker)
        else:
            self.dx = dol.Measure('dx', domain = mesh)
        self.ds = dol.Measure('ds', domain = mesh, subdomain_data = contacts_marker)
        self.dS = dol.Measure('dS', domain = mesh, subdomain_data = contacts_marker)

    #constructors
    @classmethod
    def from_points(cls, points_coords, contacts_positions, resolution = 20):
        """Construct a polygonal geometry given a list of points and contact positions

        Parameters
        ----------
        points_coords : 2D numpy array
            array containing the coordinates of the vertices of the polygon
        contacts_positions : list 
            each list element represents a contact as a (ordered) list of indices of points pertaining to it
        resolution : int, optional
            resolution to be used by mshr. Higher means finer resolution, by default 20

        Returns
        -------
        Geometry
            instance of the class
        """        
        points_coords = np.array(points_coords)
        points_list = []
        for i in range(points_coords.shape[0]):
            points_list.append(dol.Point(points_coords[i,0], points_coords[i,1]))
        sample = mshr.Polygon(points_list)
        mesh = mshr.generate_mesh(sample, resolution)
        n_contacts = len(contacts_positions)
        contacts = []
        for i in range(n_contacts):
            line = []
            for index in contacts_positions[i]:
                line.append(points_coords[index,:])
            contacts.append(Boundary_Close_To_Line(line))
        contacts_marker = dol.MeshFunction('size_t', 
                                           mesh,
                                           mesh.topology().dim() - 1)
        for i, contact in enumerate(contacts):
            contact.mark(contacts_marker, i + 1)
        return cls(mesh = mesh, 
                   contacts_marker = contacts_marker,
                   n_contacts = n_contacts)

    @classmethod
    def from_txt_file(cls, filename, resolution = 20):
        """Construct a polygonal geometry from a txt file.
        The file format must be as follows: points defining the polygon should be ordered
        points belonging to a contact should be marked by integers from 1 to Nc 
        and must be contiguous, points not belonging to a contact should be marked 
        by nan. Use # for comments. 
        Example of input file.
        #X[um]	Y[um]	contact
        -3.     1.      1
        -3.     0.      1
        3.      0.      2
        3.      1.      2

        Parameters
        ----------
        filename : str
            Name of the .txt file to read
        resolution : int, optional
            resolution to be used by mshr. Higher means finer resolution, by default 20

        Returns
        -------
        Geometry
            instance of the class
        """        
        points_coords = np.loadtxt(filename, usecols = (0,1))
        contacts_positions = []
        contacts_column = np.loadtxt(filename, usecols = (2,))
        n_contacts = int(np.nanmax(contacts_column))
        for i in range(n_contacts):
            contacts_positions.append((np.nonzero(contacts_column == i+1)[0]).tolist())
        return cls.from_points(points_coords = points_coords, 
                               contacts_positions = contacts_positions, 
                               resolution = resolution)

    @classmethod
    def from_msh_file(cls, filename, n_contacts, dim = 2, dim_keep = None):
        """Construct a geometry given a .msh file 

        Parameters
        ----------
        filename : str
            Name of the .msh file to read
        n_contacts : int
            Number of contacts in the geometry. 
            Contacts must be marked with numbers from 1 to n_contacts.
        dim : int, optional
            Topological dimension of the mesh, by default 2
        dim_keep : int, optional
            Spatial dimension of the mesh if the mesh is embedded in an higher dimensional space,
            by default None (i.e. same as dim). 
            1D geometries need dim_keep >=2.

        Returns
        -------
        Geometry
            instance of the class
        """        
        if dim_keep is None:
            dim_keep = dim
        convert_msh_to_XDMF(filename, dim = dim, dim_keep = dim_keep)
        mesh_dic = load_XDMF_files(filename, dim = dim)
        return cls(mesh = mesh_dic['mesh'], 
                   contacts_marker = mesh_dic['boundary_marker'], 
                   n_contacts = n_contacts, 
                   subdomain_marker = mesh_dic['volume_marker'])
    
    #properties
    @property
    def coordinates(self):
        return self.mesh.coordinates()
    @property
    def cells(self):
        return self.mesh.cells()
    @property
    def cells_centers(self):
        return np.array([(cell.midpoint().x(), cell.midpoint().y()) for cell in dol.cells(self.mesh)])
    
    #methods
    def plot(self, **kwargs):
        """Plot the mesh and the contacts 

        Returns
        -------
        p1, p2
            p1 is the contact marker, p2 the mesh as returned by matplotlib
        **kwargs : kwargs to be passed to plt.scatter
        """               
        plt.axis('equal')
        p2 = plot_mesh(self.mesh)
        p1 = plot_facet_function(facet_function = self.contacts_marker, 
                            markers = np.arange(1, self.n_contacts + 1, dtype = int),
                            **kwargs)
        return p1, p2

    def plot_subdomains(self, show_mesh = True, **kwargs):
        """Plot mesh and subdomains

        Parameters
        ----------
        show_mesh : bool, optional
            whether to plot the mesh, by default True
        **kwargs : kwargs to be passed to plt.tripcolor
        Returns
        -------
        p1, p2
            p1 is the subdomain marker, p2 the mesh as returned by matplotlib
        """        
        ''''''
        plt.axis('equal')
        if show_mesh:
            p2 = plot_mesh(self.mesh)
        else:
            p2 = None
        if not self.subdomain_marker is None:
            p1 = plot_cell_function(cell_function = self.subdomain_marker, **kwargs)
        else:
            warn('no subdomains')
            p1 = None
        return p1, p2

    
    def check_dimensions(self):       
        """Print total D-dimensional volume and areas of the contacts (area and lenghts in 2D)
        """        
        total_volume = dol.assemble(dol.Constant(1) * self.dx)
        total_area = dol.assemble(dol.Constant(1) * self.ds)
        print('Total volume = {}'.format(total_volume))
        print('Total area = {}'.format(total_area))
        if not(self.subdomain_marker is None):
            for i in np.unique(self.subdomain_marker.array()):
                volume = dol.assemble(1 * self.dx(i))
                print('Subdomain {} with volume = {}'.format(i, volume))
        for i in range(self.n_contacts):
            area = dol.assemble(1 * self.ds(i+1))
            print('Contact {} with area = {}'.format(i+1,area))
###############################################################################
class Problem():
    """Class that stores, solves and analyze a problem
    -------
    Properties 
    -------
    geometry
    n_fields
    self_adjoint
    L
    Gamma
    contact_resistances
    biases
    F
    fields
    fields_vertices
    currents
    currents_cells
    responsivities
    responsivities_vertices
    fluxes
    solution_basis
    adjoint_solution_basis
    solution_inhomogeneous
    response_matrix
    source_vector
    function_space
    scalar_function_space
    vector_function_space
    -------
    Methods
    -------
    __init__
    solve
    plot
    save
    compute_currents
    compute_fluxes
    compute_response_matrix
    compute_responsivities
    compute_source_vector
    compute_solution_basis
    compute_adjoint_solution_basis
    compute_solution_inhomogeneous
    """    

    def __init__(self, geometry, n_fields = 1, self_adjoint = False,
                 L = None, Gamma = None, contact_resistances = None,
                 biases = None, F = None):
        """Initialize a problem

        Parameters
        ----------
        geometry : Geometry
            geometry in which the problem must be solved
        n_fields : int, optional
            number of fields in the problem, by default 1
        self_adjoint : boolean, optional
            wheter the problem is self-adjoint, i.e. L = L^T and Gamma = Gamma^T.
            by default is False.
        L : list of lists, optional
            Linear response matrix, by default None i.e. identity matrix
        Gamma : list of lists, optional
            Decay matrix, by default None i.e. null matrix
        contact_resistances : [n_fields, n_contacts] array, optional
            contact resistances values, by default None i.e. all zeros
        biases : [n_fields, n_contacts] array, optional
            Values of the biases at contacts, by default None i.e all zeros
        F : list, optional
            Source term, by default None i.e. zero
        """        
        #checks
        assert isinstance(geometry, Geometry)
        self._geometry = geometry
        assert isinstance(n_fields, (int, np.integer)) and n_fields > 0
        self._n_fields = n_fields
        #default values
        if L is None:
            L = [[Matrix_Expression(float(alpha == beta), dimension = 1,scalar = True) for alpha in range(n_fields)] for beta in range(n_fields)]
        if Gamma is None:
            Gamma = [[Matrix_Expression(0, dimension = 1,scalar = True) for alpha in range(n_fields)] for beta in range(n_fields)]
        if contact_resistances is None:
            contact_resistances = np.zeros([n_fields, geometry.n_contacts])
        if biases is None:
            biases = np.zeros([n_fields, geometry.n_contacts])
        if F is None:
            F = [dol.Constant(0) for alpha in range(n_fields)]
        #checks
        if (len(L) != n_fields or len(Gamma) != n_fields or len(F) != n_fields): 
            raise ValueError('Non matching matrices')
        if any([len(Lrow) != n_fields for Lrow in L]): 
            raise ValueError('Non square L matrix')
        if any([len(Gammarow) != n_fields for Gammarow in Gamma]): 
            raise ValueError('Non square Gamma matrix')
        contact_resistances = np.atleast_2d(contact_resistances)
        if contact_resistances.shape != (n_fields, geometry.n_contacts):
            raise ValueError('Wrong dimension of contact resistances matrix')
        biases = np.atleast_2d(biases)
        if biases.shape != (n_fields, geometry.n_contacts):
            raise ValueError('Wrong dimension of bias matrix')
        #store values
        self._L = L
        self._Gamma = Gamma
        self._self_adjoint = self_adjoint
        self._L_T = self._transpose(L)
        self._Gamma_T = self._transpose(Gamma)
        self._contact_resistances = contact_resistances
        self._biases = biases
        self._F = F
        #initialize properties
        self._fields = None
        self._currents = None
        self._fluxes = None
        self._solution_basis = None
        self._responsivities = None
        self._responsivity_vertices = None
        self._adjoint_solution_basis = None
        self._response_matrix = None
        self._solution_inhomogeneous = None
        self._source_vector = None
        #functionspaces
        element = dol.MixedElement([dol.FiniteElement('P', self.geometry.mesh.ufl_cell(), degree = 1) for alpha in range(self.n_fields)])
        self.function_space = dol.FunctionSpace(self.geometry.mesh, element)
        self.scalar_function_space = dol.FunctionSpace(self.geometry.mesh, dol.FiniteElement('P', self.geometry.mesh.ufl_cell(), degree = 1))
        self.vector_function_space = dol.VectorFunctionSpace(self.geometry.mesh, 'DP', degree = 0)
    #properties
    @property
    def geometry(self):
        return self._geometry
    @geometry.setter
    def geometry(self, _):
        warn('read only property')

    @property
    def self_adjoint(self):
        return self._self_adjoint
    @self_adjoint.setter
    def self_adjoint(self, _):
        warn('read only property')
    
    @property
    def n_fields(self):
        return self._n_fields
    @n_fields.setter
    def n_fields(self, _):
        warn('read only property')

    @property
    def L(self):
        return self._L
    @L.setter
    def L(self, _):
        warn('read only property')

    @property
    def Gamma(self):
        return self._Gamma
    @Gamma.setter
    def Gamma(self, _):
        warn('read only property')

    @property
    def contact_resistances(self):
        return self._contact_resistances
    @contact_resistances.setter
    def contact_resistances(self, _):
        warn('read only property')

    @property
    def biases(self):
        return self._biases
    @biases.setter
    def biases(self, _):
        warn('Source terms (F and biases) can be changed only using solve(F = new_F, biases = new_biases)')

    @property
    def F(self):
        return self._F
    @F.setter
    def F(self, _):
        warn('Source terms (F and biases) can be changed only using solve(F = new_F, biases = new_biases)')

    @property
    def fields(self):
        if self._fields is None:
            self.solve()
        return self._fields
    @fields.setter
    def fields(self,_):
        warn('read only property')

    @property
    def fields_vertices(self):
        if self._fields is None:
            self.solve()
        return np.array([field.compute_vertex_values(self.geometry.mesh) for field in self._fields])
    @fields_vertices.setter
    def fields_vertices(self,_):
        warn('read only property')

    @property
    def responsivities_vertices(self):
        if self._responsivity_vertices is None:
            _responsivity_vertices = np.zeros([self.n_fields, self.geometry.n_contacts, self.n_fields,self.geometry.coordinates.shape[0]])
            for alpha in range(self.n_fields):
                for m in range(self.geometry.n_contacts):
                    for beta in range(self.n_fields):
                        _responsivity_vertices[alpha, m,beta,:] = self.responsivities[alpha][m][beta].compute_vertex_values()
            self._responsivity_vertices = _responsivity_vertices
        return self._responsivity_vertices
    @responsivities_vertices.setter
    def responsivities_vertices(self,_):

        warn('read only property')

    @property
    def currents(self):
        if self._currents is None:
            self.compute_currents()
        return self._currents
    @currents.setter
    def currents(self,_):
        warn('read only property')

    @property
    def currents_cells(self):
        if self._currents is None:
            self.compute_currents()
        current_cells = []
        for alpha in range(self.n_fields):
            current_cells.append([self._currents[alpha].vector().get_local() [self.vector_function_space.dofmap().cell_dofs(cell.index())] for cell in dol.cells(self.geometry.mesh)])
        return np.array(current_cells)
    @currents_cells.setter
    def currents_cells(self,_):
        warn('read only property')

    @property
    def fluxes(self):
        if self._fluxes is None:
            self.compute_fluxes()
        return self._fluxes
    @fluxes.setter
    def fluxes(self,_):
        warn('read only property')

    @property
    def solution_basis(self):
        if self._solution_basis is None:
            self.compute_solution_basis()
        return self._solution_basis
    @solution_basis.setter
    def solution_basis(self,_):
        warn('read only property')

    @property
    def adjoint_solution_basis(self):
        if self._adjoint_solution_basis is None:
            self.compute_adjoint_solution_basis()
        return self._adjoint_solution_basis
    @adjoint_solution_basis.setter
    def adjoint_solution_basis(self,_):
        warn('read only property')

    @property
    def responsivities(self):
        if self._adjoint_solution_basis is None:
            self.compute_responsivities()
        return self._responsivities
    @responsivities.setter
    def responsivities(self,_):
        warn('read only property')

    @property
    def response_matrix(self):
        if self._response_matrix is None:
            self.compute_response_matrix()
        return self._response_matrix
    @response_matrix.setter
    def response_matrix(self,_):
        warn('read only property')

    @property
    def solution_inhomogeneous(self):
        if self._solution_inhomogeneous is None:
            self.compute_solution_inhomogeneous()
        return self._solution_inhomogeneous
    @solution_inhomogeneous.setter
    def solution_inhomogeneous(self,_):
        warn('read only property')

    @property
    def source_vector(self):
        if self._source_vector is None:
            self.compute_source_vector()
        return self._source_vector
    @source_vector.setter
    def source_vector(self,_):
        warn('read only property')

    #internal methods
    def _transpose(self, matrix):
        'Transpose a matrix on both cartesian and field indices'
        assert len(matrix) == self._n_fields
        assert all([len(matrix[i]) == self._n_fields for i in range(self._n_fields)])
        matrix_T = []
        for i in range(self._n_fields):
            matrix_T.append([matrix[j][i].transposed() for j in range(self._n_fields)])
        return matrix_T
    
    def _solve(self, L, Gamma, contact_resistances, biases, F):
        '''Internal solving function. Does not update properties'''
        #trial and test functions
        u = dol.TrialFunction(self.function_space) 
        v = dol.TestFunction(self.function_space)    
        # quadratic form
        quadratic_terms = []
        for alpha in range(self.n_fields):
            for beta in range(self.n_fields):
                term1 = (dol.inner(dol.grad(v[alpha]), L[alpha][beta] * dol.grad(u[beta])) * self.geometry.dx)
                term2 = (v[alpha] * Gamma[alpha][beta] * u[beta] * self.geometry.dx)
                quadratic_terms.append(term1 + term2)
        
        for alpha in range(self.n_fields):
            for n in range(self.geometry.n_contacts):
                if contact_resistances[alpha, n] != 0.:
                    term3 = dol.Constant(1./contact_resistances[alpha, n]) * v[alpha] * u[alpha] * self.geometry.ds(n+1) ####!careful n+1 !!
                    quadratic_terms.append(term3)
        a = sum(quadratic_terms)
        # linear form
        linear_terms = []
        for alpha in range(self.n_fields):
            term1 = v[alpha] * F[alpha] * self.geometry.dx
            linear_terms.append(term1)
        for alpha in range(self.n_fields):
            for n in range(self.geometry.n_contacts):
                if contact_resistances[alpha, n] != 0.:
                    term2 = dol.Constant(biases[alpha, n]/contact_resistances[alpha, n]) * v[alpha] * self.geometry.ds(n+1)
                    linear_terms.append(term2)
        b = sum(linear_terms) 
        # boundary conditions 
        bc = [] 
        if self.n_fields > 1:
            for n in range(self.geometry.n_contacts):
                for beta in range(self.n_fields):
                    if contact_resistances[beta, n] == 0.:
                        bc.append(dol.DirichletBC(self.function_space.sub(beta), 
                                                dol.Constant(biases[beta, n]), 
                                                self.geometry.contacts_marker,
                                                n+1))
        else:
            for n in range(self.geometry.n_contacts):
                if contact_resistances[0, n] == 0.:
                    bc.append(dol.DirichletBC(self.function_space, 
                                              dol.Constant([biases[0, n]]), 
                                              self.geometry.contacts_marker,
                                                n+1))
        #solve linear system
        phi = dol.Function(self.function_space) #clear phi
        dol.solve(a == b, phi, bc)
        return phi
    #methods
    def solve(self, biases = None, F = None):
        """Solves the stored problem

        Parameters
        ----------
        biases : [n_fields, n_contacts], optional
            bias values, by default None, i.e. use the stored values
        F : list, optional
            Source term, by default None, i.e. use the stored value
        """        
        if (not biases is None):
            self.biases = biases
        if (not F is None):
            self._solution_inhomogeneous = None
            self._source_vector = None
            self.F = F
        phi = self._solve(L = self.L, Gamma = self.Gamma, contact_resistances = self.contact_resistances, biases = self.biases, F = self.F)
        if self.n_fields > 1:
            self._fields = phi.split()
        else:
            self._fields = [phi]
        self._currents = None
        self._currents_cells = None
        self._fluxes = None
        self._solution_inhomogeneous = None
        self._source_vector = None

    def compute_currents(self):
        """Compute currents
        """        
        if self._fields is None:
            self.solve()
        
        if self.n_fields > 1.:
            self._currents = [dol.project(- sum([self.L[alpha][beta] * dol.grad(self._fields[beta]) for beta in range(self.n_fields)]), self.vector_function_space) for alpha in range(self.n_fields)]
        else:
            self._currents = [dol.project(- self.L[0][0] * dol.grad(self._fields[0][0]) , self.vector_function_space)]

    def compute_fluxes(self):
        """Compute fluxes 
        """        
        if self._currents is None:
            self.compute_currents()
        I = np.zeros([self.n_fields, self.geometry.n_contacts])
        normal = dol.FacetNormal(self.geometry.mesh)
        for alpha in range(self.n_fields):
            for m in range(self.geometry.n_contacts):
                I[alpha, m] = dol.assemble(dol.inner(self._currents[alpha], normal) * self.geometry.ds(m + 1)) 
        self._fluxes = I

    def compute_solution_basis(self):
        '''$ Compute a solution basis for the homogeneous equation given by 
        $\phi^{(\alpha,m)}(\bm r)$, which are the solutions of the homogeneous 
        problem with $V_{\beta, m } = \delta_{\alpha \beta}\delta{m n}$ 
        '''
        if self._solution_basis is None:
            F = [dol.Constant(0) for alpha in range(self.n_fields)]
            solution_basis = []
            for alpha in range(self.n_fields):
                column = []
                for m in range(self.geometry.n_contacts):
                    biases = np.zeros([self.n_fields, self.geometry.n_contacts])
                    biases[alpha, m] = 1.
                    column.append(self._solve(L = self.L, Gamma = self.Gamma, contact_resistances = self.contact_resistances, biases = biases, F = F))
                solution_basis.append(column)
            self._solution_basis = solution_basis
        else:
            warn('solution_basis already present')

    def compute_adjoint_solution_basis(self):
        '''$ Compute a solution basis for the adjoint homogeneous equation given by 
        $\tilde{\phi}^{(\alpha,m)}(\bm r)$, which are the solutions of the adjoint homogeneous 
        problem with $V_{\beta, m } = \delta_{\alpha \beta}\delta{m n}$ 
        '''
        if self._self_adjoint:
            if self._solution_basis is None:
                self.compute_solution_basis()
            self._adjoint_solution_basis = self._solution_basis
            
        else:
            if self._adjoint_solution_basis is None:
                F = [dol.Constant(0) for alpha in range(self.n_fields)]
                adjoint_solution_basis = []
                for alpha in range(self.n_fields):
                    column = []
                    for m in range(self.geometry.n_contacts):
                        biases = np.zeros([self.n_fields, self.geometry.n_contacts])
                        biases[alpha, m] = 1.
                        column.append(self._solve(L = self._L_T, Gamma = self._Gamma_T, contact_resistances = self.contact_resistances, biases = biases, F = F))
                    adjoint_solution_basis.append(column)
                self._adjoint_solution_basis = adjoint_solution_basis
            else:
                warn('adjoint_solution_basis already present')

    def compute_responsivities(self):
        '''Compute responsivity functions'''
        self.compute_adjoint_solution_basis()
        responsivities = []
        for alpha in range(self.n_fields):
            column = []
            for m in range(self.geometry.n_contacts):
                if self.n_fields > 1:
                    fun = self._adjoint_solution_basis[alpha][m].split(deepcopy = True)
                else:
                    fun = [self._adjoint_solution_basis[alpha][m].copy(deepcopy = True)]
                column.append(fun)
            responsivities.append(column)
        self._responsivities = responsivities

    def compute_response_matrix(self, method = 1):
        ''' Compute the response matrix G_{\alpha,m;\beta,n}
        Parameters
        ----------
        method : int, by default 1
        computational method to be used: 
        1 : direct evaluation of fluxes (faster)
        2 : volume integral (symmetric by construction)

        '''
                
        if self._solution_basis is None:
            self.compute_solution_basis()
        if method == 1:
            G = np.zeros([self.n_fields, self.geometry.n_contacts, self.n_fields, self.geometry.n_contacts])
            normal = dol.FacetNormal(self.geometry.mesh)
            for alpha in range(self.n_fields):
                for m in range(self.geometry.n_contacts):
                    for beta in range(self.n_fields):
                        for n in range(self.geometry.n_contacts):
                            term = []
                            for gamma in range(self._n_fields):
                                term.append(
                                    dol.inner(normal, -self._L[alpha][gamma]*dol.grad(self._solution_basis[beta][n][gamma]))
                                    * self.geometry.ds(m+1)
                                )
                            G[alpha, m, beta, n] = dol.assemble(sum(term))
            self._response_matrix = G
        elif method == 2:
            #bulck contribution
            G = np.zeros([self.n_fields, self.geometry.n_contacts, self.n_fields, self.geometry.n_contacts])
            for alpha in range(self.n_fields):
                for m in range(self.geometry.n_contacts):
                    for beta in range(self.n_fields):
                        for n in range(self.geometry.n_contacts):
                            L_term = []
                            Gamma_term = []
                            for gamma in range(self.n_fields):
                                for delta in range (self.n_fields):
                                    term1 = (dol.inner(dol.grad(self._solution_basis[alpha][m][gamma]),self.L[gamma][delta] * dol.grad(self._solution_basis[beta][n][delta])) * self.geometry.dx)
                                    L_term.append(term1)
                                    term2 = (self._solution_basis[alpha][m][gamma] * self.Gamma[gamma][delta] * self._solution_basis[beta][n][delta] * self.geometry.dx)
                                    Gamma_term.append(term2)
                            G[alpha, m, beta, n] = (-dol.assemble(sum(L_term)) - dol.assemble(sum(Gamma_term)))
            #contact resistance contribution
            G_cont = np.zeros([self.n_fields, self.geometry.n_contacts, self.n_fields, self.geometry.n_contacts])
            if not (self._contact_resistances == 0.).all():
                normal = dol.FacetNormal(self.geometry.mesh)
                for alpha in range(self.n_fields):
                    for m in range(self.geometry.n_contacts):
                        for beta in range(self.n_fields):
                            for n in range(self.geometry.n_contacts):
                                term = []
                                for p in range(self.geometry.n_contacts):
                                    for gamma in range(self.n_fields):
                                        for delta in range(self.n_fields):
                                            for epsilon in range(self.n_fields):
                                                term.append(
                dol.Constant(self._contact_resistances[gamma,p])
                *dol.inner(normal, self.L[gamma][delta] * dol.grad(self._solution_basis[beta][n][delta])) 
                *dol.inner(normal, self.L[gamma][epsilon] * dol.grad(self._solution_basis[alpha][m][epsilon])) 
                * self.geometry.ds(p+1))
                                G_cont[alpha, m, beta, n] = -dol.assemble(sum(term))
            self._response_matrix = G + G_cont
        else:
            warn('invalid method')

    def compute_solution_inhomogeneous(self):
        '''Compute solution of the inhomogeneous equation with all the biases set to 0.
        '''
        biases = np.zeros([self.n_fields, self.geometry.n_contacts])
        self._solution_inhomogeneous = self._solve(L = self.L, Gamma = self.Gamma, contact_resistances = self.contact_resistances, biases = biases, F = self.F)

    def compute_source_vector(self, method = 1):
        """Compute the matrix S_{\alpha,m}[F]

        Parameters
        ----------
        method : int, by default 1
        computational method to be used: 
        1 : direct evaluation of fluxes (faster)
        2 : volume integral (symmetric by construction)
        """        
        if self._solution_inhomogeneous is None:
            self.compute_solution_inhomogeneous()
        if method == 1:
            S = np.zeros([self.n_fields, self.geometry.n_contacts])
            normal = dol.FacetNormal(self.geometry.mesh)
            for alpha in range(self.n_fields):
                for m in range(self.geometry.n_contacts):
                    term = []
                    for gamma in range(self.n_fields):
                        term.append(dol.inner(normal, -self._L[alpha][gamma]*dol.grad(self._solution_inhomogeneous[gamma]))
                                        * self.geometry.ds(m+1))
                    S[alpha, m] = dol.assemble(sum(term))
            self._source_vector = S
        elif method == 2:
            S = np.zeros([self.n_fields, self.geometry.n_contacts])
            for alpha in range(self.n_fields):
                for m in range(self.geometry.n_contacts):
                    L_term = []
                    Gamma_term = []
                    F_term = []
                    for gamma in range(self.n_fields):
                        for delta in range (self.n_fields):
                            term1 = (dol.inner(dol.grad(self._solution_basis[alpha][m][gamma]), self.L[gamma][delta] * dol.grad(self._solution_inhomogeneous[delta])) * self.geometry.dx)
                            L_term.append(term1)
                            term2 = (self._solution_basis[alpha][m][gamma] * self.Gamma[gamma][delta] * self._solution_inhomogeneous[delta] * self.geometry.dx)
                            Gamma_term.append(term2)
                    for gamma in range(self.n_fields):
                        term3 = (- self._solution_basis[alpha][m][gamma] * self.F[gamma] *  self.geometry.dx)
                        F_term.append(term3)
                    #for symmetric L and Gamma the first two terms are 0
                    S[alpha, m] = -(dol.assemble(sum(L_term)) + dol.assemble(sum(Gamma_term)) + dol.assemble(sum(F_term)))
            self._source_vector = S
        else:
            warn('invalid method')
    
    def plot_field(self, field, show_mesh = True, **kwargs):
        """Plot a field component

        Parameters
        ----------
        field : int
            index of the component to be plotted
        show_mesh : bool, optional
            whether to show the mesh, by default True
        **kwargs : kwargs to be passed to plt.tripcolor

        Returns
        -------
        p1, p2
            field and mesh as returned by matplotlib
        """            
        if self.fields is None:
            self.solve()
        if show_mesh:
            p2 = plot_mesh(self.geometry.mesh)
        else:
            p2 = None
        p1 = plot_function(function = self._fields[field], **kwargs)
        return p1, p2

    def plot_current(self, current, show_mesh = True, **kwargs):
        """Plot current as vector field

        Parameters
        ----------
        current : int
            current component to be plotted
        show_mesh : bool, optional
            whetheer to plot the mesh, by default True
        **kwargs : kwargs to be passed to plt.quiver

        Returns
        -------
        p1, p2 
            vector field and mesh as returned by matplotlib
        """        
        if self.currents is None:
            self.compute_currents()
        if show_mesh:
            p2 = plot_mesh(self.geometry.mesh)
        else:
            p2 = None
        p1 = plot_current(current = self.currents[current], **kwargs)
        return p1, p2
    
    def plot_responsivity(self, flux, contact, source, show_mesh = True, **kwargs):
        """Plot a responsivity function

        Parameters
        ----------
        flux : int
            flux component
        contact : int
            contact (must be 1<= contact <= n_contacts)
        source : int
            source component
        show_mesh : bool, optional
            whether to show the mesh, by default True
        **kwargs : kwargs to be passed to plt.tripcolor

        Returns
        -------
        p1, p2
            plot of responsivity and mesh as returned by matplotlib
        """        
        assert contact in range(1, self.geometry.n_contacts + 1), 'not a valid contact'
        if self._responsivities is None:
            self.compute_responsivities()
        if show_mesh:
            p2 = plot_mesh(self.geometry.mesh)
        else:
            p2 = None
        p1 = plot_function(function = self._responsivities[flux][contact-1][source], **kwargs)
        return p1, p2
    
    def save(self, folder = '', file_format = 'xdmf'):
        """Save all the output to the given folder

        Parameters
        ----------
        folder : str
            name of the directory where files are saved
        file_format : str
            type of output. Only 'xdmf' implemented
        """ 

        if not os.path.exists(folder):
            os.makedirs(folder)
        if not self._response_matrix is None:
            np.save( folder + '/response_matrix', self._response_matrix)
        if not self._source_vector is None:
            np.save( folder + '/source_vector', self._source_vector)
        if file_format == 'xdmf':
            if not self._fields is None:
                for alpha in range(self._n_fields):
                    with dol.XDMFFile(folder + '/field_{}.xdmf'.format(alpha)) as xdmf_file:
                        xdmf_file.write(self._fields[alpha])
            if not self._currents is None:
                for alpha in range(self._n_fields):
                    with dol.XDMFFile(folder + '/current_{}.xdmf'.format(alpha)) as xdmf_file:
                        xdmf_file.write(self._currents[alpha])
            if not self._responsivities is None:
                for alpha in range(self._n_fields):
                    for beta in range(self._n_fields):
                        for m in range(self.geometry.n_contacts):
                            with dol.XDMFFile(folder + '/responsivity_{}_{}_{}.xdmf'.format(alpha,m+1,beta)) as xdmf_file:
                                xdmf_file.write(self._responsivities[alpha][m][beta])
            if not self._solution_basis is None:
                for alpha in range(self._n_fields):
                    for m in range(self.geometry.n_contacts):
                        if self.n_fields > 1:
                            function_to_write = self._solution_basis[alpha][m].split(deepcopy = False)
                        else:
                            function_to_write = [self._solution_basis[alpha][m]]
                        for beta in range(self._n_fields):
                            with dol.XDMFFile(folder + '/solution_{}_{}_{}.xdmf'.format(alpha,m+1,beta)) as xdmf_file:
                                xdmf_file.write(function_to_write[beta])
            if not self._solution_inhomogeneous is None:
                if self.n_fields > 1:
                    function_to_write = self._solution_inhomogeneous.split(deepcopy = False)
                else:
                    function_to_write = [self._solution_inhomogeneous]
                for beta in range(self._n_fields):
                    with dol.XDMFFile(folder + '/solution_inhomogeneous_{}.xdmf'.format(beta)) as xdmf_file:
                                xdmf_file.write(function_to_write[beta])
        else:
            warn('unrecognized file format')