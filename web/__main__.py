import os

from dotenv import load_dotenv

from web.web import app

load_dotenv()

def main():
    app.run(debug=True, host=os.getenv('FLASK_HOST', 'localhost'), port=os.getenv('FLASK_PORT', '5000'))


if __name__ == '__main__':
    main()