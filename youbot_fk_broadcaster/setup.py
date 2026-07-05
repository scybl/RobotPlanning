from setuptools import setup
import os

package_name = 'youbot_fk_broadcaster'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), ['launch/youbot_fk_broadcaster.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kpach',
    maintainer_email='kpach@todo.todo',
    description='YouBot forward-kinematics demo and TF broadcaster nodes.',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'youbot_fk_tf_broadcaster = youbot_fk_broadcaster.fk_tf_broadcaster_node:main',
        ],
    },
)
