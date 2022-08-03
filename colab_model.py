#%%

import numpy as np
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
import matplotlib.pyplot as plt

df_data = pd.read_csv("data/data.csv")
features = ["userId","movieId","rating"]


reader = Reader()
data = Dataset.load_from_df(df_data[features], reader)

final_results = {"RMSE":{},
                 "MAE":{}}

for epoch in range(3,25):
    svd = SVD(verbose=True, n_epochs=epoch)
    results = cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    final_results["RMSE"][epoch] = results["test_rmse"].mean()
    final_results["MAE"][epoch] = results["test_mae"].mean()
    

trainset = data.build_full_trainset()
svd.fit(trainset)

print(pd.DataFrame(final_results))
pd.DataFrame(final_results).T.plot.bar()
plt.show()
# print(svd.predict(uid=56, iid=4613))