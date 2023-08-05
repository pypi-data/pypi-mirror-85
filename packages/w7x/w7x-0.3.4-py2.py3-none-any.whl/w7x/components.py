import logging
import tfields
import numpy as np
import scipy.stats
import os

import w7x
from w7x import core
import rna


def n_hits_from_load(q, n_tot, area, p_conv, ceta):
    """
    Args:
        q(float) heat load
        n_tot (int): total number of hits
        area (float)
        p_conv (float): convective power
        ceta (int): mapping factor

    Returns float: number of hits expected on area given Args
    """
    p_conv *= 1.0 / ceta  # correct for mapping all divertors to one
    return int(round((1.0 * q * n_tot * area) / p_conv))


def load_from_n_hits(n_hits, n_tot, area, p_conv, ceta):
    """
    Args:
        n_hits (int): numer of hits on the area
        n_tot(int): total number of hits
        area (float)
        p_conv (float): convective power
        ceta (int): mapping factor

    Returns float: heat per area given Args
    """
    p_conv *= 1.0 / ceta  # correct for mapping all divertors to one
    return (n_hits * p_conv) * 1.0 / (n_tot * area)


def prob_n_hits_lt_n_des(n_hits_list, n_des_list):
    """
    Returns: P(n_hits < n_des | p_conv, n_tot, q_design)
        see [Boeckenhoff2019](doi:10.1088/1741-4326/ab201e)
    """
    tile_probs = []
    for n_hits, n_des in zip(n_hits_list, n_des_list):
        n_hits = int(np.round(n_hits))
        p = scipy.stats.poisson.cdf(n_des, n_hits)
        tile_probs.append(float(p))
    return tile_probs


class Points3D(core.BasePoints3D):
    ws_server = w7x.Server.addr_components_db


class Base(core.Base):
    """
    Field Line Server Base
    """

    ws_server = w7x.Server.addr_components_db


class Polygon(Base):
    """
    element.vertices gives you the three points numbers to a triangle.
    This is normally refered to as face
    """

    prop_defaults = {"vertices": None}


class MeshedModel(Base):
    """
    Args:
        multiple ways:
            vertices (list)
            faces (list)

            - or -

            group from ObjFile

            - or -

            tfields.Mesh3D object
    Attributes:
        nodes (Points3D): = vertices (coordinates) of the points.
        elements (list[Polygon]): = faces (always three indices of points for a
            triangle). Starting at 1 here
    Examples:
        use with Mesh3D as inp
        >>> from w7x.flt import MeshedModel
        >>> import tfields
        >>> m = tfields.Mesh3D([[1,2,3], [3,3,3], [0,0,0], [5,6,7]],
        ...                    faces=[[0, 1, 2], [1, 2, 3]])
        >>> mm = MeshedModel(m)

        Get the osa type, in this case for field line server
        >>> fls = mm.as_input()

        return Mesh3D works
        >>> bool((m == mm.as_mesh3d()).all())
        True

        create with meshed Model from fls works
        >>> m2 = MeshedModel(fls).as_mesh3d()
        >>> assert tfields.Points3D(m2).equal(
        ...     [[ 1.,  2.,  3.],
        ...      [ 3.,  3.,  3.],
        ...      [ 0.,  0.,  0.],
        ...      [ 5.,  6.,  7.]])
        >>> assert tfields.Tensors(m2.faces).equal([[0, 1, 2], [1, 2, 3]])

    """

    prop_defaults = {
        "nodes": None,
        "elements": None,
        "nodesIds": None,
        "elementsIds": None,
    }

    def __init__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 1:
            logging.error(" Implementation did not work.")
            raise NotImplementedError(
                " Implementation with args %s not yet implemented!" % args
            )
        elif len(args) == 1 and issubclass(args[0].__class__, tfields.Mesh3D):
            mesh3D = args.pop(0)
            nodes = Points3D(mesh3D)
            faces = mesh3D.faces + 1
            kwargs["nodes"] = kwargs.pop("nodes", nodes)
            kwargs["elements"] = kwargs.pop(
                "elements", [Polygon(vertices=face) for face in faces]
            )
        super(MeshedModel, self).__init__(*args, **kwargs)

    @classmethod
    def from_mm_id(cls, mm_id):
        comp_db_server = w7x.get_server(w7x.Server.addr_components_db)
        # caching mechanism
        mm_id_cache_path = w7x.Defaults.Paths.cache_path_components / (
            "meshed_model_mm_id_" + str(mm_id) + ".npz"
        )
        if os.path.exists(str(mm_id_cache_path)):
            with rna.log.timeit(
                "[w7x cache] - Loading MeshedModel for mm_id"
                " {mm_id}".format(**locals())
            ):
                obj = MeshedModel.load(mm_id_cache_path)
        else:
            with rna.log.timeit(
                "[w7x cache] - Calling getComponentData(" "{mm_id})".format(**locals())
            ):
                component_data = comp_db_server.service.getComponentData(mm_id)
                obj = cls(component_data[0])
                obj.save(mm_id_cache_path)
        return obj

    @classmethod
    def mesh3d(cls, mm_id):
        """
        Equivalent to MeshedModel(mm_id).as_mesh3d() but much faster cache
        as compared to cached MeshedModel. tfields loading is fast.

        Returns:
            tfields.Mesh3D
        """
        # caching mechanism
        mm_id_cache_path = w7x.Defaults.Paths.cache_path_components / (
            "mesh_mm_id_" + str(mm_id) + ".npz"
        )
        if os.path.exists(str(mm_id_cache_path)):
            with rna.log.timeit(
                "[w7x cache] - Loading Mesh3D for mm_id" " {mm_id}".format(**locals())
            ):
                obj = tfields.Mesh3D.load(mm_id_cache_path)
        else:
            with rna.log.timeit(
                "[w7x cache] - Calling MeshedModel({mm_id})"
                ".as_mesh3d()".format(**locals())
            ):
                instance = cls.from_mm_id(mm_id)
                obj = instance.as_mesh3d()
                obj.save(mm_id_cache_path)
        return obj

    def as_mesh3d(self):
        """
        Returns:
            tfields.Mesh3D
        """
        faces = np.array([pol.vertices for pol in self.elements])
        faces -= 1
        return tfields.Mesh3D(Points3D(self.nodes), faces=faces)


class HistoryNote(Base):
    prop_defaults = {
        "comment": None,  # str
        "author": None,  # str
        "date": None,  # datetime
        "method": None,  # str
    }


class ComponentStorageInfo(Base):
    prop_defaults = {
        "comment": None,  # str
        "polygonTypes": None,  # List[int]
        "numNodes": None,  # int
        "id": None,  # str
        "machine": "w7x",  # str, ws default is None
        "min": None,  # List[float]
        "numElements": None,  # int
        "state": None,  # str
        "location": None,  # str
        "accuracy": None,  # float
        "max": None,  # List[float]
        "name": None,  # str
        "subids": None,  # List[str]
        "author": None,  # str
        "method": None,  # str
        "resolution": None,  # float
        "hisotry": None,  # List(HistoryNote)
    }


class FullComponentEntry(Base):
    prop_defaults = {
        "info": None,  # ComponentStorageInfo
        "data": None,  # MeshedModel
    }

    @property
    def parent(self):
        return self._parent
