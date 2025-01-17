# %%
import panel as pn
from final.weather_functions import get_weather, wkeys, StaNames
from final.plot_functions import plot_forecasts

# learned from our mistakes
pn.extension('plotly')

# %% [markdown]
# #### Chceme si zvoliť, aké grafy budeme zobrazovať

# %%
# what values can we choose to show on plots?
wkeys

# %%
observ_choice = pn.widgets.CheckBoxGroup(options=wkeys, value=['temp', 'clouds'], width=200)
observ_choice


# %% [markdown]
# #### Nechceme, aby sa zobrazovalo 6 grafov, trvá to dlhšie a zahltí to miesto na obrazovke...  
# #### A k tomu všetkému ešte vznikajú bugy s výškou grafov...  
# #### Čo ak chceme zobraziť len max 3 grafy?

# %% [markdown]
# ### <b>Interaktivita inak - Eventy (Udalosti)</b>

# %% [markdown]
# #### **Event** - signalizuje zmenu hodnoty parametra, obsahuje užitočné atribúty poskytujúce informácie ohľadom udalosti
# - **name**: Názov zmeneného parametra
# - **new**: Nová hodnota parametra 
# - **old**: Stará hodnota parametra (pred zmenou)
# - **type**: Typ eventu (`'triggered', 'changed'` alebo `'set'`)
# - **what**: Čo sa zmenilo (väčšinou `'value'`)
# - obj: Konkrétny objekt ktorý vyvolal udalosť
# - cls: Trieda objektu   

# %%
def print_event(*events):  # *events - any number of arguments
    for event in events:
        print(event)

        
# widget_name.param.watch( function_name, list of values to watch, e.g. value, other parameters...)
watcher_print_event = observ_choice.param.watch(print_event, ['value'], onlychanged=True)

# %%
observ_choice

# %%
# cancel printing values
observ_choice.param.unwatch(watcher_print_event)

# %%
# to prevent further disaster, set the value to temp (or anything that is max 3 values)
observ_choice.value = ['temp']

def set_observ(*events):  
    for event in events:
        if event.type == "changed" and (len(event.new) > 3 or len(event.new) == 0):
            observ_choice.value = event.old
            
observ_watcher = observ_choice.param.watch(set_observ, ['value'], onlychanged=True)

# %%
observ_choice

# %%
station_choice = pn.widgets.Select(name="Select a station", options=StaNames, width=200)

@pn.depends(station_choice, observ_choice)
def view_hourly(station_choice, observ_choice):
    data = get_weather(station_choice)
    fig = plot_forecasts(data, 'hourly', values=observ_choice)
    return fig


options = pn.Column(station_choice, observ_choice)
pn.Row(options, view_hourly)

# %%
