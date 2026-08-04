# [![CancelProtect Logo](/images/CancelProtect_logo.svg)](https://cancel-protect-03ac919826b5.herokuapp.com/)

Developer: Geraldine Morey ([geraldine-mor](https://www.github.com/geraldine-mor))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect)
[![badge](https://img.shields.io/badge/deployment-Heroku-purple)](https://cancel-protect-03ac919826b5.herokuapp.com/)

# Link to live site: [CancelProtect](https://cancel-protect-03ac919826b5.herokuapp.com/)

## How to use this repo
1. Fork this repo
2. In your newly created repo click on the green Code button. 
3. Then, from the Codespaces tab, click Create codespace on main.
4. Wait for the workspace to open. (This can take a few minutes).
5. Open a new terminal and `pip3 install -r requirements.txt`
6. Open the jupyter_notebooks directory, and click on the notebook you want to open.
7. Click the kernel button and choose Python Environments.

Note that the kernel says Python 3.12.1 as it inherits from the workspace, so it will be Python-3.12.1 as installed by Codespaces. To confirm this, you can use `! python --version` in a notebook code cell.

## Cloud IDE Reminders

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to _Account Settings_ in the menu under your avatar.
2. Scroll down to the _API Key_ and click _Reveal_
3. Copy the key
4. In the terminal, run `heroku_config`
5. Paste in your API key when asked


You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.


## Dataset Content
As a previous revenue manager, I was interested to apply a deeper data understanding to hospitality data. I found the [hotel booking demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) dataset on [kaggle](https://www.kaggle.com/).
Further investigation led me to an [article](https://www.sciencedirect.com/science/article/pii/S2352340918315191?via%3Dihub) about the dataset describing it in further detail.

The dataset comprises 119,390 rows and 32 columns. Each row represents a hotel booking made at one of 2 Portuguese properties owned by the fictional "TCS Hotels". Each column contains a booking attribute.

| Variable | Meaning | Units |
| --- | --- | --- |
| hotel | Which property was booked | City Hotel or Resort Hotel |
| is_canceled | Whether the booking cancelled or not | 0 for not cancelled, 1 for cancelled |
| lead_time | How many days prior to arrival date the booking was made | 0 - 737 | 
| arrival_date_year | Year in which the booking is due to arrive | 2015 - 2017 |
| arrival_date_month | Month in which the booking is due to arrive | January - December | 
| arrival_date_week_number | Week in the year that the booking is due to arrive in | 1 - 53 | 
| arrival_date_day_of_month | Day of the month that the booking is due to arrive | 1 - 31 |
| stays_in_weekend_nights | How many weekend nights (Saturday or Sunday) the booking will stay in the hotel | 0 - 19 |
| stays_in_week_nights | How many midweek nights (Monday - Friday) the booking will stay in the hotel | 0 - 50 |
| adults | The number of adults on the booking | 0 - 55 |
| children | The number of children on the booking | 0 - 10 |
| babies | The number of babies on the booking | 0 - 10 |
| meal | The meal package that the customer has purchased | BB - Bed and breakfast, HB - Half Board, FB - Full Board, SC - Room Only/Undefined |
| country | Country of origin | 177 unique values ISO 3166-3:2013 format |
| market_segment | The booking demographic described in terms of market segment | Online TA (Travel Agent), Offline TA/TO (Tour Operator), Groups, Direct, Corporate, Complimentary, Aviation, Undefined |
| distribution_channel | The booking channel that the booking came through | TA/TO (Travel Agent/Tour Operator), Direct, Corporate, GDS (Global Distribution System), Undefined |
| is_repeated_guest | Whether the guest has previous bookings with the hotel(s) | 0 - No, 1 - Yes |
| previous_cancellations | How many bookings the guest has cancelled previously | 0 - 26 |
| previous_bookings_not_canceled | how many bookings the guest has that were not cancelled | 0 - 72 |
| reserved_room_type | Code of room type reserved - anonymised into alphanetical categories | A - H, P, L |
| assigned_room_type | Code of room type reserved - anonymised into alphanetical categories | A - I, K | 
| booking_changes | Number of amendments made to the booking prior to check-in or cancellation | 0 - 21 |
| deposit_type | Payments made on the booking transaction table prior to arrival or cancellation date | No Deposit - no payment received, Non Refund - payments equal to or exceeding the total cost of stay, Refundable - payments less than the total cost of stay but higher than 0 |
| agent | Travel agency ID | 1 - 535 |
| company | Company ID | 6 - 543 |
| days_in_waiting_list | How long the booking was in the waiting list before confirmed to the customer | 0 - 391 |
| customer_type | Another breakdown of booking demographics based on the type of booking | Contract - booking has an associated allotment or contract, Group - booking is associated with a group booking, Transient - the booking has no associations to other bookings, Transient-Party - the booking is transient but associated with at least 1 other booking |
| adr | The sum of all payments received divided by the total nights stayed | -6.38 - 5400 |
| required_car_parking_spaces | How many carpark spaces the booking has requested | 0 - 8 |
| total_of_special_requests | How many special requests the guests have made | 0 - 5 |
| reservation_status | The final status of the reservation | Canceled - booking cancelled by the customer, Check-Out - customer stayed and has departed, No-Show - customer did not stay and did not cancel the booking |
| reservation_status_date | The date upon which the booking was last amended | 17/10/2014 - 14/09/2017 |

### Data Limitations
* The data has no unique identifiers such as booking or customer ID causing ambiguity in the nature of duplicate rows
* `customer_type`, `market_segment` and `distribution_channel` all largely serve similar functions - splitting the booking into demographics - there is some overlap and confusion much to be expected in the hospitality sector
* Weekends defined as Saturday & Sunday is not industry standard, Friday/Saturday weekend designations are more common
* During modelling it became apparent that there was were issues with the variable `deposit_type` and it had to be excluded

## Project Terms and Jargon

* A customer or guest is the person who will stay at the hotel
* Hotel or property refers to either of the 2 hotels in the dataset
* LOS is length of stay in number of nights
* OTA is online travel agent
* TA is travel agent, TO is tour operator
* Agent refers to someone who makes the booking on behalf of the guest
* Company refers to a corporate account with which the booking is associated
* ADR is average daily rate
* Reservation or booking refers to the agreement between guest and property and is also one row of the dataset.

## Business Requirements
The revenue manager at TCS hotels has requested actionable insights and data-driven recommendations to help reduce cancellations and inform hotel policy making decisions.

**BR1:** TCS Hotels wants to understand cancellation patterns, trends and guest behaviour across their 2 Portuguese properties in order to identify risk factors and develop more effective cancellation defence strategies.

**BR2:** TCS Hotels wants a machine learning model capable of predicting the likelihood of a booking cancellation, accessed through an operational dashboard that supports the reservations team with a prospective booking risk assessor.

## Hypotheses 
### H1: No deposit bookings cancel more than deposit-secured bookings.
* **Validation:** Chi-Square test on `deposit_type` vs `is_canceled`
* **Visualisation:** Grouped bar chart of cancellation rate by deposit status
* **Expected Outcome:** Confirmed - no financial commitment reduces cancellation friction
* **Evaluation Result:** Rejected - more than 99% of Non Refund bookings cancel

### H2: Bookings with longer lead times have a higher cancellation rate than last-minute bookings.
* **Validation:** Point-biserial correlation between `lead_time` and `is_canceled`
* **Visualisation:** Grouped bar chart of cancellation rate by lead time band
* **Expected outcome:** Confirmed - longer lead times provide more opportunity for plans to change or to source alternative accommodation
* **Evaluation Result:** Accepted - cancellation rate rises steadily with booking lead time

### H3: Bookings made through the Online TA market segment have a higher cancellation rate than Direct bookings.
* **Validation:** Chi-square test on `market_segment` vs `is_canceled`
* **Visualisation:** Grouped bar chart of cancellation rate by relevant segments
* **Expected Outcome:** Confirmed - OTAs act as an intermediary and reduce customer loyalty and cancellation friction
* **Evaluation Result:** Accepted - Online TAs have a higher cancellation rate than direct bookings

## Business requirements mapping

| Business Requirement | Task | Epic | Actions |
| --- | --- | --- | --- |
| BR1 | Data visualisation and correlation study | E2 | - Inspect the data <br> - Conduct a correlation study to understand how cancellation interacts with other variables<br> - Plot `is_canceled` against the main variables to visualise insights |
| BR2 | Classification | E4 | - Build a binary classifier to predict if a booking will cancel<br> - Evaluate model performance |

### Rationale to map the business requirements to the Data Visualisations and ML tasks
* BR1 is exploratory in nature and best served by visualisation and correlation analysis
* BR2 requires a predictive capability, which necessitates a classification ML task

### Epics
| Epic | Scope | Business Requirement |
| --- | --- | --- |
| E1: Data collection and preparation | Sourcing, cleaning and engineering the data | All |
| E2: Cancellation analysis | EDA, correlation study, hypothesis testing | BR1 |
| E3: Predictive modelling | Classification pipeline, tuning, evaluation | BR2 |
| E4: Dashboard development | Streamlit pages | All |
| E5: Deployment | Heroku deployment | All | 

### User Stories
|Target | Expectation | Outcome | Epic | MoSCoW |
| --- | --- | --- | --- | --- |
| As a data practitioner | I want to source and load the raw data in a repeatable process | so that data collection is trasparent and reproducible | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to investigate whether duplicate rows represent genuine bookings or export artefacts | so that I don't discard valid data or retain invalid noise | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a data practitioner | I want to identify and handle outliers and invalid records based on data quality reasoning | so that the model isn't trained on erroneous entries or biased by target-leakage driven cleaning | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a Revenue Manager | I want data quality decisions to be grounded in real-world booking operations | so that cleaning choices reflect how hotels actually take bookings, not just statistical convenience. | 1 | ![Could Have](https://img.shields.io/badge/Could_Have-1d76db) |
| As a data practitioner | I want to derive booking-level features such as `arrival_date` or `LOS` | so that downstream modelling can use interpretable, relevant variables | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a data practitioner | I want to exclude features only known after a booking's outcome (`reservation_status`, `reservation_status_date`) | so that the model only uses information genuinely available at prediction time | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to clean the dataset | so that the data used for analysis and modelling is accurate, consistent, and free of erroneous or misleading records | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see how cancellation rate varies across deposit type, lead time, and market segment | so that I can spot early candidate risk factors | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to quantify numeric correlations and categorical associations against `is_canceled` | so that visual patterns from EDA are backed by statistical evidence | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want each cancellation hypothesis statistically tested | so that I can trust the conclusions enough to act on them in policy decisions | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to build a classification pipeline predicting `is_canceled` | so that cancellation risk can be estimated for any booking | 3 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to systematically tune model hyperparameters | so that the final model is defensibly the best-performing option considered | 3 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a Revenue Manager | I want the model's performance clearly evaluated against agreed recall/precision targets | so that I know whether I can trust its risk flags before relying on them operationally | 3 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want the fitted pipeline saved and reloadable | so that the dashboard can serve live predictions without retraining | 3 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a first-time visitor to the dashboard | I want a summary of the project, dataset and business context | so that I understand what the tool does before using it | 4 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a reservations agent | I want to input a hypothetical booking's attributes and see its predicted risk | so that I can assess risk before a booking is even confirmed | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see visualised cancellation patterns | so that I can understand demand composition at a glance | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see each hypothesis and its statistical outcome in plain language | so that I can trust the analytical conclusions behind the dashboard | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want clear confirmation of whether the predictive model meets its stated performance targets | so that I know how much confidence to place in their outputs | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want the app deployable via Heroku-standard config files | so that TCS Hotels' stakeholders can access the dashboard without a local setup | 5 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) | 

### Future Features
* Add an unsupervised learning model to assess clusters and develop a clearer understanding of market segmentation
* Add a regression model to predict the cancellation window of a booking predicted to cancel to better inform overbooking policy
* Include synthesised mock 'live' data to allow the dashboard to demonstrate individual reservation lookup and generate a risk report of upcoming likely cancellations

## ML Business Case
### Predict cancellation
**Classification Model**
* We require an ML model to predict whether a booking will cancel based on historical data
* The target variable - `is_canceled` - is categorical and contains 2 classes suggesting a *classification model*
* The ideal outcome is to provide the reservations team with reliable insights into their booking to inform retention efforts and overbooking strategies 
* The main model success metric is **80% recall** on train and test set
* Precision should be monitored to avoid unnecessary man-hours spent following-up safe bookings or unsafe overbooking levels leading to guests being 'walked' on arrival, with the associated reputation damage
* The model is considered a failure if precision for Not Cancelled is less than 85% on train and test set
* The model training data comes from TCS Hotels and contains ~119k rows with 20% to be held back for the test set 
* The model output is a flag indicating that a booking will cancel and probability of cancellation
* Heuristics: Currently, the reservations team has no systematic method for flagging at-risk bookings and relies on ad-hoc judgement.

## Dashboard Design
### Page 1: ℹ️ Cancel Protect Overview
* Project background, TCS Hotels business context
* Expander sections containing the 2 business requirements and the 3 project Hypotheses
* Navigation guide to the remaining pages
* Instructions on how to use the app
* Expander section containing dashboard limitations
* Link to project README
* *Business Requirement: BR1, BR2*
![screenshot of overview page](documentation/pages/cancel_protect_overview.png)

### Page 2: ❓ Cancellation Predictor
* **Variable Inputs** — form for a prospective booking's attributes, returning a cancellation prediction and probability.
* The inputted fields populate a dataframe displayed to to the user when "Predict" is clicked
* Model ready inputs are displayed in an expander section
* *Business Requirement: BR2*
![screenshot of cancellation predictor page](documentation/pages/cancellation_predictor.png)

### Page 3: 📊 Cancellation Study
* Descriptive analytics and plots addressing cancellation patterns across the 2 properties (hotel type, deposit type, lead time, market segment, etc.)
* Textual interpretation of each plot, tied back to BR1 conclusions
* Expander sections for:
    * Cancellation timing & value
    * Correlation study and features of interest
    * Guest behaviour and booking profile
* Summary answering BR1
* *Business Requirement: BR1*
![screenshot of cancellation study page](documentation/pages/cancellation_study.png)

### Page 4: ✅ Hypothesis Validation
* Uses tabs for each hypothesis
* States each hypothesis (H1–H3), validation method used, and final evaluation verdict
* Statistical test results (chi-square, point-biserial) summarised in plain language for a non-technical stakeholder
* Includes the most relevant visual for each to back up the summary
* *Business Requirement: BR1*
![screenshot of hyposthesis validation page](documentation/pages/hypothesis_validation.png)

### Page 5: 🎯 Model Evaluation
* Clear statements of whether the model met its stated performance requirement (80% recall (Cancelled), 85% precision (Not Cancelled))
* Main metrics clearly displayed
* Pipeline steps and final model displayed in expander section
* Confusion matrix and classification report for train and test sets, pills to toggle between train and test
* Model selection and tuning sectin in expander section
* Feature importance discussion in expander session
* *Business Requirement: BR2*
![screenshot of model evaluation page](documentation/pages/model_evaluation.png)

### Page 6: 🏢 Project Conclusion
* Summary of BR1 findings and BR2 model outcome
* Outcome of all 3 hypotheses
* Business recommendations arising from the analysis
* Project limitations and future work
* *Business Requirement: BR1, BR2*
![screenshot of conclusion page](documentation/pages/project_conclusion.png)

## Validation and Testing
All python pages were validated using the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com/)
| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| app_pages | [1_overview.py](https://github.com/geraldine-mor/cancel-protect/blob/main/app_pages/1_overview.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app_pages/1_overview.py) | ![screenshot of validation result](documentation/validation/overview_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/9aeb48d4149c152d7e0e706bde1ae47b4a1ae8da) |
| app_pages | [2_cancel_predict](https://github.com/geraldine-mor/cancel-protect/blob/main/app_pages/2_cancel_predict.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app_pages/2_cancel_predict.py) | ![screenshot of validation result](documentation/validation/cancel_predict_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a226ea02df746e6a129ef9958b2af75d528c1649) |
| app_pages | [3_cancellation_study](https://github.com/geraldine-mor/cancel-protect/blob/main/app_pages/3_cancellation_study.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app_pages/3_cancellation_study.py) | ![screenshot of validation result](documentation/validation/cancellation_study_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a226ea02df746e6a129ef9958b2af75d528c1649) |
| app_pages | [4_hypothesis_validation](https://github.com/geraldine-mor/cancel-protect/blob/main/app_pages/4_hypothesis_validation.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app_pages/4_hypothesis_validation.py) | ![screenshot of validation result](documentation/validation/hypothesis_validation_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/91e90e6685b39176bd35b9af43787a255adcf0e3) |
| app_pages | [5_model_evaluation](https://github.com/geraldine-mor/cancel-protect/blob/main/app_pages/5_model_evaluation.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app_pages/5_model_evaluation.py) | ![screenshot of validation result](documentation/validation/model_evaluation_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/be3df80fd1d6094b6ef7c80fea7b7300f9002f4a) |
| src | [charts](https://github.com/geraldine-mor/cancel-protect/blob/main/src/charts.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/charts.py) | ![screenshot of validation result](documentation/validation/charts_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
| src | [custom_transformers](https://github.com/geraldine-mor/cancel-protect/blob/main/src/custom_transformers.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/custom_transformers.py) | ![screenshot of validation result](documentation/validation/custom_transformers_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
| src | [data_management](https://github.com/geraldine-mor/cancel-protect/blob/main/src/data_management.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/data_management.py) | ![screenshot of validation result](documentation/validation/data_management_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
| src | [data_processing](https://github.com/geraldine-mor/cancel-protect/blob/main/src/data_processing.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/data_processing.py) | ![screenshot of validation result](documentation/validation/data_processing_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
| src | [input_processing](https://github.com/geraldine-mor/cancel-protect/blob/main/src/input_processing.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/input_processing.py) | ![screenshot of validation result](documentation/validation/input_processing_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
| src | [model](https://github.com/geraldine-mor/cancel-protect/blob/main/src/model.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/src/model.py) | ![screenshot of validation result](documentation/validation/model_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/a133c5748d333dd7a3ea9638c97b2b9dc4fc9a32) |
|  | [app](https://github.com/geraldine-mor/cancel-protect/blob/main/app.py) | [PEP 8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/geraldine-mor/cancel-protect/refs/heads/main/app.py) | ![screenshot of validation result](documentation/validation/app_val_clear.png) | Code changes [commit](https://github.com/geraldine-mor/cancel-protect/commit/6db4946a6e93e7cbc7a989b404abeab95b8e4975) |

### Testing
Manual testing was carried out on the deplyed app on all the main features:

| Feature | Test Performed | Result | Screenshot |
| --- | --- | --- | --- |
| Page Navigation | Clicked through all options | Correct page displayed each time | ![screenshot of navigation](documentation/testing/navigation.png) |
| Expander Sections | Clicked each expander section | Sections expanded as expected | ![screenshot of expander sections](documentation/testing/expanders.png) |
| Conditional Form Fields | Clicked each conditional form field | Additional fields appeared as expected | ![screenshot of conditional form fields](documentation/testing/conditional_form_fields.png) |
| Prediction Form | Completed the form to generate a not cancel result | Not cancel prediction and probability displayed as expected | ![Screenshot of not cancel prediction](documentation/testing/not_cancel.png) |
|  | Completed the form to generate a will cancel result | Will cancel prediction and probability displayed as expected | ![screenshot of cancel prediction](documentation/testing/cancel_result.png) |
| Input Dataframes | Completed the prediction form to view generated dataframes | Input dataframe displayed, model-ready dataframe displayed in expander section as expected | ![screenshot of input dataframes](documentation/testing/dataframe_construction.png) |
| Cancellation Study Chart Selection | Selected all combinations of cancellation rate charts | Correct chart displayed as expected | ![screenshot of chart selection](documentation/testing/chart_selection.png) |
| Cancellation Study Pill Selection | Clicked each of the 3 pills to check that the correct information is displayed | The correct information displayed as expected for each corresponding pill | ![screenshot of pill selsection](documentation/testing/pill_selection.png) |
| Hypthesis Page Tab Selection | Clicked each of the 3 tabs | The correct hypothesis analysis displayed for each corresponding tab | ![screenshot of tab selection](documentation/testing/tab_selection.png) |
| Model Page Pill Selection | Clicked each of the train and test set pills | The correct confusion matrix and classificatin report displayed as expected | ![screenshot of model page pill selection](documentation/testing/pill_selection_model_page.png) |

All Jupyter Notebooks were rerun:

| Notebook | Screenshot | Notes |
| --- | --- | --- |
| [01_data_collection](/jupyter_notebooks/01_data_collection.ipynb) | ![screenshot of data collection notebook](documentation/notebooks/data_collection.png) | Kaggle import not retested due to removal of credentials |
| [02_cancellation_eda](/jupyter_notebooks/02_cancellation_eda.ipynb) | ![screenshot of cancellation eda notebook](documentation/notebooks/cancellation_eda.png) |  |
| [03_rm_analysis](/jupyter_notebooks/03_rm_analysis.ipynb) | ![screenshot of rm analysis notebook](documentation/notebooks/rm_analysis.png) |  |
| [04_cleaning](/jupyter_notebooks/04_cleaning.ipynb) | ![screenshot of cleaning notebook](documentation/notebooks/cleaning.png) |  |
| [05_correlation_study](/jupyter_notebooks/05_correlation_study.ipynb) | ![screenshot of correlation study notebook](documentation/notebooks/correlation_study.png) | 
| [06_feature_exploration](/jupyter_notebooks/06_feature_exploration.ipynb) | ![screenshot of feature exploration notebook](documentation/notebooks/feature_exploration.png) |  |
| [07_feature_engineering](/jupyter_notebooks/07_feature_engineering.ipynb) | ![screenshot of feature engineering notebook](documentation/notebooks/feature_engineering.png) |  |
| [08_predictive_modelling](/jupyter_notebooks/08_predictive_modelling.ipynb) | ![screenshot of predictive modelling notebook](documentation/notebooks/predictive_modelling.png) | The grid cv search with all parameter options for XGBClassifier took 31 mins to run. This cell was not retested ![screenshot of grid cv search](documentation/notebooks/cv_grid_final_model.png) |
| [09_predictive_model_evaluation](/jupyter_notebooks/09_predictive_model_evaluation.ipynb) | ![screenshot of predictive model evaluation notebook](documentation/notebooks/predictive_model_evaluation.png) |

## Agile Development
A kanban board was utilised via [GitHub Projects](https://github.com/users/geraldine-mor/projects/9/views/1) to manage the project.
![screenshot of kanban board](/documentation/project_board.png)

All remaining [open issues](https://github.com/geraldine-mor/cancel-protect/issues) are related to future features
![screenshot of open issues](/documentation/open_issues.png)

## Bugs
Bugs encountered were recorded in [GitHub Issues](https://github.com/geraldine-mor/cancel-protect/issues?q=label%3A%22bug%22)
![screenshot of bugs](/documentation/bugs.png)

## Difference between local and deployed version
This application is deployed on Heroku's Eco dyno tier, which provides shared, non-dedicated CPU resources. As a result, some pages — particularly the Cancellation Study page, which performs multiple statistical computations (PPS scoring, correlation analysis, guest profiling) — may exhibit noticeable latency during use. This has been mitigated as far as possible through function-level caching (st.cache_data) to avoid redundant recomputation; the residual delay reflects the hosting tier's CPU allocation rather than inefficiency in the underlying data pipeline.

## Deployment
### Heroku

* The App live link is: https://cancel-protect-03ac919826b5.herokuapp.com/
* Set the .python-version to 3.12
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. At the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.

## Main Data Analysis and Machine Learning Libraries
The project uses the following Python libraries for data analysis, exploratory data analysis, feature engineering, model development, evaluation, and application deployment:
| Library | Use |
| --- | --- |
| [![badge](https://img.shields.io/badge/Pandas-grey?logo=pandas&logoColor=150458)](https://pandas.pydata.org/docs/index.html) | Used for data loading, manipulation, cleaning, and preparation of datasets. DataFrames were used throughout the project for exploratory analysis and preprocessing. |
| [![badge](https://img.shields.io/badge/NumPy-grey?logo=numpy&logoColor=013243)](https://numpy.org/) | Used for numerical operations and efficient handling of arrays and mathematical transformations during data preparation. |
| [![badge](https://img.shields.io/badge/matplotlib-grey)](https://matplotlib.org/stable/) |  Used to create static data visualisations, including plots used during exploratory data analysis and model evaluation. |
| [![badge](https://img.shields.io/badge/seaborn-grey)](https://seaborn.pydata.org/index.html) | Used for statistical visualisations such as distribution plots, correlation heatmaps, and analysis of relationships between variables. |
| [![badge](https://img.shields.io/badge/YData-Profiling-grey)](https://docs.profiling.ydata.ai/latest/) |  Used to generate automated exploratory data analysis report, helping identify dataset characteristics, missing values, distributions, and potential data quality issues. |
| [![badge](https://img.shields.io/badge/SciPy-grey?logo=scipy&logoColor=8CAAE6)](https://scipy.org/) | Used to create a point-biserial test for lead_time vs is_canceled |
| [![badge](https://img.shields.io/badge/PPScore-grey)](https://pypi.org/project/ppscore/) | Used to analyse relationships between variables and identify features with predictive value for the target variable. |
| [![badge](https://img.shields.io/badge/Pingouin-grey)](https://pingouin-stats.org/) | Used to create a chi-square test for hypotheses 1 & 3 |
| [![badge](https://img.shields.io/badge/Feature-engine-grey)](https://feature-engine.trainindata.com/en/1.8.x/index.html) |  Used for feature engineering and preprocessing tasks, including transforming and preparing variables for machine learning models. |
| [![badge](https://img.shields.io/badge/Scikit-learn-grey?logo=scikitlearn&logoColor=F7931E)](https://feature-engine.trainindata.com/en/1.8.x/index.html) | Used for machine learning workflow components including model selection, pipeline, preprocessing, model evaluation metrics, and supporting model development. |
| [![badge](https://img.shields.io/badge/XGBoost-grey)](https://xgboost.readthedocs.io/en/stable/) | Used to train the machine learning model and generate predictions using gradient boosting techniques. |
| [![badge](https://img.shields.io/badge/Streamlit-grey?logo=streamlit&logoColor=FF4B4B)](https://docs.streamlit.io/) | Used to develop the interactive web application interface, allowing users to interact with the trained model and view predictions. |
| [![badge](https://img.shields.io/badge/Kaggle-grey?logo=kaggle&logoColor=20BEFF)](https://www.kaggle.com/) | Used to access and download the project dataset from Kaggle. |

## Credits 

### Content 

| Source | Use |
| --- | --- |
| [Hotel Booking Demand (Kaggle)](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) | Project dataset |
| [Antonio, de Almeida & Nunes (2019), *Hotel booking demand datasets*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/) | Consulted to clarify the derivation of the `deposit_type` variable during feature importance analysis and the resulting ablation study (see [09_predictive_model_evaluation](/jupyter_notebooks/09_predictive_model_evaluation.ipynb)) |
| [ScienceDirect article on the dataset](https://www.sciencedirect.com/science/article/pii/S2352340918315191?via%3Dihub) | Background reading on dataset structure and origin, referenced in Dataset Content |
| [Gignac & Szodorai (2016), effect size benchmarks](https://www.sciencedirect.com/science/article/abs/pii/S0191886916308194) | Used to contextualise the point-biserial correlation effect size for Hypothesis 2, as an alternative to Cohen's stricter conventions |
| [peterstatistics.com — Effect Size (Nominal/Nominal)](https://peterstatistics.com/CrashCourse/3-TwoVarUnpair/NomNom/NomNom-2c-Effect-Size.html) | Referenced for interpreting Cramer's V effect sizes in the Chi-Square tests for Hypotheses 1 and 3 |
| [Code Institute — Churnometer walkthrough project](https://github.com/Code-Institute-Solutions/churnometer) | This project was heavily influenced byt the Churnometer walkthrough project. The `ModelComparison` class used for cross-validated model comparison in [08_predictive_modelling](/jupyter_notebooks/08_predictive_modelling.ipynb) was adapted from this walkthrough project as was the `evaluate_missing_data()` function in [04_cleaning](/jupyter_notebooks/04_cleaning.ipynb) |
| [PEP8 CI Python Linter](https://pep8ci.herokuapp.com/) | Used to validate PEP8 compliance across all Python files (see [Validation and Testing](#validation-and-testing)) |

### Media

- The project logo was created in collaboration with [Claude AI](https://claude.ai)

## AI Use

Generative AI tools ([Claude](claude.ai) and [ChatGPT](chatgpt.com)) were used selectively during this project as guidance and problem-solving aids. Copilot remained deactivated throughout. Specific uses are outlined below:

* **Planning:** I used the LLMs to generate user stories, workflows and plan out next steps to follow.
* **Tool susggestions:** Throughout the project I asked the LLMs to suggest appropriate methods, attributes, libraries etc that I could use to solve a problem rather than displaying code solutions enabling me to search the appropriate documentation directly.
* **Code review, debugging and troubleshooting:** Claude and ChatGPT were used extensively as a debugging aid throughout the project development, AI was used to reason through possible causes and validate fixes.
* **Assessment criteria review:** Claude was used during the project to cross-check completed work (README sections, notebooks, and dashboard pages) against the Code Institute assessment criteria, helping identify gaps such as missing sections or inconsistencies between the README and the deployed dashboard before submission.
* **Minor code formatting:** ChatGPT was used to reformat a markdown hyperparameter comparison table into a Python dictionary/DataFrame structure (`hyperparameter_summary()` in `src/data_processing.py`) to avoid line-length issues.
* **Media generation:** Claude AI was used in collaboration with the developer to generate the CancelProtect logo.
* **Docstrings:** I used ChatGPT to assist in the generation of docstrings for the Python functions.
* **Conclusion Page:** Claude AI assisted in pulling together all the main points from previous pages into a single project conclusion.

**Examples**
![screenshot of AI use example](/documentation/ai/ai_example_1.png)
![screenshot of AI use example](/documentation/ai/ai_example_2.png)
![screenshot of AI use example](/documentation/ai/ai_example_3.png)

## Acknowledgements
* I would like to thank my partner Niall for his support and for picking up my duties so that I could produce this project.
* I would like to thank Marko Tot my Code Institute facilitator.
* I would also like to thank my mentor Marcel for his help and encouragement.

