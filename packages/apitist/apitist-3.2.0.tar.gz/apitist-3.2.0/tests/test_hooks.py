import datetime
import json
import logging
import typing
from dataclasses import dataclass

import pytest

import attr

from apitist import (
    AttrsConverter,
    DataclassConverter,
    request_attrs_converter_hook,
    request_dataclass_converter_hook,
    response_attrs_converter_hook,
    response_dataclass_converter_hook,
)
from apitist.hooks import (
    PreparedRequestHook,
    PrepRequestDebugLoggingHook,
    PrepRequestInfoLoggingHook,
    RequestAttrsConverterHook,
    RequestDataclassConverterHook,
    RequestDebugLoggingHook,
    RequestHook,
    RequestInfoLoggingHook,
    ResponseAttrsConverterHook,
    ResponseDataclassConverterHook,
    ResponseDebugLoggingHook,
    ResponseHook,
    ResponseInfoLoggingHook,
)
from apitist.requests import Session, session


@attr.s
class ExampleData:
    test: str = attr.ib()


@attr.s
class ExampleResponse:
    args: typing.Dict = attr.ib()
    data: str = attr.ib()
    files: typing.Dict = attr.ib()
    form: typing.Dict = attr.ib()
    headers: typing.Dict = attr.ib()
    json: typing.Any = attr.ib()
    origin: str = attr.ib()
    url: str = attr.ib()


@dataclass
class ExampleDataclass:
    test: str


@dataclass
class ExampleResponseDataclass:
    args: typing.Dict
    data: str
    files: typing.Dict
    form: typing.Dict
    headers: typing.Dict
    json: typing.Any
    origin: str
    url: str


