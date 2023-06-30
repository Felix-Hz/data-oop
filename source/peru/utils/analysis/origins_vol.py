import pandas as pd

def analyzing_origins(dfs):
    excel_new_data = pd.DataFrame()

    for df in dfs:
        volumenTotalImportacionTn = (df['Kgs. Netos'].sum() / 1000).round(2)

        registro_volumen = {
            "NCM": [],
            "Año": [],
            "Pais": [],
            "No. Importaciones": [],
            "Volumen Total (TN)": [],
            "Participacion en Vol. Total": []
        }

        for pais in df['País de Origen'].unique():
            data = df[df['País de Origen'] == pais]
            volumenTotalOrigen = (data['Kgs. Netos'].sum() / 1000).round(2)

            if data['Kgs. Netos'].sum() > 100000:
                registro_volumen['NCM'].append(''.join(df['Código NCM'].unique().astype(str).tolist()))
                registro_volumen['Año'].append(str(data["Fecha"].iloc[0].year)[:4])
                registro_volumen['Pais'].append(pais)
                registro_volumen['No. Importaciones'].append(len(data))
                registro_volumen['Volumen Total (TN)'].append(volumenTotalOrigen)
                registro_volumen['Participacion en Vol. Total'].append(f"{round((volumenTotalOrigen / volumenTotalImportacionTn) * 100)}%")
                print(f"- Done with: {pais} in {df['Código NCM'].iloc[0]} ({df['Fecha'].iloc[0].year})")

        transition_df = pd.DataFrame.from_records(registro_volumen).sort_values('Volumen Total (TN)', ascending=False).reset_index(drop=True)
        transition_df = transition_df[['NCM', 'Año', 'Pais', 'Volumen Total (TN)', "Participacion en Vol. Total", 'No. Importaciones']]
        excel_new_data = pd.concat([excel_new_data, transition_df], ignore_index=True)

    print("~~~~~~~~~~~~~~~~~~~\n> Current dataframe of the origins of each year:")
    print(excel_new_data)

    return excel_new_data
