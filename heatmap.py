import streamlit as st
import math
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(layout="wide")

# Sidebar
spot = st.sidebar.number_input(label="Current Asset Price", value = 100.00, placeholder="100", step=0.01)
strike = st.sidebar.number_input(label="Strike Price", value = 95.00, placeholder="95", step=0.01)
vol = st.sidebar.number_input(label="Volatility (σ)", value = 0.20, placeholder="0.2", step=0.01)
ttm = st.sidebar.number_input(label="Time to Maturity (Years)", value = 0.50, placeholder="0.5", step=0.01)
interest = st.sidebar.number_input(label="Risk-Free Interest Rate", value = 0.05, placeholder="0.05", step=0.01)
dividend = st.sidebar.number_input(label="Dividend Yield", value = 0.01, placeholder="0.01", step=0.01)
st.sidebar.divider()
min_spot = st.sidebar.number_input(label="Min Spot Price", value=spot*0.8, step=0.01)
max_spot = st.sidebar.number_input(label = "Max Spot Price", value=spot*1.2, step=0.01)
min_vol = st.sidebar.slider(label="Min Volatility for Heatmap", min_value=0.01, max_value=1.00, value=vol*0.5)
max_vol = st.sidebar.slider(label="Max Volatility for Heatmap", min_value=0.01, max_value=1.00, value=vol*1.5)

# Math for Black-Scholes Pricing Model For Call Options
def call(s, k, sigma, t, r, d):
    d1 = (math.log(s/k)+(r-d+(sigma**2)/2)*t)/(sigma*math.sqrt(t))
    d2 = d1-(sigma*math.sqrt(t))
    return round(((s*norm.cdf(d1))/math.exp(d*t))-((k*norm.cdf(d2))/math.exp(r*t)), 2)
def put(s, k, sigma, t, r, d):
    d1 = (math.log(s/k)+(r-d+(sigma**2)/2)*t)/(sigma*math.sqrt(t))
    d2 = d1-(sigma*math.sqrt(t))
    return round(((k*norm.cdf(-d2))/math.exp(r*t))-((s*norm.cdf(-d1))/math.exp(d*t)), 2)

# Additional Variables to Use for Future Add-ons
d1 = (math.log(spot/strike)+(interest-dividend+(vol**2)/2)*ttm)/(vol*math.sqrt(ttm))
delta = norm.cdf(d1)
gamma = math.exp(-((d1**2/2)+dividend*ttm))/(strike*vol*math.sqrt(2*ttm*math.pi))

# Actual App

# Call and Put Prices
st.title("Black-Scholes Pricing Model")
col1, col2 = st.columns(2)
col1.metric("Call Price", f"""${call(spot, strike, vol, ttm, interest, dividend)}""", border=True)
col2.metric("Put Price", f"""${put(spot, strike, vol, ttm, interest, dividend)}""", border=True)

# Heatmaps
space_spot = (max_spot - min_spot)/9
space_vol = (max_vol - min_vol)/9
num = 10
x_labels = [f"""{round(min_spot + space_spot*x, 2)}""" for x in range(num)]
y_labels = [f"""{round(min_vol + space_vol*x, 2)}""" for x in range(num)]
z1_values = [[call(min_spot+(space_spot*x), strike, min_vol+(space_vol*y), ttm, interest, dividend) for x in range(num)] for y in range(num)]
z2_values = [[put(min_spot+(space_spot*x), strike, min_vol+(space_vol*y), ttm, interest, dividend) for x in range(num)] for y in range(num)]

fig1, ax1 = plt.subplots()
ax1.set_title("CALL", fontsize=20)
sns.set(font_scale=0.65)
sns.heatmap(z1_values, xticklabels=x_labels, yticklabels=y_labels, square=True, annot=True, fmt=".2f", cmap="viridis").set(xlabel='Spot Price', ylabel='Volatility')
fig2, ax2 = plt.subplots()
ax2.set_title("PUT", fontsize=20)
sns.set(font_scale=0.65)
sns.heatmap(z2_values, xticklabels=x_labels, yticklabels=y_labels, square=True, annot=True, fmt=".2f", cmap="viridis").set(xlabel='Spot Price', ylabel='Volatility')

col1.pyplot(fig1)
col2.pyplot(fig2)