class TestHooks:
    def test_session_creation(self):
        assert isinstance(session(), Session)

    @pytest.mark.parametrize(
        "hook", [(PreparedRequestHook), (RequestHook), (ResponseHook)]
    )
    def test_empty_hooks(self, hook):
        assert hook().run(None) is None

    @pytest.mark.parametrize("hook", [int, str, bool])
    def test_incorrect_hook(self, session, hook):
        session.add_hook(hook)
        assert len(session.request_hooks) == 0
        assert len(session.prep_request_hooks) == 0
        assert len(session.response_hooks) == 0

    @pytest.mark.usefixtures("enable_debug_logging")
    @pytest.mark.parametrize(
        "hook,text",
        [
            (RequestDebugLoggingHook, "Request"),
            (PrepRequestDebugLoggingHook, "Request"),
            (ResponseDebugLoggingHook, "Response"),
        ],
    )
    def test_debug_logging_hooks(self, session, hook, text, capture):
        session.add_hook(hook)
        session.get("http://httpbin.org/get")
        assert len(capture.records) == 2
        assert capture.records[1].levelno == logging.DEBUG
        assert text in capture.records[1].msg

    @pytest.mark.parametrize(
        "hook,text",
        [
            (RequestInfoLoggingHook, "Request"),
            (PrepRequestInfoLoggingHook, "Request"),
            (ResponseInfoLoggingHook, "Response"),
        ],
    )
    def test_info_logging_hooks(self, session, hook, text, capture):
        session.add_hook(hook)
        session.get("http://httpbin.org/get")
        assert len(capture.records) == 1
        assert capture.records[0].levelno == logging.INFO
        assert text in capture.records[0].msg

    def test_request_converter_attrs_class(self, session):
        session.add_hook(RequestAttrsConverterHook)
        res = session.get("http://httpbin.org/get", data=ExampleData("test"))
        assert res.request.body == json.dumps({"test": "test"}).encode("utf-8")

    def test_request_converter_non_attrs(self, session):
        session.add_hook(RequestAttrsConverterHook)
        res = session.get("http://httpbin.org/get", data="test")
        assert res.request.body == "test"

    def test_response_converter_adding_function(self, session):
        session.add_hook(ResponseAttrsConverterHook)
        res = session.get("http://httpbin.org/get")
        assert getattr(res, "structure")

    def test_response_converter_correct_type(self, session):
        session.add_hook(ResponseAttrsConverterHook)
        res = session.post("http://httpbin.org/post")
        res.structure(ExampleResponse)
        assert isinstance(res.data, ExampleResponse)

    def test_response_converter_incorrect_type(self, session):
        session.add_hook(ResponseAttrsConverterHook)
        res = session.post("http://httpbin.org/post")
        with pytest.raises(TypeError):
            res.structure(ExampleData)

    def test_request_converter_dataclass_class(self, session):
        session.add_hook(RequestDataclassConverterHook)
        res = session.get(
            "http://httpbin.org/get", data=ExampleDataclass("test")
        )
        assert res.request.body == json.dumps({"test": "test"}).encode("utf-8")

    def test_request_converter_non_dataclass(self, session):
        session.add_hook(RequestDataclassConverterHook)
        res = session.get("http://httpbin.org/get", data="test")
        assert res.request.body == "test"

    def test_response_converter_adding_function_dataclass(self, session):
        session.add_hook(ResponseDataclassConverterHook)
        res = session.get("http://httpbin.org/get").vr()
        assert getattr(res, "structure")
        assert getattr(res, "verify_response")
        assert getattr(res, "vr")

    def test_response_verify_response_success(self, session):
        session.get("http://httpbin.org/get").vr([200, 201])

    def test_response_verify_response_error(self, session):
        with pytest.raises(ValueError):
            session.get("http://httpbin.org/get").vr(400)

    def test_response_converter_correct_dataclass_type(self, session):
        session.add_hook(ResponseDataclassConverterHook)
        res = session.post("http://httpbin.org/post")
        res.structure(ExampleResponseDataclass)
        assert isinstance(res.data, ExampleResponseDataclass)

    def test_response_converter_incorrect_dataclass_type(self, session):
        session.add_hook(ResponseDataclassConverterHook)
        res = session.post("http://httpbin.org/post")
        with pytest.raises(TypeError):
            res.structure(ExampleDataclass)

    def test_custom_converter_hooks_attrs(self, session):
        @attr.s
        class Data:
            test: datetime.datetime = attr.ib()

        @attr.s
        class ResData:
            json: Data = attr.ib()

        conv = AttrsConverter()
        req_hook = request_attrs_converter_hook(conv)
        res_hook = response_attrs_converter_hook(conv)
        session.add_hook(req_hook)
        session.add_hook(res_hook)
        with pytest.raises(TypeError):
            session.post(
                "http://httpbin.org/post", data=Data(datetime.datetime.now())
            )
        with pytest.raises(ValueError):
            session.post(
                "http://httpbin.org/post", json={"test": "22:13:44"}
            ).structure(ResData)
        conv.register_hooks(
            datetime.datetime,
            lambda obj, _: datetime.datetime.strptime(obj, "%H:%M:%S"),
            lambda obj: obj.strftime("%H:%M:%S"),
        )
        res = session.post(
            "http://httpbin.org/post", data=Data(datetime.datetime.now())
        ).structure(ResData)
        assert res.data.json.test

    def test_custom_converter_hooks_dataclasses(self, session):
        @dataclass
        class Data:
            test: datetime.datetime

        @dataclass
        class ResData:
            json: Data

        conv = DataclassConverter()
        req_hook = request_dataclass_converter_hook(conv)
        res_hook = response_dataclass_converter_hook(conv)
        session.add_hook(req_hook)
        session.add_hook(res_hook)
        with pytest.raises(TypeError):
            session.post(
                "http://httpbin.org/post", data=Data(datetime.datetime.now())
            )
        with pytest.raises(ValueError):
            session.post(
                "http://httpbin.org/post", json={"test": "22:13:44"}
            ).structure(ResData)
        conv.register_hooks(
            datetime.datetime,
            lambda obj, _: datetime.datetime.strptime(obj, "%H:%M:%S"),
            lambda obj: obj.strftime("%H:%M:%S"),
        )
        res = session.post(
            "http://httpbin.org/post", data=Data(datetime.datetime.now())
        ).structure(ResData)
        assert res.data.json.test
