import sys
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
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    os.makedirs(f'{tgt_base_dir}/{ds_name}', exist_ok=True)
    df.to_json(json_file_path, orient='records', lines=True)

def file_converter(ds_name, src_base_dir, tgt_base_dir):
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*')
    if len(files) == 0:
        raise NameError(f'No files found for dataset: {ds_name}')
    
    
    for file in files:
        df = read_csv(file, schemas)
        file_name = re.split('[/]', file)[-1]
        to_json(df, tgt_base_dir, ds_name, file_name)

def process_files(ds_names=None):
    # src_base_dir = 'data/retail_db'
    # tgt_base_dir = 'data/retail_db_json'
    src_base_dir = os.environ.get('SRC_BASE_DIR')
    tgt_base_dir = os.environ.get('TGT_BASE_DIR')
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        try:
            file_converter(ds_name,src_base_dir, tgt_base_dir)
        except NameError as e:
            print(f'Error processing dataset {ds_name}: {e}')
            pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ds_names = json.loads(sys.argv[1])
        print(f'Processing datasets: {ds_names}')
        process_files(ds_names)
    else:
        print('Processing all datasets')
        process_files()