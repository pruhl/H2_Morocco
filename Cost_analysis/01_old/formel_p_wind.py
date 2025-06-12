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

# # Verhältnis Wind zu FLH Elektrolyzer
# X = df_pv_wind_flh['Wind'] / (df_pv_wind_flh['PV'] + df_pv_wind_flh['Wind']) # unabhängige Variable(n)
# y = df_flh_el['FLH_electrolyzer']    # Zielvariable
# X = X.values.reshape(-1, 1)

# poly = PolynomialFeatures(degree=4)
# X_poly = poly.fit_transform(X)

# model = LinearRegression()
# model.fit(X_poly, y)
# print("Koeffizienten:", model.coef_)
# print("Achsenabschnitt:", model.intercept_)
# # Ausgabe der Formel
# print("Formel Wind: y =", f"{model.coef_[0]}*{poly.get_feature_names_out()[0]} +{model.coef_[1]}*{poly.get_feature_names_out()[1]} + {model.coef_[2]}*{poly.get_feature_names_out()[2]} + {model.coef_[3]}*{poly.get_feature_names_out()[3]} + {model.coef_[4]}*{poly.get_feature_names_out()[4]}")

# for i in range(len(df_flh_el)):
#     y_wind = 0.0*1 +-602525.5425687934*X[i] + 1735460.582077536*X[i]**2 + -2130294.7462292337*X[i]**3 + 959110.1708877761*X[i]**4 + 77388.76094051664
#     df_flh_el.at[i, 'FLH_function_el_with_wind'] = y_wind

# df_flh_el[['FLH_electrolyzer', 'FLH_function_el_with_wind']].plot()

# df = pd.DataFrame()
# for i in np.arange(0, 1.01, 0.01):
#         y_wind = 0.0*1 +-602525.5425687934*i + 1735460.582077536*i**2 + -2130294.7462292337*i**3 + 959110.1708877761*i**4 + 77388.76094051664
#         if y_wind > df_flh_el['FLH_electrolyzer'].max():
#             y_wind = df_flh_el['FLH_electrolyzer'].max()
        
#         df.at[i, 'FLH_function_el_with_wind_test'] = y_wind

# df['FLH_function_el_with_wind_test'].plot()

#Wind KW
y = df_flh_el['Wind']  # unabhängige Variable(n)
X = df_flh_el['FLH_electrolyzer']    # Zielvariable
X = X.values.reshape(-1, 1)

poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
print("Koeffizienten:", model.coef_)
print("Achsenabschnitt:", model.intercept_)
# Ausgabe der Formel
print("Formel Wind: y =", f"{model.coef_[0]}*{poly.get_feature_names_out()[0]} +{model.coef_[1]}*{poly.get_feature_names_out()[1]} + {model.coef_[2]}*{poly.get_feature_names_out()[2]} + {model.coef_[3]}*{poly.get_feature_names_out()[3]} + {model.coef_[4]}*{poly.get_feature_names_out()[4]}")

df_MW_wind = pd.DataFrame()
for X in range(2000, 5000, 100):
    y = 0.0*1 +2.3488108197027923e-08*X + 7.113553154609071e-05*X**2 + -1.4679236320927621e-08*X**3 + 8.297602504707571e-13*X**4 + -288.41758494153777

    df_MW_wind.at[X, 'Wind_MW'] = y

df_MW_wind['Wind_MW'].plot(title='Wind Leistung in MW in Abhängigkeit der VLH des Electrolyseurs', xlabel='VLH Elektrolyseur', ylabel='MW Wind Leistung')