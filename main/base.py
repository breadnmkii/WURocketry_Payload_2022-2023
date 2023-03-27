from Radio import telemetry

# Telemetry
def telemetryRoutine():
    telemetry.recieveData()


def test_base():
    while (True):
        telemetryRoutine()


if __name__ == '__main__':
    test_base()
