# Model card for Essay Grading

Jump to section:

- [Model card for Essay Grading](#model-card-for-essay-grading)
  - [Model details](#model-details)
  - [Intended use](#intended-use)
    - [Primary intended uses](#primary-intended-uses)
    - [Primary intended users](#primary-intended-users)
    - [Metrics and model performance measures](#metrics-and-model-performance-measures)
    - [Uncertainties](#uncertainties)
  - [Evaluation data](#evaluation-data)
    - [Datasets](#datasets)
  - [Training data](#training-data)
    - [Risks and harms](#risks-and-harms)

## Model details
_Basic information about the model._

- Problem One of the key roadblocks to advancing school-based curricula focused on critical thinking and analytical skills is the expense associated with scoring tests to measure those abilities.  For example, tests that require essays and other constructed responses are useful tools, but they typically are hand scored, commanding considerable time and expense from public agencies.  So, because of those costs, standardized examinations have increasingly been limited to using “bubble tests” that deny us opportunities to challenge our students with more sophisticated measures of ability.  
- Anna Parandiy
- version 0.0.1
- Text regression model implemented using `autokeras` library

## Intended use

This model should be used by teachers or schools/universities to automatize essays scoring.

### Primary intended uses

Use for grade essays(written in english).

### Primary intended users
Teachers or schools/universities

### Metrics and model performance measures
All performance measures and metrics are available at [wandb](https://wandb.ai/securims/ml-in-prod/reports/Model-report--VmlldzoyNzE5MDI1)


### Uncertainties
Incomplete Coverage of the Domain: model will not check some statements(for example historical facts) so its usage is a little bit limited.

## Evaluation data

Use testing dataset to check if model predictions are correct

### Datasets
Datasets are available at [link](https://www.kaggle.com/c/asap-aes/data)


## Training data

Review section 4.6 of the [model cards paper](https://arxiv.org/abs/1810.03993).


### Risks and harms
Unexpected model behavior(incorrect grading) and missing some incorrect(facts , historical dates, etc.) or hateful information(hate speech, transphobia, etc.).

