#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Useful classes and functions to work with FENICS'''
################## Import modules #############################################
import os
from warnings import warn

import numpy as np
import matplotlib.pyplot as plt

import dolfin as dol
import meshio
################## Class for matrix coefficients ##############################
class Matrix_Expression(dol.UserExpression):
    """Class for defining matrix coefficients"""    
    def __init__(self,
                 entries,
                 marker = None,
                 dimension = 1,
                 scalar = True,
                 mesh = None,
                 *args,
                 **kwargs):
        """Initialize coefficient matrix

        Parameters
        ----------
        entries : number, meshfunction, callable or list of lists of those, or dict (if marker is not None)
            the entries of the matrix
        marker : None or cellfunction returning an int, optional
            Marker of the mesh subdomains, by default None
        dimension : int, optional
            dimension of the matrix, by default 1
        scalar : bool, optional
            whether the matrix is a scalar matrix, by default True
        mesh : dolfin mesh, optional
            mesh in case entries is callable, by default None
        
        *args and **kwargs 
            to be passed to the superclass initialization"""

        self.entries = entries 
        self.marker = marker
        self.dimension = int(dimension) 
        self.scalar = scalar
        #exp feature
        assert (mesh is None or isinstance(mesh, dol.cpp.mesh.Mesh)) 
        self.mesh = mesh
        #
        self.args = args
        self.kwargs = kwargs
        #
        self._function = None
        self._cell_values = None
        #check the type of initialization (numbers or meshfunctions) 
        if scalar:
            if marker is None:
                self.is_constant = isinstance(entries,(int,float,complex)) 
                self.is_meshfunction = isinstance(entries,(dol.cpp.mesh.MeshFunctionDouble, dol.cpp.mesh.MeshFunctionInt,dol.cpp.mesh.MeshFunctionSizet)) 
                #exp feature
                self.is_callable = callable(entries)
                #
                self.is_markerfunction = False
            elif isinstance(marker,(dol.cpp.mesh.MeshFunctionDouble, dol.cpp.mesh.MeshFunctionInt ,dol.cpp.mesh.MeshFunctionSizet)):
                assert all(isinstance(value,(int,float,complex))for value in entries.values())
                self.is_constant = False
                self.is_meshfunction = False
                #exp feature
                self.is_callable = False
                #
                self.is_markerfunction = True
                
            else:
                raise TypeError('wrong marker type')
        else:
            if marker is None:
                assert len(entries) == dimension
                assert all(len(row) == dimension for row in entries)
                self.is_constant = all(isinstance(entries[i][j],(int,float,complex)) for i in range(dimension) for j in range(dimension)) 
                self.is_meshfunction = all(isinstance(entries[i][j],(dol.cpp.mesh.MeshFunctionDouble, dol.cpp.mesh.MeshFunctionInt,dol.cpp.mesh.MeshFunctionSizet)) for i in range(dimension) for j in range(dimension))
                #exp feature
                self.is_callable = all(callable(entries[i][j]) for i in range(dimension) for j in range(dimension))
                #
                self.is_markerfunction = False
            elif isinstance(marker,(dol.cpp.mesh.MeshFunctionDouble, dol.cpp.mesh.MeshFunctionInt ,dol.cpp.mesh.MeshFunctionSizet)):
                for value in entries.values():
                    assert len(value) == dimension
                    assert all(len(row) == dimension for row in value)
                assert all(isinstance(value[i][j],(int,float,complex)) for value in entries.values() for i in range(dimension) for j in range(dimension))
                self.is_constant = False
                self.is_meshfunction = False
                #exp feature
                self.is_callable = False
                #
                self.is_markerfunction = True
            else:
                raise TypeError('wrong marker type')
        ### exp 
        if not(self.is_constant or self.is_meshfunction or self.is_markerfunction or self.is_callable):
            raise(TypeError)
        ## exp
        if self.is_callable:
            if self.scalar == True:
                self.cell_function = create_cellfunction(self.mesh, entries)
            else:
                self.cell_function = [create_cellfunction(self.mesh, entries[i][j]) for i in range(self.dimension) for j in range(self.dimension)]
        ##
        if self.is_meshfunction:
            if self.scalar:
                self.mesh = self.entries.mesh
            else:
                assert all(self.entries[i][j].mesh() == self.entries[0][0].mesh() for i in range(self.dimension) for j in range(self.dimension)), 'meshfunctions with different meshes'
                self.mesh = self.entries[0][0].mesh()
        if self.is_markerfunction:
            self.mesh = self.marker.mesh()
        dol.UserExpression.__init__(self, *args, **kwargs) 


    def eval_cell(self, value, x, cell):
        if self.is_constant:
            if self.scalar:
                value[:] = self.entries * np.ravel(np.identity(self.dimension))
            else:
                value[:] = [self.entries[i][j] for i in range(self.dimension) for j in range(self.dimension)]
        elif self.is_meshfunction:
            if self.scalar:
                value[:] = self.entries[cell.index] * np.ravel(np.identity(self.dimension))
            else:
                value[:] = [self.entries[i][j][cell.index] for i in range(self.dimension) for j in range(self.dimension)]
        ###
        elif self.is_callable:
            if self.scalar:
                value[:] = self.cell_function[cell.index] * np.ravel(np.identity(self.dimension))
            else:
                value[:] = [component[cell.index] for component in self.cell_function]
        ###
        elif self.is_markerfunction:
            if self.scalar:
                value[:] = self.entries[self.marker[cell.index]] * np.ravel(np.identity(self.dimension))
            else:
                value[:] = [self.entries[self.marker[cell.index]][i][j] for i in range(self.dimension) for j in range(self.dimension)]

    def value_shape(self):
        if self.dimension >=2:
                return (self.dimension,self.dimension)
        else:
            return ()

    def transposed(self):
        '''returns an instance with the transposed coefficient '''
        if self.scalar:
            entries_transposed = self.entries
        elif self.is_constant or self.is_meshfunction or self.is_callable:
            entries_transposed = [list(i) for i in zip(*self.entries)]
        else:
            entries_transposed = {}
            for key in self.entries:
                entries_transposed[key] = [list(i) for i in zip(*self.entries[key])]
        return Matrix_Expression(entries = entries_transposed, 
                                 marker = self.marker, 
                                 dimension = self.dimension, 
                                 scalar = self.scalar, 
                                 mesh = self.mesh, 
                                 *self.args, **self.kwargs)

    def project(self, mesh = None):
        """
        docstring
        """
        assert (mesh is None or isinstance(mesh, dol.cpp.mesh.Mesh)) 
        if mesh is None:
            assert not (self.mesh is None), 'no mesh provided'
        else:
            assert (self.mesh is None or self.mesh == mesh), 'mesh already present'
            self.mesh = mesh
        if self.dimension >1:
            W2 = dol.TensorFunctionSpace(self.mesh, "DP", 0)
        else:
            W2 = dol.FunctionSpace(self.mesh, "DP", 0)
        self._function_space = W2
        self._function = dol.project(self, W2)
        return self._function

    def compute_cell_values(self, mesh = None):
        assert (mesh is None or isinstance(mesh, dol.cpp.mesh.Mesh))
        if mesh is None:
            assert not (self.mesh is None), 'no mesh provided'
        else:
            assert (self.mesh is None or self.mesh == mesh), 'mesh already present'
            self.mesh = mesh
        self.project()
        self._cell_values = np.array([self._function.vector().get_local()[self._function_space.dofmap().cell_dofs(cell.index())] for cell in dol.cells(self.mesh)]).reshape(-1,self.dimension,self.dimension)
    
    def plot(self, i, j, mesh = None, show_mesh = True, **kwargs):
        assert (mesh is None or isinstance(mesh, dol.cpp.mesh.Mesh))
        if mesh is None:
            assert not (self.mesh is None), 'no mesh provided'
        else:
            assert (self.mesh is None or self.mesh == mesh), 'mesh already present'
            self.mesh = mesh
        self.compute_cell_values()
        if self.mesh.topology().dim() == 2:
            plt.axis('equal')
            if show_mesh:
                p2 = plot_mesh(self.mesh)
            else:
                p2 = None
            p1 = plt.tripcolor(self.mesh.coordinates()[:,0], self.mesh.coordinates()[:,1], self.mesh.cells(), self._cell_values[:,i,j], **kwargs)
            return p1, p2
        else:
            warn('only 2D plotting')

    @property
    def function(self):
        if self._function is None:
            self.project()
        return self._function
    @function.setter
    def function(self, _):
        warn('read only')

    @property
    def cell_values(self):
        if self._cell_values is None:
            self.compute_cell_values()
        return self._cell_values
    @cell_values.setter
    def cell_values(self, _):
        warn('read only')
