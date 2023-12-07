from matplotlib.figure import Figure
from matplotlib import rcParams
from matplotlib.colors import to_rgba
import plotly.graph_objects as go

from pandas import DataFrame
import numpy as np

from mplsoccer import Pitch

# Setup the colors
pitch_color = '#F9F9F9'
line_color = '#666666'
text_color = '#080808'
complete_pass_color = '#FFC337'
incomplete_pass_color = '#E61415'

def get_pass_graph(df: DataFrame, mask_for_complete_pass: any, title: str, pitch_type:str = "custom") -> Figure:
    '''
    Create a pass graph. The background is a soccer field 
    and display a line for each pass.
    
    Params:
        df: DataFrame with the pass data.
            with at least col : 'x', 'y', 'end_x', 'end_y'
        mask_for_complete_pass: The mask to apply to get the complete passes.
        title: The title of the graph.
        pitch_type: The type of pitch to display.
        
    Returns: A matplotlib Figure.
    '''
    
    # Filter the passes
    df_complete_pass = df[mask_for_complete_pass]
    df_incomplete_pass = df[~mask_for_complete_pass]
    
    rcParams['text.color'] = text_color
    
    # Setup the pitch
    pitch = Pitch(pitch_type=pitch_type, 
                  pitch_color=pitch_color, line_color=line_color,
                  pitch_length = 105, pitch_width=68)
    
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
    
    return fig
    
def get_pass_network(df_position: DataFrame, df_passes: DataFrame, title: str, pitch_type:str = "custom") -> Figure:
    '''
    Create a pass network graph. Each player is represented by a node at
    the average position of the player. The size of the node is proportional
    to the number of passes made or received. The line represents the passes
    between the players.
    
    Params:
        df_position: DataFrame with the mean position of the players.
            with at least col : 'x', 'y', 'count'
        df_passes: DataFrame with the pass data between two players.
            with at least col : 'pass_count', 'x', 'y', 'end_x', 'end_y'
        title: The title of the graph.
        pitch_type: The type of pitch to display.
    '''
    # Calculate the line width
    MAX_LINE_WIDTH = 18
    MAX_MARKER_SIZE = 3000
    df_passes['width'] = (df_passes.pass_count / df_passes.pass_count.max() * MAX_LINE_WIDTH)
    df_position['marker_size'] = (df_position['count'] / df_position['count'].max() * MAX_MARKER_SIZE)
        
    # Add transparency to the line
    MIN_TRANSPARENCY = 0.3
    color = np.array(to_rgba('red'))
    color = np.tile(color, (len(df_passes), 1))
    c_transparency = df_passes.pass_count / df_passes.pass_count.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency
    
    # Plot
    pitch = Pitch(pitch_type=pitch_type, 
              pitch_color=pitch_color, line_color=line_color,
              pitch_length = 105, pitch_width=68)

    fig, ax = pitch.draw(figsize=(16, 11), 
                        constrained_layout=True, tight_layout=False)

    fig.set_facecolor(pitch_color)
    pass_lines = pitch.lines(
        df_passes.x, 
        df_passes.y,
        df_passes.x_end, 
        df_passes.y_end, 
        lw=df_passes.width,
        color=color, zorder=1, ax=ax)

    pass_nodes = pitch.scatter(
        df_position.x, 
        df_position.y,
        s=df_position.marker_size,
        color=complete_pass_color, edgecolors=line_color, linewidth=1, alpha=1, ax=ax)

    for index, row in df_position.iterrows():
        pitch.annotate(
            row.PlayerID,
            xy=(row.x, row.y), c=pitch_color,
            va='center', ha='center', 
            size=16, weight='bold', ax=ax)
    
    # Set the title
    ax_title = ax.set_title(title, fontsize=30)
    
    return fig

def get_performance_chart(team_stats: DataFrame, stats: list[str], stats_per: list[str], stats_label: list[str], 
                          team_label: list[str], team_color: list[str])-> Figure:
    '''
    Create a horizontal bar chart to compare the performance of two teams.
    
    Params:
        team_stats: DataFrame with the stats of the teams.
        stats: List of the stats.
        stats_per: List of the stats in percentage.
        stats_label: List of the stats label.
        team_label: List of the team label.
        team_color: List of the team color.
    
    Returns:
        A matplotlib Figure.
    '''
    fig = go.Figure()
    for index, team in enumerate(team_stats.index):
        fig.add_trace(go.Bar(
            x=team_stats.loc[team, stats_per].values, 
            y=stats_label, 
            name=team_label[index], 
            orientation='h',
            marker=dict(color=team_color[index])))
    
    annotations = []
    for index, stat in enumerate(stats):
        annotations.append(
            dict(xref='x', yref='y', x=0.1, y=index, 
                text=str(round(team_stats.loc[team_stats.index[0], [stat]].values[0], 2)), 
                showarrow=False, 
                font=dict(color="white", size=14))
    )
        annotations.append(
            dict(xref='x', yref='y', x=0.9, y=index, 
                text=str(round(team_stats.loc[team_stats.index[1], [stat]].values[0], 2)), 
                showarrow=False, 
                font=dict(color="white", size=14))
    )
    
    fig.update_layout(barmode='relative', title_text='Performance', annotations=annotations, xaxis=dict(visible=False))

    return fig