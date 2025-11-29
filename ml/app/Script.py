import pandas as pd

df_patterns = pd.read_csv(
    'pattern.csv',
    header=1,
    skiprows=[2],
)

df_transactions = pd.read_csv(
    'transact.csv',
    header=1,
)

print("Поведенческие паттерны: первые 5 строк:")
print(df_patterns.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\nТранзакции: первые 5 строк:")
print(df_transactions.head().to_markdown(index=False, numalign="left", stralign="left"))
# ОЧИСТКА ДАТАСЕТОВ
def safe_strip(s):
    # удаление лишних пробелов, кавычек
    if isinstance(s, str):
        return s.strip().strip("'")
    return s

pattern_object_cols = df_patterns.select_dtypes(include=['object']).columns
for col in pattern_object_cols:
    df_patterns[col] = df_patterns[col].apply(safe_strip)

df_patterns['cst_dim_id'] = df_patterns['cst_dim_id'].astype(float).round(0).astype('Int64')
df_patterns['transdate'] = pd.to_datetime(df_patterns['transdate'], errors='coerce')
cols_to_float = [
    'login_frequency_30d',
    'freq_change_7d_vs_mean',
    'var_login_interval_30d'
]
for col in cols_to_float:
    df_patterns[col] = pd.to_numeric(df_patterns[col], errors='coerce')

transaction_object_cols = df_transactions.select_dtypes(include=['object']).columns
for col in transaction_object_cols:
    df_transactions[col] = df_transactions[col].apply(safe_strip)

df_transactions['cst_dim_id'] = df_transactions['cst_dim_id'].astype(float).round(0).astype('Int64')
df_transactions['transdate'] = pd.to_datetime(df_transactions['transdate'], errors='coerce')
df_transactions['transdatetime'] = pd.to_datetime(df_transactions['transdatetime'], errors='coerce')
duplicate_count = df_patterns.duplicated(subset=['cst_dim_id', 'transdate']).sum()
print(duplicate_count)
df_patterns_unique = df_patterns.drop_duplicates(subset=['cst_dim_id', 'transdate'], keep='first')
duplicate_count = df_patterns_unique.duplicated(subset=['cst_dim_id', 'transdate']).sum()
print(duplicate_count)
df_merged = df_transactions.merge(df_patterns_unique, on=['cst_dim_id', 'transdate'], how='left')
missing_patterns = df_merged['monthly_os_changes'].isna().sum()
print(missing_patterns)
print(df_merged.head().to_markdown(index=False, numalign="left", stralign="left"))
# анализ таргет
target_counts = df_merged['target'].value_counts()
target_percentage = df_merged['target'].value_counts(normalize=True) * 100

df_target_summary = pd.DataFrame({
    'target': target_counts.index,
    'count': target_counts.values,
    'proportion': target_percentage.values
})

print(df_target_summary.to_markdown(
    index=False,
    numalign="left",
    stralign="left",
    floatfmt=[".0f", ".0f", ".2f"], # два знака после запятой для proportion
    headers=["target", "count", "proportion (%)"]
))
missing_features_mask = df_merged['monthly_os_changes'].isna()

missing_target_distribution = df_merged[missing_features_mask]['target'].value_counts()
total_fraud = df_merged['target'].sum()

print(missing_target_distribution.to_markdown(numalign="left", stralign="left"))
print(f"\nОбщее количество мошеннических транзакций в датасете: {total_fraud}")
import numpy as np

df_merged.rename(columns={
    'cst_dim_id': 'user_id',
    'transdatetime': 'timestamp',
    'direction': 'merchant_id',
    'target': 'is_fraud'
}, inplace=True)

# заполняем user_id специальным ID для NaN, чтобы сохранить строки
df_merged['user_id'] = df_merged['user_id'].fillna(-9999).astype(int)

numeric_cols_to_impute = df_merged.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols_to_impute.remove('amount')
numeric_cols_to_impute.remove('is_fraud')

df_merged[numeric_cols_to_impute] = df_merged[numeric_cols_to_impute].fillna(0)

categorical_cols_to_impute = ['last_phone_model_categorical', 'last_os_categorical']
df_merged[categorical_cols_to_impute] = df_merged[categorical_cols_to_impute].fillna('Unknown')

df_merged['hour'] = df_merged['timestamp'].dt.hour
df_merged['day_of_week'] = df_merged['timestamp'].dt.dayofweek # 0=Понедельник, 6=Воскресенье
df_merged['is_weekend'] = (df_merged['day_of_week'] >= 5).astype(int)

# признаки ночного времени (с 22:00 до 6:00)
df_merged['is_night_time'] = ((df_merged['hour'] >= 22) | (df_merged['hour'] <= 6)).astype(int)

# 3. преобразование часа в синус/косинус, чтобы модель понимала, что 23:59 и 00:01 близки)
df_merged['hour_sin'] = np.sin(2 * np.pi * df_merged['hour'] / 24)
df_merged['hour_cos'] = np.cos(2 * np.pi * df_merged['hour'] / 24)

print(df_merged[['timestamp', 'hour', 'is_night_time', 'hour_sin']].head().to_markdown(index=False, numalign="left", stralign="left"))

# сортировка данных по клиенту и времени
df_merged.sort_values(by=['user_id', 'timestamp'], inplace=True)

# время с момента предыдущей транзакции (в секундах)
# разница рассчитывается внутри каждой группы user_id
df_merged['time_diff_prev'] = df_merged.groupby('user_id')['timestamp'].diff().dt.total_seconds()

# первая транзакция клиента
df_merged['time_diff_prev'].fillna(99999999, inplace=True)

# признак: транзакция произошла слишком быстро, например, менее 5 минут (300 секунд) с предыдущей транзакции
df_merged['is_rapid_fire'] = (df_merged['time_diff_prev'] < 300).astype(int)

# количество транзакций за 1 и 7 дней
for window in ['1D', '7D']:
    df_merged_indexed = df_merged.set_index('timestamp')

    df_merged[f'tx_count_{window}'] = (
        df_merged_indexed.groupby('user_id')['docno']
        .rolling(window)
        .count()
        .reset_index(level=0, drop=True)
        .values
    )

    df_merged[f'tx_count_{window}'] = df_merged[f'tx_count_{window}'] - 1
    df_merged[f'tx_count_{window}'] = df_merged[f'tx_count_{window}'].fillna(0)


print(df_merged[['user_id', 'timestamp', 'time_diff_prev', 'is_rapid_fire', 'tx_count_1D', 'tx_count_7D']].head().to_markdown(index=False, numalign="left", stralign="left", floatfmt=".0f"))

# расчет агрегированной статистики по клиенту
user_amount_stats = df_merged.groupby('user_id')['amount'].agg(['mean', 'std', 'median']).reset_index()
user_amount_stats.columns = ['user_id', 'user_avg_amount', 'user_std_amount', 'user_median_amount']

df_merged = df_merged.merge(user_amount_stats, on='user_id', how='left')

# Z-Score (насколько текущая сумма отличается от среднего, в единицах стандартного отклонения)
df_merged['amount_zscore'] = (
    df_merged['amount'] - df_merged['user_avg_amount']
) / (df_merged['user_std_amount'] + 1e-8)

df_merged['is_amount_outlier'] = (np.abs(df_merged['amount_zscore']) > 3).astype(int)

print(df_merged[['user_id', 'amount', 'user_avg_amount', 'amount_zscore', 'is_amount_outlier']].head().to_markdown(index=False, numalign="left", stralign="left", floatfmt=".2f"))

# Merchant Degree
# сколько уникальных пользователей взаимодействовали с каждым получателем (merchant_id).
merchant_user_count = df_merged.groupby('merchant_id')['user_id'].nunique().reset_index()
merchant_user_count.rename(columns={'user_id': 'merchant_user_degree'}, inplace=True)
df_merged = df_merged.merge(merchant_user_count, on='merchant_id', how='left')

# частота встречаемости получателя
merchant_freq = df_merged['merchant_id'].value_counts(normalize=True).reset_index()
merchant_freq.columns = ['merchant_id', 'merchant_frequency']
df_merged = df_merged.merge(merchant_freq, on='merchant_id', how='left')

# создаем признак, который показывает, является ли текущая транзакция первой транзакцией с этим получателем
df_merged['user_merchant_pair'] = df_merged['user_id'].astype(str) + '_' + df_merged['merchant_id']
df_merged['user_merchant_tx_seq'] = df_merged.groupby('user_merchant_pair').cumcount() + 1
df_merged['is_new_merchant_pair'] = (df_merged['user_merchant_tx_seq'] == 1).astype(int)

df_merged.drop(columns=['user_merchant_pair', 'user_merchant_tx_seq'], inplace=True)

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif, SelectKBest
from sklearn.preprocessing import StandardScaler
import json

X = df_merged.select_dtypes(include=[np.number])
y = df_merged['is_fraud']

X = X.drop(columns=['is_fraud', 'user_id', 'docno'], errors='ignore')
X = X.fillna(0)

# Random Forest Feature Importance
def get_rf_importances(X, y, n_features_to_keep=None):
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced')
    rf.fit(X, y)
    importances = pd.Series(rf.feature_importances_, index=X.columns)
    importances = importances / importances.max()

    return importances.sort_values(ascending=False)

# Mutual Information Feature Importance
def get_mi_importances(X, y, n_features_to_keep=None):
    mi_scores = mutual_info_classif(X, y, random_state=42)
    importances = pd.Series(mi_scores, index=X.columns)
    importances = importances / importances.max()

    return importances.sort_values(ascending=False)

# Оценка независимости признаков (1 - Max_Correlation)
def get_corr_independence_score(X):
    corr_matrix = X.corr().abs()
    independence_scores = {}

    for column in X.columns:
        max_corr = corr_matrix[column].drop(column, errors='ignore').abs().max()
        independence_scores[column] = 1.0 - max_corr

    importances = pd.Series(independence_scores)
    return importances.sort_values(ascending=False)


rf_scores = get_rf_importances(X, y)
mi_scores = get_mi_importances(X, y)
corr_scores = get_corr_independence_score(X)

combined_scores = pd.concat([
    rf_scores.rename('RF_Importance'),
    mi_scores.rename('MI_Importance'),
    corr_scores.rename('Corr_Independence')
], axis=1).fillna(0)

combined_scores['Combined_Score'] = combined_scores.sum(axis=1)

N_TOP_DISPLAY = 20
df_importance_analysis = combined_scores.sort_values('Combined_Score', ascending=False)

print(df_importance_analysis.head(N_TOP_DISPLAY).to_markdown(floatfmt=".4f"))

print(f"\nОбщее количество признаков в анализе: {len(df_importance_analysis)}")

# анализ корреляции
corr_matrix = X.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
highly_correlated_pairs = []
CORR_THRESHOLD = 0.9

for i, col1 in enumerate(upper.columns):
    for col2 in upper.index[i+1:]:
        if upper.loc[col1, col2] >= CORR_THRESHOLD:
            highly_correlated_pairs.append({
                'Feature_1': col1,
                'Feature_2': col2,
                'Correlation': upper.loc[col1, col2]
            })

df_corr_pairs = pd.DataFrame(highly_correlated_pairs)

if not df_corr_pairs.empty:
    print(df_corr_pairs.sort_values('Correlation', ascending=False).to_markdown(index=False, floatfmt=".4f"))

redundant_numerical_features = [
    'login_frequency_7d',
    'freq_change_7d_vs_mean'
]

# удаление избыточных признаков
df_merged_final = df_merged.drop(
    columns=redundant_numerical_features,
    errors='ignore'
).copy()

final_numerical_features = (
    df_merged_final.select_dtypes(include=[np.number]).columns.tolist()
)

features_to_remove = ['is_fraud', 'user_id', 'docno']
for col in features_to_remove:
    if col in final_numerical_features:
        final_numerical_features.remove(col)

final_categorical_features = df_merged_final.select_dtypes(include=['object']).columns.tolist()

final_model_features = final_numerical_features + final_categorical_features

print("числовые признаки")
print(final_numerical_features)
print("\nкатегориальные признаки")
print(final_categorical_features)

print(f"\nобщее количество признаков: {len(final_model_features)}")

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from xgboost import XGBClassifier
from category_encoders import HashingEncoder
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score
import pprint

df_model_ready = df_merged_final.copy()

Y = df_model_ready['is_fraud']
X = df_model_ready.drop(
    columns=['is_fraud', 'user_id', 'docno', 'transdate', 'timestamp'],
    errors='ignore'
)

X = X.fillna(0)

cat_cols = final_categorical_features

X_train_raw, X_holdout_raw, y_train, y_holdout = train_test_split(
    X, Y,
    test_size=0.2,
    stratify=Y,
    random_state=42
)

encoder = HashingEncoder(cols=cat_cols, n_components=8)

X_train = encoder.fit_transform(X_train_raw)
X_holdout = encoder.transform(X_holdout_raw)

neg = (y_train == 0).sum()
pos = (y_train == 1).sum()
scale_pos_weight_value = neg / pos
random_state = 42

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.03, 0.05, 0.1],
    'gamma': [0, 0.5, 1],
    'subsample': [0.7, 0.9],
    'n_estimators': [100, 150]
}

