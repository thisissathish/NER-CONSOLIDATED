"""Train risk prediction model."""
import pickle
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb

from app.database import SessionLocal
from app.ml.features import build_training_data


def train_risk_model():
    """
    Train XGBoost risk prediction model.

    Model predicts probability of disruption for each road segment
    given current conditions (weather, season, terrain, history).

    Training approach:
    - Chronological train/test split (last 60 days held out)
    - XGBoost classifier for probability estimates
    - Focus on ranking quality (ROC-AUC) over threshold accuracy

    Known limitation: Low base rate (~2% disruption rate in synthetic data)
    means threshold-based metrics (precision/recall at 0.5) will look weak.
    This is expected. The route engine uses raw probabilities for ranking,
    not binary classification, so ROC-AUC is the right metric.
    """
    print("Building training dataset...")
    db = SessionLocal()
    df = build_training_data(db)
    db.close()

    print(f"Dataset shape: {df.shape}")
    print(f"Disruption rate: {df['had_disruption'].mean():.1%}")

    # Features for modeling
    feature_cols = [
        'is_monsoon',
        'is_hilly',
        'is_mountainous',
        'month',
        'day_of_year',
        'recent_disruptions',
        'estimated_precipitation_mm',
        'distance_km'
    ]

    X = df[feature_cols]
    y = df['had_disruption']

    # Chronological split: last 60 days for test
    split_idx = len(df) - (60 * len(df['segment_id'].unique()))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

    # Train XGBoost model
    # Note: scale_pos_weight was tried to handle class imbalance but removed
    # because it degraded ranking quality on this small synthetic dataset.
    # With more training volume, it might help again. See git history.
    print("\nTraining XGBoost model...")
    model = xgb.XGBClassifier(
        max_depth=5,
        learning_rate=0.1,
        n_estimators=100,
        objective='binary:logistic',
        random_state=42,
        eval_metric='auc'
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    # Evaluate
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)

    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)

    # ROC-AUC (primary metric for ranking quality)
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC: {auc:.3f}")
    print("(This is the key metric - measures ranking quality)")

    # Confusion matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    # Classification report (will show low recall due to low base rate)
    print("\nClassification Report (0.5 threshold):")
    print("Note: Low recall is expected with rare events. Route engine")
    print("uses probabilities directly, not 0.5 threshold classification.")
    print(classification_report(y_test, y_pred))

    # Feature importance
    print("\nFeature Importance:")
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))

    # Save model
    model_dir = Path(__file__).parent.parent.parent / 'models'
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / 'risk_model.pkl'

    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_cols': feature_cols,
            'version': '1.0',
            'trained_at': datetime.now().isoformat(),
            'metrics': {
                'roc_auc': float(auc),
                'train_size': len(X_train),
                'test_size': len(X_test)
            }
        }, f)

    print(f"\n[OK] Model saved to {model_path}")
    print(f"[OK] Training complete!")


if __name__ == "__main__":
    train_risk_model()
