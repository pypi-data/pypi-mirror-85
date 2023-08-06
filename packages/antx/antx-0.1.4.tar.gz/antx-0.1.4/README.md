# antx - Annotation Transfer
Transfer annotations from source text to destination using diff match patch.

![Test](https://github.com/Esukhia/annotation_transfer/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/antx.svg)](https://badge.fury.io/py/antx)

## Usage

### Install using pip.
```
$ pip install antx
```

### Import
```
from antx import transfer
```

### Transfer
```
new_target = transfer(source_text, annotations, target_text, output="txt", replaced=True)
```
**source_text** := contains source text

**annotations** := contains list of annotations in source text that you want to transfer to target text

**target_text** := contains target text

**output** := Flag to indicate type of output. It can be txt or yaml.

**replaced** := Boolean flag to choose whether you want to proceed cached diff result of given source, target and annotation. Recommended to set false during debugging so that you can used the freezed diff again and again.

**Example**

```python
source_text =  """༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
<𰵀auམཛད་པ་པོ། འཇམ་མགོན་ཀོང་སྤྲུལ་བློ་གྲོས་མཐའ་ཡས། །>
༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
""
```
```python
target_text =  """༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
མཛད་པ་པོ། འཇམ་མགོན་ཀོང་སྤྲུལ་བློ་གྲོས་མཐའ་ཡས། །
༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
༄༅། །གྲུབ་བརྒྱའི་སྤྱི་མེས་མར་མི་དྭགས་གསུམ་ནས། །དཔལ་ལྡན་དུས་གསུམ་མཁྱེན་པའི་བཀའ་བརྒྱུད་ནི།
"""
```
```python
annotations = [['author_start', r"(\<[𰵀-󴉱]?au)"], ['author_end', r"(\>)"]]
```
```python
result = transfer(src, annotations, trg, output="txt")

Annotation transfer started...
Mapping annotations to tofu-IDs
[INFO] Computing diffs ...
[INFO] Diff computed!
Transfering annotations...
```
```python
print(result)
༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
<𰵀auམཛད་པ་པོ། འཇམ་མགོན་ཀོང་སྤྲུལ་བློ་གྲོས་མཐའ་ཡས། །>
༄༅། །ཕྱག་ཆེན་སྔོན་འགྲོ་བཞི་སྦྱོར་དང་དངོས་གཞིའི་ཁྲིད་རིམ་མདོར་བསྡུས་ངེས་དོན་སྒྲོན་མེ་ཞེས་བྱ་བ་བཞུགས་སོ། །
༄༅། །གྲུབ་བརྒྱའི་སྤྱི་མེས་མར་མི་དྭགས་གསུམ་ནས། །དཔལ་ལྡན་དུས་གསུམ་མཁྱེན་པའི་བཀའ་བརྒྱུད་ནི།
```
