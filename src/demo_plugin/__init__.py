from api import Action, plugin


def sample_handler(action: Action):
    print(f"Sample handler executed for action: {action.name}")


@plugin(name="DemoPlugin")
def demo_plugin():
    handlers = {
        "sample_action": sample_handler,
    }
    requires = []
    return handlers, requires
