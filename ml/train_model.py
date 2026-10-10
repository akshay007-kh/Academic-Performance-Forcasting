import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# --------------------------------
# 1. Load Dataset
# --------------------------------

data = pd.read_csv("ml/dataset.csv")

print("Dataset loaded successfully!")
print("Total records:", len(data))


# --------------------------------
# 2. Separate Features and Target
# --------------------------------

X = data[
    [
        "attendance",
        "internal_marks",
        "assignment_marks",
        "previous_marks",
        "study_hours",
        "backlogs",
        "participation"
    ]
]

y = data["final_mark"]


# --------------------------------
# 3. Train-Test Split
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# --------------------------------
# 4. Create ML Model
# --------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# --------------------------------
# 5. Train Model
# --------------------------------

model.fit(
    X_train,
    y_train
)

print("\nModel training completed!")


# --------------------------------
# 6. Make Predictions
# --------------------------------

predictions = model.predict(X_test)


# --------------------------------
# 7. Evaluate Model
# --------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("\nModel Evaluation")

print("-------------------------")

print("Mean Absolute Error:",
      round(mae, 2))

print("R2 Score:",
      round(r2, 2))


# --------------------------------
# 8. Save Model
# --------------------------------

joblib.dump(
    model,
    "ml/performance_model.pkl"
)

print("\nModel saved successfully!")

print("File: ml/performance_model.pkl")