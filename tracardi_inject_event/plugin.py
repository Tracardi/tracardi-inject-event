from tracardi.service.storage.factory import storage_manager
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_inject_event.model.configuration import Configuration


def validate(config: dict):
    return Configuration(**config)


class InjectEvent(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):
        event = await storage_manager("event").load(self.config.event_id)
        return Result(port="payload", value=event)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_inject_event.plugin',
            className='InjectEvent',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "event_id": None
            }
        ),
        metadata=MetaData(
            name='Inject event',
            desc='This node will inject event of given id into payload',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["General"]
        )
    )
