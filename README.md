# FastNetMon API - Python Client

Interact with FastNetMon API using Python.

## Example

```python
import asyncio

from fastnetmon_api import FastNetMonAPI


async def main():
    async with FastNetMonAPI(
        host="127.0.0.1",
        port=10007,
        user="admin",
        password="admin",
    ) as api:
        await api.set_option("networks_list", "10.0.0.0/24")

        await api.set_host_group(
            "test",
            enable_ban=True,
            threshold_mbps=100,
            threshold_pps=10000,
        )


if __name__ == "__main__":
    asyncio.run(main())
```
