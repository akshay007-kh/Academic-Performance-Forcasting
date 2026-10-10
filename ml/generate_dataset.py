import pandas as pd
import numpy as np

# Same result every time
np.random.seed(42)

# Number of students
n = 1000


# Academic features

attendance = np.random.uniform(45, 100, n)

internal_marks = np.random.uniform(30, 95, n)

assignment_marks = np.random.uniform(35, 100, n)

previous_marks = np.random.uniform(30, 95, n)

study_hours = np.random.uniform(0.5, 8, n)

backlogs = np.random.randint(0, 5, n)

participation = np.random.uniform(30, 100, n)


# Calculate final mark

final_mark = (
    attendance * 0.15
    + internal_marks * 0.25
    + assignment_marks * 0.10
    + previous_marks * 0.20
    + study_hours * 3
    + participation * 0.10
    - backlogs * 3
)


# Add small random variation

noise = np.random.normal(0, 4, n)

final_mark = final_mark + noise


# Keep marks between 0 and 100

final_mark = np.clip(
    final_mark,
    0,
    100
)


# Create DataFrame

data = pd.DataFrame({

    "attendance": attendance.round(2),

    "internal_marks": internal_marks.round(2),

    "assignment_marks": assignment_marks.round(2),

    "previous_marks": previous_marks.round(2),

    "study_hours": study_hours.round(2),

    "backlogs": backlogs,

    "participation": participation.round(2),

    "final_mark": final_mark.round(2)

})


# Save dataset

data.to_csv(
    "ml/dataset.csv",
    index=False
)

print("Dataset created successfully!")

print("Total records:", len(data))

print("\nFirst 5 records:")

print(data.head())