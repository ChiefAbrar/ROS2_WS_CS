from setuptools import setup

package_name = 'basic_comm'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='Basic publisher-subscriber demo for ROS2',
    license='MIT',
    entry_points={
        'console_scripts': [
            'talker = basic_comm.talker:main',
            'listener = basic_comm.listener:main',
        ],
    },
)