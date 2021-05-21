from functools import reduce

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import font

import sqlite3
import os.path


# CONSTANTS FOR 2021
MINIMUM_WAGE = 908526
TRANSPORT_HELP = 106454


class Payroll:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(BASE_DIR, 'entries.db')

    # CONSTRUCTOR
    def __init__(self, window_):
        # MAIN WINDOW
        self.window = window_
        self.window.title("Nómina")
        self.window.geometry("1920x1000")
        self.window.iconbitmap('icon.ico')
        self.window.iconphoto(False, PhotoImage(file='icon.png'))

        # APP FONTS
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="SF Pro Rounded", size=8, weight='normal')
        self.button_font = font.Font(family="SF Pro Rounded", size=10)

        # INPUT FRAME
        frame = LabelFrame(self.window, text="Registra un nuevo empleado", font=self.button_font)
        frame.grid(row=0, column=0, columnspan=10, pady=20, padx=380)

        labels = ["Cédula",
                  "Nombre",
                  "Salario mensual básico",
                  "Dias Trabajados",
                  "Horas Extra Ord. Día",
                  "Horas Extra Ord. Noct",
                  "Horas Extra Dom. Día",
                  "Horas Extra Dom. Noct",
                  "Recargo Nocturno",
                  "Nivel de Riesgo"]

        # Input Labels
        column_aux = 0
        for label in labels:
            Label(frame, text=label).grid(row=1, column=column_aux)
            column_aux += 1

        # Inputs
        self.idnumber = Entry(frame)
        self.idnumber.grid(row=2, column=0)

        self.employee_name = Entry(frame)
        self.employee_name.grid(row=2, column=1)

        self.monthly_salary = Entry(frame)
        self.monthly_salary.grid(row=2, column=2)

        self.days_worked = Entry(frame)
        self.days_worked.grid(row=2, column=3)

        self.OEDH = Entry(frame)
        self.OEDH.grid(row=2, column=4)

        self.OENH = Entry(frame)
        self.OENH.grid(row=2, column=5)

        self.WEDH = Entry(frame)
        self.WEDH.grid(row=2, column=6)

        self.WENH = Entry(frame)
        self.WENH.grid(row=2, column=7)

        self.night_surcharge = Entry(frame)
        self.night_surcharge.grid(row=2, column=8)

        self.nivel_riesgo = Entry(frame)
        self.nivel_riesgo.grid(row=2, column=9)

        # BUTTONS
        Button(frame, text="Agregar empleado", command=self.add_entry, font=self.button_font) \
            .grid(row=3, column=0, columnspan=3, sticky=W + E)

        Button(frame, text='Editar', command=self.edit_entry, fg='#007bff', font=self.button_font) \
            .grid(row=3, column=3, columnspan=3, sticky=W + E)

        Button(frame, text='Eliminar', command=self.delete_entry, fg='#ff3b30', font=self.button_font) \
            .grid(row=3, column=6, columnspan=4, sticky=W + E)

        # EDIT WINDOW
        self.edit_window = None

        # TABLE
        table_labels = ["Cédula",
                        "Nombre",
                        "Sal. mes",
                        "DiasT",
                        "HEOD",
                        "HEON",
                        "HEDD",
                        "HEDN",
                        "Recargo Noct",
                        "Total básico",
                        "Aux. Trans.",
                        "Horas extra",
                        "Total deveng.",
                        "Salud",
                        "Pensiones",
                        "Fondo Sol.",
                        "UVT",
                        "Retefuente",
                        "Retepesos",
                        "SaludEmdr",
                        "PensiónEmdr",
                        "Nivel Riesgo",
                        "ARL",
                        "Sena",
                        "ICBF",
                        "CajasComp",
                        "Total Paraf.",
                        "Prima",
                        "Vacaciones",
                        "Cesantías",
                        "Int/Cesantias",
                        "Total Prest.",
                        "Total pagado"]

        self.table_height = 0
        self.get_num_of_entries()

        self.table = ttk.Treeview(self.window, height=self.table_height, columns=table_labels, show='headings')
        self.table.grid(row=5, column=0)

        for column_label in range(len(table_labels)):
            self.table.heading('#' + str(column_label + 1), text=table_labels[column_label], anchor=CENTER)
            if (table_labels[column_label] == "#") or \
                    (table_labels[column_label] == "DiasT") or \
                    (table_labels[column_label] == "HEOD") or \
                    (table_labels[column_label] == "HEON") or \
                    (table_labels[column_label] == "HEDD") or \
                    (table_labels[column_label] == "HEDN") or \
                    (table_labels[column_label] == "Nivel Riesgo") or \
                    (table_labels[column_label] == "Recargo Noct") or \
                    (table_labels[column_label] == "UVT") or \
                    (table_labels[column_label] == "Int/Cesantias"):
                self.table.column('#' + str(column_label + 1), width=25)
            else:
                self.table.column('#' + str(column_label + 1), width=70)

        # TOTAL SUM TABLE
        self.total_row = ttk.Treeview(self.window, height=1, columns=table_labels, show='headings')
        self.total_row.grid(row=6, column=0)

        table_labels[0], table_labels[1] = "", ""
        for column_ in range(len(table_labels)):
            self.total_row.heading('#' + str(column_ + 1), text=table_labels[column_], anchor=CENTER)
            if (table_labels[column_] == "#") or \
                    (table_labels[column_] == "DiasT") or \
                    (table_labels[column_] == "HEOD") or \
                    (table_labels[column_] == "HEON") or \
                    (table_labels[column_] == "HEDD") or \
                    (table_labels[column_] == "HEDN") or \
                    (table_labels[column_] == "Nivel Riesgo") or \
                    (table_labels[column_] == "Recargo Noct") or \
                    (table_labels[column_] == "UVT") or \
                    (table_labels[column_] == "Int/Cesantias"):
                self.total_row.column('#' + str(column_ + 1), width=25)
            else:
                self.total_row.column('#' + str(column_ + 1), width=70)

        self.get_entries()

    # DATABASE QUERY FUNCTION
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            res = cursor.execute(query, parameters)
            conn.commit()
        return res

    # VALIDATE INPUTS
    @staticmethod
    def validate_forms(idnumber, name, monthly_salary, days_worked, oedh,
                       oenh, wedh, wenh, night_surcharge, risk):
        return reduce(lambda x, y: x or y, [len(i) != 0 for i in [idnumber.get(), name.get(),
                                                                  monthly_salary.get(), days_worked.get(),
                                                                  oedh.get(), oenh.get(), wedh.get(), wenh.get(),
                                                                  night_surcharge.get(), risk.get()]])

    # CLEAR INPUTS (AFTER CRUD)
    def clear_inputs(self):
        self.idnumber.delete(0, END)
        self.employee_name.delete(0, END)
        self.monthly_salary.delete(0, END)
        self.days_worked.delete(0, END)
        self.OEDH.delete(0, END)
        self.OENH.delete(0, END)
        self.WEDH.delete(0, END)
        self.WENH.delete(0, END)
        self.night_surcharge.delete(0, END)
        self.nivel_riesgo.delete(0, END)

    # PAYROLL FORMULAS
    @staticmethod
    def payroll(idnumber, name, monthly_salary, days_worked, oedh, oenh, wedh, wenh, night_surcharge, risk):
        # DEVENGADO
        # Salario básico
        basic_total = round((int(monthly_salary) / 30) * int(days_worked))

        # Valor hora
        hour_price = int(basic_total) / 240

        # Auxilio de transporte
        if float(monthly_salary) <= (MINIMUM_WAGE * 2 / 30) * float(days_worked):
            transport_help_earned = round(float(TRANSPORT_HELP / 30) * float(days_worked))
        else:
            transport_help_earned = 0

        # Extra hours 2021
        OEDH_earned = float(oedh) * hour_price * 1.25
        OENH_earned = float(oenh) * hour_price * 1.75
        WEDH_earned = float(wedh) * hour_price * 2
        WENH_earned = float(wenh) * hour_price * 2.5
        night_surcharge_earned = float(night_surcharge) * hour_price * 0.35
        extra_hours_earned = round(OEDH_earned + OENH_earned + WEDH_earned + WENH_earned + night_surcharge_earned)

        # Total earned
        total_earned = round(float(basic_total) + float(transport_help_earned) + float(extra_hours_earned))

        # DEDUCTIONS
        # Health Insurance

        health = round((total_earned - transport_help_earned) * 0.04)
        # Pension input
        pension = health

        # Ingreso solidario
        ingreso_sol = 0
        if total_earned > MINIMUM_WAGE * 4:
            ingreso_sol += 0.1
        if MINIMUM_WAGE * 16 <= total_earned <= MINIMUM_WAGE * 17:
            ingreso_sol += 0.02
        if MINIMUM_WAGE * 17 < total_earned <= MINIMUM_WAGE * 18:
            ingreso_sol += 0.04
        if MINIMUM_WAGE * 18 < total_earned <= MINIMUM_WAGE * 19:
            ingreso_sol += 0.06
        if MINIMUM_WAGE * 19 < total_earned <= MINIMUM_WAGE * 20:
            ingreso_sol += 0.08
        if MINIMUM_WAGE * 20 < total_earned:
            ingreso_sol += 0.1
        ingreso_sol_deduction = total_earned * ingreso_sol

        # UVT
        uvt = round((total_earned - health - pension - ingreso_sol_deduction) * 0.75 / 36308)

        # RETEFUENTE
        if uvt > 2300:
            retefuente = (uvt - 2300) * 0.39 + 770
        elif uvt > 945:
            retefuente = (uvt - 945) * 0.37 + 268
        elif uvt > 640:
            retefuente = (uvt - 640) * 0.35 + 162
        elif uvt > 360:
            retefuente = (uvt - 360) * 0.33 + 69
        elif uvt > 150:
            retefuente = (uvt - 150) * 0.28 + 10
        elif uvt > 95:
            retefuente = (uvt - 95) * 0.19
        else:
            retefuente = 0

        retefuente = round(retefuente)

        retepesos = round(retefuente * 36308)

        # Total deduction
        total_deduction = round(health + pension + ingreso_sol_deduction + retepesos)

        # PARAFISCALES
        health_emp = round((total_earned - transport_help_earned) * 0.085)
        pension_emp = round((total_earned - transport_help_earned) * 0.12)

        arl = 0
        if int(risk) == 1:
            arl = (total_earned - transport_help_earned) * 0.00522
        elif int(risk) == 2:
            arl = (total_earned - transport_help_earned) * 0.01044
        elif int(risk) == 3:
            arl = (total_earned - transport_help_earned) * 0.02436
        elif int(risk) == 4:
            arl = (total_earned - transport_help_earned) * 0.0435
        elif int(risk) == 5:
            arl = (total_earned - transport_help_earned) * 0.0696
        arl = round(arl)

        # SENA
        sena = round((total_earned - transport_help_earned) * 0.02)

        # ICBF
        icbf = round((total_earned - transport_help_earned) * 0.03)

        # CAJAS
        cajas = round(total_earned * 0.04)

        # Total parafiscales
        total_parafiscales = round(arl + sena + icbf + cajas)

        # PRESTACIONES
        prima = round(total_earned * 0.0833)
        holidays = round((total_earned - transport_help_earned) * 0.0417)
        cesantias = prima
        int_cesantias = round(cesantias * 0.01)
        # Total prestaciones
        total_prest = round(prima + holidays + cesantias + int_cesantias)

        # NET PAYMENT
        net_payment = round(total_prest + total_parafiscales + total_earned - total_deduction)

        params = (idnumber,
                  name,
                  monthly_salary,
                  days_worked,
                  oedh,
                  oenh,
                  wedh,
                  wenh,
                  night_surcharge,
                  basic_total,
                  transport_help_earned,
                  extra_hours_earned,
                  total_earned,
                  health,
                  pension,
                  ingreso_sol_deduction,
                  uvt,
                  retefuente,
                  retepesos,
                  health_emp,
                  pension_emp,
                  risk,
                  arl,
                  sena,
                  icbf,
                  cajas,
                  total_parafiscales,
                  prima,
                  holidays,
                  cesantias,
                  int_cesantias,
                  total_prest,
                  net_payment)

        return params

    # GETTING AND DISPLAYING DATABASE ROWS
    def get_entries(self):
        records = self.table.get_children()

        for element in records:
            self.table.delete(element)

        query = 'SELECT * FROM employees ORDER BY nombre ASC'
        db_rows = self.run_query(query)

        for row in db_rows:
            self.table.insert('', END, values=row)

        self.sum()

    def add_entry(self):
        if self.validate_forms(self.idnumber, self.employee_name, self.monthly_salary,
                               self.days_worked, self.OEDH, self.OENH, self.WEDH,
                               self.WENH, self.night_surcharge, self.nivel_riesgo):
            query = 'INSERT INTO employees VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,' \
                    ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,' \
                    ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,' \
                    ' ?, ?, ?)'
            params = self.payroll(self.idnumber.get(), self.employee_name.get(), self.monthly_salary.get(),
                                  self.days_worked.get(), self.OEDH.get(), self.OENH.get(), self.WEDH.get(),
                                  self.WENH.get(), self.night_surcharge.get(), self.nivel_riesgo.get())
            try:
                self.run_query(query, params)
                messagebox.showinfo(title='', message=f"Has añadido a {self.employee_name.get()} a la nómina")
            except sqlite3.IntegrityError:
                messagebox.showerror(title="Error", message="Debes ingresar los datos correctamente "
                                                            "antes de añadir una nueva entrada")
            except OverflowError:
                messagebox.showerror(title='Error', message="Debes ingresar los datos "
                                                            "correctamente antes de editar la entrada")
        else:
            messagebox.showerror(title="Error", message="Debes ingresar los datos correctamente "
                                                        "antes de añadir una nueva entrada")
        self.get_num_of_entries()
        self.table.configure(height=self.table_height)
        self.get_entries()
        self.clear_inputs()

    def delete_entry(self):
        try:
            self.table.item(self.table.selection())['values'][0]
        except IndexError:
            messagebox.showerror(title="Error", message="Debes seleccionar una entrada para eliminar")
        to_delete = self.table.item(self.table.selection())['values']
        query = 'DELETE FROM employees WHERE cedula = ?'
        self.run_query(query, (to_delete[0],))
        messagebox.showinfo(title='', message=f"{to_delete[1]} ha sido eliminado de la nómina")
        self.get_num_of_entries()
        self.table.configure(height=self.table_height)
        self.get_entries()
        self.sum()

    def edit_entry(self):
        try:
            self.table.item(self.table.selection())['values'][0]
        except IndexError:
            messagebox.showerror(title='Error', message="Selecciona una entrada para editar")

        old_idnumber = self.table.item(self.table.selection())['values'][0]
        old_name = self.table.item(self.table.selection())['values'][1]
        old_monthly_salary = self.table.item(self.table.selection())['values'][2]
        old_days_worked = self.table.item(self.table.selection())['values'][3]
        old_OEDH = self.table.item(self.table.selection())['values'][4]
        old_OENH = self.table.item(self.table.selection())['values'][5]
        old_WEDH = self.table.item(self.table.selection())['values'][6]
        old_WENH = self.table.item(self.table.selection())['values'][7]
        old_night_surcharge = self.table.item(self.table.selection())['values'][8]
        old_riesgo = self.table.item(self.table.selection())['values'][21]

        self.edit_window = Toplevel()
        self.edit_window.title = "Editar empleado"
        self.edit_window.iconbitmap('icon.ico')

        edit_frame = LabelFrame(self.edit_window, text="Editar empleado", font=self.button_font)
        edit_frame.grid(row=0, column=0, columnspan=10, pady=20, padx=30)

        Label(edit_frame, text='Cédula', font=self.button_font).grid(row=0, column=1, padx=10)
        idnumber = Entry(edit_frame)
        idnumber.grid(row=0, column=2)
        idnumber.insert(0, old_idnumber)

        Label(edit_frame, text='Nombre', font=self.button_font).grid(row=1, column=1, padx=10)
        employee_name = Entry(edit_frame)
        employee_name.grid(row=1, column=2)
        employee_name.insert(0, old_name)

        Label(edit_frame, text='Salario mensual básico', font=self.button_font).grid(row=2, column=1, padx=10)
        monthly_salary = Entry(edit_frame)
        monthly_salary.grid(row=2, column=2)
        monthly_salary.insert(0, old_monthly_salary)

        Label(edit_frame, text='Días trabajados', font=self.button_font).grid(row=3, column=1, padx=10)
        days_worked = Entry(edit_frame)
        days_worked.grid(row=3, column=2)
        days_worked.insert(0, old_days_worked)

        Label(edit_frame, text='Horas extra ord. diurnas', font=self.button_font).grid(row=4, column=1, padx=10)
        OEDH = Entry(edit_frame)
        OEDH.grid(row=4, column=2)
        OEDH.insert(0, old_OEDH)

        Label(edit_frame, text='Horas extra ord. noct.', font=self.button_font).grid(row=5, column=1, padx=10)
        OENH = Entry(edit_frame)
        OENH.grid(row=5, column=2)
        OENH.insert(0, old_OENH)

        Label(edit_frame, text='Horas extra dom. diurnas', font=self.button_font).grid(row=6, column=1, padx=10)
        WEDH = Entry(edit_frame, text=old_WEDH)
        WEDH.grid(row=6, column=2)
        WEDH.insert(0, old_WEDH)

        Label(edit_frame, text='Horas extra dom. noct.', font=self.button_font).grid(row=7, column=1, padx=10)
        WENH = Entry(edit_frame)
        WENH.grid(row=7, column=2)
        WENH.insert(0, old_WENH)

        Label(edit_frame, text='Recargo Nocturno', font=self.button_font).grid(row=8, column=1, padx=10)
        night_surcharge = Entry(edit_frame)
        night_surcharge.grid(row=8, column=2)
        night_surcharge.insert(0, old_night_surcharge)

        Label(edit_frame, text='Nivel de Riesgo', font=self.button_font).grid(row=9, column=1, padx=10)
        nivel_riesgo = Entry(edit_frame)
        nivel_riesgo.grid(row=9, column=2)
        nivel_riesgo.insert(0, old_riesgo)

        Button(edit_frame, text='Editar entrada', font=self.button_font, fg='#007bff',
               command=lambda: self.edit_forms(idnumber, employee_name, monthly_salary, days_worked, OEDH, OENH, WEDH,
                                               WENH, night_surcharge, nivel_riesgo, old_idnumber)) \
            .grid(row=10, column=0, columnspan=10, sticky=W + E)

    def edit_forms(self, idnumber, name, monthly_salary, days_worked, oedh,
                   oenh, wedh, wenh, night_surcharge, risk, old_idnumber):
        if self.validate_forms(idnumber, name, monthly_salary, days_worked, oedh,
                               oenh, wedh, wenh, night_surcharge, risk):
            query = 'UPDATE employees SET cedula = ?, nombre = ?, salario_mens = ?, dias_trabajados = ?, ' \
                    'heod = ?, heon = ?, hedd = ?, hedn = ?, recargo_noct = ?, basic_total = ?, aux_trans = ?, ' \
                    'extra_hours_earned = ?, total_earned = ?, health = ?, pension = ?, fondo_sol = ?, uvt = ?, ' \
                    'retefuente = ?, retepesos = ?, salud_empdr = ?, pension_empdr = ?, nivel_riesgo = ?, arl = ?, ' \
                    'sena = ?, icbf = ?, cajas = ?, total_para = ?, prima = ?, holidays = ?, cesantias = ?, ' \
                    'int_cesantias = ?, total_prest = ?, net_payment = ? WHERE cedula = ?'
            params = self.payroll(idnumber.get(), name.get(), monthly_salary.get(), days_worked.get(), oedh.get(),
                                  oenh.get(), wedh.get(), wenh.get(), night_surcharge.get(), risk.get())
            params += (old_idnumber,)
            try:
                self.run_query(query, params)
                messagebox.showinfo(title='', message=f"Has editado la nómina de {params[1]}, "
                                                      f"con número de identificación {params[0]}")
            except sqlite3.IntegrityError:
                messagebox.showerror(title='Error', message="Debes ingresar los datos "
                                                            "correctamente antes de editar la entrada")
            except OverflowError:
                messagebox.showerror(title='Error', message="Debes ingresar los datos "
                                                            "correctamente antes de editar la entrada")
        else:
            messagebox.showerror(title='Error', message="Debes ingresar los datos "
                                                        "correctamente antes de editar la entrada")
        self.get_entries()
        self.edit_window.destroy()
        self.get_num_of_entries()
        self.table.configure(height=self.table_height)
        self.get_entries()
        self.sum()

    # SUM COLUMNS QUERY
    def sum(self):
        records = self.total_row.get_children()

        for element in records:
            self.total_row.delete(element)

        query = 'SELECT SUM(salario_mens), SUM(dias_trabajados), ' \
                'SUM(heod), SUM(heon), SUM(hedd), SUM(hedn), SUM(recargo_noct), SUM(basic_total), ' \
                'SUM(aux_trans), SUM(extra_hours_earned), SUM(total_earned), SUM(health), SUM(pension), ' \
                'SUM(fondo_sol), SUM(uvt), SUM(retefuente), SUM(retepesos), SUM(salud_empdr), SUM(pension_empdr), ' \
                'SUM(nivel_riesgo), SUM(arl), SUM(sena), SUM(icbf), SUM(cajas), SUM(total_para), SUM(prima), ' \
                'SUM(holidays), SUM(cesantias), SUM(int_cesantias), SUM(total_prest), SUM(net_payment) FROM employees'

        total = self.run_query(query)
        total_arr = ["TOTAL", '']
        for total in total:
            for vals in total:
                total_arr.append(vals)

        self.total_row.insert('', END, values=total_arr)

    def get_num_of_entries(self):
        query = 'SELECT COUNT(*) FROM employees'
        self.table_height = int(self.run_query(query).fetchall()[0][0])


if __name__ == "__main__":
    window = Tk()
    Payroll(window)
    window.mainloop()
