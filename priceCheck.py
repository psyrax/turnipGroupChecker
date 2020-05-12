# from turnips import meta
# from turnips import model
# from turnips import plots as tplot
# import streamlit as st
# print(meta)
#
# prices = meta.MetaModel.blank(98)
# prices.fix_price(2, 94)
# prices.fix_price(3, 62)
# prices.fix_price(4, 55)
# prices.fix_price(5, 47)
# print(prices.report())
# print(prices.summary())
#
# enums = model.ModelEnum
#
# modelsToPlot = []
# for model in prices.models:
#     modelsToPlot.append(model)
#
# print(modelsToPlot)
#
# st.write(tplot.global_plot(prices))


#!/usr/bin/env python3

from turnips import archipelago
#import streamlit as st

EXAMPLE_DATA = '''
{
    "islands": {
        "islaBonita": {
            "timeline": {
                "Sunday_AM":   94,
                "Monday_AM":   62,
                "Monday_PM":   55,
                "Tuesday_AM":  47,
                "Tuesday_PM":  106,
                "Wednesday_AM":null,
                "Wednesday_PM":null,
                "Thursday_AM": null,
                "Thursday_PM": null,
                "Friday_AM":   null,
                "Friday_PM":   null,
                "Saturday_AM": null,
                "Saturday_PM": null
            }
        },
        "Val Hallen": {
            "timeline": {
                "Sunday_AM":   93,
                "Monday_AM":   160,
                "Monday_PM":   46,
                "Tuesday_AM":  143,
                "Tuesday_PM":  160,
                "Wednesday_AM":null,
                "Wednesday_PM":null,
                "Thursday_AM": null,
                "Thursday_PM": null,
                "Friday_AM":   null,
                "Friday_PM":   null,
                "Saturday_AM": null,
                "Saturday_PM": null
            }
        },
        "Endor": {
            "timeline": {
                "Sunday_AM":   103,
                "Monday_AM":   92,
                "Monday_PM":   119,
                "Tuesday_AM":  187,
                "Tuesday_PM":  null,
                "Wednesday_AM":null,
                "Wednesday_PM":null,
                "Thursday_AM": null,
                "Thursday_PM": null,
                "Friday_AM":   null,
                "Friday_PM":   null,
                "Saturday_AM": null,
                "Saturday_PM": null
            }
        }
    }
}
'''
from turnips.plots import plot_models_range_interactive, plot_models_range_data, global_plot
islands = archipelago.Archipelago.load_json(EXAMPLE_DATA)
for island in islands.islands:
    print(island.plot())
print(dir(islands))
print(islands.plot())
print(print(islands.summary()))
