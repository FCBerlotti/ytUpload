
import pyautogui as pg
import time
import pyperclip
import requests
import subprocess
from datetime import datetime, timedelta, date
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill
from conteudos import conteudos
import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog


startDate = (date.today()).day
print(startDate)
startDate = startDate + 1
print(startDate)