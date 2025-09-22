# Simple Streamlit App for Universal File to Text Conversion
# This application provides a clean UI for users to upload various
# document types and convert them into a downloadable text file.

# 1. Quietly install required packages
# This command ensures that 'markitdown' and its dependencies are available
# in the Streamlit environment without displaying verbose installation logs.
!pip install -q markitdown[all]

import streamlit as st
import os
import tempfile
from markitdown import MarkItDown

def convert_file_to_text(file_path):
    """
    Function to convert a single file to text using the MarkItDown library.

    Args:
        file_path (str): The local path to the file to be converted.

    Returns:
        str: The converted text content of the file.
        None: If an error occurs during conversion.

    The function initializes a MarkItDown object and uses its 'convert' method
    to process the file, handling common exceptions.
    """
    try:
        # Initialize MarkItDown with a preference for text content
        # by disabling Markdown formatting.
        md = MarkItDown(enable_plugins=False)
        
        # Convert the file and get the result object
        result = md.convert(file_path)
        
        # Return the extracted text content
        return result.text_content

    except Exception as e:
        st.error(f"Error converting file: {e}")
        return None

# --- Main Streamlit App UI and Logic ---

# Set the title of the Streamlit app
st.title("Universal File to Text Converter")
st.write("Drag and drop a file below to convert it to plain text.")

# Step 1: Handle file upload
# The st.file_uploader widget provides a simple drag-and-drop area.
# It returns the uploaded file object.
uploaded_file = st.file_uploader(
    "Choose a file", 
    type=["docx", "xlsx", "pptx", "html", "txt", "zip", "pdf", "rtf", "md"]
)

# Step 2: Process the file if it has been uploaded
if uploaded_file is not None:
    # Use a temporary file to save the uploaded content
    # This is necessary because the markitdown library expects a file path,
    # not a Streamlit file object.
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
        
    # Process the temporary file
    text_content = convert_file_to_text(temp_file_path)

    # Clean up the temporary file after processing
    os.remove(temp_file_path)

    if text_content:
        # Step 3: Display a preview of the converted text
        st.subheader("Text Preview (First 1000 characters)")
        preview_text = text_content[:1000]
        st.text_area("Preview", preview_text, height=300)

        # Step 4: Offer a download option for the full text
        output_filename = os.path.splitext(uploaded_file.name)[0] + ".txt"
        st.download_button(
            label="Download Full Text",
            data=text_content,
            file_name=output_filename,
            mime="text/plain",
            help="Click to download the complete converted text file."
        )
