import os
import json

import matplotlib.style
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
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, ColumnDataSource, Legend
from bokeh.palettes import brewer
from IPython.display import display
from IPython.display import clear_output
from datetime import datetime
from bokeh.embed import components
from sklearn.linear_model import LinearRegression
matplotlib.style.use('classic')

# Bild als Header für den Benutzer als Einstieg in den Artikel
image = "pexels-photo-3943882.jpeg"
st.image(image)
st.caption('Bild von Pexels')

# Titel des Artikel mit Unterschrift
st.title(body='COVID-19: Ein Rückblick auf die Pandemie im deutschsprachigen Raum. '
         'Was können wir davon mitnehmen?')
st.subheader(
    'Es ist bereits ein Jahr her, seit die Massnahmen gegen COVID-19 in der Schweiz, Deutschland und Österreich '
    'aufgehoben wurden. Das Leben hat sich wieder normalisiert und der Virus verschwindet langsam aus unseren Köpfen. '
    'Doch was können wir aus der vergangenen Pandemie lernen?')

# Umstände
st.title('COVID-19 Fälle in der Schweiz, Deutschland und Österreich')

# Erläuterung zur Grafik
st.markdown("Die Schweiz implementierte im Vergleich zu Österreich und Deutschland als letzte "
        "erste Coronamassnahmen. Auch im Verlaufe der Pandemie waren die Massnahmen "
        "verglichen mit den Nachbarsländern stets weniger streng. In Betracht auf "
        "die Fallzahlen, war die Schweiz auf Platz zwei mit durchschnittlich 50'573 Fällen "
        "auf 100'000 Einwohner.")
st.markdown("Anfang des Jahres 2022 gab es in allen drei Ländern eine drastische Steigung der "
        "Fallzahlen. Dies vor allem deswegen, weil die Massnahmen gelockert wurden und " 
        "die Bevölkerung fahrlässiger handelte. Da zu diesem Zeitpunkt die Impfungen schon " 
        "recht fortgeschritten waren, nahm man die Situation etwas lockerer.")


# TODO Get Info how many tests were made at start and end of pandemic

# Schweiz

# Lesen des WHO Datensatz für den die drei Visualisierungen erstellt werden.
covid_ww = pd.read_csv(os.path.join('data', 'WHO-COVID-19-global-data.csv'))

# Datum in DateTime-Format konvertieren
covid_ww['Date_reported'] = pd.to_datetime(covid_ww['Date_reported'])

# Daten für die Schweiz filtern
switzerland = covid_ww[covid_ww['Country_code'] == 'CH']
swiss_population = 8703000 #Stand 2021

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
switzerland_quarterly = switzerland.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
switzerland_quarterly = switzerland.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

#Zahlen prozentual auf Bevölkerung reduzieren und auf 100'000 Einwohner rechnen
for index, row in switzerland_quarterly.iterrows():
    switzerland_quarterly.loc[index, 'Cumulative_cases'] = (row['Cumulative_cases'] / swiss_population) * 100000

# Daten für Deutschland filtern
germany_process_data = covid_ww[covid_ww['Country_code'] == 'DE']
germany_population = 83200000 #Stand 2021

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
germany_quarterly = germany_process_data.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

#Zahlen prozentual auf Bevölkerung reduzieren und auf 100'000 Einwohner rechnen
for index, row in germany_quarterly.iterrows():
    germany_quarterly.loc[index, 'Cumulative_cases'] = (row['Cumulative_cases'] / germany_population) * 100000
    

#Österreich

# Daten für Österreich filtern
austria_process_data = covid_ww[covid_ww['Country_code'] == 'AT']
austria_population = 8956000 #Stand 2021

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
austria_quarterly = austria_process_data.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Zahlen prozentual auf Bevölkerung reduzieren und auf 100'000 Einwohner rechnen
for index, row in austria_quarterly.iterrows():
    austria_quarterly.loc[index, 'Cumulative_cases'] = (row['Cumulative_cases'] / austria_population) * 100000

# Linien-Diagramm erstellen für alle

# Convert the index of quarterly DataFrames to a separate column 'date'
switzerland_quarterly['date'] = switzerland_quarterly.index
germany_quarterly['date'] = germany_quarterly.index
austria_quarterly['date'] = austria_quarterly.index

# Create ColumnDataSources
switzerland_source = ColumnDataSource(data=switzerland_quarterly)
germany_source = ColumnDataSource(data=germany_quarterly)
austria_source = ColumnDataSource(data=austria_quarterly)

# Create a figure object
p = figure(x_axis_type='datetime', title='COVID-19 Fälle in der Schweiz, Deutschland und Österreich',
           x_axis_label='Datum', y_axis_label="Anzahl der COVID-Fälle pro 100'000 Einwohner")

p.xaxis.axis_label_text_font_style = 'normal'
p.yaxis.axis_label_text_font_style = 'normal'

# Lines for Switzerland
switzerland_line = p.line(x='date', y='Cumulative_cases', source=switzerland_source, color='tomato', line_width=2.5,
                          legend_label='Schweiz')

# Lines for Germany
germany_line = p.line(x='date', y='Cumulative_cases', source=germany_source, color='maroon', line_width=2.5,
                      legend_label='Deutschland')

# Lines for Austria
austria_line = p.line(x='date', y='Cumulative_cases', source=austria_source, color='orange', line_width=2.5,
                      legend_label='Österreich')

