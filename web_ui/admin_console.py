import json
import streamlit as st
import requests
import socket
import pandas as pd
from decouple import config
import os
from services.services_ui import extract_ip

SRC_DIR = config('SRC_DIR',default='./src')
SERVER_URL = 'http://'+str(extract_ip())+':'+str(8000)
st.image(os.path.join(SRC_DIR,'Logo_cyrillic_red.png'))
####------

with st.sidebar:
    st.selectbox('Выберите действие',['Просмотр','Загрузка','Удаление'],index=1,key='action')
if st.session_state['action'] == 'Удаление':
    st.markdown('### Принтеры', unsafe_allow_html=True)
    if st.button('Очистить БД Принтеры'):
        re = requests.get(str(SERVER_URL + '/clear_db/printers'))
        if re.status_code == 200:
            st.success('База Принтеров успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')

    st.markdown('### Шаблоны', unsafe_allow_html=True)
    if st.button('Очистить БД Шаблоны этикеток'):
        re = requests.get(str(SERVER_URL + '/clear_db/label_templ'))
        if re.status_code == 200:
            st.success('База Шаблонов этикеток успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')

    st.markdown('### Устройтсова', unsafe_allow_html=True)
    if st.button('Очистить БД Устройств'):
        re = requests.get(str(SERVER_URL + '/clear_db/devices'))
        if re.status_code == 200:
            st.success('База Устройств успешно очищена')
        else:
            st.error('Что-то пошло не так. Повторите операцию позже')

if st.session_state['action'] == 'Просмотр':
    st.markdown('### Принтеры',unsafe_allow_html=True)

    re = requests.get(str(SERVER_URL + '/printers'))

    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id', inplace=True)
        df = df[['print_name', 'url', 'port']]
        df = df.rename(columns={
            'print_name': 'Принтер',
            'url': 'IP4'
        })
        st.data_editor(df)

    st.markdown('### Устройства', unsafe_allow_html=True)

    re = requests.get(str(SERVER_URL + '/devices'))

    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id', inplace=True)
        df = df[['device_name', 'url']]
        df = df.rename(columns={
            'device_name': 'Устройство',
            'url': 'IP4'
        })
        st.data_editor(df)

    st.markdown('### Шаблоны', unsafe_allow_html=True)

    re = requests.get(str(SERVER_URL + '/template'))

    j1 = re.json()
    if len(j1) != 0:
        df = pd.DataFrame.from_records(j1)
        df.set_index('id', inplace=True)
        df = df[['templ_name', 'templ_data']]
        df = df.rename(columns={
            'templ_name': 'Название шаблона',
            'templ_data': 'Значение'
        })
        st.data_editor(df)



if st.session_state['action'] == 'Загрузка':
    if st.checkbox('Загрузить шаблон этикетки', value=False):
        st.text_input('Название этикетки',key = 'temlate_name')
        st.text_area('Шаблон этикетки',key ='template_data')
        st.checkbox('Использовать шаблон по-умолчанию',key='is_default')
        data = {"name": st.session_state['temlate_name'], "label": st.session_state['template_data'], "is_default": int(st.session_state['is_default'])}
        if st.button('Загрузить шаблон'):
            re1 = requests.post(str(SERVER_URL + '/template'),data=json.dumps(data),headers={"accept": "application/json"})
            if re1.status_code == 200:
                st.success("Шаблон успешно загружен.")
                st.rerun()
            else:
                st.error(f"Ошибка при загрузке шаблона: {re1.status_code}")

    if st.checkbox('Добавить принтер этикеток', value=False):
        st.text_input('Наименование принтера',key = 'printer_name')
        st.text_input('Ip4 принтера',key = 'url')
        st.text_input('Port принтера', key='port',value=9100)
        st.checkbox('Использовать шаблон по-умолчанию',key='is_default_printer')
        data = {"name": st.session_state['printer_name'],
                "url": st.session_state['url'],
                'port':int(st.session_state['port']),
                'type':1,
                "is_default": int(st.session_state['is_default_printer'])}
        if st.button('Добавить принтер'):
            re1 = requests.post(str(SERVER_URL + '/printer'),data=json.dumps(data),headers={"accept": "application/json"})
            if re1.status_code == 200:
                st.success("Принтер успешно добавлен.")
                st.rerun()
            else:
                st.error(f"Ошибка при добавление принтера: {re1.status_code}")

    if st.checkbox('Добавить устройства', value=False,help='При добавление устройств доступ будет осуществлен только для добавленных устройств'):
        st.text_input('Наименование устройства',key = 'device_name')
        st.text_input('Ip4 устроqства',key = 'url_device')

        data = {"name": st.session_state['device_name'],
                "url": st.session_state['url_device'],
                }
        if st.button('Добавить устройство'):
            re1 = requests.post(str(SERVER_URL + '/device'),data=json.dumps(data),headers={"accept": "application/json"})
            if re1.status_code == 200:
                st.success("Устройство успешно добавлено.")
                st.rerun()
            else:
                st.error(f"Ошибка при добавление устройства: {re1.status_code}")





