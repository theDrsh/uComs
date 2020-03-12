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
    
## Code Generation tools
  - Use the Protocol definitions in the .yml file to generate parser code for microcontroller
  - This will generate a decoder.h and a decoder.cc(or .c if c desired over c++)
  - Command line flag --init will generate a parser.cc file which contains a class which allows you to put init code to initialize hardware inteface, and a Parser::ExecuteAction(Command_e) function whose switch-case structure you insert the actions you'd like each command to execute.
