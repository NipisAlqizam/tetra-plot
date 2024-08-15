import models


def get_measurement_adding_text(
    x_title: str, y_title: str, measurements: list[models.Measurement] | None = None
) -> str:
    begining = f"Вводите данные через пробел в формате <{x_title}> <{y_title}> <комментарий (необязательно)>.\n\nСейчас введено:\n"
    empty = "<ничего>"
    if measurements is None or len(measurements) == 0:
        return begining + empty
    measurement_strings = [
        "\t".join((str(m.x), str(m.y), m.comment)) for m in measurements
    ]
    return begining + "\n".join(measurement_strings)
