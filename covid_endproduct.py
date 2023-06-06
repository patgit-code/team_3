import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import numpy as np
from pandas.api.types import CategoricalDtype
import geopandas as gpd
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.palettes import brewer


# Bild als Header für den Benutzer als Einstieg in den Artikel
image = "pexels-photo-3943882.jpeg"
st.image(image)
st.caption('Bild von Pexels')

# Titel des Artikel mit Unterschrift
st.title(body='Ein Rückblick auf die Pandemie im deutschsprachigen Raum. Was können wir davon mitnehmen?')
st.subheader(
    'Es ist bereits ein Jahr her, seit die Massnahmen gegen Covid-19 in Deutschland, Österreich und der Schweiz '
    'aufgehoben wurden. Das Leben hat sich wieder normalisiert und der Virus verschwindet langsam aus unseren Köpfen. '
    'Doch was können wir aus der vergangenen Pandemie lernen?')

# Umstände
st.header('Verlauf des Virus')
st.subheader('')

#Erläuterung zur Grafik
st.text("Die Schweiz implementierte im Vergleich zu Österreich und Deutschland als letzte \n"
        "erste Coronamassnahmen. Auch im Verlauf der Pandemie waren die Massnahmen \n"
         "verglichen mit unseren Nachbarsländern stets weniger streng. In Betracht auf  \n"
        "die Fallzahlen, war die Schweiz auf Platz zwei mit durchschnittlich 50'573 Fällen \n"
        "auf 100'000 Einwohner.")
st.text("Anfang des Jahres 2022 gab es in allen drei Ländern eine drastische Steigung der \n"
        "Fallzahlen. Dies vor allem deswegen, weil die Massnahmen gelockert wurden und \n" 
        "die Bevölkerung fahrlässiger handelte. Da zu diesem Zeitpunkt die Impfungen schon \n" 
        "recht fortgeschritten waren, nahm man die ganze Situation etwas lockerer.")

# TODO Start all Visualisations at the same date
# TODO Get Info how many tests were made at start and end of pandemic
# TODO check if WHO-COVID-19-global-data has all austria and germany than we make all the graphs with the same data

# Schweiz
st.subheader('Schweiz')
st.text('Der Verlauf in der Schweiz...')

# Lesen des WHO Datensatz für den die drei Visualisierungen erstellt werden.
covid_ww = pd.read_csv(os.path.join('data', 'WHO-COVID-19-global-data.csv'))

# Datum in DateTime-Format konvertieren
covid_ww['Date_reported'] = pd.to_datetime(covid_ww['Date_reported'])

# Daten für die Schweiz filtern
switzerland = covid_ww[covid_ww['Country_code'] == 'CH']

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
switzerland_quarterly = switzerland.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Liniendiagramm erstellen
fig, ax_virus_process_switzerland = plt.subplots()
#
ax_virus_process_switzerland.ticklabel_format(style='plain')
ax_virus_process_switzerland.plot(switzerland_quarterly.index, switzerland_quarterly['Cumulative_cases'])

# TODO add source for all three countries
# Start der Corona Massnahmen für die Schweiz (Quelle: )
start_date_switzerland = pd.to_datetime('2020-03-16')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_switzerland, 0, max(switzerland_quarterly['Cumulative_cases']),
            label='Start der Corona Massnahmen am 16.03.2020', color='red')

# Legenden für den Leser damit die Linie verständlich ist
plt.legend()

