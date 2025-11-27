# Spelling-Correction-System

# Spelling Correction System

A Colab / notebook-based implementation of a noisy-channel spelling correction system that combines an **edit (channel) model** with several **language models** (uniform, Laplace unigram, Laplace bigram).
The system assumes **exactly one** single-word error per test sentence and selects the correction that maximizes:


where (P(x\mid w)) is the channel (edit) model and (P(w)) is the language model prior.

---

## Contents

* Notebook: `Spelling_Correction_System final.ipynb`
* Key code components:

  * `utils.py` (provides `LexicalEntry`, `Sentence`, `Corpus`, `SpellingResult`, `group_n_words`)
  * `ChannelModel` — reads `data/count_1edit.txt` and builds edit counts; generates candidate edits and probabilities
  * `UniformLanguageModel` — uniform prior over vocabulary (not shown inline but used in the notebook)
  * `LaplaceUnigramLanguageModel` — unigram with add-one smoothing
  * `LaplaceBigramLanguageModel` — bigram with add-one smoothing
  * `SpellCorrector` — ties channel + language model to produce corrected sentences
* Data files (expected paths used in the notebook):

  * `data/trainset.txt` — training corpus
  * `data/devset.txt` — dev/test corpus
  * `data/count_1edit.txt` — edit confusion counts for single edits

---

## Project goals

* Implement and evaluate a noisy-channel spelling corrector.
* Explore how different language models (uniform, Laplace unigram, Laplace bigram) affect correction accuracy.
* Demonstrate candidate generation using 1-edit (Damerau-Levenshtein) operations and scoring using edit frequencies (confusion table).

---

## Quickstart (Google Colab)

This project was developed for Google Colab. The notebook mounts Google Drive and reads data from the repository stored there.

1. Open the notebook in Colab:

   ```
   https://colab.research.google.com/drive/1DCMlEbCkOabypvYqcQD_u12abhfobkeB
   ```
2. When the notebook asks, mount your Google Drive and ensure the folder
   `/MyDrive/4.2D - Spelling Correction System/data/` exists and contains:

   * `trainset.txt`
   * `devset.txt`
   * `count_1edit.txt`
3. Run the cells sequentially. The notebook installs `pyxdameraulevenshtein` and appends the project path so `utils` can be imported.

---

## Quickstart (Local)

1. Clone / copy the notebook and data into a local folder.
2. Create & activate a Python environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate       # Windows (PowerShell)
   pip install --upgrade pip
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Or, manually:

   ```bash
   pip install pyxdameraulevenshtein jupyter
   ```
4. Start Jupyter and open the notebook:

   ```bash
   jupyter lab   # or jupyter notebook
   ```
5. Update any file paths in the notebook (they default to Colab Drive locations) to local `./data/...`.

---

## Example usage (what the notebook runs)

* Train language models on `trainset.txt`.
* Build channel model using `count_1edit.txt`.
* For each sentence in the dev set (each with exactly one error), the `SpellCorrector`:

  * Generates candidate corrections (1-edit candidates in vocabulary)
  * Scores sentence variants using `log P(w)` (LM score) + `log P(x|w)` (edit prob)
  * Picks the candidate with highest combined score
* Evaluation reports `SpellingResult` showing correct / total and accuracy.

Sample internal tests in the notebook include assertions such as:

* `laplaceUnigramLM.score(['I','am','Australian']) == -25.14565287682459`
* `laplaceBigramLM.score(['I','am','Australian']) ≈ -14.847658917530413`
* `laplaceBigramSpell.get_likely_correct_sentence(['I','lov','Australia']) == ['I','love','Australia']`

Reported dev accuracies in the notebook (examples):

* Laplace Unigram: `0.11040339702760085`
* Laplace Bigram: (printed; assertion commented out in provided copy)

---

## Dependencies (suggested)

Create `requirements.txt` with (example):

```
pyxdameraulevenshtein
jupyter
numpy
pandas
```

> The notebook also imports standard libraries (collections, math, sys) and depends on `utils.py` in the project path.

---

## Implementation notes & important details

* **ChannelModel**

  * Uses `data/count_1edit.txt` which contains tab-separated edit counts like `da|d\t13`.
  * Generates deletion / insertion / replacement / transposition candidates that are present in the vocabulary and looks up observed frequencies to compute edit probabilities.
  * Adds a strong self-count (the implementation sets a high self-count so the original word often dominates).
  * Includes a basic Damerau-Levenshtein edit distance implementation for tests/validations.
* **Language models**

  * `UniformLanguageModel` (uniform probability over vocabulary)
  * `LaplaceUnigramLanguageModel`: add-one smoothing over vocabulary
  * `LaplaceBigramLanguageModel`: bigram conditional with add-one smoothing using counts collected from the train corpus
* **SpellCorrector**

  * Assumes exactly one spelling error per sentence.
  * For each word, computes candidate edits and evaluates combined score = `LM_score(candidate_sentence) + log(edit_prob)` to pick the best correction.
  * Falls back to the original sentence if no candidate has a higher score.

---

## Troubleshooting & tips

* **Paths**: Update the hard-coded Colab `'/content/drive/MyDrive/...'` paths to your local dataset paths if running locally.
* **Large vocabulary**: Channel candidate generation loops over alphabet positions and letters — this can be expensive if vocabulary is large. Consider pruning or using a faster candidate generator (SymSpell).
* **Confusion table**: `count_1edit.txt` is essential for sensible `P(x|w)`. If missing, the channel model will have no edit counts and fall back to weak priors.
* **Multiple errors**: The system assumes exactly one error. It will not correctly handle sentences with multiple misspellings without modification (e.g., beam search or iterative corrections).
* **Floating point**: Unit tests in the notebook compare exact floats in some places; small numerical differences can break assertions. Use tolerances when adapting tests.

---

## Evaluation & extensions

Possible improvements and experiments:

* Replace hand-crafted channel model with learned confusion probabilities from a larger labeled error corpus.
* Use SymSpell or other optimized edit-table methods for speed.
* Replace language models with neural LMs (e.g., GPT-style) to improve context disambiguation.
* Extend to handle multiple errors with beam search or iterative correction.
* Improve candidate ranking by integrating word frequency priors, part-of-speech filtering or contextual embeddings.

---

## License & authorship

Add a `LICENSE` file for distribution and reuse. If you want a standard open license, consider MIT or Apache-2.0.

**Author / Contact:** (add your name / email here)

---

*README generated from the provided notebook. Edit the paths, dependencies and examples to match your environment and preferences.*
