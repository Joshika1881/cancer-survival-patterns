"""Shared analysis groups; preserve the original dataset columns."""
import pandas as pd

AGE_GROUPS = ["Under 50", "50–59", "60–69"]
GRADE_GROUPS = ["I", "II", "III–IV"]
STAGES = ["IIA", "IIB", "IIIA", "IIIB", "IIIC"]


def prepare_analysis_groups(data):
    df = data.copy()
    age = pd.to_numeric(df["Age"], errors="coerce")
    df["Age Group"] = pd.cut(age, [0, 50, 60, 70], right=False, labels=AGE_GROUPS)
    er, pr = df["Estrogen Status"], df["Progesterone Status"]
    hormone = pd.Series(pd.NA, index=df.index, dtype="string")
    hormone.loc[er.eq("Negative") & pr.eq("Negative")] = "Negative"
    hormone.loc[er.eq("Positive") | pr.eq("Positive")] = "Positive"
    df["Hormone Status"] = hormone
    df["Grade Group"] = pd.Categorical(df["Grade"].map({
        "Well differentiated; Grade I": "I",
        "Moderately differentiated; Grade II": "II",
        "Poorly differentiated; Grade III": "III–IV",
        "Undifferentiated; anaplastic; Grade IV": "III–IV",
    }), categories=GRADE_GROUPS, ordered=True)
    df["Stage"] = pd.Categorical(df["6th Stage"], categories=STAGES, ordered=True)
    df["Stage Group"] = df["6th Stage"].map({
        "IIA": "II", "IIB": "II", "IIIA": "III", "IIIB": "III", "IIIC": "III",
    })
    # Recorded vital status only; a fixed 5-year outcome needs follow-up rules.
    df["Death Event"] = df["Status"].map({"Dead": 1, "Alive": 0}).astype("Int64")
    months = pd.to_numeric(df["Survival Months"], errors="coerce")
    valid = months.ge(0) & df["Status"].isin(["Dead", "Alive"])
    outcome = pd.Series(pd.NA, index=df.index, dtype="Int64")
    outcome.loc[valid & months.ge(60)] = 0
    outcome.loc[valid & df["Status"].eq("Dead") & months.le(60)] = 1
    df["5-Year Death Outcome"] = outcome
    return df
