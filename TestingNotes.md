# Testing Notes for Temperature Bench

Testing done on Match 23, 2022.

## LC709203

- **WILL NOT WORK without a battery connected**
- MultiMeter measures a steady 3.606V; BMS measures about 3.584V

## MAX17043

- Will initialize without a battery, but will give high readings
- NEEDS Wire() initialized before it will work, but keep in mind initializing Wire multiple times can cause issues

## INA219

- Works with or without a load
- DO NOT connect battery straight to it. duh
- ONLY measures current (I)

## 