from tracardi.service.storage.factory import storage_manager
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result

from tracardi_inject_event.model.configuration import Configuration


def validate(config: dict):
    return Configuration(**config)


class InjectEvent(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):
        event = await storage_manager("event").load(self.config.event_id)
        if event is None:
            self.console.warning("Event id `{}` does not exist.".format(self.config.event_id))
        return Result(port="payload", value=event)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_inject_event.plugin',
            className='InjectEvent',
            inputs=["payload"],
            outputs=['payload'],
            version='0.3',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "event_id": None
            },
            form=Form(groups=[
                FormGroup(
                    name="Event id",
                    fields=[
                        FormField(
                            id="event_id",
                            name="Event id",
                            description="Type event id you would like to add to payload.",
                            component=FormComponent(type="text", props={"label": "Event id"})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='Inject event',
            desc='This node will inject event of given id into payload',
            type='flowNode',
            width=300,
            height=100,
            icon='json',
            group=["Input/Output"]
        )
    )
