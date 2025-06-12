import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Data
df_flh_el = pd.read_csv('FLH_electrolyzer.csv', index_col=0)
df_flh_pv_wind = pd.read_csv('pv_wind_electricity.csv', index_col=0)

# Fullloadhours (FLH) for PV and Wind
df_sum = df_flh_pv_wind.sum()
df_pv_flh = df_sum.iloc[::2]
df_wind_flh = df_sum.iloc[1::2]

df_pv_flh.reset_index(drop=True, inplace=True)
df_wind_flh.reset_index(drop=True, inplace=True)
df_pv_wind_flh = pd.concat([df_pv_flh, df_wind_flh], axis=1)
df_pv_wind_flh = df_pv_wind_flh.rename(columns={df_pv_wind_flh.columns[0]: 'PV', df_pv_wind_flh.columns[1]: 'Wind'})


#PV KW
y = df_flh_el['PV']  # unabhängige Variable(n)
X = df_flh_el['FLH_electrolyzer']    # Zielvariable
X = X.values.reshape(-1, 1)

poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
print("Koeffizienten:", model.coef_)
print("Achsenabschnitt:", model.intercept_)
# Ausgabe der Formel
print("Formel PV: y =", f"{model.coef_[0]}*{poly.get_feature_names_out()[0]} +{model.coef_[1]}*{poly.get_feature_names_out()[1]} + {model.coef_[2]}*{poly.get_feature_names_out()[2]} + {model.coef_[3]}*{poly.get_feature_names_out()[3]} + {model.coef_[4]}*{poly.get_feature_names_out()[4]}")

df_MW_pv = pd.DataFrame()
for X in range(2000, 6000, 100):
    y = 0.0*1 +2.547699558547833e-08*X + 7.715902799128186e-05*X**2 + -2.347656387286697e-08*X**3 + 1.7837178121312628e-12*X**4 -1.247296667877137
    df_MW_pv.at[X, 'PV_MW'] = y

df_MW_pv['PV_MW'].plot(title='PV Leistung in MW in Abhängigkeit der VLH des Electrolyseurs', xlabel='VLH Elektrolyseur', ylabel='MW PV Leistung')
