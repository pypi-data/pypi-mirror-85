import setuptools
from pathlib import Path

setuptools.setup(
    name='bullet_ur_gym_test',
    author="juhwakKim",
    author_email="juhk1017@naver.com",
    version='0.0.5',
    description="An OpenAI Gym Env for UR",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/juhk1017/gym-panda",
    packages=setuptools.find_packages(exclude = []),
    install_requires=['gym', 'pybullet', 'numpy'],  # And any other dependencies foo needs
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6'
)