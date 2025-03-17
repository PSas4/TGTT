from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from datetime import datetime  # Import datetime for date tracking

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from Streamlit frontend

# Define the Excel file to store bills
BILL_FILE = "bills.xlsx"

# Initialize the Excel file if not present
if not os.path.exists(BILL_FILE):
    df = pd.DataFrame(columns=["Date", "Customer Name", "Start Reading", "End Reading", "Distance",
                               "Rate per km", "Toll Charges", "State Tax", "Meal Charges",
                               "Night Stay", "Total Fare"])
    df.to_excel(BILL_FILE, index=False)


@app.route("/calculate", methods=["POST"])
def calculate_fare():
    try:
        data = request.get_json()

        start_reading = float(data.get("start_reading", 0))
        end_reading = float(data.get("end_reading", 0))
        rate_per_km = float(data.get("rate_per_km", 0))
        toll = float(data.get("toll", 0))
        state_tax = float(data.get("state_tax", 0))
        meal = float(data.get("meal", 0))
        night_stay = float(data.get("night_stay", 0))

        # Ensure valid readings
        if end_reading < start_reading:
            return jsonify({"error": "End meter reading cannot be less than start reading"}), 400

        # Calculate distance traveled
        distance = end_reading - start_reading

        # Calculate total fare
        total_fare = (distance * rate_per_km) + toll + state_tax + meal + night_stay

        return jsonify({"total_fare": round(total_fare, 2), "distance": round(distance, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/save", methods=["POST"])
def save_bill():
    try:
        data = request.get_json()
        customer_name = data.get("customer_name", "Unknown")
        start_reading = float(data.get("start_reading", 0))
        end_reading = float(data.get("end_reading", 0))
        rate_per_km = float(data.get("rate_per_km", 0))
        toll = float(data.get("toll", 0))
        state_tax = float(data.get("state_tax", 0))
        meal = float(data.get("meal", 0))
        night_stay = float(data.get("night_stay", 0))

        # Calculate distance and total fare
        distance = end_reading - start_reading
        total_fare = (distance * rate_per_km) + toll + state_tax + meal + night_stay

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD

        # Load existing data and append new entry
        df = pd.read_excel(BILL_FILE)

        new_entry = pd.DataFrame([{
            "Date": current_date,
            "Customer Name": customer_name,
            "Start Reading": start_reading,
            "End Reading": end_reading,
            "Distance": distance,
            "Rate per km": rate_per_km,
            "Toll Charges": toll,
            "State Tax": state_tax,
            "Meal Charges": meal,
            "Night Stay": night_stay,
            "Total Fare": total_fare
        }])

        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(BILL_FILE, index=False)

        return jsonify({"message": "Bill saved successfully!", "date": current_date})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
