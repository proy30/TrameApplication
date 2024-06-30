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

    # def filter_data_by_columns(data, selected_columns):
    #     result = []
    #     for row in data:
    #         filtered_row = {}
    #         for col in selected_columns:
    #             filtered_row[col] = row[col]
    #         result.append(filtered_row)
    #     return result

    def combine_files(file1_name, file2_name):
        file1 = Functions.load_data(file1_name)
        file2 = Functions.load_data(file2_name)
        return pd.merge(file1, file2, how='outer')
