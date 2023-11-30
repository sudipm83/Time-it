import warnings
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader

from EmployeeDashboard import show_dashboard_employee
from Util import show_nlp, convert_pass
from dashboard import show_dashboard

st.set_page_config(page_title="Time-It", page_icon=":bar_chart:", layout="wide")
warnings.filterwarnings("ignore")

# st.title(" :chart_with_upwards_trend: Sample swipe-in data")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# st.write(convert_pass())

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

side_bar_option = None
selected = None

name, authentication_status, username = authenticator.login('Login')

if authentication_status:
    if username == 'swanand' or username == 'shraddha' :
        st.header(f'Welcome *{name}*')
        side_bar_option = ["Your data", "NLP", "Employee Data", "Logout"]
    else:
        st.header(f'Welcome *{name}*')
        side_bar_option = ["Your data", "NLP", "Logout"]
elif not authentication_status:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')

if side_bar_option:
    st.sidebar.title(' :chart_with_upwards_trend: Time It !')
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=side_bar_option,
        )

if selected == 'Your data':
    show_dashboard_employee(name)

if selected == 'NLP':
    show_nlp()
if selected == 'Employee Data':
    show_dashboard(username)
if selected == "Logout":
    authenticator.logout('Are you sure you want to logout ?')
