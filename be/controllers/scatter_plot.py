"""Creates and returns results graph."""
from sample_data import results_list,type_list,genotype_list
import plotly.graph_objects as go
import pandas as pd
import numpy as np



def scatter_graph(choice:str,possibilities:dict):
    """Create a plot given a choice and a dictionary with whoso keys are possibilities and values are dataframes."""
    paleta=(["#95BFE1","#E83283","#42D7A7","#38CBFB","#d6e649","#f230a1","#30bff2","#f24730","#8c7649","#498c6f","#74678f"])
    N=len(paleta)
    graph = go.Figure()
    count=0
    for possibility in list(possibilities.keys()):
        if possibility == choice:
            visibility = True
        else:
            visibility = 'legendonly'
        graph.add_trace(go.Scatter(x=possibilities[possibility]["x"], y= possibilities[possibility]["y"],mode="markers+lines", name=possibility, showlegend=True, visible=visibility,fill="tonexty",line=dict(color=paleta[count%N])))
        count=count+1
    graph.update_yaxes(title_text='Tests')
    graph.update_layout(margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin

    ),
    height=350,
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)',
    paper_bgcolor= 'rgba(0, 0, 0, 0)',
    )
    return graph