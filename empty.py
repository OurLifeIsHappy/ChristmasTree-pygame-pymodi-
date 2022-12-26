
import modi

"""
Example script for the usage of mic module
Make sure you connect 1 mic module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    mic = bundle.mics[0]

    while True:
        print(f"Volume: {mic.volume} mic.frequency: {mic.frequency}")