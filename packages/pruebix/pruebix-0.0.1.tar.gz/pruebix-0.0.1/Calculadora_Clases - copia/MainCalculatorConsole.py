import pickle
import CalculatorSuma
import CalculatorResta
import CalculatorMultiplicar
import CalculatorDivision

print("Calculadora De Escritorio")
print("Suma = 1")
print("Resta = 2")
print("Multiplicacion = 3")
print("Division = 4")

operator = int(input('Selecciona Operacion Aritmetica: '))

if operator == 1:
    number_1 = float(input('Enter your first number: '))
    number_2 = float(input('Enter your second number: '))
    CalculatorSuma.main(number_1, number_2)
     
if operator == 2:
    number_1 = float(input('Enter your first number: '))
    number_2 = float(input('Enter your second number: '))
    CalculatorResta.main(number_1, number_2)

if operator == 3:
    number_1 = float(input('Enter your first number: '))
    number_2 = float(input('Enter your second number: '))
    CalculatorMultiplicar.main(number_1, number_2)

if operator == 4:
    number_1 = float(input('Enter your first number: '))
    number_2 = float(input('Enter your second number: '))
    CalculatorDivision.main(number_1, number_2)

else:
    print("El numero insertado no es valido...")

