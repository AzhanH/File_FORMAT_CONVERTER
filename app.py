import glob
import os
import json
import re
import pandas as pd


def get_column_names(schemas, df, sorting_keys='column_position'):
    column_detail = schemas[df]
    columns_name = sorted(column_detail, key=lambda x: x[sorting_keys])
    return [col['column_name'] for col in columns_name]


def read_csv(file, schemas):
    ds_name = re.split('[/]', file)[-2]
    columns = get_column_names(schemas, ds_name)
    df = pd.read_csv(file, header=None, names=columns)
    return df

def to_json(df, tgt_base_dir, ds_name, file_name):
    print(f'Converting {ds_name}/{file_name} to JSON')
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    os.makedirs(f'{tgt_base_dir}/{ds_name}', exist_ok=True)
    df.to_json(json_file_path, orient='records', lines=True)

def file_converter(ds_name, src_base_dir, tgt_base_dir):
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*')
    for file in files:
        print(f'Processing {file}')
        df = read_csv(file, schemas)
        file_name = re.split('[/]', file)[-1]
        to_json(df, tgt_base_dir, ds_name, file_name)

def process_files(ds_names=None):
    src_base_dir = 'data/retail_db'
    tgt_base_dir = 'data/retail_db_json'
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        print(f'Processing dataset: {ds_name}')
        file_converter(ds_name,src_base_dir, tgt_base_dir)

if __name__ == '__main__':
    process_files()