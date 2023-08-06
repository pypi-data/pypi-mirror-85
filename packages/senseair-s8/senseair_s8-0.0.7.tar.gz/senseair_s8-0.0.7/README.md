# Introduction
Python module for reading CO2 concentration from a Senseair S8 sensor connected to a Raspberry Pi

# Installation
`pip install senseair-s8`

# Usage
```
from senseair_s8 import SenseairS8

senseair_s8 = SenseairS8()    
print(senseair_s8.co2())
```