# ECS Employee Recognition Program

The ECS Employee Recognition Program is a web-based application that allows managers and peers to recognize and reward outstanding employee performance within the organization. It provides a platform for promoting a positive work environment, boosting employee morale, and fostering a culture of appreciation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Features

- User Authentication:
  - Secure login and registration system for employees, managers, and administrators.
  - Role-based access control with different permission levels for each user type.
  
- Recognition Submission:
  - Employees and managers can submit recognition for outstanding performance.
  - Recognition can include comments and optional rewards.
  
- Recognition Feed:
  - Real-time feed displaying the latest employee recognitions.
  - Filter and search options to view specific recognitions based on criteria such as date, department, or employee name.
  
- Rewards and Badges:
  - Recognition can include virtual rewards or badges for employees.
  - Track and display earned rewards and badges on employee profiles.
  
- Notifications and Alerts:
  - Automatic email notifications sent to recognized employees and their managers.
  - Alerts for pending or unacknowledged recognition to ensure timely responses.
  
- Reporting and Analytics:
  - Generate reports on recognition trends and statistics.
  - Analyze recognition data to identify top-performing employees or teams.

## Screenshots Examples

<p align="center">Admin Creating new Vendor</p>

<p align="center">
  <img src="https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program/blob/main/Employee_Recognission_Program/screenshots/AdminView.jpeg" alt="Login Portal" width="800">
</p>

<br><p align="center">User views Categories</p>

<p align="center">
  <img src="https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program/blob/main/Employee_Recognission_Program/screenshots/Categories.jpeg" alt="Signup Portal" width="800">
</p>

<br><p align="center">User views Vendors</p>

<p align="center">
  <img src="https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program/blob/main/Employee_Recognission_Program/screenshots/Vendors.jpeg" alt="Creating a New Flight" width="800">
</p>


<br><p align="center">Program Leaderboard</p>

<p align="center">
  <img src="https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program/blob/main/Employee_Recognission_Program/screenshots/LeaderBoard.jpeg" alt="Editing or Deleting an Existing Flight 1" width="800">
</p>

<br><p align="center">User Info Form</p>

<p align="center">
  <img src="https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program/blob/main/Employee_Recognission_Program/screenshots/UserForm.jpeg" alt="Editing or Deleting an Existing Flight 2" width="800">
</p>


## Installation

To install and set up the ECS Employee Recognition Program, follow these steps:

1. Clone the repository:
   git clone https://github.com/MahmoudAbdelkhalek5o5o/ECS_Employee_Recognition_Program.git
2. Navigate to the project directory:
   `cd ECS_Employee_Recognition_Program`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Set up the environment variables:
- Copy the `.env.example` file to `.env`.
- Update the necessary configuration values in the `.env` file.
5. Set up the database:
- Create a new database for the application.
- Update the database connection details in the `.env` file.
6. Run database migrations:
   `python manage.py migrate`
7. Start the application:   
8. Access the application in your browser:
   `http://localhost:8000`

## Usage

1. Open your web browser and navigate to `http://localhost:3000`.

2. Register a new account or log in with your existing credentials.

3. Depending on your user role (employee, manager, or administrator), you will have different permissions and capabilities within the application.

4. Explore the different features, such as submitting recognition, viewing the recognition feed, granting rewards or badges, and generating reports.

5. Customize the application settings and configurations as needed (see [Configuration](#configuration)).

## Configuration

The ECS Employee Recognition Program can be configured by modifying the values in the `.env` file. Here are some of the configurable options:

- Database connection details
- SMTP server settings for email notifications
- Default user roles and permissions
- Application branding and appearance
- Default reward types and badge categories

Make sure to restart the application after making any configuration changes for them to take effect.