plt.xlabel('Quartal')
plt.ylabel('Kumulative Fälle')
plt.title('Kumulative COVID-19-Fälle in der Schweiz (quartalsweise)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)

st.pyplot(fig)

# Deutschland
st.subheader('Deutschland')

# Daten einlesen
#df = pd.read_csv('data//Aktuell Deutschland COVID Infektionen.csv', delimiter=';')

# Meldedatum in DateTime-Format umwandeln
#df['Meldedatum'] = pd.to_datetime(df['Meldedatum'])

# Daten für Deutschland filtern
germany_process_data = covid_ww[covid_ww['Country_code'] == 'DE']

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
germany_quarterly = germany_process_data.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Gruppieren nach Meldedatum und Summieren der Anzahl der Fälle
#daily_cases = df.groupby('Meldedatum')['AnzahlFall'].sum().reset_index()

# Liniendiagramm erstellen
fig, ax_virus_process_germany = plt.subplots()

ax_virus_process_germany.ticklabel_format(style='plain')
ax_virus_process_germany.plot(germany_quarterly.index, germany_quarterly['Cumulative_cases'])

#ax_virus_process_switzerland.plot(switzerland_quarterly.index, switzerland_quarterly['Cumulative_cases'])

plt.xlabel('Datum')
plt.ylabel('Anzahl der Fälle')
plt.title('COVID-Fälle in Deutschland')

# Start der Corona Massnahmen in Deutschland (Quelle: )
start_date_germany = pd.to_datetime('2020-02-27')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_germany, 0, max(germany_quarterly['Cumulative_cases']), label='Start der Corona Massnahmen am 27.02.2020',
            color='red')
# Legenden für den Leser damit die Linie verständlich ist
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
st.pyplot(fig)

# Österreich
st.subheader('Österreich')

st.text('Im Vergleich mit Deutschland und der Schweiz hat Österreich...')

# Summe der Covid-Fälle für alle Daten berechnen
#total_cases = dat.groupby('Time')['Anzahl'].sum()

# Daten für Österreich filtern
austria_process_data = covid_ww[covid_ww['Country_code'] == 'AT']

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
austria_quarterly = austria_process_data.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Linien-Diagramm erstellen
fig, ax_virus_process_austria = plt.subplots()
ax_virus_process_austria.ticklabel_format(style='plain')
ax_virus_process_austria.plot(austria_quarterly.index, austria_quarterly['Cumulative_cases'])

# Start der Corona Massnahmen in Österreich (Quelle: )
start_date_austria = pd.to_datetime('2020-03-11')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_austria, 0, max(austria_quarterly['Cumulative_cases']), label='Start der Corona Massnahmen am 11.03.2020',
            color='red')
# Legenden für den Leser damit die Linie verständlich ist
plt.legend()

plt.xlabel('Datum')
plt.ylabel('Anzahl der Covid-Fälle')
plt.title('Covid-Fälle in Österreich')
plt.xticks(rotation=45)
plt.grid(True)

# Diagramm anzeigen
st.pyplot(fig)

st.header('Todesfälle (Heatmaps)')
st.subheader('')
st.text('')

# Schweiz
st.subheader('Schweiz')
st.text('In der Schweiz sind vor allem ältere Menschen, ab 70 Jahren gestorben und dies \n'
        'mehrheitlich zu Beginn der Pandemie 2021. Ende 2021 / Beginn 2022 stiegen die \n'
        'Zahlen nochmals, weshalb auch da eine höhere Todesrate ersichtlich ist.')
# Daten laden
data = pd.read_csv("data//COVID19Death_geoRegion_AKL10_w.csv")

# Filtern der Daten von 2021 bis 2023
data = data[data['datum'].astype(str).str[:4].astype(int).between(2021, 2023)]

#Zeilen mit Unbekannt löschen
data = data[data['altersklasse_covid19'] != 'Unbekannt']


# Extrahieren des Quartals aus dem Datum
data['quartal'] = data['datum'].astype(str).str[:4] + '-Q' + data['datum'].astype(str).str[4:5]

# Pivot-Tabelle erstellen
pivot_table = pd.pivot_table(data, values='entries', index='altersklasse_covid19', columns='quartal')

# Farbpalette definieren
cmap = sns.color_palette("Reds", as_cmap=True)

# Heatmap erstellen
fig = plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap=cmap, annot=True, fmt='.2f', cbar=True)
plt.xlabel('Quartal')
plt.ylabel('Altersklasse')
plt.title('Prozentuale Verteilung der Todesfälle nach Quartal und Altersgruppe in der Schweiz')

plt.tight_layout()
st.pyplot(fig)

# Deutschland
st.subheader('Deutschland')

# Daten laden
df = pd.read_csv("data//Aktuell Deutschland COVID Infektionen.csv", delimiter=';')

