from setuptools import setup

setup(
    name="asl-pepper-2d-sim",
    description='Python library for Pepper 2d simulation',
    author='Daniel Dugas',
    version='0.0.3',
    py_modules=[
        'gymified_pepper_envs',
        'pepper_2d_simulator',
        'pepper_2d_iarlenv',
    ],
    packages=['asl_pepper_2d_sim_maps'],
    package_data={'asl_pepper_2d_sim_maps': ['maps/*']},
)
