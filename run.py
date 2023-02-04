import os
import pandas as pd
from datetime import datetime
from pathlib import Path

epics = pd.read_csv('DukasList.txt', names=['id', 'epic'])
id_to_epic = dict(zip(epics.id, epics.epic))

timeframe = 'd1'

def createLog():
    print("Creating Log")
    log = []
    for index, row in epics.iterrows():
        log.append([row['id'], row['epic'], 'none', 'none'])
    log = pd.DataFrame(log, columns=['id', 'epic', 'from', 'to'])
    log.to_csv('./log.txt', index=None)

def readLog():
    try:
        log = pd.read_csv('./log.txt', index_col=0)
    except FileNotFoundError:
        createLog()
        return readLog()
    return log

log = readLog()

new_log = []

for index, row in log.iterrows():
    prev_start_date = row['from']
    prev_end_date = row['to']
    start_date = "2019-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    new_start_date = start_date
    if prev_start_date != "none" and prev_end_date != 'none':
        new_start_date = prev_end_date
        
    os.system(f"npx dukascopy-node -i {index} -from {new_start_date} -to {end_date} -v true -t {timeframe} -f csv")
    new_log.append([index, row['epic'], f'{start_date}', f'{end_date}'])

new_log = pd.DataFrame(new_log, columns=['id', 'epic', 'from', 'to'])
new_log.to_csv('./log.txt', index=None)

list_of_dataframes = []

for file in os.listdir('./download'):
    if file.endswith('.csv'):
        try:
            prices_df = pd.read_csv(f'./download/{file}')
            prices_df['id'] = id_to_epic[file.split("-")[0]]
            prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
            prices_df['timestamp'] = prices_df['timestamp'].dt.strftime('%Y%m%d')
            cols = prices_df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            prices_df = prices_df[cols]
            list_of_dataframes.append(prices_df)
        except:
            print(f"No data to update for {id_to_epic[file.split('-')[0]]}")


if len(list_of_dataframes) > 0:
    Path("./download/processed/").mkdir(parents=True, exist_ok=True)

    for file in os.listdir('./download/processed'):
        if file.endswith('.csv'):
            list_of_dataframes.append(pd.read_csv(f'./download/processed/{file}', names=['timestamp', 'open', 'low', 'high', 'close', 'volume']))

    all_data = pd.concat(list_of_dataframes, ignore_index=True).drop_duplicates()
    all_data['timestamp'] = all_data['timestamp'].astype(str)
    all_data.sort_values('timestamp')

    for x, y in all_data.groupby('timestamp', as_index=False):
        y.to_csv(f"./download/processed/dukascopy_{x}.csv", index=None, header=None)
else:
    print("No Data To Update")