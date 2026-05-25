# Exercise: Dictionaries 9
# I AM NOT DONE
#
# A nested dict is a dict whose values are themselves dicts.
#
# Given `school` below, set:
#   `alice_grade` — Alice's grade (school["students"]["alice"]["grade"])
#   `math_room`   — the room number for math  (school["courses"]["math"]["room"])
#   `num_students` — the total enrollment count (school["meta"]["enrollment"])

school = {
    "students": {
        "alice": {"grade": "A", "age": 20},
        "bob":   {"grade": "B", "age": 22},
    },
    "courses": {
        "math":    {"room": 101, "credits": 3},
        "english": {"room": 205, "credits": 3},
    },
    "meta": {"enrollment": 350, "founded": 1990},
}

alice_grade = ???
math_room = ???
num_students = ???
