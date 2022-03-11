import matplotlib.pyplot as plt
from matplotlib import collections
from matplotlib import patches
from shapely import geometry
import matplotlib.colors as mcolors
from matplotlib import cm


def _plot_field_layout(X, Y, Z, min_tracker_spacing):
    """Create a plot of the field layout."""
    # Collector heights is illustrated with colors from a colormap
    norm = mcolors.Normalize(vmin=min(Z)-0.000001, vmax=max(Z)+0.000001)
    # 0.000001 is added/subtracted to/from the limits in order for the colormap
    # to correctly display the middle color when all tracker Z coords are zero
    cmap = cm.viridis_r
    colors = cmap(norm(Z))
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'aspect': 'equal'})
    # Plot a circle for each neighboring collector (diameter equals min_tracker_spacing)
    ax.add_collection(collections.EllipseCollection(
        widths=min_tracker_spacing, heights=min_tracker_spacing, angles=0,
        units='xy', facecolors=colors, edgecolors=("black",), linewidths=(1,),
        offsets=list(zip(X, Y)), transOffset=ax.transData))
    # Similarly, add a circle for the origin
    ax.add_collection(collections.EllipseCollection(
        widths=min_tracker_spacing, heights=min_tracker_spacing, angles=0,
        units='xy', facecolors='red', edgecolors=("black",), linewidths=(1,),
        offsets=[0, 0], transOffset=ax.transData))
    ax.set_xlabel('Tracker position (east-west direction)')
    ax.set_ylabel('Tracker position (north-south direction)')
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.8,
                 label='Relative tracker height (vertical)')
    # Set limits
    lower_lim = min(min(X), min(Y)) - min_tracker_spacing
    upper_lim = max(max(X), max(Y)) + min_tracker_spacing
    ax.set_xlim(lower_lim, upper_lim)
    ax.set_ylim(lower_lim, upper_lim)
    return fig


def _polygons_to_patch_collection(geometries, **kwargs):
    """Convert Shapely Polygon or MultiPolygon to matplotlib PathCollection.

    kwargs are passed to PatchCollection
    """
    # Convert geometries to a list
    if isinstance(geometries, geometry.Polygon):
        geometries = [geometries]
    elif isinstance(geometries, geometry.MultiPolygon):
        geometries = list(geometries.geoms)
    exteriors = [patches.Polygon(g.exterior.coords) for g in geometries]
    path_collection = collections.PatchCollection(exteriors, **kwargs)
    return path_collection


def _plot_shading(active_collector_geometry, unshaded_geometry,
                  shading_geometries, min_tracker_spacing):
    """Plot the shaded and unshaded area for a specific solar position."""
    active_patches = _polygons_to_patch_collection(
        active_collector_geometry, facecolor='red', linewidth=0.5, alpha=0.5)
    unshaded_patches = _polygons_to_patch_collection(
        unshaded_geometry, facecolor='green', linewidth=0.5, alpha=0.5)
    shading_patches = _polygons_to_patch_collection(
        shading_geometries, facecolor='blue', linewidth=0.5, alpha=0.5)

    fig, axes = plt.subplots(1, 2, subplot_kw=dict(aspect='equal'))
    axes[0].set_title('Active area and shading areas')
    axes[0].add_collection(active_patches, autolim=True)
    axes[0].add_collection(shading_patches, autolim=True)
    axes[1].set_title('Unshaded area')
    axes[1].add_collection(unshaded_patches, autolim=True)
    for ax in axes:
        ax.set_xlim(-min_tracker_spacing, min_tracker_spacing)
        ax.set_ylim(-min_tracker_spacing, min_tracker_spacing)
    return fig
