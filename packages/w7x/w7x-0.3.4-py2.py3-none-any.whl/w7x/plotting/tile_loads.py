import rna
import numpy as np
import numpy.lib.recfunctions
import matplotlib.pyplot as plt


def plot_tile_loads(loads, **kwargs):
    """
    Args:
        mask (np.ndarray): 2d array with mask for each value to plot wiht alpha=0
        text (str): annotation which is added above the picture
    """
    po = rna.plotting.PlotManager(kwargs)
    loads = np.array(loads)
    if len(loads.shape) == 1:
        raise DeprecationWarning()
    mask = np.array(po.pop("mask", None))
    text = po.pop("text", None)
    if mask is not None:
        cmap, vmin, vmax = po.get_norm_args(cmap_default="viridis")
        loads = rna.plotting.colors.to_colors(
            loads, fmt="rgba", cmap=cmap, vmin=vmin, vmax=vmax
        )
        alphas = np.ones(mask.shape)
        alphas[mask] = 0.0
        loads[["a"]] = alphas.reshape(loads.shape)
        # get rid of rgba dtype
        loads = np.lib.recfunctions.structured_to_unstructured(loads)
    artist = po.axes.imshow(loads, **po.plot_kwargs)
    po.axes.set_xticks(np.arange(-0.5, loads.shape[1] + 0.5, 1), minor=True)
    po.axes.set_yticks(np.arange(-0.5, loads.shape[0] + 0.5, 1), minor=True)

    plt.rc("grid", linestyle="solid", color="black")
    po.axes.grid(color="k", which="minor")

    po.axes.tick_params(
        axis="both",  # changes apply to both axis
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False,
    )  # labels along the bottom edge are off
    po.axes.yaxis.set_ticks_position("none")
    plt.setp(po.axes.get_yticklabels(), visible=False)

    # optional: add an annotation
    if text is not None:
        po.axes.text(2, -2, text)
    return artist
