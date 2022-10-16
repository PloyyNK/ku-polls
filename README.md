## Online Polls and Survey
[![Unittest](https://github.com/PloyyNK/ku-polls/actions/workflows/python-app.yml/badge.svg)](https://github.com/PloyyNK/ku-polls/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/PloyyNK/ku-polls/branch/main/graph/badge.svg?token=S7RKDEEO1G)](https://codecov.io/gh/PloyyNK/ku-polls)

An application for conducting online polls and surveys based
on Django, with additional features.


App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.


## Install and Run

1. Clone the repository
```
git clone https://github.com/PloyyNK/ku-polls.git
```
2. Install require package
```
pip install -r requirement.txt
```
3. Change `sample.env` name to `.env`
4. Run migrations
```
python manage.py migrate
```
5. Install data
```
python manage.py loaddata data/polls.json data/user.json
```
6. Run the server
```
python manage.py runserver
```
You can now visit the server  `http://127.0.0.1:8000/`

## Project Documents

All project documents are in [Project Wiki](../../wiki/Home)

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Software Development Plan](../../wiki/Software%20Development%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Task Board](https://github.com/users/PloyyNK/projects/3/views/1)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan)


| Username  | Password  |
|-----------|-----------|
|   harry   | hackme22 |
|   peteparker   | spiderman |
