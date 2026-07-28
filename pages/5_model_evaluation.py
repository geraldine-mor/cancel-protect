import streamlit as st
import pandas as pd
from utils.data_management import load_evaluation_metrics
from utils.data_processing import classification_report_table
from utils.charts import plot_confusion_matrix, plot_feature_importance
from utils.model import pipeline_steps

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
metric_container.header("Test set results for the cancelled class", text_alignment="center")
col1, col2, col3, col4 = metric_container.columns(4)
with col1:
    st.metric(label="Recall",
              value="0.86",
              delta="+0.06 vs target",
              border=True)

with col2:
    st.metric(label="Precision",
              value="0.79",
              border=True,
              height="stretch")

with col3:
    st.metric(label="Accuracy",
              value="0.86",
              border=True,
              height="stretch")

with col4:
    st.metric(label="F1",
              value="0.82",
              border=True,
              height="stretch")

with st.expander(label="Prediction Pipeline"):
    st.info("The final machine learning pipeline consists of 2 pipelines combined:")

    preprocessing, model = pipeline_steps()
    st.markdown("### Preprocessing Pipeline:")

    # Display separately to avoid truncation
    pipeline_text = "Pipeline(\n"

    for name, transformer in preprocessing.steps:
        pipeline_text += f"    ('{name}', {repr(transformer)}),\n"

    pipeline_text += ")"

    st.code(pipeline_text, language="python")
    pipeline_steps_explained = pd.DataFrame({
            "Step": ["DropFeatures", "FunctionTransformer", "ArbitraryNumberImputer",
                     "CategoricalImputer", "Winsorizer", "RareLabelEncoder",
                     "OrdinalEncoder", "MonthEncoder", "OneHotEncoder"],
            "Purpose": ["Removes features not used by the final model",
                        "Replaces 'Undefined' meal type with 'SC'",
                        "Fills missing 'agent' values with '0'",
                        "Fills missing 'country' values with the most common value",
                        "Handles extreme outlier values",
                        "Combines infrequent country values into 'Other' to handle"
                        " unseen categories at test time",
                        "Replaces country codes with unique numeric values",
                        "Converts month column into 12 binary columns the model can use",
                        "Converts remaining categorical values into binary columns the model"
                        " can use"
                        ]
        })
    st.table(pipeline_steps_explained, width="content")
    st.markdown("### Model:")
    st.code(model, language="python")

    

results_container = st.container(border=True)
results_container.header("Model Performance")
selection = results_container.pills("Please Choose:", ["Train Set", "Test Set"], default="Train Set")

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
            })

