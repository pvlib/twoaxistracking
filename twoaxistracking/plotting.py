import matplotlib.pyplot as plt
from matplotlib import collections
from matplotlib import patches
from shapely import geometry
import matplotlib.colors as mcolors
from matplotlib import cm


def _plot_field_layout(X, Y, Z, L_min):
    """Plot field layout."""
    # Collector heights is illustrated with colors from a colormap
    norm = mcolors.Normalize(vmin=min(Z)-0.000001, vmax=max(Z)+0.000001)
    # 0.000001 is added/subtracted for the limits in order for the colormap
    # to correctly display the middle color when all tracker Z coords are zero
    cmap = cm.viridis_r
    colors = cmap(norm(Z))
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
    # Plot a circle for each neighboring collector (diameter equals L_min)
    ax.add_collection(collections.EllipseCollection(
        widths=L_min, heights=L_min, angles=0, units='xy', facecolors=colors,
        edgecolors=("black",), linewidths=(1,), offsets=list(zip(X, Y)),
        transOffset=ax.transData))
    # Similarly, add a circle for the origin
    ax.add_collection(collections.EllipseCollection(
        widths=L_min, heights=L_min, angles=0, units='xy', facecolors='red',
        edgecolors=("black",), linewidths=(1,), offsets=[0, 0],
        transOffset=ax.transData))
    plt.axis('equal')
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.8,
                 label='Relative tracker height (vertical)')
    # Set limits
    lower_lim = min(min(X), min(Y)) - L_min
    upper_lim = max(max(X), max(Y)) + L_min
    ax.set_ylim(lower_lim, upper_lim)
    ax.set_xlim(lower_lim, upper_lim)


def _polygons_to_patch_collection(geometries, **kwargs):
    """Convert Shapely Polygon or MultiPolygon to matplotlib PathCollection.

    kwargs are passed to PatchCollection
    """
    # Convert geometries to a MultiPolygon if it is a Polygon
    if isinstance(geometries, geometry.Polygon):
        geometries = geometry.MultiPolygon([geometries])
    exteriors = [patches.Polygon(g.exterior) for g in geometries]
    path_collection = collections.PatchCollection(exteriors, **kwargs)
    return path_collection


def _plot_shading(active_collector_geometry, unshaded_geometry,
                  shading_geometries, L_min):
    """Plot the shaded and unshaded area for a specific solar position."""
    active_patches = _polygons_to_patch_collection(
        active_collector_geometry, facecolor='red', linewidth=0.5, alpha=0.5)
    unshaded_patches = _polygons_to_patch_collection(
        unshaded_geometry, facecolor='green', linewidth=0.5, alpha=0.5)
    shading_patches = _polygons_to_patch_collection(
        shading_geometries, facecolor='blue', linewidth=0.5, alpha=0.5)

    fig, axes = plt.subplots(1, 2, subplot_kw=dict(aspect='equal'))
    axes[0].set_title('Unshaded and shading areas')
    axes[0].add_collection(active_patches, autolim=True)
    axes[0].add_collection(shading_patches, autolim=True)
    axes[1].set_title('Unshaded area')
    axes[1].add_collection(unshaded_patches, autolim=True)
    for ax in axes:
        ax.set_xlim(-L_min, L_min)
        ax.set_ylim(-L_min, L_min)
    plt.show()
