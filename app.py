# ==============================
# IMPORT LIBRARIES
# ==============================

import streamlit as st
import matplotlib.pyplot as plt

from text_analysis import analyze_profile
from image_analysis import analyze_image

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="LinkedIn Profile Auditor",
    layout="wide"
)

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title(" LinkedIn Profile Auditor")

st.sidebar.info(
    """
    This application analyzes LinkedIn profiles using:

    ✔ NLP-Based Text Analysis

    ✔ Profile Photo Analysis

    ✔ Professional Scoring System

    ✔ Personalized Recommendations
    """
)

# ==============================
# PAGE TITLE
# ==============================

st.title(" LinkedIn Profile Auditor")

st.markdown(
    """
    Upload your LinkedIn profile content and profile photo
    to receive a professional evaluation score and
    personalized recommendations.
    """
)

# ==============================
# TEXT ANALYSIS SECTION
# ==============================

st.header(" LinkedIn Text Analysis")

text = st.text_area(
    "Paste your LinkedIn profile summary"
)

# ==============================
# IMAGE ANALYSIS SECTION
# ==============================

st.header("📷 Profile Photo Analysis")

uploaded_file = st.file_uploader(
    "Upload Profile Photo",
    type=["jpg", "jpeg", "png"]
)

# ==============================
# IMAGE PREVIEW
# ==============================

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Profile Photo",
        width=250
    )

# ==============================
# ANALYZE BUTTON
# ==============================

if st.button("Analyze Profile"):

    if text and uploaded_file is not None:

        with st.spinner("Analyzing Profile..."):

            # ==============================
            # TEXT ANALYSIS
            # ==============================

            result = analyze_profile(text)

            # ==============================
            # IMAGE ANALYSIS
            # ==============================

            image_result = analyze_image(uploaded_file)

            # ==============================
            # FINAL SCORE
            # ==============================

            final_score = (
                result["score"] +
                image_result["photo_score"]
            ) / 2

        # ==============================
        # RESULTS SECTION
        # ==============================

        st.header(" Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Text Score",
                result["score"]
            )

        with col2:
            st.metric(
                "Photo Score",
                image_result["photo_score"]
            )

        with col3:
            st.metric(
                "Final Score",
                round(final_score, 2)
            )

        # ==============================
        # PROFILE EVALUATION
        # ==============================

        st.subheader(" Profile Evaluation")

        if final_score >= 80:

            st.success(
                "Excellent LinkedIn Profile"
            )

        elif final_score >= 60:

            st.info(
                "Good LinkedIn Profile"
            )

        elif final_score >= 40:

            st.warning(
                "Average LinkedIn Profile"
            )

        else:

            st.error(
                "LinkedIn Profile Needs Improvement"
            )

        # ==============================
        # SKILLS DETECTED
        # ==============================

        st.subheader(" Skills Detected")

        if result["skills_found"]:

            for skill in result["skills_found"]:
                st.success(skill)

        else:

            st.warning(
                "No technical skills detected."
            )

        # ==============================
        # PHOTO ANALYSIS RESULTS
        # ==============================

        st.subheader(" Photo Analysis")

        st.write(
            "Face Detected:",
            image_result["face_detected"]
        )

        st.write(
            "Brightness:",
            image_result["brightness"]
        )

        # ==============================
        # OPEN TO WORK DETECTION
        # ==============================

        if image_result["open_to_work"]:

            st.warning(
                "⚠ Open to Work frame detected. "
                "This may affect profile professionalism."
            )

        else:

            st.success(
                "✔ Professional profile image detected."
            )

        # ==============================
        # SCORE VISUALIZATION
        # ==============================

        st.subheader(" Score Visualization")

        scores = [
            result["score"],
            image_result["photo_score"],
            final_score
        ]

        labels = [
            "Text Score",
            "Photo Score",
            "Final Score"
        ]

        fig, ax = plt.subplots(figsize=(5,3))

        ax.bar(labels, scores,width=0.4)

        ax.set_ylim(0, 100)

        ax.set_ylabel("Score")

        st.pyplot(fig)

        # ==============================
        # SUGGESTIONS
        # ==============================

        st.subheader(" Suggestions")

        if result["suggestions"]:

            for suggestion in result["suggestions"]:

                st.warning(suggestion)

        else:

            st.success(
                "Your profile looks strong and professional."
            )

        # ==============================
        # FINAL RECOMMENDATIONS
        # ==============================

        st.subheader(" Final Recommendations")

        if image_result["photo_score"] < 70:

            st.warning(
                "Use a brighter and more professional profile image."
            )

        if result["score"] < 70:

            st.warning(
                "Improve profile content and add more technical skills."
            )

        if final_score >= 80:

            st.success(
                "Your LinkedIn profile looks professional and well-structured."
            )

    else:

        st.warning(
            "Please enter profile text and upload a profile image."
        )

# ==============================
# FOOTER
# ==============================

st.markdown("---")

st.caption(
    "LinkedIn Profile Auditor | Sprint 5 Integrated System"
)