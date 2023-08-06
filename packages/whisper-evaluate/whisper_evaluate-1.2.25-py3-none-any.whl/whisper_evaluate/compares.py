"""Compare files
"""
import pandas as pd
import json
from whisper_evaluate.config import id2label, id2level
from whisper_evaluate.utils import _get_result_type


def compare_yidun_whisper_results(result_file: str, target_file: str, columns=["example", "yidun_json", "whisper_json"]):
    df = pd.read_csv(result_file)
    df.columns = columns
    df["yidun_predict"], df["yidun_type"], df["yidun_hints"] = zip(*df["yidun_json"].apply(parse_yidun_json))
    (df["whisper_predict"],
     df["whisper_type"],
     df["whisper_predict_trie"],
     df["whisper_type_trie"],
     df["whisper_match_words"],
     df["whisper_new_words"],
     df["whisper_review_words"]) = zip(*df["whisper_json"].apply(parse_whisper_json))
    df = df.drop(columns=["yidun_json", "whisper_json"])
    df.to_csv(target_file, index=False)


def parse_yidun_json(yidun_json: str, standard_json=True):
    if not standard_json:
        yidun_json = yidun_json.replace("'", '"')
    x = yidun_json.replace("\0", "")
    data = json.loads(x)
    data = data["result"]
    _type = id2label[data['labels'][0]['label']] if data['labels'] else '健康'
    _hint = " ".join(data['labels'][0]['details']['hint'] if data['labels'] else [])
    predict_label = id2level[data['labels'][0]['level']] if data['labels'] else 'Pass'

    return predict_label, _type, _hint


def parse_whisper_json(whisper_json: str, standard_json=True):
    if not standard_json:
        whisper_json = whisper_json.replace("'", '"')
    a = json.loads(whisper_json)
    results = a['results'][0]
    _match_words = results['matched_words']
    _new_words = results['new_words']
    _review_words = results['review_words']
    predict_type = _get_result_type(_match_words + _new_words)
    predict_label = "Pass" if predict_type == "健康" else "Reject"
    predict_type_trie = "政治" if _get_result_type(_review_words) == "政治" else predict_type
    predict_label_trie = "Pass" if predict_type_trie == "健康" else "Reject"
    return (predict_label,
            predict_type,
            predict_label_trie,
            predict_type_trie,
            " ".join([x["word"] for x in _match_words]),
            " ".join([x["word"] for x in _new_words]),
            " ".join([x["word"] for x in _review_words]))
