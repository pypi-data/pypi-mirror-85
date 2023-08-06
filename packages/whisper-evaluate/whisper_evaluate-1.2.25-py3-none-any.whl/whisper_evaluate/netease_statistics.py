from whisper_evaluate import Statistics
from whisper_evaluate.config import id2level, id2label
import pandas as pd
import numpy as np
import json
from pandarallel import pandarallel


class NetEaseStatistics(Statistics):
    level = id2level

    level_review_as_pass = {
        0: 'Pass',
        1: 'Pass',
        2: 'Reject'
    }

    level_review_as_reject = {
        0: 'Pass',
        1: 'Reject',
        2: 'Reject'
    }

    id2label = id2label

    def __init__(self, standard_file: str = None, result_file: str = None):
        assert result_file is not None
        pandarallel.initialize()
        self.df, self.df_review2pass, self.df_review2reject = None, None, None
        if standard_file is None:
            self.parse_standard_and_result(result_file)
        else:
            self.parse_standard_and_result_old(standard_file, result_file)
        self.indicator = {
            "review2pass": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
                "reject_rate": {}
            },
            "review2reject": {
                "accuracy": tuple(),
                "recall": {},
                "precision": {},
                "f1": {},
                "reject_rate": {}
            }
        }

    def count_accuracy(self):
        self.indicator["review2pass"]["accuracy"] = self.accuracy(self.df_review2pass, "label", "predict_label")
        self.indicator["review2reject"]["accuracy"] = self.accuracy(self.df_review2reject, "label", "predict_label")

    def count_recall(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["review2pass"]["recall"]["整体"] = self.recall(self.df_review2pass)
            self.indicator["review2reject"]["recall"]["整体"] = self.recall(self.df_review2reject)
        else:
            self.indicator["review2pass"]["recall"][mode] = self.recall(self.df_review2pass, "type", "predict_type",
                                                                        mode)
            self.indicator["review2reject"]["recall"][mode] = self.recall(self.df_review2reject, "type",
                                                                          "predict_type", mode)

    def count_precision(self, mode: str = "整体"):
        if mode == "整体":
            self.indicator["review2pass"]["precision"]["整体"] = self.precision(self.df_review2pass, "label",
                                                                              "predict_label")
            self.indicator["review2reject"]["precision"]["整体"] = self.precision(self.df_review2reject, "label",
                                                                                "predict_label")
        else:
            self.indicator["review2pass"]["precision"][mode] = self.precision(self.df_review2pass, "type",
                                                                              "predict_type",
                                                                              mode)
            self.indicator["review2reject"]["precision"][mode] = self.precision(self.df_review2reject, "type",
                                                                                "predict_type", mode)

    def count_reject_rate(self, mode: str = "政治"):
        self.indicator["review2pass"]["reject_rate"][mode] = self.reject_rate(self.df_review2pass, "type",
                                                                              "predict_label", mode)
        self.indicator["review2reject"]["reject_rate"][mode] = self.reject_rate(self.df_review2reject, "type",
                                                                                "predict_label", mode)

    def __count_f1(self):
        for category in self.indicator["review2pass"]["precision"]:
            self.indicator["review2pass"]["f1"][category] = self.f1(
                self.indicator["review2pass"]["precision"][category][0],
                self.indicator["review2pass"]["recall"][category][0])
            self.indicator["review2reject"]["f1"][category] = self.f1(
                self.indicator["review2reject"]["precision"][category][0],
                self.indicator["review2reject"]["recall"][category][0])

    def count_all(self, other_type: list = []):
        self.count_accuracy()
        for _type in ["整体", "政治"] + other_type:
            self.count_recall(_type)
            self.count_precision(_type)
            if _type != "整体":
                self.count_reject_rate(_type)
        self.__count_f1()

    def parse_standard_and_result(self, standard_result_file: str = None):
        standard_df = pd.read_csv(standard_result_file)
        standard_df.columns = ["example", "label", "type", "result_json"]
        (standard_df["predict_label_review2pass"],
         standard_df["predict_label_review2reject"],
         standard_df["predict_type"],
         standard_df["hints"]) = zip(*standard_df["result_json"].apply(self.parse_result_json))
        standard_df = standard_df.drop(columns=["result_json"])

        self.df = standard_df
        self.df_review2pass = standard_df[["example", "label", "type", "predict_label_review2pass", "predict_type"]]
        self.df_review2reject = standard_df[["example", "label", "type", "predict_label_review2reject", "predict_type"]]

        self.df_review2pass.columns = ["example", "label", "type", "predict_label", "predict_type"]
        self.df_review2reject.columns = ["example", "label", "type", "predict_label", "predict_type"]

    def parse_result_json(self, x: str):
        # x = x.replace("\\x", "")
        a = json.loads(x)
        data = a["result"]
        _type = self.id2label[data['labels'][0]['label']] if data['labels'] else '健康'
        _hint = " ".join(data['labels'][0]['details']['hint'] if data['labels'] else [])
        predict_label_review2pass = self.level_review_as_pass[data['labels'][0]['level']] if data['labels'] else 'Pass'
        predict_label_review2reject = self.level_review_as_reject[data['labels'][0]['level']] if data[
            'labels'] else 'Pass'

        return predict_label_review2pass, predict_label_review2reject, _type, _hint

    def parse_standard_and_result_old(self, standard_file: str, result_file: str):

        standard_df = pd.read_csv(standard_file)
        standard_df.columns = ["example", "label", "type"]
        text2result = {}
        with open(result_file, 'r', encoding='utf-8') as f:
            for line in f:
                a = json.loads(line)
                text = a['text']
                data = a['details'][0]['data']
                _label = self.id2label[data['labels'][0]['label']] if data['labels'] else '健康'
                _level = self.level[data['labels'][0]['level']] if data['labels'] else 'Pass'
                _hint = data['labels'][0]['details']['hint'] if data['labels'] else []
                text2result[text] = [_level.strip(), _label.strip(), " ".join(_hint)]
        results = []
        for s in standard_df["example"].values:
            results.append(text2result[s])

        results = np.array(results)

        standard_df["predict_label_review2pass"] = pd.Series(results[:, 0]).apply(
            lambda x: "Pass" if x != "Reject" else x)
        standard_df["predict_type"] = pd.Series(results[:, 1])
        standard_df["predict_label_review2reject"] = pd.Series(results[:, 0]).apply(
            lambda x: "Reject" if x != "Pass" else x)
        standard_df["hints"] = pd.Series(results[:, 2])
        self.df = standard_df
        self.df_review2pass = standard_df[["example", "label", "type", "predict_label_review2pass", "predict_type"]]
        self.df_review2reject = standard_df[
            ["example", "label", "type", "predict_label_review2reject", "predict_type"]]
        self.df_review2pass.columns = ["example", "label", "type", "predict_label", "predict_type"]
        self.df_review2reject.columns = ["example", "label", "type", "predict_label", "predict_type"]
