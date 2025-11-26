import streamlit as st
import requests
import os

API_BASE = "https://autonomous-qa-agent-rik3.onrender.com"

st.title('Autonomous QA Agent')

# Ensure uploads folder exists
os.makedirs('uploads', exist_ok=True)

uploaded_files = st.file_uploader('Upload support documents', accept_multiple_files=True)
checkout_file = st.file_uploader('Upload checkout.html', type=['html'])

if st.button('Build Knowledge Base'):
    files = []
    for f in uploaded_files:
        path = os.path.join('uploads', f.name)
        with open(path, 'wb') as out:
            out.write(f.getbuffer())
        files.append(('files', (f.name, open(path, 'rb'), 'application/octet-stream')))
    if checkout_file:
        ch_path = os.path.join('uploads', checkout_file.name)
        with open(ch_path, 'wb') as out:
            out.write(checkout_file.getbuffer())
        checkout_payload = ('checkout_html', (checkout_file.name, open(ch_path, 'rb'), 'text/html'))
    else:
        checkout_payload = None
    with st.spinner('Uploading and building...'):
        url = API_BASE + '/ingest/upload'
        multipart = files
        if checkout_payload:
            multipart.append(checkout_payload)
        resp = requests.post(url, files=multipart)
        st.write(resp.json())

query = st.text_input('Agent query', value='Generate all positive and negative test cases for the discount code feature.')

if st.button('Generate Test Cases'):
    resp = requests.post(API_BASE + '/agent/generate_test_cases', json={'query': query})
    try:
        data = resp.json()
        st.write(data)
    except Exception:
        st.error("Backend did not return JSON. See raw response below.")
        st.text(resp.text)

selected = st.text_area('Paste one test case JSON to generate Selenium script')

checkout_path = st.text_input('Path to checkout.html', value='uploads/checkout.html')

if st.button('Generate Selenium Script'):
    try:
        tc = eval(selected)
    except Exception:
        tc = None

    resp = requests.post(
        API_BASE + '/agent/generate_selenium',
        json={'test_case': tc, 'checkout_html_path': checkout_path}
    )

    try:
        data = resp.json()
        try:
            data = resp.json()
            st.code(data.get('script', 'No script returned'))
        except Exception:
            st.error("Backend returned invalid response. See raw output below.")
            st.text(resp.text)
    except Exception:
        st.error("Backend returned invalid response. Check FastAPI console for errors.")
        st.text(resp.text)