#################### Functions for boundaries and subdomains ##################
#2d only
def close_to_segment(x, r0, r1, tol):
    '''Function that returns whether a point x is closer than tol to a segment 
    identified by its endpoints r0 and r1.
    Parameters : 
    x :
    r0 :
    r1 :
    tol :
    Returns :'''
    l = np.sqrt((r0[0]-r1[0])**2+(r0[1]-r1[1])**2)
    m = [(r1[0] + r0[0])/2. , (r1[1] + r0[1])/2.]
    if l < tol:
        return (x[0]-m[0])**2 + (x[1]-m[1])**2 <= tol**2
    else:
        f = ((r1[1]-r0[1])*(x[0]-r0[0])-(r1[0]-r0[0])*(x[1]-r0[1]))/l
        g = ((r1[0]-r0[0]) * (x[0] - m[0]) + (r1[1]-r0[1]) * (x[1]-m[1]))/l
        return ((abs(f) <= tol) and (abs(g) <= 0.5 * l + tol))

#2d only
def close_to_line(x,line,tol):
    '''returns whether a point is closer than tol to a line. line is a list of 
    points in 2D space like [[0.,0.],[0.,1.],[1.,1.]]'''
    result = False
    for i in range(len(line)-1):
        result = result or close_to_segment(x,line[i],line[i+1],tol)
    return result

