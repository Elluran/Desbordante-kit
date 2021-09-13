MEM_LIMIT = 3000 #MB
TIME_LIMIT = 10
NUM_OF_MEASURES = 6
algorithms = ['tane', 'pyro', 'fdmine', 'fastfds', 'dfd']
datasets = ['adult.csv', 'CIPublicHighway50k.csv', 
'CIPublicHighway100k.csv', 'breast_cancer.csv', 'CIPublicHighway.csv']
# telegram bot
bot_token = ''
telegram_ids = []

import psutil
MEM_LIMIT = min(MEM_LIMIT, psutil.virtual_memory()[0])