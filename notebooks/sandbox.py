import pandas as pd
import numpy as np

from xgboost.sklearn import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import KFold

from utils.metrics import ndcg_scorer

path = '../data/processed/'
train_users = pd.read_csv(path + '_encoded_train_users.csv')

train_users.fillna(-1, inplace=True)
y_train = train_users['country_destination']
train_users.drop('country_destination', axis=1, inplace=True)
train_users.drop('id', axis=1, inplace=True)

x_train = train_users.values
label_encoder = LabelEncoder()
encoded_y_train = label_encoder.fit_transform(y_train)

xgb = XGBClassifier(
    max_depth=8,
    learning_rate=0.3,
    n_estimators=55,
    gamma=0,
    min_child_weight=1,
    max_delta_step=0,
    subsample=1,
    colsample_bytree=1,
    colsample_bylevel=1,
    reg_alpha=0,
    reg_lambda=1,
    scale_pos_weight=1,
    base_score=0.5,
    missing=None,
    silent=True,
    nthread=-1,
    seed=42
)

kf = KFold(len(x_train), n_folds=10, random_state=42)

score = cross_val_score(xgb, x_train, encoded_y_train,
                        cv=kf, scoring=ndcg_scorer, verbose=10)

print np.mean(score)
