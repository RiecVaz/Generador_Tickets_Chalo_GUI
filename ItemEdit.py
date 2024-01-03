from tkinter import * #Entry, Label, Frame, Button, Checkbutton, messagebox, ttk, Toplevel, SUNKEN, StringVar, DoubleVar, IntVar, BooleanVar
from DBManager import Database
from decimal import Decimal

class General(Tk):
    def  __init__(self, Variation_ID: int) -> None:
        super().__init__()
        self.title('Edit Item')
        self.geometry('300x400')
        self.resizable(True, False)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.db = Database()
        self.show(self.getData(Variation_ID))


    def show(self, list_values: list) -> None:
        
        deparment_value =  StringVar()
        deparment_value.set(list_values[0])
        category_name = StringVar()
        category_name.set(list_values[1])
        product_name = StringVar()
        product_name.set(list_values[2])
        print(list_values[3], type(list_values[3]))
        if list_values[3] == 'True':
            weight_bool = BooleanVar()
            weight_bool.set(TRUE)
        else:
            weight_bool = BooleanVar()
            weight_bool.set(FALSE)

        print(weight_bool.get(), type(weight_bool.get()))
        Variation_name = StringVar()
        Variation_name.set(list_values[4])
        price_value = DoubleVar()
        price_value.set(Decimal(list_values[5]))

        Label_price = Label(self, text='Variación y Precio', font='Arial 12 bold')
        Label_price.pack(pady=10)
        var_frame = Frame(self)
        var_frame.pack(pady=5)

        Entry_var = Entry(var_frame, width=15, textvariable=Variation_name)
        Entry_var.config(justify='center', relief= SUNKEN)
        Entry_var.grid(row=0, column=0, padx=10, pady=5)

        Entry_price = Entry(var_frame, width=5, textvariable=price_value)
        Entry_price.config(justify='center', relief= SUNKEN)
        Entry_price.grid(row=0, column=1, padx=10, pady=5)
        
        Label_product = Label(self, text='Nombre del Producto', font='Arial 12 bold')
        Label_product.pack(pady=5)

        Entry_Product = Entry(self, width=23, textvariable=product_name)
        Entry_Product.config(justify='center', relief= SUNKEN)
        Entry_Product.pack(pady=5)

        Label_category = Label(self, text='Categoría', font='Arial 12 bold')
        Label_category.pack(pady=5)

        Entry_category = Entry(self, width=23, textvariable=category_name)
        Entry_category.config(justify='center', relief= SUNKEN)
        Entry_category.pack(pady=5)

        Label_Department = Label(self, text='Departamento', font='Arial 12 bold')
        Label_Department.pack(pady=5)

        Entry_Department = Entry(self, width=23, textvariable=deparment_value)
        Entry_Department.config(justify='center', relief= SUNKEN)
        Entry_Department.pack(pady=5)

        Frame_weight = Frame(self)
        Frame_weight.pack(pady=5)

        label_weight = Label(Frame_weight, text='Peso', font='Arial 12 bold')
        label_weight.grid(row=0, column=0, padx=10, pady=5)

        check_weight = Checkbutton(Frame_weight, var = weight_bool)
        check_weight.grid(row=0, column=1, padx=10, pady=5)

        Frame_buttons = Frame(self)
        Frame_buttons.pack(pady=5)

        Update_button = Button(Frame_buttons, text='Modificar')
        Update_button.grid(row=0, column=0, padx=5)

        Cancel_button = Button(Frame_buttons, text = 'Cancelar')
        Cancel_button.grid(row=0,column=1, padx=5)

    
    def close(self):
        self.destroy()

    def getData(self,ID: int):
        sql_string = f"""
            SELECT
                Dep.Description,
                Cat.Description,
                Prod.Description,
                Prod.Weight,
                Var.Description,
                Var.Price	
            FROM
            Variations as Var
            JOIN Departments  as Dep
            ON Dep.ID = Var.DepartmentID
            JOIN Categories as Cat 
            ON Cat.ID = Var.CatID
            JOIN Products as Prod
            ON Prod.ID = Var.ProductID
            WHERE Var.ID = '{ID}'
        """
        
        return self.db.query(sql_string)[0]


if __name__ == '__main__':
    General(3).mainloop()