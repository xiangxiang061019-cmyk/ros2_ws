from setuptools import setup

package_name = 'smart_transport_bringup'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/competition.launch.py',
            'launch/map.launch.py',
        ]),
        ('share/' + package_name + '/config', [
            'config/robot.yaml',
            'config/nav2_params.yaml',
        ]),
        ('share/' + package_name + '/rviz', [
            'rviz/competition_map.rviz',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
)
