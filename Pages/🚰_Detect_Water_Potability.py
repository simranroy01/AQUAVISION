import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import pickle


# Load and preprocess data
@st.cache_resource
def load_data():
    # Assuming the CSV file is available in the same directory
    df = pd.read_csv("water_potability.csv")

    # Impute missing values for the numeric columns using a simple strategy
    df.fillna(df.mean(), inplace=True)

    # Define feature columns and target
    X = df.drop(columns=["Potability"])
    y = df["Potability"]

    # Scale the features using MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = load_data()


# Train the model
@st.cache_resource
def train_model():
    # Initialize the RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)

    # Fit the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save the model to a pickle file
    with open("best_model.pkl", "wb") as file:
        pickle.dump(model, file)

    return model


model = train_model()


# Streamlit app interface
def main():
    st.title("Water Potability Prediction")
    st.write("Enter the water quality parameters to predict if the water is potable or not.")

    # User inputs
    ph = st.number_input("pH Value", min_value=0.0, max_value=14.0, step=0.1)
    hardness = st.number_input("Hardness (mg/L)", min_value=0.0, step=0.1)
    solids = st.number_input("Solids (ppm)", min_value=0.0, step=1.0)
    chloramines = st.number_input("Chloramines (ppm)", min_value=0.0, step=0.1)
    sulfate = st.number_input("Sulfate (mg/L)", min_value=0.0, step=0.1)
    conductivity = st.number_input("Conductivity (μS/cm)", min_value=0.0, step=0.1)
    organic_carbon = st.number_input("Organic Carbon (mg/L)", min_value=0.0, step=0.1)
    trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=0.0, step=0.1)
    turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, step=0.1)

    # Predict button
    if st.button("Predict"):
        # Collect the inputs as an array
        user_data = np.array(
            [[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

        # Scale the user data using MinMaxScaler (same scaler used during training)
        scaler = MinMaxScaler()
        user_data_scaled = scaler.fit_transform(user_data)

        # Use the trained model to make a prediction
        prediction = model.predict(user_data_scaled)

        # Display the result
        if prediction[0] == 1:
            st.success("The water is potable (safe to drink).")
        else:
            st.error("The water is not potable (not safe to drink).")


if __name__ == "__main__":
    main()
