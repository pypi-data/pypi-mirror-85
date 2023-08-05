#!/usr/bin/env
"""
Field line tracer specifics
author: daniel.boeckenhoff@ipp.mpg.de
"""
import logging
import os
import functools
import numpy as np

import rna
import tfields

import w7x
from w7x.components import MeshedModel


class Points3D(w7x.core.BasePoints3D):
    """
    Inheriting from tfields.Points3D ultimately
    Additional: methods for conversion to webservice input
    """

    ws_server = w7x.Server.addr_field_line_server


class Base(w7x.core.Base):
    """
    Field Line Server Base
    """

    ws_server = w7x.Server.addr_field_line_server


class ConnectionLength(Points3D):
    """Class to Convert ConnectionLengthResult in.
    Make it easy to handle info about the different parts you gave it.
    The Hit points are the content of the np.ndarray (Points3D)

    Args:
        connectionLengthResult

    Attributes:
        x1 (list): coordinate x
        x2 (list): coordinate y
        x3 (list): coordinate z
        lengths (list)
        parts (list): part ids refering to mm_ids index
        elements (list): element ids refering to face index + 1

    Examples:
        Adding up two instances
        >>> from w7x.flt import ConnectionLength
        >>> import numpy as np
        >>> c = ConnectionLength.create_test()
        >>> c.parts
        [0, 1, 2, 3, 4]
        >>> d = ConnectionLength.create_test()
        >>> b = ConnectionLength.merged(c, d)
        >>> b.parts
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
        >>> b
        ConnectionLength([[  1.        ,   0.        ,   0.97438334],
                          [  0.        ,   1.        ,   0.9579201 ],
                          [-80.        ,   1.        ,   1.9573    ],
                          [-80.        ,  -1.        ,   0.22222222],
                          [  0.        ,  -1.        ,   0.9579201 ],
                          [  1.        ,   0.        ,   0.97438334],
                          [  0.        ,   1.        ,   0.9579201 ],
                          [-80.        ,   1.        ,   1.9573    ],
                          [-80.        ,  -1.        ,   0.22222222],
                          [  0.        ,  -1.        ,   0.9579201 ]])
        >>> assert len(b.lengths) == 10
        >>> b.lengths[:4]
        [899.895318339, 2826.55635289, 2.55635289, 222.822222339]
        >>> b.elements
        [44301, 20291, 2, 22222, 20291, 44301, 20291, 2, 22222, 20291]
        >>> len(b)
        10

        Retrieving Groups for all the components
        >>> b.mm_ids = [15, 16, 17, 18, 19]
        >>> assert b.hits(15).equal([[ 1.,  0.,  0.97438334],
        ...                          [ 1.,  0.,  0.97438334]],
        ...                         atol=1e-6, rtol=1e-6)
        >>> p = b.hits(18)
        >>> p.to_segment_one()
        >>> assert p.equal([[ 65.3091448 , -46.21380319, 0.22222222],
        ...                 [ 65.3091448 , -46.21380319, 0.22222222]],
        ...                atol=1e-6, rtol=1e-6)

        Saving and loading like in Points3D
        >>> from tempfile import NamedTemporaryFile
        >>> outFile = NamedTemporaryFile(suffix='.npz')
        >>> c.save(outFile.name)
        >>> _ = outFile.seek(0)
        >>> c1 = ConnectionLength.load(outFile.name)
        >>> assert np.all(c == c1)
        >>> assert np.array_equal(c.parts, [0, 1, 2, 3, 4])
        >>> assert np.array_equal(c.parts, c1.parts)

    """

    __slots__ = ["coord_sys", "name", "parts", "elements", "lengths", "mm_ids"]
    __slot_setters__ = [
        tfields.bases.get_coord_system_name,
        None,
        None,
        None,
        None,
        "_set_mm_ids",
    ]

    def __new__(cls, tensors, **kwargs):
        # TODO(@dboe): this should be unneccesarry if u just use a field, idiot
        if isinstance(tensors, list):
            if w7x.is_w7x_instance(tensors, cls.get_ws_class()) or all(
                [
                    hasattr(con, attr)
                    for con in tensors
                    for attr in ["x", "y", "z", "length", "part", "element"]
                ]
            ):
                points = []
                parts = []
                elements = []
                lengths = []
                for con in tensors:
                    points.append([con.x, con.y, con.z])
                    lengths.append(con.length)
                    parts.append(con.part)
                    elements.append(con.element)
                tensors = points
                kwargs["parts"] = parts
                kwargs["elements"] = elements
                kwargs["lengths"] = lengths

        parts = kwargs.pop("parts", None)
        elements = kwargs.pop("elements", None)
        lengths = kwargs.pop("lengths", None)
        _mm_ids = kwargs.pop("_mm_ids", None)

        if issubclass(type(tensors), ConnectionLength):
            parts = parts or tensors.parts
            elements = elements or tensors.elements
            lengths = lengths or tensors.lengths
            _mm_ids = _mm_ids or tensors._mm_ids

        obj = super(ConnectionLength, cls).__new__(cls, tensors, **kwargs)
        obj.parts = parts
        obj.elements = elements
        obj.lengths = lengths
        obj._mm_ids = _mm_ids
        return obj

    @classmethod
    def merged(cls, *objects, **kwargs):
        """
        Overload merged for taking care of parts, elements and lenghts
            atrributes
        """
        if not all([isinstance(o, cls) for o in objects]):
            # TODO: could allow if all faceScalars are none
            raise TypeError(
                "Merge constructor only accepts {cls} instances.".format(**locals())
            )

        inst = super(ConnectionLength, cls).merged(*objects, **kwargs)

        kwargs["parts"] = kwargs.pop(
            "parts",
            functools.reduce(lambda x, y: x + y, [obj.parts for obj in objects]),
        )
        kwargs["elements"] = kwargs.pop(
            "elements",
            functools.reduce(lambda x, y: x + y, [obj.elements for obj in objects]),
        )
        kwargs["lengths"] = kwargs.pop(
            "lengths",
            functools.reduce(lambda x, y: x + y, [obj.lengths for obj in objects]),
        )
        inst = cls.__new__(cls, inst, **kwargs)
        return inst

    @classmethod
    def create_test(cls):
        """
        Create a test class filled with some data.
        """

        class Mock:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        a = []
        a.append(
            Mock(
                length=899.895318339,
                x=1.0,
                y=0,
                z=0.974383343584,
                part=0,
                element=44301,
            )
        )
        a.append(
            Mock(length=2826.55635289, x=0, y=1, z=0.95792010423, part=1, element=20291)
        )
        a.append(Mock(length=2.55635289, x=-80, y=1, z=1.9573, part=2, element=2))
        a.append(
            Mock(
                length=222.822222339,
                x=-80,
                y=-1,
                z=0.222222222224,
                part=3,
                element=22222,
            )
        )
        a.append(
            Mock(
                length=2826.55635289, x=0, y=-1, z=0.95792010423, part=4, element=20291
            )
        )
        obj = cls(a)
        obj.mm_ids = list(range(5))
        return obj

    def _set_mm_ids(self, mm_ids):
        """
        slot setter for mm_ids
        """
        if self.parts is not None and mm_ids is not None:
            if max([p if p is not None else 0 for p in self.parts]) >= len(mm_ids):
                raise ValueError("Too many parts for the mm_ids given.")
        return mm_ids

    def hits(self, *mm_ids):
        """
        return the hit points of the field lines on the components of the
        connection Results for the given mm_ids.

        Returns:
            Points3D
        """
        mm_ids = set(mm_ids)
        mask = []
        for part in self.parts:
            if part < 0:  # All invalid parts get False, rest True
                mask.append(False)
            elif self.mm_ids[part] not in mm_ids:
                mask.append(False)
            else:
                mask.append(True)
        points = Points3D(self[mask])
        return points

    def meshed_models(self, mm_ids=None):
        """
        Returns:
            List(MeshedModel)
        """
        if mm_ids is None:
            mm_ids = self.mm_ids
        elif not set(mm_ids).issubset(self.mm_ids):
            raise ValueError("mm_ids must be subset of self.mm_ids.")

        meshed_models = []
        for mm_id in mm_ids:
            meshed_models.append(MeshedModel.from_mm_id(mm_id))
        return meshed_models

    def parts_mm_id(self):
        """
        Returns:
            List(int): meshed model ids of terminating parts
        """
        return [self.mm_ids[part] for part in self.parts]


