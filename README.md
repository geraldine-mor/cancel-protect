# ![CancelProtect Logo](/documents/readme_images/CancelProtect_logo.svg)


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
| arrival_date_year | Year in which the booking is due to arrive | 2015 - 2017 (changed to 2023-2025 for the purposes of this project) |
| arrival_date_month | Month in which the booking is due to arrive | January - December | 
| arrival_date_week_number | Week in the year that the booking is due to arrive in | 1 - 53 | 
| arrival_date_day_of_month | Day of the month that the booking is due to arrive | 1 - 31 |
| stays_in_weekend_nights | How many weekend nights (Saturday or Sunday) the booking will stay in the hotel | 0 - 19 |
| stays_in_week_nights | How many midweek nights (Monday - Friday) the booking will stay in the hotel | 0 - 50 |
| adults | The number of adults on the booking | 0 - 55 |
| children | The number of children on the booking | 0 - 10 |
| babies | The number of babies on the booking | 0 - 10 |
| meal | The meal package that the customer has pruchased | BB - Bed and breakfast, HB - Half Board, FB - Full Board, SC - Room Only/Undefined |
| country | Country of origin | 177 unique values ISO 3155-3:2013 format |
| market_segment | The booking demographic described in terms of market segment | Online TA (Travel Agent), Offline TA/TO (Tour Operator), Groups, Direct, Corporate, Complimentary, Aviation, Undefined |
| distribution_channel | The booking channel that the booking came through | TA/TO (Travel Agen/Tour Operator), Direct, Corporate, GDS (Global Distribution System), Undefined |
| is_repeated_guest | Whether the guest has previous bookings with the hotel(s) | 0 - No, 1 - Yes |
| previous_cancellations | How many bookings the guest has cancelled prevously | 0 - 26 |
| previous_bookings_not_cancelled | how many bookings the guest has that were not cancelled | 0 - 72 |
| reserved_room_type | Code of room type reserved - anonymised into alphanetical categories | A - H, P, L |
| assigned_room_type | Code of room type reserved - anonymised into alphanetical categories | A - I, K | 
| booking_changes | Number of amendments made to the booking prior to check-in or cancellation | 0 - 21 |
| deposit_type | Payments made on the booking transaction table prior to arrival or cancellation date | No Deposit - no payment received, Non Refund - payments equal to or exceeding the total cost of stay, Refundable - payments less than the total cost of stay but higher than 0 |
| agent | Travel agency ID | 1 - 535 |
| company | Company ID | 6 - 543 |
| days_in_waiting_list | How long the booking was in the waiting list before confirmed to the customer | 0 - 391 |
| customer_type | Another breakdown of booking demographics based on the type of booking | Contract - booking has an associated allotment or contract, Group - booking is associated with a group booking, Transient - the booking has no associations to other bookings, Transient-Party - the booking is transient but associated with at least 1 other booking |
| adr | The sum of all payments received divided by the total nights stayed | -6.38 - 5400 |
| required_parking_spaces | How many carpark spaces the booking has requested | 0 - 8 |
| total_of_special_requests | How many special requests the guests have made | 0 - 5 |
| reservation_status | The final status of the reservation | Canceled - booking cancelled by the customer, Check-Out - customer stayed and has departed, No-Show - customer did not stay and did not cancel the booking |
| reservation_status_date | The date upon which the booking was last amended | 17/10/2014 - 14/09/2017 |

### Data Limitations
* The data has no unique identifiers such as booking or customer ID causing ambiguity in the nature of duplicate rows
* `customer_type`, `market_segment` and `distribution_channel` all largely serve similar functions - splitting the booking into demographics - there is some overlap and confusion much to be expected in the hospitality sector
* Weekends defined as Saturday & Sunday is not industry standard, Friday/Saturday weekend designations are more common 

## Business Requirements
* Describe your business requirements


## Hypothesis and how to validate?
* List here your project hypothesis(es) and how you envision validating it (them) 


## The rationale to map the business requirements to the Data Visualizations and ML tasks
* List your business requirements and a rationale to map them to the Data Visualizations and ML tasks


## ML Business Case
* In the previous bullet, you potentially visualized an ML task to answer a business requirement. You should frame the business case using the method we covered in the course 


## Dashboard Design
* List all dashboard pages and their content, either blocks of information or widgets, like buttons, checkboxes, images, or any other item that your dashboard library supports.
* Later, during the project development, you may revisit your dashboard plan to update a given feature (for example, at the beginning of the project you were confident you would use a given plot to display an insight but subsequently you used another plot type).



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

