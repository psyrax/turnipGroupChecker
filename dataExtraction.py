import pandas as pd
import matplotlib.pyplot as plt
import gspread_pandas
from gspread_pandas import Spread, Client
import json
import inquirer
from turnips import archipelago
import json


"""
Script to extract turnip info from a google spreadsheet, transform it and then upload
the results to google sheets.
"""


gSpreadConfig = gspread_pandas.conf.get_config(conf_dir="./", file_name="client_id.json")

gSpreadClient = Client('naboHolding',config=gSpreadConfig)
naboHoldingListFiles = gSpreadClient.list_spreadsheet_files('naboHolding')

naboFileNames = []
for file in naboHoldingListFiles:
    naboFileNames.append(file['name'])

print(naboFileNames)

questions = [
    inquirer.List('naboFile', message="Which file to work:", choices=naboFileNames, default=naboFileNames[0])
]

answers = inquirer.prompt(questions)

print(answers)

spread = Spread(answers['naboFile'], config=gSpreadConfig)
naboDF = spread.sheet_to_df()
archipielagoData = {}
archipielagoData['islands'] = {}
for index, row in naboDF.iterrows():
    archipielagoData['islands'][row['Isla']] = {
        "timeline": {
            "Sunday_AM": row['Precio Nabo'],
        }
    }
    if row['Lunes AM']:
        archipielagoData['islands'][row['Isla']]['timeline']['Monday_AM'] = row['Lunes AM']
    if row['Lunes PM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Monday_PM'] = row['Lunes PM']
    if row['Martes AM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Tuesday_AM'] = row['Martes AM']
    if row['Martes PM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Tuesday_PM'] = row['Martes PM']
    if row['Miercoles AM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Wednesday_AM'] = row['Miercoles AM']
    if row['Miercoles PM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Wednesday_PM'] = row['Miercoles PM']
    if row['Jueves AM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Thursday_AM'] = row['Jueves AM']
    if row['Jueves PM']:
        archipielagoData['islands'][row['Isla']
                                    ]['timeline']['Thursday_PM'] = row['Jueves PM']

jsonDataTurnips = json.dumps(archipielagoData)
islands = archipelago.Archipelago.load_json(jsonDataTurnips)


islandsDFData = {}
archipielagoDFs = []
for island in islands.islands:
    if islandsDFData.get(island.name) is None:
        islandsDFData[island.name] = {}
    islandsDFData[island.name].update(island.model_group.histogram())
    for histogram in islandsDFData[island.name]:
        df = pd.DataFrame.from_dict(islandsDFData[island.name][histogram], orient='index').reset_index(
        ).rename(columns={'index': 'price', 0: 'count'})
        df['selling_time'] = str(histogram)
        df['island'] = island.name
        archipielagoDFs.append(df)


archDf = pd.concat(archipielagoDFs, ignore_index=True)
labels = ['Poco probable', 'Nada probable', 'Probable', 'Muy probable']
archDf['rangoPrecio'] = pd.cut(archDf['count'], 4, labels=labels)
priceCutLabels = ['0-100', '100-200', '200-300', '300-400', '500-600', '600+']
archDf['priceCut'] = pd.cut(archDf['price'], 6, labels=priceCutLabels)
archDf['count'].fillna(0, inplace=True)


spread.df_to_sheet(archDf, index=False, sheet='10May-16MayData', replace=True)


groupedCounts = archDf.groupby(['rangoPrecio', 'priceCut', 'selling_time'])[
    'count'].sum().reset_index()
groupedCounts['percentage'] = groupedCounts['count'] / \
    groupedCounts['count'].sum()
groupedCounts['count'].fillna(0, inplace=True)
groupedCounts['percentage'].fillna(0, inplace=True)


spread.df_to_sheet(groupedCounts, index=False,
                   sheet='10May-16MayDataGrouped', replace=True)
