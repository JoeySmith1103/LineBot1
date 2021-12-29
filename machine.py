from fsm import TocMachine
def createMachine ():
    machine = TocMachine(
        states=["user", "state", "fsm", "multiple"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "state",
                "conditions": "is_going_to_state",
            },
            {
                "trigger": "advance",
                "source": "user",
                "dest": "fsm",
                "conditions": "is_going_to_fsm",
            },
            {
                "trigger": "advance",
                "source": "state",
                "dest": "multiple",
                "conditions": "is_going_to_multiple"
            },
            {
                "trigger": "advance",
                "source": "multiple",
                "dest": "state",
                "conditions": "is_going_to_state"
            },
            {"trigger": "go_back", "source": ["state"], "dest": "user"},
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine