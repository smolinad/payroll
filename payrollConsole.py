employees = []
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


def payroll():
    MINIMUM_WAGE = 908526
    TRANSPORT_HELP = 106454
    global employees

    # INPUT
    idnumber = ""
    print("Ingrese la cédula del empleado:")
    while idnumber == "":
        idnumber = str(input())
        if idnumber == "":
            print("Ingrese la cédula del empleado:")

    name = ""
    print("Ingrese el nombres y apellidos del empleado:")
    while name == "":
        name = str(input())
        if name == "":
            print("Ingrese el nombre del empleado de nuevo")

    monthly_salary = -1
    print("Ingrese su salario básico mensual:")
    while monthly_salary <= 0:
        monthly_salary = float(input())
        if monthly_salary <= 0:
            print("El salario básico mensual debe ser mayor a 0. Ingrese este valor de nuevo.")

    days_worked = -1
    print("Ingrese la cantidad de días laborados en el mes:")
    while days_worked < 0 or days_worked > 30:
        days_worked = int(input())
        if days_worked < 0 or days_worked > 30:
            print("La cantidad de días laborados en el mes debe ser mayor o igual a 0 y menor o igual a 30. "
                  "Ingrese este valor de nuevo.")

    ordinary_extra_day_hours = -1
    print("Ingrese el número de horas extra diurnas ordinarias trabajadas")
    while ordinary_extra_day_hours < 0:
        ordinary_extra_day_hours = int(input())
        if ordinary_extra_day_hours < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    ordinary_extra_night_hours = -1
    print("Ingrese el número de horas extra nocturnas ordinarias trabajadas")
    while ordinary_extra_night_hours < 0:
        ordinary_extra_night_hours = int(input())
        if ordinary_extra_night_hours < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    weekend_extra_day_hours = -1
    print("Ingrese el número de horas extra diurnas dominicales trabajadas")
    while weekend_extra_day_hours < 0:
        weekend_extra_day_hours = int(input())
        if weekend_extra_day_hours < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    weekend_extra_night_hours = -1
    print("Ingrese el número de horas extra nocturnas dominicales trabajadas")
    while weekend_extra_night_hours < 0:
        weekend_extra_night_hours = int(input())
        if weekend_extra_night_hours < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    night_surcharge = -1
    print("Ingrese el recargo nocturno")
    while night_surcharge < 0:
        night_surcharge = int(input())
        if night_surcharge < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    risk = -1
    print("Ingrese el nivel de riesgo")
    while risk < 0:
        risk = int(input())
        if risk < 0:
            print("Este valor debe ser mayor o igual a 0. Ingrese este valor de nuevo")

    # EARNED
    basic_total = (monthly_salary / 30) * days_worked
    hour_price = basic_total / 240
    transport_help_bool: bool = True if basic_total <= (MINIMUM_WAGE * 2 / 30) * days_worked else False

    if transport_help_bool:
        transport_help_earned = (TRANSPORT_HELP / 30) * days_worked
    else:
        transport_help_earned = 0

    OEDH_earned = ordinary_extra_day_hours * hour_price * 1.25
    OENH_earned = ordinary_extra_night_hours * hour_price * 1.75
    WEDH_earned = weekend_extra_day_hours * hour_price * 2
    WENH_earned = weekend_extra_night_hours * hour_price * 2.5
    total_extra_hours = OEDH_earned + OENH_earned + WEDH_earned + WENH_earned

    total_earned = basic_total + transport_help_earned + total_extra_hours

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

    params = [idnumber,
              name,
              monthly_salary,
              days_worked,
              ordinary_extra_day_hours,
              ordinary_extra_night_hours,
              weekend_extra_day_hours,
              weekend_extra_night_hours,
              night_surcharge,
              basic_total,
              transport_help_earned,
              total_extra_hours,
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
              net_payment]

    employees.append(params)


if __name__ == '__main__':
    number = -1
    while number < 0:
        print("Ingrese la cantidad de empleados que quiere añadir a la nónima")
        number = int(input())

    for i in range(number):
        payroll()

    for employee in employees:
        aux = 1
        print(f"\nEmpleado #{aux}:")
        for i in range(len(employee)):
            print(table_labels[i] + ":", employee[i])
        aux += 1

    aux = [list(employee)[2:] for employee in employees]
    sum_all = [sum(x) for x in zip(*aux)]

    print("\nTOTAL:")
    for label in range(2, len(sum_all)):
        print(table_labels[label] + ":", sum_all[label-2])



