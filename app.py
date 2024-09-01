import datetime

import streamlit as st

st.title('❶Hello Worldアプリ')

_name = st.text_input('あなたの名前は？', '小泉')

if st.button('このボタンを押すと挨拶を返してくれます'):
    if len(_name):
        _hour = datetime.datetime.now().hour
        if 4 <= _hour < 12:
            f'**おはようございます、{_name}さん**'
        elif 12 <= _hour < 18:
            f'**こんにちは、{_name}さん**'
        else:
            f'**こんばんは、{_name}さん**'

st.divider()

fruit = st.radio('どちらのほうがお好きですか？', ['みかん', 'りんご'])
if st.button('決めました'):
    f'**そうですか、『{fruit}』って美味しいですものね。**'

st.sidebar.text_input('text input')
st.sidebar.text_area('text area')
st.sidebar.slider('slider', 0, 100, 50)
st.sidebar.file_uploader('Choose file')

# import anthropic

# client = anthropic.Anthropic()
# message = client.messages.create(
#     model="claude-3-opus-20240229",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": "Hello, Claude"}
#     ]
# )

# st.write(message.content[0].text)
