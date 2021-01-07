microbit-bt-accelerometer
=========================

This is micro:bit part. It uses micro:bit ["offline toolchain"](https://lancaster-university.github.io/microbit-docs/offline-toolchains/).


How to build
------------

1. Make Python venv, install yotta:
    ```
    python -m venv pyenv
    source pyenv/bin/activate
    pip install yotta
    ```

2. Get ARM cross-compiling toolchain: `apt-get install gcc-arm-none-eabi` or fetch them from [ARM download site](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads).

3. Set up paths to cross-compiler and libs if you installed them in some random dir:
    ```
    export PATH=${PATH}:/somewhere/gcc-arm-none-eabi-5_4-2016q3/bin
    export LD_LIBRARY_PATH=/somewhere/gcc-arm-none-eabi-5_4-2016q3/lib/
    ```

4. Set cross-compiling target:
    ```
    yt target bbc-microbit-classic-gcc
    ```

5. Build the thing
    ```
    yt build
    ```

6. Upload the result to your micro:bit:
    ```
    cp build/bbc-microbit-classic-gcc/src/microbit-bt-accelerometer /mnt/MICROBIT/
    ```
