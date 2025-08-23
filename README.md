# Recipe-App

A Streamlit app that helps you decide what to have for dinner tonight. 
You can add, edit, and delete recipes.

<img width="480" height="260" alt="Screenshot 2025-08-22 at 08 38 58" src="https://github.com/user-attachments/assets/842694a8-d678-424e-960d-cbd55284f070" />

## Tech Stacks
<img src="https://img.shields.io/badge/-Python-yellow.svg?logo=python&style=for-the-badge&logoColor=#3776AB"> <img src="https://img.shields.io/badge/-Mongodb-47A248.svg?logo=mongodb&style=for-the-badge">

Requirements:
- Ubuntu 24.04
- Python 3.9+

## Installation
1. Clone the repository, and install required libraries.
```
$ git clone https://github.com/SayakaYanagi/Recipe-App.git
$ cd Recipe-App
$ pip install -r requirements.txt
```
2. Create a `secrets.toml` inside `/Recipe-App/.streamlit/`.
   Replace uri with your MongoDB credentials.
```
[mongo]
database = "cookbook"
collection = "recipes"
uri = "mongodb://{user}:{password}@{host}:{port}/"

```
3. Set up MongoDB.  
Make sure your MongoDB instance is running and has a collection named `recipes` in the `cookbook` database.

4. Set up `streamlit.service` in your systemd directory.
```
[Unit]
Description=Recipe App Streamlit Service

[Service]
WorkingDirectory=/path/to/Recipe-App
ExecStart=/path/to/Recipe-App/.venv/bin/python3 /path/to/Recipe-App/.venv/bin/streamlit run /path/to/Recipe-App/Home.py

[Install]
WantedBy=multi-user.target
```

### Usage

Run the `streamlit.service`.
```
$ sudo systemctl enable streamlit.service
$ sudo systemctl start streamlit.service
```


