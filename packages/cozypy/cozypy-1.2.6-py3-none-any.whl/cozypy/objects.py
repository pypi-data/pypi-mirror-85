import logging

from .constant import (
    DeviceType,
    DeviceState,
    DeviceCommand,
    AwayModeState,
    OperatingModeState,
    TargetingHeatingLevelState
)
from .exception import CozytouchException

logger = logging.getLogger(__name__)


class DeviceMetadata:

    def __init__(self):
        self.scheme = None
        self.device_id = None
        self.gateway_id = None
        self.entity_id = None

    @property
    def base_url(self):
        url = self.scheme + "://" + self.gateway_id + "/" + self.device_id
        if self.entity_id is not None:
            url += "#" + self.entity_id
        return url

    def __str__(self):
        return "DeviceMetadata(scheme={scheme}, device={device}, gateway={gateway},entity={entity})".\
            format(scheme=self.scheme, device=self.device_id, gateway=self.gateway_id, entity=self.entity_id)


class CozytouchCommands:

    def __init__(self, label):
        self._label = label
        self._actions = []

    def add_action(self, action):
        """add_action"""
        self._actions.append(action)


class CozytouchAction:

    def __init__(self, device_url):
        self._device_url = device_url
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)


class CozytouchCommand:

    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters
        if parameters is not None and not isinstance(parameters, list):
            self.parameters = [parameters]


class CozytouchObject:

    def __init__(self, data: dict):
        self.client = None
        self.data = data

    @property
    def id(self):
        return self.data["oid"]

    @property
    def name(self):
        return self.data["label"]

    @property
    def creationTime(self):
        return self.data["creationTime"]

    @property
    def lastUpdateTime(self):
        return self.data["lastUpdateTime"]


class CozytouchDevice(CozytouchObject):

    def __init__(self, data: dict):
        super(CozytouchDevice, self).__init__(data)
        self.states = data["states"]
        self.metadata:DeviceMetadata = None
        self.gateway:CozytouchGateway = None
        self.place:CozytouchPlace = None
        self.parent:CozytouchDevice = None

    @property
    def device_url(self):
        return self.metadata.base_url

    @property
    def widget(self):
        return DeviceType(self.data['widget'])

    @property
    def manufacturer(self):
        return self.get_state(DeviceState.MANUFACTURER_NAME_STATE)

    @property
    def model(self):
        return self.get_state(DeviceState.MODEL_STATE)

    @property
    def name(self):
        return self.place.name + " " + self.widget.name.replace("_", " ").capitalize()

    @property
    def version(self):
        return self.get_state(DeviceState.VERSION_STATE)

    def get_state_definition(self, state: DeviceState):
        for definition in self.data["definition"]["states"]:
            if definition["qualifiedName"] == state.value:
                return definition
        return None

    def get_state(self, state: DeviceState, value_only=True):
        for s in self.states:
            if s["name"] == state.value:
                return s["value"] if value_only else s
        return None

    def set_state(self, state: DeviceState, value):
        for s in self.states:
            if s["name"] == state.value:
                s["value"] = value
                break

    def has_state(self, state: DeviceState):
        for s in self.states:
            if s["name"] == state.value:
                return True
        return False

    def update(self):
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        logger.debug("Update states sensors")
        self.states = self.client.get_device_info(self.device_url)

    @staticmethod
    def build(data, client, metadata=None, gateway=None, place=None, sensors=None, parent=None):
        if sensors is None:
            sensors = []
        device = None
        if "widget" not in data or "uiClass" not in data:
            raise CozytouchException("Unable to identify device")
        device_class = DeviceType.from_str(data["widget"] if "widget" in data else data["uiClass"])
        logger.debug(device_class)
        if device_class == DeviceType.OCCUPANCY:
            device = CozytouchOccupancySensor(data)
        elif device_class == DeviceType.POD:
            device = CozytouchPod(data)
        elif device_class == DeviceType.TEMPERATURE:
            device = CozytouchTemperatureSensor(data)
        elif device_class == DeviceType.OCCUPANCY:
            device = CozytouchOccupancySensor(data)
        elif device_class == DeviceType.ELECTRICITY:
            device = CozytouchElectricitySensor(data)
        elif device_class == DeviceType.CONTACT:
            device = CozytouchContactSensor(data)
        elif device_class in [DeviceType.HEATER, DeviceType.PILOT_WIRE_INTERFACE]:
            device = CozytouchHeater(data)
            device.sensors = sensors
        elif device_class in [DeviceType.WATER_HEATER]:
            device = CozytouchWaterHeater(data)
            device.sensors = sensors
        if device is None:
            raise CozytouchException("Unknown device {type}".format(type=device_class))

        device.client = client
        device.metadata = metadata
        device.gateway = gateway
        device.place = place
        device.parent = parent
        return device

    def __str__(self):
        return "{widget} (name={name}, model={model}, manufacturer={manufacturer}, version={version})"\
            .format(
                widget=self.widget.name.capitalize(),
                name=self.name,
                model=self.model,
                manufacturer=self.manufacturer,
                version=self.version
            )


