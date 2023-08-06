# rackio_modbus/_server.py

from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server

from rackio import TagEngine

from .api import MappingResource


class FloatTagMap:

    def __init__(self, tag, lower, upper):

        self.tag = tag
        self.upper = upper
        self.lower = lower

        self.OFFSET = 0

    def register(self, value):

        upper = self.upper
        lower = self.lower
        OFFSET = self.OFFSET

        result = int(((value - lower) / (upper - lower)) * 65535) + OFFSET

        if result < 0:
            return 0

        if result > 65535:
            return 65535
        
        return result

    def value(self, register):

        upper = self.upper
        lower = self.lower

        return (register / 65535) * (upper - lower) + lower


class IntTagMap:

    def __init__(self, tag, lower, upper):

        self.tag = tag
        self.upper = upper
        self.lower = lower

        self.OFFSET = 0

    def register(self, value):

        upper = self.upper
        lower = self.lower
        OFFSET = self.OFFSET

        result = int(((value - lower) / (upper - lower)) * 65535) + OFFSET

        if result < 0:
            return 0

        if result > 65535:
            return 65535

        return result

    def value(self, register):

        upper = self.upper
        lower = self.lower

        return int((register / 65535) * (upper - lower) + lower)


class BooleanTagMap:

    def __init__(self, tag):

        self.tag = tag

    def coil(self, value):

        if value:
            return 1
        return 0

    def value(self, coil):

        if coil == 1:
            return True
        return False


class ModbusServer():

    def __init__(self):

        conf.SIGNED_VALUES = True
        TCPServer.allow_reuse_address = True

        self.app = get_server(TCPServer, ('localhost', 502), RequestHandler)

        self.mappings = list()
        self.input_registers = list()
        self.holding_registers = list()
        self.coils = list()
        self.discrete = list()

    def get_driver(self):

        return self.app

    def serialize_mappings(self):

        result = dict()

        result["holding_registers"] = list()
        
        for mapping in self.holding_registers:

            record = {
                "tag": mapping.tag,
                "upper": mapping.upper,
                "lower": mapping.lower
            }

            result["holding_registers"].append(record)

        result["input_registers"] = list()
        
        for mapping in self.input_registers:

            record = {
                "tag": mapping.tag,
                "upper": mapping.upper,
                "lower": mapping.lower
            }

            result["input_registers"].append(record)

        result["coils"] = list()
        
        for mapping in self.coils:

            record = {
                "tag": mapping.tag
            }

            result["coils"].append(record)

        result["discrete"] = list()
        
        for mapping in self.discrete:

            record = {
                "tag": mapping.tag
            }

            result["discrete"].append(record)

        return result

    def define_mapping(self, tag, direction, lower, upper):

        engine = TagEngine()

        _type = engine.get_type(tag)

        if _type == "float":
            mapping = FloatTagMap(tag, lower, upper)

            if direction == "write":
                self.holding_registers.append(mapping)
            else:
                self.input_registers.append(mapping)

        elif _type == "int":
            mapping = IntTagMap(tag, lower, upper)

            if direction == "write":
                self.holding_registers.append(mapping)
            else:
                self.input_registers.append(mapping)
        elif _type == ["bool"]:
            mapping = BooleanTagMap(tag)

            if direction == "write":
                self.discrete.append(mapping)
            else:
                self.coils.append(mapping)

        self.mappings.append(mapping)

    def write_register(self, slave_id, function_code, address, value):

        engine = TagEngine()

        mapping = self.holding_registers[address]
        tag = mapping.tag

        value = mapping.value(value)
        engine.write_tag(tag, value)

    def read_register(self, slave_id, function_code, address):
        
        engine = TagEngine()
        
        if function_code == 3:
            mapping = self.holding_registers[address]
        elif function_code == 4:
            mapping = self.input_registers[address]

        tag = mapping.tag

        value = engine.read_tag(tag)

        return mapping.register(value)

    def write_coil(self, slave_id, function_code, address, value):

        engine = TagEngine()

        mapping = self.coils[address]
        tag = mapping.tag

        value = mapping.value(value)
        engine.write_tag(tag, value)

    def read_input(self, slave_id, function_code, address):
        
        engine = TagEngine()
        
        if function_code == 1:
            mapping = self.coils[address]
        elif function_code == 2:
            mapping = self.discrete[address]

        tag = mapping.tag

        value = engine.read_tag(tag)

        return mapping.coil(value)

    def setup_bindings(self):

        hr_addresses = list(range(len(self.holding_registers)))
        ir_addresses = list(range(len(self.input_registers)))
        coil_addresses = list(range(len(self.coils)))
        discrete_addresses = list(range(len(self.discrete)))

        if hr_addresses:
            router = self.app.route(slave_ids=[1], function_codes=[6, 16], addresses=hr_addresses)
            f = self.write_register
            router(f)
        
        if ir_addresses:
            router = self.app.route(slave_ids=[1], function_codes=[3, 4], addresses=ir_addresses)
            f = self.read_register
            router(f)
        
        if coil_addresses:
            router = self.app.route(slave_ids=[1], function_codes=[5, 15], addresses=coil_addresses)
            f = self.write_coil
            router(f)

        if discrete_addresses:
            router = self.app.route(slave_ids=[1], function_codes=[1, 2], addresses=discrete_addresses)
            f = self.read_input
            router(f)

    def setup_api(self):

        from rackio import Rackio

        app = Rackio()

        resource = MappingResource(self.serialize_mappings())
        app.add_route("/api/modbus/mappings", resource)
