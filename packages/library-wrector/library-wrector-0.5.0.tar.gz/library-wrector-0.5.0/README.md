# library.wrector

![gif](https://media.giphy.com/media/YOqbsB7Ega18s/giphy.gif)

Original implementation: https://github.com/grammarly/gector

Tested (and works only :sob:) with python 3.7

```python
from library_wrector import Wrector
import spacy

nlp = spacy.load("en_core_web_sm")
wrector = Wrector(nlp, model_paths=["library_wrector/model/bert_0_gector.th"])

wrector("Does you like cats?")
'Do you like cats ?'
```