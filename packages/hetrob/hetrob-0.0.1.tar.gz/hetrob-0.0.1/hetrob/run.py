import importlib.util
import logging
import datetime
import time
import os
import sys
from typing import Callable

import numpy as np

from hetrob.util import create_folder
from hetrob.data import load_data_raw
from hetrob.result import TestResults, ExperimentResult, ExperimentStatistics, InstanceBatching


def _setup_logger(name: str, log_path: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename=log_path, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def dynamic_import(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    sys.modules[name] = config

    return config


def run_file(path: str):
    """
    **DEPRECATED**


    :param path:
    :return:
    """
    # Dynamically import the file as a module
    config = dynamic_import('config', path)

    # Setting up the logging for this computational run
    logger = _setup_logger('COMPUTE', config.LOG_PATH)

    # Creating the results object, which will store and persist all the results from the computations
    # And registering all the algorithms which are defined in the config file
    results = TestResults(config.RESULTS_PATH)
    results.shelf['file'] = path
    algorithm_count = 0
    for name, algorithm in config.ALGORITHMS.items():
        results.register_algorithm(algorithm['name'], algorithm['description'])
        logger.info('REGISTERED ALGORITHM {} FOR TEST RESULTS'.format(algorithm['name']))
        algorithm_count += 1

    # Using the variables defined in the file to run the instances
    logger.info('STARTING COMPUTATION!')
    instance_index = 1
    instance_count = len(config.INSTANCES)
    start_time = time.time()
    rep_times = []
    for instance_name, instance_path in config.INSTANCES.items():
        logger.info('STARTING INSTANCE [{}/{}] WITH NAME "{}"'.format(
            instance_index,
            instance_count,
            instance_name
        ))

        data = load_data_raw(instance_path)
        problem = config.PROBLEM_CLASS.from_dicts(
            nodes=data['nodes'],
            vehicles=data['vehicles']
        )

        # Adding the instance to all the registered algorithms results
        for name, algorithm in config.ALGORITHMS.items():
            results.add_instance(name, instance_name, data['doc'])

        rep_index = 1
        for rep in range(config.REPETITIONS):
            rep_start_time = time.time()

            for name, algorithm in config.ALGORITHMS.items():
                static_kwargs = algorithm['static_kwargs']
                dynamic_kwargs = algorithm['dynamic_kwargs'](problem)

                outcome = algorithm['solve'](
                    **dynamic_kwargs,
                    **static_kwargs
                )

                results.add_run(
                    algorithm['name'],
                    instance_name,
                    outcome,
                    fix_imports=path
                )

            rep_time = time.time() - rep_start_time
            rep_times.append(rep_time)
            missing_reps = config.REPETITIONS * instance_count - len(rep_times)
            eta = missing_reps * np.mean(rep_times)
            logger.info('   FINISHED REP ({}/{}) in {} seconds; ETA {} hrs ({})'.format(
                rep_index,
                config.REPETITIONS,
                rep_time,
                round(eta / 3600, 3),
                datetime.datetime.fromtimestamp(time.time() + eta).strftime('%d.%m.%Y %H:%M')
            ))
            rep_index += 1

        instance_index += 1

    logger.info('FINISHED COMPUTATION IN {} HOURS'.format(round((time.time() - start_time) / 3600, 3)))
    results.calculate_statistics()
    results.close()
    logger.info('CALCULATED STATISTICS AND NOW CLOSING RESULTS "{}"'.format(config.RESULTS_PATH))


def run_experiment_file(file_path: str):
    config = dynamic_import('config', file_path)
    run_experiment_module(config)


def run_experiment_module(config):
    folder_path = config.PATH
    create_folder(folder_path)

    log_path = os.path.join(folder_path, 'output.log')
    logger = _setup_logger('COMPUTE', log_path)

    result = ExperimentResult(folder_path, batching_strategy=config.BATCHING)

    logger.info('STARTING COMPUTATION!')

    instance_count = len(config.INSTANCES)
    instance_index = 1

    start_time = time.time()
    rep_times = []

    for instance_name, instance_path in config.INSTANCES.items():
        logger.info('STARTING INSTANCE [{}/{}] WITH NAME "{}"'.format(
            instance_index,
            instance_count,
            instance_name
        ))

        data = load_data_raw(instance_path)
        problem = config.PROBLEM_CLASS.from_dict(data)

        rep_index = 1
        for rep in range(config.REPETITIONS):
            rep_start_time = time.time()

            for algorithm_name, algorithm_spec in config.ALGORITHMS.items():
                static_kwargs = algorithm_spec['static_kwargs']
                dynamic_kwargs = algorithm_spec['dynamic_kwargs'](problem)

                algorithm_result = algorithm_spec['solve'](
                    **dynamic_kwargs,
                    **static_kwargs
                )

                result.add_run(algorithm_name, instance_name, str(rep_index), algorithm_result)

            rep_time = time.time() - rep_start_time
            rep_times.append(rep_time)
            missing_reps = config.REPETITIONS * instance_count - len(rep_times)
            eta = missing_reps * np.mean(rep_times)
            logger.info('   FINISHED REP ({}/{}) in {} seconds; ETA {} hrs ({})'.format(
                rep_index,
                config.REPETITIONS,
                rep_time,
                round(eta / 3600, 3),
                datetime.datetime.fromtimestamp(time.time() + eta).strftime('%d.%m.%Y %H:%M')
            ))
            rep_index += 1

        instance_index += 1

    logger.info('FINISHED COMPUTATION IN {} HOURS'.format(round((time.time() - start_time) / 3600, 3)))

    statistics = ExperimentStatistics.from_experiment_result(result)
    statistics_path = os.path.join(folder_path, 'stats.json')
    statistics.save(statistics_path)

    logger.info('CALCULATED STATISTICS AND NOW CLOSING RESULTS "{}"'.format(config.PATH))

    # 19.09.2020: This is an important addition. With the previous version of this function I did not properly close
    # the logger. This led to the fact that when this function was executed multiple times in the same logger context
    # every new execution would print an additional message. So for example the fourth execution the logger would print
    # the exact same message four times!
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # 20.09.2020: This is another important addition. Since the ExperimentResult instance deals a lot with actual files
    # and their handling, this is important to make sure that all files are properly saved at the end!
    result.close()
