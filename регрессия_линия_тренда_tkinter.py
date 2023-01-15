import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

root = Tk()
root.title("Расчет теплового эффекта")
root.geometry("250x200")

root.grid_rowconfigure(index=0, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)
data = pd.DataFrame()




def open_file():
    global data
    filepath = filedialog.askopenfilename()
    if filepath != "":
        data = pd.read_excel(filepath)

    return data



def calculate():
    global data
    data["Reversed_temperature_K"] = data["Temperature_C"].apply(lambda x: 1 / (x + 273.15))
    data["Equilibrium_constant"] = data["Equilibrium_concentration_of_the_endo-isomer"].apply(lambda x: (100 - x) / x)
    data["Ln_equilibrium_constant"] = data["Equilibrium_constant"].apply(lambda x: np.log(x))
    x = data["Reversed_temperature_K"]
    y = data["Ln_equilibrium_constant"]
    coeff = np.polyfit(x, y, 1)
    trend_line = p = np.poly1d(coeff)
    plt.scatter(x, y)
    plt.plot(x, trend_line(x), "r--")
    plt.xlabel('1/T')
    plt.ylabel('lnK')
    text = f"$y={coeff[0]:0.3f}\;x{coeff[1]:+0.3f}$\n$R^2 = {r2_score(y, trend_line(x)):0.3f}$"
    plt.gca().text(0.1, 0.9, text, transform=plt.gca().transAxes,
                   fontsize=14, verticalalignment='top')
    plt.show()


open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)

calculate_button = ttk.Button(text="Рассчитать", command=calculate)
calculate_button.grid(column=1, row=1, sticky=NSEW, padx=10)

root.mainloop()
