# namedframes

Basic type annotation support for Pandas and Spark data frames.
The goal is to provide a convenient way to specify a name-to-type mapping.
The assurance that the columns conform to the types is left to the user, 
i.e. this provides *named* data frames, not *typed* data frames. 


## Installation

```bash
pip install namedframes
```

## Usage

```python
import pandas as pd
from namedframes import PandasNamedFrame

class InputDF(PandasNamedFrame):
    x: float

class OutputDF(InputDF):
    blah: bool


def transform(input_data: InputDF) -> OutputDF:
    return OutputDF(input_data.assign(blah = True))

input_df = InputDF(pd.DataFrame({"x": [1.1, 2.2]}))

output = transform(input_df)

isinstance(input_df, InputDF)
True

isinstance(output, OutputDF)
True
```

If a column is missing, a validation error occurs,

```python
OutputDF(input_df)

ValueError: missing columns: [('blah', <class 'bool'>)]
```