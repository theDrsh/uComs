py_binary(
  name = "ucoms",
  srcs = [
    "ucoms.py",
    "example_main.py",
  ],
  main = "example_main.py",
  data = [
    "example_protocol.yml",
  ],
)


py_test(
  name = "ucoms_test",
  srcs = [
    "ucoms.py",
    "ucoms_test.py",
  ],
  main = "ucoms_test.py",
  imports = [
    "PyYaml",
  ],
  data = glob([
    "mako_files/*",
    "example_protocol.yml",
    "test.yml"
  ]),
)
