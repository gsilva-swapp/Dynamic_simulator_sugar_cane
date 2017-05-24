# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Flow_properties.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from decimal import Decimal
import re

from tempfile import mkstemp
from shutil import move
from os import remove, close

import fileinput
import sys

from physicochemical_properties import liquor_properties, water_properties, vapor_properties
liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()

from Flow_inputs import update_flow_data
flow_data=update_flow_data()

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

##--Global variables -- ##

global saturado
global Type_flow_selec
global confirm
global VariableInput
global update
global num_window
global vapor_data
global juice_data
global water_data
vapor_data=[]
juice_data=[]
water_data=[]
num_window=""
update=0
confirm=False
Type_flow_selec=""
saturado=1

VariableInput=_translate("Dialog", "Flujo másico [t/h]", None)

## -- Text field number validator -- ##
class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

## Timer for update vapor flow value ##
def call_timer(objectq):
	timer = QtCore.QTimer(objectq)
	timer.timeout.connect(update_Fv_value)
	timer.start(float(Ts)*1000)

## Update vapor flow value ##
def update_Fv_value():
	input_heat = open('Blocks_data.txt', 'r+')
	data=input_heat.readlines()
	input_heat.close()
	if len(data)>0:
		for i in data:
			info=(i.strip()).split("\t")
			flag=info[0]
			if flag==("Fv"+str(num_window)):
				Flow.setText(str(round(float(info[2]),3)))
				#break

## -- Function to update window when is close -- ##
def Update_window():
	global update
	global num_window
	global vapor_data
	global juice_data
	global water_data
	global saturado
	global VariableInput
	num_window=re.sub('([a-zA-Z]+)', "", nameDialog)
	input_heat = open('Blocks_data.txt', 'r+')
	data=input_heat.readlines()
	comBox_VariableInput.clear()
	VariableInput=_translate("Dialog", "Flujo másico [t/h]", None)
	vapor_data=[]
	juice_data=[]
	water_data=[]
	if len(data)>0:
		for i in data:
			info=(i.strip()).split("\t")
			if len(info)>1:
				flag=info[0]
				if flag==("Fv"+str(num_window)):
					comBox_Type_Flow.setDisabled(1)
					Flow_tabWidget.setCurrentIndex(0)
					update=1
					for k in range(1,len(info)):
						vapor_data.append(float(info[k]))				
					comBox_Type_Flow.setCurrentIndex(2)
					Brix.setDisabled(1)
					Purity.setDisabled(1)
					Insoluble_Solids.setDisabled(1)
					Temp.setDisabled(1)
					Flow.setDisabled(1)
					pH.setDisabled(1)
					Evaporation_Enthalpy.show()
					label_Evaporation_Enthalpy.show()
					checkBox_Saturated_vapor.setChecked(True)
					label_vapor_type.show()
					checkBox_Saturated_vapor.show()
					checkBox_Overheated_vapor.show()
					if str(vapor_data[len(vapor_data)-1])=="1.0": ##Que es un vapor saturado
						saturado=1
						Pressure.setText(str(float(vapor_data[0])/1000.0))
						Flow.setText(str(round(float(vapor_data[1]),3)))
						Temp.setText(str(round(vapor_data[2],3)))
						Specific_Heat.setText(str("{:.3E}".format(Decimal(vapor_data[3]))))
						Density.setText(str(round(vapor_data[4],3)))
						Viscosity.setText(str("{:.3E}".format(Decimal(vapor_data[5]))))
						Enthalpy.setText(str("{:.3E}".format(vapor_data[6])))
						Evaporation_Enthalpy.setText(str("{:.3E}".format(vapor_data[7])))
						Conductivity.setText(str(round(vapor_data[8],3)))
						checkBox_Saturated_vapor.setChecked(True)
						##
						comBox_VariableInput.clear()
						comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
						comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
						##
						call_timer(Dialog_window)						
					else:
						saturado=0
						comBox_VariableInput.clear()
						comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
						comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
						comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))
						pass
				elif flag==("Fj"+str(num_window)):
					comBox_Type_Flow.setDisabled(1)
					Flow_tabWidget.setCurrentIndex(0)
					update=1
					for k in range(1,len(info)):
						juice_data.append(float(info[k]))
					comBox_Type_Flow.setCurrentIndex(1)
					Brix.setEnabled(1)
					Purity.setEnabled(1)
					Insoluble_Solids.setEnabled(1)
					Temp.setEnabled(1)
					pH.setEnabled(1)
					Pressure.setEnabled(1)
					Evaporation_Enthalpy.hide()
					label_Evaporation_Enthalpy.hide()
					label_vapor_type.hide()
					checkBox_Saturated_vapor.hide()
					checkBox_Overheated_vapor.hide()
					Flow.setText(str(juice_data[0]))
					Brix.setText(str(float(juice_data[2])*100.0))
					Purity.setText(str(float(juice_data[3])*100.0))
					Temp.setText(str(round(juice_data[1],3)))
					Insoluble_Solids.setText(str(float(juice_data[4])*100.0))
					pH.setText(str(juice_data[5]))
					Pressure.setText(str(juice_data[6]/1000.0))
					Specific_Heat.setText(str("{:.3E}".format(Decimal(juice_data[7]))))
					Density.setText(str(round(juice_data[8],3)))
					Viscosity.setText(str("{:.3E}".format(Decimal(juice_data[9]))))
					Enthalpy.setText(str("{:.3E}".format(Decimal(juice_data[10]))))
					Conductivity.setText(str(round(juice_data[11],3)))
					##
					comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
					comBox_VariableInput.addItem("Brix [%]")
					comBox_VariableInput.addItem(_translate("Dialog", "Sólidos insolubles [%]", None))
					comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))	
					comBox_VariableInput.addItem("Pureza [%]")
					comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
					comBox_VariableInput.addItem("pH")
				elif flag==("Fw"+str(num_window)):
					comBox_Type_Flow.setDisabled(1)
					Flow_tabWidget.setCurrentIndex(0)
					update=1
					for k in range(1,len(info)):
						water_data.append(float(info[k]))
					comBox_Type_Flow.setCurrentIndex(3)
					Brix.setDisabled(1)
					Purity.setDisabled(1)
					Insoluble_Solids.setDisabled(1)
					pH.setEnabled(1)
					Evaporation_Enthalpy.hide()
					label_Evaporation_Enthalpy.hide()
					Temp.setEnabled(1)
					Pressure.setEnabled(1)
					label_vapor_type.hide()
					checkBox_Saturated_vapor.hide()
					checkBox_Overheated_vapor.hide()
					Flow.setText(str(water_data[0]))
					Temp.setText(str(round(water_data[1],3)))
					pH.setText(str(water_data[2]))
					Pressure.setText(str(water_data[3]/1000.0))
					Density.setText(str(round(water_data[4],3)))
					Enthalpy.setText(str("{:.3E}".format(Decimal(water_data[5]))))
					##
					comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
					comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))		
					comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
					comBox_VariableInput.addItem("pH")
	else:
		update=0
		print "no datos"
	input_heat.close()

