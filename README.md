# cancer-survival-patterns

Exploring cancer survival patterns across stages and patient groups and identifying factors associated with survival.

## Week 5

Open `week5.ipynb` for the complete analysis of age, race, and marital status by estrogen receptor (ER), progesterone receptor (PR), and joint ER/PR status. It includes executed tables, nine charts, statistical tests, findings, limitations, and optional Streamlit export.

The notebook contains all analysis functions and reads `dataset/seer_breast_cancer_cleaned.csv` directly. Keep the dataset folder alongside the notebook. The original and cleaned CSV datasets are retained for future project work.

To rerun, use Python 3.9 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Select this environment as your notebook kernel and run the cells from top to bottom. Results are already saved for review without execution. To generate the standalone Streamlit app and separate analysis outputs later, set `EXPORT_FILES = True` in the notebook's final cell; instructions are included there.
