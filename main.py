from main import build_app

if __name__ == '__main__':
    app = build_app()
    app.run(debug=True, host='0.0.0.0', port=5000)