## -- Get inputs values / Calculates physical-chemical parameters / Add data to DataBase
class window_confirm_inputs(QDialog):
		def __init__(self, parent=None):
			super(window_confirm_inputs, self).__init__(parent)
			self.setWindowTitle("Confirmar entradas")
			self.button = QPushButton('Aceptar', self)
			self.button2 = QPushButton('Cancelar', self)
			self.label_Message = QtGui.QLabel( _translate("Dialog", "¿Esta seguro que desea confirmar estos datos?",None) ,self)
			l = QHBoxLayout(self)
			l.addWidget(self.label_Message)
			l.addWidget(self.button)
			l.addWidget(self.button2)
			self.button.clicked.connect(self.OK)
			self.button2.clicked.connect(self.NO)

		#**Affirmative selection**#
		def OK(self):

			# -- If select water flow -- ##
			if Type_flow_selec=="Vapor":
				if saturado==1:
				##Get inputs
					Mvin=00.00
					Pvin=(float(Pressure.text()))*1000.0
				##Update steam flow info 
					Tvin,pv,uv,Hv,Yv,Cpv,Hvw=flow_data.update_vapor(Pvin)
				##Set data in text field
					Flow.setText(str(Mvin))
					Temp.setText(str(round(Tvin,3)))
					Density.setText(str(round(pv,3)))
					Viscosity.setText(str("{:.3E}".format(Decimal(uv))))
					Enthalpy.setText(str("{:.3E}".format(Decimal(Hv))))
					Conductivity.setText(str(round(Yv,3)))
					Specific_Heat.setText(str("{:.3E}".format(Decimal(Cpv))))
					Evaporation_Enthalpy.setText(str("{:.3E}".format(Decimal(Hvw))))
				##Prepare frame to data base
					flag0="Fv"
					dato=str(Pvin)+"\t"+str(Mvin)+"\t"+str(Tvin)+"\t"+str(Cpv)+"\t"+str(pv)+"\t"+str(uv)+"\t"+str(Hv)+"\t"+str(Hvw)+"\t"+str(Yv)+"\t"+str(saturado)
				else :
					Mvin=00.00
					Pvin=(float(Pressure.text()))*1000.0
					Tvin=float(Temp.text())
					##
					#....¿?

			# -- If select juice flow -- ##
			elif Type_flow_selec=="Jugo":
			##Get inputs
				Mjin=float(Flow.text())
				Bjin=float(Brix.text())/100.0
				SolIn=float(Insoluble_Solids.text())/100.0
				Tjin=float(Temp.text())
				Zjin=float(Purity.text())/100.0
				pHj=float(pH.text())
				Pj=(float(Pressure.text()))*1000.0
			##Update juice flow info 
				Cpj,pj,uj,Hj,Yj=flow_data.update_juice(Bjin,Zjin,Tjin)		
			##Set data in text field	
				Specific_Heat.setText(str("{:.3E}".format(Decimal(Cpj))))
				Density.setText(str(round(pj,3)))
				Viscosity.setText(str("{:.3E}".format(Decimal(uj))))
				Enthalpy.setText(str("{:.3E}".format(Decimal(Hj))))
				Conductivity.setText(str(round(Yj,3)))
			##Prepare frame to data base
				flag0="Fj"
				dato=str(Mjin)+"\t"+str(Tjin)+"\t"+str(Bjin)+"\t"+str(Zjin)+"\t"+str(SolIn)+"\t"+str(pHj)+"\t"+str(Pj)+"\t"+str(Cpj)+"\t"+str(pj)+"\t"+str(uj)+"\t"+str(Hj)+"\t"+str(Yj)
			
			# -- If select water flow -- ##
			elif Type_flow_selec=="Agua":
			##Get inputs
				Mw=float(Flow.text())
				Tw=float(Temp.text())
				pHw=float(pH.text())
				Pw=(float(Pressure.text()))*1000.0
			##Update water flow info 
				pw,Hw=flow_data.update_water(Tw)
			##Set data in text field
				Density.setText(str(round(pw,3)))
				Enthalpy.setText(str("{:.3E}".format(Decimal(Hw))))
			##Prepare frame to data base
				flag0="Fw"
				dato=str(Mw)+"\t"+str(Tw)+"\t"+str(pHw)+"\t"+str(Pw)+"\t"+str(pw)+"\t"+str(Hw)

			##New changes in data base
			flag=re.sub('([a-zA-Z]+)', "", nameDialog)
			upd, change=update_DB(flag0+flag)
			##First data instance
			if upd==0:
				outfile = open('Blocks_data.txt', 'a')
				outfile.write("\n"+flag0+flag+"\t"+dato)
				outfile.close()
			#Overwrite data instance
			else:
				replace("Blocks_data.txt",change,flag0+flag+"\t"+dato)
			##Information message and close window
			self.close()
			Resultado=QtGui.QDialog()
			QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
			Dialog_window.close()
		def NO(self):
			self.close()

