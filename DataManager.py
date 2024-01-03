from tkinter import  *
from tkinter import  ttk
from tkinter import messagebox
import  sqlite3
import time
from DBManager import Database as DB
from ItemEdit import General

#SECCIONES
def Data_Window():
    
    db = DB()
    Options = ['Productos','Empleados','Registro']
    #Sections_All = ['Cocteles', 'Bebidas','Platillos','Caldos','Pescados','Postres']
    
    #FUNCIONES
    def on_closing():
        DataWn.destroy()

    def Change_Frame(*args):
        Frametype = var.get()
        Frames = [Frame_Product,Frame_Employe,Frame_registro]
        count = 0
        for x in Options:
            if Frametype == x:
                Frames[count].tkraise()
            else:
                pass
            count +=1
    
    def UpdateSearch_Product(event):
        Lectura = Product_items.get_children()
        Product_items.delete(*Lectura)
        for i in event:
            Product_items.insert("", END, values=i)

    def getrow(event, section):
        match section:
            case 'Departament':
                DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]
                query_string = f"""
                            SELECT ID, Description FROM Categories
                            WHERE DepartmentID = '{DepartmentID}'
                            """
                categories_list = db.query(query_string)
                update_treeview(Category_Tvw, categories_list,clean_lvl=1)
            case 'Category':
                CategoryID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                query_string = f"""
                            SELECT ID, Description, Weight FROM Products
                            WHERE CatID = '{CategoryID}'
                            """
                products_list = db.query(query_string)
                update_treeview(Product_Tvw, products_list,clean_lvl=2)
            case 'Product':
                ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                query_string = f"""
                            SELECT ID, Description, Price FROM Variations
                            WHERE ProductID = '{ProductID}'
                            """
                variations_list = db.query(query_string)
                update_treeview(Variation_Tvw, variations_list,None)
            case default:
                pass

    def update_treeview(tree: ttk.Treeview, data: list, clean_lvl: int ) -> None:
        tree.delete(*tree.get_children())
        match clean_lvl:
            case 1:
                Product_Tvw.delete(*Product_Tvw.get_children())
                Variation_Tvw.delete(*Variation_Tvw.get_children())
            case 2:
                Variation_Tvw.delete(*Variation_Tvw.get_children())
            
            case 3:
                Entsearch.delete(0, END)
            case default:
                pass
        for i in data:
            tree.insert("", END, values=i)
        
    def Delete_Item(section):
        try:
            DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]
        except:
            messagebox.showerror('Error', 'No se ha seleccionado un departamento')
            return
        match section:
            case 'Departament':
                location = 'este departamento'
                query_string = f"""
                            DELETE FROM Departments
                            WHERE ID = '{DepartmentID}'
                            """
                clear_lvl = 1
                fill_string = f"""
                            SELECT ID, Description FROM Departments
                            """
                treeview = Department_Tvw
            case 'Category':
                location = 'esta categoría'
                CategoryID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                query_string = f"""
                            DELETE FROM Categories
                            WHERE ID = '{CategoryID}'
                            """
                clear_lvl = 2
                fill_string = f"""  
                            SELECT ID, Description FROM Categories
                            WHERE DepartmentID = '{DepartmentID}'
                            """
                treeview = Category_Tvw
            case 'Product':
                location = 'este producto'
                CategoryID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                query_string = f"""
                            DELETE FROM Products
                            WHERE ID = '{ProductID}'
                            """
                clear_lvl = 3
                fill_string = f"""
                            SELECT ID, Description, Weight FROM Products
                            WHERE CatID = '{CategoryID}'
                            """ 
                treeview = Product_Tvw
            case 'Variation':
                ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                location = 'esta variante'
                VariationID = Variation_Tvw.item(Variation_Tvw.focus())['values'][0]
                query_string = f"""
                            DELETE FROM Variations
                            WHERE ID = '{VariationID}'
                            """
                clear_lvl = None
                fill_string = f"""
                            SELECT ID, Description, Price FROM Variations
                            WHERE ProductID = '{ProductID}'
                            """
                treeview = Variation_Tvw
            case default:
                pass
        option = messagebox.askyesno(f"CONFIRMAR", f"¿Estás seguro de querer eliminar {location}?")
        if option:
            db.update(query_string)
            update_treeview(treeview, db.query(fill_string),clean_lvl=clear_lvl)
        
    def Get_Employee(event):
        item = Employee_items.item(Employee_items.focus())
        Em_ID.set(item['values'][0])
        Em_Name.set(item['values'][1])
        Em_AP1.set(item['values'][2])
        Em_AP2.set(item['values'][3])

    def Clear_Em_Data():
        cursor.execute("SELECT id, NOMBRE, APELLIDO1, APELLIDO2 FROM EMPLEADOS")
        Lectura = Employee_items.get_children()
        Employee_items.delete(*Lectura)
        
        for x in cursor.fetchall(): 
            Employee_items.insert("",END, values = x)

        EntEmID.delete(0, END)
        EntEmAP1.delete(0, END)
        EntEmAP2.delete(0, END)
        EntEmName.delete(0, END)

    def Employee_Data(arg):
        Nom = Em_Name.get()
        Ape1 = Em_AP1.get()
        Ape2 = Em_AP2.get()
        Ident = Em_ID.get()

        if arg == 1:
            cursor.execute("INSERT INTO EMPLEADOS (id, NOMBRE, APELLIDO1, APELLIDO2) VALUES(?,?,?,?)",(Ident, Nom, Ape1, Ape2))
            db.commit()
            Clear_Em_Data()
        elif arg == 2:
            if messagebox.askyesno("Eliminar Empleado", "¿Estás seguro de querer Borrar los datos de este empleado?"):
                cursor.execute("DELETE FROM EMPLEADOS WHERE id = ?", [Ident])
                db.commit()
                Clear_Em_Data()
            
            return True

        elif arg == 3:
            if messagebox.askyesno("CONFIRMAR", "¿Estás seguro de querer modificar la información de este Empleado?"):
                cursor.execute("UPDATE EMPLEADOS SET NOMBRE = ?, APELLIDO1 = ?, APELLIDO2 = ? WHERE id = ?", (Nom, Ape1, Ape2, Ident))
                db.commit()
                Clear_Em_Data()
        else:
            Clear_Em_Data()

    def Get_Registro(event):
        Regitems_mesas.delete(*Regitems_mesas.get_children())
        item = Registro_items.item(Registro_items.focus())
        Id_venta = item['values'][0]
        varborrar.set(item['values'][0])
        cursor.execute("SELECT MESA_CONSUMO.COD_VENTA, MESA_CONSUMO.ID_MESA, CANTIDAD, PRODUCTO, COSTO FROM REGISTRO INNER JOIN MESA_CONSUMO ON REGISTRO.COD_VENTA = MESA_CONSUMO.COD_VENTA WHERE REGISTRO.COD_VENTA = ?",[Id_venta])
        for i in cursor.fetchall():
                Regitems_mesas.insert("",END, values = i)

    def Borrar_Registro():
        Id_venta = varborrar.get()
        if messagebox.askyesno("CONFIRMAR", "¿Estás seguro de querer ELMINAR este registro?"):
            cursor.execute("DELETE FROM REGISTRO WHERE REGISTRO.COD_VENTA = ?",[Id_venta])
            cursor.execute("DELETE FROM MESA_CONSUMO WHERE MESA_CONSUMO.COD_VENTA = ?",[Id_venta])
            db.commit()
            Limpiar_Registro()
        
    def Update_Registro(): 
        Regitems_mesas.delete(*Regitems_mesas.get_children())
        Registro_items.delete(*Registro_items.get_children()) #Limpiar y hacer coincidir con respecto a la fecha
        cursor.execute("SELECT * FROM REGISTRO WHERE FECHA LIKE '%"+Fecha+"%' AND COD_VENTA > 0")
        for i in cursor.fetchall():
                Registro_items.insert("",END, values = i)
    
    def Limpiar_Registro():
        BorrarEntry.delete(0,END)
        Update_Registro()

    def modify_in_tree(branch: str, add: bool, values: list) -> None:
        
        match branch:
            case 'Departamento':
                New_name = values[0]
                if add:
                    query_string = f"""
                        INSERT INTO Departments (Description)
                        VALUES ('{New_name}')
                        """
                    mod = messagebox.askquestion('Agregar', '¿Estás seguro de querer agregar este departamento?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Department_Tvw, db.query("SELECT * FROM Departments"),clean_lvl=1)
                    add_window.destroy()
                else:
                    try:
                        Old_name = Department_Tvw.item(Department_Tvw.focus())['values'][1]

                        if Old_name == New_name:
                            raise RuntimeError
                            
                    except:
                        messagebox.showerror('Error', 'El nombre no ha cambiado')
                        add_window.destroy()
                        return
                    try:
                        DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado un departamento')
                        return
                    
                    query_string = f"""
                        UPDATE Departments
                        SET Description = '{New_name}'
                        WHERE ID = '{DepartmentID}'
                        """
                    mod = messagebox.askquestion('Modificar', '¿Estás seguro de querer modificar este departamento?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Department_Tvw, db.query("SELECT * FROM Departments"),clean_lvl=1)
                    add_window.destroy()
            case 'Categoría':
                New_name = values[0]
                if add:
                    try:
                        DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado una categoría')
                        return
                    query_string = f"""
                        INSERT INTO Categories (DepartmentID, Description)
                        VALUES ('{DepartmentID}','{New_name}')
                        """
                    mod = messagebox.askquestion('Agregar', '¿Estás seguro de querer agregar esta categoría?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Category_Tvw, db.query(f"SELECT ID, Description FROM Categories WHERE DepartmentID = {DepartmentID}"),clean_lvl=1)
                    add_window.destroy()
                else:
                    try:
                        Old_name = Category_Tvw.item(Category_Tvw.focus())['values'][1]
                        DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]
                        if Old_name == New_name:
                            raise RuntimeError
                            
                    except:
                        messagebox.showerror('Error', 'El nombre no ha cambiado')
                        add_window.destroy()
                        return
                    try:
                        CategoryID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado una categoría')
                        add_window.destroy()
                        return
                    
                    query_string = f"""
                        UPDATE Categories
                        SET Description = '{New_name}'
                        WHERE ID = '{CategoryID}'
                        """
                    mod = messagebox.askquestion('Modificar', '¿Estás seguro de querer modificar esta categoría?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Category_Tvw, db.query(f"SELECT ID, Description FROM Categories WHERE DepartmentID = '{DepartmentID}'"),clean_lvl=2)
                    add_window.destroy()
            case 'Producto':
                New_name = values[0]
                Weight = values[1] 
                if add:
                    try:
                        CatID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado un producto')
                        return
                    query_string = f"""
                        INSERT INTO Products (CatID, Description, Weight)
                        VALUES ('{CatID}','{New_name}', '{Weight}')
                        """
                    mod = messagebox.askquestion('Agregar', '¿Estás seguro de querer agregar este producto?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Product_Tvw, db.query(f"SELECT ID, Description, Weight FROM Products WHERE CatID = '{CatID}'"),clean_lvl=2)
                    add_window.destroy()
                else:
                    try:
                        
                        if Weight:
                            Weight = 'True'
                        else:
                            Weight = 'False'

                        Old_name = Product_Tvw.item(Product_Tvw.focus())['values'][1]
                        Old_weight = Product_Tvw.item(Product_Tvw.focus())['values'][2]
                        CategoryID = Category_Tvw.item(Category_Tvw.focus())['values'][0]

                        if (Old_name == New_name and Old_weight == Weight):
                            raise RuntimeError
                            
                    except:
                        messagebox.showerror('Error', 'Ningún parámetro ha cambiado')
                        add_window.destroy()
                        return
                    try:
                        ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado un producto')
                        add_window.destroy()
                        return
                    
                    query_string = f"""
                        UPDATE Products
                        SET Description = '{New_name}', Weight = '{Weight}'
                        WHERE ID = '{ProductID}'
                        """
                    mod = messagebox.askquestion('Modificar', '¿Estás seguro de querer modificar este producto?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Product_Tvw, db.query(f"SELECT ID, Description, Weight FROM Products WHERE CatID = '{CategoryID}'"),clean_lvl=2)
                    add_window.destroy()
            case 'Variación':
                New_name = values[0]
                price = values[1]
                if add:
                    try:
                        ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                        CatID = Category_Tvw.item(Category_Tvw.focus())['values'][0]
                        DepartmentID = Department_Tvw.item(Department_Tvw.focus())['values'][0]

                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado una variación')
                        return
                    query_string = f"""
                        INSERT INTO Variations (DepartmentID, CatID, ProductID, Description, Price)
                        VALUES ('{DepartmentID}','{CatID}','{ProductID}','{New_name}', '{price}')
                        """
                    mod = messagebox.askquestion('Agregar', '¿Estás seguro de querer agregar esta variación?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Variation_Tvw, db.query(f"SELECT ID, Description, Price FROM Variations WHERE ProductID = '{ProductID}'"),clean_lvl=None)
                    add_window.destroy()
                else:
                    try:
                        Old_name = Variation_Tvw.item(Variation_Tvw.focus())['values'][1]
                        Old_price = Variation_Tvw.item(Variation_Tvw.focus())['values'][2]
                        ProductID = Product_Tvw.item(Product_Tvw.focus())['values'][0]
                        if Old_name == New_name and Old_price == price:
                            raise RuntimeError
                            
                    except:
                        messagebox.showerror('Error', 'El nombre no ha cambiado')
                        add_window.destroy()
                        return
                    try:
                        VariationID = Variation_Tvw.item(Variation_Tvw.focus())['values'][0]
                    except:
                        messagebox.showerror('Error', 'No se ha seleccionado una variación')
                        add_window.destroy()
                        return
                    
                    query_string = f"""
                        UPDATE Variations
                        SET Description = '{New_name}', Price = '{price}'
                        WHERE ID = '{VariationID}'
                        """
                    mod = messagebox.askquestion('Modificar', '¿Estás seguro de querer modificar esta variación?')
                    if not mod == 'yes':
                        add_window.destroy()
                        return

                    db.update(query_string)
                    update_treeview(Variation_Tvw, db.query(f"SELECT ID, Description, Price FROM Variations WHERE ProductID = '{ProductID}'"),clean_lvl=None)
                    add_window.destroy()
            case default:
                pass
    
    def Add_Item_window(Type: str, add: bool, weight: bool, price: bool) -> None:

        global add_window 
        add_window = Toplevel()
        add_window.geometry('300x200')
        add_window.config(bg = '#E9967A')
        weight_boolean = BooleanVar()
        weight_boolean.set(False)
        price_value = DoubleVar()
        price_value.set(0.0)

        if add == True:
            add_window.title(f'Agregar {Type}')
        else:
            add_window.title(f'Modificar {Type}')

        if price:
            text = f'Nombre {Type} y precio'
        else:
            text = f'Nombre {Type}'

        Name_label = Label(add_window, text = text)
        Name_label.config(bg = '#E9967A', font = 'Arial 14 bold')
        Name_label.pack(pady = 10)

    
        Body_frame = Frame(add_window)
        Body_frame.config(bg = '#E9967A')
        Body_frame.pack(anchor=CENTER, pady = 10)

        if price:
            Name_entry = Entry(Body_frame)
            Name_entry.config(justify = 'center', bd = 3, relief = SUNKEN, width=20)
            Name_entry.grid(row = 0, column = 0, padx = 10, pady = 10)

            Price_entry = Entry(Body_frame, textvariable = price_value)
            Price_entry.config(justify = 'center', bd = 3, relief = SUNKEN, width=10)
            Price_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
            
        else:
            Name_entry = Entry(Body_frame)
            Name_entry.config(justify = 'center', bd = 3, relief = SUNKEN, width=30)
            Name_entry.grid(row = 0, column = 0, padx = 10, pady = 10)

        if not add:
            try:
                match Type:
                    case 'Departamento':
                        Name_entry.insert(0, Department_Tvw.item(Department_Tvw.focus())['values'][1])
                    case 'Categoría':
                        Name_entry.insert(0, Category_Tvw.item(Category_Tvw.focus())['values'][1])
                    case 'Producto':
                        Name_entry.insert(0, Product_Tvw.item(Product_Tvw.focus())['values'][1])
                        if weight:
                            weight_value = Product_Tvw.item(Product_Tvw.focus())['values'][2]
                            if weight_value == 'True':
                                weight_boolean.set(True)
                            else:   
                                weight_boolean.set(False)

                            print(weight_boolean.get(), type(weight_boolean.get()))
                    case 'Variación':
                        Name_entry.insert(0, Variation_Tvw.item(Variation_Tvw.focus())['values'][1])
                        if price:
                            price_value.set(Variation_Tvw.item(Variation_Tvw.focus())['values'][2])
                    case default:
                        pass
            except:
                messagebox.showerror('Error', 'No se ha seleccionado un departamento')
                add_window.destroy()
                return

        if weight == True:
            weight_frame = Frame(add_window)
            weight_frame.config(bg = '#E9967A')
            weight_frame.pack(pady = 10)

            weight_label = Label(weight_frame, text = 'Peso')
            weight_label.config(bg = '#E9967A', font = 'Arial 14 bold')
            weight_label.pack(side = LEFT)

            weight_check = Checkbutton(weight_frame, var = weight_boolean)
            weight_check.config(bg = '#E9967A')
            weight_check.pack(side = LEFT)

            Command = lambda: modify_in_tree(Type, add, [Name_entry.get(), weight_boolean.get()])

        else:
            Command = lambda: modify_in_tree(Type, add, [Name_entry.get()])
            if price:
                Command = lambda: modify_in_tree(Type, add, [Name_entry.get(), price_value.get()])
        Button_frame = Frame(add_window)
        Button_frame.config(bg = '#E9967A')
        Button_frame.pack(pady = 10)

        if add == True:
            Add_button = Button(Button_frame, text = 'Agregar', command= Command)
            Add_button.config(width = 20)
            Add_button.pack(side = 'left', padx = 10)
        else:
            Update_button = Button(Button_frame, text = 'Modificar', command= Command)
            Update_button.config(width = 20)
            Update_button.pack(side = 'left', padx = 10)

        Cancel_button = Button(Button_frame, text = 'Cancelar', command = add_window.destroy)
        Cancel_button.config(width = 20)
        Cancel_button.pack(side = LEFT, padx = 10)

        add_window.protocol("WM_DELETE_WINDOW", add_window.destroy)
    
    def Search(args, ID, searchbox):

        if searchbox:
            search_option = f"Prod.Description like '%{ID}%'"
            pass
        else:
            search_option = f"Var.ID = {ID}"
            pass
        try:
            fill_variation_query_string = f"""
                SELECT Var.ID, 
                    Dep.Description,
                    Cat.Description,
                    Prod.Description,
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
                WHERE {search_option}
                """
            if searchbox:
                items = db.query(fill_variation_query_string)
                update_treeview(Items_Tvw, items,clean_lvl=3)
            else:
                item = db.query(fill_variation_query_string)[0]
                update_treeview(Items_Tvw, [item],clean_lvl=None)
            return
        except:
            return
    ######################################

    DataWn = Toplevel()

    winy = DataWn.winfo_screenheight() * 0.8
    winx = DataWn.winfo_screenwidth() * 0.5

    dy = 600
    dx = 700

    DataWn.geometry('%ix%i'%(winx,winy))
    DataWn.title("ADMINISTRADOR DE DATOS")
    DataWn.config(bg = '#E9967A')

    TimePress = IntVar()
    TimePress.set(0)

    #ETIQUETAS
    var = StringVar()
    var.set(Options[2])
    var.trace('w', Change_Frame)
    barraMenu = OptionMenu(DataWn, var, *Options)
    barraMenu.place(relx = 0.5, rely = 0.03, relwidth = 0.3, anchor = CENTER)

    #Frame Productos
    Frame_Product = Frame(DataWn)
    Frame_Product.config(bg = '#E9967A')
    Frame_Product.place(relx = 0, rely = 50/dy, relwidth = 1, relheight = 1)

    Frame_Seccion3 = Frame(Frame_Product)  #Sección de edición
    Frame_Seccion3.config(bg = '#E9967A')
    Frame_Seccion3.place(x= 0, rely=0.5,relwidth=1,relheight=1)


    ##LABEL FRAMES IN PRODUCTS
 
    ###LISTAS
    Frame_buttons1 = Frame(Frame_Product)
    Frame_buttons1.config(bg = '#E9967A')
    Frame_buttons1.place(relx = 0.15, rely = 0.01, relwidth = 0.15, relheight = 0.05)

    plus_button1 = Button(Frame_buttons1, text= '+', fg= 'green', command= lambda: Add_Item_window('Departamento', True, False, False))
    plus_button1.pack(side = LEFT, padx = 2)
    minus_button1 = Button(Frame_buttons1, text= '-', fg= 'red', command= lambda: Delete_Item('Departament'))
    minus_button1.pack(side = LEFT, padx = 2)
    edit_button1 = Button(Frame_buttons1, text= 'Editar', fg= 'blue', command= lambda: Add_Item_window('Departamento', False, False, False))
    edit_button1.pack(side = LEFT, padx = 2)    

    Department_Tvw = ttk.Treeview(Frame_Product, columns=(1,2),show='headings')
    Department_Tvw.place(relx=0.1,rely=0.05, relwidth=0.25,relheight=0.15)
    Department_Tvw.column(1, width=25)
    Department_Tvw.column(2, width=180)
    Department_Tvw.heading(1, text = 'ID')
    Department_Tvw.heading(2, text = 'Departamento')
    Department_Tvw.bind('<Double 1>',lambda x: getrow(x, 'Departament'))

    for i in db.query("SELECT * FROM Departments"):
        Department_Tvw.insert("",END, values = i)

    Frame_buttons2 = Frame(Frame_Product)
    Frame_buttons2.config(bg = '#E9967A')
    Frame_buttons2.place(relx = 0.15, rely = 0.21, relwidth = 0.15, relheight = 0.05)

    plus_button2 = Button(Frame_buttons2, text= '+', fg= 'green', command= lambda: Add_Item_window('Categoría', True, False, False))
    plus_button2.pack(side = LEFT, padx = 2)
    minus_button2 = Button(Frame_buttons2, text= '-', fg= 'red', command= lambda: Delete_Item('Category'))
    minus_button2.pack(side = LEFT, padx = 2)
    edit_button2 = Button(Frame_buttons2, text= 'Editar', fg= 'blue', command= lambda: Add_Item_window('Categoría', False, False, False)) 
    edit_button2.pack(side = LEFT, padx = 2)

    Category_Tvw = ttk.Treeview(Frame_Product, columns=(1,2),show='headings')
    Category_Tvw.place(relx=0.1,rely=0.25, relwidth=0.25,relheight=0.2)
    Category_Tvw.column(1, width=25)
    Category_Tvw.column(2, width=180)
    Category_Tvw.heading(1, text = 'ID')
    Category_Tvw.heading(2, text = 'Categoría')
    Category_Tvw.bind('<Double 1>',lambda x: getrow(x, 'Category'))

    Frame_buttons3 = Frame(Frame_Product)
    Frame_buttons3.config(bg = '#E9967A')
    Frame_buttons3.place(relx = 0.45, rely = 0.01, relwidth = 0.15, relheight = 0.05)

    plus_button3 = Button(Frame_buttons3, text= '+', fg= 'green', command= lambda: Add_Item_window('Producto', True, True, False))
    plus_button3.pack(side = LEFT, padx = 2)
    minus_button3 = Button(Frame_buttons3, text= '-', fg= 'red', command= lambda: Delete_Item('Product'))
    minus_button3.pack(side = LEFT, padx = 2)
    edit_button3 = Button(Frame_buttons3, text= 'Editar', fg= 'blue', command= lambda: Add_Item_window('Producto', False, True, False))
    edit_button3.pack(side = LEFT, padx = 2)

    Product_Tvw = ttk.Treeview(Frame_Product, columns=(1,2,3),show='headings')
    Product_Tvw.place(relx=0.37,rely=0.05, relwidth=0.32,relheight=0.40)
    Product_Tvw.column(1, width=10)
    Product_Tvw.column(2, width=180)
    Product_Tvw.column(3, width=20)
    Product_Tvw.heading(1, text = 'ID')
    Product_Tvw.heading(2, text = 'Producto')
    Product_Tvw.heading(3, text = 'Peso')
    Product_Tvw.bind('<Double 1>',lambda x: getrow(x, 'Product'))

    Frame_buttons4 = Frame(Frame_Product)
    Frame_buttons4.config(bg = '#E9967A')
    Frame_buttons4.place(relx = 0.75, rely = 0.01, relwidth = 0.15, relheight = 0.05)

    plus_button4 = Button(Frame_buttons4, text= '+', fg= 'green', command= lambda: Add_Item_window('Variación', True, False, True))
    plus_button4.pack(side = LEFT, padx = 2)
    minus_button4 = Button(Frame_buttons4, text= '-', fg= 'red', command= lambda: Delete_Item('Variation'))
    minus_button4.pack(side = LEFT, padx = 2)
    edit_button4 = Button(Frame_buttons4, text= 'Editar', fg= 'blue', command= lambda: Add_Item_window('Variación', False, False, True))
    edit_button4.pack(side = LEFT, padx = 2)

    Variation_Tvw = ttk.Treeview(Frame_Product, columns=(1,2,3),show='headings')
    Variation_Tvw.place(relx=0.72,rely=0.05, relwidth=0.2,relheight=0.40)
    Variation_Tvw.column(1, width=10)
    Variation_Tvw.column(2, width=60)
    Variation_Tvw.column(3, width=20)
    Variation_Tvw.heading(1, text = 'ID')
    Variation_Tvw.heading(2, text = 'Variación')
    Variation_Tvw.heading(3, text = 'Precio')
    Variation_Tvw.bind('<Double 1>',lambda x: Search(x,Variation_Tvw.item(Variation_Tvw.focus())['values'][0], False))
    fill_variation_query_string = f"""
        SELECT Var.ID, 
            Dep.Description,
            Cat.Description,
            Prod.Description,
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
    """

    Items_Tvw = ttk.Treeview(Frame_Product, columns=(1,2,3,4,5,6),show='headings')
    Items_Tvw.place(relx=0.1,rely=0.50, relwidth=0.82,relheight=0.3)
    Items_Tvw.column(1, width=25)
    Items_Tvw.column(2, width=80)
    Items_Tvw.column(3, width=80)
    Items_Tvw.column(4, width=180)
    Items_Tvw.column(5, width=80)
    Items_Tvw.column(6, width=80)
    Items_Tvw.heading(1, text = 'ID')
    Items_Tvw.heading(2, text = 'Departamento')
    Items_Tvw.heading(3, text = 'Categoría')
    Items_Tvw.heading(4, text = 'Producto')
    Items_Tvw.heading(5, text = 'Variación')
    Items_Tvw.heading(6, text = 'Precio')
    Items_Tvw.bind('<Double 1>',lambda x: General(Items_Tvw.item(Items_Tvw.focus())['values'][0]))

    for row in db.query(fill_variation_query_string):
        try:
            Items_Tvw.insert("",END, values = row)
        except:
            messagebox.showerror('Error', 'Error al cargar la tabla de variaciones')


    ### FRAME BUSCAR PRODUCTOS Y SU VARIACIONES

    Frame_buscar_productos = Frame(Frame_Product)
    Frame_buscar_productos.config(bg = '#E9907A')
    Frame_buscar_productos.place(relx = 0.1, rely = 0.82, relwidth = 0.82, relheight = 0.07)
    
    ##ETIQUETAS
    lblsearch= Label(Frame_buscar_productos, text = 'Buscar:')
    lblsearch.config(bg = '#E9967A', font = 'Arial 14 bold')
    lblsearch.grid(row=0, column=0, padx=10)
    
    Entsearch = Entry(Frame_buscar_productos)
    Entsearch.config(justify = 'center',width=55)
    Entsearch.grid(row=0, column=1, padx=10)
    Entsearch.bind('<Return>', lambda x: Search(x,Entsearch.get(), True))
    
    
    ##BOTONES

    Botsearch = Button(Frame_buscar_productos,text = '   Buscar   ' ,command = lambda: Search(None,Entsearch.get(), True))
    Botsearch.grid(row=0, column=2,padx=10)

    Botclear = Button(Frame_buscar_productos, text = '  Limpiar  ', command = lambda: update_treeview(Items_Tvw, db.query(fill_variation_query_string),clean_lvl=3))
    Botclear.grid(row=0, column=3,padx=10)

    ###################################################################################################

    #Frame Empleados
    Frame_Employe = Frame(DataWn)
    Frame_Employe.config(bg = '#E9967A')
    Frame_Employe.place(x = 0, rely = 50/dy, relwidth = 1, relheight = 1)

    ##LISTA
    Employee_items = ttk.Treeview(Frame_Employe, columns=(1,2,3,4),show='headings')
    Employee_items.place(x=0,rely=50/dy, relwidth=1,relheight=0.4)
    Employee_items.column(1, width=10)
    Employee_items.column(2, width=50)
    Employee_items.column(3, width= 50)
    Employee_items.column(4, width = 30)

    Employee_items.heading(1, text = 'id')
    Employee_items.heading(2, text = 'Nombre')
    Employee_items.heading(3, text = 'Apellido')
    Employee_items.heading(4, text = 'Segundo Apellido')

    #Employee_items.bind('<Double 1>',Get_Employee)

    ##FRAME DE DATOS

    EnvolturaEmployeeDATA = LabelFrame(Frame_Employe, text = 'Datos de los Empleados')
    EnvolturaEmployeeDATA.config(bg = '#E9967A')
    EnvolturaEmployeeDATA.place(relx = 5/dx, rely = 300/dy, relwidth = 0.98, height = 200)
    
    ##ETIQUETAS
    lblEmID = Label(EnvolturaEmployeeDATA, text = 'ID:')
    lblEmID.config(bg = '#E9967A', font = 'Arial 12 bold')
    lblEmID.grid(row = 0, column=0,pady = 10)

    lblEmName = Label(EnvolturaEmployeeDATA, text = 'Nombre:')
    lblEmName.config(bg = '#E9967A', font = 'Arial 12 bold')
    lblEmName.grid(row = 1, column=0,pady = 10)

    lblEmAP1 = Label(EnvolturaEmployeeDATA, text = 'Apellido:')
    lblEmAP1.config(bg = '#E9967A', font = 'Arial 12 bold')
    lblEmAP1.grid(row = 2, column = 0,pady = 10)

    lblEmAP2 = Label(EnvolturaEmployeeDATA, text= 'Apellido 2:')
    lblEmAP2.config(bg = '#E9967A', font = 'Arial 12 bold')
    lblEmAP2.grid(row = 3, column = 0, pady = 10)

    ##ENTRADAS DE DATOS
    Em_ID = IntVar()
    Em_ID.set("")
    Em_Name = StringVar()
    Em_AP1 = StringVar()
    Em_AP2 = StringVar()


    EntEmID = Entry(EnvolturaEmployeeDATA, textvariable = Em_ID)
    EntEmID.config(justify = 'center')
    EntEmID.grid(row = 0, column = 1)

    EntEmName = Entry(EnvolturaEmployeeDATA, textvariable = Em_Name)
    EntEmName.config(justify = 'center')
    EntEmName.grid(row = 1, column = 1)

    EntEmAP1 = Entry(EnvolturaEmployeeDATA, textvariable = Em_AP1)
    EntEmAP1.config(justify = 'center')
    EntEmAP1.grid(row = 2, column = 1)

    EntEmAP2 = Entry(EnvolturaEmployeeDATA, textvariable = Em_AP2)
    EntEmAP2.config(justify = 'center')
    EntEmAP2.grid(row = 3, column = 1)

    ##BOTONES

    EmAddBoton = Button(EnvolturaEmployeeDATA, text = '  Agregar  ', command = lambda : Employee_Data(1))
    EmAddBoton.config(width = 20)
    EmAddBoton.grid(row = 0, column = 2, columnspan = 4, padx = 30)

    EmDeleteBoton = Button(EnvolturaEmployeeDATA, text = '  Borrar  ', command = lambda: Employee_Data(2))
    EmDeleteBoton.config(width = 20)
    EmDeleteBoton.grid(row = 1, column = 2, columnspan = 4, padx = 30)

    EmupdateBoton = Button(EnvolturaEmployeeDATA, text = '  Actualizar  ',command = lambda: Employee_Data(3))
    EmupdateBoton.config(width = 20)
    EmupdateBoton.grid(row = 2, column = 3, columnspan = 4, padx = 30)

    EmClearBoton = Button(EnvolturaEmployeeDATA, text = '  Limpiar  ',command = lambda: Employee_Data(0))
    EmClearBoton.config(width = 20)
    EmClearBoton.grid(row = 3, column = 3, columnspan = 4, padx = 30)

    ##FRAME REGISTRO
    Frame_registro = Frame(DataWn)
    Frame_registro.config(bg = '#E9967A')
    Frame_registro.place(relx = 0, rely = 50/dy, relwidth = 1, relheight = 1)

    Registro_items = ttk.Treeview(Frame_registro, columns=(1,2,3,4,5,6,7,8,10,9,11),show='headings')
    Registro_items.place(x=0,rely=50/dy, relwidth=1,relheight=0.4)
    Registro_items.column(1, width=5)
    Registro_items.column(2, width=5)
    Registro_items.column(3, width= 5)
    Registro_items.column(4, width = 10)
    Registro_items.column(5, width=10)
    Registro_items.column(6, width=10)
    Registro_items.column(7, width= 10)
    Registro_items.column(8, width = 10)
    Registro_items.column(9, width = 10)
    Registro_items.column(10, width = 10)
    Registro_items.column(11, width = 10)

    Registro_items.heading(1, text = 'Cod_Venta')
    Registro_items.heading(2, text = 'Mesa')
    Registro_items.heading(3, text = 'Tipo')
    Registro_items.heading(4, text = 'ID_Empleado')
    Registro_items.heading(5, text = 'Ganancia')
    Registro_items.heading(6, text = 'Importe')
    Registro_items.heading(7, text = 'Descuento')
    Registro_items.heading(8, text = 'No.Per')
    Registro_items.heading(9, text = 'Factura')
    Registro_items.heading(10, text = 'Met_Pago')
    Registro_items.heading(11, text = 'Fecha')
    
    Regitems_mesas = ttk.Treeview(Frame_registro, columns=(1,2,3,4,5), show = 'headings')
    Regitems_mesas.place(x = 0, rely = 300/dy, relwidth = 0.55, relheight = 0.4)
    Regitems_mesas.column(1, minwidth = 0, width = 20)
    Regitems_mesas.column(2, minwidth = 0, width = 20)
    Regitems_mesas.column(3, minwidth = 0, width = 40)
    Regitems_mesas.column(4, minwidth = 0, width = 70)
    Regitems_mesas.column(5, minwidth = 0, width = 20)


    Regitems_mesas.heading(1, text = 'Cod_Venta')
    Regitems_mesas.heading(2, text = 'No.Mesa')
    Regitems_mesas.heading(3, text = 'Cantidad')
    Regitems_mesas.heading(4, text = 'Producto')
    Regitems_mesas.heading(5, text = 'Costo')
    
    Fecha = time.strftime("%d/%b/%Y") #Fecha actual

    #Registro_items.bind('<Double 1>',Get_Registro)

    ###FRAME LABEL
    EnvolutrainteractReg = LabelFrame(Frame_registro, text = 'Opciones')
    EnvolutrainteractReg.config(bg = '#E9967A')
    EnvolutrainteractReg.place(relx = 410/dx, rely = 300/dy, relwidth = 0.4, relheight = 23/60)

    ####ETIQUETAS
    Borrarlbl = Label(EnvolutrainteractReg, text = 'Borrar')
    Borrarlbl.config(bg ='#E9967A', font = 'Arial 15 bold')
    Borrarlbl.pack()

    ####ENTRADAS DE TEXTO
    varborrar = StringVar()
    BorrarEntry = Entry(EnvolutrainteractReg, textvariable = varborrar)
    BorrarEntry.config(justify = 'center', bd = 3, relief = SUNKEN)
    BorrarEntry.pack(pady = 5)

    ####BOTONES
    BorrarBoton = Button(EnvolutrainteractReg, text = '  Borrar  ', command = Borrar_Registro)
    BorrarBoton.pack(pady = 5)

    LimpiarBoton = Button(EnvolutrainteractReg, text = '  Limpiar  ', command = Limpiar_Registro)
    LimpiarBoton.pack(pady = 5)

    Frame_registro.tkraise()
    DataWn.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == '__main__':
    Data_Window()
    print("Hola")