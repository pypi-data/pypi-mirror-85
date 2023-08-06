from whisper_evaluate import WhisperStatistics, NetEaseStatistics
from whisper_evaluate.utils import logging
import os
import time


class Report(object):

    def __init__(self, task_name: str = "new_test", xd_other_type: list = [], wy_other_type: list = []):
        self.task_name = task_name
        self.xd_other_type = xd_other_type
        self.wy_other_type = wy_other_type
        self._ws, self._ns = None, None
        self.task_dir = f"reports/{task_name}-{int(time.time())}"
        if not os.path.exists(self.task_dir):
            os.makedirs(self.task_dir)
            logging.info(f"Create task dir: {self.task_dir}")

    def report(self, stand_file: str = None, xd_file: str = None, wy_file: str = None) -> dict:
        """Get the evaluate report.
        :param stand_file: 标准测试数据 (当下方两个结果数据中不包含测试标签时,此参数必须传递)
        :param xd_file: whisper结果数据
        :param wy_file:  netease结果数据
        :return: a dict, 评估指标
        """
        logging.info("Just loading files...")
        if stand_file:
            ws = self._ws = WhisperStatistics(standard_file=stand_file, result_file=xd_file)
        else:
            ws = self._ws = WhisperStatistics(result_file=xd_file)
        ns = self._ns = NetEaseStatistics(stand_file, wy_file)
        start_time = time.time()
        ws.count_all(self.xd_other_type)
        logging.info(f"Whisper count successfully, cost {int(time.time() - start_time)} seconds.")
        start_time = time.time()
        ns.count_all(self.wy_other_type)
        logging.info(f"NetEase count successfully, cost {int(time.time() - start_time)} seconds.")
        return {"网易": ns.indicator, "语心": ws.indicator}

    def whisper_report(self, stand_file: str = None, xd_file: str = None) -> dict:
        logging.info("Just loading files...")
        if stand_file is None:
            ws = self._ws = WhisperStatistics(result_file=xd_file)
        else:
            ws = self._ws = WhisperStatistics(stand_file, xd_file)
        start_time = time.time()
        ws.count_all(self.xd_other_type)
        logging.info(f"Whisper count successfully, cost {int(time.time() - start_time)} seconds.")
        return ws.indicator

    def netease_report(self, stand_file: str = None, wy_file: str = None) -> dict:
        logging.info("Just loading files...")
        ns = self._ns = NetEaseStatistics(stand_file, wy_file)
        start_time = time.time()
        ns.count_all(self.wy_other_type)
        logging.info(f"NetEase count successfully, cost {int(time.time() - start_time)} seconds.")
        return ns.indicator

    def save(self):
        if self._ws:
            self._ws.df.to_csv(os.path.join(self.task_dir, "whisper-check-data.csv"), index=False)
        if self._ns:
            self._ns.df.to_csv(os.path.join(self.task_dir, "netease-check-data.csv"), index=False)

        report_str = self.__report_format()
        with open(os.path.join(self.task_dir, "eval-result.tsv"), "w", encoding='utf-8') as f:
            f.write(report_str)

    def __report_format(self) -> str:
        rows = ""
        rows += "\t".join(
            ["Serving", "accuracy", "precision", "recall", "f1", "precision-politics", "recall-politics"]) + "\n"
        if self._ws:
            rows += self.__row_format("Whisper纯模型", self._ws.indicator["no_trie"])
            rows += self.__row_format("Whisper综合模型", self._ws.indicator["trie"])
        if self._ns:
            rows += self.__row_format("网易review2pass", self._ns.indicator["review2pass"])
            rows += self.__row_format("网易review2reject", self._ns.indicator["review2reject"])

        return rows

    def __row_format(self, name: str, obj: dict) -> str:
        return "\t".join([name,
                          f'{round(obj["accuracy"][0], 4)} ({obj["accuracy"][1]})',
                          f'{round(obj["precision"]["整体"][0], 4)} ({obj["precision"]["整体"][1]})',
                          f'{round(obj["recall"]["整体"][0], 4)} ({obj["recall"]["整体"][1]})',
                          f'{round(obj["f1"]["整体"], 4)}',
                          f'{round(obj["precision"]["政治"][0], 4)} ({obj["precision"]["政治"][1]})',
                          f'{round(obj["recall"]["政治"][0], 4)} ({obj["recall"]["政治"][1]})',
                          f'{round(obj["f1"]["政治"], 4)}',
                          ]) + "\n"