## -- Function to overwrite line in text file --##
def replace(path, pattern, subst):
	flags=0
	with open(path, "r+" ) as filex:
		fileContents = filex.read()
		textPattern = re.compile( re.escape( pattern ), flags )
		fileContents = textPattern.sub( subst, fileContents )
		filex.seek( 0 )
		filex.truncate()
		filex.write(fileContents) 

## -- Function to know line for update Database -- ##
def update_DB(dato):
	flg=0
	dats=""
	input_heat = open('Blocks_data.txt', 'r+')
	data=input_heat.readlines()
	for i in data:
		info=(i.strip()).split("\t")
		if info[0]==dato:
			flg=1
			dats=(i.strip())
	return flg, dats

class Ui_Dialog(object):
## -- Function to confirm all data is complete for each type of flow -- ##
	def confirm_data(self):
		global confirm
		if Type_flow_selec=="Jugo":
			confirm=((len(Flow.text())>0)and(len(Brix.text())>0)and(len(Insoluble_Solids.text())>0)and(len(Temp.text())>0)
				and(len(pH.text())>0)and(len(Purity.text())>0)and(len(Pressure.text())>0))
		elif Type_flow_selec=="Vapor":
			if saturado==1:
				confirm=(len(Pressure.text())>0)
			else:
				confirm=(len(Pressure.text())>0)and(len(Temp.text())>0)
		elif Type_flow_selec=="Agua":
			confirm=(len(Flow.text())>0)and(len(Temp.text())>0)and(len(pH.text())>0)
		else:
			confirm=False

		if Type_flow_selec!="" and confirm==True:
			self.Resultado=QtGui.QDialog()
			pd = window_confirm_inputs(self.Resultado.window())
			pd.exec_()
		else:
			self.Resultado=QtGui.QDialog()
			QtGui.QMessageBox.warning(self.Resultado, 
			'Advertencia',
			"Falta por ingresar algun dato.",QtGui.QMessageBox.Ok)

