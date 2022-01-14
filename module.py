import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from nba_api.stats.endpoints import shotchartdetail
import urllib.request
from matplotlib.offsetbox import  OffsetImage
import colormaps as cmaps
import ipywidgets as widgets
import nbaFuncs
import shot_chart_form
from IPython.display import display

abbrevOptions = shot_chart_form.getTeamAbbrevs()
teamNameOptions = shot_chart_form.getTeamNames()
seasonOptions = shot_chart_form.getSeasonOptions()
seasonTypeOptions = shot_chart_form.getSeasonTypeOptions()

out = widgets.Output()

playerFirstName_widget = widgets.Text(placeholder="Enter player's first name")
playerFirstName_box = widgets.HBox([widgets.Label("First Name:"), playerFirstName_widget])
display(playerFirstName_box)

playerLastName_widget = widgets.Text(placeholder="Enter player's last name")
playerLastName_box = widgets.HBox([widgets.Label("Last Name:"), playerLastName_widget])
display(playerLastName_box)

teamName_widget = widgets.Dropdown(options=teamNameOptions, value='-', disabled=False)
teamName_box = widgets.Box([widgets.Label("Player's Team:"), teamName_widget])
display(teamName_box)

playerSeason_widget = widgets.Dropdown(options=seasonOptions, value='-', disabled=False)
playerSeason_box = widgets.Box([widgets.Label("Season"), playerSeason_widget])
display(playerSeason_box)

seasonType_widget = widgets.RadioButtons(options=seasonTypeOptions,value='Regular Season', disabled=False)
seasonType_box = widgets.Box([widgets.Label("Part of Season:"), seasonType_widget])
display(seasonType_box)

submitButton = widgets.Button(
    description='Submit',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Click me',
    icon='check' # (FontAwesome names without the `fa-` prefix)
)
display(submitButton)

def on_button_clicked(b):
    
    if shot_chart_form.isValidValues(playerFirstName_widget.value,
                                     playerLastName_widget.value, 
                                     teamName_widget.value,
                                     playerSeason_widget.value,
                                     seasonType_widget.value):
        generateShotChart(playerFirstName_widget.value, playerLastName_widget.value, 
                                   teamName_widget.value, playerSeason_widget.value, seasonType_widget.value)
    else:
        print("Invalid values")

submitButton.on_click(on_button_clicked)

def generateShotChart(player_first_name, player_last_name, team_name, player_season, season_type):
    
    plt.ioff()
    
    team_id = nbaFuncs.get_team_ID(team_name)

    player_id = nbaFuncs.get_player_ID(player_first_name + " " + player_last_name)

    # Create JSON request for shot chart data
    shot_chart_json = shotchartdetail.ShotChartDetail(
                        team_id = team_id,
                        player_id = player_id,
                        context_measure_simple = "PTS",
                        season_nullable = player_season,
                        season_type_all_star = season_type)

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
                                           str(player_id) + ".png"), ("player_images/" + str(player_id) + ".png")) # Get player image from NBA website
    chart_pic = plt.imread(pictures[0]) # Extract first picture which is player head shot

    fig = plt.figure(figsize=(10,9.375))
    axis = fig.add_axes([0, 0, 1, 1])
    axis = nbaFuncs.create_court(axis, 'black')
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
            display(fig)
        
display(widgets.VBox([out]))