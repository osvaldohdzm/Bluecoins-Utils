# Bluecoins-Utils

Import BBVA account statements in Mexico to [Bluecoins App](https://www.bluecoinsapp.com/ ) format.

Example: Download excel file from 01 to 31 movements. Or for all to current Sunday.





CARGO PAGO TARJETA DE CRÉDITO								
No se registran movimientos en efectivo								
			

##### 		Importing			

Menu/Ajustes/Gestión de datos/Importar datos/Excel (CSV)/Importar desde excelk

Select the file.

Set estándar version

Codificacion Utf8

Date format dd/MM/yyy

​				
​								

	For Transfer Transaction Type, use the letter “t” – without quotes							
								
	For transfers, create two rows in your CSV file.							
	The first row is the sending account. Make the 1st row a negative amount.							
	The second is the receiving account. Make the 2nd row a negative amount. It must be the same amount.							


​								
​								
	15-Mar							
	15 de marzo en adelante							
								
	Categorizar las transferencias en cada cuenta						Entra	Gasto
	Dejar solo las transferencias de BBVA egreso						Entra	Transfiere
	Dejar solo las transferencias de las demás de ingreso							



python .\ficon.py .\bbva-as-2021-05-05.xlsx

Ingresos BBVA
Trabajo:


Todas las filas que tengan la t deben ser duplicadas para replicar al transacción de transferencia





ñó



Seleccionar la cuenta de Debito / 
Definir ingreso o egreso
=SI(C8=0,"i","e")
Sumar cargo y abono.
=C5+D5
Ordenar de antiguo a  reciente

=SI(Tabla2[@[(1)Type]]="t",-1*Tabla2[@[(4)Amount]],Tabla2[@[(4)Amount]])

Debajo de cada rojo insertas un espacio

Arriba por menos uno
=D260*-1



#Gastos Santander Crédito
Selecionar cuenta de cret6dito
Exportar movimientos
Formato tabla
Fecha corta
DEl mas antiguo al más reciente
=SI([@CONCEPTO]="PAGO POR TRANSFERENCIA","t",SI([@IMPORTE]>0,"e","i"))
Eliminar pagos por transferencia


# Gastos Santander Debito
Seleccionar la cuenta
Exportar movimientos
Hacer tabla
=SI([@CONCEPTO]="CARGO PAGO TARJETA CREDITO","t",SI([@RETIRO]="","i","e"))
=[@RETIRO]+[@DEPOSITO]

Cuando se pase a cuenta ed gastos usar referencias CTA GASTOS

atajo isnert6ar fila excel 
CTRL SPACE
CTRL +

CARGO PAGO TARJETA DE CRÉDITO								
No se registran movimientos en efectivo								
		




​								
​	For Transfer Transaction Type, use the letter “t” – without quotes							
​								
​	For transfers, create two rows in your CSV file.							
​	The first row, which is the sending account, should have a negative sign.						
​	The second row, which is the receiving account, should have a positive sign. It must be the same amount.							


​								
​								
​	15-mar							
​	15 de marzo en adelante							
​								
​	Categorizar las transferencias en cada cuenta						Entra	Gasto
​	Dejar solo las transferencias de BBVA egreso						Entra	Transfiere
​	Dejar solo las transferencias de las demás de ingreso							


Cueeda cuando hagas transiferencias poner como concepto en mayusculas sin acentos
el combre de la cuenta
