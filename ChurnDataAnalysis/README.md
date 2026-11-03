Customer Churn Prediction – Project Summary Report
Project: IBM Telco Customer Churn Prediction | Domain: Machine Learning / Customer Analytics | Application: Python, Scikit-learn, XGBoost and Streamlit
1. Executive summary
The objective of this project is to develop a machine learning solution that identifies telecom customers who are likely to discontinue their services.

The solution uses customer demographics, account information, service subscriptions, contract details, and billing information to estimate churn probability. The goal is to help a telecom business identify at-risk customers early and support targeted customer retention initiatives.

The project progresses beyond model training by incorporating probability-based risk assessment, business recommendations, and a Streamlit interface for interactive predictions.
2. Business problem
Customer churn directly affects recurring revenue, customer lifetime value, and business growth.

Telecom companies need to answer three questions:
1. Which customers are most likely to leave?
2. What customer characteristics are associated with churn?
3. How can retention teams prioritize customers for intervention?
Proposed solution: Build a predictive classification model that assigns each customer a churn probability and translates that score into an actionable risk category.
3. Dataset overview
The project uses the IBM Telco Customer Churn dataset.
Attribute	Description
Total records	7,043 customers
Original columns	21
Target variable	Churn
Target classes	Yes / No
Numerical features	Tenure, MonthlyCharges, TotalCharges
Categorical features	Customer demographics, services, contracts and payment information

The customerID column was excluded from model training because it is an identifier rather than a meaningful predictive feature.

TotalCharges required conversion from text to numeric values. Blank entries were converted to missing values and handled through the preprocessing pipeline.
4. Data preparation and feature engineering
The following preparation steps were implemented:
- Removed customer identifiers from predictive features.
- Converted the target variable into binary values: Yes = 1 and No = 0.
- Converted TotalCharges into a numeric column.
- Used an 80:20 stratified train-test split.
- Applied mean imputation and standardization to numerical variables.
- Applied most-frequent-value imputation and one-hot encoding to categorical variables.
- Used a Scikit-learn ColumnTransformer and machine learning pipelines to combine preprocessing and model training.
This approach helps prevent preprocessing information from the test dataset leaking into model training.
5. Machine learning models
Four model configurations were evaluated:
- Logistic Regression – baseline classification model.
- Random Forest – ensemble-based classification.
- XGBoost – gradient-boosting classification.
- Tuned XGBoost – hyperparameter optimization using RandomizedSearchCV.
6. Model evaluation and results
The following results were recorded in the later model-comparison run of the notebook.
Model	Accuracy	Precision	Recall	F1-score	PR-AUC
Logistic Regression	80.6%	65.7%	55.9%	60.4%	66.7%
Random Forest	78.5%	62.5%	47.6%	54.0%	62.0%
XGBoost	80.1%	65.7%	52.1%	58.1%	65.2%
Tuned XGBoost	81.0%	67.8%	54.0%	60.1%	67.0%
More-tuned XGBoost	81.0%	68.4%	52.7%	59.5%	66.8%

These are previously recorded notebook results, not independently rerun or verified in this report.
Interpretation
- Tuned XGBoost achieved the highest accuracy in this comparison.
- More-tuned XGBoost achieved the highest precision.
- Logistic Regression achieved a slightly higher F1-score than the tuned XGBoost version.
- Tuned XGBoost achieved the highest PR-AUC, although its advantage over Logistic Regression was small.
- Random Forest performed less effectively than the other evaluated models.
Model selection recommendation: Tuned XGBoost is a reasonable candidate for the application, but Logistic Regression should remain a benchmark. The final choice should consider validation results, business priorities, model stability, and interpretability—not just accuracy.
7. Probability threshold optimization
A classification model typically uses a default threshold of 0.50. However, this may not be ideal for churn prediction because missing a customer who is about to leave can be costly.