# Legenden mit Klick verstecken
p.legend.click_policy = 'hide'

# Legenden zu den drei Linien anzeigen.
p.legend.location = "top_left"

# Hover-Tool
hover = HoverTool(tooltips=[('Datum', '@date{%F}'), ('Anzahl der Fälle', '@Cumulative_cases{0,0}')],
                  formatters={'@date': 'datetime'})
p.add_tools(hover)

# Konvertieren des Bokeh plot in HTML Komponenten
script, div = components(p)

# korrekte Darstellung auf Smartphone sicherstellen
p.toolbar.active_drag = None
st.bokeh_chart(p, use_container_width=True)

# Quellenangabe
st.caption('Datenquelle: World Health Organization (WHO), Stand: 26.04.2023')


st.header('Die tödliche Wirkung von COVID-19')
st.subheader('Ein Blick auf Quartal und Altersgruppe in der Schweiz, Deutschland und Österreich')

st.markdown('In den Heatmaps werden die Todesfälle nach Quartal und Altersgruppe in der Schweiz, '
        'Deutschland und Österreich dargestellt. Mittels Dropdown-Menü können Sie '
        'das gewünschte Land anwählen und es werden die Todesfälle pro Altersgruppe ab 2021 bis '
        'heute dargestellt. Dunklere Felder bedeuten eine höhere Anzahl von COVID-19-bedingten '
        'Todesfällen. '
        'In der Schweiz, starben hauptäschlich ältere Menschen an COVID-19. '
        'Dank der implementierten Massnahmen und den Impfungen konnten die Todeszahlen'
        ' reduziert werden. '
        'Deutschland weist einen ähnlichen Verlauf auf wie die Schweiz. In Österreich hingegen'
        ' steigen die Todesfälle im Laufe der Jahre. Aber auch hier sind hauptsächlich ältere'
        ' Menschen betroffen.'
        )

# Funktionen zur Erstellung der Heatmaps
def create_heatmap_switzerland():
    # Daten laden
    data_alt = pd.read_csv('data//COVID19Death_geoRegion_AKL10_w.csv')

    # 'Unbekannt' aus der Altersklasse entfernen
    data = data_alt[data_alt['altersklasse_covid19'] != 'Unbekannt']

    # Filtern der Daten von 2021 bis 2023
    data = data[data['datum'].astype(str).str[:4].astype(int).between(2021, 2023)]

    # Extrahieren des Jahres und der Woche aus dem Datum
    data['jahr'] = data['datum'].astype(str).str[:4]
    data['woche'] = data['datum'].astype(str).str[4:].astype(int)

    # Funktion zum Zuordnen des Quartals basierend auf der Woche
    def map_quartal(woche):
        if 1 <= woche <= 13:
            return 'Q1'
        elif 14 <= woche <= 26:
            return 'Q2'
        elif 27 <= woche <= 39:
            return 'Q3'
        else:
            return 'Q4'

    # Quartalsspalte erstellen
    data['quartal'] = data['woche'].map(map_quartal)

    # Pivot-Tabelle erstellen
    pivot_table = pd.pivot_table(data, values='entries', index='altersklasse_covid19', columns=['jahr', 'quartal'])

    # Farbpalette definieren
    cmap = sns.color_palette("Reds", as_cmap=True)

    # Heatmap erstellen
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap=cmap, annot=True, fmt='.0f', cbar=True, ax=ax)
    ax.set_xlabel('Quartal')
    ax.set_ylabel('Altersgruppe')
    ax.set_title('Anzahl der Todesfälle nach Quartal und Altersgruppe in der Schweiz')

    # Horizontale Ausrichtung der xticklabels
    plt.xticks(rotation=0)

    # Horizontale Ausrichtung der yticklabels
    plt.yticks(rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Bundesamt für Gesundheit (BAG), Stand: 01.01.2023')

def create_heatmap_austria():
    # Daten laden
    dat = pd.read_csv("data//CovidFaelle_Altersgruppe.csv", delimiter=';')

    # Änderung von Altersnotation
    dat['Altersgruppe'] = dat['Altersgruppe'].replace('<5', '0-5')
    dat['Altersgruppe'] = dat['Altersgruppe'].replace('>84', '84+')
    dat['Altersgruppe'] = dat['Altersgruppe'].replace('5-14', '05-14')
    dat = dat[dat['Bundesland'] != 'Österreich']

    # Datumsspalte in datetime umwandeln
    dat['Time'] = pd.to_datetime(dat['Time'], format='%d.%m.%Y %H:%M:%S')

    # Filtern der Daten von 2021 bis 2023
    dat = dat[dat['Time'].dt.year.between(2021, 2023)]

    # Quartalsinformationen hinzufügen
    dat['Quarter'] = dat['Time'].dt.to_period('Q')

    # Pivot-Tabelle erstellen
    pivot_table = pd.pivot_table(dat, values='AnzahlTot', index='Altersgruppe', columns='Quarter')

    # Quartalsüberschriften formatieren
    quarter_labels = pivot_table.columns.strftime('%Y Q%q')

    # Spalte 'AnzahlTot' in ganze Zahlen umwandeln
    dat['AnzahlTot'] = dat['AnzahlTot'].astype(int)

    # Farbpalette definieren
    cmap = sns.color_palette("Reds", as_cmap=True)

    # Heatmap erstellen
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap=cmap, annot=True, fmt='.0f', cbar=True, ax=ax)
    ax.set_xlabel('Quartal')
    ax.set_ylabel('Altersgruppe')
    ax.set_title('Anzahl der Todesfälle nach Quartal und Altersgruppe in Österreich')
    ax.set_xticks(np.arange(len(quarter_labels))+0.5)
    ax.set_xticklabels(quarter_labels, rotation=0, ha='center')

    # Umkehrung der y-Achse
    ax.set_yticks(np.arange(len(pivot_table.index))[::-1]+0.5)
    ax.set_yticklabels(pivot_table.index[::-1], rotation=0, va='center')

    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Epidemiologischen Meldesystem (EMS), Stand: 15.05.2023')

