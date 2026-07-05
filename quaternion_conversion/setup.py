from setuptools import setup, find_packages

package_name = 'quaternion_conversion'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robotics Portfolio Maintainers',
    maintainer_email='maintainers@example.com',
    description='ROS 2 services for quaternion conversions.',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'quaternion_services = quaternion_conversion.quaternion_service_node:main',
        ],
    },
)
