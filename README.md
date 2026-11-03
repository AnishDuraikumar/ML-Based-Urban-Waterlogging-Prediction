# Machine Learning-Based Early Warning System for Predicting Urban Waterlogging Risk During Heavy Rainfall

## Project Overview

This project develops an experimental machine learning prototype to estimate potential urban waterlogging risk using rainfall patterns and historical flood-event records.

## Objectives
- Analyse historical rainfall data.
- Perform rainfall feature engineering.
- Train a Random Forest Classifier.
- Evaluate model performance.
- Develop an interactive Streamlit application.

## Dataset
- Source: India Meteorological Department (IMD).
- Rainfall period: 2023.
- Processed dataset: 212,064 district-day records.
- Districts covered: 576.
- Historical flood inventory: 1967–2023.

## Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit

## Machine Learning Model

Random Forest Classifier with six rainfall features:
1. Mean rainfall
2. Maximum rainfall
3. Previous 3-day rainfall
4. Previous 7-day rainfall
5. 3-day total rainfall
6. 7-day total rainfall

## Model Evaluation

| Metric | Result |
|---|---:|
| Accuracy | 94.26% |
| Precision | 0.47% |
| Recall | 28.57% |
| F1-score | 0.93% |

The results are affected by severe class imbalance and incomplete flood-event labels. The prototype is not validated for real-world early-warning deployment.

## Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Research Paper

The IEEE-format research paper available in the `paper/` directory.

## Limitations

- Incomplete historical flood-event labels.
- Low precision and false alerts.
- Rainfall-only input features.
- Validation limited to the 2023 study period.

## Future Work

- Include multiple years of rainfall data.
- Integrate elevation and drainage information.
- Compare different machine learning algorithms.
- Validate predictions using reliable timestamped waterlogging observations.

## Author

Anish D

M.Tech – Computer Science

