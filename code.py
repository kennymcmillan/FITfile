import os
import fitparse
import pandas as pd
import streamlit as st
import base64


from PIL import Image
image = Image.open('Aspire_Academy_Logo_White.png') 


def parse_fit_file(file):
    # Load the .fit file
    fitfile = fitparse.FitFile(file)

    records = [record.get_values() for record in fitfile.get_messages('record')]
    df = pd.DataFrame.from_records(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    start_time = df['timestamp'].min()
    df['time'] = (df['timestamp'] - start_time).apply(lambda x: x.total_seconds() + 1)

    df = df.drop('unknown_87', axis=1)
    #df = df.drop('timestamp', axis=1)

    return df

def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download file to Downloads Folder</a>'
    st.markdown(href, unsafe_allow_html=True)


def app():

    st.set_page_config(page_title='Parse .fit File')
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.title("This is an app for downloading .FIT files as a csv file")
    file = st.sidebar.file_uploader('Upload .fit File', type='.fit')

    if file is not None:
        df = parse_fit_file(file)
        start_date = df['timestamp'].min().strftime('%d-%m-%Y')
        st.write(f"Date: {start_date}")

        time_col = df.pop('time')
        df.insert(0, 'time', time_col)
        df['time'] = df['time'].astype(int)
        df['distance'] = df['distance'].apply(lambda x: round(x, 1))

        st.write(df)

        if st.button('Process a CSV file'):
            download_csv(df)
            download_location = os.path.join(os.path.expanduser("~"), "Downloads")


# Run the Streamlit app
if __name__ == '__main__':
    app()
