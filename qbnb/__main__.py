from qbnb import app
from qbnb .models import *
from qbnb.controllers import *

FLASK_PORT = 8081

if __name__ == '__ main__':
    app.run(debug=True, port=FLASK_PORT, host='0.0.0.0')

   
