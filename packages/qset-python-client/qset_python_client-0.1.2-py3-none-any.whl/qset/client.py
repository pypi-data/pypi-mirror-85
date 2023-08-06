import logging
import requests
import pandas as pd
import os
import math

from tenacity import retry, stop_after_attempt, wait_exponential

from qset import utils


class ClientV0:
    def __init__(self, api_key, api_url='http://api.qset.ai/v0', verbose=True):
        self.api_key = api_key
        self.api_url = api_url

        self.verbose = verbose
        self.progress_bar = None

        self._overview = None

    def _log(self, msg, level=logging.INFO):
        if self.verbose:
            logging.log(level, msg)

    def _url(self, path):
        return f'{self.api_url}{path}'

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=5., exp_base=1.5))
    def _call(self, api_path, params=None, decoder=utils.cast_dict_or_list):
        req = requests.get(self._url(api_path), headers={"x-api-key": self.api_key}, params=params)
        return decoder(req.content)

    def get_available_datasets(self, format='dataframe'):
        res = self._call('/available_datasets')

        if format == 'dataframe':
            return pd.DataFrame(res)
        elif format == 'list':
            return res
        else:
            raise Exception('Unknown format')

    def get_dataset_overview(self, dataset):
        return self._call('/dataset_overview', params={'dataset': dataset})

    def get_asset_dataset_range(self, dataset, ticker):
        return self._call('/asset_dataset_range', params={'dataset': dataset, 'ticker': ticker})

    def get_asset_dataset(self, dataset, ticker, start, end, columns=None):
        params = {'dataset': dataset, 'ticker': ticker, 'start': start, 'end': end}
        if columns:
            params['columns'] = utils.cast_js(columns)
        params['format'] = 'msgpack' # for speed and easier type conversion
        return self._call('/asset_dataset', params=params, decoder=utils.MsgPackSerializer.decode)

    def _iter_data(self, dataset, query=None):
        dataset_overview = self.get_dataset_overview(dataset)

        if dataset_overview['type'] != 'asset':
            raise Exception('Client supports only asset datasets at the moment')

        query = query or {}
        query = utils.cast_dict_or_list(query)

        start = utils.cast_datetime(query['start'])
        end = utils.cast_datetime(query['end'])
        ticker = query['ticker']
        columns = query.get('columns')

        if not columns:
            columns = dataset_overview['columns']  # [(column_name, column_type), ...]
            columns = [c[0] for c in columns]

        yield {'type': 'columns', 'data': columns}

        asset_range = self.get_asset_dataset_range(dataset, ticker)

        start = max(utils.cast_datetime(asset_range['minStartRange']), start)
        end = min(utils.cast_datetime(asset_range['maxStartRange']), end)

        if dataset_overview['max_request_range'] == '31d':
            total = len(list(utils.iter_range_by_months(start, end)))
            range_iterator = utils.iter_range_by_months(start, end)
        else:
            total = len(list(utils.iter_range(start, end, utils.cast_timedelta(dataset_overview['max_request_range']))))
            range_iterator = utils.iter_range(start, end, utils.cast_timedelta(dataset_overview['max_request_range']))

        if self.verbose:
            range_iterator = utils.tqdm(range_iterator, total=total, desc=dataset)

        for cur_start, cur_end in range_iterator:
            logging.info(f'Iterating over {cur_start} {cur_end}')
            chunk = self.get_asset_dataset(dataset, ticker, cur_start, cur_end, columns=columns)
            total = chunk['total']

            if total > 0:
                # new chunk
                yield {'type': 'values', 'data': chunk['values']}

    def iter_dataset(self, dataset, handler, query=None):
        self._log(f'Iterating through field data: {dataset}')

        for data in self._iter_data(dataset, query=query):
            handler(**data)

    def get_dataset(self, dataset, query=None):
        self._log(f'Getting field data: {dataset}')

        columns = []
        values = []

        def _load_data_handler(type, data):
            if type == 'columns':
                columns.extend(data)
            elif type == 'values':
                values.extend(data)

        # make requests to load granular_storage
        self.iter_dataset(dataset, _load_data_handler, query=query)

        return pd.DataFrame(values, columns=columns)

    def download_dataset(self, dataset, fn, query=None):
        self._log(f'Downloading field {dataset} data to file {fn}')
        if os.path.exists(fn):
            raise Exception(f'File {fn} already exists')

        writer = utils.PandasWriter(fn)

        def _save_handler(type, data):
            if type == 'columns':
                writer.write_header(data)
            elif type == 'values':
                writer.write_values(data)
        # make requests to save granular_storage
        self.iter_dataset(dataset, _save_handler, query=query)
        writer.flush()


Client = ClientV0