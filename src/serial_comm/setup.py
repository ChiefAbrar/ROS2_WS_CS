from setuptools import setup

package_name = 'serial_comm'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[('share/serial_comm/launch', ['launch/system_launch.py'])],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='email@example.com',
    description='ROS2 Serial Communication with Arduino',
    license='MIT',
    entry_points={
        'console_scripts': [
            'user_input_node = serial_comm.user_input_node:main',
            'serial_node = serial_comm.serial_node:main',
            'logger_node = serial_comm.logger_node:main',
        ],
    },
)