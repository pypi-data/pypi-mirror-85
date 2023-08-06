# pytest-multilog
A pytest plugin to persist logs from parallel test processes (and other helpers)

## Usage
To use the multilog feature, a test class just needs to inherit from the **`TestHelper`** class:

```python
from pytest_multilog import TestHelper

class TestCustom(TestHelper):
    def test_custom(self):
        # Custom test implementation
        ...
```

The **`TestHelper`** class declares a **`logs`** fixture which will be automatically used by its children classes.

## Behavior and attributes

### Root folder
The **`TestHelper`** class provides a **`root_folder`** property, matching with the **pytest** root folder.

### Output folder
The **`TestHelper`** class provides a **`output_folder`** property, where all files will be written. It's set to **`output_folder / "out" / "tests"`**

### Test name
Each test is associated to a name (provided in **`TestHelper.test_name`**), computed from the file name, the class name and the method name.

E.g. for the snippet above, if stored in a **`test_custom.py`** file, the test name will be: **test_custom_TestCustom_test_custom**.

### Current worker
In multi-process environment (**pytest** was invoked with **-n X** argument), the current worker name is provided in **`TestHelper.worker`** attribute.
It's set to **"master"** in single-process environment.

The class also provides a **`TestHelper.worker_index`** attribute, giving the working index as an integer value (will be set to 0 for **"master"**).

### Test folder
Test logs will be written in a **pytest.log** file (path provided in **`TestHelper.test_logs`**), stored in each test folder (provided in **`TestHelper.test_folder`** attribute):
* While the test is running, it's set to **`TestHelper.output_root / "__running__" / TestHelper.worker / TestHelper.test_name`**
* Once the test is terminated, the folder is moved directly under the output root one.

It means that during the test execution, it's possible to check which test is running on which worker 
(easing troubleshooting situations where a given worker is blocked)

### Checking logs
It is possible to verify if some strings are present in the current test log, by using the **`TestHelper.check_logs`** method.
It takes as input argument:
* either a simple string
* or a list of strings

The method will assert if all input strings are found in the log.