# Datumsspalten in datetime umwandeln
df['Meldedatum'] = pd.to_datetime(df['Meldedatum'], format='%Y-%m-%d')
df['Refdatum'] = pd.to_datetime(df['Refdatum'], format='%Y-%m-%d')

# Filtern der Daten von 2021 bis 2023
df = df[df['Meldedatum'].dt.year.between(2021, 2023)]

# Quartalsinformationen hinzufügen
df['Quarter'] = df['Meldedatum'].dt.to_period('Q')

# Pivot-Tabelle erstellen
pivot_table = pd.pivot_table(df, values='AnzahlTodesfall', index='Altersgruppe', columns='Quarter', aggfunc='sum',
                             fill_value=0)

# Quartalsüberschriften formatieren
quarter_labels = pivot_table.columns.strftime('%Y Q%q')

# Konvertieren in Prozentsätze
percentage_table = pivot_table.apply(lambda x: (x / x.sum()) * 100, axis=1)

# Farbpalette definieren
cmap = sns.color_palette("Reds", as_cmap=True)

# Heatmap erstellen
fig = plt.figure(figsize=(12, 8))
sns.heatmap(percentage_table, cmap=cmap, annot=True, fmt='.1f', cbar=True)
plt.xlabel('Quartal')
plt.ylabel('Altersgruppe')
plt.title('Prozentuale Verteilung der Todesfälle nach Quartal und Altersgruppe in Deutschland')
plt.xticks(ticks=np.arange(len(quarter_labels)) + 0.5, labels=quarter_labels, rotation=45, ha='right')
plt.yticks(rotation=0)

# Anpassung der Farbskala basierend auf den Werten
norm = plt.Normalize(percentage_table.min().min(), percentage_table.max().max())
heatmap = sns.heatmap(percentage_table, cmap=cmap, annot=True, fmt='.1f', cbar=True, norm=norm)
heatmap.collections[0].colorbar.set_label("Prozent")

# Hinzufügen von Linien zur besseren Sichtbarkeit der Quadrate
plt.hlines(np.arange(0.5, len(percentage_table)), *plt.xlim(), colors='white', linewidths=0.5)
plt.vlines(np.arange(0.5, len(percentage_table.columns)), *plt.ylim(), colors='white', linewidths=0.5)

plt.tight_layout()

st.pyplot(fig)

# Österreich
st.subheader('Österreich')

# CSV-Daten laden
dat = pd.read_csv("data//CovidFaelle_Altersgruppe.csv", delimiter=';')

# Konvertiere 'Time' in ein Datumsformat
dat['Time'] = pd.to_datetime(dat['Time'], format='%d.%m.%Y %H:%M:%S')

# Filtern der Daten von 2021 bis 2023
dat = dat[dat['Time'].dt.year.between(2021, 2023)]

# Quartalsinformationen hinzufügen
dat['Quarter'] = dat['Time'].dt.to_period('Q')

# Pivot-Tabelle erstellen
pivot_table = pd.pivot_table(dat, values='AnzahlTot', index='Altersgruppe', columns='Quarter')

# Quartalsüberschriften formatieren
quarter_labels = pivot_table.columns.strftime('%Y Q%q')

# Konvertieren in Prozentsätze
percentage_table = pivot_table.apply(lambda x: (x / x.sum()) * 100, axis=1)

# Farbpalette definieren
cmap = sns.color_palette("Reds", as_cmap=True)

# Heatmap erstellen
fig = plt.figure(figsize=(12, 8))
sns.heatmap(percentage_table, cmap=cmap, annot=True, fmt='.1f', cbar=True)
plt.xlabel('Quartal')
plt.ylabel('Altersgruppe')
plt.title('Prozentuale Verteilung der Todesfälle nach Quartal und Altersgruppe in Österreich')
plt.xticks(ticks=np.arange(len(quarter_labels)) + 0.5, labels=quarter_labels, rotation=45, ha='right')
plt.yticks(rotation=0)

