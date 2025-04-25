# Open-AML-Engine

An open Algebraic Machine Learning (AML) engine for building models and
performing inference. Designed for community-driven exploration and research in
AML.

The current version has been tested on Linux.

## Installation

### 1. Create a new Python environment (recommended)

### 2. Install dependencies:

- `cffi`
- `networkx` (only for `example03`)
- `matplotlib` (only for `example03`)

### 3. Compile C-extensions

``` bash
cd aml/aml_fast
python build_amlFastLibrary.py
```

### 4. Install AML library.

From the root folder, where `setup.py` is placed, run the following command:

``` bash
python -m pip install -e .
```

Note that the command ends with a dot.

### 5. Extra

If you plan to run example04_mnist.py you will need to obtain the MNIST dataset and place the files in `Examples/mnist_datasets` (the path can be modified in MNIST.py):

- t10k-images-idx3-ubyte
- t10k-labels-idx1-ubyte
- train-images-idx3-ubyte
- train-labels-idx1-ubyte

The dataset can be downloaded from [Yann Lecun MNIST](http://yann.lecun.com/exdb/mnist/) database or [Huggingface](https://huggingface.co/datasets/ylecun/mnist).

## How to cite

Work done with this engine should be cited with [Algebraic Machine Learning: Learning as computing an algebraic decomposition of a task](https://arxiv.org/abs/2502.19944).

## FAQ

### When using the library I get "Illegal instruction (core dumped)"

It is possible that AVX or SSE are not supported.
If that is the case, remove the following lines from `build_amlFastLibrary.py`.

``` py
"-msse2",
"-march=core-avx2",
```

-----


![EU Flag](./eu_flag.jpg | height=45px) This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 952091.
