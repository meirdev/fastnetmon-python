from typing import Any, Unpack, overload

import httpx

from .types import (
    ArrayResponse,
    BanSettings,
    BanSettingsRequired,
    BaseResponse,
    FlowSpecRule,
    FlowSpecRuleAnnounce,
    GlobalOptions,
    HostGroupOptions,
)


class FastNetMonAPIError(Exception):
    pass


class FastNetMonAPI:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        base_url = f"http://{host}:{port}"

        self.client = httpx.AsyncClient(base_url=base_url, auth=(user, password))

    async def __aenter__(self) -> "FastNetMonAPI":
        return self

    async def __aexit__(self, *_exc: Any) -> None:
        await self.client.aclose()

    @overload
    def _parse_response[T: BaseResponse](
        self, response: httpx.Response, type_: type[T]
    ) -> T: ...

    @overload
    def _parse_response[T: BaseResponse](
        self, response: httpx.Response, type_: None = None
    ) -> None: ...

    def _parse_response[T: BaseResponse](
        self, response: httpx.Response, type_: type[T] | None = None
    ) -> T | None:
        response.raise_for_status()

        data: T = response.json()

        if not data["success"]:
            raise FastNetMonAPIError(data["error_text"])

        if type_ is BaseResponse:
            return None

        return data

    def _get_option_value(self, value: str | int | bool) -> str:
        if isinstance(value, bool):
            return "enable" if value else "disable"

        return str(value)

    async def set_host_group(self, name: str, **kwargs: Unpack[BanSettings]):
        res = await self.client.post(f"/hostgroup/{name}")

        data = self._parse_response(res, BaseResponse)

        for key, value in kwargs.items():
            if not isinstance(value, list):
                value = [value]

            for item in value:  # type: ignore
                await self.set_host_group_option(name, key, item)  # type: ignore

        return data

    async def remove_host_group(self, name: HostGroupOptions):
        res = await self.client.delete(f"/hostgroup/{name}")

        return self._parse_response(res)

    async def get_host_group(self, name: HostGroupOptions):
        res = await self.client.get(f"/hostgroup/{name}")

        data = self._parse_response(res, ArrayResponse[BanSettingsRequired])

        return data["values"][0]

    async def get_host_groups(self):
        res = await self.client.get("/hostgroup")

        data = self._parse_response(res, ArrayResponse[BanSettingsRequired])

        return data["values"]

    async def set_host_group_option(
        self, host_group: str, option: HostGroupOptions, value: str | int | bool
    ) -> None:
        value = self._get_option_value(value)

        res = await self.client.put(f"/hostgroup/{host_group}/{option}/{value}")

        return self._parse_response(res)

    async def remove_host_group_option(
        self, host_group: str, option: HostGroupOptions, value: str | int | bool
    ) -> None:
        value = self._get_option_value(value)

        res = await self.client.delete(f"/hostgroup/{host_group}/{option}/{value}")

        return self._parse_response(res)

    async def get_host_group_option(
        self, host_group: str, option: HostGroupOptions
    ) -> list[str] | str | int | bool:
        res = await self.client.get(f"/hostgroup/{host_group}/{option}")

        return self._parse_response(res)  # type: ignore

    async def set_option(self, option: GlobalOptions, value: str | int | bool):
        value = self._get_option_value(value)

        res = await self.client.put(f"/main/{option}/{value}")

        return self._parse_response(res)

    async def remove_option(self, option: GlobalOptions, value: str | int | bool):
        value = self._get_option_value(value)

        res = await self.client.delete(f"/main/{option}/{value}")

        return self._parse_response(res)

    async def get_option(
        self, option: GlobalOptions
    ) -> list[str] | list[int] | str | int | bool:
        res = await self.client.get(f"/main/{option}")

        return self._parse_response(res)  # type: ignore

    async def commit(self):
        res = await self.client.put("/commit")

        return self._parse_response(res)

    async def add_flow_spec_rule(self, flow_spec_rule: FlowSpecRule):
        res = await self.client.put("/flowspec", json=flow_spec_rule)

        return self._parse_response(res)

    async def get_flow_spec_rules(self, mitigation_uuid: str):
        res = await self.client.get(f"/flowspec/{mitigation_uuid}")

        data = self._parse_response(res, ArrayResponse[FlowSpecRuleAnnounce])

        return data["values"]

    async def remove_flow_spec_rule(self, mitigation_uuid: str):
        res = await self.client.delete(f"/flowspec/{mitigation_uuid}")

        return self._parse_response(res)
