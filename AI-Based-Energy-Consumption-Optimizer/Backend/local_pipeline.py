import os
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from stable_baselines3 import PPO

LSTM_MODEL_PATH = "lstm_energy_model.keras"

LSTM_SCALER_X_PATH = "x_scaler.pkl"

LSTM_SCALER_Y_PATH = "y_scaler.pkl"

PPO_MODEL_PATH = "ppo_fan_controller_finalv1_2"

PPO_SCALER_PATH = "ppo_scaler.pkl"


# Global LSTM Objects

lstm_model = None

x_scaler = None

y_scaler = None

ppo_model = None

ppo_scaler = None

# Required Columns and Accepted Aliases

REQUIRED_COLUMNS = {
    "indoor_temp_C": [
        "indoor_temp_c",
        "indoor temperature",
        "indoor temp",
        "room temperature",
        "room temp"
    ],

    "indoor_humidity": [
        "indoor_humidity",
        "indoor humidity",
        "room humidity"
    ],

    "outdoor_temp_C": [
        "outdoor_temp_c",
        "outdoor temperature",
        "outdoor temp",
        "outside temperature",
        "outside temp"
    ],

    "outdoor_humidity": [
        "outdoor_humidity",
        "outdoor humidity",
        "outside humidity"
    ],

    "outdoor_wind_speed": [
        "outdoor_wind_speed",
        "wind speed",
        "windspeed",
        "outdoor wind"
    ],

    "occupant_presence": [
        "occupant_presence",
        "occupancy",
        "occupied",
        "presence"
    ]
}

# Dataset Validation