#2d only
class Boundary_Close_To_Line(dol.SubDomain):
    '''class for boundary points close to a line'''
    def __init__(self, line, tol = dol.DOLFIN_EPS):
        dol.SubDomain.__init__(self)
        self.line = line
        self.tol = tol
    def inside(self, x, on_boundary):
        return on_boundary and close_to_line(x, self.line, self.tol)

#2d only
class Close_To_Line(dol.SubDomain):
    '''class for points close to a line'''
    def __init__(self, line, tol = dol.DOLFIN_EPS):
        dol.SubDomain.__init__(self)
        self.line = line
        self.tol = tol
    def inside(self, x, on_boundary):
        return close_to_line(x,self.line, self.tol)

class Periodic_Boundary(dol.SubDomain):
    def __init__(self, direction = 0, xmin = 0, xmax = 1):
        self.direction = direction
        self.xmin = xmin
        self.xmax = xmax
        dol.SubDomain.__init__(self)
    def inside(self, x, on_boundary):
        return bool(x[self.direction] < self.xmin + dol.DOLFIN_EPS 
                    and x[self.direction] > self.xmin - dol.DOLFIN_EPS 
                    and on_boundary)
    def map(self, x, y):
        for i in range(len(x)):
            if i == self.direction:
                y[i] = x[i] - self.xmax + self.xmin
            else:
                y[i] = x[i]
############ Create a cell function from callable #############################
def create_cellfunction(mesh, f):
    '''creates a cell function from a mesh and a python function'''
    dim = mesh.topology().dim()
    fun = dol.MeshFunction("double", mesh, dim)
    for cell in dol.cells(mesh):
        if dim == 1:
            fun[cell] = f(cell.midpoint().x())
        elif dim == 2:
            fun[cell] = f(cell.midpoint().x(),cell.midpoint().y())
        elif dim == 3:
            fun[cell] = f(cell.midpoint().x(),cell.midpoint().y(), cell.midpoint().z())
    return fun
########### Plotting functions#################################################
def plot_mesh(mesh, **kwargs):
    if mesh.topology().dim() == 2:
        if not 'c' in kwargs.keys():
            kwargs['c'] = 'k'
        if not 'lw' in kwargs.keys():
            kwargs['lw'] = '0.1'
        p1 = plt.triplot(mesh.coordinates()[:,0], mesh.coordinates()[:,1], triangles = mesh.cells(), **kwargs)
        return p1
    else:
        warn('only 2D plotting')

def plot_cell_function(cell_function, **kwargs):
    mesh = cell_function.mesh()
    if mesh.topology().dim() == 2:
        p1 = plt.tripcolor(mesh.coordinates()[:,0], mesh.coordinates()[:,1], mesh.cells(), cell_function.array(), **kwargs)
        return p1
    else:
        warn('only 2D plotting')

def plot_function(function, **kwargs):
    mesh = function.function_space().mesh()
    if mesh.topology().dim() == 2:
        p1 = plt.tripcolor(mesh.coordinates()[:,0], mesh.coordinates()[:,1], mesh.cells(), function.compute_vertex_values(mesh), **kwargs)
        return p1
    else:
        warn('only 2D plotting')

def plot_current(current, **kwargs): 
    mesh = current.function_space().mesh()
    if mesh.topology().dim() == 2:
        vector_function_space = current.function_space()
        cells_centers = np.array([(cell.midpoint().x(), cell.midpoint().y()) for cell in dol.cells(mesh)])
        current_cells = np.array([current.vector().get_local() [vector_function_space.dofmap().cell_dofs(cell.index())] for cell in dol.cells(mesh)])
        abs_current = np.sqrt(current_cells[:,0]**2+current_cells[:,1]**2)
        if not 'cmap' in kwargs.keys():
            kwargs['cmap'] = 'Greys_r'
        if not 'scale' in kwargs.keys():
            kwargs['scale'] = 50
        p1 = plt.quiver(cells_centers[:,0],cells_centers[:,1],
                        current_cells[:,0]/abs_current, 
                        current_cells[:,1]/abs_current ,
                    abs_current,
                        **kwargs)
        return p1
    else:
        warn('only 2D plotting')