## -- Initialization window interface --- ##
	def setupUi(self,name,ts,Dialog):
		#Global input
		global Flow
		global Brix
		global Insoluble_Solids
		global Purity
		global Temp
		global pH
		global Pressure
		global comBox_VariableInput
		global comBox_Type_Flow
		global checkBox_Saturated_vapor
		global checkBox_Overheated_vapor
		global SpinBox_VariableInput
		global label_vapor_type
		global Flow_tabWidget
		#Global output
		global Specific_Heat
		global Enthalpy
		global Evaporation_Enthalpy
		global label_Evaporation_Enthalpy
		global Viscosity
		global Density
		global Conductivity
		#Global others
		global Dialog_window
		global nameDialog
		global Ts

		Vali = Validator()
		Ts=ts
		Dialog_window=Dialog
		nameDialog=name

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(444, 319)

	##--Tab widget--##
		Flow_tabWidget = QtGui.QTabWidget(Dialog)
		Flow_tabWidget.setGeometry(QtCore.QRect(10, 37, 421, 271))
		Flow_tabWidget.setObjectName(_fromUtf8("Flow_tabWidget"))
		self.Flow_tab_1 = QtGui.QWidget()
		self.Flow_tab_1.setObjectName(_fromUtf8("Flow_tab_1"))

		Flow_tabWidget.addTab(self.Flow_tab_1, _fromUtf8(""))
		self.Flow_tab_2 = QtGui.QWidget()
		self.Flow_tab_2.setObjectName(_fromUtf8("Flow_tab_2"))

		Flow_tabWidget.addTab(self.Flow_tab_2, _fromUtf8(""))
		self.Flow_tab_3 = QtGui.QWidget()
		self.Flow_tab_3.setObjectName(_fromUtf8("Flow_tab_3"))

	##--Instance button--##
		self.OKButton_Flow = QtGui.QPushButton(self.Flow_tab_1)
		self.OKButton_Flow.setGeometry(QtCore.QRect(270, 213, 131, 23))
		self.OKButton_Flow.setObjectName(_fromUtf8("OKButton_Flow"))
		self.OKButton_Flow.clicked.connect(self.confirm_data)

	##----Instantiation of elements for inputs----##
		#Selector type flow
		Flow_tabWidget.addTab(self.Flow_tab_3, _fromUtf8(""))
		comBox_Type_Flow = QtGui.QComboBox(Dialog)
		comBox_Type_Flow.setGeometry(QtCore.QRect(10, 10, 421, 22))
		comBox_Type_Flow.setObjectName(_fromUtf8("comBox_Type_Flow"))
		comBox_Type_Flow.addItem("--Tipo de flujo--")
		comBox_Type_Flow.addItem("Jugo")
		comBox_Type_Flow.addItem("Vapor")
		comBox_Type_Flow.addItem("Agua")	

		comBox_Type_Flow.activated.connect(self.selection_TypeFlow)

		#Group box
		self.Inputs_GrBx = QtGui.QGroupBox(self.Flow_tab_1)
		self.Inputs_GrBx.setGeometry(QtCore.QRect(10, 11, 401, 191))
		self.Inputs_GrBx.setTitle(_fromUtf8(""))
		self.Inputs_GrBx.setObjectName(_fromUtf8("Inputs_GrBx"))
		#Flow
		self.label_Mas_Flow = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Mas_Flow.setGeometry(QtCore.QRect(12, 18, 101, 16))
		self.label_Mas_Flow.setObjectName(_fromUtf8("label_Mas_Flow"))
		Flow = QtGui.QLineEdit(self.Inputs_GrBx)
		Flow.setGeometry(QtCore.QRect(142, 15, 61, 20))
		Flow.setObjectName(_fromUtf8("Flow"))
		Vali.NumValidator(Flow)
		#Brix
		self.label_Brix = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Brix.setGeometry(QtCore.QRect(12, 47, 81, 16))
		self.label_Brix.setObjectName(_fromUtf8("label_Brix"))
		Brix = QtGui.QLineEdit(self.Inputs_GrBx)
		Brix.setGeometry(QtCore.QRect(142, 44, 61, 20))
		Brix.setObjectName(_fromUtf8("Brix"))
		Vali.NumValidator(Brix)
		#Insoluble Solids
		self.label_Insoluble_Solids = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Insoluble_Solids.setGeometry(QtCore.QRect(12, 75, 131, 16))
		self.label_Insoluble_Solids.setObjectName(_fromUtf8("label_Insoluble_Solids"))
		Insoluble_Solids = QtGui.QLineEdit(self.Inputs_GrBx)
		Insoluble_Solids.setGeometry(QtCore.QRect(142, 72, 61, 20))
		Insoluble_Solids.setObjectName(_fromUtf8("Insoluble_Solids"))
		Vali.NumValidator(Insoluble_Solids)
		#Purity
		self.label_Purity = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Purity.setGeometry(QtCore.QRect(230, 18, 101, 16))
		self.label_Purity.setObjectName(_fromUtf8("label_Purity"))
		Purity = QtGui.QLineEdit(self.Inputs_GrBx)
		Purity.setGeometry(QtCore.QRect(325, 15, 61, 20))
		Purity.setObjectName(_fromUtf8("Purity"))
		Vali.NumValidator(Purity)
		#Temperature		
		self.label_Temp = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Temp.setGeometry(QtCore.QRect(230, 47, 111, 16))
		self.label_Temp.setObjectName(_fromUtf8("label_Temp"))
		Temp = QtGui.QLineEdit(self.Inputs_GrBx)
		Temp.setGeometry(QtCore.QRect(326, 44, 61, 20))
		Temp.setObjectName(_fromUtf8("Temp"))
		Vali.NumValidator(Temp)
		#pH
		self.label_pH = QtGui.QLabel(self.Inputs_GrBx)
		self.label_pH.setGeometry(QtCore.QRect(15, 106, 46, 13))
		self.label_pH.setObjectName(_fromUtf8("label_pH"))
		pH = QtGui.QLineEdit(self.Inputs_GrBx)
		pH.setGeometry(QtCore.QRect(142, 102, 61, 20))
		pH.setObjectName(_fromUtf8("pH"))
		Vali.NumValidator(pH)
		#Pressure		
		self.label_Pressure = QtGui.QLabel(self.Inputs_GrBx)
		self.label_Pressure.setGeometry(QtCore.QRect(232, 76, 71, 16))
		self.label_Pressure.setObjectName(_fromUtf8("label_Pressure"))
		Pressure = QtGui.QLineEdit(self.Inputs_GrBx)
		Pressure.setGeometry(QtCore.QRect(326, 73, 61, 20))
		Pressure.setObjectName(_fromUtf8("Pressure"))
		Vali.NumValidator(Pressure)
	#CheckBox to select vapor type
		label_vapor_type = QtGui.QLabel(self.Inputs_GrBx)
		label_vapor_type.setGeometry(QtCore.QRect(253, 125, 81, 20))
		label_vapor_type.setObjectName(_fromUtf8("label_vapor_type"))
		checkBox_Saturated_vapor = QtGui.QCheckBox(self.Inputs_GrBx)
		checkBox_Saturated_vapor.setGeometry(QtCore.QRect(270, 148, 101, 17))
		checkBox_Saturated_vapor.setObjectName(_fromUtf8("checkBox_Saturated_vapor"))
		checkBox_Overheated_vapor = QtGui.QCheckBox(self.Inputs_GrBx)
		checkBox_Overheated_vapor.setGeometry(QtCore.QRect(270, 169, 131, 17))
		checkBox_Overheated_vapor.setObjectName(_fromUtf8("checkBox_Overheated_vapor"))
	
	##----Instantiation of elements for inputs----##
		#GroupBox		
		self.Outputs_GrBx = QtGui.QGroupBox(self.Flow_tab_2)
		self.Outputs_GrBx.setGeometry(QtCore.QRect(8, 14, 401, 141))
		self.Outputs_GrBx.setTitle(_fromUtf8(""))
		self.Outputs_GrBx.setObjectName(_fromUtf8("Outputs_GrBx"))
		#Specific Heat
		self.label_Specific_Heat = QtGui.QLabel(self.Outputs_GrBx)
		self.label_Specific_Heat.setGeometry(QtCore.QRect(12, 18, 101, 31))
		self.label_Specific_Heat.setObjectName(_fromUtf8("label_Specific_Heat"))
		Specific_Heat = QtGui.QLineEdit(self.Outputs_GrBx)
		Specific_Heat.setGeometry(QtCore.QRect(142, 24, 61, 20))
		Specific_Heat.setReadOnly(True)
		Specific_Heat.setObjectName(_fromUtf8("Specific_Heat"))
		#Density
		self.label_Density = QtGui.QLabel(self.Outputs_GrBx)
		self.label_Density.setGeometry(QtCore.QRect(12, 55, 91, 16))
		self.label_Density.setObjectName(_fromUtf8("label_Density"))
		Density = QtGui.QLineEdit(self.Outputs_GrBx)
		Density.setGeometry(QtCore.QRect(142, 54, 61, 20))
		Density.setReadOnly(True)
		Density.setObjectName(_fromUtf8("Density"))
		#Enthalpy
		self.label_Enthalpy = QtGui.QLabel(self.Outputs_GrBx)
		self.label_Enthalpy.setGeometry(QtCore.QRect(12, 83, 131, 16))
		self.label_Enthalpy.setObjectName(_fromUtf8("label_Enthalpy"))
		Enthalpy = QtGui.QLineEdit(self.Outputs_GrBx)
		Enthalpy.setGeometry(QtCore.QRect(142, 82, 61, 20))
		Enthalpy.setReadOnly(True)
		Enthalpy.setObjectName(_fromUtf8("Enthalpy"))
		#Viscosity		
		self.label_Viscosity = QtGui.QLabel(self.Outputs_GrBx)
		self.label_Viscosity.setGeometry(QtCore.QRect(230, 19, 101, 31))
		self.label_Viscosity.setObjectName(_fromUtf8("label_Viscosity"))
		Viscosity = QtGui.QLineEdit(self.Outputs_GrBx)
		Viscosity.setGeometry(QtCore.QRect(327, 26, 61, 20))
		Viscosity.setReadOnly(True)
		Viscosity.setObjectName(_fromUtf8("Viscosity"))
		#Thermal conductivity
		self.label_Therma_Conductivity = QtGui.QLabel(self.Outputs_GrBx)
		self.label_Therma_Conductivity.setGeometry(QtCore.QRect(230, 61, 111, 31))
		self.label_Therma_Conductivity.setObjectName(_fromUtf8("label_Therma_Conductivity"))
		Conductivity = QtGui.QLineEdit(self.Outputs_GrBx)
		Conductivity.setGeometry(QtCore.QRect(327, 67, 61, 20))
		Conductivity.setReadOnly(True)
		Conductivity.setObjectName(_fromUtf8("Conductivity"))
		#Evaporation enthalpy
		label_Evaporation_Enthalpy = QtGui.QLabel(self.Outputs_GrBx)
		label_Evaporation_Enthalpy.setGeometry(QtCore.QRect(230, 101, 111, 31))
		label_Evaporation_Enthalpy.setObjectName(_fromUtf8("label_Evaporation_Enthalpy"))
		label_Evaporation_Enthalpy.hide()
		Evaporation_Enthalpy = QtGui.QLineEdit(self.Outputs_GrBx)
		Evaporation_Enthalpy.setGeometry(QtCore.QRect(327, 111, 61, 20))
		Evaporation_Enthalpy.setReadOnly(True)
		Evaporation_Enthalpy.setObjectName(_fromUtf8("Evaporation_Enthalpy"))
		Evaporation_Enthalpy.hide()

	## -- Variable inputs -- ##
		#Selector
		comBox_VariableInput = QtGui.QComboBox(self.Flow_tab_3)
		comBox_VariableInput.setGeometry(QtCore.QRect(18, 15, 151, 22))
		comBox_VariableInput.setObjectName(_fromUtf8("comBox_VariableInput"))
		comBox_VariableInput.activated.connect(self.selection_VariableInput)
		#Spinbox
		SpinBox_VariableInput = QtGui.QDoubleSpinBox(self.Flow_tab_3)
		SpinBox_VariableInput.setGeometry(QtCore.QRect(181, 15, 72, 22))
		SpinBox_VariableInput.setObjectName(_fromUtf8("SpinBox_VariableInput"))
		SpinBox_VariableInput.setRange(0, 1000000);
		
		self.retranslateUi(Dialog)
		Flow_tabWidget.setCurrentIndex(0)
		Flow_tabWidget.currentChanged.connect(self.TabChange)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		Update_window()

		if update==1:
			SpinBox_VariableInput.valueChanged.connect(self.variable_change)