def create_heatmap_germany():
    # Daten laden
    df_alt = pd.read_csv('data//Aktuell Deutschland COVID Infektionen.csv', delimiter=';')

    df_alt['Altersgruppe'] = df_alt['Altersgruppe'].replace({'A00-A04': '00-04',
                                                            'A05-A14': '05-14',
                                                            'A15-A34': '15-34',
                                                            'A35-A59': '35-59',
                                                            'A60-A79': '60-79',
                                                            'A80+': '80+'})

    # 'Unbekannt' aus der Altersklasse rauslöschen
    df = df_alt[df_alt['Altersgruppe'] != 'unbekannt']

    # Datumsspalten in datetime umwandeln
    df['Meldedatum'] = pd.to_datetime(df['Meldedatum'], format='%Y-%m-%d')
    df['Refdatum'] = pd.to_datetime(df['Refdatum'], format='%Y-%m-%d')

    # Filtern der Daten von 2021 bis 2023
    df = df[df['Meldedatum'].dt.year.between(2021, 2023)]

    # Quartalsinformationen hinzufügen
    df['Quartal'] = df['Meldedatum'].dt.to_period('Q')

    # Pivot-Tabelle erstellen
    pivot_table = pd.pivot_table(df, values='AnzahlTodesfall', index='Altersgruppe', columns='Quartal', aggfunc='sum', fill_value=0)

    # Konvertieren in ganze Anzahlen
    pivot_table = pivot_table.astype(int)

    # Quartalsüberschriften formatieren
    quarter_labels = pivot_table.columns.strftime('%Y-Q%q')

    # Farbpalette definieren
    cmap = sns.color_palette("Reds", as_cmap=True)

    # Heatmap erstellen
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap=cmap, annot=True, fmt='d', cbar=True, ax=ax)
    ax.set_xlabel('Quartal')
    ax.set_ylabel('Altersgruppe')
    ax.set_title('Anzahl der Todesfälle nach Quartal und Altersgruppe in Deutschland')
    ax.set_xticks(np.arange(len(quarter_labels))+0.5)
    ax.set_xticklabels(quarter_labels, rotation=0, ha='center')
    ax.set_yticklabels(pivot_table.index[::-1], rotation=0, ha='center')

    # Horizontale Ausrichtung der Y-Achse
    ax.set_yticklabels(pivot_table.index[::-1], rotation=0, ha='right')

    # Anpassung der Farbskala basierend auf den Werten
    norm = plt.Normalize(pivot_table.min().min(), pivot_table.max().max())
    heatmap = sns.heatmap(pivot_table, cmap=cmap, annot=True, fmt='d', cbar=False, norm=norm, ax=ax)

    # Horizontale Ausrichtung der xticklabels
    plt.xticks(rotation=0)

    # Horizontale Ausrichtung der yticklabels
    plt.yticks(rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Robert Koch-Institut (RKI), Stand: 01.01.2023')


# Dropdown-Widget für Länderauswahl erstellen
country_dropdown_heatmap = st.selectbox(
    'Wählen Sie ein Land aus:',
    ['Schweiz', 'Österreich', 'Deutschland'],
    key = 'heatmap'
)

# Funktion zur Handhabung der Dropdown-Änderungen erstellen
def on_country_dropdown_change(country):
    if country == 'Schweiz':
        create_heatmap_switzerland()
    elif country == 'Österreich':
        create_heatmap_austria()
    elif country == 'Deutschland':
        create_heatmap_germany()

# Dropdown-Widget anzeigen und Änderungen überwachen
on_country_dropdown_change(country_dropdown_heatmap)



st.header('Geografische Verteilung')
st.subheader('In den folgenden Grafiken sind die Todeszahlen pro Kanton, resp. Bundesland ersichtlich. \
Können Sie einen Unterschied zwischen den Kantonen bzw. Bundesländern sehen? \
Gibt es einen Unterschied zwischen dem Land und der Stadt?')

st.markdown('In den Karten sind die Todesfälle, die Bevölkerungsanzahl, und die Sterberate der einzelnen Kanton bzw. Bundesländer in den Tooltips ersichtlich. '
            'Wenn Sie mit der Maus über die Karte fahren, werden die Tooltips automatisch angezeigt.'
            ''
            )


population = pd.read_csv("data//population.csv", delimiter=';')

# Schweiz
def create_map_switzerland():

    # Infos zu den Bevölkerunganzahl von Statista (https://de.statista.com/statistik/daten/studie/75536/umfrage/schweiz-bevoelkerung-nach-kanton-zeitreihe/)
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
        population[population['Bundesländer'] == row['NAME']]['Population'].values[0]) * 1000)

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
    bokeh_swiss.patches('xs', 'ys', fill_alpha=0.8, line_width=0.6, line_color='white', source=geo_source_switzerland, fill_color="tomato")

    # Hover Tool für die Todesfälle erstellen.
    # Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
    hover_switzerland = bokeh_swiss.select(dict(type=HoverTool))
    hover_switzerland.tooltips = [
        ("Kanton", "@NAME"), ("Todesfälle", "@deaths"),
        ("Bevölkerung", "@Population"), ("Stand (Bevölkerung)","@YearOfPopulation"),
        ("Sterberate", '@ProcentageOfDeathPop')
                                  ]
    hover_switzerland.mode = 'mouse'

    # Anzeigen der Karte
    st.bokeh_chart(bokeh_swiss)

    # Quellenangabe
    st.caption('Todesfälle Datenquelle: Bundesamt für Gesundheit (BAG), Stand: 01.01.2023')
    st.caption('Bevölkerung Datenquelle: Statista, Stand: 31.12.2021')

