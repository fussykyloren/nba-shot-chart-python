import ipywidgets as widgets
import ipyForm.form_funcs as form_funcs
from IPython.display import display
from ipyForm.generate_shot_chart import generateShotChart

abbrevOptions = form_funcs.getTeamAbbrevs()
teamNameOptions = form_funcs.getTeamNames()
seasonOptions = form_funcs.getSeasonOptions()
seasonTypeOptions = form_funcs.getSeasonTypeOptions()

out = widgets.Output()

playerFirstName_widget = widgets.Text(placeholder="Enter player's first name")
playerFirstName_box = widgets.VBox([widgets.Label("First Name:"), playerFirstName_widget])
display(playerFirstName_box)

playerLastName_widget = widgets.Text(placeholder="Enter player's last name")
playerLastName_box = widgets.VBox([widgets.Label("Last Name:"), playerLastName_widget])
display(playerLastName_box)

teamName_widget = widgets.Dropdown(options=teamNameOptions, value='-', disabled=False)
teamName_box = widgets.VBox([widgets.Label("Player's Team:"), teamName_widget])
display(teamName_box)

playerSeason_widget = widgets.Dropdown(options=seasonOptions, value='-', disabled=False)
playerSeason_box = widgets.VBox([widgets.Label("Season (Optional):"), playerSeason_widget])
display(playerSeason_box)

seasonType_widget = widgets.RadioButtons(options=seasonTypeOptions,value='Regular Season', disabled=False)
seasonType_box = widgets.VBox([widgets.Label("Part of Season (Optional):"), seasonType_widget])
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
    
    if form_funcs.isValidValues(playerFirstName_widget.value,
                                     playerLastName_widget.value, 
                                     teamName_widget.value,
                                     playerSeason_widget.value,
                                     seasonType_widget.value):
        generateShotChart(playerFirstName_widget.value, playerLastName_widget.value, 
                          teamName_widget.value, playerSeason_widget.value, 
                          seasonType_widget.value, out)
    else:
        print("Invalid values")

submitButton.on_click(on_button_clicked)
        
display(widgets.VBox([out]))