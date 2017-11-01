# Beam Search
Beam search implementation with examples optimizing BLEU score of COCO image captions.

## Install
Clone this repo into a directory also containing the [MS COCO Caption Evaluation](https://github.com/tylin/coco-caption.git) repo.

## Examples
See the example and results by running `jupyter notebook coco-experiment.ipynb`

## Takeaways:
- Beam search initialized with the start-of-sentence token achieves a perfect BLEU score. (this also holds with 1 beam, i.e. greedy search)
- Considering words in the reference captions as actions instead of all words in the dictionary improves search speed by 1000 fold and produces identical results.

