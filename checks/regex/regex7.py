assert match is not None, "pattern should match the phone number"
assert area_code == "415", f"area_code should be '415', got {area_code!r}"
m2 = re.search(pattern, "(800) 123-4567")
assert m2 is not None and m2.group(1) == "800", "should also extract '800' from '(800) 123-4567'"
print("regex7 ✓")
