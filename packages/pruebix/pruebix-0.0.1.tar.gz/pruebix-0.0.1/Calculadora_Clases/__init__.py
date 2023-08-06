from pathlib import Path
import os
import subprocess
import string
import re


path = str(Path().absolute())
executable = "\dist\MainCalculatorConsole.exe"
subprocess.call([path + executable])


#subprocess.call(["C:\Users\Ari Bautista\Videos\Calculadora_Clases\dist\MainCalculatorConsole.exe"])


