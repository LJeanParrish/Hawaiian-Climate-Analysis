# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to my 'Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    return "Welcome to my Precipitation page!"

# 5. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
     return "Welcome to my Stations page!"

# 6. Define what to do when a user hits the /temperature route
@app.route("/api/v1.0/tobs")
def tobs():
     return "Welcome to my Temperature page!"


if __name__ == "__main__":
    app.run(debug=True)# 3. Define what to do when a user hits the index route
