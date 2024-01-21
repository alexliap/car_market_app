import streamlit as st

st.set_page_config(initial_sidebar_state="expanded")

st.title('Homepage')

st.markdown('This is a demo app for the ML course of MSc Program in AI by University of Piraeus and NCSR Demokritos. '
            'For this project, car listing data was collected along with vehicle features for the corresponding VIN numbers. '
            'In the homepage, the user can see various stats about the data collected.\n\n'
            'Two extra features of the demo app are:\n'
            '- Price Recommendation, where the user gets a suggestion of how he should price his car.\n'
            '- Car Recommendation, where the user inputs a car and gets recommended with up to five similar cars.')

# if __name__ == '__main__':