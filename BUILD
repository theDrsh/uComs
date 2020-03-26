py_binary(
  name = "microplot",
  srcs = [
    "microplot.py",
    "example_main.py",
  ],
  main = "example_main.py",
  data = [
    "example_protocol.yml",
  ],
)

py_test(
  name = "mako_files/microplot_test",
  srcs = [
    "microplot.py",
    "example_main.py",
    "microplot_test.py",
  ],
  main = "microplot_test.py",
  imports = [
    "PyYaml",
  ],
  data = [
    "example_protocol.yml",
    "test.yml",
  ],
)