xgb_model = XGBClassifier(
    scale_pos_weight=scale_pos_weight_value,
    random_state=random_state,
    tree_method="hist",
    eval_metric='aucpr'
)

grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    scoring='roc_auc',
    cv=cv,
    verbose=2,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_xgb_model = grid_search.best_estimator_

def evaluate(trainedmodel, x, y):
    y_pred = trainedmodel.predict(x)
    f1 = f1_score(y, y_pred)
    acc = accuracy_score(y, y_pred)
    y_pred_proba = trainedmodel.predict_proba(x)[:, 1]
    roc_auc = roc_auc_score(y, y_pred_proba)

    report = classification_report(y, y_pred)

    return {
        'f1_score': f1,
        'accuracy': acc,
        'roc_auc_score': roc_auc
    }, report

eval_holdout, report_holdout = evaluate(best_xgb_model, X_holdout, y_holdout)

print("Лучшие параметры:", grid_search.best_params_)
print("CV ROC-AUC:", grid_search.best_score_)
print("\nHoldout evaluation:")
pprint.pprint(eval_holdout)
print("\n", report_holdout)

# Метрики на TRAIN
train_eval, train_report = evaluate(best_xgb_model, X_train, y_train)
print("Train evaluation:")
print(train_eval)
print(train_report)

