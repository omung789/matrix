
from operator import index
import tkinter as tk
import numpy as np
import pandas as pd
import csv
import os
import ast

class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # initial settings
        self.title("Matrix Learning Tool")
        self.geometry("1000x500")
        self.resizable(True, True)


        # create a container
        self.container = tk.Frame(self, bg="#AFE3E4")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initialise frames
        self.frames = {}


        # define frames and pack them
        for F in (HomePage, CreateExercisePage, CompleteExercisePage, CreateAddSubMultExercisePage, CreateInvDetEigenExercisePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()






class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#AFE3E4")

        label = tk.Label(self, text="Matrix Learning Tool", font={"Helvetica", 20}, bg="#AFE3E4")
        label.pack(side="left", fill="x", padx = 100, pady=100)

        button1 = tk.Button(self, text="Go to Create Exercise", bg="light blue",
                    command=lambda: controller.show_frame("CreateExercisePage"),
                    padx= 50, pady = 50)
        button2 = tk.Button(self, text="Go to Complete Exercise", bg="light blue",
                    command=lambda: controller.show_frame("CompleteExercisePage"),
                    padx= 50, pady = 50)
        button3 = tk.Button(self, text="Go to Leaderboard", bg="light blue",
                    command=lambda: controller.show_frame("LeaderboardPage"),
                    padx= 50, pady = 50) 

        button1.pack(fill="none", expand=True)
        button2.pack(fill="none", expand=True)
        button3.pack(fill="none", expand=True) 

      
class CreateExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#AFE3E4")
        self.controller = controller

        #header
        label = tk.Label(self, text="Create Exercise", font={"Helvetica", 20, "bold"}, width=25, bg="#AFE3E4")
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: self.controller.show_frame("HomePage"), bg="light blue")
        button.grid()



        self.file_name = "test.csv"
        file_entry = tk.StringVar()
        tk.Entry(self, text="Hi", textvariable=file_entry).place(x=450, y=75)
        tk.Label(self, text="Enter Filename: ", font={"Helvetica", 20},  bg="#AFE3E4").place(x=450, y=50)
        set_file = tk.Button(self, text="Submit Filename", command=lambda: self.setFileName(file_entry.get()), width=15, padx=10)
        set_file.place(x=600, y=75)

        # operation menu
        self.v = tk.StringVar()
        self.operation = ""
        operations = {"Addition" : "addition",
                      "Subtraction" : "subtraction",
                      "Multiplication" : "multiplication",
                      "Eigenvalue" : "eigenvalue",
                      "Eigenvector" : "eigenvector",
                      "Inverse" : "inverse",
                      "Determinant" : "determinant"}

        for (text, value) in operations.items():
            tk.Radiobutton(self, text=text, variable=self.v, value=value, command=lambda: self.controller.show_frame(self.getOperationPage(self.v.get())), indicator=0, background="light blue", width=15).grid(column=0, pady=10)


    def getOperationPage(self, operation):
        self.operation = operation

        label = tk.Label(self, text=self.operation.title(), font={"Helvetica", 20, "bold"}, width=25, bg="#AFE3E4")
        label.place(x=450, y=10)

        if operation == "addition" or operation == "multiplication" or operation == "subtraction":
            return "CreateAddSubMultExercisePage"
        elif operation == "inverse" or operation == "determinant" or operation == "eigenvalue" or operation == "eigenvector":
            return "CreateInvDetEigenExercisePage"

    def setFileName(self, file_name):
        self.file_name = file_name




class CreateAddSubMultExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.matrix1 = MatrixInput(self, 3, 3)
        self.matrix2 = MatrixInput(self, 3, 3)

        self.matrix1.place(x=350, y=200)
        self.matrix2.place(x=650, y=200)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.place(x=550, y=350)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()
        npMatrix2 = self.matrix2.get()

        question = {"operation": [self.operation], "matrix 1": [npMatrix1], "matrix 2": [npMatrix2]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)

class CreateInvDetEigenExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.matrix1 = MatrixInput(self, 3, 3)

        self.matrix1.place(x=450, y=200)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.place(x=500, y=350)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()

        question = {"operation": [self.operation], "matrix 1": [npMatrix1], "matrix 2": [""]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)





class MatrixInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self.entry = {}
        self.rows = rows
        self.columns = columns

        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, width=3, font={"Helvetica", 30})
                e.grid(row=row, column=column, stick="nsew", ipadx=10, ipady=10)
                self.entry[index] = e

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(int(self.entry[index].get()))
                self.entry[index].delete(0, "end")
            result.append(current_row)
        return result
        #np.reshape(result, (self.rows, self.columns))


class CompleteExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#AFE3E4")
        self.controller = controller
        self.current_exercise = ""
        self.answer = ""

        #header
        label = tk.Label(self, text="Complete Exercise", font={"Helvetica", 20}, width=25, bg="#AFE3E4")
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: self.controller.show_frame("HomePage"), bg="light blue")
        button.grid()

        self.getExercises()


    def getExercises(self):
        exercises = os.listdir(os.path.join(os.getcwd(), "exercises"))
        self.variable = tk.StringVar(self)
        menu = tk.OptionMenu(self, self.variable, *exercises)
        menu.config(bg = "light blue")
        menu.place(x=50, y=100)

        tk.Button(self, text="select exercise", command=lambda: self.setExercise(self.variable), bg="light blue").place(x=50, y=140)



    def setExercise(self, variable):
        self.current_exercise = variable.get()
        path = os.path.join(os.getcwd(), "exercises", self.current_exercise)
        df = pd.read_csv(path)
        File = open(path)
        Reader = csv.reader(File)
        self.Data = list(Reader)
        # del(Data[0])

        list_of_entries = []
        for x in list(range(0,len(self.Data))):
            list_of_entries.append(self.Data[x][0])
        var = tk.StringVar(value = list_of_entries)
        listbox1 = tk.Listbox(self, listvariable = var)
        listbox1.place(x=50, y=200)

        def update():
            try:
                self.index = listbox1.curselection()[0]
            except:
                self.index = 0
            operationLabel2.config(text = self.Data[self.index][0])
            matrix1Label2.config(text = np.reshape(ast.literal_eval(self.Data[self.index][1]), (3,3)))
            if self.Data[self.index][2] != "":
                matrix2Label2.config(text = np.reshape(ast.literal_eval(self.Data[self.index][2]), (3,3)))
            # answerlabel2.config(text = Data[index][3])
            
        def ans():
            update()
            self.bigtuple = (self.index, self.Data[self.index][0], self.Data[self.index][1], self.Data[self.index][2])
            return self.checkANS(self.bigtuple)

        buttonANS = tk.Button(self, text="Check Answer", command=ans, bg="light blue").place(x=535, y=275)
        ans = tk.Label(self ,text = "Answer:", bg="#AFE3E4").place(x=475, y= 250)
        self.answer = tk.StringVar()
        ansForm = tk.Entry(self, textvariable=self.answer).place(x=525, y= 250)
        answerFormat = tk.Label(self, text="Give matrix in format [[x1,x2,x3],[x4,x5,x6],[x7,x8,x9]]\nPut decimal answers in 2.d.p.\nGive eigenvector in format [x1,x2,x3]", bg="#AFE3E4").place(x=450, y= 315)


        button1 = tk.Button(self, text="Update", command=update, bg="light blue")
        button1.place(x=85, y=375)

        operationLabel = tk.Label(self, text="Operation: ", bg="#AFE3E4", font={"Helvetica", 20, "bold"}).place(x=225, y=15)
        matrix1Label = tk.Label(self, text="Matrix 1", bg="#AFE3E4", font={"Helvetica", 20, "bold"}, width=20).place(x=350, y=100)
        matrix2Label = tk.Label(self, text="Matrix 2", bg="#AFE3E4", font={"Helvetica", 20, "bold"}, width=20).place(x=650, y=100)
        # answerlabel = tk.Label(self, text="Answer").grid(row=4, column=0,sticky="w")

        operationLabel2 = tk.Label(self, text="", width=10, bg="#AFE3E4", font={"Helvetica", 20, "bold"})
        operationLabel2.place(x=300, y=15)
        matrix1Label2 = tk.Label(self, text="", width=20, bg="#AFE3E4", font={"Helvetica", 40, "bold"})
        matrix1Label2.place(x=350, y=125)
        matrix2Label2 = tk.Label(self, text="", width=20, bg="#AFE3E4", font={"Helvetica", 40, "bold"})
        matrix2Label2.place(x=650, y=125)
        # answerlabel2 = tk.Label(self, text="")
        # answerlabel2.grid(row=4, column=1,sticky="w")
        # print(df)
        return update()
        

    def checkANS(self, bigtuple):
        index, DataOperation, matrix1, matrix2 = bigtuple

        if DataOperation == "addition" or DataOperation == "subtraction" or DataOperation == "multiplication":
            npMatrix2 = np.reshape(ast.literal_eval(matrix2), (3,3))
        npMatrix1 = np.reshape(ast.literal_eval(matrix1), (3,3))

        if DataOperation not in ["eigenvalue", "eigenvector", "determinant"]:
            answer = np.reshape(ast.literal_eval(self.answer.get()), (3,3))
        else:
            answer = self.answer.get()


        def correct():
            tk.Label(self, text="Correct!", width=20, bg="#AFE3E4", fg="green").place(x=475, y= 225)

        def incorrect():
            tk.Label(self, text="Incorrect!", width=20, bg="#AFE3E4", fg="red").place(x=475, y= 225)
        
        if DataOperation == "addition":
            correct() if (answer == np.add(npMatrix1, npMatrix2)).all() else incorrect()
        elif DataOperation == "subtraction":
            correct() if (answer == np.subtract(npMatrix1, npMatrix2)).all() else incorrect()
        elif DataOperation == "multiplication":
            correct() if (answer == np.multiply(npMatrix1, npMatrix2)).all() else incorrect()
        elif DataOperation == "eigenvalue":
            values, vector = np.linalg.eigh(npMatrix1)
            eigenanswer = float(self.answer.get())
            correct() if eigenanswer == (values[0]) or eigenanswer == (values[1]) or eigenanswer == (values[2]) else incorrect()
        elif DataOperation == "eigenvector":
            values, vector = np.linalg.eigh(npMatrix1)
<<<<<<< HEAD
            for x in range(3):
                for y in range(3):
                   vector[x][y] = round(vector[x][y],2)
            correct() if self.answer.get() == str(vector[0].tolist()) or self.answer.get() == str(vector[1].tolist()) or self.answer.get() == str(vector[2].tolist()) else incorrect()
=======
            correct() if self.answer.get() == (str(vector).tolist()).replace(" ", "") else incorrect()
>>>>>>> 6ab7e4df50e2134e051ddada09321da6a7ca941e
        elif DataOperation == "inverse":
            correct() if (answer == np.linalg.inv(npMatrix1)).all() else incorrect()
        elif DataOperation == "determinant":
            correct() if self.answer.get() == (str(round(np.linalg.det(npMatrix1), 3))) else incorrect()



if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()
        