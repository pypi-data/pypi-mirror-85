import pandas as pd


class Statistics(object):
    """Evaluation model indicators
    Accuracy/Precision/Recall/F1/PrecisionPolitics/RecallPolitics
    ...
    """

    def accuracy(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label") -> (
            float, str):
        """Count the accuracy of the df.
        (tp + tn) / (tp + fp + tn + fn)
        """
        a = df[df[label_name] == df[predict_name]].shape[0]
        b = df.shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def precision(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label",
                  value: str = "Reject") -> (float, str):
        """Count the precision of the df.
        tp / (tp + fp)
        """
        a = df[(df[label_name] == value) & (df[predict_name] == value)].shape[0]
        b = df[df[predict_name] == value].shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def recall(self, df: pd.DataFrame, label_name: str = "label", predict_name: str = "predict_label",
               value: str = "Reject") -> (float, str):
        """Count the precision of the df.
        tp / (tp + fn)
        """
        a = df[(df[label_name] == value) & (df[predict_name] == value)].shape[0]
        b = df[df[label_name] == value].shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"

    def f1(self, precision: float, recall: float) -> float:
        assert precision + recall > 0
        return 2 * precision * recall / (precision + recall)

    def reject_rate(self, df: pd.DataFrame, label_name: str = "type", predict_name: str = "predict_label",
                    value: str = "政治"):
        """Count a classification reject rate
        """
        a = df[(df[label_name] == value) & (df[predict_name] == "Reject")].shape[0]
        b = df[df[label_name] == value].shape[0]
        if b == 0: return (1, "缺少该类数据")
        return a / b, f"{a}/{b}"