# Deutschland
#st.subheader('Deutschland')

def create_map_germany():

    death_de = pd.read_csv("data//statistic_id1100750_fallzahl-des-coronavirus--covid-19--nach-bundeslaendern-2023.csv",
                     delimiter = ';')

    # Shapefile Deutschland von bund.de laden. (https://gdz.bkg.bund.de/index.php/default/digitale-geodaten/verwaltungsgebiete.html)
    # Wir wählen die Karte, in dem die Bundesländer eingezeichnet sind, für die Visualisierung.
    germany = gpd.read_file("data//shapefiles//deutschland//vg2500_bld.shp")

    # Erstellen der Spalte für die Todesfälle
    germany['Deaths'] = ''
    germany['Population'] = ''
    germany['ProcentageOfDeathPop'] = ''
    germany['YearOfPopulation'] = ''

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
        population[population['Bundesländer'] == row['GEN']]['Population'].values[0]) * 1000)

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
    bokeh_germany.patches('xs', 'ys', fill_alpha=0.8, line_width=0.6, line_color='white', source=geo_source_germany, fill_color="maroon")

    # Hover Tool für die Todesfälle erstellen.
    # Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
    hover_germany = bokeh_germany.select(dict(type=HoverTool))
    hover_germany.tooltips = [
        ("Bundesland", "@GEN"), ("Todesfälle", "@Deaths"),
        ("Bevölkerung", "@Population"), ("Stand (Bevölkerung)","@YearOfPopulation"),
        ("Sterberate", '@ProcentageOfDeathPop')
                              ]
    hover_germany.mode = 'mouse'

    # Anzeigen der Karte
    st.bokeh_chart(bokeh_germany)

    # Quellenangabe
    st.caption('Todesfälle Datenquelle: Statista, Robert Koch-Institut (RKI), Stand: 25.01.2023')
    st.caption('Bevölkerung Datenquelle: Destatis, Stand: 31.12.2021')

# Österreich

def create_map_austria():

    # Shapefile Österreich von arcgis.com laden.(https://data-synergis.opendata.arcgis.com/maps/a16c7b8ef72f4ec2b36f7c7ebbcdf2e5)
    # Wir wählen die Bundesland Variante, für die Visualisierung.
    austria = gpd.read_file("data//shapefiles//oesterreich//Bundeslaender_50.shp")

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
        "{:.2f}".format((death_at[death_at['Bundesländer'] == row['BL']]['Anzahl Tode'].values[0] / population[population['Bundesländer'] == row['BL']]['Population'].values[0]) * 1000)

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
    bokeh_austria.patches('xs', 'ys', fill_alpha=0.8, line_width=0.6, line_color='white', source=geo_source_austria, fill_color="orange")

    # Hover Tool für die Todesfälle erstellen.
    # Falls nun über das Gebiet mit der Maus gefahren wird, wird der Name des Gebiets und die Todesfälle angezeigt.
    hover_austria = bokeh_austria.select(dict(type=HoverTool))
    hover_austria.tooltips = [
        ("Bundesland", "@BL"), ("Todesfälle", "@Deaths"), \
        ("Bevölkerung", "@Population"), ("Stand (Bevölkerung)","@YearOfPopulation"), \
        ("Sterberate", '@ProcentageOfDeathPop')
    ]

    hover_austria.mode = 'mouse'

    # Anzeigen der Karte
    st.bokeh_chart(bokeh_austria)

    # Quellenangabe
    st.caption('Todesfälle Datenquelle: Statista, Bundesministerium für Soziales, Gesundheit, Pflege und Konsumentenschutz, Stand: 31.05.2023')
    st.caption('Bevölkerung Datenquelle: Google, Stand: 2022/2023')

# Dropdown-Widget für Länderauswahl erstellen
country_dropdown_map = st.selectbox(
    'Wählen Sie ein Land aus: ',
    ['Schweiz', 'Österreich', 'Deutschland'],
    key = 'map'
)

def on_country_dropdown_map_change(country):
    if country == 'Schweiz':
        create_map_switzerland()
    elif country == 'Österreich':
        create_map_austria()
    elif country == 'Deutschland':
        create_map_germany()

on_country_dropdown_map_change(country_dropdown_map)

st.header('Impfungen')

