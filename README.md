
# Metro Car Funnel Analysis
## Table of Contents
- Project Description
- Tools
- Usage
- Project Structure
- Data analysis and Results
- Contact

## Project Description
### Inrtoduction
In any business, customer satisfaction and profit maximization are important aspects that ensure sustainability of a company. The Metro Car company in USA provide car services for customers. In this project, the ride and users success rates at different stages in the ride services using SQL, Pandas and other visualization tools.
- **User_level stages:** App_download > signup > ride_request > ride_accept > ride_completion > review
- **ride_level stages:** ride_request > ride_accept > ride_completion > transaction > review 
### Project specific questions
- How the ride request, acceptance, rejection and completion vary across the hours of a day?
- Which stage of the ride process invovle a big drop-off in users and ride completion?
- What is the impact of user platform for ride request affect the funnel?
- Does age affect the users rate of ride request and completion?
- What is the GAP level in ride demand and supply during the peak hours?

These are some of the questions that are addressed by this project.

### Specific Objectives

- To examine the success rate of users transfer from one stage to another using funnel charts

- To examine the ride success rates from ride request to ride review using the funnel charts

- Identify peak hours for ride requests 

### Significance
The project has a significance of identifying the maximum drop-off stages in number of customers and ride services. This allows to identify targets that need to be ammended for sustainable growth of the company interms of profit and customer satisfaction.


## Screenshoots

![Metrocar-project](https://github.com/derewor/Metrocar-Project/blob/main/Results/Ride%20Funnel.png)

## Tools
Google colab, 
Googlesheets, 
Beekeper Studio,
SQLAlchemy to connect to the Postgress database,
SQL, 
Panda, 
Numpy for analysis,
Plotly express, 
seaborn, 
matplotlib for data visualization,
Google slides


## Usage

To reproduce the code, run the googlecolab notebook file final_metrocar_project.ipynb file in the Github Metrocar_project. 


## Project Structure
- Data/: A directory containing the raw data.
- Notebook/: A directory containing the googlecolab notebook with an active code.
- Script/: A directory containing codes for an interactive dashboard for the user base and ride funnels using DASH.
- Results:/ A funnel that shows the ride drop off at each stage.
- Docs/: A Metrocar Project pdf file that contains the major findings of the project for communication with stakeholders.
- README.md/: A file containing an overview of the project.
## Data Analysis and Results
### Libraries
- Libraries required for analysis such as numpy, pandas, matplotlib etc. have been imported.
### Data
- The Metrocar data was imported from the postgress database using the SQLalchemy engine. Five table containing the different stages of the funnel are imported separately.
### Data Pre-processing
- The data was checked for nulls and duplications.
- The tables were joined based on joining keys.
## Analysis Results
- The age of users and the platform they use for ride completion do not have impact on the whole process.
- For user_level funnels: Users drop-off occur at all level but the biggest drop-off (45%) occurs between the ride acceptance and completion.
- At the ride level, the biggest drop-off (~35%) occurs between the ride request and ride acceptance stages.
- There are two peak perionds during the day where the ride demand is high i.e. 8AM-9AM and 4PM - 7PM.
- In these two periods the ride supply is ~35% of the demand. 
- This can be an opportunity to increase revenue.
## Visualization
- The funnels were visualized by using plotly express
- Interactive funnels were constructed using DASH. 
## Authors

- [@derewor](https://github.com/derewor/TravelTide_Customer_Segmentation_projecte)

https://www.linkedin.com/in/dereje-worku-mekonnen-a8345217/

https://www.linkedin.com/in/charlesudoutun/

https://www.linkedin.com/in/tsaishiou/

https://www.linkedin.com/in/anna-matviichuk0812/
