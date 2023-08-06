"""
Tests for coast
"""
import pytest

from .. import Figure
from ..helpers.testing import check_figures_equal


@pytest.mark.mpl_image_compare
def test_coast():
    "Simple plot from the GMT docs"
    fig = Figure()
    fig.coast(
        R="-30/30/-40/40",
        J="m0.1i",
        B=5,
        I="1/1p,blue",
        N="1/0.25p,-",
        W="0.25p,white",
        G="green",
        S="blue",
        D="c",
        A=10000,
    )
    return fig


@check_figures_equal()
def test_coast_iceland():
    "Test passing in R as a list"
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="-30/-10/60/65", J="m1c", B="", G="p28+r100")
    fig_test.coast(
        region=[-30, -10, 60, 65], projection="m1c", frame=True, land="p28+r100"
    )
    return fig_ref, fig_test


@pytest.mark.mpl_image_compare
def test_coast_aliases():
    "Test that all aliases work"
    fig = Figure()
    fig.coast(
        region="-30/30/-40/40",
        projection="m0.1i",
        frame="afg",
        rivers="1/1p,black",
        borders="1/0.5p,-",
        shorelines="0.25p,white",
        land="moccasin",
        water="skyblue",
        resolution="i",
        area_thresh=1000,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_coast_world_mercator():
    "Test passing generating a global Mercator map with coastlines"
    fig = Figure()
    fig.coast(
        region=[-180, 180, -80, 80],
        projection="M10i",
        frame="af",
        land="#aaaaaa",
        resolution="l",
        water="white",
    )
    return fig
