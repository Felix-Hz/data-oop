import pandas as pd

class DataWrangler:
    """

        Data wrangling for initial dataframes. This class selects columns, deletes airway products, standardizes NCMs,
        creates a unitary U$S price, filters unitary price, removes outliers & drops nulls.

            Args:
                - dfs (list): A list of dataframes to be cleaned and processed.

            Returns:
                - list: A list of clean dataframes.

    """

    def __init__(self, dfs: list) -> list:
        self.dfs = dfs
        self.results_dfs = []

    def wrangle(self):
        print(f"\n> WRANGLING HISTORICAL DATA:\n")

        for i in range(len(self.dfs)):
            df = self.dfs[i]
            year_error_memory = df["Fecha"].iloc[0].year

            df = self.select_columns(df)
            df = self.delete_airway_products(df)
            df = self.standardize_ncms(df)
            df = self.create_unitary_price(df)
            df = self.filter_unitary_price(df)
            df = self.drop_outliers(df)
            df = self.drop_nulls(df)
            df = self.convert_to_datetime(df)

            self.results_dfs.append(df)
            self.dfs[i] = df

            if self.check_valid_dataframe(df):
                print(
                    f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')
            else:
                print(
                    f'> No data for: {year_error_memory}\n~~~~~~~~~~~~~~~~~~~')

        return self.results_dfs

    def select_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[:, ['Código NCM', 'Fecha', 'País de Origen', 'Importador', 'Cantidad Comercial', 'Unidad de Medida',
                      'Tipo de Bulto', 'Proveedor', 'Aduana', 'Vía Transporte', 'U$S CIF', 'U$S FOB', 'Kgs. Netos',
                          'Marca', 'Descripción de Mercadería', 'Descripción para Filtro']]

    def delete_airway_products(self, df: pd.DataFrame) -> pd.DataFrame:
        subset = df['Vía Transporte']
        return df[subset != 'AEREA']

    def standardize_ncms(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Código NCM'] = df['Código NCM'].astype(
            str).str.replace('.', '')
        df['Código NCM'] = df['Código NCM'].astype(
            str).str.replace('[a-zA-Z]', '')
        df['Código NCM'] = df['Código NCM'].astype(str).str[:6]
        return df

    def create_unitary_price(self, df: pd.DataFrame) -> pd.DataFrame:
        df["U$S Unitario"] = (df['U$S CIF'] / df['Kgs. Netos']).round(2)
        return df

    def filter_unitary_price(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[df['U$S Unitario'] <= 1.2]

    def drop_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        q1 = df['U$S Unitario'].quantile(0.25)
        q3 = df['U$S Unitario'].quantile(0.75)
        interquartileRange = q3 - q1
        lower_bound = q1 - 1.5 * interquartileRange
        upper_bound = q3 + 1.5 * interquartileRange
        outlier_indices = df[(df['U$S Unitario'] < lower_bound) | (
            df['U$S Unitario'] > upper_bound)].index
        return df.drop(outlier_indices)

    def drop_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna()

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
        return df

    def check_valid_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        return df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year)
