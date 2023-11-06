# task_manager

Here is the detailed instruction to run the project

1. Clone the repository
	"git clone https://github.com/ajay016/task_manager.git"

2. Switch to branch "dev.0.0.1"
	"git switch dev.0.0.1"

3. After successfully cloning the repository create a virtual environment in the project directory using the command "python -m venv <env_name>" e.g.
	"python -m venv venv" 

4. Activate the environment "<env_name>/Scripts/activate". I have given the name of the environment "venv". So the command will be:
	For Windows: "venv/Scripts/activate"
	For Linux: venv/bin/activate

5. Install all the dependencies
	"pip install -r requirements.txt"

6. Create a file ".env" where the settings.py file is located i.e. in your project folder

7. Set the environment variables. In this projects the environment variables file contains API KEY and DATABASE credentials
	API_KEY=
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=Your_Database_name
	DB_USER=Your_Username
	DB_PASSWORD=Your_password
	DB_HOST=Local_server (127.0.0.1)
	DB_PORT=Port_number (5432)
	
	Note: If you have an API key, you can set it now or you can go to Step 8. Then set the "API_KEY"

8. (Optional) You can generate the API Key using the command
	"python manage.py generate_api_key"

9. Assuming you have PostgreSQL installed on your machine, create database. The name of my database is "task_manager"
	"CREATE DATABASE task_manager;"
	
10. Import the database. Replace the path:
	"C:\Program Files\PostgreSQL\16\bin\psql" -U <username> -d <database_name> -f database_dump.sql"
	"C:\Program Files\PostgreSQL\16\bin\psql" -U postgres -d task_manager -f database_dump.sql"

11. Run migrations
	"python manage.py makemigrations"
	"python manage.py migrate"



12. Import the fixtures
	"iconv -f UTF-16 -t UTF-8 input.json -o output.json"


------------------------API Urls------------------------
View Task list:         "api/task_list/"
Create Task:            "api/task_create/"
Task Details:           "api/task_detail/<int:task_id>/"
Task Update (put):      "api/task_update/<int:task_id>/"
Task Update (patch):    "api/task_update_patch/<int:task_id>/"
Task Delete:            "api/task_delete/<int:task_id>/"