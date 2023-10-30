# praktikum_new_diplom

### Description

"Food Assistant" application: a website where users can publish recipes, add other users' recipes to their favorites, and subscribe to posts from other authors. The "Shopping List" feature allows users to create a list of groceries required for preparing selected dishes.


### Technologies

* Python 3.7
* Django 3.2.16
* Django Rest Framework


### Author

Alina Almukhametova <br>
This project was created as part of Python Developer Professional Training Course. <br>
The project leverages the provided frontend by the course creators.


### How to Run the Project

Clone the repository and navigate to it in the command line:

```
git clone https://github.com/almalina/final_project_foodgram.git
```

```
cd backend
```

Create and activate a virtual environment:

```
python3 -m venv env
```

* For Linux/macOS:

    ```
    source env/bin/activate
    ```

* For Windows:

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Install dependencies from the requirements.txt file:

```
pip install -r requirements.txt
```

Perform migrations:

```
python3 manage.py migrate
```

Run the project:

```
python3 manage.py runserver
```