# Anpassung der Farbskala basierend auf den Werten
norm = plt.Normalize(percentage_table.min().min(), percentage_table.max().max())
heatmap = sns.heatmap(percentage_table, cmap=cmap, annot=True, fmt='.1f', cbar=True, norm=norm)
heatmap.collections[0].colorbar.set_label("Prozent")

# Hinzufügen von Linien zur besseren Sichtbarkeit der Quadrate
plt.hlines(np.arange(0.5, len(percentage_table)), *plt.xlim(), colors='white', linewidths=0.5)
plt.vlines(np.arange(0.5, len(percentage_table.columns)), *plt.ylim(), colors='white', linewidths=0.5)

plt.tight_layout()
st.pyplot(fig)

st.header('Geografische Verteilung')
st.subheader('Wo sind die unterschieder der Todesfälle. \
Können wir einen Unterschied sehen zwischen den Kantonen bzw. Bundesländer? \
Gibt es einen Unterschied zwischen dem Land und der Stadt')

# Schweiz
# static map

st.subheader('Schweiz')

population = pd.read_csv("data//population.csv", delimiter=';')

# TODO REMOVE THIS CODE AND SAVE TO CORRECTED CSV in a seperate folder in teams \
#  so we load the already corrected data into the streamlit
# any other changes to the data should be done in a def function above \
# so this is better readable aka def the graph above and here we can see the structure of the article
# TODO add comments to this and remove any not needed code

# Shapefile der Schweiz von admin.ch laden. (https://www.swisstopo.admin.ch/de/geodata/landscape/boundaries3d.html)
# Wir wählen die Kantonsgebiet Variante, für die Visualisierung.
cantons = gpd.read_file("data//shapefiles//swissboundaries//swissBOUNDARIES3D_1_4_TLM_KANTONSGEBIET.shp")

# Lesen der Datei mit den Informationen zu den Anzahl Todesfälle pro Kanton
death = pd.read_csv("data//COVID19Death_geoRegion.csv")

# Bereinigen der Daten. Georegion CH ist zu allgemein und kann nicht auf der Karte angezeigt werden.
# CHFL (Liechtenstein) ist nicht auf der Karte ersichtlich und kann ebenfalls entfernt werden.
# NA (Not Available) kann auch nicht auf der Karte dargestellt werden und kann auch entfernt werden.
death.drop(death[death['geoRegion'] == 'CH'].index, inplace=True)
death.drop(death[death['geoRegion'] == 'CHFL'].index, inplace=True)
death.drop(death[death['entries'] == 'NA'].index, inplace=True)
death_count_canton = death.groupby('geoRegion')['entries'].sum().reset_index()

# Erstellen von einem Dictionary damit die unterschiedlichen Notationen, in das Geo Dataframe gemapped werden kann.
dict_canton = {
    "Graubünden": "GR",
    "Bern": "BE",
    "Valais": "VS",
    "Vaud": "VD",
    "Ticino": "TI",
    "St. Gallen": "SG",
    "Zürich": "ZH",
    "Fribourg": "FR",
    "Luzern": "LU",
    "Aargau": "AG",
    "Uri": "UR",
    "Thurgau": "TG",
    "Schwyz": "SZ",
    "Jura": "JU",
    "Neuchâtel": "NE",
    "Solothurn": "SO",
    "Glarus": "GL",
    "Basel-Landschaft": "BL",
    "Obwalden": "OW",
    "Nidwalden": "NW",
    "Genève": "GE",
    "Schaffhausen": "SH",
    "Appenzell Ausserrhoden": "AR",
    "Zug": "ZG",
    "Appenzell Innerrhoden": "AI",
    "Basel-Stadt": "BS"
}

# Erstellen der Spalte für die Todesfälle
cantons['deaths'] = ''
cantons['Population'] = ''
cantons['ProcentageOfDeathPop'] = ''
cantons['YearOfPopulation'] = ''