st.markdown('In allen drei Ländern stieg die Anzahl der Impfungen stark an. Die folgende Grafik bezieht sich ausschliesselich auf die ersten Impfungen (ohne Booster etc.).')


#Schweiz
vacc_type = pd.read_csv('data//COVID19VaccPersons_vaccine.csv')
vacc_type['date'] = pd.to_datetime(vacc_type['date'])
vacc_type = vacc_type.sort_values('date')
vacc_type = vacc_type[vacc_type['type'] == 'COVID19FullyVaccPersons']
vacc_type['Kumulative Summe'] = vacc_type['entries'].cumsum()
vacc_type['Kumulative Summe'] = (vacc_type['Kumulative Summe'] / swiss_population) * 100000


#Deutschland
de_vacc = pd.read_csv('data//Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv', delimiter=',')
# Daten nur von Impfserie 1 nehmen
de_vacc = de_vacc[de_vacc['Impfserie'] == 1]
# Sortieren Sie den DataFrame nach dem Impfdatum
de_vacc_sorted = de_vacc.sort_values('Impfdatum')
# Gruppieren Sie den DataFrame nach dem Impfdatum und summiere die Anzahl
de_vacc_grouped = de_vacc_sorted.groupby('Impfdatum')['Anzahl'].sum().reset_index()
# Berechne die kumulierten Impfungen pro Tag
de_vacc_grouped['kumulierte Impfungen'] = de_vacc_grouped['Anzahl'].cumsum()
# Meldedatum in DateTime-Format umwandeln
de_vacc_grouped['Impfdatum'] = pd.to_datetime(de_vacc_grouped['Impfdatum'])

# Gruppieren nach Meldedatum und Summieren der Anzahl der Fälle
daily_cases = de_vacc_grouped.groupby('Impfdatum')['kumulierte Impfungen'].sum().reset_index()
daily_cases = de_vacc_grouped.groupby('Impfdatum')['kumulierte Impfungen'].sum().reset_index()
daily_cases['Impfungen pro 100k'] = (daily_cases['kumulierte Impfungen'] / germany_population) * 100000

# Österreich
vacc_ak = pd.read_csv("data//CovidFaelle_Altersgruppe.csv", delimiter=';')
vacc_ak['Time'] = pd.to_datetime(vacc_ak['Time'], format='%d.%m.%Y %H:%M:%S')
vacc_ak = vacc_ak[vacc_ak['Time'] >= '2021-01-01']  # Datumsfilter hinzufügen
total_vaccinations = vacc_ak.groupby('Time')['Anzahl'].sum()
total_vaccinations_per_100k = (total_vaccinations / austria_population) * 100000

# Daten für die Grafik erstellen
source_swiss = ColumnDataSource(data=dict(date=vacc_type['date'], cum_sum=vacc_type['Kumulative Summe']))
source_germany = ColumnDataSource(data=dict(date=daily_cases['Impfdatum'], impfungen_pro_100k=daily_cases['Impfungen pro 100k']))
source_austria = ColumnDataSource(data=dict(date=total_vaccinations.index, impfungen=total_vaccinations_per_100k.values))

# Werkzeug für Tooltips erstellen
tooltips = [
    ('Datum', '@date{%F}'),
    ("Impfungen pro 100'000 Einwohner (Schweiz)", '@cum_sum{0.00}'),
    ("Impfungen pro 100'000 Einwohner (Deutschland)", '@impfungen_pro_100k{0.00}'),
    ("Impfungen pro 100'000 Einwohner (Österreich)", '@impfungen{0.00}')
]
formatters = {'@date': 'datetime'}
hover_tool = HoverTool(tooltips=tooltips, formatters=formatters)

# Figure-Objekt erstellen
p = figure(x_axis_type='datetime', y_axis_type='auto', plot_width=600, plot_height=600, title="COVID-19 Impfungen pro 100'000 Einwohner")
p.xaxis.axis_label_text_font_style = 'normal'
p.yaxis.axis_label_text_font_style = 'normal'

# Entfernen der Scientific (e+...) Formatierung auf der Y-Achse
p.left[0].formatter.use_scientific = False

# Linien für die einzelnen Länder zeichnen
switzerland_line = p.line(x='date', y='cum_sum', source=source_swiss, line_color='tomato', line_width=2, legend_label='Schweiz')
germany_line = p.line(x='date', y='impfungen_pro_100k', source=source_germany, line_color='maroon', line_width=2, legend_label='Deutschland')
austria_line = p.line(x='date', y='impfungen', source=source_austria, line_color='orange', line_width=2, legend_label='Österreich')

# Achsenbeschriftungen festlegen
p.xaxis.axis_label = 'Datum'
p.yaxis.axis_label = "Anzahl der Impfungen pro 100'000 Einwohner"

# korrekte Darstellung auf Smartphone sicherstellen
p.toolbar.active_drag = None
st.bokeh_chart(p, use_container_width=True)

st.caption('Schweiz Datenquelle: Bundesamt für Gesundheit (BAG), Stand: 24.04.2023')
st.caption('Deutschland Datenquelle: Robert Koch-Institut (RKI), Stand: 07.04.2023')
st.caption('Österreich Datenquelle: Epidemiologischen Meldesystem (EMS), Stand: 15.05.2023')

st.header('Impfstoffe im Vergleich')