class CozytouchPod(CozytouchDevice):

    def __init__(self, data: dict):
        super(CozytouchPod, self).__init__(data)

    @property
    def available(self):
        return self.data["available"]

    @property
    def is_on(self):
        return self.data["enabled"]

    @property
    def supported_states(self):
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
        return supported_state

    def is_state_supported(self, state: DeviceState):
        return state in self.supported_states


class CozytouchSensor(CozytouchDevice):

    def __init__(self, data: dict):
        super(CozytouchSensor, self).__init__(data)

    @property
    def id(self):
        return self.parent.id + "_" + self.sensor_class

    @property
    def name(self):
        name = self.parent.name if self.parent is not None else self.name
        return name + " " + self.sensor_class

    @property
    def sensor_class(self):
        return "unknown"


class CozytouchContactSensor(CozytouchSensor):

    def __init__(self, data: dict):
        super(CozytouchContactSensor, self).__init__(data)

    @property
    def sensor_class(self):
        return "contact"

    @property
    def is_opened(self):
        state = self.get_state(DeviceState.CONTACT_STATE)
        return state != "closed"


class CozytouchElectricitySensor(CozytouchSensor):

    def __init__(self, data: dict):
        super(CozytouchElectricitySensor, self).__init__(data)

    @property
    def sensor_class(self):
        return "electricity"

    @property
    def consumption(self):
        return int(self.get_state(DeviceState.ELECTRIC_ENERGY_CONSUMPTION_STATE))


class CozytouchTemperatureSensor(CozytouchSensor):

    def __init__(self, data: dict):
        super(CozytouchTemperatureSensor, self).__init__(data)

    @property
    def sensor_class(self):
        return "temperature"

    @property
    def temperature(self):
        return self.get_state(DeviceState.TEMPERATURE_STATE)


class CozytouchOccupancySensor(CozytouchSensor):

    def __init__(self, data: dict):
        super(CozytouchOccupancySensor, self).__init__(data)

    @property
    def sensor_class(self):
        return "occupancy"

    @property
    def is_occupied(self):
        state = self.get_state(DeviceState.OCCUPANCY_STATE)
        return state == "personInside"


