# ![CancelProtect Logo](/images/CancelProtect_logo.svg)

Developer: Geraldine Morey ([geraldine-mor](https://www.github.com/geraldine-mor))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/geraldine-mor/cancel-protect)](https://www.github.com/geraldine-mor/cancel-protect)
[![badge](https://img.shields.io/badge/deployment-Heroku-purple)](⚠️)

⚠️ ## How to use this repo ⚠️
1. Fork this repo
2. In your newly created repo click on the green Code button. 
3. Then, from the Codespaces tab, click Create codespace on main.
4. Wait for the workspace to open. (This can take a few minutes).
5. Open a new terminal and `pip3 install -r requirements.txt`
6. Open the jupyter_notebooks directory, and click on the notebook you want to open.
7. Click the kernel button and choose Python Environments.

⚠️ Note that the kernel says Python 3.12.8 as it inherits from the workspace, so it will be Python-3.12.8 as installed by Codespaces. To confirm this, you can use `! python --version` in a notebook code cell. ⚠️

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

The dataset comprises ~119k rows and 32 columns. Each row represents a hotel booking made at one of 2 Portuguese properties owned by the fictional "TCS Hotels". Each column contains a booking attribute.

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

## Project Terms and Jargon
```text
* A customer or guest is the person who will stay at the hotel
* Hotel or property refers to either of the 2 hotels in the dataset
* LOS is length of stay
* OTA is online travel agent
* TA is travel agent, TO is tour operator
* Agent refers to someone who makes the booking on behalf of the guest
* Company refers to a corporate account that books on behalf of their employees or VIPs
* ADR is average daily rate
* Reservation or booking refers to the agreement between guest and property and is also one row of the dataset.

```

## Business Requirements
The revenue manager at TCS hotels has requested actionable insights and data-driven recommendations to help reduce cancellations and inform hotel policy making decisions.

**BR1:** TCS Hotels wants to understand cancellation patterns, trends and guest behaviour across their 2 Portuguese properties in order to identify risk factors and develop more effective cancellation defence strategies.

**BR2:** TCS Hotels wants a machine learning model capable of predicting the likelihood of a booking cancellation, accessed through an operational dashboard that supports the reservations team in three ways: a risk report of upcoming arrivals, individual reservation search and a prospective booking risk assessor.

**BR3:** TCS Hotels wants to identify distinct guest booking segments with meaningfully different cancellation profiles, in order to better understand the composition of their demand and inform targeted retention strategies.


## Hypotheses 
### H1: No deposit bookings cancel more than deposit-secured bookings.
* **Validation:** Chi-Square test on `deposit_type` vs `is_canceled`
* **Visualisation:** Grouped bar chart of cancellation rate by deposit type
* **Expected Outcome:** Confirmed - no financial commitment reduces cancellation friction
* **Evaluation Result:** ⚠️

### H2: Bookings with longer lead times have a higher cancellation rate than last-minute bookings.
* **Validation:** Point-biserial correlation between `lead_time` and `is_canceled`
* **Visualisation:** Violin plot of lead time distribution by cancellation status; histogram with KDE overlay
* **Expected outcome:** Confirmed — longer lead times provide more opportunity for plans to change or to source alternative accommodation
* **Evaluation Result:** ⚠️

### H3: Bookings made through the Online TA market segment have a higher cancellation rate than bookings made through the Direct market segment.
* **Validation:** Chi-square test on `market_segment` vs `is_canceled`
* **Visualisation:** Grouped bar chart of cancellation rate by segment
* **Expected Outcome:** Confirmed - OTAs act as an intermediary and reduce customer loyalty and cancellation friction
* **Evaluation Result:** ⚠️

### H4: Distinct guest booking segments exist within the data. These segments exhibit meaningfully different cancellation rates suggesting cancellation risk is not uniform across the customer base.
* **Validation:** ⚠️ ANOVA/Kruskal-Wallis on cancellation rate across cluster means and/or chi-square on cluster label vs cancellation ⚠️
* **Visualisation:** Bar chart of cancellation rate by cluster, cluster profile summary
* **Expected Outcome:** Confirmed - Clear cluster profiles with distinct cancellation patterns
* **Evaluation Result:** ⚠️

## Business requirements mapping

| Business Requirement | Task | Epic | Actions |
| --- | --- | --- | --- |
| BR1 | Data visualisation and correlation study | E2 | - Inspect the data <br> - Conduct a correlation study to understand how cancellation interacts with other variables<br> - Plot `is_canceled` again the main variables to visualise insights |
| BR2 | Classification | E4 | - Build a binary classifier to predict if a booking will cancel<br> - Evaluate model performance |
| BR3 | Cluster and Data Analysis | E3 | - Build an unsupervised model to cluster the data<br> - Evaluate clusters against `is_canceled` |

### Epics
| Epic | Scope | Business Requirement |
| --- | --- | --- |
| E1: Data collection and preparation | Sourcing, cleaning and engineering the data | All |
| E2: Cancellation analysis | EDA, correlation study, hypothesis testing | BR1 |
| E3: Customer segmentation | Clustering. cluster analysis, profiling | BR3 |
| E4: Predictive modelling | Classification pipeline, tuning, evaluation | BR2 |
| E5: Dashboard development | Streamlit pages | All |
|E6: Deployment | Heroku deployment | All | 

### User Stories
|Target | Expectation | Outcome | Epic | MoSCoW |
| --- | --- | --- | --- | --- |
| As a data practitioner | I want to source and load the raw data in a repeatable process | so that data collection is trasparent and reproducible | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to investigate whether duplicate rows represent genuine bookings or export artefacts | so that I don't discard valid data or retain invalid noise | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a data practitioner | I want to identify and handle outliers and invalid records based on data quality reasoning | so that the model isn't trained on erroneous entries or biased by target-leakage driven cleaning | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a Revenue Manager | I want data quality decisions to be grounded in real-world booking operations | so that cleaning choices reflect how hotels actually take bookings, not just statistical convenience. | 1 | ![Could Have](https://img.shields.io/badge/Could_Have-1d76db) |
| As a data practitioner | I want to derive booking-level features such as `arrival_date` or `LOS` | so that downstream clustering and modelling can use interpretable, relevant variables | 1 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a data practitioner | I want to exclude features only known after a booking's outcome (`reservation_status`, `reservation_status_date`) | so that the model only uses information genuinely available at prediction time | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to clean the dataset | so that the data used for analysis and modelling is accurate, consistent, and free of erroneous or misleading records | 1 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see how cancellation rate varies across deposit type, lead time, and market segment | so that I can spot early candidate risk factors | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to quantify numeric correlations and categorical associations against `is_canceled` | so that visual patterns from EDA are backed by statistical evidence | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want each cancellation hypothesis statistically tested | so that I can trust the conclusions enough to act on them in policy decisions | 2 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to group bookings into distinct segments using unsupervised learning | so that guest demand composition becomes visible beyond raw categorical fields | 3 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to test whether clusters have meaningfully different cancellation rates | so that segmentation is validated as operationally useful, not just statistically distinct | 3 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want each segment described in business-relevant terms | so that I can design retention strategies tailored to how each segment actually behaves | 3 | ![Could Have](https://img.shields.io/badge/Could_Have-1d76db) |
| As a data practitioner | I want to build a classification pipeline predicting `is_canceled` | so that cancellation risk can be estimated for any booking | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want to systematically tune model hyperparameters | so that the final model is defensibly the best-performing option considered | 4 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a Revenue Manager | I want the model's performance clearly evaluated against agreed recall/precision targets | so that I know whether I can trust its risk flags before relying on them operationally | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want the fitted pipeline saved and reloadable | so that the dashboard can serve live predictions without retraining | 4 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a first-time visitor to the dashboard | I want a summary of the project, dataset and business context | so that I understand what the tool does before using it | 5 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) |
| As a reservations agent | I want a labelled list of upcoming arrivals with high cancellation risk | so that I can prioritise proactive outreach to only the highest-risk guests | 5 | ![Should Have](https://img.shields.io/badge/Should_Have-ff8c00)  |
| As a reservations agent | I want to look up an individual reservation's risk score during a live guest interaction | so that I can make an informed decision on the call | 5 | ![Could Have](https://img.shields.io/badge/Could_Have-1d76db) |
| As a reservations agent | I want to input a hypothetical booking's attributes and see its predicted risk | so that I can assess risk before a booking is even confirmed | 5 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see visualised cancellation patterns and segment profiles | so that I can understand demand composition at a glance | 5 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want to see each hypothesis and its statistical outcome in plain language | so that I can trust the analytical conclusions behind the dashboard | 5 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a Revenue Manager | I want clear confirmation of whether the predictive and clustering models meet their stated performance targets | so that I know how much confidence to place in their outputs | 5 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) |
| As a data practitioner | I want the app deployable via Heroku-standard config files | so that TCS Hotels' stakeholders can access the dashboard without a local setup | 6 | ![Must Have](https://img.shields.io/badge/Must_Have-ff0000) | 

⚠️ ![Must Have](https://img.shields.io/badge/Must_Have-ff0000)
![Should Have](https://img.shields.io/badge/Should_Have-ff8c00) 
![Could Have](https://img.shields.io/badge/Could_Have-1d76db)
![Won't Have](https://img.shields.io/badge/Won't_Have-6e6e6e) ⚠️

## ML Business Case
### Predict cancellation
**Classification Model**
* We require an ML model to predict whether a booking will cancel based on historical data
* The target variable - `is_canceled` - is categorical and contains 2 classes suggesting a *classification model*
* The ideal outcome is to provide the revenue manager with reliable insights into their booking to inform retention efforts and overbooking strategies 
* ⚠️ The main model success metric is 80% recall on train and test set
* ⚠️ Precision should be monitored to avoid an inflated risk report and unnecessary man-hours spent chasing safe bookings or unsafe overbooking levels leading to guests being 'walked' on arrival, with the associated reputation damage and should be in the 60-65% range
* ⚠️ F2-score weighting recall x2 against precision 
* ⚠️ The model training data comes from TCS Hotels and contains ~119k rows with 20% to be held back for the test set - ⚠️ features used
* The model output is a flag indicating that a booking will cancel ⚠️ and/or probability of cancellation

### Clustering 
**Clustering Model**
* We require an ML model to cluster similar booking behaviour, an *unsupervised model*
* The ideal outcome is to provide the revenue manager with a clearer picture of market segmentation 
* ⚠️ Minimum silhouette score of 0.50 is the main success metric here 
* ⚠️ Maximum 10 clusters to be considered successful
* The model training data comes from TCS Hotels and contains ~119k rows - ⚠️ features used
* The model output is an additional colum appended to the dataset suggesting a cluster designation per booking

## Dashboard Design
### Page 1: About CancelProtect
* Project background, TCS Hotels business context, and summary of the 3 Business Requirements
* Dataset overview and link to source
* Navigation guide to the remaining pages
* *Business Requirement: BR1, BR2, BR3

### Page 2: CancelProtect
* **Risk Report** — mock-live "at-risk arrivals" table for the next 14 days, with a configurable cancellation-probability threshold slider/widget
* **Reservation Search** — lookup a booking by reservation number and view its individual cancellation risk score
* **Variable Inputs** — form for a prospective booking's attributes, returning a predicted cancellation probability/flag
* *Business Requirement: BR2*

### Page 3: Cancellation Profiling
* Descriptive analytics and plots addressing cancellation patterns across the 2 properties (hotel type, deposit type, lead time, market segment, etc.)
* Cluster segment summary and profiles (linking BR3 findings into a business-facing narrative)
* Textual interpretation of each plot, tied back to BR1/BR3 conclusions
* *Business Requirement: BR1, BR3*

### Page 4: Hypothesis and Validation
* States each hypothesis (H1–H4), validation method used, and final evaluation verdict
* Statistical test results (chi-square, point-biserial, cluster significance test) summarised in plain language for a non-technical stakeholder
* *Business Requirement: BR1, BR3*

### Page 5: Predict Cancel Model Performance
* Model type, training data, and features used
* Confusion matrix and classification report for train and test sets
* Clear statement of whether the model met its stated performance requirement (80% recall, 60–65% precision target)
* Feature importance discussion
* *Business Requirement: BR2*

### Page 6: Cluster Model Performance
* Clustering method, features used, and number of clusters selected
* Silhouette score and cluster evaluation against `is_canceled`
* Clear statement of whether the model met its stated performance requirement (≥0.50 silhouette, ≤10 clusters)
* *Business Requirement: BR3*

## Unfixed Bugs
* You will need to mention unfixed bugs and why they were not fixed. This section should include shortcomings of the frameworks or technologies used. Although time can be a significant variable to consider, paucity of time and difficulty understanding implementation is not a valid reason to leave bugs unfixed.

## Deployment
### Heroku

* The App live link is: https://YOUR_APP_NAME.herokuapp.com/ 
* Set the runtime.txt Python version to a [Heroku-24](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version.
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. At the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.


## Main Data Analysis and Machine Learning Libraries
* Here you should list the libraries you used in the project and provide an example(s) of how you used these libraries.


## Credits 

* In this section, you need to reference where you got your content, media and extra help from. It is common practice to use code from other repositories and tutorials, however, it is important to be very specific about these sources to avoid plagiarism. 
* You can break the credits section up into Content and Media, depending on what you have included in your project. 

### Content 

- The text for the Home page was taken from Wikipedia Article A
- Instructions on how to implement form validation on the Sign-Up page were taken from [Specific YouTube Tutorial](https://www.youtube.com/)
- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/)

### Media

- The photos used on the home and sign-up page are from This Open-Source site
- The images used for the gallery page were taken from this other open-source site



## Acknowledgements (optional)
* Thank the people who provided support through this project.

