from src.webapp import app

if __name__ == '__main__':
    # test port
    app.run(host='0.0.0.0', port=8000 , debug=True)