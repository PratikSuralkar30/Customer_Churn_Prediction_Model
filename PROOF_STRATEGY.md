# GitHub Proof Strategy: Customer Churn Prediction Model

To effectively showcase this project to recruiters, data science managers, and ML engineering hiring teams, we recommend a structured, day-by-day commit strategy. This makes the project look organically developed rather than uploaded all at once.

## Day 1: Project Skeleton & Data Engineering
- **Commit 1**: `Initial commit: Set up directory structure and requirements`
- **Commit 2**: `feat(data): Add data simulation script for advanced churn features (SLA, tickets)`
- **Commit 3**: `docs: Add initial README structure and dataset definitions`

## Day 2: Machine Learning Pipeline
- **Commit 1**: `feat(ml): Create scikit-learn preprocessing pipeline for numerical/categorical features`
- **Commit 2**: `feat(ml): Train XGBoost baseline model with evaluate metrics`
- **Commit 3**: `fix(ml): Tune XGBoost hyperparameters to optimize ROC-AUC and PR-AUC`

## Day 3: Serving Layer & API
- **Commit 1**: `feat(api): Initialize FastAPI app and load pickled XGBoost pipeline`
- **Commit 2**: `feat(api): Implement Pydantic data models for /score endpoint`
- **Commit 3**: `feat(api): Integrate SHAP TreeExplainer for the /explain endpoint`

## Day 4: Full-Stack Integration & Dashboard
- **Commit 1**: `feat(web): Bootstrap Next.js 15 app with TailwindCSS`
- **Commit 2**: `feat(web): Build SuccessOps Dashboard UI and API integration`
- **Commit 3**: `style(web): Add dynamic risk alerts and SHAP driver visualizations`

## Day 5: Final Polish
- **Commit 1**: `docs: Update README with architecture diagrams and run instructions`
- **Commit 2**: `chore: Code cleanup and final testing`

## Interview Talking Points
1. **Business Value**: "I noticed public datasets lacked complex features like SLA breaches, so I simulated them to mirror real-world B2B SaaS scenarios."
2. **MLOps Best Practices**: "Instead of just a Jupyter notebook, I deployed the model using FastAPI to show I understand the serving layer."
3. **Actionability**: "The Next.js dashboard uses SHAP to not only predict *if* a customer will churn, but *why*, so customer success teams can take immediate action."
