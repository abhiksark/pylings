assert [member.name for member in Status] == ["TODO", "DOING", "DONE"]
assert [member.value for member in Status] == [1, 2, 3]
print("enums2 ok")
