# Description
API_yamdb is review-site of movies, books and songs with functionality:
  * register by email with confirmation
  * get JWT-token by email and password for future use
  * Titles, genres and catogories are for admin create/edit or user read with search and filter by names and slugs
  * Users can:
      * create review or comment
      * edit and delete only their reviews or comments 
      * edit their profile

# Installation
Clone repository:
```
git clone https://github.com/Mackleroy/api_yamdb.git
```
Create virtual environment and activate it
```
python3 -m venv venv
source venv/bin/activate
```
Install all dependencies
```
pip install -r requirements.txt
```
Then come in root directory of project and apply regular configurations
```
python3 manage.py makemigratons
python3 manage.py migrate
```
Start server
```
python3 manage.py runserver
```
