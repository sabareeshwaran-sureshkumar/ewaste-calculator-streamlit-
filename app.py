import streamlit as st
import numpy as np
import joblib
from io import BytesIO
import pandas as pd

# Load models and scaler
reward_model = joblib.load("reward_model.pkl")
recyclable_model = joblib.load("recyclable_model.pkl")
scaler = joblib.load("scaler.pkl")
le_device = joblib.load("le_device.pkl")

# Function to predict using the model
def calculate_with_model(device_type, component_scores):
    # Label encode device type
    device_type_encoded = le_device.transform([device_type])[0]
    
    # Combine input features
    component_features = [device_type_encoded] + component_scores
    
    # Scale features
    X_scaled = scaler.transform([component_features])
    
    # Predict reward and recyclability
    predicted_reward = reward_model.predict(X_scaled)[0]
    predicted_recyclable = recyclable_model.predict(X_scaled)[0]
    
    return predicted_reward, predicted_recyclable

# Generate a detailed report with inline CSS
def generate_report_html(device_type, component_scores, predicted_reward, predicted_recyclable, waste_reduced, co2_reduced, other_savings):
    component_names = device_components[device_type]
    
    report_html = f"""
    <html>
    <head>
    <style>
    body {{
        font-family: Arial, sans-serif;
        margin: 20px;
        padding: 20px;
        border: 2px solid #457B9D;
        background-color: #F1FAEE;
        color: #1D3557;
    }}
    h1 {{
        text-align: center;
        color: #E63946;
    }}
    h2 {{
        color: #457B9D;
    }}
    .container {{
        padding: 10px;
        margin-bottom: 15px;
    }}
    .content {{
        margin-bottom: 20px;
    }}
    .savings {{
        padding: 10px;
        border: 1px solid #1D3557;
        margin: 10px;
        background-color: #A8DADC;
    }}
    .score {{
        font-size: 1.2em;
        font-weight: bold;
    }}
    </style>
    </head>
    <body>
        <h1>Environmental Savings Detailed Report</h1>
        <div class="content">
            <h2>Device Type: {device_type}</h2>
            <p class="score">Predicted Reward: ${predicted_reward:.2f}</p>
            <p class="score">Predicted Recyclable Score: {predicted_recyclable:.2f}</p>
        </div>

        <h2>Component Scores and Details:</h2>
        <ul>
    """
    
    for component, score in zip(component_names, component_scores):
        report_html += f"<li>{component} Score: {score} - Contribution to sustainability: {score * 2}% reduction in waste.</li>"
    
    report_html += f"""
        </ul>

        <div class="savings">
            <h2>Environmental Savings:</h2>
            <p><strong>Metals Saved:</strong> Copper, Aluminum, Gold</p>
            <p><strong>Waste Reduced:</strong> {waste_reduced:.2f} kg</p>
            <p><strong>CO2 Emission Reduced:</strong> {co2_reduced:.2f} kg</p>
            <p><strong>Other Environmental Savings:</strong> {other_savings:.2f}</p>
        </div>

        <div class="content">
            <p>Thank you for your contribution to a sustainable future! Your efforts to recycle your device have helped reduce environmental damage and saved precious materials from being wasted.</p>
        </div>
    </body>
    </html>
    """
    
    return report_html

# Generate a certificate with inline CSS styling
def generate_certificate_html(name, device_type, co2_reduced):
    certificate_content = f"""
    <div style='padding: 30px; border: 10px solid #1D3557; width: 80%; margin: auto; background-color: #F1FAEE;'>
        <h1 style='text-align: center; font-family: Georgia, serif; color: #457B9D; font-size: 40px;'>CERTIFICATE OF APPRECIATION</h1>
        <p style='text-align: center; font-size: 18px; font-family: Arial, sans-serif;'>This certificate is proudly presented to:</p>
        <h2 style='text-align: center; font-family: Arial, sans-serif; color: #E63946; font-size: 30px;'>{name}</h2>
        <p style='text-align: center; font-size: 18px; font-family: Arial, sans-serif;'>
            For contributing to environmental sustainability by recycling your <b>{device_type}</b>,
            and helping to reduce CO2 emissions by <b>{co2_reduced:.2f} kg</b>.
        </p>
        <p style='text-align: center; font-size: 18px; font-family: Arial, sans-serif;'>Your efforts are making a positive impact on the planet!</p>
        <div style='text-align: center; margin-top: 50px;'>
            <p style='font-size: 16px; font-family: Georgia, serif;'>E-Waste Environmental Savings Team</p>
        </div>
    </div>
    """
    return certificate_content

