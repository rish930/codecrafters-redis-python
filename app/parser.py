
class RedisParser:

    def parse(self, data: bytes):
        data_str = data.decode()
        type_identifier = data_str[0]
        
        if type_identifier=="+":
            return self.parse_simple_str(data)
        elif type_identifier=="$":
            return self.parse_bulk_str(data)
        elif type_identifier=="*":
            return self.parse_array_str(data)
        else:
            raise ValueError(f"Unable to parse. Type not supported for char {type_identifier}")
    

    def parse_simple_str(self, data: bytes):
        suffix = b"\r\n"
        end_index = data.find(suffix)
        if end_index!=-1:
            return data[1:end_index], end_index+2
        else:
            raise TypeError("Unrecognized data type")
    

    def parse_bulk_str(self, data: bytes):
        data_str = data.decode()
        str_length = int(data_str[1])
        start = data_str.find("\r\n") + 2
        end = start + str_length
        return data[start:end], end+2
    
    def parse_array_str(self, data: bytes):
        num_of_elements = int(data.decode()[1])
        start_index = 4
        out = []
        for i in range(num_of_elements):
            element, next_index = self.parse(data[start_index:])
            start_index = start_index+next_index
            out.append(element)
        return out, start_index
            
       
    
