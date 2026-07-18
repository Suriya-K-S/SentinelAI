"""
SentinelAI
Security Manager
"""

from security.alert_manager import AlertManager
from security.rules import SECURITY_RULES, AlertLevel


class SecurityManager:

    def __init__(self):

        self.alerts = AlertManager()

    # ------------------------------------------------

    def process_event(self, event_type, message):

        """
        Process an event and generate an alert based on
        the configured security rule.
        """

        level = SECURITY_RULES.get(event_type)

        if level is None:

            return self.alerts.info(
                "System",
                message
            )

        if level == AlertLevel.INFO:

            return self.alerts.info(
                event_type.value,
                message
            )

        elif level == AlertLevel.WARNING:

            return self.alerts.warning(
                event_type.value,
                message
            )

        elif level == AlertLevel.ALERT:

            return self.alerts.alert(
                event_type.value,
                message
            )

        elif level == AlertLevel.CRITICAL:

            return self.alerts.critical(
                event_type.value,
                message
            )

        else:

            return self.alerts.info(
                event_type.value,
                message
            )