# Метрики на HOLDOUT
holdout_eval, holdout_report = evaluate(best_xgb_model, X_holdout, y_holdout)
print("Holdout evaluation:")
print(holdout_eval)
print(holdout_report)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_holdout_pred = best_xgb_model.predict(X_holdout)

cm = confusion_matrix(y_holdout, y_holdout_pred) # Используем holdout набор

import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, f1_score

y_proba_holdout = best_xgb_model.predict_proba(X_holdout)[:, 1]

precision, recall, thresholds = precision_recall_curve(y_holdout, y_proba_holdout)
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
best_f1_index = np.argmax(f1_scores)
best_threshold_f1 = thresholds[best_f1_index]

print("Анализ Порога (Максимум F1-score)")
print(f"Порог, максимизирующий F1: {best_threshold_f1:.4f}")
print(f"Precision при F1-max: {precision[best_f1_index]:.4f}")
print(f"Recall при F1-max: {recall[best_f1_index]:.4f}")

NEW_THRESHOLD = 0.67

y_holdout_pred_optimized = np.where(y_proba_holdout >= NEW_THRESHOLD, 1, 0)

print(classification_report(y_holdout, y_holdout_pred_optimized))

cm_optimized = confusion_matrix(y_holdout, y_holdout_pred_optimized)