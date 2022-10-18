from Utils import utils
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Stock Performance",
    page_icon="📈",
    layout="wide")

st.title('Compare Stock performance')
index_option = st.selectbox( 'How would you like to be contacted?', utils.index_list())
dropdown=st.multiselect("Pick your assets", utils.get_stock_list(index_option))
year_slider=st.slider("Choose Year", min_value=2010,max_value=utils.cur_year(), step=1)
if len(dropdown) > 0:
    df = utils.relative_return(
        yf.download(dropdown,period = "1d", interval = "1m")['Adj Close'])
    st.line_chart(df)
