import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# Charger les données d'entraînement
train_df = pd.read_csv("ranking_with_40depths_train.csv", sep=',', header=0)

# Séparer les caractéristiques (X) et la variable cible (Y) pour l'entraînement
X_train = train_df[[f"Ranking depth{i}" for i in range(1, 40)]].values
Y_train = train_df["Ranking depth40"].values

# Charger les données de test
test_df = pd.read_csv("ranking_with_40depths_test.csv", sep=',', header=0)

X_test = test_df[[f"Ranking depth{i}" for i in range(1, 40)]].values
Y_test = test_df["Ranking depth40"].values

# Redimensionner les données pour qu'elles aient la forme (samples, timesteps, features) pour le CNN
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Construire le modèle CNN
model = Sequential()

# Première couche Conv1D avec plus de filtres
model.add(Conv1D(filters=128, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))  # Plus de filtres
model.add(Dropout(0.3))  # Augmentation du taux de Dropout

# Ajouter une autre couche Conv1D
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))  # Deuxième couche Conv1D
model.add(Dropout(0.3))  # Ajouter Dropout

# Aplatissement des données
model.add(Flatten())

# Ajouter une couche Dense plus grande
model.add(Dense(128, activation='relu'))  # Couche Dense
model.add(Dropout(0.3))  # Dropout pour éviter l'overfitting

# Couche de sortie
model.add(Dense(1))

# Compiler le modèle avec un optimiseur Adam et un taux d'apprentissage
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# Utilisation de EarlyStopping pour éviter l'overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Entraînement du modèle
history = model.fit(X_train, Y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Prédictions sur les données de test
Y_pred = model.predict(X_test)

# Calculer l'erreur quadratique moyenne (MSE)
mse = mean_squared_error(Y_test, Y_pred)
print("Improved Model - MSE:", mse)

# Calculer le coefficient de détermination R²
r2 = 1 - (np.sum((Y_test - Y_pred.flatten())**2) / np.sum((Y_test - np.mean(Y_test))**2))
print("Improved Model - R²:", r2)

# Créer le parity plot pour visualiser les prédictions vs les vraies valeurs
plt.figure(figsize=(8, 6))
plt.scatter(Y_test, Y_pred, color='blue', edgecolors='k', alpha=0.7)
plt.plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], color='red', linestyle='--', linewidth=2)
plt.title('Improved Model - Parity Plot')
plt.xlabel('True Values (Y_test)')
plt.ylabel('Predicted Values (Y_pred)')
plt.grid(True)
plt.show()
plt.savefig("Poor_Plot.png")