# Setzen der Todesfälle auf den korrekten Kanton.
# Die Todesfälle müssen auf int gecastet werden, ansonsten wirft GeoJSONDataSource einen Fehler
for index, row in cantons.iterrows():
    cantons.loc[index, 'deaths'] = \
    int(death_count_canton[death_count_canton['geoRegion'] == dict_canton[row['NAME']]]['entries'].values[0])
    cantons.loc[index, 'Population'] = \
    int(population[population['Bundesländer'] == row['NAME']]['Population'].values[0])
    cantons.loc[index, 'YearOfPopulation'] = \
    int(population[population['Bundesländer'] == row['NAME']]['Stand'].values[0])
    cantons.loc[index, 'ProcentageOfDeathPop'] = \
    "{:.2f}".format((death_count_canton[death_count_canton['geoRegion'] == dict_canton[row['NAME']]]['entries'].values[0] /
    population[population['Bundesländer'] == row['NAME']]['Population'].values[0]) * 100000)

geo_source_switzerland = GeoJSONDataSource(geojson=cantons.to_json())

bokeh_swiss = figure(tools='wheel_zoom, hover')

# Entfernen der Raster und Achsen
bokeh_swiss.axis.visible = False
bokeh_swiss.xgrid.visible = False
bokeh_swiss.ygrid.visible = False
bokeh_swiss.outline_line_color = None
bokeh_swiss.background_fill_color = None

# Grösse des Graphen auf die Breite skalieren
bokeh_swiss.sizing_mode = 'scale_width'

# Erstellen der Karte und befüllen mit Farbe
bokeh_swiss.patches('xs', 'ys', fill_alpha=1.0, line_width=0.0, source=geo_source_switzerland, fill_color="#008800")

# Hover Tool für die Todesfälle erstellen.
# Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
hover_switzerland = bokeh_swiss.select(dict(type=HoverTool))
hover_switzerland.tooltips = [
    ("Kanton", "@NAME"), ("Todesfälle", "@deaths"),
    ("Bevölkerung", "@Population"), ("Stand","@YearOfPopulation"),
    ("Prozentualer Anteil der Todesfälle pro Bevölkerung", '@ProcentageOfDeathPop')
                              ]
hover_switzerland.mode = 'mouse'

# Anzeigen der Karte
st.bokeh_chart(bokeh_swiss)

# Deutschland
st.subheader('Deutschland')

# TODO ungefähre Anzahl pro Bundesland bzw. Land / Menschen Ratio herraussuchen
# TODO explain this csv where did we get the data here
death_de = pd.read_csv("data//statistic_id1100750_fallzahl-des-coronavirus--covid-19--nach-bundeslaendern-2023.csv",
                 delimiter = ';')

# Shapefile Deutschland von bund.de laden. (https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete.html)
# Wir wählen die Bundesland Variante, für die Visualisierung.
germany = gpd.read_file("data//shapefiles//deutschland//vg2500_bld.shp")

# Erstellen der Spalte für die Todesfälle
germany['Deaths'] = ''
germany['Population'] = ''
germany['ProcentageOfDeathPop'] = ''
germany['YearOfPopulation'] = ''
# Infos zu den Bevölkerunganzahl von Statista (https://de.statista.com/statistik/daten/studie/75536/umfrage/schweiz-bevoelkerung-nach-kanton-zeitreihe/)

# Setzen der Todesfälle auf den korrekten Kanton.
# Die Todesfälle müssen auf int gecastet werden, ansonsten wirft GeoJSONDataSource einen Fehler
for index, row in germany.iterrows():
    germany.loc[index, 'Deaths'] = \
    int(death_de[death_de['Bundesländer'] == row['GEN']]['Todesfälle'].values[0])
    germany.loc[index, 'Population'] = \
    int(population[population['Bundesländer'] == row['GEN']]['Population'].values[0])
    germany.loc[index, 'YearOfPopulation'] = \
    int(population[population['Bundesländer'] == row['GEN']]['Stand'].values[0])
    germany.loc[index, 'ProcentageOfDeathPop'] = \
    "{:.2f}".format((death_de[death_de['Bundesländer'] == row['GEN']]['Todesfälle'].values[0] /
    population[population['Bundesländer'] == row['GEN']]['Population'].values[0]) * 100000)

geo_source_germany = GeoJSONDataSource(geojson=germany.to_json())

bokeh_germany = figure(tools='wheel_zoom, hover')

