import os
import time
from helpers import OutOfRangeError

class Reader:
    def __init__(self, file_path: str | os.PathLike, **kwargs) -> None:
        self.file_path = file_path
        self.contents: str = None
        
        self.make_logs = kwargs.get("make_logs", True)

        self.initialize()

    @property
    def file_exists(self) -> bool:
        return os.path.exists(self.file_path)
    
    @property
    def curr_length(self) -> int:
        return len(self.contents)

    def initialize(self) -> None:
        checks: dict[str, bool] = {
            'File exists': self.file_exists
        }
        status: list[int] = [0, 0]
        texts: tuple[str, str] = ('Failed', 'Passed')
        if self.make_logs:
            with open(f'run-{time.time()}', 'a') as f:
                for name, check in checks.items():
                    f.write(f'{name}: {texts[check]}\n')
                    status[check] += 1
                f.write(f'Passed {status[1]}/{sum(status)}') # Use sum(status) instead of len(checks) because O(1) is better than O(n)

            with open(self.file_path, 'r') as f:
                self.contents = "".join(f.readlines()).strip('\n ')
    
    def peek(self, position: int = 0) -> str | OutOfRangeError:
        if 0 <= position < self.curr_length:
            return self.contents[position]
        return OutOfRangeError(f"Requested position {position} is out of range for file {self.file_path} which has length {self.curr_length} (after consumption)")

    def consume(self, position: int = 0) -> str | OutOfRangeError:
        if 0 <= position < self.curr_length:
            copy = list(self.contents)
            popped_char = copy.pop(position)
            self.contents = "".join(copy)
            return popped_char
        return OutOfRangeError(f"Requested position {position} is out of range for file {self.file_path} which has length {self.curr_length} (after consumption)")

    @property
    def is_eof(self) -> bool:
        return self.curr_length == 0

    def first_instance_of(self, character: str) -> int:
        return self.contents.index(character)
