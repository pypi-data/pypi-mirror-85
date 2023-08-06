import pickle
import tkinter as tk

#Encapsulamiento de GUI de Tkinder
class Division():
    def __init__(self, master, num1, num2):
        self.master = master
        var1 = tk.DoubleVar()
        t1 = tk.Entry(master, textvariable=var1)
        t1.pack()

        var2 = tk.DoubleVar()
        t2 = tk.Entry(master, textvariable=var2)
        t2.pack()

        result = tk.DoubleVar()
        l = tk.Label(master, textvariable=result)
        l.pack()

        #Configurar las variables
        var1.set(num1)
        var2.set(num2)
        
        result.set(var1.get() / var2.get())
        
#Main function
def main(number_1, number_2): 

    root = tk.Tk()
    root.title('Dividir')
    root.geometry("300x300")
    app = Division(root, number_1, number_2)
    root.mainloop()

if __name__ == '__main__':
    main()