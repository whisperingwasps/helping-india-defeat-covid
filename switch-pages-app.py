import SessionState
import streamlit as st
import io
import pandas as pd
import base64


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


st.set_page_config(
    page_icon=":shark:",
    layout="wide",
)


def pageZero(sesh):
    st.title("Ask for Help")
    st.write(
        "some text for zeroth page. Welcome to the app. Follow the nav buttons above to move forward and backwards one page"
    )


def pageOne(sesh):
    st.title("Find useful Contacts")
    st.write("Contacts:")


def pageTwo(sesh):
    st.title("Give Help to someone")
    st.write("Contribute to the Site:")


sesh = SessionState.get(curr_page=0)
PAGES = [pageZero, pageOne, pageTwo]


def main():
    ####SIDEBAR STUFF
    st.sidebar.title("this is an app:")

    st.sidebar.markdown(
        "Might be easier to import the pageOne/pageTwo/pageThree from a separate file to make the code cleaner"
    )

    #####MAIN PAGE NAV BAR:
    st.sidebar.markdown(" ### Navigation")
    st.sidebar.markdown("Choose a page to proceed:")
    genre = st.sidebar.radio(
        "What do you want us to help you with?",
        ("Ask for Help", "Find Contacts", "Give help"),
    )
    if genre == "Ask for Help":
        sesh.curr_page = 0
    elif genre == "Find Contacts":
        sesh.curr_page = 1
    elif genre == "Give help":
        sesh.curr_page = 2

    st.sidebar.markdown("----------------------------------")

    #####MAIN PAGE APP:
    st.write("PAGE NUMBER:", sesh.curr_page)
    page_turning_function = PAGES[sesh.curr_page]
    st.write(sesh.curr_page)
    page_turning_function(sesh)

    # Examples


if __name__ == "__main__":
    main()