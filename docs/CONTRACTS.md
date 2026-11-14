
# Team Integration Contracts

**Project:** Adaptive Model Updating in Automated Data Pipelines

**Version:** 0.1.0

**Status:** Draft - Pending Team Approval

---

## 1. Purpose

This document defines the shared technical interfaces between the three project teams:

- Data Pipeline
- AI
- MLOps

The purpose is to allow all teams to develop their components independently without waiting for other teams to finish their implementation.

Each team must agree on the required inputs, outputs, data formats, function interfaces, and metrics before integration.

Teams can use sample data or mock implementations while the actual components are being developed.

This document focuses on three main interfaces:

1. Feature Table Contract (Data Pipeline → AI).
2. Model Interface Contract (AI → MLOps).
3. Metrics Contract (MLOps → All Teams).

---

## 2. Shared Conventions

The following conventions are proposed for all teams.

| Item | Convention | Status |
|---|---|---|
| Python version | Python 3.11 | Agreed |
| Timestamp format | ISO 8601 | Proposed |
| Timezone | UTC | Proposed |
| Python naming | snake_case | Proposed |
| Streaming format | JSON | Proposed |
| Processed data format | Parquet | Proposed |
| Version control | Git and GitHub | Agreed |

All teams should follow the agreed conventions when implementing shared interfaces.

---

## 3. Feature Table Contract

**Direction:** Data Pipeline → AI

**Purpose:** Define how Data Pipeline provides feature data to the AI team for model training and prediction.

### 3.1. Table Definition

Proposed table name:

`pm25_hourly_features`

Description:

An hourly feature table containing air quality and weather information required for PM2.5 forecasting.

| Property | Proposed Definition |
|---|---|
| Table name | `pm25_hourly_features` |
| Data format | Parquet |
| Update frequency | Every hour |
| Timestamp format | ISO 8601 |
| Timezone | UTC |
| Row granularity | One station per observation time |

Status: Proposed - Pending Data Pipeline and AI agreement.

### 3.2. Feature Schema

The following schema is an initial example for discussion.

| Column Name | Data Type | Unit | Description |
|---|---|---|---|
| `station_id` | STRING | - | Monitoring station identifier |
| `event_time` | TIMESTAMP | UTC | Observation timestamp |
| `pm25_ug_m3` | FLOAT | µg/m³ | Historical PM2.5 measurement |
| `temperature_c` | FLOAT | °C | Air temperature |
| `relative_humidity_pct` | FLOAT | % | Relative humidity |
| `wind_speed_m_s` | FLOAT | m/s | Wind speed |
| `wind_direction_deg` | FLOAT | Degree | Wind direction |

Additional features may be added after discussion with the AI team.

The final feature list must be based on actual source data availability.

### 3.3. Sample Feature Data

Example:

```csv
station_id,event_time,pm25_ug_m3,temperature_c,relative_humidity_pct,wind_speed_m_s,wind_direction_deg
HN001,2026-11-13T08:00:00Z,25.4,30.5,75.0,2.1,180.0
HN001,2026-11-13T09:00:00Z,27.2,31.0,72.0,2.3,185.0
HN001,2026-11-13T10:00:00Z,29.1,31.8,70.0,2.5,190.0
```

This sample allows the AI team to start implementing data loading, preprocessing, feature validation, and training without waiting for the real pipeline.

### 3.4. Timestamp and Update Frequency

Proposed rules:

- All timestamps use UTC.
- The timestamp format follows ISO 8601.
- Feature data is updated hourly.
- Each row represents one station at one observation time.
- Duplicate records should be identifiable using `station_id` and `event_time`.

### 3.5. Late Label Delivery

The model requires actual PM2.5 values to compare against previous predictions.

Feature data and actual labels must be distinguished.

Proposed label table:

`pm25_actual_labels`

| Column Name | Data Type | Description |
|---|---|---|
| `station_id` | STRING | Monitoring station identifier |
| `target_time` | TIMESTAMP | Time of the actual observation |
| `actual_pm25_ug_m3` | FLOAT | Actual PM2.5 value |
| `label_available_at` | TIMESTAMP | Time when the actual label becomes available |

Example:

```json
{
  "station_id": "HN001",
  "target_time": "2026-11-13T09:00:00Z",
  "actual_pm25_ug_m3": 27.2,
  "label_available_at": "2026-11-13T09:15:00Z"
}
```

Proposed handling:

- Late labels must be retained rather than silently discarded.
- Each label must be linked to its corresponding station and target time.
- Previously generated predictions must be retained for later evaluation.
- Model errors should only be calculated when the corresponding actual label becomes available.

The maximum label delay and update mechanism are TBD.

### 3.6. Responsibilities

**Data Pipeline provides:**

- Hourly feature table.
- Feature schema and data types.
- Timestamp information.
- Actual labels when available.
- Data quality information.

**AI requires:**

- Stable feature names and types.
- Historical data for training.
- New feature data for prediction and model updating.
- Actual labels for model evaluation.

**Open questions:**

- Is the prediction horizon one hour or another interval?
- Which features are mandatory?
- How are missing observations handled?
- How are late labels delivered?
- Where will the feature table be stored and accessed?

---

## 4. Model Interface Contract

**Direction:** AI → MLOps

**Purpose:** Define how the AI team hands trained models to MLOps for registration, deployment, and serving.

### 4.1. Training Interface

Proposed function signature:

```python
def train_model(train_data, config=None):
    """
    Train a PM2.5 forecasting model.

    Args:
        train_data: Training dataset containing features and target.
        config: Optional training configuration.

    Returns:
        A result containing the trained model and evaluation metrics.
    """
    pass
```

Expected inputs:

- Training features.
- Target values.
- Optional model parameters.

Expected outputs:

- Trained model.
- Training parameters.
- Evaluation metrics.
- Training metadata.

### 4.2. Prediction Interface

Proposed function signature:

```python
def predict(model, input_data):
    """
    Generate PM2.5 predictions.

    Args:
        model: Loaded trained model.
        input_data: Feature data for prediction.

    Returns:
        Prediction results.
    """
    pass
```

Expected prediction output:

| Field | Data Type | Description |
|---|---|---|
| `station_id` | STRING | Monitoring station |
| `target_time` | TIMESTAMP | Forecast target time |
| `predicted_pm25_ug_m3` | FLOAT | Predicted PM2.5 value |
| `model_version` | STRING | Model version used |

The final function signatures and input/output schema must be confirmed by AI and MLOps.

### 4.3. Model File Format

Proposed standard:

**MLflow Model format**

The AI team should provide a model that can be logged and loaded using MLflow.

The model package should include:

- Model artifact.
- Model signature.
- Input example.
- Required preprocessing components.
- Model parameters and metadata.
- Evaluation results.

The exact MLflow flavor depends on the model implementation.

Standalone `.pkl` or `.joblib` files may be used for local experiments but should not be the only agreed integration interface.

### 4.4. MLflow Registration

Proposed registered model name:

`pm25-forecasting`

Suggested experiment name:

`pm25_forecasting`

Expected workflow:

1. AI trains a candidate model.
2. Training parameters and metrics are logged to MLflow.
3. Model artifacts are logged.
4. The model is registered under `pm25-forecasting`.
5. MLOps can load the registered model for validation and serving.
6. The approved model is assigned the production alias.

Example MLflow model URI:

```text
models:/pm25-forecasting/1
```

Example alias:

```text
models:/pm25-forecasting@champion
```

### 4.5. Model Metadata

Each registered model should provide:

| Metadata | Description |
|---|---|
| `model_name` | Registered model name |
| `model_version` | Model version |
| `training_timestamp` | Training time |
| `dataset_version` | Training dataset version |
| `model_strategy` | Periodic, Drift-triggered, or Continuous |
| `feature_schema_version` | Input feature schema |
| `mae` | Mean Absolute Error |
| `rmse` | Root Mean Squared Error |
| `r2` | R-squared score |

### 4.6. Responsibilities

**AI provides:**

- Training and prediction functions.
- Model artifact.
- Input/output schema.
- Model evaluation results.
- Model metadata.

**MLOps provides:**

- MLflow tracking and registry.
- Model version management.
- Model loading and serving.
- Deployment and rollback mechanisms.

**Open questions:**

- Will AI or MLOps own the model registration operation?
- Which MLflow flavor will be used?
- What metadata is mandatory?
- How will candidate models be promoted?
- What are the acceptance criteria for deployment?

---

## 5. Metrics Contract

**Direction:** MLOps → All Teams

**Purpose:** Define consistent metric names, types, units, and meanings for model monitoring and experimental comparison.

### 5.1. Prediction Error Metrics

These metrics evaluate model predictions against actual PM2.5 measurements.

| Metric Name | Type | Unit | Description |
|---|---|---|---|
| `prediction_mae` | Gauge | µg/m³ | Mean absolute prediction error |
| `prediction_rmse` | Gauge | µg/m³ | Root mean squared prediction error |

