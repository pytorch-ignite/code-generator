from ignite.engine.events import EventEnum


class TrainEvents(EventEnum):
    """Additional Training Events. includes

    - BACKWARD_COMPLETED : trigger after calling loss.backward()
    - OPTIM_STEP_COMPLETED : trigger after calling optimizer.step()
    """

    BACKWARD_COMPLETED = "backward_completed"
    OPTIM_STEP_COMPLETED = "optim_step_completed"


# define events and attribute mapping
# so that we can trigger them with custom filter function
train_events_to_attr = {
    TrainEvents.BACKWARD_COMPLETED: "backward_completed",
    TrainEvents.OPTIM_STEP_COMPLETED: "optim_step_completed",
}

# Any custom events can go below
# fire them in process_function of the respective engine and
# register them with the respective engine
