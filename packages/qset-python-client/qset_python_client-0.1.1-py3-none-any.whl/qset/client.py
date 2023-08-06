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
    def _call(self, api_path, params=None, decoder=utils.cast_dict):
        req = requests.get(self._url(api_path), headers={"x-api-key": self.api_key}, params=params)
        return decoder(req.content)

    def get_overview(self):
        return self._call('/overview')

    def get_field_id(self, universe, dataset, meta):
        return self._call('/field_id', params={'universe': universe, 'dataset': dataset, 'meta': utils.cast_js(meta)})

    def get_field_info(self, field_id):
        return self._call('/field', params={'field_id': field_id})

    def get_historical_info(self, field_id, ticker):
        return self._call('/historical_info', params={'field_id': field_id, 'ticker': ticker})

    def get_historical(self, field_id, ticker, start, end, columns=None):
        params = {'field_id': field_id, 'ticker': ticker, 'start': start, 'end': end}
        if columns:
            params['columns'] = utils.cast_js(columns)
        params['format'] = 'msgpack' # for speed and easier type conversion
        return self._call('/historical', params=params, decoder=utils.MsgPackSerializer.decode)

    def _iter_data(self, field_id, query=None):
        field_info = self.get_field_info(field_id)

        if field_info['field_type'] != 'historical':
            raise Exception('Client supports only historical fields at the moment')

        query = query or {}
        query = utils.cast_dict(query)

        start = utils.cast_datetime(query['start'])
        end = utils.cast_datetime(query['end'])
        ticker = query['ticker']
        columns = query.get('columns')

        if not columns:
            columns = field_info['columns']  # [(column_name, column_type), ...]
            columns = [c[0] for c in columns]

        yield {'type': 'columns', 'data': columns}

        historical_info = self.get_historical_info(field_id, ticker)

        start = max(utils.cast_datetime(historical_info['minStartRange']), start)
        end = min(utils.cast_datetime(historical_info['maxStartRange']), end)

        if field_info['max_request_range'] == '31d':
            total = len(list(utils.iter_range_by_months(start, end)))
            range_iterator = utils.iter_range_by_months(start, end)
        else:
            total = len(list(utils.iter_range(start, end, utils.cast_timedelta(field_info['max_request_range']))))
            range_iterator = utils.iter_range(start, end, utils.cast_timedelta(field_info['max_request_range']))

        if self.verbose:
            range_iterator = utils.tqdm(range_iterator, total=total, desc=field_id)

        for cur_start, cur_end in range_iterator:
            logging.info(f'Iterating over {cur_start} {cur_end}')
            chunk = self.get_historical(field_id, ticker, cur_start, cur_end, columns=columns)
            total = chunk['total']

            if total > 0:
                # new chunk
                yield {'type': 'values', 'data': chunk['values']}

    def iter_data(self, field_id, handler, query=None):
        self._log(f'Iterating through field data: {field_id}')

        for data in self._iter_data(field_id, query=query):
            handler(**data)

    def get_data(self, field_id, query=None):
        self._log(f'Getting field data: {field_id}')

        columns = []
        values = []

        def _load_data_handler(type, data):
            if type == 'columns':
                columns.extend(data)
            elif type == 'values':
                values.extend(data)

        # make requests to load granular_storage
        self.iter_data(field_id, _load_data_handler, query=query)

        return pd.DataFrame(values, columns=columns)

    def download_data(self, field_id, fn, query=None):
        self._log(f'Downloading field {field_id} data to file {fn}')
        if os.path.exists(fn):
            raise Exception(f'File {fn} already exists')

        writer = utils.PandasWriter(fn)

        def _save_handler(type, data):
            if type == 'columns':
                writer.write_header(data)
            elif type == 'values':
                writer.write_values(data)
        # make requests to save granular_storage
        self.iter_data(field_id, _save_handler, query=query)
        writer.flush()


Client = ClientV0