import pandas as pd

import pandas as pd

def top_importers(dfs):
    companies_df = pd.DataFrame(columns=[
        "Año", "NCM", "Importador", "Proveedores",
        "Precio Promedio", "Volumen Total (TN)", "Participacion"
    ])

    for df in dfs:
        volumenTotalImportacionTn = (df['Kgs. Netos'].sum() / 1000).round(2)

        company_dic = {
            "Año": [],
            "NCM": [],
            "Importador": [],
            "Proveedores": [],
            "Precio Promedio": [],
            "Volumen Total (TN)": [],
            "Participacion": []
        }

        for company in df['Importador'].unique():
            data = df[df['Importador'] == company]

            if data['Kgs. Netos'].sum() > 1500:
                volumenTotalCompania = (data['Kgs. Netos'].sum() / 1000).round(2)

                company_dic['Importador'].append(company)
                company_dic['NCM'].append(''.join(df['Código NCM'].unique().astype(str).tolist()))
                company_dic['Proveedores'].append(', '.join(data['Proveedor'].unique().tolist()))
                company_dic['Año'].append(data["Fecha"].iloc[0].year)
                company_dic['Precio Promedio'].append((data['U$S Unitario'].mean().round(2)) * 1000)
                company_dic['Volumen Total (TN)'].append(volumenTotalCompania)
                company_dic['Participacion'].append(f"{round((volumenTotalCompania / volumenTotalImportacionTn) * 100)}%")

                print(f"- Done with: {company} - {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year})")

        transition_df = pd.DataFrame.from_records(company_dic)
        transition_df = transition_df.sort_values(by="Volumen Total (TN)", ascending=False)
        transition_df_head = transition_df.head(3)

        companies_df = pd.concat([companies_df, transition_df_head], ignore_index=True)

    return companies_df
