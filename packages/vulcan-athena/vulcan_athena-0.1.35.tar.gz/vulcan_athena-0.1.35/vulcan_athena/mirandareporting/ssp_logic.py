import pandas as pd
from vulcan_athena.mirandareporting.setup import filepath, sheetname


def ssp_processing(ssp_data):
    ssp_data = ssp_data.loc[2:]
    ssp_data = ssp_data.drop(['Unnamed: 0', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10'], axis=1)
    new_header = ssp_data.iloc[0]  # grab the first row for the header
    ssp_data = ssp_data[1:]  # take the data less the header row
    header = [str(x).split('.')[0] for x in new_header]
    ssp_data.columns = header  # set the header row as the df header
    ssp_data = ssp_data.fillna(0)

    return ssp_data


def ssp_logic(name, year, df):
    ssp = df[(df['Name'] == name) & (df['year'] == year) & (df['Status'] == 'Delivered')]['SSP']
    if len(ssp):
        return ssp.iloc[0]  # TODO: check with Alex
    else:
        # future deal same year
        ssp = df[(df['Name'] == name) & (df['year'] == year) & (df['Status'] == 'Future')]['SSP']
        if len(ssp):
            return max(ssp)  # highest ssp returned
        else:
            # future deal year before
            ssp = df[(df['Name'] == name) & (df['year'] == (year - 1)) & (df['Status'] == 'Future')]['SSP']
            if len(ssp):
                return max(ssp)
            else:
                # future deal year after
                ssp = df[(df['Name'] == name) & (df['year'] == (year + 1)) & (df['Status'] == 'Future')]['SSP']
                if len(ssp):
                    return max(ssp)
                else:
                    # highest ssp in the delivered deal
                    ssp = df[(df['Name'] == name) & (df['Status'] == 'Delivered')]['SSP']
                    if len(ssp):
                        return max(ssp)
                    else:
                        return 0


def ssp_df_creator():
    ssp_sheetname = 'Current SSPs'
    # reading in the data and manipulating it
    ssp_data = pd.read_excel(filepath, ssp_sheetname)

    df = pd.read_excel(filepath, sheetname)
    df['year'] = df['ValueDate'].dt.year

    ssp_df = ssp_processing(ssp_data)
    # for the purposes of this report, we only need 2019, 2020 and 2021
    # ssp_df = ssp_df.drop(['2022', '2023'], axis=1)

    for idx, row in ssp_df.iterrows():
        years = ['2019', '2020', '2021', '2022', '2023']
        for year in years:
            if not row[year] or row[year] == 9999:
                ssp_df.at[idx, year] = ssp_logic(row['Row Labels'], int(year), df)

    ssp_df = ssp_df.set_index('Row Labels')

    return ssp_df
