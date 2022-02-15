import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from matplotlib import cm


def _plot_field_layout(X, Y, Z, L_min):
    """Plot field layout."""
    # 0.000001 is added/subtracted for the limits in order for the colormap
    # to correctly display the middle color when all tracker Z coords are zero
    norm = mcolors.Normalize(vmin=min(Z)-0.000001, vmax=max(Z)+0.000001)
    cmap = cm.viridis_r
    colors = cmap(norm(Z))
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
    # Plot a circle with a diameter equal to L_min
    ax.add_collection(EllipseCollection(widths=L_min, heights=L_min,
                                        angles=0, units='xy',
                                        facecolors=colors,
                                        edgecolors=("black",),
                                        linewidths=(1,),
                                        offsets=list(zip(X, Y)),
                                        transOffset=ax.transData))
    # Similarly, add a circle for the origin
    ax.add_collection(EllipseCollection(widths=L_min, heights=L_min,
                                        angles=0, units='xy',
                                        facecolors='red',
                                        edgecolors=("black",),
                                        linewidths=(1,), offsets=[0, 0],
                                        transOffset=ax.transData))
    plt.axis('equal')
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.8,
                 label='Relative tracker height (vertical)')
    lower_lim = min(min(X), min(Y)) - L_min
    upper_lim = max(max(X), max(Y)) + L_min
    ax.set_ylim(lower_lim, upper_lim)
    ax.set_xlim(lower_lim, upper_lim)


def _plot_shading(collector_geometry, unshaded_geomtry, shade_geometries):
    """Plot the shaded and unshaded area for a specific solar position."""
    shade_exterios = [Polygon(g.exterior) for g in shade_geometries]
    shade_patches = PatchCollection(shade_exterios, facecolor='blue',
                                    linewidth=0.5, alpha=0.5)
    collector_patch = PatchCollection(
        [Polygon(collector_geometry.exterior)],
        facecolor='red', linewidth=0.5, alpha=0.5)
    unshaded_patch = PatchCollection([Polygon(unshaded_geomtry.exterior)],
                                     facecolor='green', linewidth=0.5,
                                     alpha=0.5)
    fig, ax = plt.subplots(1, 2, subplot_kw=dict(aspect='equal'))
    ax[0].add_collection(collector_patch, autolim=True)
    ax[0].add_collection(shade_patches, autolim=True)
    ax[1].add_collection(unshaded_patch, autolim=True)
    ax[0].set_xlim(-6, 6), ax[1].set_xlim(-6, 6)
    ax[0].set_ylim(-2, 2), ax[1].set_ylim(-2, 2)
    plt.show()
