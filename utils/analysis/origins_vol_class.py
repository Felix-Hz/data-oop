import pandas as pd


class AnalyzeOrigins:
    '''

        Calculates the annual total volume for each NCM code in the provided DataFrames.

            Args:
                - dfs: a list of pandas DataFrames containing import data.

            Returns:
                - annual_total_volume: a pandas DataFrame with columns 'NCM', 'Año', and 'Volumen Total',
                where 'NCM' is the NCM code, 'Año' is the year of the data, and 'Volumen Total' is the
                annual total import volume in metric tons.

    '''

    def __init__(self, dfs: list):
        self.dfs = dfs
        self.excel_new_data = pd.DataFrame()

    def aggregate_per_origins(self) -> pd.DataFrame:
        # instantiate var
        self.total_import_volume = 0

        for df in self.dfs:
            # need total import vol to calculate mkt participation of each country
            total_import_volume = self.calculate_total_import(df)
            self.total_import_volume += total_import_volume
            self.calculate_values_per_country(df)

        return self.excel_new_data

    def calculate_total_import(self, df: pd.DataFrame) -> float:
        total_import_volume_tonne = (df['Kgs. Netos'].sum() / 1000).round(2)
        return total_import_volume_tonne

    def calculate_values_per_country(self, df: pd.DataFrame) -> None:
        for country in df['País de Origen'].unique():
            # iterate countries to grab their stats
            register_volume = {
                "NCM": [],
                "Year": [],
                "Country": [],
                "No. Imports": [],
                "Total Volume (TN)": [],
                "Participation": []
            }

            data = df[df['País de Origen'] == country]
            origin_total_volume = (data['Kgs. Netos'].sum() / 1000).round(2)

            if self.bigger_than_100(data):
                # calculate the stats only if the country has more than 100.000 kg of imports
                self.calculate_country(
                    register_volume, df, data, country, origin_total_volume)

    def calculate_country(self, register_volume: dict, df: pd.DataFrame, data: pd.DataFrame, country: str, origin_total_volume: float) -> None:
        # add code
        register_volume['NCM'].append(
            ''.join(df['Código NCM'].unique().astype(str).tolist()))
        # add year
        register_volume['Year'].append(
            str(data["Fecha"].iloc[0].year)[:4])
        # add name of the country
        register_volume['Country'].append(country)
        # add qty of imports
        register_volume['No. Imports'].append(len(data))
        # add volume sum in tonnes
        register_volume['Total Volume (TN)'].append(
            origin_total_volume)
        # add market participation calculated out of the total import volume
        register_volume['Participation'].append(
            f"{round((origin_total_volume / self.total_import_volume) * 100)}%")
        # log process on console
        print(
            f"- Done with: {country} in {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year})")
        # add the country to the main df
        self.append_dataframe(register_volume)

    def bigger_than_100(self, df: pd.DataFrame) -> bool:
        # check if the current df surpasses the threshold
        return df['Kgs. Netos'].sum() > 100000

    def append_dataframe(self, register_volume: dict) -> None:
        transition_df = pd.DataFrame.from_records(register_volume).sort_values(
            'Total Volume (TN)', ascending=False).reset_index(drop=True)
        transition_df = transition_df[[
            'NCM', 'Year', 'Country', 'Total Volume (TN)', "Participation", 'No. Imports']]
        self.excel_new_data = pd.concat(
            [self.excel_new_data, transition_df], ignore_index=True)
