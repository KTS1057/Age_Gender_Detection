import os
import tempfile

import streamlit as st

from predict import predict_image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Age & Gender Detection",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():

    css_path = os.path.join(
        "static",
        "css",
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🤖 AI Age & Gender Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload a facial image for prediction</div>',
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD IMAGE
# ============================================================

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)


# ============================================================
# IMAGE PREVIEW
# ============================================================

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width=450
    )

    st.write("")

    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    if st.button(
        "🔍 Predict",
        type="primary",
        use_container_width=True
    ):

        temp_path = None

        try:

            extension = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name

            # =================================================
            # PREDICTION
            # =================================================

            with st.spinner("Analyzing image..."):

                age, gender = predict_image(
                    temp_path
                )

            st.success(
                "Prediction completed successfully!"
            )

            # =================================================
            # RESULT
            # =================================================

            st.markdown(
                '<div class="result-title">Prediction Result</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    label="PREDICTED AGE",
                    value=f"{age} years"
                )

            with col2:

                st.metric(
                    label="PREDICTED GENDER",
                    value=gender
                )

        except Exception as error:

            st.error(
                f"Prediction failed: {error}"
            )

        finally:

            if (
                temp_path is not None
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)

else:

    st.info(
        "Upload an image to start prediction."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">AI Age & Gender Detection</div>',
    unsafe_allow_html=True
)