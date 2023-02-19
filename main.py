from website import create_app

# Create a flask app
app = create_app()

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', debug=True, port=8080)