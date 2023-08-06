import asyncio

from nio import InviteMemberEvent

import hopfenmatrix.run
import hopfenmatrix.config
import hopfenmatrix.client
import hopfenmatrix.callbacks


async def test(client, config):
    while True:
        try:
            print("test")
        except Exception:
            pass


async def test_send(client, config):
    while True:
        await asyncio.sleep(1)
        print("Function got called")
        try:
            content = {
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": "Test",
                "formatted_body": "<b>Test</b>"
            }
            print(client.rooms)
            for room in client.rooms:
                print(f"room: {room}")
                await client.room_send(
                    room, "m.room.message", content, ignore_unverified_devices=True,
                )
        except Exception as err:
            print(err)


async def main():
    config = TestAppConfig.from_json("config.json")

    client = hopfenmatrix.client.new_async_client(config)
    client.add_event_callback(
        hopfenmatrix.callbacks.apply_filter(
            hopfenmatrix.callbacks.auto_join(client),
            hopfenmatrix.callbacks.allowed_users(["@izomikron:matrix.hopfenspace.org"])),
        InviteMemberEvent)

    callbacks = [test_send(client, config)]

    await hopfenmatrix.run.run(client, config, callbacks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
