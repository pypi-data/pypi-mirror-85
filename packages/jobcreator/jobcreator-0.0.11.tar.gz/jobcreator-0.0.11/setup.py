import os

from setuptools import find_packages, setup
import versioneer

install_requires = [
    line.rstrip()
    for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
]

setup(
    name="jobcreator",
    install_requires=install_requires,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CLI for setting up and running slurm jobs",
    url="https://github.com/donatolab/jobcreator",
    license="GPL",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "jobcreator=jobcreator.__main__:main",
            "jobcreator-desktop=jobcreator.__main__:desktop_runner",
            "suite2p_runner=jobcreator._pipeline_runners.suite2p.suite2p_runner:main",
            "caiman_runner=jobcreator._pipeline_runners.caiman.caiman_runner:main",
            "caiman_mcorr_runner=jobcreator._pipeline_runners.caiman.caiman_mcorr:main",
        ]
    },
    zip_safe=False,
)
