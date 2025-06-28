import pytest
from unittest.mock import MagicMock
from source.school import Classroom, Teacher, Student, TooManyStudents


@pytest.fixture
def default_students():
    """Return a list of Student objects representing Hogwarts students."""
    return [Student(name) for name in [
        "Hermione Granger", "Ron Weasley", "Neville Longbottom", "Luna Lovegood", "Dean Thomas",
        "Seamus Finnigan", "Ginny Weasley", "Lavender Brown", "Parvati Patil", "Padma Patil"
    ]]


@pytest.fixture
def potions_teacher():
    """Return a Potions Master (initial teacher)."""
    return Teacher("Severus Snape")


@pytest.fixture
def hogwarts_classroom(potions_teacher, default_students):
    """Return a Hogwarts Classroom instance."""
    return Classroom(teacher=potions_teacher, students=default_students, course_title="Potions")


def test_add_student_success(hogwarts_classroom):
    new_student = Student("Harry Potter")
    hogwarts_classroom.add_student(new_student)
    assert new_student in hogwarts_classroom.students


def test_add_student_too_many(hogwarts_classroom):
    hogwarts_classroom.add_student(Student("Draco Malfoy"))  # 11th student
    with pytest.raises(TooManyStudents):
        hogwarts_classroom.add_student(Student("Crabbe"))  # 12th student


@pytest.mark.parametrize("name_to_remove,expected_names", [
    ("Ron Weasley", ["Hermione Granger", "Neville Longbottom", "Luna Lovegood", "Dean Thomas",
                     "Seamus Finnigan", "Ginny Weasley", "Lavender Brown", "Parvati Patil",
                     "Padma Patil"]),
    ("Hermione Granger", ["Ron Weasley", "Neville Longbottom", "Luna Lovegood", "Dean Thomas",
                          "Seamus Finnigan", "Ginny Weasley", "Lavender Brown", "Parvati Patil",
                          "Padma Patil"]),
])
def test_remove_student(name_to_remove, expected_names, hogwarts_classroom):
    hogwarts_classroom.remove_student(name_to_remove)
    remaining_names = [s.name for s in hogwarts_classroom.students]
    assert sorted(remaining_names) == sorted(expected_names)


def test_change_teacher(hogwarts_classroom):
    new_teacher = Teacher("Horace Slughorn")
    hogwarts_classroom.change_teacher(new_teacher)
    assert hogwarts_classroom.teacher.name == "Horace Slughorn"


def test_remove_nonexistent_student_does_nothing(hogwarts_classroom):
    initial_count = len(hogwarts_classroom.students)
    hogwarts_classroom.remove_student("Tom Riddle")  # Not in the class
    assert len(hogwarts_classroom.students) == initial_count


def test_add_student_mocked_list(potions_teacher):
    # Use MagicMock to monitor method calls on the list
    students = MagicMock()
    students.__len__.return_value = 5
    classroom = Classroom(potions_teacher, students, "Defense Against the Dark Arts")

    new_student = Student("Harry Potter")
    classroom.add_student(new_student)

    students.append.assert_called_once_with(new_student)
