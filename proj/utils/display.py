import streamlit as st # creates a display item upon request, used in dashboard mainly
def show_dataframe_box(df, title=""):
    if title:
        st.subheader(title)
    if df.empty:
        st.info("No data to display.")
        return
    with st.container():
        st.dataframe(df)
