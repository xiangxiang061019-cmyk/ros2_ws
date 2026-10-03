from smart_transport_task.task_code import parse_task_code


def test_valid_task_code():
    parsed = parse_task_code('156+123+516+231')
    assert parsed['first_colors'] == [1, 5, 6]
    assert parsed['first_places'] == [1, 2, 3]


def test_invalid_group_count():
    try:
        parse_task_code('156+123')
    except ValueError:
        return
    raise AssertionError('invalid group count should be rejected')


def test_invalid_digit():
    try:
        parse_task_code('157+123+516+231')
    except ValueError:
        return
    raise AssertionError('digit 7 should be rejected')
