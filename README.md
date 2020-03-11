# MicroPlot
### ![Python application](https://github.com/theDrsh/MicroPlot/workflows/Python%20application/badge.svg)

## Graphing tool:
 - Use graphing.yml to define what signals to graph.
 - Use QtDesigner to edit the .ui file to create buttons and texts boxes as needed to control your embedded device.

 ## Database module:
 - Record {Key : Value} pairs to a MySQL database.
 - Database can be local or tied to a remote database(given IP/Port)

 ## Parser Module:
 - The meat of microplot, it parses commands from your embedded project.
 - Types of protocols supported:
    - ASCII Serial(UART/RS-232)
 - Future:
    - I2C(Raspberry PI only, support for aardvark?)
    - SPI(same as I2C)
    - Nanopb over Serial?
    - USB bulk transfer?