st.markdown('Obwohl alle drei Länder täglich Impfungen durchführte, setzte jedes Land auf andere Impfstoffe. ' 
            'Ein Grund, weshalb bestimmte Impfstoffe mehr geimpft wurden, war das Zulassungsdatum. '
            'So war Novavax beispielsweise in der EU ab dem 4. August 2021 und in der Schweiz erst ab dem 13. April 2022 zugelassen. '
            "Am meisten wurde der Pfizer Biontech Impfstoff, mit 137'755'538 Impfdosen über alle drei Länder geimpft. "
            "Pfizer Biontech war der erste Impfstoff, der in der EU und der Schweiz zugelassen wurde."
            )
st.markdown('Bitte beachten Sie, dass die Anzahl der Impfdosen an der gesamten Bevölkerungszahl gemessen wird und die Zahlen der drei Grafiken '
            'somit nicht direkt miteinander vergleichbar sind.')

# Schweiz
vaccine_swiss = pd.read_csv('data//COVID19VaccPersons_AKL10_vaccine_w.csv')

# Entferne unknown und all Einträge
vaccine_swiss.drop(vaccine_swiss[vaccine_swiss['vaccine'] == 'unknown'].index, inplace = True)
vaccine_swiss.drop(vaccine_swiss[vaccine_swiss['vaccine'] == 'all'].index, inplace = True)

# Gruppiere nach den Impfstofftypen
vaccine_swiss_grouped = vaccine_swiss.groupby('vaccine')['entries'].sum().reset_index()

# Sortieren nach der Anzahl
vaccine_swiss_grouped = vaccine_swiss_grouped.sort_values(by='entries', ascending=False)

def create_vaccinetype_bar_switzerland():
    # Bardiagramm erstellen
    fig, ax_vacc_type_swiss = plt.subplots(figsize=(10, 8))
    ax_vacc_type_swiss.ticklabel_format(style='plain')
    bar_swiss = ax_vacc_type_swiss.bar(vaccine_swiss_grouped['vaccine'], vaccine_swiss_grouped['entries'], width=0.6, color='tomato', edgecolor='None')

    # Werte überhalb des Graph setzen
    ax_vacc_type_swiss.bar_label(bar_swiss, labels=[e for e in vaccine_swiss_grouped['entries']], padding=3, color='Black', fontsize=8)

    # Neue Labels setzen
    labels = ['Johnson Johnson', 'Moderna', 'Moderna Bivalent', 'Novavax', 'Pfizer Biontech', 'Pfizer Biontech Bivalent']
    ax_vacc_type_swiss.set_xticks(vaccine_swiss_grouped['vaccine'], labels, rotation=90)

    # Achsen oben und rechts entfernen
    ax_vacc_type_swiss.spines[['right', 'top']].set_visible(False)

    # Ticks oben und rechts entfernen
    plt.tick_params(right = False, top = False)

    # Labels und Titel setzen
    plt.xlabel('Impfstoff')
    plt.ylabel('Anzahl Impfungen')
    plt.title('Anzahl der Impfungen pro Impfstoff in der Schweiz')
    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Bundesamt für Gesundheit (BAG), Stand: 2023')

# Deutschland

# Stand: 27. Mai 2022 statista (https://de.statista.com/statistik/daten/studie/1197550/umfrage/impfungen-gegen-das-coronavirus-nach-hersteller/)
vaccine_germany = pd.read_csv('data//statistic_id1197550_impfungen-gegen-das-coronavirus-nach-hersteller-2022.csv', delimiter=';')

def create_vaccinetype_bar_germany():

    # Bardiagramm erstellen
    fig, ax_vacc_type_germany = plt.subplots(figsize=(10, 8))
    ax_vacc_type_germany.ticklabel_format(style='plain')
    bar_austria = ax_vacc_type_germany.bar(vaccine_germany['vaccine'], vaccine_germany['entries'], width=0.6, color='maroon', edgecolor='None')

    # Achsen oben und rechts entfernen
    ax_vacc_type_germany.spines[['right', 'top']].set_visible(False)

    # Werte überhalb des Graph setzen
    ax_vacc_type_germany.bar_label(bar_austria, labels=[e for e in vaccine_germany['entries']], padding=3, color='Black', fontsize=8)

    # Neue Labels setzen
    labels = ['Pfizer Biontech', 'Moderna', 'Astra Zeneca', 'Johnson Johnson', 'Novavax']
    ax_vacc_type_germany.set_xticks(vaccine_germany['vaccine'], labels, rotation=90)

    # Ticks oben und rechts entfernen
    plt.tick_params(right = False, top = False)
    plt.tick_params(axis='x', rotation=90)

    plt.xlabel('Impfstoff')
    plt.ylabel('Anzahl Impfungen')
    plt.title('Anzahl der Impfungen pro Impfstoff in Deutschland')
    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Statista, Robert Koch-Institut (RKI), Stand: 27.05.2022')

# Österreich
#st.subheader('Österreich')
vaccine_austria = pd.read_csv('data//COVID19_vaccination_agegroups_v202210.csv', delimiter=';')

# Gruppiere nach den Impfstofftypen
vaccine_austria_grouped = vaccine_austria.groupby('vaccine').sum().reset_index()

