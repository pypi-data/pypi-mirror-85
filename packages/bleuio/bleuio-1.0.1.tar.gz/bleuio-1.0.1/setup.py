from setuptools import find_packages, setup

setup(
    name='bleuio',
    version='1.0.1',
    packages=find_packages(include=['bleuio_lib']),
    url='https://smart-sensor-devices-ab.github.io/ssd005-manual/',
    install_requires=['pyserial'],
    python_requires='>=3.6',
    license='MIT',
    author='Smart Sensor Devices',
    author_email='smartzenzor@gmail.com',
    description='Library for using the bleuio dongle.'
)
