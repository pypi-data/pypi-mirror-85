import struct


def friendly_name_to_classname(name, *, check_plural=False, remove_plural=False):
    if check_plural and not name.endswith("s"):
        raise ValueError
    if remove_plural and name.endswith("s"):
        name = name[:-1]
    result = name.title().replace(" ", "")
    assert result and result[0].isalpha() and all(c.isalnum() for c in result)
    return result


def friendly_name_to_varname(name):
    result = name.lower().replace(" ", "_")
    assert result and result[0].isalpha() and all(c.isalnum() or c == "_" for c in result)
    return result


def read_exactly(f, size):
    remaining = size
    chunks = []
    while remaining > 0:
        data = f.read(remaining)
        if not data:
            raise Exception("Unexpected EOF")
        chunks.append(data)
        remaining -= len(data)
    return b''.join(chunks)


def read_section_header(f):
    data = read_exactly(f, 2)
    sec_id, sec_size = struct.unpack('<BB', data)
    if sec_size % 2 == 1:
        data += read_exactly(f, 3)
        sec_size, = struct.unpack_from('<I', data, 1)
    sec_size //= 2
    return sec_id, sec_size


def write_section_header(f, sec_id, sec_size):
    f.write(struct.pack("<B", sec_id))
    if sec_size > 127:
        f.write(struct.pack("<I", sec_size * 2 + 1))
    else:
        f.write(struct.pack("<B", sec_size * 2))


def parse_custom_type(field_type):
    fixed_size = 0
    is_list = field_type.startswith("List(")
    if is_list:
        assert field_type[-1] == ")"
        list_params = [s.strip() for s in field_type[5:-1].split(',')]
        field_type = list_params[0]
        fixed_size = list_params[1] if len(list_params) >= 2 else 0
    return field_type, is_list, fixed_size


class SectionScope:
    def __init__(self, file, section_id=None):
        self.file = file
        self.section_id = section_id
        self.size = None
        self.start_pos = None
        self.end_pos = None

    def __enter__(self):
        sec_id, self.size = read_section_header(self.file)
        if self.section_id is not None and sec_id != self.section_id:
            raise Exception(f'Invalid section id: {sec_id}')
        self.section_id = sec_id
        self.start_pos = self.file.tell()
        self.end_pos = self.start_pos + self.size
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None and self.file.tell() != self.end_pos:
            raise Exception('Inconsistent subsections size')