# Sortieren nach der Anzahl
vaccine_austria_grouped = vaccine_austria_grouped.sort_values(by='vaccinations_administered_cumulative', ascending=False)
def create_vaccinetype_bar_austria():

    # Bardiagramm erstellen
    fig, ax_vacc_type_austria = plt.subplots(figsize=(10, 8))
    ax_vacc_type_austria.ticklabel_format(style='plain')
    bar_austria = ax_vacc_type_austria.bar(vaccine_austria_grouped['vaccine'], vaccine_austria_grouped['vaccinations_administered_cumulative'], width=0.6, color='orange', edgecolor='None')

    # Achsen oben und rechts entfernen
    ax_vacc_type_austria.spines[['right', 'top']].set_visible(False)

    # Werte überhalb des Graph setzen
    ax_vacc_type_austria.bar_label(bar_austria, labels=[e for e in vaccine_austria_grouped['vaccinations_administered_cumulative']], padding=3, color='Black', fontsize=8)

    # Neue Labels setzen
    labels = ['Astra Zeneca', 'Pfizer Biontech', 'Johnson Johnson', 'Moderna', 'Novavax', 'Sanofi Pasteur', 'Valneva']
    ax_vacc_type_austria.set_xticks(vaccine_austria_grouped['vaccine'], labels, rotation=90)

    # Ticks oben und rechts entfernen
    plt.tick_params(right = False, top = False)

    plt.xlabel('Impfstoff')
    plt.ylabel('Anzahl Impfungen')
    plt.title('Anzahl der Impfungen pro Impfstoff in Österreich')
    plt.tight_layout()
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: Österreichisches COVID-19 Open Data Informationsportal, Stand: 17.05.2023')

country_dropdown_vacctypebar = st.selectbox(
    'Wählen Sie ein Land aus: ',
    ['Schweiz', 'Österreich', 'Deutschland'],
    key = 'bar'
)

def on_country_dropdown_vacctypebar_change(country):
    if country == 'Schweiz':
        create_vaccinetype_bar_switzerland()
    elif country == 'Österreich':
        create_vaccinetype_bar_austria()
    elif country == 'Deutschland':
        create_vaccinetype_bar_germany()

on_country_dropdown_vacctypebar_change(country_dropdown_vacctypebar)

#Ausblick
st.header('Ausblick der Fallzahlen')
st.markdown("Die folgenden Grafiken zeigen den Ausblick der Fallzahlen im Jahr 2024."
            "Die Trendanalysen wurden anhand der bisher gesammelten Daten erstellt und sind somit nur eine Annahme der Fallzahlen. "
            "Die tatsächlichen Fallzahlen können sich anders entwickeln.")
st.write("Die Vorhersage wurde auf Basis der Bevölkerungsanzahl des jeweiligen Landes gemessen. Ein direkter Vergleich ist somit nicht möglich.")

#Schweiz

switzerland['Date_reported'] = switzerland['Date_reported'].astype(str)
switzerland['year'] = switzerland['Date_reported'].str[0:4]
year_ch = switzerland.groupby('year')['New_cases'].sum()

# Daten von years_ch
years_ch = np.array([2020, 2021, 2022, 2023]).reshape(-1, 1) # von year_ch
cases_ch = np.array([451142, 883690, 3045631, 20909])

# Lineare Regression
regressor = LinearRegression()
regressor.fit(years_ch, cases_ch)

#Deutschland

# Daten DE
years_de = np.array([2020, 2021, 2022, 2023]).reshape(-1, 1)
cases_de = np.array([1734444, 5430604, 30220321, 1011090])


#Österreich

austria_process_data['Date_reported'] = austria_process_data['Date_reported'].astype(str)
austria_process_data['year'] = austria_process_data['Date_reported'].str[0:4]
year_at = austria_process_data.groupby('year')['New_cases'].sum()


# Funktion zur Durchführung der linearen Regression und Prognose
def perform_linear_regression(years, cases, future_year):
    regressor = LinearRegression()
    regressor.fit(years, cases)
    
    slope = regressor.coef_[0]
    intercept = regressor.intercept_
    trend = f"y = {slope:.2f}x + {intercept:.2f}"
    
    future_cases = regressor.predict([[future_year]])
    
    return trend, future_cases

# Schweiz

switzerland = pd.DataFrame({
    'Date_reported': ['2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01'],
    'New_cases': [451142, 883690, 3045631, 20909]
})

years_ch = np.array([2020, 2021, 2022, 2023]).reshape(-1, 1)
cases_ch = np.array([451142, 883690, 3045631, 20909])

# Deutschland

years_de = np.array([2020, 2021, 2022, 2023]).reshape(-1, 1)
cases_de = np.array([1734444, 5430604, 30220321, 1011090])

# Österreich

austria_process_data = pd.DataFrame({
    'Date_reported': ['2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01'],
    'New_cases': [352657, 911871, 4436351, 359753]
})

years_at = np.array([2020, 2021, 2022, 2023]).reshape(-1, 1)
cases_at = np.array([352657, 911871, 4436351, 359753])

# Dropdown-Menü
selected_country = st.selectbox('Wählen Sie ein Land aus:', ['Schweiz', 'Deutschland', 'Österreich'])