class ComponentLoad:
    """
    Collection class for flt.ComponentLoad instances
    Provides methods for choosing specific components only

    Note:
        This class intentioanlly breaks the concept of Base class wrappers
        because the ComponentLoad class is too fine grained and not storage
        efficient

    Args:
        *component_load (webservice ComponentLoad):
            e.g.:
                (ComponentLoad){
                    id = 0
                    events = 1
                    elements[] = [
                                  (ElementLoad){
                                      id = 103638
                                      events = 1
                                      area = 0.000175667334795
                                  }
                                  ]
                }

    Examples:
        >>> import w7x
        >>> l = w7x.flt.ComponentLoad.create_test()
        >>> l.load_dict()[181]['events'] == [1, 42, 1]
        True

    """

    def __init__(self, component_load, mm_ids=None):
        self._component_id_dict = {}
        self._mm_ids = mm_ids
        for obj in component_load:
            if obj.id not in self._component_id_dict:
                self._component_id_dict[obj.id] = {}
            for element in obj.elements:
                if element.id not in self._component_id_dict[obj.id]:
                    self._component_id_dict[obj.id][element.id] = element.events
                else:
                    self._component_id_dict[obj.id][element.id] += element.events

    @property
    def mm_ids(self):
        """
        database IDs from ComponentsDB
        """
        return self._mm_ids

    @mm_ids.setter
    def mm_ids(self, mm_ids):
        self._mm_ids = mm_ids

    def _get_element_ids(self, component_id):
        return sorted(self._component_id_dict[component_id].keys())

    def _get_element_events(self, component_id):
        return [
            self._component_id_dict[component_id][eId]
            for eId in self._get_element_ids(component_id)
        ]

    def save(self, path):
        """
        Examples:
            >>> import w7x
            >>> from tempfile import NamedTemporaryFile
            >>> outFile = NamedTemporaryFile(suffix='.npz')
            >>> l = w7x.flt.ComponentLoad.create_test()
            >>> l.save(outFile.name)
            >>> _ = outFile.seek(0)
            >>> l1 = w7x.flt.ComponentLoad.load(outFile.name)
            >>> assert l.mm_ids == l1.mm_ids
            >>> assert l1.load_dict()[181]['events'] == [1, 42, 1]
        """
        if not path.endswith(".npz"):
            raise NotImplementedError(path)
        np.savez(
            rna.path.resolve(path),
            _component_id_dict=self._component_id_dict,
            _mm_ids=self._mm_ids,
        )

    @classmethod
    def load(cls, path):
        """
        See save
        """
        obj = cls([])
        with np.load(rna.path.resolve(path), allow_pickle=True) as data:
            obj._component_id_dict = data["_component_id_dict"].tolist()
            obj._mm_ids = data["_mm_ids"].tolist()
        return obj

    def load_dict(self):
        """
        Returns:
            dictionary with following structure:
                {<mm_id>: {'elementIds': <list of ids of elements/triangles>,
                           'events': <list with the number of occuring events
                                corresponding to an element/triangle>},
                 <mm_id2>: ...}
        """
        mm_id_load_dict = {}
        if self.mm_ids is None:
            raise ValueError("Please set mm_ids before.")
        for component_id in sorted(self._component_id_dict.keys()):
            mm_id_load_dict[self.mm_ids[component_id]] = {
                "elementIds": self._get_element_ids(component_id),
                "events": self._get_element_events(component_id),
            }
        return mm_id_load_dict

    def as_mesh3d_list(self, *sub_mm_ids):
        """
        Args:
            sub_mm_ids: subset of self.mm_ids of interest
            p_conv (float | None): if float, return heat load instead of n_hits

        Returns:
            List(Mesh3D): meshes have two fields:
                index 0: number of hits on triangle
                index 1: number of hits per triangle area
        """
        # assign subset of mm_ids
        mm_ids = self.mm_ids
        comp_ids = list(range(len(mm_ids)))
        if sub_mm_ids:
            mm_ids = []
            comp_ids = []
            for sub_mm_id in sub_mm_ids:
                mm_ids.append(sub_mm_id)
                comp_ids.append(self.mm_ids.index(sub_mm_id))

        # collect meshes and n_hits
        meshes = []
        for comp_id, mm_id in zip(comp_ids, mm_ids):
            mesh = MeshedModel.mesh3d(mm_id)

            # n_hits_field
            n_hits_field = tfields.Tensors(np.zeros(len(mesh.faces)))
            if comp_id in self._component_id_dict:
                for e_id, e_events in self._component_id_dict[comp_id].items():
                    n_hits_field[e_id] = e_events
            mesh.faces.fields.append(n_hits_field)

            # n_hits_per_area_field
            # TODO: calculation of the area is rather slow.
            #   Options:
            #       1: cash areas like MeshedModel.mesh3D (MeshedModel.areas)
            #       2: cash triangles3d when cashing mesh3D
            #       3: __getitem__ magic problem with areas? This is too slow
            n_hits_per_area_field = tfields.Tensors(
                n_hits_field / mesh.triangles().areas()
            )
            mesh.faces.fields.append(n_hits_per_area_field)
            meshes.append(mesh)

        return meshes

    @classmethod
    def create_test(cls):
        """
        Create a test class filled with some data.
        """

        class Mock:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        objs = []
        objs.append(
            Mock(
                id=0,
                events=3,
                elements=[
                    Mock(id=103638, events=1, area=0.00017),
                    Mock(id=123456, events=1, area=0.00017),
                    Mock(id=134679, events=1, area=0.00017),
                ],
            )
        )
        objs.append(
            Mock(id=3, events=21, elements=[Mock(id=123, events=21, area=0.00017)])
        )
        objs.append(
            Mock(id=0, events=41, elements=[Mock(id=123456, events=41, area=0.00017)])
        )
        mm_ids = [181, 182, 183, 184, 185]
        return cls(objs, mm_ids)


def interprete_mm_id(mm_id):
    """
    Examples:
        >>> from w7x.flt import interprete_mm_id

        mm_id defined in web service
        >>> interprete_mm_id(30)
        (30, None)

        mm_id derived from web service
        >>> interprete_mm_id(420000030)
        (30, 42)

        Own independent mm_id
        >>> interprete_mm_id(421000000)
        (None, 42)

        Own independent mm_id
        >>> interprete_mm_id(1000)
        (None, 1000)

    Returns:
        tuple with 2 arguments:
            1) ws_mm_id (int or None): mm_id from web service
                if derived from web service definition
            2) own_mm_id (int or None): user defined id

    """
    ws_mm_id = None
    own_mm_id = None
    if mm_id < 1e6:
        if mm_id < 1e3:
            ws_mm_id = mm_id
        else:
            own_mm_id = mm_id
    else:
        head_tmp = mm_id // int(1e6)
        head = head_tmp // 10
        mid = head_tmp - head * 10
        tail = mm_id - head_tmp * int(1e6)

        if mid == 1:
            # not derived
            if tail != 0:
                raise ValueError(
                    "If mid index is 1, The mm_id"
                    "should not be derived by definition!"
                )
        elif mid == 0:
            ws_mm_id = tail
        else:
            raise ValueError("Mid digit must be either 1 or 0.")
        own_mm_id = head

    return ws_mm_id, own_mm_id


def component_module(mm_id):
    """
    Returns:
        int: which module the geometry is in
    """
    comp_db_server = w7x.get_server(w7x.Server.addr_components_db)
    if mm_id >= 1000:
        mm_id = int(mm_id / 1000)
    componentInfo = comp_db_server.service.getComponentInfo(mm_id)[0]
    return int(componentInfo.location.replace("m ", ""))


class LCFSSettings(Base):
    prop_defaults = {
        "LCFSLeftX": None,
        "LCFSRightX": None,
        "LCFSNumPoints": 40,
        "LCFSThreshold": 1000.0,
        "LCFSAccuracy": 0.001,
    }
    prop_order = ["LCFSLeftX", "LCFSRightX"]


class CylindricalGrid(Base):
    """
    Order of grid in the ws is
    for phi
        for r
            for z
    """

    prop_defaults = {
        "RMin": w7x.Defaults.CylindricalGrid.RMin,
        "RMax": w7x.Defaults.CylindricalGrid.RMax,
        "ZMin": w7x.Defaults.CylindricalGrid.ZMin,
        "ZMax": w7x.Defaults.CylindricalGrid.ZMax,
        "numR": w7x.Defaults.CylindricalGrid.numR,
        "numZ": w7x.Defaults.CylindricalGrid.numZ,
        "numPhi": w7x.Defaults.CylindricalGrid.numPhi,
        "PhiMin": w7x.Defaults.CylindricalGrid.PhiMin,
        "PhiMax": w7x.Defaults.CylindricalGrid.PhiMax,
    }


