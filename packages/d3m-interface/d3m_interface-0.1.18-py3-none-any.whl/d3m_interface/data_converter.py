import os
import json
import shutil
import logging
import pandas as pd
from os.path import join, exists, split
from d3m.container import Dataset
from d3m.utils import fix_uri
from d3m.container.utils import save_container
from d3m.metadata.problem import PerformanceMetricBase, TaskKeywordBase

logger = logging.getLogger(__name__)
DATASET_ID = 'internal_dataset'


def is_d3m_format(dataset, suffix):
    if isinstance(dataset, str) and exists(join(dataset, 'dataset_%s/datasetDoc.json' % suffix)):
        return True

    return False


def convert_d3m_format(dataset_uri, output_folder, problem_config, suffix):
    logger.info('Reiceving a raw dataset, converting to D3M format')
    problem_config = check_problem_config(problem_config)
    dataset_folder = join(output_folder, 'temp', 'dataset_d3mformat', suffix, 'dataset_%s' % suffix)
    problem_folder = join(output_folder, 'temp', 'dataset_d3mformat', suffix, 'problem_%s' % suffix)
    dataset = create_d3m_dataset(dataset_uri, dataset_folder)
    create_d3m_problem(dataset['learningData'], problem_folder, problem_config)

    return join(output_folder, 'temp', 'dataset_d3mformat', suffix)


def check_problem_config(problem_config):
    if problem_config['target_column'] is None:
        raise ValueError('Parameter "target" not provided, but it is mandatory')

    valid_task_keywords = {keyword for keyword in TaskKeywordBase.get_map().keys() if keyword is not None}
    if problem_config['task_keywords'] is None:
        problem_config['task_keywords'] = ['classification', 'multiClass']
        logger.warning('Task keywords not defined, using: [%s]' % ', '.join(problem_config['task_keywords']))

    for task_keyword in problem_config['task_keywords']:
        if task_keyword not in valid_task_keywords:
            raise ValueError('Unknown "%s" task keyword, you should choose among [%s]' %
                             (task_keyword, ', '.join(valid_task_keywords)))

    valid_metrics = {metric for metric in PerformanceMetricBase.get_map()}
    if problem_config['metric'] is None:
        problem_config['metric'] = 'accuracy'
        if 'regression' in problem_config['task_keywords']:
            problem_config['metric'] = 'rootMeanSquaredError'
        logger.warning('Metric not defined, using: %s' % problem_config['metric'])
    elif problem_config['metric'] not in valid_metrics:
        raise ValueError('Unknown "%s" metric, you should choose among [%s]' %
                         (problem_config['metric'], ', '.join(valid_metrics)))

    #  Check special cases
    if problem_config['metric'] == 'f1' and 'binary' in problem_config['task_keywords'] and \
            'pos_label' not in problem_config['optional']:
        raise ValueError('pos_label parameter is mandatory for f1 and binary problems')

    return problem_config


def create_d3m_dataset(dataset_uri, destination_path):
    if callable(dataset_uri):
        dataset_uri = 'sklearn://' + dataset_uri.__name__.replace('load_', '')
    if exists(destination_path):
        shutil.rmtree(destination_path)

    dataset = Dataset.load(fix_uri(dataset_uri), dataset_id=DATASET_ID)
    save_container(dataset, destination_path)

    return dataset


def create_d3m_problem(dataset, destination_path, problem_config):
    target_index = dataset.columns.get_loc(problem_config['target_column'])
    problem_config['target_index'] = target_index

    if exists(destination_path):
        shutil.rmtree(destination_path)
    os.makedirs(destination_path)

    metric = {"metric": problem_config['metric']}
    if 'pos_label' in problem_config['optional']:
        metric['posLabel'] = str(problem_config['optional']['pos_label'])

    problem_json = {
          "about": {
            "problemID": "",
            "problemName": "",
            "problemDescription": "",
            "problemVersion": "4.0.0",
            "problemSchemaVersion": "4.0.0",
            "taskKeywords": problem_config['task_keywords']
          },
          "inputs": {
            "data": [
              {
                "datasetID": DATASET_ID,
                "targets": [
                  {
                    "targetIndex": 0,
                    "resID": "learningData",
                    "colIndex": problem_config['target_index'],
                    "colName": problem_config['target_column']
                  }
                ]
              }
            ],
            "performanceMetrics": [metric]
          },
          "expectedOutputs": {
            "predictionsFile": "predictions.csv"
          }
        }

    with open(join(destination_path, 'problemDoc.json'), 'w') as fout:
        json.dump(problem_json, fout, indent=4)


def convert_d3mtext_dataframe(folder_path, text_column):
    suffix = split(folder_path)[1]
    dataframe = pd.read_csv(join(folder_path, 'dataset_%s/tables/learningData.csv' % suffix))
    folder_files = join(folder_path, 'dataset_%s/media/' % suffix)

    for index, row in dataframe.iterrows():
        file_path = join(folder_files, row[text_column])
        with open(file_path, 'r') as fin:
            text = fin.read().replace('\n', ' ')
            dataframe.at[index, text_column] = text

    return dataframe


def copy_folder(source_path, destination_path):
    if exists(destination_path):
        shutil.rmtree(destination_path)

    shutil.copytree(source_path, destination_path)
