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
  name = "microplot_test",
  srcs = [
    "microplot.py",
    "microplot_test.py",
  ],
  main = "microplot_test.py",
  imports = [
    "PyYaml",
  ],
  data = glob([
    "mako_files/*",
    "example_protocol.yml",
    "test.yml"
  ]),
)
