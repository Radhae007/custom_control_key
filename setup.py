from setuptools import setup
import os
from glob import glob

package_name = 'custom_control_key'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='radhae',
    maintainer_email='radhae@todo.todo',
    description='Robot control and lidar visualization package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={  
        'console_scripts': [
            'imu_node = custom_control_key.imu_node:main',
            'pose_integrator_node = custom_control_key.pose_integrator_node:main',
            'velocity_fusion_node = custom_control_key.velocity_fusion_node:main'
        ],
    },
)
