# Import
import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth

import pandas as pd
from db_fcns_core import create_table, add_data, view_data, edit_data, del_data


# --- USER AUTHENTICATION ---
usernames = ['kc','ss']
names = ['Ken','Suzy']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names,
                                    usernames,
                                    hashed_passwords,
                                    "webtoken_cookie",
                                    "abcdef",
                                    30)

name, authentication_status, username = authenticator.login('Login','main')

if authentication_status is False:
    st.error('Username/password is incorrect')

if authentication_status is None:
    st.warning('Please enter your username and password')

if authentication_status:
    if name[0]:
        st.write(f'Welcome *{name}*!')
    def main():
        st.title('Food Tracker')
    # Create table
        create_table()

        # Food input with 4 columns of food, count, expiration date, and submit button
        input_col1, input_col2, input_col3, input_col4 = st.columns([2, 2, 1, 1])

        with input_col1:
            food = st.text_input("Food")

        with input_col2:
            count = st.number_input("Count", step=1)

        with input_col3:
            exp_date = st.date_input("Expiration Date")

        with input_col4:
            # Insert item
            if st.button("Add Item"):
                add_data(food, count, exp_date)

        # Changing data
        with st.expander("Alter Data"):
            with st.form("Edit Form"):
                # Use the DataFrame index to select the row to edit or delete
                row_to_edit = st.number_input("Row Index to Change", min_value=1, step=1)
                new_col1, new_col2, new_col3 = st.columns([2,1,1])
                with new_col1:
                    new_food = st.text_input("New Food")
                with new_col2:
                    new_count = st.number_input("New Count", step=1)
                with new_col3:
                    new_exp_date = st.date_input("New Expiration Date")
                new_button_col1, new_button_col2 = st.columns([1,1])
                # Editing
                with new_button_col1:
                    edit_button = st.form_submit_button("Edit")
                if edit_button:
                    edit_data(row_to_edit,new_food,new_count,new_exp_date)
                # Deleting
                with new_button_col2:
                    delete_button = st.form_submit_button("Delete")
                if delete_button:
                    del_data(row_to_edit)

        # Viewing the data
        result = view_data()
        # Display the sorted DataFrame
        df = pd.DataFrame(result, columns=['Food', 'Count', 'Expiration Date'])
        # Set index starting at 1
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        st.dataframe(df)
    
    authenticator.logout('Logout','sidebar')

    if __name__ == '__main__':
        main()



