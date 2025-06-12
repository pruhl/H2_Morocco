import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from mpl_toolkits.mplot3d import Axes3D 

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


# Polynomial Regression for FLH Electrolyzer
X = df_pv_wind_flh[['PV', 'Wind']]  # unabhängige Variable(n)
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
    y_el = 0.0*1 +-6.6770138990268e-05*df_pv_flh[i] + 0.0009983995228525259*df_wind_flh[i] + -0.0792907929992582*df_pv_flh[i]**2 + 0.6015039377643137*df_pv_flh[i]*df_wind_flh[i] + -0.17342074638805446*df_wind_flh[i]**2 + 0.00023937794024431227*df_pv_flh[i]**3 + -0.0006510799366329*df_pv_flh[i]**2*df_wind_flh[i] + 0.00019244450456020793*df_pv_flh[i]*df_wind_flh[i]**2 + -1.816467055199652e-06*df_wind_flh[i]**3 + -8.5611244271594e-08*df_pv_flh[i]**4 + 1.7739890917961985e-07*df_pv_flh[i]**3*df_wind_flh[i] + -5.4292976076750066e-08*df_pv_flh[i]**2*df_wind_flh[i]**2 +1.3219706105279685e-09*df_pv_flh[i]*df_wind_flh[i]**3 +-4.5916292049454945e-11*df_wind_flh[i]**4 +-244026.2227515451
    df_flh_el.at[i, 'FLH_function_el'] = y_el

df_flh_el[['FLH_electrolyzer', 'FLH_function_el']].plot()

# Erstelle die 3D-Oberfläche
X = np.linspace(1800, 1950, 100)
Y = np.linspace(2500, 5000, 100) # wenn wind kleiner als 1500 oder pv geringer als 1700, dann kein elektrolyseur
X, Y = np.meshgrid(X, Y)
Z = 0.0*1 +-6.6770138990268e-05*X + 0.0009983995228525259*Y + -0.0792907929992582*X**2 + 0.6015039377643137*X*Y + -0.17342074638805446*Y**2 + 0.00023937794024431227*X**3 + -0.0006510799366329*X**2*Y + 0.00019244450456020793*X*Y**2 + -1.816467055199652e-06*Y**3 + -8.5611244271594e-08*X**4 + 1.7739890917961985e-07*X**3*Y + -5.4292976076750066e-08*X**2*Y**2 +1.3219706105279685e-09*X*Y**3 +-4.5916292049454945e-11*Y**4 +-244026.2227515451
Z[Z < 0] = 0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z , cmap='viridis')


# Achsen Beschriftungen
ax.set_xlabel('PV VLH')
ax.set_ylabel('Wind VLH')
ax.set_zlabel('Elektrolyzer VLH')

plt.title('VLH des Elektrolyzers in Abhängigkeit der VLH PV und Wind')
plt.tight_layout()

plt.show()