results_container.markdown(
    "The model was evaluated on both the training and test sets to check "
    "whether performance holds up on data it hasn't seen before. Test recall "
    "for the Cancelled class (0.86) is close to train recall (0.90) — a "
    "4-point gap — and test accuracy (0.86) sits 3 points below train "
    "accuracy (0.89). This is a modest, expected level of overfitting,"
    " the model generalises reasonably well to new bookings, "
    "and its performance on the test set is what should be trusted as a "
    "realistic estimate of how it will behave in production."
)


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
         all close to the target recall value of 0.8 while GradientBoostingClassifier
         and LogisticRegression (added to provide a baseline) were discounted as they
         failed to come close to target.
    """)

    st.markdown("""
        :green-badge[Class Imbalance Handling:]

        Class weighting was chosen over resampling techniques such as SMOTE
         for two main reasons: several features are one-hot encoded categoricals,
         and SMOTE's interpolation approach can produce synthetic samples with no
         valid real-world interpretation for these; and the observed class imbalance
         (~63/37) was moderate rather than severe, a regime where weighting is
         generally sufficient without the added pipeline complexity resampling
         introduces. All candidate models (DecisionTree, RandomForest, XGBoost)
         support weighting natively, keeping the pipeline simpler and avoiding
         the risk of resampling-related data leakage between train and test folds.
    """)

    st.markdown("""
        DecisionTree, RandomForest, and XGBoost were carried forward from baseline
         comparison for class-weighting trials. Unlike the other two, DecisionTree
         did not benefit from weighting — mean recall fell slightly (0.798 → 0.796)
         rather than improving, and cross-fold stability also worsened (std_score
         rising from 0.007 to 0.009). RandomForest and XGBoost both improved
         substantially and cleared the 0.80 target with tighter, more consistent
         spreads. DecisionTree was therefore dropped at this stage, while the other
         two proceeded to hyperparameter tuning.
    """)

    st.markdown("""
        :violet-badge[Hyperparameter Tuning:]

        The weighted models were tested using cross-validation score with a range
         of hyperparameters to see if any further improvement could be found:

        | Model | Hyperparameter | Value |  |  |  |  |  |
        | --- | --- | --- | --- | --- | --- | --- | --- |
        | RandomForest | max_depth | None | 10 | 20 | 30 | 40 |
        |  | *Mean Recall:* | 0.839 | 0.779 | 0.845 | 0.844 | 0.840 |
        |  | n_estimators | 100 | 300 | 500 |
        |  | *Mean Recall:* | 0.839 | 0.840 | 0.840 |
        |  | min_samples_leaf | 1 | 2 | 4 |
        |  | *Mean Recall:* | 0.839 | 0.846 | 0.841 | 
        | XGBoost | max_depth | 3 | 5 | 7 | 10 |
        |  | *Mean Recall:* | 0.851 | 0.859 | 0.860 | 0.859 |
        |  | n_estimators | 100 | 200 | 300 | 500 |
        |  | *Mean Recall:* | 0.860 | 0.861 | 0.859 | 0.852 |
        |  | learning_rate | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 |
        |  | *Mean Recall:* | 0.849 | 0.860 | 0.860 | 0.862 | 0.859 | 0.856 |
        |  | subsample | 0.6 | 0.8 | 1.0 |
        |  | *Mean Recall:* | 0.860 | 0.860 | 0.860 |
        |  | colsample_bytree | 0.6 | 0.8 | 1.0 |
        |  | *Mean Recall:* | 0.860 | 0.862 | 0.860 |
    """)

    st.caption(
        "Note: individual sweeps test one parameter at a time with others held at "
        "default. The final combined grid search retested top candidates together, "
        "since hyperparameters can interact — this is why the joint result "
        "(learning_rate=0.2) differs from, and slightly outperforms, the best "
        "individually-tested value."
    )

    st.success("The tuning options were retested via the same 5-fold cross validation"
           " grid search method and the top performing model was XGBClassifier with"
           " `scale_pos_weight=<neg_count/pos_count>`, `learning_rate=0.2` and "
           "`n_estimators=200` producing a mean recall of 0.863")

with st.expander(label="Feature Importance"):
    col8, col9, col10 = st.columns([0.1, 0.8, 0.1])
    with col9:
        plot_feature_importance()

    st.markdown("""
    Feature importance is fairly evenly distributed across the model's inputs, with
     no single feature dominating the prediction. `market_segment_Online TA` (0.202)
     and `required_car_parking_spaces` (0.183) are the leading predictors, followed by
    `previous_cancellations` (0.102) — together these three account for roughly half of
    total importance.

    The remaining top-15 features show a gradual, expected decline in importance
    (0.047 down to 0.011), reflecting a model that draws on a broad mix of booking
    behaviour (`previous_cancellations`, `total_of_special_requests`), booking channel
    (`market_segment_*`, `distribution_channel_Direct`, `agent`), and customer type
    (`customer_type_Transient`) rather than relying heavily on any single variable.

    This balanced profile supports the model's predictive performance not being
    dependent on any one feature, making it more robust to changes in the underlying
    booking data over time.
    """)

    st.warning("""
    ### Deposit Type Ablation Study:
    In the initial v1 model, `deposit_type_Non Refund` was identified as the strongest
     predictor with an importance of 0.685, nearly 9x greater than the next-ranked 
     feature.

    Deposit type Non Refund had a cancellation rate of 99% (as discovered in the
     correlation study), and combined with its importance as a predictor, raised
     concerns that the feature may have been acting as a proxy for `is_canceled`

    Additionally, there are some concerns as to the derivation of the feature:
    > Value calculated based on the payments identified for the booking in the
     transaction (TR) table before the booking's arrival or cancellation date.  
    > Non Refund – a deposit was made in the value of the total stay cost;
    > — *Hotel booking demand datasets* (Antonio, de Almeida & Nunes, 2019)
    
    This wording suggests that the deposit status may not be known at time of
     booking and as such could actually be a source of data leakage.

    For these reasons, an ablation study was conducted, the model was retrained
     with `deposit_type` removed to assess whether the model would predict as
     well with the uncertain feature removed. The results are as follows:

    | Metric (Cancelled class) | With deposit_type | Without deposit_type | Difference |
    | --- | --- | --- | --- |
    | Precision | 0.80 | 0.79 | -0.01 |
    | Recall | 0.86 | 0.86 | 0.00 |
    | F1-score | 0.83 | 0.82 | -0.01 |
    | Accuracy | 0.87 | 0.86 | -0.01 |

    To confirm this difference wasn't just an artifact of one particular train/test
     split, both versions of the model were also compared using 5-fold
     cross-validation. This confirmed the same result: the small drop in
     performance was consistent across folds, not a one-off, giving 
     confidence that removing `deposit_type` is a stable, reliable choice.    

    Given the insignificant impact on model performance and the reasons laid out
     above, the feature `deposit_type` was removed from the final (v2) model.
    """)
