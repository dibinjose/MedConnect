# MedConnect

Disease Predicting ChatBot using JavaScript and Python

---

# Folder Structure

There are two folders:

*  Scraping : For scrapping data from website.
*  ml : The Machine Learning and python flask codes.

---

# 1. Scrapping

```bash
cd Scraping
npm install
```

To run the program

```bash
node index.js
```

---

# 2. ML

```bash
cd ml
```

## Create an Environment

```bash
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

On Windows:

```bash
$ py -3 -m venv venv
```

## Activate the environment

Before you work on your project, activate the corresponding environment:

```bash
$ . venv/bin/activate
```

On Windows:

```bash
> venv\Scripts\activate
```

Your shell prompt will change to show the name of the activated environment.


## Installing packages

```bash
$ pip install -r requirements.txt
```

## Creating ML Model

```bash
python model_creation.py
```
Three files would be added to project with an extension of .pickle

## Run Project

```bash
python app_api.py
```

---

# Other Important Codes

---

## Export MySQL Database

```bash
$ mysqldump -u root -p medconnect > medconnect.sql
```

## Export current environment configuration file: pip freeze

```bash
$ python -m pip freeze > requirements.txt
```