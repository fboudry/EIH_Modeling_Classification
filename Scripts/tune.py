import optuna
import numpy as np
import sklearn.metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb

def objective(trial):
    train_x = r.light_gbm_train_data
    train_y = r.light_gbm_train_data_label
    test_x = r.light_gbm_test_data
    test_y = r.light_gbm_test_data_label
    dtrain = lgb.Dataset(train_x, label=train_y)
 
    param = {
      'boosting_type': 'dart',
      'objective': 'binary',
      'metric': 'binary_logloss',
      'learning_rate': trial.suggest_loguniform('learning_rate',0.005,1 ),
      'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 5.0),
      'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 5.0),
      'num_leaves': trial.suggest_int('num_leaves', 3, 36),
      'max_depth': trial.suggest_int('max_depth', 5, 101),
      'feature_fraction': trial.suggest_uniform('feature_fraction', 0.5, 1.0),
      'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.5, 1.0),
      'bagging_freq': trial.suggest_int('bagging_freq', 2, 7),
      'is_unbalance':True,
    }
 
    gbm = lgb.train(param, dtrain, num_boost_round=150)
    preds = gbm.predict(test_x)
    pred_labels = np.rint(preds)
    accuracy = sklearn.metrics.accuracy_score(test_y, pred_labels)
    return accuracy
 
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=5000)
 
print('Number of finished trials:', len(study.trials))
print('Best trial:', study.best_trial.params)
