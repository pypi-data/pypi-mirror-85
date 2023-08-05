"""
specific methods for poincare plotting
"""
import tfields
import rna


def plot_poincare_surfaces(poincareSurfaces, **kwargs):
    """
    Args:
        poincareSurfaces (list of Points3D): each Points3D instance is one
            fieldLine followed around the torus
    """
    method = kwargs.pop("method", "scatter")
    po = rna.plotting.PlotManager(kwargs)
    rMin = po.pop("rMin", 4.0)
    rMax = po.pop("rMax", 6.6)
    zMin = po.pop("zMin", -1.3)
    zMax = po.pop("zMax", +1.3)
    phiRad = po.pop("phiRad", None)

    po.setdefault("y_index", 2)
    po.setdefault("labels", ["r (m)", r"$\phi$ (rad)", "z (m)"])
    if method == "scatter":
        po.setdefault("marker", ".")
        po.setdefault("s", 1)
    po.setdefault("method", method)
    color_given = True
    if "color" not in po.plot_kwargs:
        color_given = False
        cmap, _, _ = po.get_norm_args()
        color_cycle = rna.plotting.colors.color_cycle(cmap, len(poincareSurfaces))
    elif isinstance(po.get("color"), list):
        color_given = False  # hack to set the color from list
        color_cycle = iter(po.get("color"))
    artists = []
    for i, surfacePoints in enumerate(poincareSurfaces):
        with surfacePoints.tmp_transform(tfields.bases.CYLINDER):
            phiSurface = surfacePoints[:, 1]
            if phiRad is None:
                phiRad = phiSurface[0]
            if bool((phiSurface != phiRad).any()):
                continue
            if not color_given:
                po.set("color", next(color_cycle))
            artists.append(surfacePoints.plot(axes=po.axes, **po.plot_kwargs))
    rna.plotting.set_aspect_equal(po.axes)
    po.axes.set_xlim(rMin, rMax)
    po.axes.set_ylim(zMin, zMax)
    return artists


def plot_poincare_geometries(geometries, **kwargs):
    po = rna.plotting.PlotManager(kwargs)
    po.setdefault("method", "plot")
    po.setdefault("lw", 1)
    artists = []
    for p in range(len(geometries)):
        for g in range(len(geometries[p])):
            artists.extend(
                plot_poincare_surfaces(geometries[p][g], axes=po.axes, **po.plot_kwargs)
            )
    return artists
