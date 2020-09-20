import pandas as pd
from datetime import datetime as dt
from scraper.models import *
from datetime import timedelta

class DocLoader:
    def __init__(self):
        self.engine = db_connect()

    def _write_to_db(self, data, tablename, db_mode):
        data.to_sql(tablename, self.engine, if_exists=db_mode, index_label='id')

    def _write_to_txt(self, data, folder, file):
        self.data = data.input_data
        with open(f'{folder}\{file}.txt', 'w', encoding="utf-8") as fw:
            for sample in self.data:
                fw.write(sample + "\n")

    def _read_from_txt(self, folder, file):
        txt_list = []
        with open(f"{folder}\{file}.txt", "r", encoding="utf-8") as fr:
            for line in fr:
                stripped_line = line.strip()
                txt_list.append(stripped_line)
        txt_list = pd.DataFrame(txt_list)
        return txt_list

    def select_data(self, tablename, nDays):
        self.nDays = nDays
        self.tablename = tablename
        data = pd.read_sql_query(f'select * from {tablename}', con=self.engine)
        # fill empty cells with NaN
        data.content = data.content.fillna('').astype(str)
        data.id = data.index
        data = data.loc[data.pubDate >= (dt.now().astimezone() - timedelta(days=self.nDays))]
        print(f'Found {data.shape[0]} Articles!')
        return data