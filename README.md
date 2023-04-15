Clone the Git repository to your local machine using the following command: git clone https://github.com/pusteugene/testworkpython.git
Install the required packages by running: pip install -r requirements.txt
Create the SQLite database by running the following command: python manage.py migrate
Load the test data by running the following command: python manage.py loaddata dump.json
Start the development server: python manage.py runserver
You can now access the API endpoints using a web browser or a tool like Postman by navigating to http://localhost:8000/.
To access the Django admin panel, go to http://localhost:8000/admin and log in with the superuser credentials you created during the installation process.
That's it! You should now be able to run the project on your local machine.
