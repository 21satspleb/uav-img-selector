import streamlit as st
st.set_page_config(
    page_title="1_Load Images",
    page_icon=":minidisc:",
    layout="wide",
    initial_sidebar_state="expanded")

from uav_img_toolbox.classes.UAVImages import UAVImages


st.markdown("""
## Loading your images!
""")

# Options for the selectbox
options = ["None", "demo", "data"]

# Use a selectbox for directory selection
directory = st.selectbox("Select a directory", options)

# Check if directory is not "None"
if directory != "None":
    # Create a UAVImages object
    # Always update the UAVImages object with the new directory
    st.session_state.uav_images = UAVImages(directory)
  
    # Display the images

    # Create a progress bar
    progress_bar = st.progress(0)

    # Use the create_image_dict method to process the images and update the progress bar
    st.session_state.uav_images.create_image_dict(progress_bar)

    # Display a success message
    st.write(f"Finished processing {len(st.session_state.uav_images.image_dict)} images!")
else:
    st.write("Please select a directory to begin.")

