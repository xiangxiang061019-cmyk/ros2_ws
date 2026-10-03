from setuptools import find_packages, setup

package_name = 'smart_transport_perception'

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
            'qr_detector = smart_transport_perception.qr_detector_stub:main',
            'yolo_detector = smart_transport_perception.yolo_detector_stub:main',
            'radar_obstacle = smart_transport_perception.radar_obstacle_stub:main',
            'competition_landmarks = smart_transport_perception.competition_landmarks:main',
        ],
    },
)
