from nba_api.stats.static import teams, players
import matplotlib as mpl
from matplotlib.pyplot import axis

nba_teams = teams.get_teams()
nba_players = players.get_players()

# Function definitions
def get_team_ID(team_check):
    team_info = [team for team in nba_teams if team['full_name'] == team_check][0]

    if team_info is None:
        return -1
    else:
        return team_info['id']



def get_player_ID(name_check):
    player_info = [player for player in nba_players if player['full_name'] == name_check][0]

    if player_info is None:
        return -1
    else:
        return player_info['id']

def create_court(axis, color='black'):
    # Add short corner 3pt lines
    axis.plot([-220,-220], 
              [0,140], 
              linewidth=2, 
              color=color)
    axis.plot([220,220], 
              [0,140], 
              linewidth=2, 
              color=color)
    
    # Add 3pt arc
    axis.add_artist(mpl.patches.Arc((0,140), 
                                    440, 
                                    315, 
                                    theta1=0, 
                                    theta2=180, 
                                    facecolor='none', 
                                    edgecolor=color, 
                                    lw=2))
    
    # Add the lane and key
    axis.plot([-80,-80], 
              [0,190], 
              linewidth=2, 
              color=color)
    axis.plot([80,80], 
              [0,190], 
              linewidth=2, 
              color=color)
    axis.plot([-60,-60], 
              [0,190], 
              linewidth=2, 
              color=color)
    axis.plot([60,60], 
              [0,190], 
              linewidth=2, 
              color=color)
    axis.plot([-80,80], 
              [190,190], 
              linewidth=2, 
              color=color)
    axis.add_artist(mpl.patches.Circle((0,190), 
                                       60, 
                                       facecolor='none', 
                                       edgecolor=color, 
                                       lw=2))
    
    # Add the rim
    axis.add_artist(mpl.patches.Circle((0,60), 
                                       15, 
                                       facecolor='none', 
                                       edgecolor=color, 
                                       lw=2))
    
    # Add the backboard
    axis.plot([-30,30], 
              [40,40], 
              linewidth=2, 
              color=color)
    
    # Remove ticks
    axis.set_xticks([])
    axis.set_yticks([])
    
    # Add halfcourt arcs
    axis.add_artist(mpl.patches.Arc((0, 470), 
                                    120, 
                                    120, 
                                    theta1=180, 
                                    theta2=0,
                                    linewidth=2, 
                                    color=color))
    axis.add_artist(mpl.patches.Arc((0, 470), 
                                    40, 
                                    40, 
                                    theta1=180, 
                                    theta2=0,
                                    linewidth=2, 
                                    color=color))
    
    # Set the axis limits
    axis.set_xlim(-250,250)
    axis.set_ylim(0,470)
    
    return axis