The project explored different probability thresholds.
Threshold	Precision	Recall	F1-score
0.10	39.8%	94.7%	56.0%
0.20	47.7%	85.0%	61.2%
0.30	54.0%	76.7%	63.4%
0.40	59.7%	65.0%	62.2%
0.50	67.8%	54.0%	60.1%

The threshold of 0.30 produced the highest F1-score in that particular experiment.

Business interpretation: Lowering the threshold identifies more potentially at-risk customers, but also increases false positives. This can be useful when the business wants to prioritize churn prevention over minimizing unnecessary retention outreach.

Important methodological correction: the threshold should be selected using validation data or out-of-fold training predictions, not the final test set. The final test set should be reserved for one unbiased evaluation.
8. Business application and customer retention strategy
The prediction system can convert model probabilities into customer risk categories.

An illustrative segmentation approach:
Churn probability	Risk category	Suggested action
Below 30%	Low	Regular engagement and service communication
30–60%	Medium	Monitor customer activity and identify service concerns
60% or higher	High	Prioritize personalized retention outreach

Potential retention strategies include:
- Contract optimization: Encourage suitable customers to consider longer-term plans.
- Pricing interventions: Review high monthly charges and offer appropriate packages.
- Service improvement: Investigate complaints and technical support issues.
- Customer engagement: Identify customers with limited service adoption and improve engagement.
- Payment experience: Address billing friction and payment-related concerns.
These are proposed business interventions, not proven outcomes. Their effectiveness would need to be tested through retention campaigns and controlled experiments.
9. Streamlit application
The next stage is to deploy the trained model through a Streamlit application.







medium.com


The proposed application will provide:
1. Customer information input form.
2. Churn probability prediction.
3. Low, medium, and high risk classification.
4. Suggested retention actions.
5. Batch customer scoring through CSV upload.
6. Business-level churn analytics dashboard.
The intended architecture is:
IBM Telco Customer Churn Dataset
Customer demographics, services and billing data

Data preprocessing and feature engineering
Imputation, encoding and scaling

Machine learning model
Logistic Regression / XGBoost

Saved model artifact
Joblib model pipeline and decision threshold

Streamlit application
Predictions, customer segmentation and retention insights

The application is currently at the integration stage. Streamlit is installed, but the local command invocation issue still needs to be resolved. The model artifact also needs to be tested with the same compatible Python and library versions used during training.
10. Technology stack
Area	Technology
Programming	Python
Data manipulation	Pandas, NumPy
Data visualization	Matplotlib, Seaborn
Machine learning	Scikit-learn, XGBoost
Preprocessing	ColumnTransformer, Pipeline
Model evaluation	Precision, Recall, F1, ROC-AUC, PR-AUC
Model explainability	SHAP (planned / to be validated)
Model persistence	Joblib
Application	Streamlit
Development	Google Colab, VS Code

11. Future enhancements
To make this a stronger portfolio project, the following improvements are recommended:
1. Model explainability: Use SHAP to explain the strongest churn drivers at both global and individual customer levels.
2. Customer segmentation: Build actionable customer segments based on churn probability, contract type, tenure and billing.
3. Batch prediction: Allow business teams to upload customer records and generate churn scores in bulk.
4. Executive dashboard: Display churn distribution, high-risk customers, contract patterns and revenue exposure.
5. Model monitoring: Track prediction distributions, data drift and model performance over time.
6. Retention experimentation: Measure whether targeted retention offers actually reduce churn.
7. Deployment: Publish the Streamlit application using Streamlit Community Cloud or another cloud platform.
12. Conclusion
This project demonstrates an end-to-end customer churn prediction workflow, from data cleaning and preprocessing to model comparison, probability-based classification and business recommendations.

The most important achievement is not simply building a machine learning classifier. It is translating predictive outputs into a decision-support solution that can help a telecom business prioritize customer retention activities.

The project can demonstrate practical capabilities in:
- Machine learning and predictive analytics.
- Python-based data processing.
- Feature engineering and model evaluation.
- Model deployment and application development.
- Business problem-solving and data-driven decision-making.
