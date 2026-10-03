from setuptools import find_packages, setup

package_name = 'smart_transport_hardware'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'ops9_driver = smart_transport_hardware.ops9_driver:main',
            'lower_driver = smart_transport_hardware.lower_driver:main',
        ],
    },
)
