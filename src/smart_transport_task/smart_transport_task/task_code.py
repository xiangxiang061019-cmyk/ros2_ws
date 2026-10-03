def parse_task_code(raw_code):
    """Parse four three-digit groups from the competition task code."""
    groups = raw_code.strip().split('+')
    if len(groups) != 4 or any(len(group) != 3 or not group.isdigit() for group in groups):
        raise ValueError('expected four three-digit groups separated by +')

    values = [[int(char) for char in group] for group in groups]
    if any(value < 1 or value > 6 for group in values for value in group):
        raise ValueError('task colors and ring numbers must be in the range 1..6')

    return {
        'first_colors': values[0],
        'first_places': values[1],
        'second_colors': values[2],
        'second_places': values[3],
    }
