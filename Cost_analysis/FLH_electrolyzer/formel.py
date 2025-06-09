import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

df_flh_el = pd.read_csv('FLH_electrolyzer.csv', index_col=0)

df = pd.read_csv('pv_wind_electricity.csv', index_col=0)

df_sum = df.sum()
df_pv = df_sum.iloc[::2]
df_wind = df_sum.iloc[1::2]

df_pv.reset_index(drop=True, inplace=True)
df_wind.reset_index(drop=True, inplace=True)
df_pv_wind = pd.concat([df_pv, df_wind], axis=1)
df_pv_wind = df_pv_wind.rename(columns={df_pv_wind.columns[0]: 'PV', df_pv_wind.columns[1]: 'Wind'})


# Polynomial Regression
X = df_pv_wind[['PV', 'Wind']]  # unabhängige Variable(n)
y = df_flh_el['FLH_electrolyzer']    # Zielvariable

poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
print("Koeffizienten:", model.coef_)
print("Achsenabschnitt:", model.intercept_)
# Ausgabe der Formel
print("Formel: y =", f"{model.coef_[0]}*{poly.get_feature_names_out()[0]} +{model.coef_[1]}*{poly.get_feature_names_out()[1]} + {model.coef_[2]}*{poly.get_feature_names_out()[2]} + {model.coef_[3]}*{poly.get_feature_names_out()[3]} + {model.coef_[4]}*{poly.get_feature_names_out()[4]} + {model.coef_[5]}*{poly.get_feature_names_out()[5]} + {model.coef_[6]}*{poly.get_feature_names_out()[6]} + {model.coef_[7]}*{poly.get_feature_names_out()[7]} + {model.coef_[8]}*{poly.get_feature_names_out()[8]} + {model.coef_[9]}*{poly.get_feature_names_out()[9]} + {model.coef_[10]}*{poly.get_feature_names_out()[10]} + {model.coef_[11]}*{poly.get_feature_names_out()[11]} +{model.coef_[12]}*{poly.get_feature_names_out()[12]} +{model.coef_[13]}*{poly.get_feature_names_out()[13]} +{model.coef_[14]}*{poly.get_feature_names_out()[14]} +{model.intercept_}")

for i in range(len(df_flh_el)):
    y = 0.0*1 +-6.6770138990268e-05*df_pv[i] + 0.0009983995228525259*df_wind[i] + -0.0792907929992582*df_pv[i]**2 + 0.6015039377643137*df_pv[i]*df_wind[i] + -0.17342074638805446*df_wind[i]**2 + 0.00023937794024431227*df_pv[i]**3 + -0.0006510799366329*df_pv[i]**2*df_wind[i] + 0.00019244450456020793*df_pv[i]*df_wind[i]**2 + -1.816467055199652e-06*df_wind[i]**3 + -8.5611244271594e-08*df_pv[i]**4 + 1.7739890917961985e-07*df_pv[i]**3*df_wind[i] + -5.4292976076750066e-08*df_pv[i]**2*df_wind[i]**2 +1.3219706105279685e-09*df_pv[i]*df_wind[i]**3 +-4.5916292049454945e-11*df_wind[i]**4 +-244026.2227515451
    #y = 0.0*1 +2.3300847735746117e-05*df_pv[i] + 0.000989975461021474*df_wind[i] + 0.039698250531352605*df_pv[i]**2 + 0.6773889381668023*df_pv[i]*df_wind[i] + -0.18346173742823574*df_wind[i]**2 + 0.00018972780598021586*df_pv[i]**3 + -0.0007363766172944372*df_pv[i]**2*df_wind[i] + 0.00020457303904330951*df_pv[i]*df_wind[i]**2 + -1.8899238803569144e-06*df_wind[i]**3 + -8.385932855961002e-08*df_pv[i]**4 + 2.0311812318590393e-07*df_pv[i]**3*df_wind[i] + -5.9474915476495186e-08*df_pv[i]**2*df_wind[i]**2 + 1.9176669613403185e-09*df_pv[i]*df_wind[i]**3 + -1.151973484729259e-10*df_wind[i]**4 + -365571.94351789093
    df_flh_el.at[i, 'FLH function graph'] = y

df_flh_el.plot(ylabel='FLH_electrolyzer', title='FLH_electrolyzer with PV and Wind', xlabel= 'Itteration')