import os
import json
from concurrent.futures import ThreadPoolExecutor
import time
import dill
import numpy as np
import requests
from kyqlos.exceptions.client import DataAxisError, DataSizeError, FeatureSizeError
from kyqlos.exceptions.server import RegisterMonitoringError
from kyqlos.exceptions.server import RegisterDevDataError
from kyqlos.exceptions.server import RegisterProdDataError
from kyqlos.exceptions.server import CalculateMetricError
from kyqlos.exceptions.server import FetchMetrichTimeoutError
from kyqlos.exceptions.server import FetchMetrichError
from kyqlos.utils import args_type_check


class DataMonitorClient(object):
    """
    | このクラスはKyqlosサーバーにリクエストを送信するためのAPIを提供する。
    | APIの利用はKyqlos GUI Clientでアカウント登録済であることを前提とする。
    | アカウント登録後に発行されるcredentialsファイルを指定してアカウント認証を行う。
    |
    | 各メソッドの引数"thread"は、Trueが指定されるとスレッドによる非同期処理を行い、
    | 戻り値としてfuture（concurrent.futures.Future object）を返す。
    | future.result()によりメインプロセスと同期、実行結果の取得が行われる。

    Args:
        credentials(str): credentialsファイルのパス。\
            credentialsファイルとはKyqlosサーバーのアカウント認証に必要な情報が記載されたjson形式ファイル。\
            アカウント登録後に発行される。
    """

    def __init__(self, credentials):
        self._verify_credentials(credentials)
        self.registered = False
        self.base_url = f"{self.host}/api-proxy/api/{self.api_version}/data-monitoring"
        self.registration_url = self.base_url+"/monitor"
        self.dev_data_registration_url = self.registration_url+"/{}/dev-data"
        self.prod_data_registration_url = self.registration_url+"/{}/prod-data"
        self.calculate_url = self.prod_data_registration_url+"/{}/calculate-metric"
        self.dev_data_id = None
        self.prod_data_ids = []
        self.metric_id_map = {}
        self.thread = ThreadPoolExecutor(max_workers=1)
        self.MAX_FEATURE_SIZE = np.prod((3, 300, 300))

    def _verify_credentials(self, credential_path):
        with open(credential_path, "r") as json_file:
            credentials = json.load(json_file)
        self.host = credentials["host"]
        self.api_version = credentials["api_version"]
        self.token = credentials["credential"]

    def _register_data_monitoring(self, data_shape):
        data_shape = [int(i) for i in data_shape]
        response = requests.post(
            self.registration_url,
            headers={
                "token": self.token
            },
            data={
                "data_shape": json.dumps(data_shape)
            }
        )
        if response.status_code == requests.codes.ok:
            data_monitoring_id = json.loads(response.content)[
                "data_monitoring_id"]
        else:
            raise RegisterMonitoringError(response)
        return data_monitoring_id

    def _register_development_data(self, data_monitoring_id, data):
        data_byte_str = dill.dumps(data)
        response = requests.post(
            self.dev_data_registration_url.format(data_monitoring_id),
            headers={
                "token": self.token
            },
            files={
                "data": data_byte_str
            }
        )
        if response.status_code == requests.codes.ok:
            self.dev_data_id = json.loads(response.content)["dev_data_id"]
        else:
            raise RegisterDevDataError(response)

    def _calculate_metric(self, data_monitoring_id, metric_name):
        response = requests.post(
            self.calculate_url.format(data_monitoring_id, self.prod_data_ids[-1]),
            headers={
                "token": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id
            },
            data={
                "prod_data_id": self.prod_data_ids[-1],
                "metric_name": metric_name
            }
        )
        if response.status_code == requests.codes.ok:
            response = json.loads(response.content)
            metric_calculation_id = response["metric_calculation_id"]
            self.metric_id_map[metric_calculation_id] = self.prod_data_ids[-1]
            return metric_calculation_id
        else:
            raise CalculateMetricError(response)

    def _register_production_data(self, data_monitoring_id, data, latency, metric_name):
        data_byte_str = dill.dumps(data)
        response = requests.post(
            self.prod_data_registration_url.format(data_monitoring_id),
            headers={
                "token": self.token
            },
            files={
                "data": data_byte_str
            },
            data={
                "latency": latency
            }
        )
        if response.status_code == requests.codes.ok:
            self.prod_data_ids.append(json.loads(
                response.content)["prod_data_id"])
        else:
            raise RegisterProdDataError(response)
        return self._calculate_metric(data_monitoring_id, metric_name)

    def _retrieve_metric(self, data_monitoring_id, metric_calculation_id):
        response = requests.get(
            os.path.join(
                self.calculate_url.format(
                    data_monitoring_id,
                    self.metric_id_map[metric_calculation_id]
                ),
                metric_calculation_id
            ),
            headers={
                "token": self.token
            },
            params={
                "data_monitoring_id": data_monitoring_id,
                "metric_calculation_id": metric_calculation_id
            }
        )
        if response.status_code == requests.codes.ok:
            response = json.loads(response.content)
            return response
        else:
            raise FetchMetrichError(response)

    def _fetch_metric(self, data_monitoring_id, metric_calculation_id, timeout):
        job_status = None
        start_time = time.time()
        while job_status != "finished":
            response = self._retrieve_metric(
                data_monitoring_id, metric_calculation_id)
            job_status = response["job_status"]
            if job_status == "finished":
                break
            if job_status == "failed":
                raise FetchMetrichError(response)
            if time.time() - start_time > timeout:
                raise FetchMetrichTimeoutError()
            time.sleep(2)
        return response["result"]

    def _select_process(self, thread, func, *args):
        if thread:
            future = self.thread.submit(
                func, *args)
            return future
        else:
            result = func(*args)
            return result

    def _check_axis_num(self, shape, th):
        if len(shape) < th:
            raise DataAxisError(shape)

    def _check_data_size(self, data_size, th):
        if data_size > th:
            raise DataSizeError(data_size, th)

    def _check_feature_size(self, shape):
        feature_size = np.prod(shape[1:])
        if feature_size > self.MAX_FEATURE_SIZE:
            raise FeatureSizeError(feature_size, self.MAX_FEATURE_SIZE)

    @ args_type_check
    def register_data_monitoring(self, data_shape: tuple, thread: bool = False):
        """
        新規データ監視の登録、データモニタリングID発行のリクエストを送信

        Args:
            data_shape(tuple): 登録する学習データのshape
            thread(bool): スレッドによる非同期処理
        Returns:
            データモニタリングID
        """
        self._check_axis_num(data_shape, th=2)
        self._check_data_size(data_shape[0], th=1)
        self._check_feature_size(data_shape)
        return self._select_process(thread, self._register_data_monitoring, data_shape)

    @ args_type_check
    def register_development_data(self, data_monitoring_id: str, data: np.ndarray, thread: bool = False):
        """
        学習データ登録リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            data(numpy.ndarray): 学習データ時のデータ
            thread(bool): スレッドによる非同期処理
        """
        self._check_axis_num(data.shape, th=2)
        self._check_feature_size(data.shape)
        return self._select_process(thread, self._register_development_data, data_monitoring_id, data)

    @ args_type_check
    def register_production_data(
            self, data_monitoring_id: str, data: np.ndarray,
            latency: float = 0.0, metric_name: str = 'distance', thread: bool = False):
        """
        運用データ登録リクエスト、データ変化メトリックの計算リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            data(numpy.ndarray): 運用データ時のデータ
            latency(float): モデル推論時のレイテンシ
            metric_name(str): データ変化メトリックの種類
            thread(bool): スレッドによる非同期処理
        Returns:
            メトリック計算ID
        """
        self._check_axis_num(data.shape, th=2)
        self._check_data_size(data.shape[0], th=1)
        self._check_feature_size(data.shape)
        return self._select_process(
            thread, self._register_production_data, data_monitoring_id, data, latency, metric_name)

    @ args_type_check
    def fetch_metric(
            self, data_monitoring_id: str, metric_calculation_id: str, timeout: int = 180, thread: bool = False):
        """
        データ変化メトリックの計算結果取得リクエストを送信

        Args:
            data_monitoring_id(str): データモニタリングID
            metric_calculation_id(str): メトリック計算ID
            timeout(bool): タイムアウト発生時間。\
                指定時間までサーバーから取得ができない場合はFetchMetrichTimeoutErrorの例外を発生する。
            thread(bool): スレッドによる非同期処理
        Returns:
            データ変化メトリックの計算結果
        """
        return self._select_process(thread, self._fetch_metric, data_monitoring_id, metric_calculation_id, timeout)