class CozytouchHeater(CozytouchDevice):

    def __init__(self, data: dict):
        super(CozytouchHeater, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, device_type: DeviceType):
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    @property
    def is_on(self):
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            return self.target_heating_level != TargetingHeatingLevelState.OFF
        elif self.widget == DeviceType.HEATER:
            return self.operating_mode != OperatingModeState.STANDBY
        return False

    @property
    def is_away(self):
        away = self.get_state(DeviceState.AWAY_STATE)
        if away is None:
            return False
        return True if away == "on" else False

    @property
    def temperature(self):
        sensor = self.__get_sensors(DeviceType.TEMPERATURE)
        if sensor is None:
            return 0
        return sensor.temperature

    @property
    def target_temperature(self):
        return self.get_state(DeviceState.TARGET_TEMPERATURE_STATE)

    @property
    def comfort_temperature(self):
        return self.get_state(DeviceState.COMFORT_TEMPERATURE_STATE)

    @property
    def eco_temperature(self):
        comfort_temp = self.comfort_temperature
        if comfort_temp is None:
            return 0
        return comfort_temp - self.get_state(DeviceState.ECO_TEMPERATURE_STATE)

    @property
    def operating_mode(self):
        return OperatingModeState.from_str(self.get_state(DeviceState.OPERATING_MODE_STATE))

    @property
    def operating_mode_list(self):
        definition = self.get_state_definition(DeviceState.OPERATING_MODE_STATE)
        if definition is not None:
            return [OperatingModeState.from_str(value) for value in definition["values"]]
        return []

    @property
    def target_heating_level(self):
        return TargetingHeatingLevelState.from_str(self.get_state(DeviceState.TARGETING_HEATING_LEVEL_STATE))

    @property
    def target_heating_level_list(self):
        definition = self.get_state_definition(DeviceState.TARGETING_HEATING_LEVEL_STATE)
        if definition is not None:
            return [TargetingHeatingLevelState.from_str(value) for value in definition["values"]]
        return []

    @property
    def supported_states(self):
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
            for sensor in self.sensors:
                if sensor.has_state(state):
                    supported_state.append(state)
                    break
        return supported_state

    def is_state_supported(self, state: DeviceState):
        return state in self.supported_states

    def set_operating_mode(self, mode):
        if not self.has_state(DeviceState.OPERATING_MODE_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_OPERATION_MODE))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_OPERATION_MODE, mode))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_OPERATION_MODE))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.OPERATING_MODE_STATE, mode)

    def set_targeting_heating_level(self, level):
        if not self.has_state(DeviceState.TARGETING_HEATING_LEVEL_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_HEATING_LEVEL))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change heating level")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_HEATING_LEVEL, level))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.TARGETING_HEATING_LEVEL_STATE, level)

    def set_eco_temperature(self, temp):
        if not self.has_state(DeviceState.ECO_TEMPERATURE_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_ECO_TEMP))
        if self.client is None:
            raise CozytouchException("Unable to execute command")
        temperature = self.comfort_temperature - temp

        commands = CozytouchCommands("Set eco temperature")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_ECO_TEMP, temperature))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.ECO_TEMPERATURE_STATE, temperature)

    def set_comfort_temperature(self, temperature):
        if not self.has_state(DeviceState.COMFORT_TEMPERATURE_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_COMFORT_TEMP))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        eco_temp = temperature - self.eco_temperature

        commands = CozytouchCommands("Set comfort temperature")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_COMFORT_TEMP, temperature))
        action.add_command(CozytouchCommand(DeviceCommand.SET_ECO_TEMP, eco_temp))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_TARGET_TEMPERATURE))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.COMFORT_TEMPERATURE_STATE, temperature)
        self.set_state(DeviceState.ECO_TEMPERATURE_STATE, eco_temp)

    def set_target_temperature(self, temperature):
        if not self.has_state(DeviceState.TARGET_TEMPERATURE_STATE):
            raise CozytouchException("Unsupported command {command}".
                                     format(command=DeviceCommand.TARGET_TEMPERATURE_STATE))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set eco temperature")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_TARGET_TEMP, temperature))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_ECO_TEMPERATURE))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_COMFORT_TEMPERATURE))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_LOWERING_TEMP_PROG))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.TARGET_TEMPERATURE_STATE, temperature)

    def turn_away_mode_off(self):
        if not self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_AWAY_MODE))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set away mode OFF")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_AWAY_MODE, AwayModeState.OFF))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_STATE, AwayModeState.OFF)

    def turn_away_mode_on(self):
        if not self.has_state(DeviceState.AWAY_STATE):
            raise CozytouchException("Unsupported command {command}".format(command=DeviceCommand.SET_AWAY_MODE))
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Set away mode ON")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_AWAY_MODE, AwayModeState.ON))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_STATE, AwayModeState.ON)

    def turn_on(self):
        from .constant import DeviceType, OperatingModeState, TargetingHeatingLevelState
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            self.set_targeting_heating_level(TargetingHeatingLevelState.COMFORT)
        elif self.widget == DeviceType.HEATER:
            self.set_operating_mode(OperatingModeState.INTERNAL)

    def turn_off(self):
        from .constant import DeviceType, OperatingModeState, TargetingHeatingLevelState
        if self.widget == DeviceType.PILOT_WIRE_INTERFACE:
            self.set_targeting_heating_level(TargetingHeatingLevelState.OFF)
        elif self.widget == DeviceType.HEATER:
            self.set_operating_mode(OperatingModeState.STANDBY)

    def update(self):
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Heater : Update sensor")
            sensor.update()
        super(CozytouchHeater, self).update()