# Function to download content as a file
def download_file(content, filename):
    b = BytesIO()
    b.write(content.encode())
    b.seek(0)
    return b

# Components for each device type (7 features for each device)
device_components = {
    "Mobile": ["Display", "Processor", "Battery", "Camera", "Plastics", "Metals", "Memory"],
    "Laptop": ["Display", "CPU", "Battery", "Keyboard", "Trackpad", "Plastics", "Metals"],
    "Refrigerator": ["Compressor", "Thermostat", "Insulation", "Plastic", "Metal Shelves", "Door Seal", "Refrigerant"],
    "Television": ["Display", "Circuit Board", "Speakers", "Plastics", "Metals", "Cables", "Power Supply"],
    "Accessories": ["Cables", "Connectors", "Battery", "Plastics", "Metals", "Power Adapter", "PCB"],
    "Other": ["Component 1", "Component 2", "Component 3", "Component 4", "Component 5", "Component 6", "Component 7"]
}

# Streamlit app layout
def main():
    st.title("E-Waste Environmental Savings Calculator")
    
    # User input for name
    name = st.text_input("Enter Your Name", "Your Name")
    
    # User input for device type
    device_type = st.selectbox("Select Device Type", list(device_components.keys()))
    
    st.write("### Enter Component Scores (1-50):")
    
    # Display sliders for the 7 components based on the device type
    components = device_components[device_type]
    component_scores = []
    
    for component in components:
        score = st.slider(f"{component} Score", 1, 50, 25)
        component_scores.append(score)
    
    if st.button("Calculate"):
        predicted_reward, predicted_recyclable = calculate_with_model(device_type, component_scores)
        
        # Simulate environmental savings
        waste_reduced = np.random.uniform(10, 30)  # Waste reduced in kg
        co2_reduced = np.random.uniform(5, 15)  # CO2 emission reduced in kg
        other_savings = np.random.uniform(5, 20)  # Other environmental savings
        
        # Display Results
        st.write(f"**Predicted Reward:** ${predicted_reward:.2f}")
        predicted_recyclable = predicted_recyclable * 10
        st.write(f"**Predicted Recyclable Score (scaled):** {predicted_recyclable:.2f}")
        
        st.write("### Environmental Savings Report:")
        metals_saved = "Copper, Aluminum, Gold"
        st.write(f"**Metals Saved:** {metals_saved}")
        st.write(f"**Waste Reduced:** {waste_reduced:.2f} g")
        st.write(f"**CO2 Emission Reduced:** {co2_reduced:.2f} g")
        st.write(f"**Other Environmental Savings:** {other_savings:.2f}")
        
        # Generate the detailed report
        report_html = generate_report_html(device_type, component_scores, predicted_reward, predicted_recyclable, waste_reduced, co2_reduced, other_savings)
        
        # Generate the certificate content with HTML and CSS styling
        certificate_html = generate_certificate_html(name, device_type, co2_reduced)

        # Download buttons for report and certificate
        st.download_button("Download Detailed Report", download_file(report_html, "environmental_savings_report.html"), file_name="environmental_savings_report.html")
        
        st.markdown(certificate_html, unsafe_allow_html=True)
        
        st.download_button("Download Certificate", download_file(certificate_html, "certificate.html"), file_name="certificate.html")

if __name__ == "__main__":
    main()
