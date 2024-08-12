
class RedisParser:

    def parse(self, data: str):
        type_identifier = data[0]
        
        if type_identifier=="+":
            return self.parse_simple_str(data)
        elif type_identifier=="$":
            return self.parse_bulk_str(data)
        elif type_identifier=="*":
            return self.parse_array_str(data)
        else:
            raise ValueError(f"Unable to parse. Type not supported for char {type_identifier}")
    

    def parse_simple_str(self, data: str):
        suffix = "\r\n"
        end_index = data.find(suffix)
        if end_index!=-1:
            return data[1:end_index], end_index+2
        else:
            raise TypeError("Unrecognized data type")
    

    def parse_bulk_str(self, data: str):
        sep_index = data.find("\r\n")
        str_length = int(data[1:sep_index])
        start = sep_index + 2
        end = start + str_length
        return data[start:end], end+2
    
    def parse_array_str(self, data: str):
        sep_index = data.find("\r\n")
        num_of_elements = int(data[1:sep_index])
        start_index = sep_index+2
        out = []
        for i in range(num_of_elements):
            element, next_index = self.parse(data[start_index:])
            start_index = start_index+next_index
            out.append(element)
        return out, start_index
            
       
    
