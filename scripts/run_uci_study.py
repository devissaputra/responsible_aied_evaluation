import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))

from responsible_aied_evaluation.core import (
    EvaluationRecord,brier_score,confusion_metrics,expected_calibration_error,
    fairness_report,group_calibration_report,predictions_at_threshold,
    threshold_sensitivity,
)

SEED=42
UCI_ID=697
CONTINUOUS={
    "Previous qualification (grade)","Admission grade","Age at enrollment",
    "Unemployment rate","Inflation rate","GDP"
}

def normalize_target(raw):
    s=pd.Series(raw).astype(str).str.strip()
    allowed={"Dropout","Enrolled","Graduate"}
    if not set(s.unique()).issubset(allowed):
        raise ValueError(f"unexpected target labels: {sorted(s.unique())}")
    return (s=="Dropout").astype(int)

def enrollment_feature_frame(X):
    forbidden=[c for c in X.columns if "Curricular units 1st sem" in c or "Curricular units 2nd sem" in c]
    protected=[c for c in ["Gender","Nacionality"] if c in X.columns]
    model=X.drop(columns=forbidden+protected).copy()
    return model,forbidden,protected

def build_model(X):
    numeric=[c for c in X.columns if c in CONTINUOUS]
    categorical=[c for c in X.columns if c not in numeric]
    pre=ColumnTransformer([
        ("continuous",StandardScaler(),numeric),
        ("categorical",OneHotEncoder(handle_unknown="ignore"),categorical),
    ])
    return Pipeline([
        ("preprocess",pre),
        ("model",LogisticRegression(max_iter=4000,random_state=SEED))
    ])

def main():
    ds=fetch_ucirepo(id=UCI_ID)
    X=ds.data.features.copy()
    target=ds.data.targets
    y=normalize_target(target.iloc[:,0])
    model_X,forbidden,protected=enrollment_feature_frame(X)

    indices=np.arange(len(X))
    train_idx,test_idx=train_test_split(indices,test_size=.20,random_state=SEED,stratify=y)
    model=build_model(model_X.iloc[train_idx])
    model.fit(model_X.iloc[train_idx],y.iloc[train_idx])
    probability=model.predict_proba(model_X.iloc[test_idx])[:,1]
    y_test=y.iloc[test_idx].to_numpy()

    if "Gender" not in X.columns:
        raise ValueError("Gender column required for the frozen group audit")
    groups=[f"gender_code_{v}" for v in X.iloc[test_idx]["Gender"].tolist()]
    records=[
        EvaluationRecord(str(i),float(p),int(outcome),group)
        for i,p,outcome,group in zip(test_idx,probability,y_test,groups)
    ]
    predictions=predictions_at_threshold(records,.5)
    result={
        "research_bundle":True,
        "dataset":{"name":"Predict Students' Dropout and Academic Success","uci_id":UCI_ID,
                   "doi":"10.24432/C5MC89","n":int(len(X))},
        "design":{"seed":SEED,"n_train":int(len(train_idx)),"n_test":int(len(test_idx)),
                  "target":"Dropout vs Enrolled/Graduate",
                  "forbidden_post_enrollment_columns":forbidden,
                  "protected_excluded_from_prediction":protected,
                  "n_model_features":int(model_X.shape[1])},
        "overall":{
            "roc_auc":float(roc_auc_score(y_test,probability)),
            "brier":float(brier_score(probability.tolist(),y_test.tolist())),
            "ece_10":float(expected_calibration_error(probability.tolist(),y_test.tolist(),bins=10)),
            "confusion":confusion_metrics(predictions,y_test.tolist()),
        },
        "gender_audit":fairness_report(records,threshold=.5,min_group_size=30),
        "gender_calibration":group_calibration_report(records,bins=5,min_group_size=30),
        "threshold_sensitivity":threshold_sensitivity(records,[.3,.4,.5,.6,.7],min_group_size=30),
        "interpretation_boundary":"measurement audit only; not fairness certification or deployment approval"
    }
    out=ROOT/"results"; out.mkdir(exist_ok=True)
    (out/"uci697_audit.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
