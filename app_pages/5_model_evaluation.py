import streamlit as st
import pandas as pd
from src.data_management import load_evaluation_metrics
from src.data_processing import (classification_report_table,
                                 hyperparameter_summary)
from src.charts import plot_confusion_matrix, plot_feature_importance
from src.model import pipeline_steps

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Cancellation Prediction Model Evaluation")
st.info("""
This page describes and evaluates the performance of the ML model
 generating the cancellation predictions behind CancelProtect
""")

st.success(
    "**Model meets its target.** The final model achieves 86% "
    "recall on the Cancelled class, exceeding the 80% target set"
    " out in the ML Buiness Case."
)

metric_container = st.container(border=False)
metric_container.header("Test set results for the cancelled class",
                        text_alignment="center")
col1, col2, col3, col4 = metric_container.columns(4)
with col1:
    st.metric(label="Recall",
              value="0.87",
              delta="+0.07 vs target",
              border=True)

with col2:
    st.metric(label="Precision",
              value="0.80",
              border=True,
              height="stretch")

with col3:
    st.metric(label="Accuracy",
              value="0.87",
              border=True,
              height="stretch")

with col4:
    st.metric(label="F1",
              value="0.83",
              border=True,
              height="stretch")

with st.expander(label="Prediction Pipeline"):
    st.info("The final machine learning pipeline"
            " consists of 2 pipelines combined:")

    preprocessing, model = pipeline_steps()
    st.markdown("### Preprocessing Pipeline:")

    # Display separately to avoid truncation
    pipeline_text = "Pipeline(\n"

    for name, transformer in preprocessing.steps:
        pipeline_text += f"    ('{name}', {repr(transformer)}),\n"

    pipeline_text += ")"

    st.code(pipeline_text, language="python")
    pipeline_steps_explained = pd.DataFrame({
            "Step": ["DropFeatures", "FunctionTransformer",
                     "ArbitraryNumberImputer", "CategoricalImputer",
                     "Winsorizer", "RareLabelEncoder", "OrdinalEncoder",
                     "MonthEncoder", "OneHotEncoder"],
            "Purpose": ["Removes features not used by the final model",
                        "Replaces 'Undefined' meal type with 'SC'",
                        "Fills missing 'agent' values with '0'",
                        "Fills missing 'country' values with the most"
                        " common value",
                        "Handles extreme outlier values",
                        "Combines infrequent country values into 'Other'"
                        " to handle unseen categories at test time",
                        "Replaces country codes with unique numeric values",
                        "Converts month column into 12 binary columns the"
                        " model can use",
                        "Converts remaining categorical values into binary"
                        " columns the model can use"
                        ]
        })
    st.table(pipeline_steps_explained, width="content")
    st.markdown("### Model:")
    st.code(model, language="python")

results_container = st.container(border=True)
results_container.header("Model Performance")
selection = results_container.pills("Please Choose:",
                                    ["Train Set", "Test Set"],
                                    default="Train Set")

evaluation_results = load_evaluation_metrics()
split = "train" if selection == "Train Set" else "test"

cm = evaluation_results[split]["confusion_matrix"]
col5, col6, col7 = results_container.columns([0.2, 0.6, 0.2])
with col6:
    st.markdown("### Confusion Matrix")
    st.pyplot(plot_confusion_matrix(
        tn=cm["tn"], fp=cm["fp"], fn=cm["fn"], tp=cm["tp"],
        title=selection
    ))

    st.markdown("### Classification Report")
    st.dataframe(
        classification_report_table(
            evaluation_results[split]["classification_report"]),
        column_config={
            "_index": st.column_config.Column(width="medium"),
            "precision": st.column_config.NumberColumn(format="%.2f"),
            "recall": st.column_config.NumberColumn(format="%.2f"),
            "f1-score": st.column_config.NumberColumn(format="%.2f"),
        },
    )

results_container.markdown(
    "The model was evaluated on both the training and test sets to check "
    "whether performance holds up on data it hasn't seen before. Test recall "
    "for the Cancelled class (0.87) is close to train recall (0.90) — a "
    "3-point gap — and test accuracy (0.87) sits 2 points below train "
    "accuracy (0.89). This is a modest, expected level of overfitting,"
    " the model generalises reasonably well to new bookings, "
    "and its performance on the test set is what should be trusted as a "
    "realistic estimate of how it will behave in production."
)

results_container.success("""
    As a secondary metric, precision was identified in the ML business case
     as needing to be above 0.85 for the Not Cancelled class for the model
     to be considered successful.

    Precision for the Not Cancelled class is 0.92, this condidtion is also
     met 
    """)


