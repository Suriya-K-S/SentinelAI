"""
SentinelAI
Screenshot Manager
"""

import os
from datetime import datetime

import mss


class ScreenshotManager:

    def __init__(self, folder="screenshots"):

        self.folder = folder

        os.makedirs(self.folder, exist_ok=True)

    # -------------------------------------------------

    def capture(self, prefix="capture"):

        """
        Capture the current screen.

        Returns:
            Path of saved image.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{prefix}_{timestamp}.png"

        filepath = os.path.join(
            self.folder,
            filename
        )

        with mss.mss() as sct:

            sct.shot(output=filepath)

        return filepath

    # -------------------------------------------------

    def capture_multiple(self, count=3):

        """
        Capture multiple screenshots.

        Returns:
            List of image paths.
        """

        files = []

        for i in range(count):

            files.append(

                self.capture(
                    prefix=f"capture_{i+1}"
                )

            )

        return files


# ---------------------------------------------------------

if __name__ == "__main__":

    manager = ScreenshotManager()

    image = manager.capture()

    print("Saved:", image)