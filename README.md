# uComs
### ![Python application](https://github.com/theDrsh/ucoms/workflows/Python%20application/badge.svg)
## Parser Module:
 - The meat of uComms, it parses commands from your embedded project.
 - Supports protocols which are strings when the uComs.parse() method is called

## FUTURE PLANS:
### Code Generation tools
  - Use the Protocol definitions in the .yml file to generate parser code for microcontroller
  - This will generate a decoder.h and a decoder.cc(or .c if c desired over c++)
  - Command line flag --init will generate a parser.cc file which contains a class which allows you to put init code to initialize hardware interface. It also creates files which you will maintain that define the behavior of the reciever device when it recieves defined commands.

### Graphing tool:
 - Use graphing.yml to define what signals to graph.
 - Use QtDesigner to edit the .ui file to create buttons and texts boxes as needed to control your embedded device.

### Database module:
 - Record {Key : Value} pairs to a MySQL database.
 - Database can be local or tied to a remote database(given IP/Port)

 - Future:
    - I2C(Raspberry PI could host)
    - SPI(same as I2C)

### Ideas:
- Async commands(should have a device pattern with no host)
- Versioning using pickled data with a reserved async
- C/C++ generated host-side decode