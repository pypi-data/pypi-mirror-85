"""
abstract classes to work with the webservice revolving around the osa package
"""
import w7x.lib
import six
import copy
from six import string_types
import osa
import logging
import numpy as np
import rna
import tfields

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import HTTPError


def compare_error_attributes(
    error, errors=None, attributes=None, messageContent=None, **kwargs
):
    """
    Annotation:
        if you want a content in the msg, use args attribute.
    Returns:
        True if error.attributes == error_list.attributes else False
    Examples:
        >>> from w7x import core
        >>> d = {'errors': [core.HTTPError(None, 500, None, None, None),
        ...                 core.HTTPError("ASDF", 600, None, None, None)],
        ...      'attributes': ['code'],
        ...      'messageContent': None}
        >>> core.compare_error_attributes(core.HTTPError(None, 500, None, None, None), **d)  # NOQA
        [True, False]
        >>> e = {'errors': [RuntimeError("A special Message content"),
        ...                 core.HTTPError("ASDF", 600, None, None, None)],
        ...      'attributes': ['args']}
        >>> core.compare_error_attributes(RuntimeError("This is A special Message content for you"), **e)  # NOQA
        [True, False]

    """
    errors = errors or []
    attributes = attributes or ["code"]
    comparisons = []
    for inst in errors:
        return_bool = True
        if type(error) is not type(inst):  # must be same type ...
            return_bool = False
        else:
            for (
                attr
            ) in attributes:  # ... and contain the same requested attribute values
                if not hasattr(error, attr) or not hasattr(inst, attr):
                    return_bool = False
                    break
                if attr == "args":
                    if len(error.args) == 0:
                        raise TypeError("Length of args is not suiting.")
                    if not inst.args[0] in error.args[0]:
                        return_bool = False
                        break
                elif not getattr(error, attr) == getattr(inst, attr):
                    return_bool = False
                    break
        comparisons.append(return_bool)
    return comparisons


def run_service(fun, *args, **kwargs):
    """
    Run a service function with the arguments args. Check for HTTPError
    occurence and redo if you get it.
    Kwargs:
        max_tries (int): Maximum tries, Default is 1
        max_time (int): Maximum time for the process [s]. Default is inf (<None> value)
        errors (list of dicts describing errors): Each dict has the
            keywords:
                'errors' (list of Error instances)
                'attributes' (list of attributes)
                'action' (str): 'retry' / 'skip'
            Perform action if error.attributes == errors.attributes for any
            error
    Returns:
        Result of service or function. None if Error from errorDict says skip
    """
    log = logging.getLogger()
    max_tries = kwargs.pop("max_tries", 1)
    if max_tries < 1:
        raise ValueError("max_tries needs to be 1 at minimum.")
    max_time = kwargs.pop("max_time", None)
    errors_default = [
        {
            "errors": [HTTPError(None, 500, None, None, None)],
            "attributes": ["code"],
            "action": "retry",
        },
        {
            "errors": [HTTPError(None, 404, None, None, None)],
            "attributes": ["code"],
            "action": "retry",
        },
        {
            "errors": [HTTPError(None, 413, None, None, None)],
            "attributes": ["code"],
            "action": "retry",
        },
        {
            "errors": [RuntimeError("Grid_CylLowendel")],
            "attributes": ["args"],
            "action": "skip",
        },
        {
            "errors": [RuntimeError("ThreadTracer failed.")],
            "attributes": ["args"],
            "action": "skip",
        },
        {
            "errors": [RuntimeError("zero field")],
            "attributes": ["args"],
            "action": "skip",
        },
    ]
    errors = kwargs.pop("errors", [])
    errors.extend(errors_default)

    result = None
    try_count = 1

    @w7x.lib.timeout.timeout(max_time)
    def run(fun, *args):
        return fun(*args)

    while result is None:
        try:
            result = run(fun, *args)  # run service with arguments
            if result is None:
                log.warning("Result is really None")
            break
        except w7x.lib.timeout.TimeoutError:
            log.error("TimeoutError. Took more than %s seconds." % max_time)
            if try_count < max_tries:
                try_count += 1
                log.info("Retry service %s." % fun)
            else:
                raise  # Also allows result being <None>
        except Exception as err:
            log.error(err)
            skip = False
            retry = False
            for eD in errors:
                if any(compare_error_attributes(err, **eD)):
                    if eD["action"] == "retry":
                        retry = True
                    elif eD["action"] == "skip":
                        skip = True
                    else:
                        raise TypeError("%s is no allowed Action" % eD["action"])
            if skip:
                log.info("Skip service %s." % fun)
                break
            elif retry:
                if try_count < max_tries:
                    try_count += 1
                    log.info("Retry service %s." % fun)
                    continue
            raise
    return result


