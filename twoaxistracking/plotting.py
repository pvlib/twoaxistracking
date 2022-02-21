import matplotlib.pyplot as plt
from matplotlib import collections
from matplotlib import patches
from shapely import geometry


def _plot_field_layout(X, Y, L_min):
    """Plot field layout."""
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect='equal'))
    # Plot a circle for each neighboring collector (diameter equals L_min)
    ax.add_collection(collections.EllipseCollection(
        widths=L_min, heights=L_min, angles=0, units='xy', facecolors='white',
        edgecolors=("black",), linewidths=(1,), offsets=list(zip(X, Y)),
        transOffset=ax.transData))
    # Add a circle for the origin (reference collector)
    ax.add_collection(collections.EllipseCollection(
        widths=L_min, heights=L_min, angles=0, units='xy', facecolors='red',
        edgecolors=("black",), linewidths=(1,), offsets=[0, 0],
        transOffset=ax.transData))
    ax.grid()
    ax.set_ylim(min(Y)-L_min, max(Y)+L_min)
    ax.set_xlim(min(X)-L_min, max(X)+L_min)


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
