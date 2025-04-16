import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MinMaxScaler
import shap
import matplotlib.pyplot as plt

# 1. 데이터 불러오기
df = pd.read_csv("session_dataset.csv")  # 파일명에 맞게 조정 필요

# 2. 전처리
X = df.drop(columns=['label'])
y = df['label']

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 3. 모델 학습
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 4. 예측 및 성능 평가
y_pred = clf.predict(X_test)
print("✅ Classification Results:")
print("Accuracy:  ", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("Precision: ", round(precision_score(y_test, y_pred) * 100, 2), "%")
print("Recall:    ", round(recall_score(y_test, y_pred) * 100, 2), "%")
print("F1-score:  ", round(f1_score(y_test, y_pred) * 100, 2), "%")

# 5. SHAP 분석 (상위 1000개 샘플만)
print("\n✅ Running SHAP analysis on 1000 samples...")

# 1000개 샘플만 선택
X_sample = X_test[:1000]

explainer = shap.TreeExplainer(clf)
shap_values = explainer.shap_values(X_sample)

# SHAP 중요도 시각화 (Global)
shap.summary_plot(shap_values[1], X_sample, feature_names=X.columns, max_display=10, show=False)
plt.tight_layout()
plt.savefig("shap_summary_plot.png")
plt.show()




# CLI에서 force_plot 생략하거나 저장하는 방식으로 대체 가능

