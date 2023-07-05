import pandas as pd


class TopImporters:
    '''
            Calculates the annual total volume for each NCM code in the provided DataFrames,
            and identifies the top importers for each NCM code.

            Args:
                dfs (list): A list of pandas DataFrames containing import data.

            Returns:
                companies_df (pandas DataFrame): A DataFrame with columns "Año", "NCM", "Importador",
                "Proveedores", "Precio Promedio", "Volumen Total (TN)", and "Participacion".
                This DataFrame represents the top importers for each NCM code, where:
                - "Año" is the year of the data,
                - "NCM" is the NCM code,
                - "Importador" is the importer name,
                - "Proveedores" is a comma-separated list of suppliers,
                - "Precio Promedio" is the average unit price in USD,
                - "Volumen Total (TN)" is the total import volume in metric tons,
                - "Participacion" is the importer's contribution as a percentage of the total import volume.

    '''

    def __init__(self, dfs: list) -> None:
        self.dfs = dfs
        self.companies_df = pd.DataFrame(columns=[
            "Year", "NCM", "Importer", "Providers",
            "Avg. Price", "Total Volume (TN)", "Participation"
        ])

    def aggregate_imports_per_company(self):
        # iterate the dfs and grab the top three importers
        for df in self.dfs:
            # total volume to calculate the mkt participation of each company in the end
            total_volume_import_tonnes = (
                df['Kgs. Netos'].sum() / 1000).round(2)

            company_dic = {
                "Year": [],
                "NCM": [],
                "Importer": [],
                "Providers": [],
                "Avg. Price": [],
                "Total Volume (TN)": [],
                "Participation": []
            }

            # do the stats for each company that is registered as an importer
            for company in df['Importador'].unique():
                data = df[df['Importador'] == company]
                self.calculate_company(
                    df, data, company_dic, company, total_volume_import_tonnes)

            # add the ones that checked all the requirements
            self.append_company(company_dic)

        return self.companies_df

    def calculate_company(self, df: pd.DataFrame, data: pd.DataFrame, company_dic: dict, company: str, total_volume_import_tonnes: float):
        # check if the data is bigger than the 1.5k threshold
        if self.import_lower_bound(data):
            # append companies to dict
            # calculate volume per company to grab the mkt participation/year of each
            total_volume_per_company = (
                data['Kgs. Netos'].sum() / 1000).round(2)
            # add name
            company_dic['Importer'].append(company)
            # add product code
            company_dic['NCM'].append(
                ''.join(df['Código NCM'].unique().astype(str).tolist()))
            # add providers
            company_dic['Providers'].append(
                ', '.join(data['Proveedor'].unique().tolist()))
            # add year
            company_dic['Year'].append(data["Fecha"].iloc[0].year)
            # add average price of import
            company_dic['Avg. Price'].append(
                (data['U$S Unitario'].mean().round(2)) * 1000)
            # add total import volume in tonnes
            company_dic['Total Volume (TN)'].append(
                total_volume_per_company)
            # add market participation
            company_dic['Participation'].append(
                f"{round((total_volume_per_company / total_volume_import_tonnes) * 100)}%")
            # log progress in console
            print(
                f"- Done with: {company} - {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year})")

    def append_company(self, company_dic: dict):
        # filter the best companies from the df
        transition_df = pd.DataFrame.from_records(company_dic)
        transition_df = transition_df.sort_values(
            by="Total Volume (TN)", ascending=False)
        # select the top three importers
        transition_df_head = transition_df.head(3)

        # append only the top three importers of each country
        self.companies_df = pd.concat(
            [self.companies_df, transition_df_head], ignore_index=True)

    def import_lower_bound(self, df: pd.DataFrame) -> bool:
        # check if the companies pass the threshold
        return df['Kgs. Netos'].sum() > 1500
