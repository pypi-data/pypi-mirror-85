from whisper_evaluate import Statistics
from whisper_evaluate.utils import _get_result_type
import pandas as pd
from pandarallel import pandarallel
from whisper_evaluate.config import en_zh
import json


class WhisperStatistics(Statistics):

    def __init__(self, standard_file: str = None, result_file: str = None):
        """Incoming files that the calculation depends on
        Args:
        standard_file: the standard test file. csv. contains 3 columns "example", "label", "type"
        result_file: the result of the standard test file query,
                    If you not input in standard file, it should contain result_json, like:
                    "example", "label", "type", "result_json"
                    "aaaaaaaa", "Pass", "健康",  "{...}"
        """
        assert result_file is not None
        pandarallel.initialize()
        self.df, self.df_no_trie, self.df_trie = None, None, None
        if standard_file is None:
            self.parse_standard_and_result(standard_file=result_file)
        else:
            self.parse_standard_and_result(standard_file=standard_file, result_file=result_file)
        self.indicator = {
            "no_trie": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
                "reject_rate": {}
            },
            "trie": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
                "reject_rate": {}
            }
        }

    def count_accuracy(self):
        self.indicator["no_trie"]["accuracy"] = self.accuracy(self.df_no_trie, "label", "predict_label")
        self.indicator["trie"]["accuracy"] = self.accuracy(self.df_trie, "label", "predict_label")

    def count_recall(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["no_trie"]["recall"]["整体"] = self.recall(self.df_no_trie)
            self.indicator["trie"]["recall"]["整体"] = self.recall(self.df_trie)
        else:
            self.indicator["no_trie"]["recall"][mode] = self.recall(self.df_no_trie, "type", "predict_type", mode)
            self.indicator["trie"]["recall"][mode] = self.recall(self.df_trie, "type", "predict_type", mode)

    def count_precision(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["no_trie"]["precision"]["整体"] = self.precision(self.df_no_trie, "label", "predict_label")
            self.indicator["trie"]["precision"]["整体"] = self.precision(self.df_trie, "label", "predict_label")
        else:
            self.indicator["no_trie"]["precision"][mode] = self.precision(self.df_no_trie, "type", "predict_type",
                                                                          mode)
            self.indicator["trie"]["precision"][mode] = self.precision(self.df_trie, "type", "predict_type", mode)

    def count_reject_rate(self, mode: str = "政治"):
        self.indicator["no_trie"]["reject_rate"][mode] = self.reject_rate(self.df_no_trie, "type", "predict_label",
                                                                          mode)
        self.indicator["trie"]["reject_rate"][mode] = self.reject_rate(self.df_trie, "type", "predict_label", mode)

    def parse_standard_and_result(self, standard_file: str, result_file: str = None):
        standard_df = pd.read_csv(standard_file)
        if result_file:
            standard_df.columns = ["example", "label", "type"]
            with open(result_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            standard_df["result_json"] = pd.Series(lines)
        else:
            standard_df.columns = ["example", "label", "type", "result_json"]
        (standard_df["predict_label"],
         standard_df["predict_type"],
         standard_df["predict_label_trie"],
         standard_df["predict_type_trie"],
         standard_df["match_words"],
         standard_df["new_words"],
         standard_df["review_words"]) = zip(*standard_df["result_json"].parallel_apply(self._parse_result_json))
        standard_df = standard_df.drop(columns=["result_json"])
        self.df = standard_df
        self.df_no_trie = standard_df[["example", "label", "type", "predict_label", "predict_type"]]
        self.df_trie = standard_df[["example", "label", "type", "predict_label_trie", "predict_type_trie"]]
        self.df_trie.columns = ["example", "label", "type", "predict_label", "predict_type"]

        # self.__parse_result_json(standard_df)

    def _parse_result_json(self, x: str):
        # x = x.replace("'", '"')
        a = json.loads(x)
        results = a['results'][0]
        _match_words = results['matched_words']
        _new_words = results['new_words']
        _review_words = results['review_words']
        predict_type = self._get_result_type(_match_words + _new_words)
        predict_label = "Pass" if predict_type == en_zh["Normal"] else "Reject"
        predict_type_trie = "政治" if self._get_result_type(_review_words) == "政治" else predict_type
        predict_label_trie = "Pass" if predict_type_trie == en_zh["Normal"] else "Reject"

        return (predict_label, predict_type, predict_label_trie, predict_type_trie,
                " ".join([x["word"] for x in _match_words]),
                " ".join([x["word"] for x in _new_words]),
                " ".join([x["word"] for x in _review_words]))

    def __count_f1(self):
        for category in self.indicator["no_trie"]["precision"]:
            self.indicator["no_trie"]["f1"][category] = self.f1(self.indicator["no_trie"]["precision"][category][0],
                                                                self.indicator["no_trie"]["recall"][category][0])
            self.indicator["trie"]["f1"][category] = self.f1(self.indicator["trie"]["precision"][category][0],
                                                             self.indicator["trie"]["recall"][category][0])

    def count_all(self, other_type: list = []):
        self.count_accuracy()
        for _type in ["整体", "政治"] + other_type:
            self.count_recall(_type)
            self.count_precision(_type)
            if _type != "整体":
                self.count_reject_rate(_type)
        self.__count_f1()

    def _get_result_type(self, words: list):
        return _get_result_type(words)