# Entfernen der Raster und Achsen
bokeh_germany.axis.visible = False
bokeh_germany.xgrid.visible = False
bokeh_germany.ygrid.visible = False
bokeh_germany.outline_line_color = None
bokeh_germany.background_fill_color = None

# Grösse des Graphen auf die Breite skalieren
bokeh_germany.sizing_mode = 'scale_width'

# Erstellen der Karte und befüllen mit Farbe
bokeh_germany.patches('xs', 'ys', fill_alpha=1.0, line_width=0.0, source=geo_source_germany, fill_color="#008800")

# Hover Tool für die Todesfälle erstellen.
# Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
hover_germany = bokeh_germany.select(dict(type=HoverTool))
hover_germany.tooltips = [
    ("Bundesland", "@GEN"), ("Todesfälle", "@Deaths"),
    ("Bevölkerung", "@Population"), ("Stand","@YearOfPopulation"),
    ("Prozentualer Anteil der Todesfälle pro Bevölkerung", '@ProcentageOfDeathPop')
                          ]
hover_germany.mode = 'mouse'

# Anzeigen der Karte
st.bokeh_chart(bokeh_germany)

# Österreich
st.subheader('Österreich')

# Shapefile Österreich von arcgis.com laden.(https://data-synergis.opendata.arcgis.com/maps/a16c7b8ef72f4ec2b36f7c7ebbcdf2e5)
# Wir wählen die Bundesland Variante, für die Visualisierung.
austria = gpd.read_file("data//shapefiles//oesterreich//Bundeslaender_50.shp")

# TODO explain this csv where did we get the data here
# Statista csv
death_at = pd.read_csv("data//statistic_id1104271_todesfaelle-mit-dem-coronavirus--covid-19--in-oesterreich-nach-bundesland-2023.csv",
                 delimiter = ';')

# Erstellen der Spalte für die Todesfälle
austria['Deaths'] = ''
austria['Population'] = ''
austria['ProcentageOfDeathPop'] = ''
austria['YearOfPopulation'] = ''
# Setzen der Todesfälle auf den korrekten Kanton.
# Die Todesfälle müssen auf int gecastet werden, ansonsten wirft GeoJSONDataSource einen Fehler
for index, row in austria.iterrows():
    austria.loc[index, 'Deaths'] = \
    int(death_at[death_at['Bundesländer'] == row['BL']]['Anzahl Tode'].values[0])
    austria.loc[index, 'Population'] = \
    int(population[population['Bundesländer'] == row['BL']]['Population'].values[0])
    austria.loc[index, 'YearOfPopulation'] = \
    int(population[population['Bundesländer'] == row['BL']]['Stand'].values[0])
    austria.loc[index, 'ProcentageOfDeathPop'] = \
    "{:.2f}".format((death_at[death_at['Bundesländer'] == row['BL']]['Anzahl Tode'].values[0] / population[population['Bundesländer'] == row['BL']]['Population'].values[0]) * 100000)


 # TODO add comment
geo_source_austria = GeoJSONDataSource(geojson=austria.to_json())

bokeh_austria = figure(tools='wheel_zoom, hover')

# Entfernen der Raster und Achsen
bokeh_austria.axis.visible = False
bokeh_austria.xgrid.visible = False
bokeh_austria.ygrid.visible = False
bokeh_austria.outline_line_color = None
bokeh_austria.background_fill_color = None

# Grösse des Graphen auf die Breite skalieren
bokeh_austria.sizing_mode = 'scale_width'

# Erstellen der Karte und befüllen mit Farbe
bokeh_austria.patches('xs', 'ys', fill_alpha=1.0, line_width=0.0, source=geo_source_austria, fill_color="#008800")

# Hover Tool für die Todesfälle erstellen.
# Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
hover_austria = bokeh_austria.select(dict(type=HoverTool))
hover_austria.tooltips = [
    ("Bundesland", "@BL"), ("Todesfälle", "@Deaths"), \
    ("Bevölkerung", "@Population"), ("Stand","@YearOfPopulation"), \
    ("Prozentualer Anteil der Todesfälle pro Bevölkerung", '@ProcentageOfDeathPop')
]

