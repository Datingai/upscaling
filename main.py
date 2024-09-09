import streamlit as st
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from PIL import Image
import requests
import io
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Streamlit app
st.title("Image Upscaling with Cloudinary")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Generate a unique filename to avoid caching issues
    unique_filename = f"temp_image_{uuid.uuid4().hex}.jpg"

    # Save uploaded file temporarily
    with open(unique_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    st.image(unique_filename, caption="Uploaded Image", use_column_width=True)

    # Select upscale factor
    scale_factor = st.slider("Select Upscale Factor", 1, 4, 2)

    # Generate button
    if st.button("Upscale Image"):
        # Upload the image to Cloudinary
        public_id = f"upscale-image-{uuid.uuid4().hex}"
        upload_result = cloudinary.uploader.upload(unique_filename, public_id=public_id)
        
        # Generate the upscaled image URL with upscale effect
        upscaled_image_url, _ = cloudinary_url(
            public_id,
            effect=f"upscale:scale_{scale_factor}"
        )
        
        # Load images
        original_image = Image.open(unique_filename)

        # Fetch the upscaled image from the generated URL
        response = requests.get(upscaled_image_url)
        upscaled_image = Image.open(io.BytesIO(response.content))

        # Display images
        st.subheader("Compare Images")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(original_image, caption="Original Image", use_column_width=True)
        
        with col2:
            st.image(upscaled_image, caption="Upscaled Image", use_column_width=True)
    
    # Clean up the temporary file
    os.remove(unique_filename)
