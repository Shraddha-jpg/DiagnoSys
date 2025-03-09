To run the code on Linux/macOS:
FLASK_PORT=<port> python app1.py

To run on Windows:
set FLASK_PORT=<port>
python app1.py

where <port>=5000, 5001, 5002 etc.

Now, every instance of the flask app, i.e. , the port, simulates a new storage system.

The information for every object of each storage system is stored in data_instance_<port>, which is automatically created when you run the flask app on a new port, or if you run it on a port which you have already run before, it fetches, or posts data to the json files in that directory respectively.


The global_systems.json has information about all the systems across different ports

When you run the http://127.0.0.1:<port> on browser, it will show URL not found.
You will need to add /ui at the end of it to run. i.e.http://127.0.0.1:<port>/ui


