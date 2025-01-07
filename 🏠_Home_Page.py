import streamlit as st


def main():
    st.set_page_config(page_title="Water Analysis App", layout="centered")

    # Add a title and header for the homepage
    st.title("Welcome to the Water Analysis App: AQUAVISION")

    # Add an image with a smaller size
    st.image("Water-Sampling-2048x1365.jpg", width=500, caption="Making Water Analysis Accessible for Everyone")

    st.header("✨ WHAT WE DO? ✨")

    # Add descriptions of the app's features with more styling
    st.markdown("""
    <div style="background-color:#e6f7ff; padding:20px; border-radius:10px;">
    <h3 style="color:#007acc;">1. Water Potability Analysis</h3>
    <ul style="color:#333;">
        <li>Enter values of various water quality parameters such as <b>pH</b>, <b>hardness</b>, <b>chloramines</b>, <b>sulfates</b>, and more.</li>
        <li>Determine if the water is <b>potable</b> (safe for drinking) or not using advanced analysis.</li>
    </ul>

    <h3 style="color:#007acc;">2. Underwater Image Analysis</h3>
    <ul style="color:#333;">
        <li>Upload an underwater image.</li>
        <li>Detect and classify objects such as <b>trash</b>, <b>water organisms</b>, <b>machines</b>, and other underwater elements using <b>computer vision</b>.</li>
    </ul>

    <h3 style="color:#007acc;">3. Interactive Water Turbidity Analysis</h3>
    <ul style="color:#333;">
        <li>Select a specific area on an <b>interactive map</b> containing rivers or oceans.</li>
        <li>Analyze the <b>water turbidity</b> in the selected area.</li>
        <li>Visualize turbidity levels with <b>color variations</b>, making it easy to interpret the data.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Add a footer
    st.markdown("""
    <hr style="border:1px solid #dcdcdc;">
    <p style="text-align:center;">🌟 Explore the features using the navigation menu on the left. 🌟</p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
