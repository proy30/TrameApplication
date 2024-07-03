import pandas as pd

class Functions:
    def load_data(file_path):
        df = pd.read_csv(file_path, sep=' ')
        return df

    def convert_to_dict(combined_data):
        dictionary = combined_data.to_dict(orient='records')
        columns = combined_data.columns
        headers = [{"text": column.strip(), "value": column.strip()} for column in columns]
        return dictionary, headers

    def combine_files(file1_name, file2_name):
        file1 = Functions.load_data(file1_name)
        file2 = Functions.load_data(file2_name)
        return pd.merge(file1, file2, how='outer')

    def filter_headers(allHeaders, selected_headers):
        filtered_headers = []
        for selectedHeader in allHeaders:
            if selectedHeader['value'] in selected_headers:
                filtered_headers.append(selectedHeader)
        return filtered_headers

    def filter_data(allData, selected_headers):
        filtered_data = []
        for row in allData:
            filtered_row = {}
            for key, value in row.items():
                if key in selected_headers:
                    filtered_row[key] = value
            filtered_data.append(filtered_row)
        return filtered_data