with st.expander(label="Model Selection and Tuning"):
    st.info("The binary classification task (Cancelled vs Not Cancelled)"
            " suggested a tree based algorithm. Several options "
            "were tested using 5-fold cross validation with recall as the"
            " primary metric since the main focus is catching cancellations"
            " and the cost of false alarms is low")

    st.markdown("""
        :blue-badge[Model Selection:]

        The results of the cross-validation testing showed that
         DecisionTreeClassifier, RandomForestClassifier and XGBClassifier were
         all close to the target recall value of 0.8 while
         GradientBoostingClassifier and LogisticRegression (added to provide
         a baseline) were discounted as they failed to come close to target.
    """)

    st.markdown("""
        :green-badge[Class Imbalance Handling:]

        Class weighting was chosen over resampling techniques such as SMOTE
         for two main reasons: several features are one-hot encoded
         categoricals, and SMOTE's interpolation approach can produce
         synthetic samples with no valid real-world interpretation for these;
         and the observed class imbalance (~63/37) was moderate rather than
         severe, a regime where weighting is generally sufficient without the
         added pipeline complexity resampling introduces. All candidate models
         (DecisionTree, RandomForest, XGBoost) support weighting natively,
         keeping the pipeline simpler and avoiding the risk of
         resampling-related data leakage between train and test folds.
    """)

    st.markdown("""
        DecisionTree, RandomForest, and XGBoost were carried forward from
         baseline comparison for class-weighting trials. Unlike the other
         two, DecisionTree did not benefit from weighting — mean recall
         fell slightly (0.797 → 0.796) rather than improving, and cross-fold
         rising from 0.003 to 0.004). RandomForest and XGBoost both improved
         recall and stability (std_score) and cleared the 0.80
         target with tighter, more consistent spreads. DecisionTree was
         therefore dropped at this stage, while the other two proceeded to
         hyperparameter tuning.
    """)

    st.markdown("""
        :violet-badge[Hyperparameter Tuning:]

        The weighted models were tested using cross-validation score with
         a range of hyperparameters to see if any further improvement could
         be found:
    """)

    st.dataframe(hyperparameter_summary(),
                 hide_index=True,
                 width="stretch")

    st.caption(
        "Note: individual sweeps test one parameter at a time with others"
        " held at default. The final combined grid search retested top"
        " candidates together, since hyperparameters can interact."
    )

    st.success("The tuning options were retested via the same 5-fold cross"
               " validation grid search method and the top performing model"
               " was **XGBClassifier** with `scale_pos_weight=<neg_count/pos_"
               "count>`, `learning_rate=0.2`, `max_depth=8` `and min_child_"
               "weight=3` producing a mean recall of 0.864")

with st.expander(label="Feature Importance"):
    col8, col9, col10 = st.columns([0.1, 0.8, 0.1])
    with col9:
        plot_feature_importance()

    st.markdown("""
    Feature importance is fairly evenly distributed across the model's
     inputs, with no single feature dominating the prediction. `market_
    segment_Online TA` (0.168) and `required_car_parking_spaces` (0.144) are
     the leading predictors, followed by`previous_cancellations` (0.104) -
     together these three account for nearly half of total importance.

    The remaining top-15 features show a gradual, expected decline in
     importance (0.059 down to 0.013), reflecting a model that draws on a
     broad mix of booking behaviour (`previous_cancellations`, `total_of_
    special_requests`), booking channel (`market_segment_*`, `distribution
    _channel_Direct`, `agent`), and customer type (`customer_type_Transient*`)
     rather than relying heavily on any single variable.

    This balanced profile supports the model's predictive performance not being
    dependent on any one feature, making it more robust to changes in the
     underlying booking data over time.
    """)

    st.warning("""
    ### Deposit Type Ablation Study:
    In the initial v1 model, `deposit_type_Non Refund` was identified as
     the strongest predictor with an importance of 0.647, 8.5x greater
     than the next-ranked feature (`required_car_parking_spaces`, 0.076).

    Deposit type Non Refund had a cancellation rate of 99% (as discovered in
     the correlation study), and combined with its importance as a predictor,
     raised concerns that the feature may have been acting as a proxy for
     `is_canceled`

    Additionally, there are some concerns as to the derivation of the feature:

    **Dataset description (Antonio, de Almeida & Nunes, 2019):**
    - "Value calculated based on the payments identified for the booking in the
    transaction table (TR) before the booking's arrival or cancellation date."
    - "Non Refund – a deposit was made in the value of the total stay cost."

    This wording suggests that the deposit status may not be known at time of
     booking and as such could actually be a source of data leakage.

    For these reasons, an ablation study was conducted, the model was retrained
     with `deposit_type` removed to assess whether the model would predict as
     well with the uncertain feature removed. The results are as follows:

    |Metric (Cancelled class)|With deposit_type|Without deposit_type|Diff|
    | --- | --- | --- | --- |
    | Precision | 0.80 | 0.80 | 0.00 |
    | Recall | 0.86 | 0.87 | +0.01 |
    | F1-score | 0.83 | 0.83 | 0.00 |
    | Accuracy | 0.87 | 0.87 | 0.00 |

    To confirm that this result was not simply an artifact of a particular
     train/test split, both versions of the model were evaluated using 5-fold
     cross-validation. Although the model without deposit_type showed a very
     slight reduction in mean F1 score (0.02) across the validation folds, the
     held-out test set produced virtually identical precision, recall,
     F1-score and accuracy. These findings suggest that removing deposit_type
     has little practical impact on predictive performance while yielding a
     more balanced feature importance distribution and a more robust,
     interpretable model.

    Given the insignificant impact on model performance and the reasons laid
     out above, the feature `deposit_type` was removed from the final (v2)
     model.
    """)
