# Automotive Data Analysis with Python

## Overview
This project focuses on automotive sensor data analysis using Python.

It simulates and analyzes vehicle data such as vehicle speed, engine RPM, throttle position, brake pressure, battery voltage and motor temperature.

The goal of this project is to demonstrate how Python can be used for engineering data analysis, vehicle performance evaluation, warning detection, visualization and automated technical reporting.

This project is especially relevant for automotive engineering, mechatronics, embedded systems and data analysis applications.

## Main Features
- Read automotive sensor data from a CSV file
- Validate numeric data before analysis
- Sort data by time
- Detect duplicate or incorrect time values
- Calculate acceleration from speed data
- Analyze vehicle speed behavior
- Analyze engine RPM behavior
- Analyze throttle and brake signals
- Detect high motor temperature warnings
- Detect low battery voltage warnings
- Detect high-speed events
- Detect hard acceleration events
- Detect hard braking events
- Generate separate plots for vehicle signals
- Generate one dashboard plot
- Create an automated engineering report
- Save generated files inside an `outputs/` folder

## Technologies Used
- Python
- Pandas
- Matplotlib
- CSV data analysis
- Automotive sensor data
- Engineering automation
- Vehicle performance analysis
- Data validation
- Automated reporting

## Repository Structure

```text
automotive-data-analysis-python/
│
├── README.md                    # Project documentation
├── automotive_analysis.py        # Main Python analysis script
├── vehicle_data.csv              # Sample automotive sensor dataset
├── requirements.txt              # Required Python libraries
└── outputs/                      # Generated plots and report
Input Data

The project uses a CSV file named:

vehicle_data.csv

The dataset contains simulated automotive sensor values:

Column	Description
time_s	Time in seconds
vehicle_speed_kmh	Vehicle speed in km/h
engine_rpm	Engine speed in revolutions per minute
throttle_percent	Throttle position in percent
brake_pressure_bar	Brake pressure in bar
battery_voltage_v	Battery voltage in volts
motor_temperature_c	Motor temperature in degrees Celsius
Analysis Logic
Data Validation

Before the analysis starts, the script checks that:

the CSV file exists
all required columns are available
all values are numeric
time values are sorted
time values do not repeat or go backwards

This makes the project more reliable and closer to a real engineering workflow.

Speed Analysis

The script analyzes vehicle speed behavior and calculates:

Average speed
Maximum speed
Minimum speed
Maximum acceleration
Minimum acceleration

Acceleration is calculated from speed and time data.

Engine RPM Analysis

The script analyzes engine RPM values and calculates:

Average RPM
Maximum RPM
Minimum RPM
Temperature Monitoring

The script detects high motor temperature events.

A warning is triggered when:

motor_temperature_c > 90
Battery Monitoring

The script detects low battery voltage events.

A warning is triggered when:

battery_voltage_v < 12.0
Driving Behavior Analysis

The script analyzes simple driving behavior by detecting:

High-speed events
Braking events
Hard acceleration events
Hard braking events

The limits used in the script are:

High speed: vehicle_speed_kmh > 100
Hard acceleration: acceleration_mps2 > 2.5
Hard braking: acceleration_mps2 < -3.0
Generated Output

After running the script, the following files are generated in the outputs/ folder:

outputs/automotive_report.txt
outputs/speed_plot.png
outputs/rpm_plot.png
outputs/temperature_plot.png
outputs/battery_plot.png
outputs/throttle_brake_plot.png
outputs/automotive_dashboard.png
How to Run
1. Install required libraries
pip install -r requirements.txt
2. Run the analysis script
python automotive_analysis.py
Example Output
Automotive analysis completed successfully.
Report saved as: outputs/automotive_report.txt
Plots saved in: outputs
Project Purpose

The purpose of this project is to show how Python can be used in automotive engineering workflows.

It demonstrates:

Data analysis
Sensor signal evaluation
Data validation
Automated reporting
Warning detection
Vehicle behavior analysis
Engineering visualization
Python automation for technical reports
What I Learned
How to analyze automotive sensor data with Python
How to work with CSV datasets using Pandas
How to validate input data before analysis
How to calculate acceleration from speed data
How to visualize vehicle signals using Matplotlib
How to detect warning conditions from sensor values
How to generate automated engineering reports
How Python can support automotive and mechatronics projects
Possible Applications
Automotive data analysis
Vehicle performance evaluation
Sensor data monitoring
Engineering test reports
Mechatronics projects
Embedded systems data analysis
Internship portfolio project for automotive companies
Future Improvements
Add real vehicle data
Add CAN bus data analysis
Add OBD-II data support
Add battery performance analysis
Add electric vehicle data analysis
Add dashboard visualization with Streamlit
Add PDF report generation
Add comparison between different driving cycles
Add machine learning for anomaly detection
Project Status

This project was created as a Python engineering portfolio project focused on automotive data analysis, warning detection and automated reporting.
