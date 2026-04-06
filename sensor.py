"""Sensor platform for UrbanHive."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Wir erstellen für jede Reihe im JSON einen Sensor
    entities = []
    for index, row in enumerate(coordinator.data.get("rows", [])):
        entities.append(UrbanHiveWaterSensor(coordinator, index))
    
    async_add_entities(entities)

class UrbanHiveWaterSensor(CoordinatorEntity, SensorEntity):
    """Representation of an UrbanHive Water Level sensor."""

    def __init__(self, coordinator, row_index):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._row_index = row_index
        
        # Daten aus dem Koordinator beziehen
        farm_id = coordinator.data.get("id", "unknown")
        # Falls "farmName" im JSON auf oberster Ebene steht:
        farm_name = coordinator.data.get("farmName", f"UrbanHive {farm_id}")

        # Eindeutige ID für die Entität
        self._attr_unique_id = f"{farm_id}_row_{row_index}_water"
        self._attr_name = f"Reihe {row_index + 1} Wasserstand"
        
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_icon = "mdi:water-percent"

        # Definition des Geräts (Device)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, farm_id)},
            name=farm_name,
            manufacturer="UrbanHive",
            model="Homefarm",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            return self.coordinator.data["rows"][self._row_index]["waterLevel"]
        except (KeyError, IndexError):
            return None