def plot_facet_function(facet_function, markers = None, **kwargs):
    mesh = facet_function.mesh()
    if mesh.topology().dim() == 2:
        x_list, y_list = [],[]
        if markers is None:
            for facet in dol.facets(mesh):
                mp = facet.midpoint()
                x_list.append(mp.x())
                y_list.append(mp.y())
            new_facet_function = facet_function.array()
        else:
            i = 0
            new_facet_function = []
            for facet in dol.facets(mesh):
                if facet_function[i] in markers:
                    mp = facet.midpoint()
                    x_list.append(mp.x())
                    y_list.append(mp.y())
                    new_facet_function.append(facet_function[i])
                i+=1
        p1 = plt.scatter(x_list, y_list, c=new_facet_function, **kwargs)
        return p1
    else:
        warn('only 2D plotting')
########### Mesh conversion functions ##################################
def convert_msh_to_XDMF(filename, dim, dim_keep = None):
    '''reads a .msh file and writes mesh, subdomains, and boundary subdomains 
    to XDMF files'''
    if filename.split(sep = '.')[-1] != 'msh':
        raise TypeError('.msh file required')
    fn = '.'.join(filename.split(sep ='.')[:-1])
    if dim_keep is None:
        dim_keep = dim
    msh = meshio.read(filename)
    if dim == 1:
        volume_cell_type = 'line'
        surface_cell_type = 'vertex'
    elif dim == 2:
        volume_cell_type = 'triangle'
        surface_cell_type = 'line'
    elif dim == 3:
        volume_cell_type = 'tetra'
        surface_cell_type = 'triangle'
    else:
        raise ValueError('dim can only be 1,2, or 3')
    
    volume_cells = []
    surface_cells = []
    for cell in msh.cells:
        if cell.type == volume_cell_type:
            if len(volume_cells) == 0:
                volume_cells = cell.data
            else:
                volume_cells = np.vstack([volume_cells, cell.data])

        if cell.type == surface_cell_type:
            if len(surface_cells) == 0:
                surface_cells = cell.data
            else:
                surface_cells = np.vstack([surface_cells, cell.data])
        
    volume_data = None
    surface_data = None
    for key in msh.cell_data_dict['gmsh:physical'].keys():
        if key == volume_cell_type:
            volume_data = msh.cell_data_dict['gmsh:physical'][key]
        elif key == surface_cell_type:
            surface_data = msh.cell_data_dict['gmsh:physical'][key]
    volume_mesh = meshio.Mesh(points = msh.points[:,:dim_keep],
                                cells = [(volume_cell_type, volume_cells)],
                                cell_data = {'marker' : [volume_data]})
    meshio.write(fn + '_{}D_mesh.xdmf'.format(dim), volume_mesh)
    if not (surface_data is None):
        surface_mesh = meshio.Mesh(points = msh.points[:,:dim_keep], 
                                    cells = [(surface_cell_type, surface_cells)],
                                    cell_data = {'marker' : [surface_data]})
        meshio.write(fn + '_{}D_mesh.xdmf'.format(dim-1), surface_mesh)
    

def load_XDMF_files(filename, dim):
    '''create mesh from XDMF files'''
    mesh = dol.Mesh()
    fn = '.'.join(filename.split(sep ='.')[:-1])
    with dol.XDMFFile(fn + '_{}D_mesh.xdmf'.format(dim)) as infile:
        infile.read(mesh)
    mvc = dol.MeshValueCollection('size_t', mesh = mesh, dim = dim) 
    with dol.XDMFFile(fn + '_{}D_mesh.xdmf'.format(dim)) as infile:
        infile.read(mvc, 'marker')
    volume_marker = dol.cpp.mesh.MeshFunctionSizet(mesh, mvc)
    del(mvc)
    dx = dol.Measure('dx', domain = mesh, subdomain_data = volume_marker)

    if os.path.exists(fn + '_{}D_mesh.xdmf'.format(dim-1)):
        mvc = dol.MeshValueCollection('size_t', mesh = mesh, dim = dim -1) 
        with dol.XDMFFile(fn +  '_{}D_mesh.xdmf'.format(dim-1)) as infile:
            infile.read(mvc, 'marker')
        boundary_marker = dol.cpp.mesh.MeshFunctionSizet(mesh, mvc)
        del(mvc)
        ds = dol.Measure('ds', domain = mesh, subdomain_data = boundary_marker)
        dS = dol.Measure('dS', domain = mesh, subdomain_data = boundary_marker)
    else:
        warn('{}D mesh not found'.format(dim-1))
        boundary_marker = None
        ds = dol.Measure('ds', domain = mesh)
        dS = dol.Measure('dS', domain = mesh)
    return {'mesh' : mesh, 
            'volume_measure' : dx,
            'boundary_measure' : ds,
            'internal_boundary_measure' : dS,
            'volume_marker' : volume_marker,
            'boundary_marker' : boundary_marker}