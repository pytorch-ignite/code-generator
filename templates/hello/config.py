import streamlit as st


def get_configs() -> dict:
    """Example Config.
    """
    config = {}
    st.info("Very simple single file template.")

    config["say"] = st.selectbox("Say", ("Hello", "Goodbye"))
    config["user"] = st.text_input("User Name", value="Ignite")
    return config
