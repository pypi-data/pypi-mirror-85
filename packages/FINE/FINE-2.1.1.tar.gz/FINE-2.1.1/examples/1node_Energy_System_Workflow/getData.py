import pandas as pd
import os


def getData():
    cwd = os.getcwd()
    inputDataPath = os.path.join(cwd, "InputData")
    data = {}

    # Onshore data
    capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Wind', 'maxCapacityOnshore_GW_el.xlsx'),
                                index_col=0, squeeze=True)
    operationRateMax = pd.read_excel(
        os.path.join(inputDataPath, 'SpatialData', 'Wind', 'maxOperationRateOnshore_el.xlsx'))

    data.update({'Wind (onshore), capacityMax': capacityMax.loc['cluster_0']})
    data.update({'Wind (onshore), operationRateMax': operationRateMax.loc[:, 'cluster_0']})

    # Hydrogen salt cavern data
    capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'GeologicalStorage',
                                             'existingSaltCavernsCapacity_GWh_methane.xlsx'),
                                index_col=0, squeeze=True) * 3 / 10

    data.update({'Salt caverns (hydrogen), capacityMax': capacityMax.loc['cluster_0']})

    # Electricity demand data
    operationRateFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Demands',
                                                  'electricityDemand_GWh_el.xlsx'))

    data.update({'Electricity demand, operationRateFix': operationRateFix.loc[:, 'cluster_0']})

    # Hydrogen demand data
    operationRateFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Demands',
                                                  'hydrogenDemand_GWh_hydrogen.xlsx'))

    data.update({'Hydrogen demand, operationRateFix': operationRateFix.loc[:, 'cluster_0']})

    return data
