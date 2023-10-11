import asyncio
from abc import abstractmethod
from typing import Dict
from pydantic_settings import BaseSettings

from ace.logger import Logger


class TelemetrySettings(BaseSettings):
    name: str
    label: str
    namespaces: Dict[str, int] = {}
    data_depth: int = 5


class Telemetry:
    def __init__(self, publisher=None):
        self.publisher = publisher
        self.log = Logger(self.__class__.__name__)
        self.data_points = {k: [] for k in self.settings.namespaces.keys()}
        self.event_listeners = {}
        self.scheduler = {}
        self.stop_event = {}

    @property
    @abstractmethod
    def settings(self) -> TelemetrySettings:
        pass

    @abstractmethod
    async def collect_data_sample(self, namespace):
        raise NotImplementedError

    @property
    def labeled_name(self):
        return f"{self.settings.name} ({self.settings.label})"

    @property
    def namespaces(self):
        return self.settings.namespaces

    def manage_data_points(self, namespace, data):
        data_points = self.data_points[namespace]
        data_points.extend(data)
        if len(data_points) > self.settings.data_depth:
            remove_count = len(data_points) - self.settings.data_depth
            self.log.debug(f"{self.labeled_name} truncating oldest {remove_count} data points for namespace: {namespace}")
            self.data_points[namespace] = data_points[remove_count:]

    async def publish(self, namespace, data):
        self.log.debug(f"{self.labeled_name} publishing telemetry data to: {namespace}")
        await self.publisher(namespace, data)
        self.log.debug(f"{self.labeled_name} published telemetry data to: {namespace}")

    async def collect_data(self, namespace):
        self.log.debug(f"{self.labeled_name} collecting data for namespace: {namespace}")
        data = await self.collect_data_sample(namespace)
        if data is not None:
            self.log.debug(f"{self.labeled_name} collected data for namespace {namespace}: {data}")
            data = data if isinstance(data, list) else [data]
            self.manage_data_points(namespace, data)
            self.log.debug(f"{self.labeled_name} collected data for namespace: {namespace}")

    async def get_data(self, namespace, return_data_points=1):
        data_points = self.data_points[namespace]
        self.log.debug(f"{self.labeled_name} getting data for namespace: {namespace}, data points: {data_points}")
        if return_data_points > 1:
            return data_points[-return_data_points:]
        return data_points[-1] if len(data_points) > 0 else None

    async def collection_event(self, namespace):
        self.log.debug(f"{self.labeled_name} starting data collection event for namespace: {namespace}")
        await self.collect_data(namespace)
        data = await self.get_data(namespace)
        await self.publish(namespace, data)
        self.log.debug(f"{self.labeled_name} finished data collection event for namespace: {namespace}")

    async def schedule_collection(self, namespace):
        if namespace in self.settings.namespaces:
            interval = self.settings.namespaces[namespace]
            if interval > 0:
                self.log.info(f"{self.labeled_name} scheduled data collection interval for namespace: {namespace}, interval seconds: {interval}")
                while not self.stop_event[namespace].is_set():
                    await self.collection_event(namespace)
                    await asyncio.sleep(interval)

    def start_collecting(self, namespace):
        self.stop_event[namespace] = asyncio.Event()
        loop = asyncio.get_event_loop()
        self.scheduler[namespace] = loop.create_task(self.schedule_collection(namespace))

    def stop_collecting(self, namespace):
        self.stop_event[namespace].set()
        self.scheduler[namespace].cancel()
