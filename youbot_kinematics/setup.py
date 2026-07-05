from setuptools import setup, find_packages
import os

package_name = 'youbot_kinematics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['model.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tianchi',
    maintainer_email='mithrandir_chen@hotmail.com',
    description='YouBot forward kinematics and analytical Jacobian implementation.',
    license='TODO',
    entry_points={
    'console_scripts': [
        'youbot_kinematics_node = youbot_kinematics.youbot_kinematic_model:main',
    ],
},
)
