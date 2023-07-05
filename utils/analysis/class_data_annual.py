import pandas as pd


class AnnualTotalVolume:
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
        self.transition_dic = {
            "NCM": [],
            "Año": [],
            "Volumen Total": []
        }

    def aggregate_per_year(self) -> pd.DataFrame:

        for df in self.dfs:
            if self.check_valid_dataframe(df):
                df = self.add_code(df)
                df = self.add_year(df)
                df = self.add_total_volume(df)

                print(
                    f"- {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year}) appended.")

                annual_total_volume = pd.DataFrame.from_records(
                    self.transition_dic)

        return annual_total_volume

    def add_code(self, df: pd.DataFrame) -> pd.DataFrame:
        self.transition_dic['NCM'].append(
            ''.join(df['Código NCM'].unique().astype(str).tolist()))
        return df

    def add_year(self, df: pd.DataFrame) -> pd.DataFrame:
        self.transition_dic['Año'].append(df["Fecha"].iloc[0].year)
        return df

    def add_total_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        volumenTotalImportacionTn = (df['Kgs. Netos'].sum()/1000).round(2)
        self.transition_dic['Volumen Total'].append(volumenTotalImportacionTn)
        return df

    def check_valid_dataframe(self, df: pd.DataFrame) -> bool:
        return df is not None and not df.empty
