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

All necessary packages are contained in the requirements.txt.
```bash
asgiref==3.5.0
certifi==2021.10.8
charset-normalizer==2.0.12
Django==4.0.3
django-icons==21.3
django-widget-tweaks==1.4.12
flake8==4.0.1
flake8-html==0.4.1
idna==3.3
importlib-metadata==4.11.2
Jinja2==3.0.3
MarkupSafe==2.1.0
mccabe==0.6.1
Pillow==9.0.1
pycodestyle==2.8.0
pyflakes==2.4.0
Pygments==2.11.2
requests==2.27.1
sqlparse==0.4.2
tzdata==2021.5
urllib3==1.26.9
zipp==3.7.0
```

Install them all by running the following command in terminal.
```bash
pip install -r requirements.txt
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