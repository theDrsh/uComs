# uComs
### ![Python application](https://github.com/theDrsh/ucoms/workflows/Python%20application/badge.svg) ![gtest](https://github.com/theDrsh/ucoms/workflows/gtest/badge.svg)
## Parser Module:
 - The meat of uComms, it parses commands from your embedded project.
 - Supports protocols which are strings when the uComs.parse() method is called

 # Protocol Description:
 ## Names:
 * **Pattern**: A pattern describes a set of characters/bytes/bits that make up a packet of data sent either from host to device or device to host
 * **Interaction**: An interaction is a set of pattern(s) usually with a host and a device pattern but also could just be one or the other.
 * **Command**: A command implements an Interaction, there can be many commands that are described by an interaction, you can get an analog value(interaction), or you can get analog pin 1's value(command)
 ![Protocol Yml](protocol_yml.png)

## FUTURE PLANS:
    Outline future plans as issues