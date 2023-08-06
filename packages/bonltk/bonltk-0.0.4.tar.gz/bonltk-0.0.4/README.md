# Natural Language Toolkit for Boyig (BoNLTK)
> BoNLTK aims to provide out of the box support for various NLP tasks that an application developer might need for Boyig (TIbetan) language.


## Install

`pip install bonltk`

## How to use

Comming soon

## Todo:
 - Tokenizers:
    - [ ] Hugging face [tokenizers](https://github.com/huggingface/tokenizers/tree/master/bindings/python)
    - [x] [sentencepiece tokenizer](https://github.com/google/sentencepiece/tree/master/python)
    - [ ] Compare above tokenizers with [botok](https://github.com/esukhia/botok)
 - WordVectors:
    - [x] Word2Vec with [gensim](https://github.com/RaRe-Technologies/gensim)
    - [ ] Emlo
 - Language Models:
    - [ ] Huggingface [transformers](https://github.com/huggingface/transformers)
    - [ ] UMLFit Language model with [fastai](https://forums.fast.ai/t/language-model-zoo-gorilla/14623)

- Text Similarity:
    - [ ] Sentence similarity using UMLFit, like in [inltk](https://github.com/goru001/inltk/blob/e6baa7f03164e977da899548a5c6e42a2a60db77/inltk/inltk.py#L120)
    - [ ] Implement Text similarity techniques mention in [here]((https://medium.com/@adriensieg/text-similarities-da019229c894)
    - [ ] Compare all the text similarity algorithms

### Resrouce links:
- [UMLFit for sequence tagging](https://forums.fast.ai/t/ulmfit-for-sequence-tagging/20328)
- [Text Similarities : Estimate the degree of similarity between two texts](https://medium.com/@adriensieg/text-similarities-da019229c894)
