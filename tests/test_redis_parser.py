
from app.parser import RedisParser

def test_redis_parser_parse_simple_str():
    data = "+OK\r\n"
    parser = RedisParser()

    parsed_data = parser.parse(data)

    assert parsed_data==("OK",len(data))

def test_redis_parser_parse_bulk_str():
    data = "$10\r\nheyheyheyy\r\n"
    parser = RedisParser()

    parsed_data = parser.parse(data)

    assert parsed_data == ("heyheyheyy",len(data))

def test_redis_parser_parse_arr_str():
    data = "*10\r\n" + "$3\r\nhey\r\n$2\r\nhi\r\n"*10

    parser = RedisParser()

    parsed_data = parser.parse(data)

    assert parsed_data[0] == ["hey", "hi"]*5