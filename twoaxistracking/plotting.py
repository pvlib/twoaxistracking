import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def _plot_field_layout(X, Y, L_min):
    """Plot field layout."""
    fig, ax = plt.subplots(figsize=(6, 6))
    # Plot a circle with a diameter equal to L_min
    ax.add_collection(EllipseCollection(widths=L_min, heights=L_min,
                                        angles=0, units='xy',
                                        facecolors='white',
                                        edgecolors=("black",),
                                        linewidths=(1,),
                                        offsets=list(zip(X, Y)),
                                        transOffset=ax.transData))
    # Add a circle for the origin
    ax.add_collection(EllipseCollection(widths=L_min, heights=L_min,
                                        angles=0, units='xy',
                                        facecolors='red',
                                        edgecolors=("black",),
                                        linewidths=(1,), offsets=[0, 0],
                                        transOffset=ax.transData))
    plt.axis('equal')
    ax.grid()
    ax.set_ylim(min(Y)-L_min, max(Y)+L_min)
    ax.set_xlim(min(X)-L_min, max(X)+L_min)


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