SERVERCACHE = {}


def get_server(address):
    """
    Cached method to retrieve osa.Client from adress.
    Timeout is implemented.
    Examples:
        TODO: this example only works if the server can connect
        >>> import w7x
        >>> addr = w7x.Server.addr_field_line_server
        >>> addr in str(w7x.get_server(addr))
        True

    """
    if address in SERVERCACHE:
        return SERVERCACHE[address]

    server = None
    log = logging.getLogger()

    server = run_service(osa.Client, address, max_tries=1, max_time=1)
    try:
        server = run_service(osa.Client, address, max_tries=1, max_time=1)
    except Exception:
        log.error("Server at {0} could not connect.".format(address))
    SERVERCACHE[address] = server
    return server


def get_ws_class(ws_server, ws_class):
    """
    Args:
        ws_server (str): address of webservice
        ws_class (str): name of webService type class
    Returns:
        server.types.ws_class
    """
    server = get_server(ws_server)
    return getattr(server.types, ws_class)


def is_w7x_instance(obj, tpe, convert=True):
    """
    Check, if an object is instance of a web server class
    Args:
        obj (object instance): instance to check the ...
        tpe (class or <webservice>.types.<class>): ... type for
        convert (bool): convert all obj and tpe to osa before checking
            you can provide conversion ability by defining the methods
            'as_input' for objs and 'get_ws_class' for tpes
    Returns:
        bool
    Examples:
        >>> import w7x
        >>> p = w7x.Points3D([[5, 1, 0]])

        checking osa type directly
        >>> fieldLineServer = w7x.get_server(w7x.Server.addr_field_line_server)
        >>> w7x.core.is_w7x_instance(p, fieldLineServer.types.Points3D)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), fieldLineServer.types.Points3D)
        True

        checking objects that provide get_ws_class methods
        >>> w7x.core.is_w7x_instance(p, w7x.Points3D)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), w7x.Points3D)
        True

        checking only osa types
        >>> w7x.core.is_w7x_instance(p, w7x.Points3D, convert=False)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), w7x.Points3D, convert=False)
        False
        >>> w7x.core.is_w7x_instance(p, fieldLineServer.types.Points3D, convert=False)
        False
        >>> w7x.core.is_w7x_instance(p.as_input(), fieldLineServer.types.Points3D, convert=False)
        True

        test the same for Base derived instance
        >>> m = w7x.MagneticConfig.default()
        >>> w7x.core.is_w7x_instance(m.as_input(), w7x.MagneticConfig)
        True
        >>> w7x.core.is_w7x_instance(m, w7x.MagneticConfig)
        True
        >>> w7x.core.is_w7x_instance(m, w7x.MagneticConfig.get_ws_class())
        True

    """
    # convert all Base derived objs and tpes to osa
    if convert:
        if issubclass(obj.__class__, Base) or hasattr(obj, "as_input"):
            obj = obj.as_input()
        if issubclass(tpe, Base) or hasattr(tpe, "get_ws_class"):
            tpe = tpe.get_ws_class()

    if isinstance(tpe, osa.xmltypes.ComplexTypeMeta):
        if convert or isinstance(obj.__class__, osa.xmltypes.ComplexTypeMeta):
            return obj.__class__.__name__ == tpe.__name__

    return isinstance(obj, tpe)


