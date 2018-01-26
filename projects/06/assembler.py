#!/usr/bin/python

from sys import argv
import re

script, addr = argv

def convert(line):
	#if a instruction
	if line.startswith("@"):
		value = re.search('\d+',line).group()
		result="{0:016b}".format(int(value))
	else:
		result = convertC(line)
	return result

def convertC(line):
	(dest, comp, jmp) = re.search('(?:(.*)=)?([^=;]+)(?:;(.*))?', line).groups();
	if dest == None:
		dest = ''
	if jmp == None:
		jmp = ''

	d1 = '0'
	d2 = '0'
	d3 = '0'
	if dest.find('A') != -1:
		d1 = '1'
	if dest.find('D') != -1:
		d2 = '1'
	if dest.find('M') != -1:
		d3 = '1'
	destination = d1 + d2 + d3
	a = '0'
	if comp.find('M') != -1:
		a='1'
	comp = comp.replace('M','A')
	computationDict = {'0': '101010', '1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}
	computation = a + computationDict[comp]
	jumpDict = {'JGT': '001', 'JEQ': '010', 'JGE': '011','JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111','':'000'}
	jump = jumpDict[jmp]
	result = '111' + computation + destination + jump
	return result

# SP     0   0x0000
# LCL     1   0x0001
# ARG     2   0x0002
# THIS     3   0x0003
# THAT         4   0x0004
# R0-R15 0-15   0x0000-f
# SCREEN 16384   0x4000
# KBD 24576   0x6000


def makeSymbol(data,defaults):
	symbolTables = defaults
	linenum = 0
	seek = 16
	for line in data:
		if line.startswith('('):
			symbol = line[1:-1]
			value = linenum

			if not symbol in symbolTables:
				symbolTables[symbol] = str(value)
		else:
			linenum += 1

	for line in data:
		if line.startswith('@'):
			symbol = line[1:]
			value = seek
			if not symbol in symbolTables and not symbol.isdigit():
				symbolTables[symbol] = str(value)
				seek += 1

	return symbolTables


def transSymbolFile(file,symbols):
	results = []
	for line in file:
		if not line.startswith('('):
			results.append(transSymbolLine(line,symbols))
	return results

def transSymbolLine(line,symbols):
	if line.startswith("@"):
		value = line[1:]
		if value.isdigit():
			return '@' + value
		else:
			return '@' + symbols[value]
	else:
		return line

def main(script,in_addr):
#preprocessing file - removing empty lines whitespaces as well as 
	out_addr = addr.replace('.asm','.hack')
	data = []
	with open(addr) as f:
		for l in f:
			if l.strip():
				if not l.startswith('//'):
					line = l.split("//")[0].strip()
					data.append(line)
	defaultSymbols = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4','SCREEN': '16384', 'KBD': '24576','R0': '0', 'R1': '1', 'R2':'2', 'R3':'3', 'R4':'4', 'R5':'5','R6':'6', 'R7':'7', 'R8':'8', 'R9':'9', 'R10': '10', 'R11':'11', 'R12':'12', 'R13':'13', 'R14': '14', 'R15':'15' }
	symbols = makeSymbol(data,defaultSymbols)
	# print symbols
	data = transSymbolFile(data,symbols)
	results=[]
	for line in data:
		results.append(convert(line))

	with open(out_addr,'w') as f:
		f.write('\n'.join(results))

main(script,addr)

#convert to machine code
#converting