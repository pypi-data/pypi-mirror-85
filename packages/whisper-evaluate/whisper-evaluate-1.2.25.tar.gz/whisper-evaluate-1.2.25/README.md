# whisper-evaluate

Evaluate the effectiveness of the Whisper model.

## Install
从pypi安装:
```shell script
pip install whisper-evaluate
```
从本地安装:
```shell script
git clone https://git.xindong.com/fengyanglu/whisper-evaluate.git
cd whisper-evaluate
pip install dist/whisper_evaluate-1.2.22-py3-none-any.whl
```
更新包
```shell script
pip install --upgrade whisper-evaluate
```

## How to use

可参考 [examples](./examples) , [test.py](./test.py)

### 请求模型结果
`WhisperQuery`
```python
from whisper_evaluate import WhisperQuery

wq = WhisperQuery(url="http://localhost:8901/v1/models/whisper:predict",
                  source_file="test_data/test-data-standard-latest.csv",
                  target_file="test_result.csv",
                  semaphore=500)
wq.run()
```

`NeteaseQuery`

为了不影响线上正常业务,请求网易结果时每秒请求数请控制在100以内.
```python
from whisper_evaluate import NeteaseQuery
nq = NeteaseQuery(source_file="test_data/test-data-standard-latest.csv",
                  target_file="test_result.csv")
nq.run()

# 上面的请求可能会有请求失败的数据
# 修正请求错误的数据
nq.fix_failed("test_result.csv")
```


### 计算模型指标
`Report`
```python
from whisper_evaluate import Report
import pprint
# 有三个参数: 
# task_name: 任务名称
# xd_other_type: 语心除了整体和政治,需要计算的分类指标, 传入一个list 如: ["色情", "辱骂"]
# wy_other_type: 网易除了整体和政治,需要计算的分类指标
rep = Report("testv1.1")

# 一步计算语心及网易的评估指标
rep = Report("testv1.1")
result = rep.report(xd_file="test_data/standard-whisper-result.csv",
                    wy_file="test_data/standard-yidun-result.csv")
pprint.pprint(result)
rep.save()  # 保存检查文件及评估结果


 # 单独计算语心结果
result = rep.whisper_report(xd_file="test_data/standard-whisper-result.csv")
pprint.pprint(result)
rep.save()  # 保存检查文件及评估结果


# 单独计算网易结果
result = rep.netease_report(wy_file="test_data/standard-yidun-result.csv")
pprint.pprint(result)
rep.save()  # 保存检查文件及评估结果

```


`WhisperStatistics`
```python
from whisper_evaluate import WhisperStatistics
import pprint

ws = WhisperStatistics(result_file="test_data/standard-whisper-result.csv")
xd_other_type = ["其他"]   # 其他需要计算的
ws.count_all(xd_other_type)
pprint.pprint(ws.indicator)
```

`NetEaseStatistics`
```python
from whisper_evaluate import NetEaseStatistics
import pprint

ns = NetEaseStatistics(result_file="test_data/standard-yidun-result.csv")

other_type = []
ns.count_all(other_type)

pprint.pprint(ns.indicator)
```

### 通用指标计算
```python
from whisper_evaluate import Statistics
import pandas as pd
file_name = "your file to count, contains label and predict columns"
df = pd.read_csv(file_name)
ss = Statistics()
label_name = "your label columns name"
predict_name = "your predict result columns name"
tp_label = "the true positive label"
accuracy = ss.accuracy(df, label_name=label_name, predict_name=predict_name)
recall = ss.recall(df, label_name=label_name, predict_name=predict_name, value=tp_label)
precision = ss.precision(df, label_name=label_name, predict_name=predict_name, value=tp_label)
f1 = ss.f1(precision=precision[0], recall=recall[0])
```

### 语境测试
`context_test_single`

`True` 表示通过,`False`表示未通过

```python
from whisper_evaluate import context_test_single

# 语境测试
label = ["给蛤蟆+1s", "蛤蟆", "[1,2]", "政治"]
predict = {'matched_words': [], 'review_words': [],
           'new_words': [{'word': '+1s', 'offset_start': 3, 'offset_end': 5, 'type': 'Politics'}]}
assert context_test_single(label, predict) is False
label = ["给蛤蟆+1s", "+1s", "[3,5]", "政治"]
predict = {'matched_words': [], 'review_words': [],
           'new_words': [{'word': '+1s', 'offset_start': 3, 'offset_end': 5, 'type': 'Politics'}]}
assert context_test_single(label, predict) is True
```

### 回归测试
`regression_test_single`

`True` 表示通过,`False`表示未通过

```python
from whisper_evaluate import regression_test_single
label = ["你们马后炮有一套的", "你们马", "[0,2]", "其他"]
predict = {'matched_words': [], 'review_words': [],
           'new_words': [{'word': '你们', 'offset_start': 0, 'offset_end': 1, 'type': 'Abuse'}]}
assert regression_test_single(label, predict) is False


label = ["习大大我爱你", "习大大", "[0,3]", "政治"]
predict = {'review_words': [], 'new_words': [],
           'matched_words': [{'word': '习大大', 'offset_start': 0, 'offset_end': 2, 'type': 'Politics'}]}
assert regression_test_single(label, predict) is True
```

### 新增网易结果与语心结果的对比功能
```python
from whisper_evaluate import compares
compares.compare_yidun_whisper_results("yidun_whisper_result.csv", "compare_result.csv")
```