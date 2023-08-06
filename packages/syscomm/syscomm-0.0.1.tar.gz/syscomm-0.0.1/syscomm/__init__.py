import os
import sys
import tkinter
from tkinter import *

class folderhandler:
    def mkdir(folname):
        os.system(f'mkdir {folname}')
        
    def rmdir(folname):
        os.system(f'rmdir {folname}')  
        
class filehandler:
    def startprogram(file):
        os.system(f'start {file}')
        
    def delfile(file):
        os.system(f'del {file}')    
        
    def showfiles():
        os.system('dir')  
        
class batchfile:
    def echo(text):
        os.system(f'echo {text}')
        
    def pause():
        os.system('pause')    
        
    def makeblankbatchfile(name):
        os.system(f'echo @echo off > {name}.bat')