Rules:

- Calculate errors only when actual labels are available.
- Use the agreed evaluation window.
- Include the model version and update strategy in the metric labels.
- Do not treat unavailable labels as zero.

### 5.2. Drift Metrics and Alerts

| Metric Name | Type | Unit | Description |
|---|---|---|---|
| `drift_alerts_total` | Counter | Events | Total detected drift alerts |
| `drift_score` | Gauge | Score | Drift score for the monitored feature |

Drift alert information should include:

- Feature name.
- Drift detection method.
- Drift score.
- Detection timestamp.
- Drift type.
- Model version, when applicable.

### 5.3. Model Retraining Metrics

| Metric Name | Type | Unit | Description |
|---|---|---|---|
| `model_retrain_events_total` | Counter | Events | Total model retraining or updating events |
| `model_retrain_duration_seconds` | Histogram | Seconds | Duration of each update operation |

Each retraining event should record:

- Model name.
- Previous model version.
- New model version, if successful.
- Update strategy.
- Update trigger.
- Start and end timestamps.
- Training status.

### 5.4. Resource Usage Metrics

| Metric Name | Type | Unit | Description |
|---|---|---|---|
| `model_update_cpu_seconds_total` | Counter | CPU seconds | CPU time consumed by model updating |
| `process_resident_memory_bytes` | Gauge | Bytes | Current process memory usage |

Resource metrics should be recorded consistently across the three updating strategies.

### 5.5. Common Metric Labels

The following labels are proposed:

| Label | Description |
|---|---|
| `model_name` | Model identifier |
| `model_version` | Model version |
| `strategy` | Updating strategy |
| `feature_name` | Monitored feature, when applicable |
| `method` | Drift detection method, when applicable |

Avoid using high-cardinality labels such as unique request IDs.

### 5.6. Responsibilities

**MLOps provides:**

- Metric collection and exposure.
- Monitoring dashboards.
- Drift and retraining event tracking.
- CPU and memory measurements.
- Consistent metric naming and units.

**AI requires:**

- Model error metrics.
- Drift information.
- Retraining event information.
- Results for experimental comparison.

**Data Pipeline requires:**

- Data pipeline and data quality monitoring.
- Information about missing or delayed data.
- Visibility into data delivery and processing status.

**Open questions:**

- What is the agreed evaluation window?
- How often are prediction errors calculated?
- Which drift methods and scores are exposed?
- How are retraining failures recorded?
- Are CPU and memory measured per process, container, or experiment?

---

## 6. Mock and Sample Data

All teams should be able to develop independently using sample data or mock implementations.

Suggested files:

```text
data/
└── sample/
    ├── feature_sample.csv
    ├── labels_sample.csv
    ├── prediction_sample.json
    ├── drift_event_sample.json
    └── metrics_sample.json
```

Suggested mock implementations:

```text
models/
├── train.py
├── predict.py
└── mock_model.py
```

### Development Rules

**Data Pipeline:**

- Provides sample feature and label data.
- Maintains the agreed schema.

**AI:**

- Uses sample feature data for training and prediction development.
- Provides mock predictions and drift events when needed.

**MLOps:**

- Uses a mock model to test MLflow and FastAPI.
- Uses mock metrics to develop monitoring dashboards.

When real components become available, they should replace the mock implementations without changing the agreed interfaces unless all affected teams approve the change.

---

## 7. Team Approval

This document must be reviewed and approved by at least one member from each team.

| Team | Reviewer | Approval Status |
|---|---|---|
| Data Pipeline | TBD | Pending |
| AI | TBD | Pending |
| MLOps | TBD | Pending |

Approval must be provided through GitHub Pull Request reviews.

---

## 8. Contract Change Management

Any change to an agreed interface must follow this process:

1. Describe the requested change.
2. Identify affected teams.
3. Discuss the proposed change.
4. Record the decision in this document.
5. Update the relevant implementation or mock.
6. Submit a Pull Request.
7. Obtain approval from affected teams.

No team should independently modify an agreed interface without notifying the affected teams.

---

## 9. Definition of Done

This contract task is complete when:

- Feature Table Contract is defined.
- Model Interface Contract is defined.
- Metrics Contract is defined.
- All teams can develop using sample data or mock implementations.
- `CONTRACTS.md` is merged into the main branch.
- At least one member from Data Pipeline, AI, and MLOps has approved the Pull Request.

**End of Document**