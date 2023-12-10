from ace.framework.telemetry import Telemetry, TelemetrySettings
from ace.util import get_system_resource_usage

CONSOLE_PROGRAMS = """
1. /usr/bin/figlet: A program that creates large text banners in various typefaces.
2. /usr/bin/toilet: A program that creates large banner-like text with various styles.
3. /usr/games/cowsay: A program that generates ASCII pictures of a cow with a message.
"""
ENVIRONMENT_CONSTANTS = {
    "environment.type": "digital",
    "environment.interface": "Operating System",
    "environment.os.distribution.name": "Debian",
    "environment.os.distribution.version": "12",
    "environment.os.shell": "bash",
    "environment.os.packages.console": CONSOLE_PROGRAMS,
}


class TelemetryEnvironment(Telemetry):
    @property
    def settings(self):
        return TelemetrySettings(
            name="telemetry_environment",
            label="Telemetry - Environment",
            namespaces={
                "environment.type": 0,
                "environment.interface": 0,
                "environment.os.distribution.name": 0,
                "environment.os.distribution.version": 0,
                "environment.os.shell": 0,
                "environment.os.packages.console": 0,
                "environment.os.resource_usage": 30,
            },
        )

    async def collect_data_sample(self, namespace):
        if namespace in ENVIRONMENT_CONSTANTS:
            return ENVIRONMENT_CONSTANTS[namespace]
        elif namespace == "environment.os.resource_usage":
            return get_system_resource_usage()
