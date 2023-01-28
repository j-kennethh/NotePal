from website import create

app = create()

# Run the web application
if __name__ == '__main__':
    app.run(debug=True)