class CartesianGrid(Base):
    """
    Order of grid in the ws is
    for phi
        for r
            for z
    """

    prop_defaults = {
        "numX": w7x.Defaults.CartesianGrid.numX,
        "numY": w7x.Defaults.CartesianGrid.numY,
        "numZ": w7x.Defaults.CartesianGrid.numZ,
        "ZMin": w7x.Defaults.CartesianGrid.ZMin,
        "ZMax": w7x.Defaults.CartesianGrid.ZMax,
        "XMin": w7x.Defaults.CartesianGrid.XMin,
        "XMax": w7x.Defaults.CartesianGrid.XMax,
        "YMin": w7x.Defaults.CartesianGrid.YMin,
        "YMax": w7x.Defaults.CartesianGrid.YMax,
    }


class Grid(Base):
    """
    see http://webservices.ipp-hgw.mpg.de/docs/fieldlinetracer.html#Grid
    Examples:
        >>> import w7x
        >>> cyl = w7x.flt.CylindricalGrid(numPhi=49)
        >>> afsFilePath = "/fieldline/w7x/field_mfbe181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.dboe_01.v_00_pres_00_it_12.dat"  # noqa
        >>> grid = w7x.flt.Grid(cylindrical=cyl, afsFileName=afsFilePath)
        >>> grid.as_input()  # noqa
        (Grid){
            cylindrical = (CylindricalGrid){
                              RMin = 4.05
                              RMax = 6.75
                              ZMin = -1.35
                              ZMax = 1.35
                              numR = 181
                              numZ = 181
                              PhiMin = None (float)
                              PhiMax = None (float)
                              numPhi = 49
                          }
            hybrid = None (CylindricalGrid)
            afsFileName = /fieldline/w7x/field_mfbe181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.dboe_01.v_00_pres_00_it_12.dat
            gridField = None (Points3D)
            fieldSymmetry = 5
        }

    """

    prop_defaults = {
        "cylindrical": None,
        "hybrid": None,
        "afsFileName": None,
        "gridField": None,
        "fieldSymmetry": w7x.Defaults.fieldSymmetry,
    }

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        """
        Do not use the hybrid unless you know what you are doing
        """
        if self.hybrid is not None:
            raise AttributeError("You should not use the hybrid grid.")
        if self.cylindrical is None:
            self.cylindrical = CylindricalGrid()