def validate_dataset(dataset_source):

    print("\n" + "=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)

    # Detect Source Type
   
    if isinstance(dataset_source, str):

        if not os.path.exists(dataset_source):
            raise FileNotFoundError(
                f"\nERROR: Dataset not found:\n{dataset_source}"
            )

        extension = os.path.splitext(dataset_source)[1].lower()

    else:

        extension = os.path.splitext(dataset_source.filename)[1].lower()

    # Read Dataset

    if extension == ".csv":

        df = pd.read_csv(dataset_source)

    elif extension == ".xlsx":

        df = pd.read_excel(dataset_source)

    else:

        raise ValueError(
            "\nERROR: Only CSV or Excel files are supported."
        )

    # Minimum Rows
    
    if len(df) < 24:

        raise ValueError(
            "\nERROR: At least 24 historical records are required."
        )

    # Normalize Uploaded Column Names
    
    normalized_columns = {
        col.lower().strip(): col
        for col in df.columns
    }

    rename_dict = {}

    missing_columns = []

    # Detect Required Columns
    
    for standard_name, aliases in REQUIRED_COLUMNS.items():

        found = False

        for alias in aliases:

            if alias.lower() in normalized_columns:

                original_name = normalized_columns[
                    alias.lower()
                ]

                rename_dict[original_name] = standard_name

                found = True
                break

        if not found:

            missing_columns.append(standard_name)

    # Missing Columns
   
    if len(missing_columns) > 0:

        print("\nMissing Required Columns:")

        for column in missing_columns:

            print(f"• {column}")

        error_message = (
         "Missing required measurements:\n\n"
        )

        for column in missing_columns:
         error_message += f"• {column}\n"

        raise ValueError(error_message)

    # Rename Columns
  
    df.rename(
        columns=rename_dict,
        inplace=True
    )

    # Display Mapping

    print("\nDetected Column Mapping")
    print("-" * 40)

    for original, new in rename_dict.items():

        print(f"{original}  --->  {new}")

    # Missing Values
  
    if df[
        list(REQUIRED_COLUMNS.keys())
    ].isnull().sum().sum() > 0:

        raise ValueError(
            "\nERROR: Dataset contains missing values."
        )

    # Numeric Validation

    for column in REQUIRED_COLUMNS.keys():

        if not pd.api.types.is_numeric_dtype(df[column]):

            raise ValueError(
                f"\nERROR: '{column}' must contain numeric values only."
            )

    # Occupancy Validation

    if not df["occupant_presence"].isin([0, 1]).all():

        raise ValueError(
            "\nERROR: Occupancy must contain only 0 or 1."
        )

    # Value Range Validation

    if not df["indoor_temp_C"].between(-20, 60).all():

        raise ValueError(
            "\nERROR: Indoor temperature must be between -20°C and 60°C."
        )

    if not df["outdoor_temp_C"].between(-30, 60).all():

        raise ValueError(
            "\nERROR: Outdoor temperature must be between -30°C and 60°C."
        )

    if not df["indoor_humidity"].between(0, 100).all():

        raise ValueError(
            "\nERROR: Indoor humidity must be between 0 and 100."
        )

    if not df["outdoor_humidity"].between(0, 100).all():

        raise ValueError(
            "\nERROR: Outdoor humidity must be between 0 and 100."
        )

    if not df["outdoor_wind_speed"].between(0, 150).all():

        raise ValueError(
            "\nERROR: Outdoor wind speed is outside the expected range."
        )

    # Success

    print("\n" + "=" * 60)
    print("DATASET VALIDATION SUCCESSFUL")
    print("=" * 60)

    print(f"Rows Loaded    : {len(df)}")
    print(f"Columns Loaded : {len(df.columns)}")
    print("Status         : VALID")

    return df

def load_lstm_resources():

    global lstm_model
    global x_scaler
    global y_scaler


    lstm_model = load_model(LSTM_MODEL_PATH)

    x_scaler = joblib.load(LSTM_SCALER_X_PATH)

    y_scaler = joblib.load(LSTM_SCALER_Y_PATH)



# Predict Future Environment using LSTM

def predict_future_environment(df):

    print("\n" + "=" * 60)
    print("LSTM PREDICTION")
    print("=" * 60)

    # Feature Order
    # same as training

    feature_columns = [

        "indoor_temp_C",

        "indoor_humidity",

        "outdoor_temp_C",

        "outdoor_humidity",

        "outdoor_wind_speed",

        "occupant_presence"

    ]

    # Extracting Last 24 Records

    sequence = df[feature_columns].tail(24)

    # Scale Input
  
    sequence_scaled = x_scaler.transform(sequence)

    # Reshape
    # LSTM expects (1, 24, 6)

    sequence_scaled = sequence_scaled.reshape(
        1,
        24,
        6
    )

    # Predict Future Environment

    prediction = lstm_model.predict(
        sequence_scaled,
        verbose=0
    )

    # Convert Back to Original Scale

    prediction = y_scaler.inverse_transform(
        prediction
    )[0]

    # Store Results

    prediction_dict = {

        "indoor_temp_C": float(prediction[0]),

        "indoor_humidity": float(prediction[1]),

        "outdoor_temp_C": float(prediction[2]),

        "outdoor_humidity": float(prediction[3])

    }

    # Display Prediction

    print("\nPredicted Future Environmental Conditions")
    print("-" * 45)

    print(
        f"Indoor Temperature  : "
        f"{prediction_dict['indoor_temp_C']:.2f} °C"
    )

    print(
        f"Indoor Humidity     : "
        f"{prediction_dict['indoor_humidity']:.2f} %"
    )

    print(
        f"Outdoor Temperature : "
        f"{prediction_dict['outdoor_temp_C']:.2f} °C"
    )

    print(
        f"Outdoor Humidity    : "
        f"{prediction_dict['outdoor_humidity']:.2f} %"
    )

    # Return Prediction

    return prediction_dict    


def load_ppo_resources():

    global ppo_model
    global ppo_scaler

    ppo_model = PPO.load(PPO_MODEL_PATH)

    ppo_scaler = joblib.load(PPO_SCALER_PATH)



def predict_fan_decision(prediction_dict,
    occupancy):


    if ppo_model is None or ppo_scaler is None:

     raise RuntimeError(
        "PPO resources are not loaded. "
        "Call load_ppo_resources() first."
    )

    if occupancy not in [0,1]:

     raise ValueError(
        "Occupancy must be 0 or 1."
    )

    ppo_input = np.array([

     prediction_dict["indoor_temp_C"],

     prediction_dict["indoor_humidity"],
 
     prediction_dict["outdoor_temp_C"],

     prediction_dict["outdoor_humidity"],

     occupancy

]).reshape(1,-1)
    
    ppo_input_scaled = ppo_scaler.transform(
    ppo_input
)
    
    action, _ = ppo_model.predict(

    ppo_input_scaled,

    deterministic=True

)
    
    fan_status = "ON" if action == 1 else "OFF"


    analysis = []

    if occupancy == 0:

     analysis.append(
        "Room is currently unoccupied."
    )

    if prediction_dict["indoor_temp_C"] < 22:

     analysis.append(
        "Indoor temperature is below the comfort range."
    )

    elif prediction_dict["indoor_temp_C"] > 26:

     analysis.append(
        "Indoor temperature is above the comfort range."
    )

    else:

     analysis.append(
        "Indoor temperature is within the comfort range."
    )

    if prediction_dict["indoor_humidity"] < 40:

     analysis.append(
        "Indoor humidity is below the comfort range."
    )

    elif prediction_dict["indoor_humidity"] > 60:

     analysis.append(
        "Indoor humidity is above the comfort range."
    )

    else:

     analysis.append(
        "Indoor humidity is within the comfort range."
    )

    return {

     "fan_status": fan_status,

     "occupancy": occupancy,

     "analysis": analysis
}

# Generating Final Report

def generate_report(future_environment, decision):

    print("\n" + "=" * 70)
    print("               ENERGY OPTIMIZATION REPORT")
    print("=" * 70)

    # Predicted Environmental Conditions

    print("\nPredicted Future Environmental Conditions")
    print("-" * 45)

    print(
        f"Indoor Temperature  : "
        f"{future_environment['indoor_temp_C']:.2f} °C"
    )

    print(
        f"Indoor Humidity     : "
        f"{future_environment['indoor_humidity']:.2f} %"
    )

    print(
        f"Outdoor Temperature : "
        f"{future_environment['outdoor_temp_C']:.2f} °C"
    )

    print(
        f"Outdoor Humidity    : "
        f"{future_environment['outdoor_humidity']:.2f} %"
    )

    # Occupancy

    print("\nCurrent Occupancy")
    print("-" * 45)

    print(
        "Occupied"
        if decision["occupancy"] == 1
        else
        "Unoccupied"
    )

    # Environmental Analysis

    print("\nEnvironmental Analysis")
    print("-" * 45)

    for item in decision["analysis"]:

        print(f"• {item}")

    # AI Recommendation

    print("\nAI Recommendation")
    print("-" * 45)

    if decision["fan_status"] == "ON":

        print("Fan Status : 🟢 ON")

        print(
            "Recommendation : Cooling is recommended "
            "based on the predicted environmental conditions."
        )

    else:

        print("Fan Status : 🔴 OFF")

        print(
            "Recommendation : Cooling is not required "
            "under the predicted environmental conditions."
        )

    print("\n" + "=" * 70)
    print("Prediction Completed Successfully.")
    print("=" * 70)

# Main (Local Testing)

if __name__ == "__main__":

    load_lstm_resources()

    load_ppo_resources()

    df = validate_dataset("fan_data_clean.csv")

    future_environment = predict_future_environment(df)

    decision = predict_fan_decision(
        future_environment
    )

    generate_report(
        future_environment,
        decision
    )