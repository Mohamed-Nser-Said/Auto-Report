# Python libraries
from fpdf import FPDF
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

WIDTH = 210
HEIGHT = 297

df = pd.read_csv("data/reading.csv")

time = df["time(s)"]
temp = df["temperature(C)"]
volt1 = df["ChargingVoltage(mV)"]
volt2 = df["DischargingVoltage(mV)"]
pump_speed = df["pumpFlowRate(mL)"]

df.plot.scatter(x="ChargingVoltage(mV)",y="time(s)",c="temperature(C)",cmap='coolwarm')
plt.savefig("data/scatter.jpg")
df.plot.scatter(x="DischargingVoltage(mV)",y="time(s)",c="temperature(C)",cmap='coolwarm')
plt.savefig("data/scatter1.jpg")
df.plot.scatter(x="pumpFlowRate(mL)",y="ChargingVoltage(mV)",c="temperature(C)",cmap='coolwarm')
plt.savefig("data/scatter2.jpg")
df.plot.scatter(x="pumpFlowRate(mL)",y="DischargingVoltage(mV)",c="temperature(C)",cmap='coolwarm')
plt.savefig("data/scatter3.jpg")

pdf = FPDF()


def graph_generator(x, y, label, xlabel, ylabel, title, pen='r'):

    fig, axes = plt.subplots(figsize=(6, 5))
    axes.plot(x, y, pen, markeredgewidth=2, markersize=10, label=label)

    #axes.plot(time, voltage, 'r-+', markeredgewidth=2, markersize=10, label='voltage')
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_title(title)
    axes.grid(True)
    axes.legend()
    plt.savefig("/data"+label+".jpg")


def summary_graph():
    graph_generator(time, temp, 'Temperature', 'Time (s)', 'Temperature (C)', 'Temperature change with Time')
    graph_generator(time, volt1, 'voltageCharging', 'Time (s)', 'voltage (mV)', 'voltage change with Time - charging')
    graph_generator(time, volt2, 'voltageDischarging', 'Time (s)', 'voltage (mV)', 'voltage change with Time - discharging')
    graph_generator(time, pump_speed, 'pumpFlowRate', 'Time (s)', 'ml', 'pump flow rate Time when charging')
    graph_generator(pump_speed, temp, 'pumpFlowRateWithTemperatue', 'flow rate (ml)', 'Temperature (C))', 'pump Flow Rate with Temperature - charging', pen="r")
    graph_generator(pump_speed, volt2, 'pumpFlowRateWithVoltageDischarging', 'flow rate (ml)', 'voltage (mV)', 'pump Flow Rate with voltage change -discharging', pen="r")

    pdf.add_page()
    pdf.image('data/Temperature.jpg', 5, 20, WIDTH / 2 - 10)
    pdf.image('data/voltageCharging.jpg', WIDTH / 2, 20, WIDTH / 2 - 10)

    pdf.image("data/voltageDischarging.jpg", 5, 110, WIDTH / 2 - 10)
    pdf.image("data/pumpFlowRate.jpg", WIDTH / 2, 110, WIDTH / 2 - 10)

    pdf.image("data/voltageChargingTemperatue.jpg", 5, 200, WIDTH / 2 - 10)
    pdf.image("data/voltageDischargingTemperatue.jpg", WIDTH / 2, 200, WIDTH / 2 - 10)

    pdf.add_page()

    pdf.image('data/scatter.jpg', 5, 20, WIDTH / 2 - 10)
    pdf.image('data/scatter1.jpg', WIDTH / 2, 20, WIDTH / 2 - 10)

    pdf.image("data/scatter2.jpg", 5, 110, WIDTH / 2 - 10)
    pdf.image("data/scatter3.jpg", WIDTH / 2, 110, WIDTH / 2 - 10)


def first_page():
    pdf.add_page()
    pdf.set_title(f"Automatic Generated Report for Measurement of Redox Flow Battery")
    pdf.set_author("Mohamed Said")
    pdf.set_font('Helvetica', '', 24)
    pdf.image("data/CoverPage2.jpg", 0, 0, WIDTH)
    pdf.ln(120)
    pdf.cell(w=0, h=10, txt="Report for Measurement of Redox Flow Battery")
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    pdf.cell(w=0, h=10, txt=f"Date: {datetime.today()}")


def data_page():
    pdf.add_page()
    pdf.set_font('Courier', 'B', 14)
    pdf.cell(w=0, h=10, txt="this report is automatically generated may contains some error ")
    pdf.ln(20)
    pdf.set_font('Courier', '', 12)
    # 'time(s) temperature(C) ChargingVoltage(mV) DischargingVoltage(mV) pumpFlowRate(mL)'
    pdf.write(h=10, txt=f"The total measurement consist of \n: {list(df.columns)[1:]}")
    pdf.ln(20)
    pdf.write(h=10,
              txt=f"maximum and minimum voltage generated \n: {df['ChargingVoltage(mV)'].max(), df['ChargingVoltage(mV)'].min()}")
    pdf.ln(20)
    pdf.write(h=10,
              txt=f"maximum and minimum voltage of discharging\n :{df['DischargingVoltage(mV)'].max(), df['DischargingVoltage(mV)'].min()} ")
    pdf.ln(20)
    pdf.write(h=10, txt=f"total duration in (S)\n: {df['time(s)'].max()}")
    pdf.ln(20)
    pdf.write(h=10,
              txt=f"maximum and minimum pump speed \n:  {df['pumpFlowRate(mL)'].max(), df['pumpFlowRate(mL)'].min()}")
    pdf.ln(20)
    pdf.write(h=10, txt=f"highest and lowest temperature\n :  {df['temperature(C)'].max(), df['temperature(C)'].min()}")


if __name__ == "__main__":

    first_page()
    summary_graph()
    data_page()
    pdf.output("report.pdf", 'F')