class Machine(Base):
    """
    Object to closely lie above web service Machine object
    Examples:
        >>> from w7x.flt import Machine, CartesianGrid
        >>> a = Machine(meshedModelsIds=w7x.MeshedModelsIds.divertor,
        ...             grid=CartesianGrid())
        >>> a.as_input()
        (Machine){
            meshedModels[] = [
        <BLANKLINE>
                              ]
            meshedModelsIds[] = [
                                 165,
                                 166,
                                 167,
                                 168,
                                 169
                                 ]
            assemblyIds[] = None (int)
            grid = (CartesianGrid){
                       XMin = -7
                       XMax = 7
                       YMin = -7
                       YMax = 7
                       ZMin = -1.5
                       ZMax = 1.5
                       numX = 500
                       numY = 500
                       numZ = 100
                   }
        }

    """

    prop_defaults = {
        "meshedModels": None,
        "meshedModelsIds": None,
        "assemblyIds": None,
        "grid": None,
    }
    ws_class_args = [1]

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args (int | Mesh3D | str):
                int -> mm_ids
                Mesh3D | str -> MeshedModel
                str -> component name
        """
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        if len(args) == 1 and w7x.is_w7x_instance(args[0], self.get_ws_class()):
            # copy constructor
            pass
        elif len(args) > 0:
            raise DeprecationWarning("args only supported for copy constructor")

        meshed_models = kwargs.pop("meshedModels", [])
        for i in range(len(meshed_models)):
            mm = meshed_models[i]
            if issubclass(type(mm), tfields.Mesh3D):
                meshed_models[i] = MeshedModel(mm)
            if not isinstance(meshed_models[i], MeshedModel):
                raise ValueError("meshed model of wrong type {0}".format(type(mm)))
        mm_ids_db = []
        mm_ids_user = []
        mm_ids = kwargs.pop("meshedModelsIds", [])
        for mm_id in mm_ids:
            ws_mm_id, own_mm_id = interprete_mm_id(mm_id)
            if own_mm_id is None:
                mm_ids_db.append(mm_id)
            else:
                mm_ids_user.append(mm_id)
        if len(meshed_models) != 0:
            if len(mm_ids_user) == 0:
                mm_ids_user = [1000 + i for i in range(len(meshed_models))]
            else:
                if len(mm_ids_user) != len(meshed_models):
                    raise ValueError("len(meshed_models) != len(mm_ids_user)")
        elif len(mm_ids_user) != 0:
            raise ValueError("len(meshed_models) != len(mm_ids_user)")

        kwargs["meshedModels"] = meshed_models
        kwargs["meshedModelsIds"] = mm_ids_db
        kwargs["grid"] = kwargs.pop("grid", CartesianGrid())
        super(Machine, self).__init__(**kwargs)
        self._mm_ids_user = mm_ids_user

    @classmethod
    def default(cls):
        return cls.from_mm_ids(*w7x.Defaults.Machine.mm_ids)

    @classmethod
    def from_mm_ids(cls, *mm_ids, **kwargs):
        grid = CartesianGrid()
        return cls(grid=grid, meshedModelsIds=w7x.GeoSet(mm_ids))

    def get_mm_ids(self, user_defined=True, pre_defined=True):
        """
        Args:
            user_defined (bool): return mm_ids, defined by yourself (mm_id >= 1000)?
            pre_defined (bool): return mm_ids, defined by ws?
        """
        if pre_defined:
            mm_ids_db = self.meshedModelsIds or []
        else:
            mm_ids_db = []
        if user_defined:
            mm_ids_user = self._mm_ids_user
        else:
            mm_ids_user = []
        return mm_ids_user + mm_ids_db
        # pre_defined_mm_ids = []
        # user_defined_mm_ids = []
        # for mm_id in self.meshedModelsIds:
        #     if mm_id < 1000:
        #         if pre_defined:
        #             pre_defined_mm_ids.append(mm_id)
        #     else:
        #         if user_defined:
        #             user_defined_mm_ids.append(mm_id)
        # return tfields.lib.util.flatten(user_defined_mm_ids + pre_defined_mm_ids)

    @property
    def mm_ids(self):
        """
        database IDs from ComponentsDB
        """
        return self.get_mm_ids()

    @mm_ids.setter
    def mm_ids(self, mm_ids):
        self.meshedModelsIds = mm_ids

    def meshed_models(self, user_defined=True, pre_defined=False, geoFileDir=None):
        """
        Args:
            user_defined (bool): return MeshedModels, defined by yourself (mm_id >= 1000)?
            pre_defined (bool): return MeshedModels, defined by ws?
        """
        meshed_models = []
        # go through user_defined mm_ids
        for mm_id in self.get_mm_ids(user_defined=user_defined, pre_defined=False):
            geoFilePath = os.path.join(geoFileDir, "mm_id_{0}.obj".format(mm_id))
            meshed_model = MeshedModel.load(geoFilePath).as_input()
            meshed_models.append(meshed_model)

        # go through pre_defined mm_ids
        comp_db_server = w7x.get_server(w7x.Server.addr_components_db)
        for mm_id in self.get_mm_ids(user_defined=False, pre_defined=pre_defined):
            meshed_model = MeshedModel(
                comp_db_server.service.getComponentData(mm_id)[0]
            )
            meshed_models.append(meshed_model)
        return meshed_models

    def as_mesh3d_list(self, user_defined=True, pre_defined=True):
        return [
            m.as_mesh3d()
            for m in self.meshed_models(
                user_defined=user_defined, pre_defined=pre_defined
            )
        ]

    def plot_poincare(self, phi=0, **kwargs):
        inters = self.intersect_mesh_phi_planes([phi])
        artists = []
        for mm_id, geoPoints in zip(self.mm_ids, inters[0]):
            geoSet = w7x.get_geo_set(mm_id)
            color = geoSet.color if geoSet else w7x.Defaults.Poincare.geometry_color
            plotKwargs = {"color": color, "method": "plot", "lw": 1}
            plotKwargs.update(kwargs)
            artists.append(w7x.plot_poincare_surfaces(geoPoints, **plotKwargs))
        return artists

    def intersect_mesh_phi_planes(self, phi_list_rad):
        """Get poincare points for a set of mm_ids and phis
        with intersectMeshPhiPlane service from the Mesh server web service.

        Args:
            phi_list_rad (list of floats): list of phi in rad
        Returns:
            phi_container (list[list[Points3D for each vertex] for each mm_id] for each phi)
        Raises:

        Examples:
            >>> import w7x
            >>> machine = w7x.flt.Machine.from_mm_ids(165, 166)
            >>> res = machine.intersect_mesh_phi_planes([0.0, 0.34, 6 * 0.34])
            >>> assert res[0][0][0].equal([[ 5.74323774,  0.,  0.98876001],
            ...                            [ 5.7433343 ,  0.,  0.98801955]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[0][0][1].equal([[ 5.74201939,  0.,  0.99807376],
            ...                            [ 5.74099873,  0.,  1.00585009]],
            ...                           atol=1e-6, rtol=1e-6)

            >>> res = machine.intersect_mesh_phi_planes([0.0,  5*0.31])
            >>> assert res[0][0][0].equal([[5.74323774, 0., 0.98876001],
            ...                            [5.7433343 , 0., 0.98801955]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[0][0][1].equal([[ 5.74201939, 0.,  0.99807376],
            ...                            [ 5.74099873, 0.,  1.00585009]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[1][1][0].equal([[ 6.07343869, 1.55, -0.68684114],
            ...                            [ 6.07343617, 1.55, -0.68893482]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[1][1][1].equal([[ 6.07340735, 1.55, -0.70596002],
            ...                            [ 6.07343617, 1.55, -0.68893482]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> len(machine.mm_ids) == len(res[0])
            True

        """
        # Check input
        if not type(phi_list_rad) is list:
            raise TypeError(
                "phi_list_rad has to be of type list but is of type {}".format(
                    type(phi_list_rad)
                )
            )

        if len(phi_list_rad) == 0:
            return []

        mesh_server = w7x.get_server(w7x.Server.addr_mesh_server)

        # Run intersectMeshPhiPlane service for each phi AND mm_id
        phi_container = []
        for iPhi, phi in rna.log.progressbar(
            zip(range(len(phi_list_rad)), phi_list_rad)
        ):
            mm_id_container = []
            for mm_id in self.mm_ids:
                poincare_points_list = []
                # Set up mesh set
                mesh_set = mesh_server.types.SurfaceMeshSet()
                wrap = mesh_server.types.SurfaceMeshWrap()
                reference = mesh_server.types.DataReference()
                reference.dataId = "10"
                wrap.reference = reference
                mesh_set.meshes = [
                    wrap,
                ]

                # append mm_id_wrap
                mm_id_wrap = mesh_server.types.SurfaceMeshWrap()
                mm_id_reference = mesh_server.types.DataReference()
                mm_id_reference.dataId = str(mm_id)
                mm_id_wrap.reference = mm_id_reference
                mesh_set.meshes.append(mm_id_wrap)

                # ask web service for result and process it to right format
                # careful: Returns None if there is no component.
                res = mesh_server.service.intersectMeshPhiPlane(phi, mesh_set)

                if type(res) is list:
                    if res[0] is None:
                        return []
                    elif (
                        str(type(res[0]))
                        == "<class 'osa.xmltypes.PolygonPlaneIntersection'>"
                    ):
                        # Result is from MeshPhiIntersection
                        for intersection in res:
                            # res.surfs has entries for every phi
                            vertex_points = Points3D(
                                intersection.vertices, coord_sys=tfields.bases.CARTESIAN
                            )
                            vertex_points.transform(tfields.bases.CYLINDER)
                            # phi is correct with rounding precision before.
                            # This way it is perfectly correct
                            vertex_points[:, 1].fill(phi)
                            poincare_points_list.append(vertex_points)
                    else:
                        logging.error("Can not handle result list content.")
                elif res is None:
                    logging.debug(
                        "Result was None. Probably there was no"
                        "intersection of the mesh with this plane."
                    )
                else:
                    logging.error("Result is not of the right type")

                mm_id_container.append(poincare_points_list)
            phi_container.append(mm_id_container)
        return phi_container


class MagneticConfig(Base):
    """
    Object to closely lie above web service MagneticConfig object
    Examples:
        >>> import w7x
        >>> datFileName=w7x.Defaults.Paths.test_dat_file
        >>> cyl = w7x.flt.CylindricalGrid(numR=60, numPhi=101, numZ=10)
        >>> grid = w7x.flt.Grid(cylindrical=cyl)
        >>> m = w7x.flt.MagneticConfig.from_dat_file(datFileName, grid=grid)
        >>> flsType = m.as_input()
        >>> flsType  # noqa doctest: +ELLIPSIS
        (MagneticConfig){
            coils[] = None (PolygonFilament)
            coilsCurrents[] = None (float)
            coilsIds[] = None (int)
            coilsIdsCurrents[] = None (float)
            configIds[] = None (int)
            grid = (Grid){
                       cylindrical = (CylindricalGrid){
                                         RMin = 4.05
                                         RMax = 6.75
                                         ZMin = -1.35
                                         ZMax = 1.35
                                         numR = 60
                                         numZ = 10
                                         PhiMin = None (float)
                                         PhiMax = None (float)
                                         numPhi = 101
                                     }
                       hybrid = None (CylindricalGrid)
                       afsFileName = /fieldline/w7x/field_mfbe181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.dboe_01.v_00_pres_00_it_12.dat
                       gridField = None (Points3D)
                       fieldSymmetry = 5
                   }
            inverseField = None (bool)
        }

    """

    prop_defaults = {
        "coils": None,
        "coilsCurrents": None,
        "coilsIds": None,
        "coilsIdsCurrents": None,
        "configIds": None,
        "grid": None,
        "inverseField": None,
    }

    @classmethod
    def default(cls):
        """
        Standard case with ideal coils
        """
        return cls.from_currents()

    @classmethod
    def from_id(cls, config_id, **kwargs):
        kwargs["configIds"] = [config_id]
        return cls(**kwargs)

    @classmethod
    def from_currents(cls, *currents, **kwargs):
        """
        Factory method for vacuum magnetic field construction with biot-savart.

        Args:
            *currents (float):
                first 5 currents -> non planar currents
                optional:
                    next 2 currents -> planar currents
                    next 2 | 10 currents -> sweep coil currents
                        If 2 currents are given, assume equal current drive
                        in all upper and lower sweep coils respectively
                    next 5 -> trim coils
            **kwargs:
                unit (str):
                    The currents given have the unit Aw like in the web service
                    input for magnetic configs (see coil_currents method
                    docstring)
                scale (float): For all relative units ('rw', 'r'), the 'scale'
                    attribute is active. The default is
                    w7x.Defaults.MagneticConfig.n_windings_npcs in 'rw'
                coilsIds: specify the coils by picking their ids from the
                    database.
                    NOTE: The order of the coils is not arbitrary. The coil ids
                        have to be given in the order:
                            1. 50 non planar coils NPC1-NPC5,NPC1-NPC5,...
                            2. 20 planar coils PCA,PCB,PCA,PCB,...
                            3. 10 sweep coils in the order of the half modules
                                (hm10, hm11,...)
                        Some coils_ids are already compiled into a list in
                        w7x.Defaults.MagneticConfig.coilsIds

        Examples:
            >>> import w7x

            Build a low iota configuration from relative winding currents
            >>> m = w7x.flt.MagneticConfig.from_currents(
            ...     1, 1, 1, 1, 1, -0.23, -0.23, 0.001, 0.001,
            ...     unit='rw')

            Build the same config with any other unit combination
            >>> units = ['rw', 'r', 'Aw', 'A']
            >>> for unit in units:
            ...     m_tmp = w7x.flt.MagneticConfig.from_currents(
            ...         *m.coil_currents(unit=unit),
            ...         unit=unit, scale=None)

            or with pre-defined configurations
            >>> m_alternative = w7x.flt.MagneticConfig.from_currents(
            ...     *w7x.config.Defaults.MagneticConfig.low_iota_rw,
            ...     unit='rw')

        """
        unit = kwargs.pop("unit", "rw")
        scale = kwargs.pop("scale", None)
        if scale is None:
            if unit == "rw":
                scale = w7x.Defaults.MagneticConfig.scale
            elif unit == "r" and scale is None:
                scale = (
                    w7x.Defaults.MagneticConfig.scale
                    / w7x.Defaults.MagneticConfig.n_windings_npcs
                )
            else:
                scale = 1.0
        if "r" not in unit and scale != 1:
            raise ValueError("Scale given for absolute currents.")
        if "coilsIdsCurrents" in kwargs:
            raise ValueError("Conflict between coilsIdsCurrents and currents")
        kwargs.setdefault("coilsIds", w7x.Defaults.MagneticConfig.coilsIds)

        if len(currents) == 1 and hasattr(currents[0], "__iter__"):
            logging.warning("Passed iterable instead of single values")
            currents = currents[0]
        if len(currents) < 14:
            currents = list(currents)
            if len(currents) < 5:
                if unit == "rw":
                    # standard case if no currents given
                    currents = currents + [1.0] * (5 - len(currents))
                else:
                    raise ValueError(
                        "For all units except 'rw' we expect"
                        " at least the planar coil currents"
                    )
            # TODO The following is dangerous in case default is changed
            currents = currents + [0.0] * (14 - len(currents))

        """
        convert to Aw
        """
        currents = np.array(currents, dtype=float)
        currents = currents * scale

        """
        Transform symmetric currents
        """
        currents = list(currents)

        # only partial currents given
        if len(currents) in (5, 7, 9):
            currents = currents + [0.0] * (14 - len(currents))
        plcs = currents[:5] * 10  # non planar coils
        npcs = currents[5:7] * 10  # planar coils
        if len(currents) == 14:
            # stellarator symmetric sweep coils
            scs = currents[7:9] * 5  # sweep coils
            tcs = currents[9:]  # trim coils
        elif len(currents) == 22:
            # 10 sweep, 2 trim coils
            scs = currents[7:17]  # sweep coils
            tcs = currents[17:]  # trim coils
        else:
            raise ValueError(len(currents))

        currents = plcs + npcs + scs + tcs

        n_total_expected = 85  # yes, that looks hardcoded but is a constant
        if not len(kwargs["coilsIds"]) == len(currents) == n_total_expected:
            raise ValueError(
                "#Coils: {0}, \t#Currents: {1}, \texpected: {2}".format(
                    len(kwargs["coilsIds"]), len(currents), n_total_expected
                )
            )

        """
        Multiply by winding number for 'winding' units
        """
        if "w" not in unit:
            currents = np.array(currents)
            currents[:50] *= w7x.Defaults.MagneticConfig.n_windings_npcs
            currents[50:70] *= w7x.Defaults.MagneticConfig.n_windings_plcs
            currents[70:80] *= w7x.Defaults.MagneticConfig.n_windings_scs
            currents[80] *= w7x.Defaults.MagneticConfig.n_windings_tcs_a
            currents[81:82] *= w7x.Defaults.MagneticConfig.n_windings_tcs_b
            currents[82:] *= w7x.Defaults.MagneticConfig.n_windings_tcs_a
            currents = list(currents)

        kwargs["coilsIdsCurrents"] = currents

        # NOTE: tests if removing coilsIds with current 0 would speed things up
        #   were performed. Preliminary outcome: if at all a minor effect.
        return cls(**kwargs)

    @classmethod
    def from_afs_file(cls, file_path, **kwargs):
        """
        set AFS BField file
        Args:
            file_path (str): afs file path
            **kwargs: forwarded to constructor of cls

        """
        if "grid" not in kwargs:
            raise AttributeError("Please specify a grid.")
        # create Grid with afsFileName and hybrid grid if existing.
        kwargs["grid"] = kwargs.pop("grid", Grid())
        # check that file is afs file
        if file_path.startswith(w7x.Defaults.Paths.tracer_network_share):
            file_path = file_path.lstrip(w7x.Defaults.Paths.tracer_network_share)
        if not file_path.startswith("/"):
            file_path = "/" + file_path
        if not file_path.startswith(
            "/" + w7x.Defaults.Paths.tracer_network_share_relative_path.split("/")[0]
        ):
            raise TypeError("File must be shared on network drive.")
        kwargs["grid"].afsFileName = file_path

        return cls(**kwargs)

    @classmethod
    def from_dat_file(
        cls,
        file_path_dat,
        network_share=w7x.Defaults.Paths.tracer_network_share,
        network_share_mount=w7x.Defaults.Paths.tracer_network_share_mount,  # NOQA
        network_share_workgroup=w7x.Defaults.Paths.tracer_network_share_workgroup,  # NOQA
        network_share_relative_path=w7x.Defaults.Paths.tracer_network_share_relative_path,  # NOQA
        **kwargs
    ):
        """
        Copy file to afs and return the instance with afsFile
        Args:
            see from_afs_file and __init__
        Examples:
            >>> import w7x
            >>> datFileName=w7x.Defaults.Paths.test_dat_file
            >>> cyl = w7x.flt.CylindricalGrid(numR=60, numPhi=101, numZ=10)
            >>> grid = w7x.flt.Grid(cylindrical=cyl)
            >>> m = w7x.flt.MagneticConfig.from_dat_file(datFileName, grid=grid)

        """
        file_path_dat = rna.path.resolve(file_path_dat)
        if file_path_dat.startswith(network_share):
            logging.warning(
                "Passing network share path to 'from_dat_file'."
                " Consider using 'from_afs_file'"
            )
            network_file_path_dat = file_path_dat
        else:
            network_file_path_dat = rna.path.resolve(
                network_share,
                network_share_relative_path,
                os.path.basename(file_path_dat),
            )

        # locally mounted?
        local_mount_file_path_dat = ""
        if os.name == "nt":
            local_mount_file_path_dat = network_file_path_dat
        if os.name == "posix":
            if os.path.exists(network_share_mount):
                local_mount_file_path_dat = rna.path.resolve(
                    network_share_mount,
                    network_share_relative_path,
                    os.path.basename(file_path_dat),
                )

        # copy if not existing
        if os.path.exists(local_mount_file_path_dat):
            # If file is on nas you have nothing to do
            file_already_exists_message = (
                "File {network_file_path_dat} is already existing. "
                "It is mounted as {local_mount_file_path_dat} ."
                "I will not copy."
            ).format(**locals())
            logging.info(file_already_exists_message)
        elif local_mount_file_path_dat:
            # Copy file to nas
            logging.info(
                "Copy {file_path_dat} to {local_mount_file_path_dat}".format(**locals())
            )
            rna.path.cp(file_path_dat, local_mount_file_path_dat)
        elif os.name == "posix":
            # Copy file to nas with smbclient.
            # Inspired by smbclient python package
            import subprocess

            logging.info(
                "Copy {file_path_dat} to {network_file_path_dat}".format(**locals())
            )
            remote_path = os.path.join(
                network_share_relative_path, os.path.basename(file_path_dat)
            )
            remote_path = remote_path.replace("/", "\\")  # nt compatible
            smbclient_cmd = [
                "smbclient",
                network_share.rstrip("/"),
                "-k",  # kerberos!
            ]
            smbclient_cmd = [x.encode("utf8") for x in smbclient_cmd]
            command_list = ["put"]
            command_list.extend(u'"%s"' % arg for arg in [file_path_dat, remote_path])
            command = u" ".join(command_list)
            cmd = smbclient_cmd + [b"-c", command.encode("utf8")]

            # retry because sambaclient is buggy
            n_tries = 10
            attempts = 0
            while attempts < n_tries:
                p = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                result = p.communicate()[0].rstrip().decode("utf8")
                if p.returncode != 0:
                    logging.warning(
                        u"Attempting to copy by smbclient failed. "
                        u"Number of attemps: {0} (cmd: {1})".format(
                            attempts, (b" ".join(cmd).decode("utf8"))
                        )
                    )
                    attempts += 1
                else:
                    break

            else:
                raise OSError(
                    u"Error on %r: %r" % (b" ".join(cmd).decode("utf8"), result)
                )

        return cls.from_afs_file(network_file_path_dat, **kwargs)

    def scale_currents(self, scale, unit="Aw"):
        """
        Scale the currents with scale
        """
        if self.coilsIdsCurrents is None:
            raise ValueError("No coil currents set yet.")
        if unit == "Aw":
            self.coilsIdsCurrents = [c * scale for c in self.coilsIdsCurrents]
        else:
            raise NotImplementedError(
                "Unit {unit} not implemented yet.".format(**locals())
            )

    def set_nominal_current(self, nominalCurrent, unit="Aw"):
        """
        Scale the currents to reach the nomianlCurrent
        """
        self.scale_currents(nominalCurrent / self.coilsCurrents[0], unit=unit)

    def coil_currents(self, unit="rw"):
        """
        Retrieve the coil currents (coilsIdsCurrents) in units of choice. This
        method is the opposite to tfields.MagneticConfig.from_currents.

        Args:
            unit (str): what spec
                'A': the current that is actually applied to the coil set
                'Aw': in A * winding number - the current that is applied if
                    there would be just 1 winding. Non planar coils have 108
                    windings each, planar coils, 36 and control coils 8
                    windings each. The trim coils have 46 or 72 windings,
                    depending on the coil type.
                'rw': 'Aw' normalized by (i.e. relative to - hence 'r') the
                    first non planar coil
                'r': 'A' normalized by (i.e. relative to - hence 'r') the first
                    non planar coil

        Examples:
            >>> from w7x import MagneticConfig
            >>> import numpy as np

            >>> m = MagneticConfig.from_currents(
            ...     1, 1, 1, 1, 1, 0.23, 0.23, 0, 0,
            ...     scale = 15000 * 108)
            >>> assert np.array_equal(
            ...     [round(x, 2) for x in m.coil_currents('rw')],
            ...      [1.0, 1.0, 1.0, 1.0, 1.0, 0.23, 0.23] + [0.0] * 7)
            >>> assert np.array_equal(
            ...     [round(x, 2) for x in m.coil_currents('r')],
            ...     [1.0, 1.0, 1.0, 1.0, 1.0, 0.69, 0.69] + [0.0] * 7)
            >>> assert np.array_equal(
            ...     [round(x) for x in m.coil_currents('Aw')],
            ...     [1620000.0, 1620000.0, 1620000.0, 1620000.0, 1620000.0,
            ...      372600.0, 372600.0] + [0.0] * 7)
            >>> assert np.array_equal([round(x) for x in m.coil_currents('A')],
            ...                       [15000.0, 15000.0, 15000.0, 15000.0,
            ...                        15000.0, 10350.0, 10350.0] + [0.0] * 7)

        """
        if unit == "r":
            currents = np.array(self.coil_currents("A"))
            currents = currents * 1.0 / currents[0]
            return currents

        npcs = self.coilsIdsCurrents[:5]
        plcs = self.coilsIdsCurrents[50:52]
        scs = self.coilsIdsCurrents[70:80]
        tcs = self.coilsIdsCurrents[80:]
        npcs = np.array(npcs)
        plcs = np.array(plcs)
        scs = np.array(scs)
        tcs = np.array(tcs)
        I_n = npcs[0]
        if (
            len(set(scs[[i for i in range(10) if i % 2 == 0]])) == 1
            and len(set(scs[[i for i in range(10) if i % 2 == 1]])) == 1
        ):
            # stellarator symmetric
            scs = scs[:2]

        if unit == "Aw":
            return list(npcs) + list(plcs) + list(scs) + list(tcs)
        if unit == "A":
            return (
                list(npcs * 1.0 / w7x.Defaults.MagneticConfig.n_windings_npcs)
                + list(plcs * 1.0 / w7x.Defaults.MagneticConfig.n_windings_plcs)
                + list(scs * 1.0 / w7x.Defaults.MagneticConfig.n_windings_scs)
                + list(tcs[:1] * 1.0 / w7x.Defaults.MagneticConfig.n_windings_tcs_a)
                + list(tcs[1:2] * 1.0 / w7x.Defaults.MagneticConfig.n_windings_tcs_b)
                + list(tcs[2:] * 1.0 / w7x.Defaults.MagneticConfig.n_windings_tcs_a)
            )
        if unit == "rw":
            return (
                list(npcs * 1.0 / I_n)
                + list(plcs * 1.0 / I_n)
                + list(scs * 1.0 / I_n)
                + list(tcs * 1.0 / I_n)
            )

        raise NotImplementedError(unit)

    def geiger_string(self):
        """
        Examples:
            >>> import w7x
            >>> w7x.MagneticConfig.default().geiger_string()
            '1000_1000_1000_1000_+0000_+0000'

        """
        return "{0:-04d}_{1:-04d}_{2:-04d}_{3:-04d}_{4:0=+5d}_{5:0=+5d}".format(
            *[int(x * 1000) for x in self.coil_currents()[1:8]]
        )

    def poincare_in_phi_plane(
        self, phi_list_rad, seeds=None, numPoints=300, errors=None
    ):
        """
        Calculate poincare points flux surface wise with field line tracer
        service from the web service.

        Args:
            phi_list_rad (list of floats): list of phi in rad
            seeds (PoincareSeeds): seeds object for initial points for field
            lines. Each seed in seeds will give a surface
            numPoints (int, optional): number of toroidal revolutions per
                seed = number of points per fluxSurface.

        Returns:
            list of w7x.Points3D instances: poincareFluxSurfaces.
            Each fluxSurface
                        ->length: number of seeds
                        ->meaning: it represents a closed flux surface
                        ->phi0 is attached to the object as a stamp

        Raises:

        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> config = MagneticConfig.default()
            >>> res = config.poincare_in_phi_plane(
            ...     [0.0, 2.0],
            ...     Points3D([[6.0, 0.0, 0.0]]), 3)
            >>> assert len(res) == 2
            >>> assert res[0].shape == (3, 3)
            >>> assert res[1].shape == (3, 3)
            >>> res2 = config.poincare_in_phi_plane(
            ...     [0.0, 2.0],
            ...     Points3D([[6.0, 0.0, 0.0]]), 1)
            >>> assert len(res2) == 2
            >>> assert res2[0].shape == (1, 3)
            >>> assert res2[1].shape == (1, 3)
            >>> res3 = config.poincare_in_phi_plane(
            ...     [2.0], Points3D([[6.0, 0.0, 0.0]]), 1)
            >>> assert len(res3) == 1
            >>> assert res3[0].shape == (1, 3)

        """
        if seeds is None:
            logging.info("No seeds given. I will build default seeds.")
            seeds = w7x.Defaults.Poincare.seeds

        seeds = Points3D(seeds)
        errors = errors or []

        if not numPoints > 0:
            raise ValueError("numPoints must be greater than 0")

        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)

        # Poincare Task
        task = field_line_server.types.Task()
        # parameter controling the accurancy of the calculation.
        task.step = w7x.Defaults.Poincare.stepSize
        task.poincare = field_line_server.types.PoincareInPhiPlane()
        task.poincare.numPoints = numPoints
        # list of phi in radians or just one phi.
        task.poincare.phi0 = phi_list_rad

        poincareFluxSurfaces = []
        nSuccess = 0
        nFailed = 0
        logging.info("Running through Seeds. Tracing each seed for all given phi.")
        for i_seed in range(len(seeds)):
            seed_point = seeds[i_seed : i_seed + 1]
            res = w7x.run_service(
                field_line_server.service.trace,
                seed_point.as_input(),
                self.as_input(),
                task,
                errors=errors,
            )

            if res is None:
                logging.warning("Turn {0} of {1}: fail".format(i_seed + 1, len(seeds)))
                nFailed += 1
                continue
            else:
                nSuccess += 1
                for surf in res.surfs:
                    p = Points3D(surf.points)
                    p.transform(tfields.bases.CYLINDER)
                    # phi is correct with rounding precision before. This way
                    # it is perfectly correct
                    p[:, 1].fill(surf.phi0)
                    poincareFluxSurfaces.append(p)
                logging.info("Turn %i of %i : success" % (i_seed + 1, len(seeds)))
        if nFailed > 0:
            logging.warning(
                "Trace finished with {0} succeded and {1} failed.".format(
                    nSuccess, nFailed
                )
            )
        else:
            logging.info(
                "Trace finished with {0} succeded and {1} failed.".format(
                    nSuccess, nFailed
                )
            )

        return poincareFluxSurfaces

    def magnetic_characteristics(self, points3D, taskStepSize=0.2, return_type=list):
        """
        Args:
            points3D (field_line_server.types.Points3D): points to retrieve
                characteristics from. Give None to take lcfs point
            taskStepSize (float)
            return_type (type): return either list or tfields.TensorFields.

        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> config = MagneticConfig.default()
            >>> mchars = config.magnetic_characteristics(
            ...     Points3D([[6.2, 0., 0.]]))  # This is long lasting.
            >>> assert len(mchars) == 1
            >>> mchar = mchars[0]
            >>> assert mchar.iota < 1
            >>> assert mchar.iota > 0.95
            >>> assert mchar.reff < 0.6
            >>> assert mchar.reff > 0.5
            >>> assert mchar.phi0 == 0.0

        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        # process input points3D
        points3D = Points3D(points3D)
        points3D.transform(tfields.bases.CARTESIAN)

        # define task
        task = field_line_server.types.Task()
        task.step = taskStepSize
        task.characteristics = field_line_server.types.MagneticCharacteristics()  # NOQA
        task.characteristics.axisSettings = (
            field_line_server.types.AxisSettings()
        )  # NOQA

        # run web service
        logging.info("Retrieving MagneticCharacteristics with the points given.")
        # the None after 'task' can be machine boundary.
        result = w7x.run_service(
            field_line_server.service.trace,
            points3D.as_input(),
            self.as_input(),
            task,
            None,
            None,
        )

        if result is None:
            return None
        if return_type is list:
            return result.characteristics
        elif issubclass(return_type, tfields.TensorFields):
            fields = [[], [], [], [], [], []]
            for x in result.characteristics:
                fields[0].append(x.iota)
                fields[1].append(x.diota)
                fields[2].append(x.reff)
                fields[3].append(x.dreff)
                fields[4].append(x.phi0)
                fields[5].append(x.theta0)
            return return_type(points3D, *fields)

    def iota(self, points3D, taskStepSize=0.2, return_type=list):
        """
        Args: see magnetic_characteristics
        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> import tfields
            >>> config = MagneticConfig.default()

            # >>> iotas = config.iota(Points3D([[6.2, 0., 0.]]))
            # >>> assert iotas[0] > 0.95
            # >>> assert iotas[0] < 1.0

            >>> tf = config.iota(Points3D([[ 6.2, 0., 0.]]),
            ...                  return_type=tfields.TensorFields)
            >>> assert tf.equal([[6.2, 0. , 0. ]])
            >>> assert tf.fields[0].equal([0.9627], atol=1e-4)

        """
        mag_char = self.magnetic_characteristics(points3D, taskStepSize, return_type)
        if return_type is list:
            return [x.iota for x in mag_char]
        elif issubclass(return_type, tfields.TensorFields):
            mag_char.fields = mag_char.fields[0:1]
            return mag_char

    def find_axis_at_phi(
        self, phi=0, size=w7x.Defaults.Poincare.stepSize, settings=None
    ):
        """
        Args:
            phi (float): phi in rad
            size (float): step size
            settings (field_line_server.types.AxisSettings())
        Returns:
            Points3D: magnetic axis position at phi=<phi>
        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if settings is not None:
            settings = settings.as_input()
        else:
            settings = field_line_server.types.AxisSettings(1)
        logging.getLogger().info("Finding axis at phi.")
        result = w7x.run_service(
            field_line_server.service.findAxisAtPhi,
            phi,
            size,
            self.as_input(),
            settings,
        )
        return Points3D(result.points, coord_sys=tfields.bases.CARTESIAN)

    def magnetic_field(self, points3D):
        # assure points3D has the correct format and coord_sys
        points3D = Points3D(points3D)
        points3D.transform(tfields.bases.CARTESIAN)

        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        logging.getLogger().info("Evaluating magnetic field at points.")
        result = w7x.run_service(
            field_line_server.service.magneticField,
            points3D.as_input(),
            self.as_input(),
        )
        return Points3D(result.field, coord_sys=tfields.bases.CARTESIAN)

    def plot_poincare(self, phi=0, seeds=None, numPoints=300, errors=None, **kwargs):
        """
        Plot a poincare plot
        Args:
            phi (float): phi in rad
            seeds (Points3D): seed points. If None, take default seeds
        """
        surfs = self.poincare_in_phi_plane(
            [phi], seeds=seeds, numPoints=numPoints, errors=errors
        )
        return w7x.plot_poincare_surfaces(surfs, **kwargs)


class Run(object):
    """
    Container class that knows everything important about the w7x setup you want to use.
    Note:

    Args:
        magnetic_config (MagneticConfig):
        machine (Machine):
    Attributes:

    Examples:

        >>> from w7x.flt import Run
        >>> config = Run()

    """

    def __init__(self, magnetic_config=None, machine=None):
        self.magnetic_config = magnetic_config
        self.machine = machine

    @property
    def magnetic_config(self):
        """
        (w7x.flt.MagneticConfig): magnetic configuration of the run
        """
        return self._magnetic_config

    @magnetic_config.setter
    def magnetic_config(self, magnetic_config):
        if magnetic_config is None:
            magnetic_config = MagneticConfig.default()
        else:
            magnetic_config = MagneticConfig(magnetic_config)
        self._magnetic_config = magnetic_config

    @property
    def machine(self):
        """
        (w7x.flt.Machine): machine geometry of the run
        """
        return self._machine

    @machine.setter
    def machine(self, machine):
        if machine is None:
            machine = Machine.default()
        else:
            Machine(machine)
        self._machine = machine

    def find_lcfs(self, step=0.001, settings=None, max_time=None):
        """
        Examples:
            >>> import w7x
            >>> run = w7x.flt.Run()
            >>> lcfs_point = run.find_lcfs(0.1)  # This is long lasting.
            >>> assert lcfs_point[0, 0] > 6.2
            >>> assert lcfs_point[0, 0] < 6.21

        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if settings is None:
            settings = field_line_server.types.LCFSSettings(1)
        else:
            settings = settings.as_input()

        logging.getLogger().info("Retrieving Point on Last closed flux surface")
        lCFSPoint = w7x.run_service(
            field_line_server.service.findLCFS,
            step,
            self.magnetic_config.as_input(),
            self.machine.as_input(),
            settings,
            max_time=max_time,
        )  # find last closed flux surface
        return Points3D([[lCFSPoint.x, lCFSPoint.y, lCFSPoint.z]])

    def line_tracing(self, points, step=0.01, numSteps=300):
        """
        Args:
            points (w7x.flt.Points3D)
            step (flota): step width of the tracer task
        """
        points = Points3D(points)
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)

        config = self.magnetic_config.as_input()

        task = field_line_server.types.Task()
        task.step = step
        task.lines = field_line_server.types.LineTracing()
        task.lines.numSteps = numSteps

        logging.info("starting line tracing ...")
        res = field_line_server.service.trace(points.as_input(), config, task, None)
        logging.info("... done")
        return [Points3D(line.vertices) for line in res.lines]

    def line_phi_span(self, points, phi, step=0.01):
        """
        Args:
            points (w7x.flt.Points3D)
            phi (float): phi in radian
            step (flota): step width of the tracer task
        """
        points = Points3D(points)
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)

        config = self.magnetic_config.as_input()

        task = field_line_server.types.Task()
        task.step = step
        task.linesPhi = field_line_server.types.LinePhiSpan()
        task.linesPhi.phi = phi

        logging.info("starting line tracing ...")
        res = field_line_server.service.trace(
            points.as_input(), config, task, self.machine.as_input()
        )
        logging.info("... done")
        return [Points3D(line.vertices) for line in res.lines]

    def line_phi(self, points, phi, phi_tolerance=1.0 / 180 * np.pi, step=0.01):
        """
        Get the crossection of the field lines starting at <points> at exactly one
        phi (exact within the tolerance given by <phi_tolerance>).
        You can specify the direction of tracing by switching the bool
        self.magnetic_config.inverseField
        Args:
            points (w7x.Points3D): starting points of tracing
            phi (float): phi in radian
        Returns:
            w7x.Points3D: piercing points of the lines,
                starting at <points> at exactly one
                phi (exact within the tolerance given by <phi_tolerance>).
                The return value will be empty an empty seuqence of Points3D,
                if the step size was not small enough.
        """
        lines = self.line_phi_span(points, phi, step=step)
        container = []
        for line in lines:
            line.transform(tfields.bases.CYLINDER)
            inds = line.where_phi_between(phi - phi_tolerance, phi + phi_tolerance)
            line = line[inds[0][-1:]]
            line[:, 1] = phi
            container.append(line)
        return Points3D.merged(*container)

    def line_diffusion(
        self,
        start_points=w7x.Defaults.Diffusion.nRevolutions,
        diffusion=w7x.Defaults.Diffusion.diffusion,
        velocity=w7x.Defaults.Diffusion.velocity,
        size=w7x.Defaults.Diffusion.stepSize,
        mean_free_path=w7x.Defaults.Diffusion.meanFreePath,
        additiona_shifts=None,
        start_point_shift=w7x.Defaults.Diffusion.startPointShift,
        **kwargs
    ):
        """
        Args:
            start_points(int | str | Points3D):
                int: number of points to trace
                str: path to full start point set that should be traced
                Points3D: full start point set that should be traced
            diffusion (float): perp. diffusion coefficient
        Returns:
            tuple:
                w7x.flt.ConnectionLength:
                w7x.flt.ComponentLoad:
                w7x.flt.Points3D: start points lying on lcfs
        Examples:
            >>> import w7x
            >>> import tfields

            Triangle approximating the bean plane
            >>> mesh = tfields.Mesh3D([[5.4,0,-1], [5.4,0,1], [6.5,0,0]],
            ...                       faces=[[0,1,2]], coord_sys='cylinder')

            Machine constitued from bean plane triangle and divertor
            >>> machine = w7x.flt.Machine(meshedModels=[mesh],
            ...                           meshedModelsIds=[165])
            >>> run = w7x.flt.Run(machine=machine)

            Initial point starting very close to the triangle
            >>> initial_points = w7x.flt.Points3D([[6.0,0.0001,0]],
            ...                                   coord_sys='cylinder')
            >>> conn_len, comp_load, start_points = run.line_diffusion(
            ...     initial_points)
            >>> assert initial_points.equal(start_points,atol=1e-9)

            As expected, the triangle was hit only
            >>> conn_len.parts
            [0, 0]

            The mm_id 1000 is added automatically
            >>> conn_len.mm_ids
            [1000, 165]

        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if additiona_shifts is None:
            additiona_shifts = [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1]

        nStart = None
        launchPointsPath = None
        if type(start_points) is int:
            nStart = start_points
            start_points = None
        elif type(start_points) is str:
            launchPointsPath = start_points
            start_points = None
        elif isinstance(start_points, tfields.Points3D):
            nStart = start_points.shape[0]
            if not isinstance(start_points, Points3D):
                start_points = Points3D(start_points)

        # define all setting inputs for diffusion
        fld_task = field_line_server.types.Task()
        fld_task.step = size
        line_diffusion = field_line_server.types.LineDiffusion()
        line_diffusion.diffusionCoeff = diffusion
        line_diffusion.freePath = mean_free_path
        line_diffusion.velocity = velocity
        fld_task.diffusion = line_diffusion
        fld_task.connection = field_line_server.types.ConnectionLength()
        fld_task.connection.limit = kwargs.pop("connectionLimit", 3000000.0)
        fld_task.connection.returnLoads = True
        config = self.magnetic_config.as_input()
        machine = self.machine.as_input()
        logging.info("Machine flsType: \n{machine}".format(**locals()))
        logging.info("Config flsType: \n{config}".format(**locals()))

        # check start_points validity
        if start_points is None and launchPointsPath is None:
            logging.info(
                "Creating random start lcfs_init_points on last closed flux surface"
            )
            lcfs_init_points = self.find_lcfs()

            """
            remove small value to be save to be inside
            offset changed on 2.11 from 0.001 to 0.02. It shows, that the
            computation time increase due to longer diffusion path
            is waaay less than repeating a whole shot (at least for D=1m^s/s).
            """
            lcfs_init_points[:, 0] -= 0.02 + start_point_shift

        for iShift, additional_shift in enumerate(additiona_shifts):
            if iShift == 0 and start_points is not None:
                # before start_points could have been set by fld it has been
                # given
                logging.info("Start points were given.")
            elif launchPointsPath is None:
                lcfs_init_points[:, 0] -= additional_shift
                logging.info(" Startpoint: %s", lcfs_init_points)

                trace_task = field_line_server.types.Task()
                trace_task.step = 0.5
                line = field_line_server.types.LineTracing()
                line.numSteps = nStart - 1
                trace_task.lines = line

                logging.info("Trace this point %s-times.", line.numSteps)
                res = w7x.run_service(
                    field_line_server.service.trace,
                    lcfs_init_points.as_input(),
                    config,
                    trace_task,
                    machine,
                    max_time=None,
                )

                start_points = res.lines[0].vertices

                # END  creating random start_points on last closed flux surface
            else:
                logging.info("Reading launch points")
                start_points = Points3D.load(launchPointsPath)

            # force start_points to CARTESIAN and check dimension
            start_points = w7x.Points3D(start_points)
            start_points.transform(tfields.bases.CARTESIAN)

            logging.info("Line diffusion forwards.")
            # max_time could be something like int(round(line.numSteps / 4000. * 2000)))
            resForward = w7x.run_service(
                field_line_server.service.trace,
                start_points.as_input(),
                config,
                fld_task,
                machine,
                max_time=None,
            )
            resForwardClass = ConnectionLength(resForward.connection)
            if len(resForwardClass) == nStart:
                logging.info("Length %s accepted!", len(resForwardClass))
                if launchPointsPath is None:
                    start_points = Points3D(start_points)
                break
            elif launchPointsPath is not None:
                logging.warning(
                    "LaunchPointsPath is given but number of HitPoints"
                    "is not meeting requested number."
                )
                break
            elif iShift == len(additiona_shifts) - 1:
                logging.error(
                    "Also after shift of {} number of H".format(sum(additiona_shifts))
                )
                raise ValueError(
                    "Also after shift of %s number of H" % sum(additiona_shifts)
                )
            else:
                logging.warning(
                    "Restart the forward tracing with a new lCFSInitPoint "
                    "offset of %s since the number of output points (%s) "
                    "does not meet opts.nRevolutions(%s)",
                    sum(additiona_shifts[: iShift + 2]),
                    len(resForwardClass),
                    nStart,
                )

        logging.info("Line diffusion backwards.")
        config.inverseField = True
        # max_time estimate: int(round(line.numSteps / 4000. * 2000)))
        res_invers = w7x.run_service(
            field_line_server.service.trace,
            start_points.as_input(),
            config,
            fld_task,
            machine,
            max_time=None,
        )

        connection_length = ConnectionLength(
            resForward.connection + res_invers.connection
        )
        connection_length.mm_ids = self.machine.mm_ids

        component_load = ComponentLoad(
            resForward.loads.components + res_invers.loads.components
        )
        component_load.mm_ids = self.machine.mm_ids
        return connection_length, component_load, start_points

    def connection_length(self, points, **kwargs):
        """
        Args:
            points: Points3D
            **kwargs:
                limit (float): lenght limit of line tracing
                step (float): step size of line tracing
                diffusion (field_line_server.type.LineDiffusion()): add diffusion
                    to the tracing

        Returns:
            ConnectionLength

        """
        step = kwargs.pop("step", 5e-3)
        limit = kwargs.pop("limit", 2.0e4)
        diffusion = kwargs.pop("diffusion", None)

        points.transform(tfields.bases.CARTESIAN)

        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        task = field_line_server.types.Task()
        task.step = step
        con = field_line_server.types.ConnectionLength()
        con.limit = limit
        con.returnLoads = False
        task.connection = con

        if diffusion:
            task.diffusion = diffusion

        logging.info("Start tracing ...")
        res = w7x.run_service(
            field_line_server.service.trace,
            points.as_input(),
            self.magnetic_config.as_input(),
            task,
            self.machine.as_input(),
        )
        connection_length = ConnectionLength(res.connection)
        connection_length.mm_ids = self.machine.mm_ids
        lengths = np.array(connection_length.lengths)
        lengths[lengths == limit] = np.inf
        connection_length.lengths = list(lengths)
        return connection_length

    def plot_poincare(self, phi, seeds=None, **kwargs):
        """
        forward to self.magnetic_config.plot_poincare and
        self.machine.plot_poincare
        """
        artists = []
        if self.magnetic_config is not None:
            artists.extend(
                self.magnetic_config.plot_poincare(phi, seeds=seeds, **kwargs)
            )
        if self.machine is not None:
            artists.extend(self.machine.plot_poincare(phi, **kwargs))
        return artists


if __name__ == "__main__":
    import doctest

    doctest.testmod()