## -- Function that identify changes in SpinBox and update DB -- ##
	def variable_change(self):
		global VariableInput
		input_heat = open('Blocks_data.txt', 'r+')
		data=input_heat.readlines()
		input_heat.close()
		Kj=False
		valor=SpinBox_VariableInput.value()
		if(VariableInput==(_translate("Dialog", "Flujo másico [t/h]", None))):
			Flow.setText(str(valor))
		elif(VariableInput==("Brix [%]")):
			Brix.setText(str(valor))
		elif(VariableInput==(_translate("Dialog", "Sólidos insolubles [%]", None))):
			Insoluble_Solids.setText(str(valor))
		elif(VariableInput==(_translate("Dialog", "Temperatura [°C]", None))):
			Temp.setText(str(valor))
		elif(VariableInput==("Pureza [%]")):
			Purity.setText(str(valor))
		elif(VariableInput==(_translate("Dialog", "Presión [kPa]", None))):
			Pressure.setText(str(valor))
		elif(VariableInput==("pH")):
			pH.setText(str(valor))
		if len(data)>0:
			for i in data:
				info=(i.strip()).split("\t")
				if len(info)>1:
					flag=info[0]

					## -- If the change is realized in a vapor flow -- ##
					if flag==("Fv"+str(num_window)):
						dato1=str(i.strip())
						Kj=True
						if saturado==1:
						##Get inputs
							Pvin=(float(Pressure.text()))*1000.0
						##Update steam flow info 
							Tvin,pv,uv,Hv,Yv,Cpv,Hvw=flow_data.update_vapor(Pvin)
						##Set data in text field
							Temp.setText(str(round(Tvin,3)))
							Density.setText(str(round(pv,3)))
							Viscosity.setText(str("{:.3E}".format(Decimal(uv))))
							Enthalpy.setText(str("{:.3E}".format(Decimal(Hv))))
							Conductivity.setText(str(round(Yv,3)))
							Specific_Heat.setText(str("{:.3E}".format(Decimal(Cpv))))
							Evaporation_Enthalpy.setText(str("{:.3E}".format(Decimal(Hvw))))
						##Prepare frame to data base
							dato2=(flag+"\t"+str(Pvin)+"\t"+Flow.text()+"\t"+str(Tvin)+"\t"+str(Cpv)+"\t"+str(pv)+"\t"+str(uv)+"\t"+str(Hv)+"\t"+str(Hvw)+"\t"+str(Yv)+"\t"+"1")
						else:
							pass

					## -- If the change is realized in a juice flow -- ##
					elif flag==("Fj"+str(num_window)):
						dato1=str(i.strip())
						Kj=True
					##Get inputs
						Mjin=float(Flow.text())
						Bjin=float(Brix.text())/100.0
						SolIn=float(Insoluble_Solids.text())/100.0
						Tjin=float(Temp.text())
						Zjin=float(Purity.text())/100.0
						pHj=float(pH.text())
						Pj=(float(Pressure.text()))*1000.0
					##Update juice flow info 
						Cpj,pj,uj,Hj,Yj=flow_data.update_juice(Bjin,Zjin,Tjin)		
					##Set data in text field	
						Specific_Heat.setText(str("{:.3E}".format(Decimal(Cpj))))
						Density.setText(str(round(pj,3)))
						Viscosity.setText(str("{:.3E}".format(Decimal(uj))))
						Enthalpy.setText(str("{:.3E}".format(Decimal(Hj))))
						Conductivity.setText(str(round(Yj,3)))
					##Prepare frame to data base
						dato2=(flag+"\t"+str(Mjin)+"\t"+str(Tjin)+"\t"+str(Bjin)+"\t"+str(Zjin)+"\t"+str(SolIn)+"\t"+str(pHj)+"\t"+str(Pj)+"\t"+str(Cpj)+"\t"+str(pj)+"\t"+str(uj)+"\t"+str(Hj)+"\t"+str(Yj))
						# dato2=(flag+"\t"+str(Mjin)+"\t"+str(Bjin)+"\t"+str(Zjin)+"\t"+str(Tjin)+"\t"+str(SolIn)+"\t"+str(pHj)+"\t"+str(Pj)+"\t"
						# 	+str(Cpj)+"\t"+str(pj)+"\t"+str(uj)+"\t"+str(Hj)+"\t"+str(Yj))

					## -- If the change is realized in a water flow -- ##
					elif flag==("Fw"+str(num_window)):
						dato1=str(i.strip())
						Kj=True
					##Get inputs
						Mw=float(Flow.text())
						Tw=float(Temp.text())
						pHw=float(pH.text())
						Pw=(float(Pressure.text()))*1000.0
					##Update water flow info 
						pw,Hw=flow_data.update_water(Tw)
					##Set data in text field
						Density.setText(str(round(pw,3)))
						Enthalpy.setText(str("{:.3E}".format(Decimal(Hw))))
					##Prepare frame to data base
						dato2=flag+"\t"+str(Mw)+"\t"+str(Tw)+"\t"+str(pHw)+"\t"+str(Pw)+"\t"+str(pw)+"\t"+str(Hw)
		if Kj==True:
			##-- Overwrite flow data with changes --##
			replace("Blocks_data.txt",dato1,dato2)

