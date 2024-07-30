# Auto Repair

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Version](#version)
- [OS](#os)
- [Prerequisites](#prerequisites)
- [Executable](#executable)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Overview
Auto Repair is a comprehensive Python project developed for a fictional vehicle repair shop. The application helps manage various services, track costs, and generate reports, making it easier to run and organize repair shop operations.

## Features
- Insert, manage, and export services
- Export services as Excel or CSV files
- Initial dashboard to display key information (e.g., revenue, number of services, number of unpaid services, etc.)
- Data is always updated according to the database information
- While inserting a service, the program checks if the inserted tax number already exists in the database. If it does, it automatically fills the entries with the related information.
- Select a vehicle or client directly from the database
- Search engine in the manage section to search for a specific vehicle or client and filter the services to see all services, paid services, or unpaid services
- Many other features

## Version

Python version: 3.12.0

## OS

Windows

## Prerequisites

To run this project, you will need the following Python libraries:

- flask
- flask_sqlalchemy
- sqlalchemy
- flask_bcrypt
- Pillow
- pandas
- tkcalendar
- numpy
- babel
- openpyxl

You can install the required libraries using pip:

```bash
pip install flask flask_sqlalchemy sqlalchemy flask_bcrypt Pillow pandas tkcalendar numpy babel openpyxl
```
##  Executable
Link to download the executable file:
https://drive.google.com/file/d/17vv3QcDl9wfsgzHXHn3HddD7NdIm8yC3/view?usp=drive_link

## Contact
Email: tiagogitdev@gmail.com

## Acknowledgements
The theme used is the Azure-ttk-theme, from the github user rdbende. Link below.

https://github.com/rdbende/Azure-ttk-theme