class Base(object):
    """
    Base class wrapping osa types.

    Static Attrs:
        prop_defaults (dict): keys are attributes and values default values
        prop_order (list): order of osa type attributes. *args in __init__ are
            interpreted in this order
        ws_server (str): address of web service
        ws_class (type): osa type to be wrapped by this class. If this is not
            not set or None, it will default to ws_server.types.<cls.__name__>
        ws_class_args (list): args for instantiating ws_class object
        ws_class_kwargs (dict): kwargs for instantiating ws_class object
    """

    prop_defaults = None
    prop_order = None

    ws_server = None
    ws_class = None
    ws_class_args = None
    ws_class_kwargs = None

    def __init__(self, *args, **kwargs):
        self.prop_defaults = self.prop_defaults or {}
        self.prop_order = self.prop_order or []

        if len(args) == 1 and is_w7x_instance(args[0], self.__class__):
            # copy constructor from cls or related ws class
            other = args[0]
            if is_w7x_instance(other, self.get_ws_class(), convert=False):
                for attr in self.prop_attrs():
                    if hasattr(other, attr):
                        kwargs[attr] = getattr(other, attr)
            else:
                kwargs = other.prop_dict(kwargs)
            if len(args) > 1:
                raise ValueError("More than one argument given in copy " "constructor.")
        else:
            # update kwargs with arguments defined in args
            for attr, arg in zip(self.prop_order, args):
                if attr in kwargs:
                    raise AttributeError(
                        "Attribute {attr} specified in args "
                        "and kwargs! I will use args!".format(**locals())
                    )
                kwargs[attr] = arg

        # default properties
        props = self.prop_dict()
        props.update(self.prop_defaults)
        # set attributes from kwargs or props
        for key, default in six.iteritems(props):
            val = kwargs.pop(key, default)
            setattr(self, key, val)

        if len(kwargs) > 0:
            raise AttributeError("kwargs have unused arguments %s" % kwargs.keys())

    def prop_attrs(self):
        """
        Returns:
            list of str: properties that are occuring in the osa type input
        """
        try:
            attrs = dir(self.get_ws_class())
        except Exception:
            log = logging.getLogger()
            log.warning(
                "could not connect to server and thus not dynamically "
                "get the property defaults."
            )
            if self.prop_defaults is not None:
                attrs = self.prop_defaults.keys()

        prop_attrs = []
        for attr in attrs:
            if attr.startswith("_"):
                continue
            if attr in ["from_file", "from_xml", "to_file", "to_xml"]:
                continue
            prop_attrs.append(attr)
        return prop_attrs

    def prop_dict(self, kwargs=None):
        kwargs = kwargs or {}
        for key in self.prop_attrs():
            kwargs[key] = getattr(self, key, None)
        return kwargs

    def __deepcopy__(self, memo):
        """
        copy with the copy constructor
        """
        kwargs = copy.deepcopy(self.prop_dict(), memo)
        return self.__class__(**kwargs)

    def copy(self):
        """
        copy with deepcopy
        """
        return copy.deepcopy(self)

    @classmethod
    def get_ws_class(cls):
        """
        Returns the osa class version of this class
        """
        ws_class = cls.ws_class or cls.__name__
        return get_ws_class(cls.ws_server, ws_class)

    def to_file(self, path):
        """
        Forward to xml.to_file(self, path)
        Examples:
            >>> import w7x
            >>> mc = w7x.flt.MagneticConfig.default()
            >>> mc.to_file('/tmp/mc.xlm')
            >>> mc_loaded = w7x.flt.MagneticConfig.from_file('/tmp/mc.xlm')
            >>> mc.as_input() == mc_loaded.as_input()
            True

        """
        self.as_input().to_file(rna.path.resolve(path))

    @classmethod
    def from_file(cls, path):
        return cls(cls.get_ws_class().from_file(rna.path.resolve(path)))

    def save(self, path):
        """
        Alias for to_file
        """
        path = rna.path.resolve(path)
        rna.path.mkdir(path)
        self.to_file(path)

    @classmethod
    def load(cls, path):
        """
        Alias for from_file
        """
        return cls.from_file(rna.path.resolve(path))

    def as_input(self):
        """
        return copy in get_ws_class format. Chain this to the attributes.
        """
        cls = self.get_ws_class()
        ws_class_args = self.ws_class_args or []
        ws_class_kwargs = self.ws_class_kwargs or {}
        instance = cls(*ws_class_args, **ws_class_kwargs)
        for (prop, default) in six.iteritems(self.prop_defaults):
            value = self.__dict__.get(prop, default)
            if value is not None:
                if issubclass(value.__class__, Base) or hasattr(value, "as_input"):
                    value = value.as_input()
                elif hasattr(value, "__iter__") and not isinstance(value, string_types):
                    value = [
                        v.as_input() if hasattr(v, "as_input") else v for v in value
                    ]
                setattr(instance, prop, value)
        return instance