## -- Function to update text field with Spinbox value when Tab change -- ##	
	def TabChange(self):
		global VariableInput
		CurrentTab=Flow_tabWidget.currentIndex()
		if CurrentTab==2:
			if(VariableInput==(_translate("Dialog", "Flujo másico [t/h]", None))):
				if len(Flow.text())>0:
					SpinBox_VariableInput.setValue(float(Flow.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==("Brix [%]")):
				if len(Brix.text())>0:
					SpinBox_VariableInput.setValue(float(Brix.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==(_translate("Dialog", "Sólidos insolubles [%]", None))):
				if len(Insoluble_Solids.text())>0:
					SpinBox_VariableInput.setValue(float(Insoluble_Solids.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==(_translate("Dialog", "Temperatura [°C]", None))):
				if len(Temp.text())>0:
					SpinBox_VariableInput.setValue(float(Temp.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==("Pureza [%]")):
				if len(Purity.text())>0:
					SpinBox_VariableInput.setValue(float(Purity.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==(_translate("Dialog", "Presión [kPa]", None))):
				if len(Pressure.text())>0:
					SpinBox_VariableInput.setValue(float(Pressure.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)
			elif(VariableInput==("pH")):
				if len(pH.text())>0:
					SpinBox_VariableInput.setValue(float(pH.text()))
				else:
					SpinBox_VariableInput.setValue(0.0)

## -- Function to update text field with Spinbox value when variable input is selected -- ##	
	def selection_VariableInput(self):
		global VariableInput
		VariableInput=comBox_VariableInput.currentText()
		if(VariableInput==(_translate("Dialog", "Flujo másico [t/h]", None))):
			if len(Flow.text())>0:
				SpinBox_VariableInput.setValue(float(Flow.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==("Brix [%]")):
			if len(Brix.text())>0:
				SpinBox_VariableInput.setValue(float(Brix.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==(_translate("Dialog", "Sólidos insolubles [%]", None))):
			if len(Insoluble_Solids.text())>0:
				SpinBox_VariableInput.setValue(float(Insoluble_Solids.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==(_translate("Dialog", "Temperatura [°C]", None))):
			if len(Temp.text())>0:
				SpinBox_VariableInput.setValue(float(Temp.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==("Pureza [%]")):
			if len(Purity.text())>0:
				SpinBox_VariableInput.setValue(float(Purity.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==(_translate("Dialog", "Presión [kPa]", None))):
			if len(Pressure.text())>0:
				SpinBox_VariableInput.setValue(float(Pressure.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)
		elif(VariableInput==("pH")):
			if len(pH.text())>0:
				SpinBox_VariableInput.setValue(float(pH.text()))
			else:
				SpinBox_VariableInput.setValue(0.0)

## -- Function of conditionals for type flow selector -- ##		
	def selection_TypeFlow(self):
		global Type_flow_selec
		#print Type_flow_selec
		comBox_VariableInput.clear()
		Type_flow_selec=comBox_Type_Flow.currentText()
		if Type_flow_selec=="Vapor":
			Brix.setDisabled(1)
			pH.setDisabled(1)
			Flow.setDisabled(1)
			Purity.setDisabled(1)
			Evaporation_Enthalpy.show()
			label_Evaporation_Enthalpy.show()
			Insoluble_Solids.setDisabled(1)
			Temp.setDisabled(1)
			checkBox_Saturated_vapor.setChecked(True)
			label_vapor_type.show()
			checkBox_Saturated_vapor.show()
			checkBox_Overheated_vapor.show()
			##
			if saturado==1:
				comBox_VariableInput.clear()
				comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
			else:
				comBox_VariableInput.clear()
				comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))
		elif Type_flow_selec=="Jugo":
			Brix.setEnabled(1)
			Purity.setEnabled(1)
			Insoluble_Solids.setEnabled(1)
			Flow.setEnabled(1)
			Temp.setEnabled(1)
			pH.setEnabled(1)
			Pressure.setEnabled(1)
			Evaporation_Enthalpy.hide()
			label_Evaporation_Enthalpy.hide()
			label_vapor_type.hide()
			checkBox_Saturated_vapor.hide()
			checkBox_Overheated_vapor.hide()
			##
			comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
			comBox_VariableInput.addItem("Brix [%]")
			comBox_VariableInput.addItem(_translate("Dialog", "Sólidos insolubles [%]", None))
			comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))	
			comBox_VariableInput.addItem("Pureza [%]")
			comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
			comBox_VariableInput.addItem("pH")
		elif Type_flow_selec=="Agua":
			Brix.setDisabled(1)
			Purity.setDisabled(1)
			Flow.setEnabled(1)
			pH.setEnabled(1)
			Insoluble_Solids.setDisabled(1)
			Temp.setEnabled(1)
			Pressure.setEnabled(1)
			Evaporation_Enthalpy.hide()
			label_Evaporation_Enthalpy.hide()
			label_vapor_type.hide()
			checkBox_Saturated_vapor.hide()
			checkBox_Overheated_vapor.hide()
			##
			comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
			comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))		
			comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
			comBox_VariableInput.addItem("pH")

## -- Function of conditionals for type vapor checkboxes -- ##
	def selection_TypeVapor(self):
		global saturado
		if Type_flow_selec=="Vapor":
			if checkBox_Saturated_vapor.isChecked():
				saturado=1
				Temp.setDisabled(1)
				comBox_VariableInput.clear()
				comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))			
			elif checkBox_Overheated_vapor.isChecked():
				Temp.setEnabled(1)
				comBox_VariableInput.clear()
				comBox_VariableInput.addItem(_translate("Dialog", "Flujo másico [t/h]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Presión [kPa]", None))
				comBox_VariableInput.addItem(_translate("Dialog", "Temperatura [°C]", None))				
				saturado=0
		else:
			self.Pressure.setEnabled(1)

## -- Complete label texts -- ##		
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Datos "+str(nameDialog), None))
		self.label_Mas_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_Brix.setText(_translate("Dialog", "Brix [%]", None))
		self.label_Insoluble_Solids.setText(_translate("Dialog", "Sólidos insolubles [%]", None))
		self.label_Purity.setText(_translate("Dialog", "Pureza [%]", None))
		self.label_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_pH.setText(_translate("Dialog", "pH", None))
		self.label_Pressure.setText(_translate("Dialog", "Presión [kPa]", None))
		
		self.mood_button_group = QtGui.QButtonGroup()
		checkBox_Saturated_vapor.setText(_translate("Dialog", "Vapor saturado", None))
		checkBox_Saturated_vapor.stateChanged.connect(self.selection_TypeVapor)
		self.mood_button_group.addButton(checkBox_Saturated_vapor)
		checkBox_Overheated_vapor.setText(_translate("Dialog", "Vapor sobre-calentado", None))
		checkBox_Overheated_vapor.stateChanged.connect(self.selection_TypeVapor)
		self.mood_button_group.addButton(checkBox_Overheated_vapor)
		label_vapor_type.setText(_translate("Dialog", "-Tipo de vapor-", None))
		self.OKButton_Flow.setText(_translate("Dialog", "Aceptar", None))
		Flow_tabWidget.setTabText(Flow_tabWidget.indexOf(self.Flow_tab_1), _translate("Dialog", "Datos de entrada", None))
		self.label_Specific_Heat.setText(_translate("Dialog", "Calor específico \n"
		"[J/kg °K]", None))
		self.label_Density.setText(_translate("Dialog", "Densidad [kg/m3]", None))
		self.label_Enthalpy.setText(_translate("Dialog", "Entalpía [J/kg]", None))
		self.label_Viscosity.setText(_translate("Dialog", "Viscosidad \n"
		"dinámica [Pa s]", None))
		self.label_Therma_Conductivity.setText(_translate("Dialog", "Conductividad \n"
		"térmica [W/ m °K]", None))
		label_Evaporation_Enthalpy.setText(_translate("Dialog", "Entalpía de \nevaporación [J/kg]", None))
		Flow_tabWidget.setTabText(Flow_tabWidget.indexOf(self.Flow_tab_2), _translate("Dialog", "Datos calculados", None))
		Flow_tabWidget.setTabText(Flow_tabWidget.indexOf(self.Flow_tab_3), _translate("Dialog", "Entradas dinámicas", None))

		
		label_vapor_type.hide()
		checkBox_Saturated_vapor.hide()
		checkBox_Overheated_vapor.hide()

## -- Manual execution of window -- ##
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QDialog()
	ui = Ui_Dialog()
	ui.setupUi("Flujo",Dialog)
	Dialog.show()
	sys.exit(app.exec_())

