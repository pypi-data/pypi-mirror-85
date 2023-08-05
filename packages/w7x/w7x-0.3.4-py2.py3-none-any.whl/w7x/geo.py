from six import string_types


class GeoSet(list):
    def __init__(self, mm_ids=[], name="mm_id", color="black", paths=None):
        self.name = name
        self.color = color
        self.paths = paths
        self.hits = 0
        self.load = 0.0
        content = []
        for mm_id in mm_ids:
            if isinstance(mm_id, int):
                content.append(mm_id)
            elif isinstance(mm_id, GeoSet):
                content.extend(mm_id)
            elif isinstance(mm_id, string_types):
                from w7x import MeshedModelsIds

                content.extend(getattr(MeshedModelsIds, mm_id))
            else:
                raise NotImplementedError("mm_id {mm_id}".format(**locals()))
        super(GeoSet, self).__init__(content)

    @property
    def paths(self):
        return self._path

    @paths.setter
    def paths(self, paths):
        if not isinstance(paths, list):
            paths = [paths] * len(self)
        self._path = paths

    def __hash__(self):
        return hash(self.name + str(self))


def get_geo_set(mm_id, cls=None):
    """
    Find a GeoSet static attribute in the MeshedModelsIds class defined in config.py
    """
    if cls is None:
        import w7x

        cls = w7x.MeshedModelsIds
    for attr in cls.__dict__:
        thing = cls.__dict__[attr]
        if isinstance(thing, GeoSet):
            if mm_id in thing:
                return thing
    return None


def get_geo_sets(mm_ids, cls=None):
    """

    Find the suiting GeoSet objects to the goeIds
    Examples:
        >>> import w7x
        >>> gss = w7x.geo.get_geo_sets(list(range(320, 345)))
        >>> assert [gs.name for gs in gss] == ['baffle', 'tda', 'shield',
        ...                                    'panel', 'vessel']

    Raises:
        Not the complete GeoSet given
        >>> w7x.geo.get_geo_sets(list(range(320, 321)))  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: GeoSet 'baffle' is not complete.

    """

    def checkCompleteness(geo_set, counter):
        if counter != len(geo_set) - 1:
            raise ValueError(
                "GeoSet '{geo_set.name}' is not complete.".format(**locals())
            )

    geoSets = []
    lastGeoSet = None
    counter = 0
    for i, mm_id in enumerate(mm_ids):
        geo_set = get_geo_set(mm_id, cls=cls)
        if geo_set is None:
            raise ValueError(
                "No GeoSet found for mm_id {mm_id} in cls '{cls}'".format(**locals())
            )
        if lastGeoSet == geo_set:
            counter += 1
            if geo_set[counter] != mm_id:
                raise ValueError(
                    "mm_id {mm_id} found at wrong position".format(**locals())
                )
        else:
            if i != 0:
                checkCompleteness(lastGeoSet, counter)
            counter = 0
            lastGeoSet = geo_set
            geoSets.append(geo_set)
    else:
        checkCompleteness(lastGeoSet, counter)

    return geoSets


if __name__ == "__main__":
    import doctest

    doctest.testmod()
