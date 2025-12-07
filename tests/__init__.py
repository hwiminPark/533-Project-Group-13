import sys
from pathlib import Path

# Add project root so "from retire_plan import ..." works
sys.path.insert(0, str(Path(__file__).parent.parent))

# Print for debugging
print(f"Added to sys.path: {Path(__file__).parent.parent}")