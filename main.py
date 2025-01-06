from project import Project  # type: ignore

p = Project("pylang", "testdata", ".")

p.scan()
p.parse_files()

print(p.dump())
