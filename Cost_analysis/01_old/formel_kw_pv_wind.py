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
X = df_flh_el[['PV', 'Wind']]  # unabhängige Variable(n)
y = df_flh_el['FLH_electrolyzer']    # Zielvariable

poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
print("Koeffizienten:", model.coef_)
print("Achsenabschnitt:", model.intercept_)
# Ausgabe der Formel
print("Formel kw: y =", f"{model.coef_[0]}*{poly.get_feature_names_out()[0]} +{model.coef_[1]}*{poly.get_feature_names_out()[1]} + {model.coef_[2]}*{poly.get_feature_names_out()[2]} + {model.coef_[3]}*{poly.get_feature_names_out()[3]} + {model.coef_[4]}*{poly.get_feature_names_out()[4]} + {model.coef_[5]}*{poly.get_feature_names_out()[5]} + {model.coef_[6]}*{poly.get_feature_names_out()[6]} + {model.coef_[7]}*{poly.get_feature_names_out()[7]} + {model.coef_[8]}*{poly.get_feature_names_out()[8]} + {model.coef_[9]}*{poly.get_feature_names_out()[9]} + {model.coef_[10]}*{poly.get_feature_names_out()[10]} + {model.coef_[11]}*{poly.get_feature_names_out()[11]} +{model.coef_[12]}*{poly.get_feature_names_out()[12]} +{model.coef_[13]}*{poly.get_feature_names_out()[13]} +{model.coef_[14]}*{poly.get_feature_names_out()[14]} +{model.intercept_}")

# Erstelle die 3D-Oberfläche
X = np.linspace(50, 200, 100)
Y = np.linspace(150, 200, 100) # wenn wind kleiner als 1500 oder pv geringer als 1700, dann kein elektrolyseur
X, Y = np.meshgrid(X, Y)
Z = 0.0*1 +-4335.895425185187*X + -4249.214798468962*Y + 28.95355171663641*X**2 + 49.231872604000955*X*Y + 26.570796723720765*Y**2 + -0.08075531136764624*X**3 + -0.2002729313183611*X**2*Y + -0.1917999451311072*X*Y**2 + -0.06464177699202667*Y**3 + 7.230409710246022e-05*X**4 + 0.0002938074983376282*X**3*Y + 0.00032614218821436225*X**2*Y**2 + 0.00026465796554475673*X*Y**3 + 4.056042985212116e-05*Y**4 + 244284.8281860922 
Z[Z > 8760] = 8760
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z , cmap='viridis')


# Achsen Beschriftungen
ax.set_xlabel('Leistung PV [MW]')
ax.set_ylabel('Leistung Wind [MW]')
ax.set_zlabel('Elektrolyzer VLH')

plt.title('VLH des Elektrolyzers in Abhängigkeit der Leistung von PV und Wind')
plt.tight_layout()

plt.show()