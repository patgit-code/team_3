import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import numpy as np
from pandas.api.types import CategoricalDtype
import geopandas as gpd
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer

image = "pexels-photo-3943882.jpeg"
st.image(image)
st.caption('Bild von Pexels')
st.title(body='Ein Rückblick auf die Covid Pandemie im Deutschsprachigen Raum')
st.subheader(
    'Es ist bereits ein Jahr her, als die Massnahmen gegen den Corona Virus in Deutschland, Österreich und Schweiz '
    'aufgehoben wurden. Das Leben hat sich wieder normalisiert und der Virus verschwindet langsam aus den Köpfen der '
    'Menschen. Doch was können wir aus den vergangenen Pandemie Jahren lernen?')

# Umstände
st.header('Verlauf des Virus')
st.subheader('')

# TODO Start all Visualisations at the same date

# Schweiz
st.subheader('Schweiz')
st.text('Der Verlauf in der Schweiz...')


covid_ww = pd.read_csv(os.path.join('data', 'WHO-COVID-19-global-data.csv'))

# Daten für die Schweiz filtern
switzerland = covid_ww[covid_ww['Country_code'] == 'CH']

# Datum in DateTime-Format konvertieren
switzerland['Date_reported'] = pd.to_datetime(switzerland['Date_reported'])

# Daten nach Quartal gruppieren und kumulative Fälle berechnen
switzerland_quarterly = switzerland.groupby(pd.Grouper(key='Date_reported', freq='Q')).agg({'Cumulative_cases': 'max'})

# Liniendiagramm erstellen
fig, ax_virus_process_switzerland = plt.subplots()
ax_virus_process_switzerland.ticklabel_format(style='plain')
ax_virus_process_switzerland.plot(switzerland_quarterly.index, switzerland_quarterly['Cumulative_cases'])

# Start der Corona Massnahmen
start_date_switzerland = pd.to_datetime('2020-03-16')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_switzerland, 0, max(switzerland_quarterly['Cumulative_cases']),
            label='Start der Corona Massnahmen am 16.03.2020', color='red')
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
df = pd.read_csv('data//Aktuell Deutschland COVID Infektionen.csv', delimiter=';')

# Meldedatum in DateTime-Format umwandeln
df['Meldedatum'] = pd.to_datetime(df['Meldedatum'])

# Gruppieren nach Meldedatum und Summieren der Anzahl der Fälle
daily_cases = df.groupby('Meldedatum')['AnzahlFall'].sum().reset_index()

# Liniendiagramm erstellen
fig, ax_virus_process_germany = plt.subplots()
ax_virus_process_germany.ticklabel_format(style='plain')
ax_virus_process_germany.plot(daily_cases['Meldedatum'], daily_cases['AnzahlFall'])
plt.xlabel('Datum')
plt.ylabel('Anzahl der Fälle')
plt.title('COVID-19 Fälle in Deutschland')

# Start der Corona Massnahmen
start_date_germany = pd.to_datetime('2020-02-27')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_germany, 0, max(daily_cases['AnzahlFall']), label='Start der Corona Massnahmen am 27.02.2020',
            color='red')
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
st.pyplot(fig)

# Österreich
st.subheader('Österreich')
# TODO change font
st.text('Im Vergleich mit Deutschland und der Schweiz hat Österreich...')
# CSV-Daten laden
dat = pd.read_csv(r"data\CovidFaelle_Altersgruppe.csv", delimiter=';')

# Konvertiere 'Time' in ein Datumsformat
dat['Time'] = pd.to_datetime(dat['Time'], format='%d.%m.%Y %H:%M:%S')

# Summe der Covid-Fälle für alle Daten berechnen
total_cases = dat.groupby('Time')['Anzahl'].sum()

# Linien-Diagramm erstellen
fig, ax_virus_process_austria = plt.subplots()
ax_virus_process_austria.ticklabel_format(style='plain')
ax_virus_process_austria.plot(total_cases.index, total_cases.values)

# Start der Corona Massnahmen
start_date_austria = pd.to_datetime('2020-03-11')
# Vertikale Line des Start Datums anzeigen
plt.axvline(start_date_austria, 0, max(total_cases.values), label='Start der Corona Massnahmen am 11.03.2020',
            color='red')
