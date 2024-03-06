# Student Grade Predictor: An Interactive Learning Analytics Tool

Welcome to the Student Grade Predictor, an application designed to assist students in understanding their academic performance through predictive modeling and data visualization. In this tool, we leverage machine learning to predict student grades based on a variety of factors, utilizing both a personalized approach (based on individual student data) and a non-personalized approach (through general grade trends and attributes). The Student Grade Predictor is developed to be user-friendly and accessible to students across all disciplines.






<img width="1465" alt="image" src="https://github.com/nilm9/Student_Grade_Predictor/assets/85683608/adc1a2e5-de0e-4677-90a0-079f0b671f99">


# Index

- [Student Grade Predictor: An Interactive Learning Analytics Tool](#student-grade-predictor-an-interactive-learning-analytics-tool)
- [Dataset Description](#dataset-description)
- [Data Storage and Retrieval with MongoDB](#data-storage-and-retrieval-with-mongodb)
- [Needed Libraries](#needed-libraries)
- [The Stack](#the-stack)
  - [Data Preprocessing and Analysis](#data-preprocessing-and-analysis)
  - [Front-End](#front-end)
  - [Visualization](#visualization)
  - [Back-End](#back-end)
  - [Machine Learning](#machine-learning)
- [Other Developed Functionalities](#other-developed-functionalities)
  - [Counterfactual Analysis](#counterfactual-analysis)
  - [Feature Importance](#feature-importance)
  - [Student Clustering](#student-clustering)
- [App Structure](#app-structure)
  - [Backend Components](#backend-components)
  - [Frontend Components](#frontend-components)
  - [Machine Learning](#machine-learning-1)
  - [Others](#others)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Visualization](#visualization-1)
- [Getting Started](#getting-started)
- [Further Cloud Deployment on AWS](#further-cloud-deployment-on-aws)



## Dataset Description

For this project, we have compiled a comprehensive dataset which includes information about student grades, their demographic details, academic background, and other relevant factors from 2013 to 2014. Key data points include:

- Student demographics (age, gender, region, etc.)
- Course details
- Historical grades
- Attendance records
- Other academic factors

## Data Storage and Retrieval with MongoDB

The application uses MongoDB for efficient data storage and retrieval. Data relevant to student grades, including historical data and predictive analysis results, are stored in a MongoDB database. This approach facilitates:

- Persistent storage of prediction results.
- Efficient retrieval of data for visualization and further analysis in the web application.

## Needed Libraries

To run this project, the following libraries are required:

- Pandas
- Numpy
- Scikit-learn
- Joblib
- Flask
- Vue.js
- Pymongo (for MongoDB integration)

## The Stack

![img.png](img.png)

This project employs various technologies and tools:

### Data Preprocessing and Analysis

- Pandas and Numpy for data handling.
- Jupyter Notebooks for exploratory data analysis and model development.

### Front-End

- Vue.js for interactive web interface.
- HTML, CSS, and JavaScript for website structure and styling.

### Visualization

- Integrated data visualizations using Vue.js components and using the framework Primevue.

### Back-End

- Flask web server.
- Database integration with MongoDB for data storage and retrieval.

### Machine Learning

We developed a predictive model using several learning models to determine which could most accurately forecast student grades. Our suite of models included Linear Regression, Ridge Regression, Lasso Regression, Random Forest, Gradient Boosting, and Support Vector Regression (SVR). Each model was initialized with default parameters, except for Random Forest, which was fine-tuned with the best hyperparameters discovered during the optimization process.

After rigorous training and evaluation, it was determined that an XGBoost model outperformed the others. The XGBoost (eXtreme Gradient Boosting) algorithm is known for its efficiency and performance in machine learning competitions. It operates by constructing a multitude of decision trees in a sequential manner, where each tree corrects the errors of its predecessor, resulting in a powerful ensemble method.

The selection was based on several performance metrics, including Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and the coefficient of determination (R²). The XGBoost model demonstrated a superior balance of bias and variance, providing robust predictions with lower errors and higher R² values, indicative of a better fit to the data.


### Other developed funcitonalities

  #### Counterfactual Analysis:
    
  This functionality allows students to modify input factors and observe how these changes might alter their predicted grades. It's a form of sensitivity analysis that provides           actionable insights.
    
  #### Feature Importance:
    
  Displays the relative importance of each feature used in the predictive model. It helps to visualize which aspects of a student's profile and academic record are most predictive of     their grade outcomes.

  #### Student Clustering:
  
  Several unsupervised learning methods have been used such as K-Means, DBSCAN, PCA and others.


## App Structure

The project is organized into a backend and a frontend directory, each with specific components and scripts:

### Backend Components:

- **API**:
  - `routes.py`: Contains the API routes for the web application.
  
- **Models**:
  - `final_model.joblib`: The machine learning model for predicting student grades.

- **Services**:
  - `config.py`: Configuration settings for the backend.
  - `database.py`: Script for database connection and operations.
  - `predictions.py`: Service for generating grade predictions using the model.

- **Utilities**:
  - `db_save_data.py`: Utility script for saving data to the database.
  - `utilities.py`: General utility functions for the backend.

- **Root Files**:
  - `requirements.txt`: Required libraries and dependencies for the backend.
  - `run.py`: The main script to run the Flask server for the backend.

### Frontend Components:

- **Components**:
  - `App.vue`: The main Vue.js application file.
  - `CounterFactual.vue`: Component for counterfactual analysis.
  - `DashboardCharts.vue`: Components for dashboard chart visualizations.
  - `DataViz.vue`: Data visualization component.
  - `FeatureImportance.vue`: Component to show the importance of features.
  - `HomeLanding.vue`: Landing page component.
  - `PredictGrade.vue`: Component for the grade prediction feature.

- **Assets**:
  - Static files like images, stylesheets, etc.

- **Utilities**:
  - JavaScript utilities for the frontend.

### Machine Learning:

- **Jupyter Notebooks**:
  - `Clustering_Students.ipynb`: Notebook for clustering student data.
  - `EDA-StudentGrades.ipynb`: Notebook for exploratory data analysis.
  - `Modelling-StudentGrades.ipynb`: Notebook for developing the predictive models.

- **Data**:
  - `Expanded_data_with_more_features.csv`: Primary dataset for the project.
  - `modified_dataset2.csv`: A modified version of the dataset, potentially used for further analysis or model refinement.

### Others:

- **Root Directory Files**:
  - `.gitignore`: Specifies intentionally untracked files to ignore.
  - `babel.config.js`, `jsconfig.json`, `package.json`: Configuration files for JavaScript and Vue.js.

## Machine Learning Pipeline

This project utilizes a machine learning pipeline implemented in Python. The model is trained on historical student data to predict future grades. The process involves data preprocessing, feature engineering, model training, and evaluation. The final model is saved as `final_model.joblib` and is used for grade predictions in the application.

## Visualization

The application includes an interactive data visualization component built with Vue.js. It provides insights into grade distributions, student demographics, and other relevant academic factors.

## Getting Started

To get started with the Student Grade Predictor:

1. Clone the repository.
2. Install the required libraries.
3. Run the Jupyter notebooks for data preprocessing and model training.
4. Start the Flask server for the back-end.
5. Launch the Vue.js application for the front-end.

## Further Cloud Deployment on AWS

Deploying the Student Grade Predictor on AWS involves several steps to ensure scalability, security, and accessibility. Below is the deployment strategy:

1. **Configure an EC2 Instance**: Launch an EC2 instance suitable for the web server. Select an instance type that offers a balance between cost and performance. Install Docker on this instance for application container management.
2. **Dockerize the Application**: Create Docker containers for the frontend and backend. Write Dockerfiles to define the environment, install dependencies, and specify run commands.
3. **Set Up MongoDB**: Use Amazon DocumentDB with MongoDB compatibility for the database. Configure it to connect with the application, setting up VPC and security groups for secure access.
4. **Deploy Containers**: Deploy the Docker containers onto the EC2 instance using Docker Compose, which manages multi-container Docker applications and ensures cohesive deployment.
5. **Establish Load Balancing**: Set up an AWS Elastic Load Balancer to distribute incoming traffic across multiple instances, ensuring high availability and fault tolerance.
6. **Enable Autoscaling**: Configure AWS Autoscaling to adjust the number of EC2 instances automatically in response to application demand, ensuring consistent performance.
7. **Monitor with CloudWatch**: Implement AWS CloudWatch for application performance monitoring. Set alarms and automate responses to changes in AWS resources.
8. **Configure DNS with Route 53**: Use AWS Route 53 to direct users to the application by linking the domain name to the load balancer's DNS name.


## Group Members
Elham Najafi, 
Elaheh Najafi, 
Lucie Stecker, 
Lisa Mühl, 
Eric Souobu Ndjoughem,
Nil Monfort


We hope this tool proves to be a valuable resource for students and educators alike, providing insights into academic performance and aiding in educational planning.
