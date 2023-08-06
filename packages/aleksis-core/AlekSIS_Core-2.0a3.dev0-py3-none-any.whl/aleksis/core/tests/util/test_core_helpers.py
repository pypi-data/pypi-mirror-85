import re

from aleksis.core.util.core_helpers import path_and_rename


def test_path_and_rename():
    re_base = r"[a-z0-9]+"

    example_1 = "sdjaasjkl.jpg"
    re_example_1 = "files/" + re_base + r"\.jpg"
    re2_example_1 = "images/" + re_base + r"\.jpg"
    assert re.match(re_example_1, path_and_rename(None, example_1))
    assert re.match(re2_example_1, path_and_rename(None, example_1, upload_to="images"))

    example_2 = "sdjaasjkl"
    re_example_2 = "files/" + re_base
    re2_example_2 = "images/" + re_base
    assert re.match(re_example_2, path_and_rename(None, example_2))
    assert re.match(re2_example_2, path_and_rename(None, example_2, upload_to="images"))
