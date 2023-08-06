import plotly.graph_objects as go

from graph_polisher import cleaner
from graph_polisher.configs import GREY


def test_remove_grids():
    """Should set show grid to false for y and x axis"""
    fig = go.Figure()
    cleaned_fig = cleaner.remove_grids(figure=fig)
    assert not cleaned_fig.layout.xaxis.showgrid
    assert not cleaned_fig.layout.yaxis.showgrid


def test_remove_background():
    """Should set paper bg color and plot bg color to rgba(0,0,0,0)"""
    fig = go.Figure()
    cleaned_fig = cleaner.remove_background(figure=fig)
    assert cleaned_fig.layout.paper_bgcolor == 'rgba(0,0,0,0)'
    assert cleaned_fig.layout.plot_bgcolor == 'rgba(0,0,0,0)'


def test_send_to_background():
    """Should set everything grey"""
    fig = go.Figure()
    cleaned_fig = cleaner.send_to_background(figure=fig)

    assert cleaned_fig.layout.title.font.color == GREY
    assert cleaned_fig.layout.xaxis.color == GREY
    assert cleaned_fig.layout.yaxis.color == GREY
