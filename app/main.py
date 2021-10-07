import config
import telegram_api as tg
import psutil
import pandas as pd
import platform
import subprocess
import time
import os
import io
import multiprocessing
import re
import resource
import traceback
import seaborn as sns
import matplotlib.pyplot as plt

def get_cpu_caches_sizes():
    tmp = subprocess.check_output(['lscpu']).decode('utf-8').split('\n')
    tmp = list(filter(lambda x: re.search('cache', x), tmp))[:4]
    L1d, L1i, L2, L3 = map(lambda x: int(x.split()[2]) * 1024 if x.split()[3] == 'MiB' else int(x.split()[2]), tmp) 
    return L1d, L1i, L2, L3


def get_cpu_model():
    cpu_model = subprocess.check_output(['grep', 'model name', '/proc/cpuinfo']).decode('utf-8')
    return cpu_model.split('\n')[0].split(':')[1]


def get_ram_freq():
    
    freq = subprocess.check_output(['dmidecode', '--type=17']).decode('utf-8').split('\n')
    freq = list(filter(lambda x: re.search('Configured Memory Speed', x), freq))[0]
    return freq.split(':')[1].split()[0]


def run_desbordante(algorithm, dataset):
    try:
        start = time.time_ns()
        devnull = open(os.devnull, 'w')

        subprocess.check_output(['Desbordante/build/target/fdtester_run', 
        '--algo=' + algorithm, '--data=' + dataset], timeout=config.TIME_LIMIT, stderr=devnull)

        return time.time_ns() - start
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError:
        # std::bad_alloc
        return None


def measure():
    measures = []

    for algorithm in config.algorithms:
        for dataset in config.datasets:
            for _ in range(config.NUM_OF_MEASURES):
                
                t = run_desbordante(algorithm=algorithm, dataset=dataset)

                measures.append([algorithm, dataset, t])

                if t:
                    print(algorithm, dataset, f"time: {t / 1e9} sec")
                else:
                    print(algorithm, dataset, "TL or ML")
                    if config.SKIP_IF_FAILED_ONCE:
                        break

    return measures


def form_dataframe(measures):
    df = pd.DataFrame(measures, columns=['algo', 'dataset', 'time'])

    # system
    df['system'] = platform.system()
    # cpu
    df['cpu_model'] = get_cpu_model()
    df['cpu_freq_current'] = psutil.cpu_freq(percpu=False)[0]
    df['cpu_freq_min'] = psutil.cpu_freq(percpu=False)[1]
    df['cpu_freq_max'] = psutil.cpu_freq(percpu=False)[2]
    df['cpu_cores'] = len(psutil.Process().cpu_affinity())
    # cpu caches
    L1d, L1i, L2, L3 = get_cpu_caches_sizes()
    df['cpu_L1d'] = L1d
    df['cpu_L1i'] = L1i
    df['cpu_L2'] = L2
    df['cpu_L3'] = L3
    # mem
    df['ram_size'] = config.MEM_LIMIT
    df['ram_freq'] = get_ram_freq()

    return df

def send_results(filename):
    for user_id in config.telegram_ids:
        tg.send_document(user_id=user_id, filename=f'{filename}.csv')
        tg.send_document(user_id=user_id, filename=f'{filename}.png')



def plot_graph(data, filename):   
    f, ax = plt.subplots(figsize=(12, 14))
    sns.swarmplot(x='dataset', y='time', hue='algo', data=data, ax=ax)
    plt.xticks(rotation=45)
    plt.savefig(f'{filename}.png')

if __name__ == "__main__":
    try:
        if os.getuid() != 0:
            print('You should provide admin rights to the program')
            quit(0)

        # ram limit
        # resource.setrlimit(resource.RLIMIT_DATA, (config.MEM_LIMIT * 1024 * 1024, config.MEM_LIMIT * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_AS, (config.MEM_LIMIT * 1024 * 1024, config.MEM_LIMIT * 1024 * 1024))

        measures = measure()
        df = form_dataframe(measures)
        print(df)

        filename = str(time.time_ns())   
        plot_graph(df, filename)
        
        df.to_csv(f'{filename}.csv')
        send_results(filename)

    except Exception as e:
        for user_id in config.telegram_ids:
            tg.send_message(user_id=user_id, message=str(e))
            tg.send_message(user_id=user_id, message=traceback.format_exc())

        raise e
            