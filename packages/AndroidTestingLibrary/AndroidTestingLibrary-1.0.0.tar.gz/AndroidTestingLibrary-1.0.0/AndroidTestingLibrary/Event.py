"""
Event.py

Contains the Event class, which is the superclass for all events. It should not be instantiable by
the user, so it is in the _private directory.
"""

# superclass to make sure every subclass has the get_cmd_str() and __str__() methods
class Event:

    cmd_str: str = None

    def get_cmd_str(self) -> str:
        return self.cmd_str
    
    def __str__(self) -> str:
        pass
