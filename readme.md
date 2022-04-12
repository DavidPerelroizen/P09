# LITReview app

The LITReview app aims at helping a community of users to consult or ask for a book review at will.

## Installation

Below the instructions will be given to properly proceed to the needed packages installing.

### Virtual environment configuration

**Install the virtual environment package**

```bash
pip install virtualenv
```

**Create the virtual environment**

```bash
virtualenv localdir
```

You must specify the local directory path

**Activate the virtual environment**

Mac OS/Linux
```bash 
source localdir/bin/activate
```

Windows
```bash
localdir/Scripts/activate
```

### Install the necessary packages

Django
```bash
python pip install django
```

Django widget tweaks
```bash
python pip install django-widget-tweaks
```

Pillow
```bash
python pip install Pillow
```

Flake8
```bash
python -m pip install flake8
```

Flake8 html report
```bash
pip install flake8-html
```

## Usage

### Run the server

Open your terminal and run the following command:
```bash
python .\manage.py runserver
```

### Connect to the app website

Once the terminal command is executed, click on the link contained in the terminal message as below in order to connect
to the login page.
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 12, 2022 - 16:58:17
Django version 4.0.3, using settings 'LITReview.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Flake8 set-up and checks

### Flake 8 configuration

In the project directory, create a file as follows:
```bash
setup.cfg
```

In this file, write the following:
```bash
[flake8]
max-line-length = 119
exclude = venv, __init__.py, *.txt, *.csv, *.md
```
We restrict the maximum number of characters per line at 119. So flake8 won't consider as errors a line as long as it
has fewer characters.
We exclude from the flake8 checks the followings:
- Our virtual environment libraries
- Our packages init files
- Our requirement file
- Our readme file
- Our CSV databases
- Our migrations files


### Execute flake8 report

In case the user requests a regular flake8 check on the terminal, proceed as follows:
```bash
flake8 path/to/project/directory
```

In case a html reporting is preferred, proceed as follows:
```bash
flake8 --format=html --htmldir=flake-report
```