# cancer-survival-patterns
Exploring cancer survival patterns across stages and patient groups and identifying factors associated with survival.

## Run the app

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use the sidebar to open **Data Overview** for the overall dataset or
**Hormone & Demographics** for receptor counts, age comparisons, and receptor
proportions by race, marital status, and grade. The latter adapts Han's EDA
notebook and adds the grade comparison using the cleaned dataset.
