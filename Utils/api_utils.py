import requests,json
from datetime import datetime
import pandas as pd


def edelweiss_OptionChain_Df_v1(expiry, scrip):
    # url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)
    jsoned_response = response.json()
    df = pd.json_normalize(jsoned_response['opChn'])
    new_df = df[['stkPrc', 'atm',
                 # 'ceQt.trdSym',
                 'ceQt.ltp', 'ceQt.chg', 'ceQt.chgP',
                 'ceQt.bidPr', 'ceQt.askPr', 'ceQt.vol',
                 'ceQt.opInt', 'ceQt.opIntChg',
                 'ceQt.ltpivfut', 'ceQt.ltpivspt',
                 # 'peQt.trdSym',
                 'peQt.ltp', 'peQt.chg', 'peQt.chgP',
                 'peQt.bidPr', 'peQt.askPr', 'peQt.vol',
                 'peQt.opInt', 'peQt.opIntChg',
                 'peQt.ltpivfut', 'peQt.ltpivspt',
                 # ]].apply(pd.to_numeric)
                 ]]

    # new_df.set_index('stkPrc', inplace=True)
    strike_list=list(df['stkPrc'].astype(float).astype(int))


    put_oi  =sum(df['peQt.opInt'].astype(float))
    call_oi =sum(df['ceQt.opInt'].astype(float))
    pcr = round(put_oi / call_oi, 2)

    # return round(put_oi,2),round(call_oi,2),pcr, strike_list, new_df
    return strike_list, new_df


def recordData(expiry, scrip):
    # url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)

    jsoned_response = response.json()
    data_length = len(jsoned_response['opChn'])

    url = "https://ewmw.edelweiss.in/api/Market/Process/GetMarketStatus/20559,26753"
    atmresponse = requests.get(url)
    jsoned_atmresponse = atmresponse.json()
    jsoned_atmresponse = json.loads(jsoned_atmresponse)
    if scrip == "NIFTY":
        atm = jsoned_atmresponse['JsonData']['NSE']
        atm = round(atm / 50) * 50
    if scrip == "BANKNIFTY":
        atm = jsoned_atmresponse['JsonData']['BSE']
        atm = round(atm / 100) * 100

    # print("ATM: ", atm)

    oiData = []
    atm_premium = 0

    for i in range(data_length):
        strike = jsoned_response['opChn'][i]['stkPrc']
        strike = int(float(strike))
        ce_premium = jsoned_response['opChn'][i]['ceQt']['ltp']
        pe_premium = jsoned_response['opChn'][i]['peQt']['ltp']
        ce_oi = jsoned_response['opChn'][i]['ceQt']['opInt']
        pe_oi = jsoned_response['opChn'][i]['peQt']['opInt']
        ce_oichg = jsoned_response['opChn'][i]['ceQt']['opIntChg']
        pe_oichg = jsoned_response['opChn'][i]['peQt']['opIntChg']

        temp_dict = {}

        temp_dict['strike'] = strike
        if strike == atm:
            atm_premium = float(ce_premium) + float(pe_premium)

        temp_dict['ceOI'] = ce_oi
        temp_dict['peOI'] = pe_oi
        temp_dict['ceOIchg'] = ce_oichg
        temp_dict['peOIchg'] = pe_oichg

        oiData.append(temp_dict)

    print(atm_premium)
    time_now = datetime.now()
    time_now = time_now.strftime("%H:%M")
    data = {"time": time_now, "OI": oiData, "ATM": atm, "ATMPremium": atm_premium}
    json_data = json.dumps(data)
    # print(json_data)
    # file = open("MyOIWorld/todaysData.txt", 'a')
    # file.write(json.dumps(data))
    # file.write(json_data)
    # print(json_data)
    return json_data

## api_data=recordData("29Sep2022","NIFTY")

############### use below to get data only once
#
### https://discuss.streamlit.io/t/avoid-rerunning-some-code/1313/4
#
# import socket
#
# @st.cache(hash_funcs={socket.socket: id})
# def bindSocket(socket, port, addr):
#     print(“Binding receive socket to {}, port {}.”.format(udp_addr_receive, udp_port_receive))
#     socket.bind((addr, port))