plt.legend()

plt.xlabel('Datum')
plt.ylabel('Anzahl der Covid-Fälle')
plt.title('Covid-Fälle im Laufe der Zeit')
plt.xticks(rotation=45)
plt.grid(True)

# Diagramm anzeigen
st.pyplot(fig)

st.header('Todesfälle (Heatmaps)')
st.subheader('')

# Schweiz
st.subheader('Schweiz')
# Daten laden
data = pd.read_csv(r'data\COVID19Death_geoRegion_AKL10_w.csv')

# Filtern der Daten von 2021 bis 2023
data = data[data['datum'].astype(str).str[:4].astype(int).between(2021, 2023)]

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
df = pd.read_csv(r'data\Aktuell Deutschland COVID Infektionen.csv', delimiter=';')

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

# Daten laden
# dat = pd.read_csv("CovidFaelle_Altersgruppe.csv", delimiter=';')

# Datumsspalte in datetime umwandeln
# dat['Time'] = pd.to_datetime(dat['Time'], format='%d.%m.%Y %H:%M:%S')

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
st.subheader('')

# Schweiz
st.subheader('Schweiz')

# Getting the coords for applying the information per canton
cantons = gpd.read_file(r'data\shapefiles\swissboundaries\swissBOUNDARIES3D_1_4_TLM_KANTONSGEBIET.shp')
cantons['coords'] = cantons['geometry'].apply(lambda x: x.representative_point().coords[:])

cantons['coords'] = [coords[0] for coords in cantons['coords']]

# cleaning data
death = pd.read_csv(r'data\COVID19Death_geoRegion.csv')
death.drop(death[death['geoRegion'] == 'CH'].index, inplace=True)
death.drop(death[death['geoRegion'] == 'CHFL'].index, inplace=True)
death.drop(death[death['entries'] == 'NA'].index, inplace=True)
death_count_canton = death.groupby('geoRegion')['entries'].sum().reset_index()

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

cantons['deaths'] = ''

for index, row in cantons.iterrows():
    cantons.loc[index, 'deaths'] = \
    death_count_canton[death_count_canton['geoRegion'] == dict_canton[row['NAME']]]['entries'].values[0]

fig, ax_map_switzerland = plt.subplots(figsize=(20, 20), dpi=96)
ax_map_switzerland.set_axis_off()

# color graph
colours = ["#ff9900", "#ff3300"]
cmap = colors.LinearSegmentedColormap.from_list("colour_map", colours, N=256)
norm = colors.Normalize(cantons['deaths'].min(), cantons['deaths'].max())

# ADD Custom Colormap, and maybe add quanntile management of colors
cantons.plot(ax=ax_map_switzerland, column='deaths', cmap='autumn')

for idx, row in cantons.iterrows():
    # we want only to annotate each cantons once
    if not np.isnan(row['KANTONSFLA']):
        plt.annotate(row['deaths'], xy=row['coords'], horizontalalignment='center', color='black', size=20)

plt.title('Todesfälle pro Kanton', fontsize=30)
st.pyplot(fig)

# Deutschland
st.subheader('Deutschland')

# Getting the coords for applying the information per canton
germany = gpd.read_file(r"data\shapefiles\deutschland\vg2500_bld.shp")

fig, ax_map_germany = plt.subplots(figsize=(20, 20), dpi=96)
ax_map_germany.set_axis_off()

germany.plot(ax=ax_map_germany, column='RS', cmap='autumn')

plt.title('Todesfälle pro Bundesland', fontsize=30)
st.pyplot(fig)

# Österreich
st.subheader('Österreich')

# Getting the coords for applying the information per canton
austria = gpd.read_file(r'data\shapefiles\oesterreich\Bundeslaender_50.shp')

fig, ax_map_austria = plt.subplots(figsize=(20, 20), dpi=96)
ax_map_austria.set_axis_off()

austria.plot(ax=ax_map_austria, column='FL_KM', cmap='autumn')

plt.title('Todesfälle pro Bundesland', fontsize=30)
st.pyplot(fig)

st.header('Impfungen')
st.subheader('')

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
