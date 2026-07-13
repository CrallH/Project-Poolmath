"""Sensor platform for the Pool Math integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import PoolMathConfigEntry
from .const import (
    ATTR_LAST_MEASURED,
    CONF_TEMP_UNIT,
    DEFAULT_TEMP_UNIT,
    DOMAIN,
    SHARE_URL,
)
from .coordinator import PoolMathCoordinator


@dataclass(frozen=True, kw_only=True)
class PoolMathSensorEntityDescription(SensorEntityDescription):
    """Describes a Pool Math sensor."""

    json_key: str


SENSOR_TYPES: tuple[PoolMathSensorEntityDescription, ...] = (
    PoolMathSensorEntityDescription(
        key="fc",
        json_key="fc",
        translation_key="fc",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flask",
    ),
    PoolMathSensorEntityDescription(
        key="cc",
        json_key="cc",
        translation_key="cc",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flask-outline",
    ),
    PoolMathSensorEntityDescription(
        key="ph",
        json_key="ph",
        translation_key="ph",
        device_class=SensorDeviceClass.PH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PoolMathSensorEntityDescription(
        key="ta",
        json_key="ta",
        translation_key="ta",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-opacity",
    ),
    PoolMathSensorEntityDescription(
        key="ch",
        json_key="ch",
        translation_key="ch",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-percent",
    ),
    PoolMathSensorEntityDescription(
        key="cya",
        json_key="cya",
        translation_key="cya",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:shield-sun-outline",
    ),
    PoolMathSensorEntityDescription(
        key="salt",
        json_key="salt",
        translation_key="salt",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:shaker-outline",
    ),
    PoolMathSensorEntityDescription(
        key="borate",
        json_key="bor",
        translation_key="borate",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:molecule",
    ),
    PoolMathSensorEntityDescription(
        key="csi",
        json_key="csi",
        translation_key="csi",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calculator-variant-outline",
    ),
    PoolMathSensorEntityDescription(
        key="water_temp",
        json_key="waterTemp",
        translation_key="water_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PoolMathSensorEntityDescription(
        key="swg_cell_percent",
        json_key="swgCellPercent",
        translation_key="swg_cell_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:lightning-bolt-outline",
    ),
    PoolMathSensorEntityDescription(
        key="pressure",
        json_key="pressure",
        translation_key="pressure",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
)


@dataclass(frozen=True, kw_only=True)
class PoolMathDaysSinceSensorEntityDescription(SensorEntityDescription):
    """Describes a Pool Math 'days since last logged' sensor."""

    ts_key: str


STATUS_SENSOR_TYPES: tuple[PoolMathDaysSinceSensorEntityDescription, ...] = (
    PoolMathDaysSinceSensorEntityDescription(
        key="backwashed",
        ts_key="backwashedTs",
        translation_key="backwashed",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:pool",
    ),
    PoolMathDaysSinceSensorEntityDescription(
        key="brushed",
        ts_key="brushedTs",
        translation_key="brushed",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:broom",
    ),
    PoolMathDaysSinceSensorEntityDescription(
        key="cleaned_filter",
        ts_key="cleanedFilterTs",
        translation_key="cleaned_filter",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
    ),
    PoolMathDaysSinceSensorEntityDescription(
        key="vacuumed",
        ts_key="vacuumedTs",
        translation_key="vacuumed",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:robot-vacuum",
    ),
    PoolMathDaysSinceSensorEntityDescription(
        key="opened",
        ts_key="openedTs",
        translation_key="opened",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calendar-start",
    ),
    PoolMathDaysSinceSensorEntityDescription(
        key="closed",
        ts_key="closedTs",
        translation_key="closed",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calendar-end",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PoolMathConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pool Math sensors from a config entry."""
    coordinator = entry.runtime_data
    overview: dict[str, Any] = coordinator.data.get("overview") or {}

    entities: list[SensorEntity] = [
        PoolMathSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
        if description.json_key in overview
        and overview.get(description.json_key) is not None
    ]
    entities.extend(
        PoolMathDaysSinceSensor(coordinator, description)
        for description in STATUS_SENSOR_TYPES
        if overview.get(description.ts_key) is not None
    )
    async_add_entities(entities)


class PoolMathSensor(CoordinatorEntity[PoolMathCoordinator], SensorEntity):
    """A water chemistry sensor backed by PoolMath."""

    entity_description: PoolMathSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PoolMathCoordinator,
        entry: PoolMathConfigEntry,
        description: PoolMathSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.share_id}_{description.key}"

        if description.key == "water_temp":
            temp_unit = entry.options.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)
            self._attr_native_unit_of_measurement = (
                UnitOfTemperature.FAHRENHEIT
                if temp_unit == "fahrenheit"
                else UnitOfTemperature.CELSIUS
            )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.share_id)},
            name=coordinator.data.get("name") or "Pool Math",
            manufacturer="Trouble Free Pool",
            model="Pool Math",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=SHARE_URL.format(share_id=coordinator.share_id),
        )

    @property
    def native_value(self) -> float | int | None:
        """Return the current value."""
        overview = self.coordinator.data.get("overview") or {}
        return overview.get(self.entity_description.json_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the last-measured timestamp when the API provides one."""
        overview = self.coordinator.data.get("overview") or {}
        for ts_key in (
            f"{self.entity_description.json_key}Ts",
            f"{self.entity_description.json_key}DateTime",
        ):
            if overview.get(ts_key):
                return {ATTR_LAST_MEASURED: overview[ts_key]}
        return None


class PoolMathDaysSinceSensor(CoordinatorEntity[PoolMathCoordinator], SensorEntity):
    """Days elapsed since a maintenance activity was last logged in Pool Math."""

    entity_description: PoolMathDaysSinceSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PoolMathCoordinator,
        description: PoolMathDaysSinceSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.share_id}_{description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.share_id)},
            name=coordinator.data.get("name") or "Pool Math",
            manufacturer="Trouble Free Pool",
            model="Pool Math",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=SHARE_URL.format(share_id=coordinator.share_id),
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of days since the activity was last logged."""
        overview = self.coordinator.data.get("overview") or {}
        timestamp = overview.get(self.entity_description.ts_key)
        if not timestamp:
            return None
        parsed = dt_util.parse_datetime(timestamp)
        if parsed is None:
            return None
        return (dt_util.utcnow() - parsed).days

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the raw last-logged timestamp."""
        overview = self.coordinator.data.get("overview") or {}
        timestamp = overview.get(self.entity_description.ts_key)
        if timestamp:
            return {ATTR_LAST_MEASURED: timestamp}
        return None
