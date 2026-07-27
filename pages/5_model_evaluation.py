import streamlit as st
from utils.data_management import load_evaluation_metrics
from utils.data_processing import classification_report_table
from utils.charts import plot_confusion_matrix

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


# 6. Feature importance & the leakage investigation
# As previously scoped — v2 chart as primary visual, ablation before/after table, brief CV confirmation line, cross-reference to Hypothesis Validation H1 rather than re-deriving the stats.

# 7. Limitations / next steps
# Short, from your conclusions.

# 8. Cross-reference footer
# Links to Cancellation Study (PPS) and Hypothesis Validation (H1).