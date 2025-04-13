from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

# Charger les données d'entraînement
train_df = pd.read_csv("ranking_with_40depths_train.csv", sep=',', header=0)

# Séparer les caractéristiques (X) et la variable cible (Y) pour l'entraînement
# Séparer les caractéristiques (X) et la variable cible (Y) pour l'entraînement
X_train = train_df[[f"Ranking depth{i}" for i in range(1, 40)]].values
Y_train = train_df["Ranking depth40"].values

# Charger les données de test
test_df = pd.read_csv("ranking_with_40depths_test.csv", sep=',', header=0)

# Charger les données de test
X_test = test_df[[f"Ranking depth{i}" for i in range(1, 40)]].values
Y_test = test_df["Ranking depth40"].values


# Définir les hyperparamètres à explorer
param_grid = {
    'n_estimators': [100],  # Nombre d'arbres
    'max_depth': [10], # Profondeur des arbres
    'min_samples_split': [3],  # Nombre minimal d'échantillons pour diviser un nœud
    'min_samples_leaf': [1]  # Nombre minimal d'échantillons pour qu'un nœud soit une feuille
}

# Créer le modèle Random Forest
rf = RandomForestRegressor(random_state=10000)

# Configurer la recherche en grille
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')

# Exécuter la recherche en grille sur les données d'entraînement
grid_search.fit(X_train, Y_train)

# Meilleurs hyperparamètres
print("Meilleurs hyperparamètres trouvés :")
print(grid_search.best_params_)

# Utiliser le meilleur modèle trouvé pour prédire sur les données de test
best_rf = grid_search.best_estimator_

# Prédictions avec le modèle optimal
Y_pred = best_rf.predict(X_test)

# Calculer l'erreur quadratique moyenne (MSE)
mse = mean_squared_error(Y_test, Y_pred)
print("Mean Squared Error (MSE):", mse)

# Calculer le coefficient de détermination R²
r2 = best_rf.score(X_test, Y_test)
print("R² (Coefficient de détermination):", r2)

import matplotlib.pyplot as plt

# Créer le parity plot
plt.figure(figsize=(8, 6))
plt.scatter(Y_test, Y_pred, color='blue', edgecolors='k', alpha=0.7)
plt.plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], color='red', linestyle='--', linewidth=2)
plt.title('Parity Plot: Observed vs Predicted')
plt.xlabel('True Values (Y_test)')
plt.ylabel('Predicted Values (Y_pred)')
plt.grid(True)
plt.show()
plt.savefig("Plot.png")