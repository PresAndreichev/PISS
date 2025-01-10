class RoomEvent:
    def __init__(self, host, topic, room, day, start_time, end_time):
        self.__host = host
        self.__topic = topic
        self.__room = room
        self.__day = day
        self.__start_time = start_time
        self.__end_time = end_time

    def __init__(self, room_id):
        self.load_resources_from_db(room_id)

