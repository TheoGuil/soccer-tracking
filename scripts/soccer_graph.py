from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import rcParams

from mplsoccer import Pitch

from pandas import DataFrame

def get_pass_graph(df: DataFrame, mask_for_complete_pass: any, title: str) -> Figure:
    '''
    Create a pass graph. The background is a soccer field 
    and display a line for each pass.
    
    Params:
        df: DataFrame with the pass data.
            with a leat col : 'x', 'y', 'end_x', 'end_y'
        mask_for_complete_pass: The mask to apply to get the complete passes.
        title: The title of the graph.
        
    Returns: A matplotlib Figure.
    '''
    
    # Filter the passes
    df_complete_pass = df[mask_for_complete_pass]
    df_incomplete_pass = df[~mask_for_complete_pass]

    # Setup the colors
    pitch_color = '#F9F9F9'
    line_color = '#666666'
    text_color = '#080808'
    complete_pass_color = '#FFC337'
    incomplete_pass_color = '#E61415'
    
    rcParams['text.color'] = text_color
    
    # Setup the pitch
    pitch = Pitch(pitch_type='statsbomb', 
                  pitch_color=pitch_color, line_color=line_color)
    
    fig, ax = pitch.draw(figsize=(16, 11), 
                         constrained_layout=False, tight_layout=True)
    fig.set_facecolor(pitch_color)
    
    # Plot the completed passes
    lc1 = pitch.lines(
        xstart = df_complete_pass.x, 
        ystart = df_complete_pass.y,
        xend = df_complete_pass.end_x, 
        yend = df_complete_pass.end_y,
        lw=5, transparent=True, comet=True, 
        label='Completed passes',
        color=complete_pass_color, ax=ax)
    
    # Plot the other passes
    lc2 = pitch.lines(
        xstart = df_incomplete_pass.x, 
        ystart = df_incomplete_pass.y,
        xend = df_incomplete_pass.end_x, 
        yend = df_incomplete_pass.end_y,
        lw=5, transparent=True, comet=True, 
        label='Incompleted passes',
        color=incomplete_pass_color, ax=ax)
    
    
    # Plot the legend
    ax.legend(facecolor=pitch_color, edgecolor='None', 
            fontsize=20, loc='upper left', handlelength=4)

    # Set the title
    ax_title = ax.set_title(title, fontsize=30)
    
    
    
    