# Ausblick basierend auf dem ausgewählten Land
if selected_country == 'Schweiz':
    # Lineare Regression
    regressor = LinearRegression()
    regressor.fit(years_ch, cases_ch)

    # Trendanalyse
    slope = regressor.coef_[0]
    intercept = regressor.intercept_
    trend = f"y = {slope:.2f}x + {intercept:.2f}"

    # Prognose erstellen
    future_year = np.array([2024]).reshape(-1, 1)
    future_cases = regressor.predict(future_year)

    # Visualisierung erstellen
    fig, ax = plt.subplots()
    ax.scatter(years_ch, cases_ch, color='orange', s=50, label='Bisherige Zahlen')
    ax.plot(years_ch, regressor.predict(years_ch), color='tomato', linewidth=2.5, label='Lineare Regression')
    ax.scatter(2024, future_cases, color='maroon', s=100, label='Prognose für 2024')
    ax.set_xlabel('Jahr')
    ax.set_ylabel('Fallzahlen')
    ax.set_title('COVID-19 Fallzahlen in der Schweiz')
    # Legende
    ax.legend(scatterpoints=1)
    ax.ticklabel_format(style='plain')

    ax.set_xticks(years_ch.flatten())
    ax.set_xticklabels([str(int(year)) for year in years_ch.flatten()])
    ax.set_ylim(bottom=0)
    ax.grid(True)
    p.grid.grid_line_color = 'gray'
    p.grid.grid_line_alpha = 0.5
    p.legend.border_line_color = 'black'  # Farbe der Umrandung
    p.legend.border_line_width = 1  # Dicke der Umrandung
    p.legend.border_line_alpha = 0.8  # Transparenz der Umrandung

    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: World Health Organization (WHO), Stand: 26.04.2023')

elif selected_country == 'Deutschland':

    # Lineare Regression
    regressor = LinearRegression()
    regressor.fit(years_de, cases_de)

    # Trendanalyse
    slope = regressor.coef_[0]
    intercept = regressor.intercept_
    trend = f"y = {slope:.2f}x + {intercept:.2f}"

    # Prognose erstellen
    future_year = np.array([2024]).reshape(-1, 1)
    future_cases = regressor.predict(future_year)

    # Visualisierung erstellen
    fig, ax = plt.subplots()
    ax.scatter(years_de, cases_de, color='orange', s=50, label='Bisherige Zahlen')
    ax.plot(years_de, regressor.predict(years_de), color='tomato', linewidth=2.5, label='Lineare Regression')
    ax.scatter(2024, future_cases, color='maroon', s=100, label='Prognose für 2024')
    ax.set_xlabel('Jahr')
    ax.set_ylabel('Fallzahlen')
    ax.set_title('COVID-19 Fallzahlen in Deutschland')
    ax.legend(scatterpoints=1)
    ax.ticklabel_format(style='plain')
    ax.set_xticks(years_de.flatten())
    ax.set_xticklabels([str(int(year)) for year in years_de.flatten()])
    ax.set_ylim(bottom=0)
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: World Health Organization (WHO), Stand: 26.04.2023')

elif selected_country == 'Österreich':
    # Lineare Regression
    regressor = LinearRegression()
    regressor.fit(years_at, cases_at)

    # Trendanalyse
    slope = regressor.coef_[0]
    intercept = regressor.intercept_
    trend = f"y = {slope:.2f}x + {intercept:.2f}"

    # Prognose erstellen
    future_year = np.array([2024]).reshape(-1, 1)
    future_cases = regressor.predict(future_year)

    fig, ax = plt.subplots()
    ax.scatter(years_at, cases_at, color='orange', s=50, label='Bisherige Zahlen')
    ax.plot(years_at, regressor.predict(years_at), color='tomato', linewidth=2.5, label='Lineare Regression')
    ax.scatter(2024, future_cases, color='maroon', s=100, label='Prognose für 2024')
    ax.set_xlabel('Jahr')
    ax.set_ylabel('Fallzahlen')
    ax.set_title('COVID-19 Fallzahlen in Österreich')
    ax.legend(scatterpoints=1)
    ax.ticklabel_format(style='plain')
    ax.set_xticks(years_at.flatten())
    ax.set_xticklabels([str(int(year)) for year in years_at.flatten()])
    ax.set_ylim(bottom=0)
    st.pyplot(fig)

    # Quellenangabe
    st.caption('Datenquelle: World Health Organization (WHO), Stand: 26.04.2023')

st.write("Trendanalyse:", trend)

# Fazit
st.header('Fazit')
st.markdown(
    'Durch die gewonnenen Erkenntnisse kann die Bevölkerung beruhigt werden. Auch wenn die Fallzahlen im nächsten Jahr nochmals steigen sollten, '
    'ist jedes Land mit Impfdosen und den passenden Massnahmen vorbereitet. '
    'Mit dem analytischen Rückblick auf die vergangenen Jahre können bei zukünftigen Pandemien die besten Massnahmen ergriffen werden, welche '
    'die Gesundheit der Bevölkerung sicherstellt und die wirtschaftlichen Leistungen beibehält.')

#TODO - Vorschläge für effizientere Massnahmen

st.caption('Autoren: Céline Felix, Katharina Azevedo, Kirishana Kiritharan, Patrick Häusermann')
st.caption('Veröffentlichung Artikel: Juni 2023')
st.caption('Daten bis April 2023')

st.caption("Für weitere länderspezifische Informationen besuchen Sie: \
            Schweiz: Bundesamt für Gesundheit (BAG) \
            Deutschland:  Robert Koch-Institut (RKI) \
            Österreich:  Bundesministerium für Soziales, Gesundheit, Pflege und Konsumentenschutz (BMSGPK)")
