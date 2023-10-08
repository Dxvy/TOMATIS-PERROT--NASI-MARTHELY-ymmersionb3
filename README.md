# TrashTalk Project
### Description
This project is an e-commerce website for a company called TrashTalk.
The company sells trashcans of many kind to help people sort their waste both at home and at work.

### Team
For this project we decided to make a team of 3 people:
- [Davy](https://github.com/Dxvy)
- [Matéo](https://github.com/MateoPerrotNasi)
- [Margot](https://github.com/xhmyjae)

We all worked together on different tasks to make this project a reality.

# Installation
Those are the steps to follow to install the project on your computer.

- Clone the project
- Create a virtual environment (with Conda or Venv)
- Install the dependencies with `pip install -r requirements.txt`
- Create a database with the following info `trashtalk` for the name, `root` for the user and `` for the password, on 'localhost' with port `3306`.
- Import the `dump.sql` file in the database
- You can import the products.csv file to have some products in the product table
- Run the main.py file to start the server


# Technologies

Our project is using many tehcnologies:
- Flask for the backend and API creation and management
- MySQL for the database
- An environment to manage the dependencies

# Dependencies
# Project Structure
The projetc is structured as follows :
- /backend : The folder of the backend section
- /environments : The folder for managing LocationIQ API Key
- /flask_session : The folder in which flask stores the numbers of the sessions created
- /frontend : The main folder of the frontend section
  - /component : The component of the website
  - /static : The folder that contains files that don't require server-side processing.
    - /images : The images used in the website
  - /templates : The templates used in the webdsite
# Database
The database structure is as follows :

![alt text](https://github.com/Dxvy/TOMATIS-PERROT--NASI-MARTHELY-ymmersionb3/blob/main/database_schema.png?raw=true)
# License
This project is licensed under GPL-3.0 license. You can find the lincense in the LICENSE file.