def edelweiss_nse_index_data():
    ######### Gets NIFTY and SENSEX price data
    url = "https://ewmw.edelweiss.in/api/Market/Process/GetMarketStatus/20559,26753"
    atmresponse = requests.get(url)
    jsoned_atmresponse = atmresponse.json()
    jsoned_atmresponse = json.loads(jsoned_atmresponse)
    return jsoned_atmresponse

def edelweiss_OptionChain_thiya(expiry, scrip):
    # url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)
    jsoned_response = response.json()
    return jsoned_response


def edelweiss_OptionChain_Df(expiry, scrip):
    # url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
    url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
    payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
    response = requests.post(url, payload)
    jsoned_response = response.json()
    df = pd.json_normalize(jsoned_response['opChn'])

    # new_df = df[['stkPrc', 'atm',
    #              'ceQt.trdSym', 'ceQt.ltp', 'ceQt.chg', 'ceQt.chgP',
    #              'ceQt.bidPr', 'ceQt.askPr', 'ceQt.vol',
    #              'ceQt.opInt', 'ceQt.opIntChg',
    #              'ceQt.ltpivfut', 'ceQt.ltpivspt',
    #              'peQt.trdSym', 'peQt.ltp', 'peQt.chg', 'peQt.chgP',
    #              'peQt.bidPr', 'peQt.askPr', 'peQt.vol',
    #              'peQt.opInt', 'peQt.opIntChg',
    #              'peQt.ltpivfut', 'peQt.ltpivspt',
    #              ]]


    new_df = df[['stkPrc', 'atm',
                 # 'ceQt.trdSym',
                 'ceQt.ltp', 'ceQt.chg', 'ceQt.chgP',
                 'ceQt.bidPr', 'ceQt.askPr', 'ceQt.vol',
                 'ceQt.opInt', 'ceQt.opIntChg',
                 'ceQt.ltpivfut', 'ceQt.ltpivspt',
                 # 'peQt.trdSym',
                 'peQt.ltp', 'peQt.chg', 'peQt.chgP',
                 'peQt.bidPr', 'peQt.askPr', 'peQt.vol',
                 'peQt.opInt', 'peQt.opIntChg',
                 'peQt.ltpivfut', 'peQt.ltpivspt',
                 ]].apply(pd.to_numeric)


    # new_df = df[['atm',
    #              'ceQt.opIntChg','ceQt.opInt',
    #              'ceQt.ltpivspt',
    #              'ceQt.chgP','ceQt.ltp',
    #              'stkPrc',
    #              'peQt.ltp','peQt.chgP',
    #              'peQt.ltpivspt',
    #              'peQt.opInt', 'peQt.opIntChg'
    #              ]]

    new_df.set_index('stkPrc', inplace=True)
    return new_df


# def edelweiss_OptionChain_Df(expiry, scrip):
#     url = "https://ewmw.edelweiss.in/api/Market/optionchainguest"
#     # url = "https://ewmw.edelweiss.in/api/Market/optionchaindetails"
#     payload = {"exp": str(expiry), "aTyp": "OPTIDX", "uSym": scrip}
#     response = requests.post(url, payload)
#     jsoned_response = response.json()
#     df = pd.json_normalize(jsoned_response['opChn'])
#
#     new_df = df[['stkPrc', 'atm',
#                  'ceQt.trdSym', 'ceQt.ltp', 'ceQt.chg', 'ceQt.chgP',
#                  'ceQt.bidPr', 'ceQt.askPr', 'ceQt.vol',
#                  'ceQt.opInt', 'ceQt.opIntChg',
#                  'ceQt.ltpivfut', 'ceQt.ltpivspt',
#                  'peQt.trdSym', 'peQt.ltp', 'peQt.chg', 'peQt.chgP',
#                  'peQt.bidPr', 'peQt.askPr', 'peQt.vol',
#                  'peQt.opInt', 'peQt.opIntChg',
#                  'peQt.ltpivfut', 'peQt.ltpivspt',
#                  ]]
#     return new_df