hover_austria.mode = 'mouse'

# Anzeigen der Karte
st.bokeh_chart(bokeh_austria)

st.header('Impfungen')

st.subheader('Schweiz')

# Daten einlesen
vacc_ch = pd.read_csv('data//COVID19Cases_vaccpersons_AKL10_w.csv')

# Datum in DateTime-Format umwandeln
vacc_ch['date'] = pd.to_datetime(vacc_ch['date'])

# Liniendiagramm erstellen
fig, ax_vacc_swiss = plt.subplots()
ax_vacc_swiss.ticklabel_format(style='plain')
ax_vacc_swiss.plot(vacc_ch['date'], vacc_ch['entries'])
plt.xlabel('Impfdatum')
plt.ylabel('Anzahl der Impfungen')
plt.title('Gesamtzahl der Impfungen in der Schweiz')

# X-Achse anpassen, um quartalsweise Beschriftungen anzuzeigen
quarter_labels = vacc_ch['date'].dt.to_period('Q').astype(str)
plt.xticks(vacc_ch['date'], quarter_labels, rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.subheader('Deutschland')

df_vacc = pd.read_csv('data//Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv', 
                     delimiter=',')

# Sortieren Sie den DataFrame nach dem Impfdatum
df_vacc_sorted = df_vacc.sort_values('Impfdatum')

# Gruppieren Sie den DataFrame nach dem Impfdatum und summiere die Anzahl
df_vacc_grouped = df_vacc_sorted.groupby('Impfdatum')['Anzahl'].sum().reset_index()

# Berechne die kumulierten Impfungen pro Tag
df_vacc_grouped['kumulierte Impfungen'] = df_vacc_grouped['Anzahl'].cumsum()


# Liniendiagramm erstellen
# Meldedatum in DateTime-Format umwandeln
df_vacc_grouped['Impfdatum'] = pd.to_datetime(df_vacc_grouped['Impfdatum'])

# Gruppieren nach Meldedatum und Summieren der Anzahl der Fälle
daily_cases = df_vacc_grouped.groupby('Impfdatum')['kumulierte Impfungen'].sum().reset_index()


# Liniendiagramm erstellen
plt.plot(df_vacc_grouped['Impfdatum'], df_vacc_grouped['kumulierte Impfungen'])
plt.xlabel('Datum')
plt.ylabel('Anzahl der kumulierten Impfungen')
plt.title('COVID-19 Impfungen in Deutschland')
plt.ticklabel_format(style='plain', axis='y')

plt.tight_layout()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.subheader('Österreich')

# Daten einlesen
vacc_ak = pd.read_csv("data//CovidFaelle_Altersgruppe.csv", delimiter=';')

# Datumsformat konvertieren
vacc_ak['Time'] = pd.to_datetime(vacc_ak['Time'], format='%d.%m.%Y %H:%M:%S')

# Summe der Impfungen für jeden Zeitpunkt berechnen
total_vaccinations = vacc_ak.groupby('Time')['Anzahl'].sum()

# Liniendiagramm erstellen
fig, ax_vacc_austria = plt.subplots()
ax_vacc_austria.ticklabel_format(style='plain')
ax_vacc_austria.plot(total_vaccinations.index, total_vaccinations.values)
plt.xlabel('Impfdatum')
plt.ylabel('Gesamtimpfungen')
plt.title('Gesamtzahl der Impfungen in Österreich')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

# TODO add graphs with the used vac for each country to add statement about effectiveness of vacc.
#st.subheader('Wirksamkeit der Unterschiedlichen Impfungen')

# Problem
st.header('')
st.subheader('')

# Lösung
st.header('')
st.subheader('')

# Fazit
st.header('Fazit')
st.subheader(
    'Durch die Erkenntnisse können wir die Menschen beruhigen. Mit dem analytischen Rückblick auf die vergangenen '
    'Jahre können bei zukünftigen Pandemien verbesserte Massnahmen bestimmt werden.')

st.caption('Céline Felix, Katharina Azevedo, Kirishana Kiritharan, Patrick Häusermann')
