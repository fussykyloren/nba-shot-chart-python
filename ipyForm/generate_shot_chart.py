from nba_api.stats.endpoints import shotchartdetail
import json
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import urllib.request
from matplotlib.offsetbox import  OffsetImage
import shotCharts.colormaps as cmaps
from IPython.display import display, clear_output
import ipyForm.create_court as court
import ipyForm.form_funcs as form_funcs

def generateShotChart(player_first_name, player_last_name, team_name, player_season, season_type, out):
    
    team_id = form_funcs.get_team_ID(team_name)

    player_id = form_funcs.get_player_ID(player_first_name + " " + player_last_name)

    # Create JSON request for shot chart data
    shot_chart_json = shotchartdetail.ShotChartDetail(
                        team_id = team_id,
                        player_id = player_id,
                        context_measure_simple = "PTS",
                        #season_nullable = player_season,
                        #season_type_all_star = season_type
    )

    # Load shot chart data into a dictionary
    shot_chart_data = json.loads(shot_chart_json.get_json())

    # Grab the data that is relevant to make the short chart
    shot_chart_relevant_data = shot_chart_data['resultSets'][0]
    # Get the headers
    headers = shot_chart_relevant_data['headers']
    # Get the row data
    rows = shot_chart_relevant_data['rowSet']

    # Create the pandas DataFrame
    player_data = pd.DataFrame(rows)
    player_data.columns = headers

    mpl.rcParams['font.family'] = 'Avenir' # Set plot font
    mpl.rcParams['font.size'] = 18 # Set plot font size
    mpl.rcParams['axes.linewidth'] = 2 # Set universal plot linewidths

    pictures = urllib.request.urlretrieve(("https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" +
                                           str(player_id) + ".png"), ("output/player_headshots/" + str(player_id) + ".png")) # Get player image from NBA website
    chart_pic = plt.imread(pictures[0]) # Extract first picture which is player head shot

    fig = plt.figure(figsize=(10,9.375))
    axis = fig.add_axes([0, 0, 1, 1])
    axis = court.create_court(axis, 'black')
    cmap = plt.get_cmap(cmaps.viridis)

    axis.hexbin(player_data["LOC_X"], 
                (player_data["LOC_Y"] + 60), 
                gridsize=(30,30), 
                extent=(-300,300,0,940), 
                bins='log',
                cmap=cmap)
    axis.text(0, 
            1.05, 
            (player_first_name + " " + player_last_name + "\n" + team_name + "\n" + player_season + " " + season_type), 
            transform=axis.transAxes, 
            ha="left", 
            va="baseline", 
            fontsize=24)

    img = OffsetImage(chart_pic, zoom=0.7)
    img.set_offset((558,685))
    axis.add_artist(img)

    axis2 = fig.add_axes([1.01, 0.1, 0.02, 0.8])
    axis2.yaxis.tick_right()

    cb = mpl.colorbar.ColorbarBase(axis2, 
                                cmap=cmap, 
                                orientation='vertical')
    cb.set_label('Shooting %')
    cb.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cb.set_ticklabels(['0%','25%', '50%','75%', '100%'])

    # fig.savefig('output/rwest2016.jpg', bbox_inches='tight', transparent=True)
    with plt.ioff():
        with out:
            clear_output()
            display(fig)