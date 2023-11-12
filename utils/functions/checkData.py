def is_there_events_file_uploaded(objects):
    for obj in objects:
        if obj.is_event_file:
            return True
    return False


def is_there_devices_file_uploaded(objects):
    for obj in objects:
        if not obj.is_event_file:
            return True
    return False
