import streamlit as st
import os
from uav_img_toolbox.classes.UAVImages import UAVImages

def st_dir_selector(st_placeholder, path='.', label='Please, select a folder...'):
    base_path = '.' if path is None or path == '' else path
    base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    base_path = '.' if base_path is None or base_path == '' else base_path

    directories = [f.name for f in os.scandir(base_path) if f.is_dir()]
    if not directories:
        return None

    # Get the directory name from the path to be used as the default value
    default_directory = os.path.basename(path)
    # If the default directory is not in the list of directories, set the index to 0
    if default_directory not in directories:
        default_index = 0
    else:
        default_index = directories.index(default_directory)

    selected_directory = st_placeholder.selectbox(label, directories, index=default_index)
    return os.path.join(base_path, selected_directory)


# Define functions for each page
def home_page():
    st.title("Welcome to the UAV Image Metadata Explorer!")

    # Create a placeholder for the directory selection
    dir_placeholder = st.empty()

    # Let the user select a directory
    directory = st_dir_selector(dir_placeholder)

    # If the user has selected a directory, process the images in that directory
    if directory:
        # Create a UAVImages object
        uav_images = UAVImages(directory)

        # Create a progress bar
        progress_bar = st.progress(0)

        # Use the create_image_dict method to process the images and update the progress bar
        uav_images.create_image_dict(progress_bar)

        # Display a success message
        st.write(f"Finished processing {len(uav_images.image_dict)} images!")
    else:
        st.write("Please select a directory to begin.")

def image_metadata_page():
  st.title("Image Metadata")

# Define a dictionary to map page names to functions
pages = {
    "Import Images": home_page,
    "Image Metadata Explorer": image_metadata_page,
}

# In the sidebar, let the user select a page using buttons
for page_name in pages.keys():
    if st.sidebar.button(page_name):
        # If the user clicks a button, render the corresponding page
        pages[page_name]()
