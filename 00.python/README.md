# Python Documentation
https://docs.python.org/3.13/tutorial/datastructures.html

# Python?
- dynamically typed
- intepreted language
- object oriented

# Python Ecosystems
Data Science: pandas, numpy, scikit-learn
Web: Django, Flask
DevOps: Ansible, Fabric
AI/ML: TensorFlow, PyTorch

# Special methods in Python class
__init__ : Constructor
__str__: User-Friendly String Representation. print(obj) invokes __str__()
__repr__: Developer-Friendly Representation print(repr(p))  # Person(name='Alice', age=30)
__del__: Destructor (e.g. del obj)


# for vs while
"for" is easy to use on iteratable objects like list, string, tuple, and range.

# What is the difference between *args and **kwargs?
*args - used for positional arguments
```python
def func(*args):
    print(args)

func(1, 2, 3)
# Output: (1, 2, 3)
```

**kwargs - Stands for "keyword arguments" (arbitrary named arguments).
```python
def func(**kwargs):
    print(kwargs)

func(a=1, b=2)
# Output: {'a': 1, 'b': 2}
```

# lamda function
lambda function is one-liner annonymous function in python
```python
f = lambda n : n ** 2
print(f(5)) 
```

# Installing Python and Jupyter Notebook
https://www.youtube.com/watch?v=uB9SNAhfFKE


# What are map(), filter(), and reduce()?

# What are __init__.py files used for?
It’s a file that makes a directory into a Python package. 

# canonical pattern __name__ == "__main__"
This is the only built-in condition for checking the execution context (main vs imported).

When a code file is executed directly (e.g. python file.py), python treats condition __name__ == "__main__" in file.py as the starting point. But when file.py is imported into another file, the condition is never executed.

This gives the python ability to unit test each file code.

# What are Python decorators and how do they work?
Decorators are functions that modify the behavior of another function or class without changing its source code. They are often used for logging, access control, caching, etc.

It takes another function as input, adds some functionality to it and returns the modified function. 

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")

```
```output
Something is happening before the function is called.
Hello, Alice!
Something is happening after the function is called.
```

# What is generator in Python and where it is used?
Generator in python is a special-type of iterator that allows you to yield values one at a time using the yield keyword, instead of returning them all at once like a normal function with return.

```python
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

counter = count_up_to(3)
print(next(counter))  # 1
print(next(counter))  # 2
print(next(counter))  # 3
# next(counter) would raise StopIteration
```
```python
for num in count_up_to(3):
    print(num)

```

Generator is usually used for streaming large file in a HTTP response.
```python (server)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def file_stream():
    with open("large_file.txt", "rb") as f:
        while chunk := f.read(4096):
            yield chunk

@app.get("/download")
def download_file():
    return StreamingResponse(file_stream(), media_type="application/octet-stream")


```

```javascript (client)
const fs = require("fs");
const axios = require("axios");

axios({
  method: "get",
  url: "http://localhost:8000/download",
  responseType: "stream"
}).then(response => {
  response.data.pipe(fs.createWriteStream("output.txt"));
});

```

# self vs cls
self refers to the instance/object. It is used to access the instance attributes.
```python
class MyClass:
    def __init__(self, value):
        self.value = value  # instance attribute

    def show(self):
        print(f"Instance value: {self.value}")

obj = MyClass(10)
obj.show()  # self refers to obj here

```

cls refers to the class (not the object). It is accessible from @classmethod
```python
class MyClass:
    count = 0  # class attribute

    def __init__(self):
        MyClass.count += 1

    @classmethod
    def get_count(cls):
        print(f"Number of instances created: {cls.count}")

a = MyClass()
b = MyClass()
MyClass.get_count()  # cls refers to MyClass here

```

# @classmethod vs @staticmethod and their practical use
@classmethod and @staticmethod are decorators that define methods inside a Python class, but they behave differently and serve distinct purposes.

@classmethod method receives the class itself as the first argument, conventionally named cls. It is often used to define factory and singleton pattern.

```python
class Person:
    species = "Homo sapiens"

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_fullname(cls, fullname):
        first_name = fullname.split()[0]
        return cls(first_name)  # calls __init__

    @classmethod
    def get_species(cls):
        return cls.species

p = Person.from_fullname("Alice Johnson")
print(p.name)          # Alice
print(Person.get_species())  # Homo sapiens

```

@staticmethod does not receive self or cls.
```python
class MathUtils:
    
    @staticmethod
    def add(x, y):
        return x + y

print(MathUtils.add(5, 3))  # 8

```

# Factory Pattern - Building LLMClient (that connects to Azure OpenAI, OpenAI, and HuggingFace)
```python - Base LLMClient
from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass

```

```python - LLMClients
class AzureOpenAIClient(LLMClient):
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        # Initialize Azure SDK client here

    def generate_text(self, prompt: str) -> str:
        # Call Azure OpenAI API
        return f"Azure OpenAI response for: {prompt}"


class OpenAIClient(LLMClient):
    def __init__(self, api_key):
        self.api_key = api_key
        # Initialize OpenAI SDK client here

    def generate_text(self, prompt: str) -> str:
        # Call OpenAI API
        return f"OpenAI response for: {prompt}"


class HuggingFaceClient(LLMClient):
    def __init__(self, model_name):
        self.model_name = model_name
        # Initialize HuggingFace client here

    def generate_text(self, prompt: str) -> str:
        # Call HuggingFace API or local model
        return f"HuggingFace response for: {prompt}"

```

```python Factory Class
class LLMFactory:
    @staticmethod
    def create_llm(provider: str, **kwargs) -> LLMClient:
        provider = provider.lower()
        if provider == "azure":
            return AzureOpenAIClient(kwargs.get("api_key"), kwargs.get("endpoint"))
        elif provider == "openai":
            return OpenAIClient(kwargs.get("api_key"))
        elif provider == "huggingface":
            return HuggingFaceClient(kwargs.get("model_name"))
        else:
            raise ValueError(f"Unknown provider: {provider}")

```

```python using Factory
llm = LLMFactory.create_llm("openai", api_key="my-openai-key")
print(llm.generate_text("Hello world!"))

llm2 = LLMFactory.create_llm("huggingface", model_name="gpt2")
print(llm2.generate_text("Hello world!"))

```

# Singleton Pattern (reading environment variables)
```python
import os

class EnvConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        # Load and cache environment variables here
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
        self.HF_TOKEN = os.getenv("HF_TOKEN")
        self.MODE = os.getenv("APP_MODE", "development")

```


