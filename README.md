# Paper Class Helper _( Version 2.0 )_

[![Push to Docker Hub - BOT](https://github.com/kavishka-sulakshana/Official_RD_Paper_Bot/actions/workflows/main.yml/badge.svg)](https://github.com/kavishka-sulakshana/Official_RD_Paper_Bot/actions/workflows/main.yml)

## PIP Dependancy Libraries

`pip install <...>`

-   python-telegram-bot
-   requests
-   python-dotenv
-   firebase-admin

### Create Virtual Environment

-   `python -m venv myenv`

### Activate the virtual Environment

-   `myenv\Scripts\activate`

### Deactivate the virtual Environment

-   `deactivate`

### Run the Bot

-   `python bot.py`

> googleCredentials.json - has google credentials

<br>

## Database Structure

### students

-   barcode _(document_id)_
-   name
-   username
-   school

### classes

-   name _(document_id)_
-   name
-   papers
    -   number _(document_id)_
    -   name
    -   status
    -   students
        -   barcode _(document_id)_
        -   rank
        -   marks
        -   student_id _(reference from `student`)_
        -   paper_link
