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

**Stage Survival** shows Kaplan-Meier survival curves, 5-year survival and log-rank tests by stage, T stage and N stage. 
**Factors Together** uses a Cox model to show how each factor (age, tumor size, lymph nodes, grade, hormone status and race) changes the risk of death when all factors are looked at together.