class BasePoints3D(tfields.Points3D, Base):
    """Imitation of the field_line_server Points3D Type.
    Inheriting from tfield.Points3D so the coordinate system is tracked and
    coordinate transformations are inherently possible

    Args:
        many ways to initialize:
        1.
            like tfields.Points3D
        2.
            points3D (osa.Points3D): copyConstructor
        3.
            pointsList (list): list of triples in varioues formats
    Attributes:

    Examples:
        see tfields.points3D.Points3D

        One further constructor implemented:
        >>> import w7x
        >>> ws_points = w7x.Points3D([[1, 2, 3], [4, 5, 6]])
        >>> ws_points_2 = w7x.Points3D(ws_points.as_input())
        >>> assert ws_points.equal(ws_points_2)

    """

    def __new__(cls, tensors, *args, **kwargs):
        if w7x.is_w7x_instance(tensors, cls.get_ws_class(), convert=False):
            tensors = np.array([tensors.x1, tensors.x2, tensors.x3]).T
        obj = tfields.Points3D.__new__(cls, tensors, *args, **kwargs)
        return obj

    def __init__(self, *args, **kwargs):
        for attr in self.__slots__:  # TODO remove that
            kwargs.pop(attr, None)
        super().__init__(self, *args, **kwargs)

    def as_input(self):
        """
        return field_line_server type copy of self
        """
        raw_points = self.get_ws_class()()
        raw_points.x1 = list(self[:, 0])
        raw_points.x2 = list(self[:, 1])
        raw_points.x3 = list(self[:, 2])
        return raw_points

    def to_segment_one(self, mirror_z=True):
        """
        Map the points to the first module of w7x and mirror to positive z
        if mirror_zOption is True. The mirror option is interesting for the
        divertor for example.
        Examples:
            >>> import w7x
            >>> import numpy as np
            >>> pStart = w7x.Points3D([[6, np.pi, 1],
            ...                        [6, np.pi / 5 * 3, -1]],
            ...                       coord_sys='cylinder')
            >>> pStart.to_segment_one()
            >>> pStart
            Points3D([[ 6.        , -0.62831853,  1.        ],
                      [ 6.        ,  0.62831853,  1.        ]])

        """
        with self.tmp_transform(tfields.bases.CYLINDER):
            offset_segment_0 = -2 * np.pi / 10
            self.to_segment(0, 5, 1, offset=offset_segment_0)
            if mirror_z:
                condition = self[:, 2] < 0
                self.mirror([1, 2], condition=condition)

    def where_phi_between(self, phi_min, phi_max):
        """
        Args:
            phi_min (float): minimum phi in radian
            phi_max (float): maximum phi in radian
        Returns:
            output of np.where with condition
        """
        with self.tmp_transform(tfields.bases.CYLINDER):
            phi = self[:, 1]
        if phi_min < phi_max:
            return np.where((phi_min <= phi) & (phi <= phi_max))
        elif phi_min > phi_max:
            return np.where(np.logical_not((phi_max < phi) & (phi < phi_min)))
        else:
            return np.where(phi == phi_min)

    def phi_between(self, phi_min, phi_max):
        """
        Args:
            phi_min (float): minimum phi in radian
            phi_max (float): maximum phi in radian
        Returns:
            bool: if phi of all points is in between the given values
        """
        return len(self.where_phi_between(phi_min, phi_max)[0]) == len(self)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
