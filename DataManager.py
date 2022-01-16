import collections
from tkinter import  *
from tkinter import  ttk
from tkinter import messagebox

import  sqlite3
import time
from typing import Collection

with sqlite3.connect('Base_de_Datos/DataBase.db') as db:
    cursor = db.cursor()

#SECCIONES

def Data_Window():
   
    Options = ['Productos','Empleados','Registro']
    Sections_All = ['Cocteles', 'Bebidas','Platillos','Caldos','Pescados','Postres']
    
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
    
    def Change_Section(event):
        Lectura = Product_items.get_children()
        veces = TimePress.get()
        Labelframetype = Section.get()  

        if event == 1:
            veces = veces + 1
            if veces >= 0 and veces <= 5:
                TimePress.set(veces)
                Section.set(Sections_All[veces])
        else:
            if veces > 0:
                veces = veces - 1 
                TimePress.set(veces)
                Section.set(Sections_All[veces])
        if Section.get() == 'Cocteles':
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM COCTELES")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)

        elif Section.get() == 'Platillos':
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM PLATILLOS")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)
            pass
        elif Section.get() == 'Caldos':
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM CALDOS")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)
            pass
        elif Section.get() == 'Pescados':
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM PESCADOS")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)
            pass
        elif Section.get() == 'Postres':
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM POSTRES")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)
            pass
        else:
            Product_items.delete(*Lectura)
            cursor.execute("SELECT id, Nombre, Precio FROM BEBIDAS")
            rows = cursor.fetchall()
            for x in rows:
                Product_items.insert("", END, values=x)
            pass
    
    def UpdateSearch_Product(event):
        Lectura = Product_items.get_children()
        Product_items.delete(*Lectura)
        for i in event:
            Product_items.insert("", END, values=i)

    def Search_Product(section):
        q = str(query.get())

        for row in Sections_All:
            if row == section:
                cursor.execute("SELECT * FROM " + row + " WHERE Nombre LIKE '%"+q+"%' OR Precio = ?",[q])
                a = cursor.fetchall()
        UpdateSearch_Product(a) 

    def Clear_Product(section):
        Entsearch.delete(0,END)
        cursor.execute("SELECT * FROM " + section +" ")
        rows = cursor.fetchall()
        UpdateSearch_Product(rows)

    def getrow(event):
        rowid = Product_items.identify_row(event.y)
        item = Product_items.item(Product_items.focus())
        p_id.set(item['values'][0])
        p_Name.set(item['values'][1])
        p_Price.set(item['values'][2])

    def Clear(section):
        cursor.execute("SELECT * FROM " + section + " ")
        Product_items.delete(*Product_items.get_children())
        for i in cursor.fetchall():
            Product_items.insert("",END, values = i)

            EntID.delete(0, END)
            EntName.delete(0, END)
            EntPrice.delete(0, END)
        
    def Delete_Product(section):
        Productid = p_id.get()
        if messagebox.askyesno('Eliminar Producto','¿Estás seguro de querer borrar este producto?'):
            cursor.execute("DELETE FROM " + section +" WHERE id = ?", [Productid])
            db.commit()
            Clear(section)

    def Add_Product(section):
        Identidad = p_id.get()
        Nombre = p_Name.get()
        Precio = p_Price.get()
        cursor.execute("INSERT INTO "+ section + " (id, Nombre, Precio) VALUES(?,?,?)",(Identidad,Nombre,Precio))
        db.commit()
        Clear(section)

    def Update_Product(section):
        Identidad = p_id.get()
        Nombre = p_Name.get()
        Precio = p_Price.get()

        if messagebox.askyesno("CONFIRMAR", "¿Estás seguro de querer modificar este producto?"):
            cursor.execute("UPDATE " + section + " SET Nombre = ?, Precio = ? WHERE id = ?", (Nombre, Precio, Identidad))
            Clear(section)
            db.commit()
        
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

    ######################################

    DataWn = Toplevel()

    winy = DataWn.winfo_screenheight() * (600/768)
    winx = DataWn.winfo_screenwidth() * (700/1366)

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

    ## Secciones del frame productos

    Frame_Seccion1 = Frame(Frame_Product)  #Cambiador de listas
    Frame_Seccion1.config(bg = '#E9967A')
    Frame_Seccion1.place(relx=0.38, y = 0)

    Frame_Seccion3 = Frame(Frame_Product)  #Sección de edición
    Frame_Seccion3.config(bg = '#E9967A')
    Frame_Seccion3.place(x= 0, rely=0.5,relwidth=1,relheight=1)
    ### FRAME SECCIÓN 1:
    LeftButton = Button(Frame_Seccion1, text = '<', command = lambda : Change_Section(0))
    LeftButton.grid(row=0,column=0)
    #LeftButton.place(relx = 222/dx, rely = 13/dy)

    Section = StringVar(Frame_Product)
    Section.set(Sections_All[0]) 
    Section.trace('w',Change_Section)
    Sect = Label(Frame_Seccion1, textvariable = Section)
    Sect.config(bg = "#E9967A",bd = 2, relief = SUNKEN, font = 'Arial 18 bold',width=10)
    Sect.grid(row=0, column=1)

    Right_Button = Button(Frame_Seccion1, text = '>', command = lambda : Change_Section(1))
    Right_Button.grid(row=0,column=2)

    ##LABEL FRAMES IN PRODUCTS
 
    ###LISTAS
    Product_items = ttk.Treeview(Frame_Product, columns=(1,2,3),show='headings')
    Product_items.place(relx=0,rely=50/dy, relwidth=1,relheight=0.4)
    Product_items.column(1, width=25)
    Product_items.column(2, width=180)
    Product_items.column(3, width= 30)
    Product_items.heading(1, text = 'id')
    Product_items.heading(2, text = 'Nombre')
    Product_items.heading(3, text = 'Precio')
    Product_items.bind('<Double 1>',getrow)

    cursor.execute("SELECT id, Nombre, Precio FROM COCTELES")
    rows = cursor.fetchall()
    for x in rows:
        Product_items.insert("", END, values=x)
    
    ### ENVOLTURAS PARA LA SECCIÓN 3:
    Envoltura_Buscar = LabelFrame(Frame_Seccion3, text='  BUSCADOR  ')
    Envoltura_Buscar.config(bg = '#E9967A')
    Envoltura_Buscar.place(relx=0.05, y=0, relwidth=0.90,relheight=0.075)

    Envoltura_Modificar = LabelFrame(Frame_Seccion3, text='  AGREGAR O MODIFICAR EXISTENTES  ')
    Envoltura_Modificar.config(bg = '#E9967A')
    Envoltura_Modificar.place(relx=0.05, rely=0.1, relwidth=0.90,relheight=0.30)

    ##ETIQUETAS
    lblsearch= Label(Envoltura_Buscar, text = 'Ingrese:')
    lblsearch.config(bg = '#E9967A', font = 'Arial 14 bold')
    lblsearch.grid(row=0, column=0, padx=10)

    lblName = Label(Envoltura_Modificar, text = 'Nombre:')
    lblName.config(bg='#E9967A', font = 'Arial 14 bold')
    lblName.grid(row=0, column=0,padx=10)

    lblID = Label(Envoltura_Modificar, text = "ID Producto:")
    lblID.config(bg='#E9967A', font = 'Arial 14 bold')
    lblID.grid(row=1, column=0,padx=10)

    lblPrice = Label(Envoltura_Modificar, text = 'Precio:')
    lblPrice.config(bg='#E9967A', font = 'Arial 14 bold')
    lblPrice.grid(row=2, column=0,padx=10)

    ##ENTRADAS
    query = StringVar()
    p_id = IntVar()
    p_Name = StringVar()
    p_Price = IntVar()
    
    Entsearch = Entry(Envoltura_Buscar, textvariable = query)
    Entsearch.config(justify = 'center',width=70)
    Entsearch.grid(row=0, column=1)
    
    #EntName = Entry(Frame_Product, textvariable = p_Name)
    EntName = Entry(Envoltura_Modificar, textvariable=p_Name)
    EntName.config(justify = 'center',width=50)
    EntName.grid(row=0, column=1)

    EntID = Entry(Envoltura_Modificar, textvariable = p_id)
    EntID.config(justify = 'center',width=50)
    EntID.grid(row=1, column=1)

    EntPrice = Entry(Envoltura_Modificar, textvariable = p_Price)
    EntPrice.config(justify = 'center',width=50)
    EntPrice.grid(row=2, column=1)
    
    ##BOTONES

    Botsearch = Button(Envoltura_Buscar,text = '   Buscar   ' ,command = lambda : Search_Product(Section.get()))
    Botsearch.grid(row=0, column=2,padx=10)

    Botclear = Button(Envoltura_Buscar, text = '  Limpiar  ', command = lambda : Clear_Product(Section.get()))
    Botclear.grid(row=0, column=3,padx=10)

    Frame_Botones_modificar = Frame(Envoltura_Modificar)
    Frame_Botones_modificar.config(bg = '#E9967A')
    Frame_Botones_modificar.grid(row=3, column=0, columnspan=2,padx=30,pady=20, sticky='nsew')

    BotAdd = Button(Frame_Botones_modificar, text = '  Agregar  ', command= lambda : Add_Product(Section.get()))
    BotAdd.grid(row=0, column=0,padx=20)

    BotUpdate = Button(Frame_Botones_modificar, text = '  Actualizar  ', command = lambda : Update_Product(Section.get()))
    BotUpdate.grid(row=0, column=1,padx=20)

    BotErase = Button(Frame_Botones_modificar, text = '  Borrar  ', command = lambda : Delete_Product(Section.get()))
    BotErase.grid(row=0, column=2,padx=20)

    BotClearData = Button(Frame_Botones_modificar, text = '  Limpiar  ', command = lambda: Clear(Section.get()))
    BotClearData.grid(row=0, column=3,padx=20)

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

    Employee_items.bind('<Double 1>',Get_Employee)

    cursor.execute("SELECT id, NOMBRE, APELLIDO1, APELLIDO2 FROM EMPLEADOS")
    rows_E = cursor.fetchall()
    for i in rows_E:
        Employee_items.insert("", END, values=i)

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
    
    Fecha = time.strftime("%d/%b/%Y") 
    cursor.execute("SELECT * FROM REGISTRO WHERE FECHA LIKE '%"+Fecha+"%' AND COD_VENTA > 0")
    for i in cursor.fetchall():
        Registro_items.insert("",END,values = i)

    Registro_items.bind('<Double 1>',Get_Registro)

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
