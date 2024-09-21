# page2.py
import streamlit as st

st.title('page2')

# Insert containers separated into tabs:
tab1, tab2, tab3, tab4 = st.tabs(['Tab 1', 'Tab2', 'Tab3', 'Tab4'])

# You can also use "with" notation:
with tab4:
    st.radio('Select one:', [1, 2])
    st.write('this is tab 1')

with tab2:
    st.radio('Select one:', [3, 4])
    st.write('this is tab 2')

with tab3:
    st.title('app')
    st.json({'foo': 'bar', 'fu': 'ba'})

with tab1:
    if 'value' not in st.session_state:
        st.session_state.value = 'Title2'

    ##### Option using st.rerun #####
    st.header(st.session_state.value)

    if st.button('Foo'):
        st.session_state.value = 'Foo'
        st.rerun()

    if st.toggle('Activate feature'):
        st.write('Feature activated!')
