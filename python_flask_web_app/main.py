'''
Install the following modules before proceeding:

install the lightweight python framework
- pip3 install flask

for logging users in
- pip3 install flask-login

wrapper for sql
- pip3 install flask-sqlalchemy

'''

#folders within the website package is automatically executed and can be used to import func(s)
from website import create_app

app = create_app()

#run web app only if main.py is executed
if __name__ == '__main__':
    #auto rerun web app if any changes had been made, change to False if running production
    app.run(debug=True)
    