class CozytouchWaterHeater(CozytouchDevice):

    def __init__(self, data: dict):
        super(CozytouchWaterHeater, self).__init__(data)
        self.sensors = []

    def __get_sensors(self, device_type: DeviceType):
        for sensor in self.sensors:
            if sensor.widget == device_type:
                return sensor
        return None

    @property
    def is_on(self):
        return self.operating_mode != OperatingModeState.STANDBY

    @property
    def operating_mode(self):
        return OperatingModeState.from_str(self.get_state(DeviceState.OPERATING_MODE_STATE))

    @property
    def supported_states(self):
        supported_state = [state for state in DeviceState if self.has_state(state)]
        for state in DeviceState:
            if state in supported_state:
                continue
            for sensor in self.sensors:
                if sensor.has_state(state):
                    supported_state.append(state)
                    break
        return supported_state

    def is_state_supported(self, state: DeviceState):
        return state in self.supported_states

    def set_operating_mode(self, mode):
        if not self.has_state(DeviceState.OPERATING_MODE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(command=DeviceCommand.SET_DWH_MODE)
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_DWH_MODE, mode))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_DHW_MODE))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.OPERATING_MODE_STATE, mode)

    def set_away_mode(self, duration):
        if not self.has_state(DeviceState.AWAY_MODE_DURATION_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(command=DeviceCommand.SET_DWH_MODE)
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change operating mode")
        action = CozytouchAction(device_url=self.device_url)
        if int(duration) == 0:
            action.add_command(
                CozytouchCommand(DeviceCommand.SET_CURRENT_OPERATION_MODE, {"relaunch": "off", "absence": "off"})
            )
        else:
            action.add_command(
                CozytouchCommand(DeviceCommand.SET_CURRENT_OPERATION_MODE, {"relaunch": "off", "absence": "on"})
            )
        action.add_command(CozytouchCommand(DeviceCommand.SET_ALWAYS_MODE_DURATION, duration))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_ALWAYS_MODE_DURATION))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.AWAY_MODE_DURATION_STATE, duration)

    def set_boost_mode(self, duration):
        if not self.has_state(DeviceState.BOOST_MODE_DURATION_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(command=DeviceCommand.SET_BOOST_MODE_DURATION)
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change Boost mode")
        action = CozytouchAction(device_url=self.device_url)
        if int(duration) == 0:
            action.add_command(
                CozytouchCommand(DeviceCommand.SET_CURRENT_OPERATION_MODE, {"relaunch": "off", "absence": "off"})
            )
        else:
            action.add_command(
                CozytouchCommand(DeviceCommand.SET_CURRENT_OPERATION_MODE, {"relaunch": "on", "absence": "off"})
            )
            action.add_command(CozytouchCommand(DeviceCommand.SET_BOOST_MODE_DURATION, duration))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_BOOST_MODE_DURATION))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.BOOST_MODE_DURATION_STATE, duration)

    def set_temperature(self, temp):
        if not self.has_state(DeviceState.TARGET_TEMPERATURE_STATE):
            raise CozytouchException(
                "Unsupported command {command}".format(command=DeviceCommand.SET_TARGET_TEMP)
            )
        if self.client is None:
            raise CozytouchException("Unable to execute command")

        commands = CozytouchCommands("Change target temperature")
        action = CozytouchAction(device_url=self.device_url)
        action.add_command(CozytouchCommand(DeviceCommand.SET_TARGET_TEMP, temp))
        action.add_command(CozytouchCommand(DeviceCommand.REFRESH_TARGET_TEMPERATURE))
        commands.add_action(action)

        self.client.send_commands(commands)

        self.set_state(DeviceState.TARGET_TEMPERATURE_STATE, temp)

    def update(self):
        if self.client is None:
            raise CozytouchException("Unable to update heater")
        for sensor in self.sensors:
            logger.debug("Water Heater : Update sensor")
            sensor.update()
        super(CozytouchWaterHeater, self).update()


class CozytouchPlace(CozytouchObject):

    def __init__(self, data):
        super(CozytouchPlace, self).__init__(data)

    def __str__(self):
        return "Place(id={id},name={name})"\
            .format(id=self.id, name=self.name)


class CozytouchGateway:

    def __init__(self, data: dict, place: CozytouchPlace):
        self.data = data
        self.place = place

    @property
    def device_url(self):
        return self.data["deviceURL"]

    @property
    def id(self):
        return self.data["gatewayId"]

    @property
    def is_on(self):
        return self.data["alive"]

    @property
    def version(self):
        return self.data["connectivity"]["protocolVersion"]

    @property
    def status(self):
        return self.data["connectivity"]["status"] == "OK"

    def __str__(self):
        return "Gateway(id={id},is_on={is_on},status={status}, version={version})"\
            .format(id=self.id, is_on=self.is_on, version=self.version, status=self.status)