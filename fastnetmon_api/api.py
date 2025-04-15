from typing import Any, Unpack, overload

import httpx

from .types import (
    ArrayResponse,
    BanSettings,
    BanSettingsRequired,
    BaseResponse,
    GlobalIntOptions,
    GlobalStrOptions,
    HostGroupBoolOptions,
    HostGroupIntOptions,
    HostGroupStrOptions,
)


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
            raise httpx.HTTPStatusError(
                data["error_text"],
                request=response.request,
                response=response,
            )

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

    async def remove_host_group(self, name: str):
        res = await self.client.delete(f"/hostgroup/{name}")

        return self._parse_response(res)

    async def get_host_group(self, name: str):
        res = await self.client.get(f"/hostgroup/{name}")

        data = self._parse_response(res, ArrayResponse[BanSettingsRequired])

        return data["values"][0]

    async def get_host_groups(self):
        res = await self.client.get("/hostgroup")

        data = self._parse_response(res, ArrayResponse[BanSettingsRequired])

        return data["values"]

    @overload
    async def set_host_group_option(
        self, host_group: str, option: HostGroupStrOptions, value: str
    ) -> None: ...

    @overload
    async def set_host_group_option(
        self, host_group: str, option: HostGroupBoolOptions, value: bool
    ) -> None: ...

    @overload
    async def set_host_group_option(
        self, host_group: str, option: HostGroupIntOptions, value: int
    ) -> None: ...

    async def set_host_group_option(
        self, host_group: str, option: str, value: str | int | bool
    ) -> None:
        value = self._get_option_value(value)

        res = await self.client.put(f"/hostgroup/{host_group}/{option}/{value}")

        return self._parse_response(res)

    @overload
    async def remove_host_group_option(
        self, host_group: str, option: HostGroupStrOptions, value: str
    ) -> None: ...

    @overload
    async def remove_host_group_option(
        self, host_group: str, option: HostGroupBoolOptions, value: bool
    ) -> None: ...

    @overload
    async def remove_host_group_option(
        self, host_group: str, option: HostGroupIntOptions, value: bool
    ) -> None: ...

    async def remove_host_group_option(
        self, host_group: str, option: str, value: str | int | bool
    ) -> None:
        value = self._get_option_value(value)

        res = await self.client.delete(f"/hostgroup/{host_group}/{option}/{value}")

        return self._parse_response(res)

    @overload
    async def get_host_group_option(
        self, host_group: str, option: HostGroupStrOptions
    ) -> str: ...

    @overload
    async def get_host_group_option(
        self, host_group: str, option: HostGroupBoolOptions
    ) -> bool: ...

    @overload
    async def get_host_group_option(
        self, host_group: str, option: HostGroupIntOptions
    ) -> int: ...

    async def get_host_group_option(
        self, host_group: str, option: str
    ) -> str | int | bool:
        res = await self.client.get(f"/hostgroup/{host_group}/{option}")

        return self._parse_response(res)  # type: ignore

    @overload
    async def set_option(self, option: GlobalIntOptions, value: int) -> None: ...

    @overload
    async def set_option(self, option: GlobalStrOptions, value: str) -> None: ...

    async def set_option(self, option: str, value: str | int | bool) -> None:
        value = self._get_option_value(value)

        res = await self.client.put(f"/main/{option}/{value}")

        return self._parse_response(res)

    @overload
    async def remove_option(self, option: GlobalIntOptions, value: int) -> None: ...

    @overload
    async def remove_option(self, option: GlobalStrOptions, value: str) -> None: ...

    async def remove_option(self, option: str, value: str | int | bool) -> None:
        value = self._get_option_value(value)

        res = await self.client.delete(f"/main/{option}/{value}")

        return self._parse_response(res)

    @overload
    async def get_option(self, option: GlobalIntOptions) -> list[int]: ...

    @overload
    async def get_option(self, option: GlobalIntOptions) -> list[str]: ...

    async def get_option(self, option: str) -> list[str] | list[int] | str | int | bool:
        res = await self.client.delete(f"/main/{option}")

        return self._parse_response(res)  # type: ignore

    async def commit(self):
        res = await self.client.put("/commit")

        return self._parse_response(res)
