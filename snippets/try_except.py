try:
   print(1 / 0)
except Exception as exc:
   print(exc)
"""Division by zero"""

try:
   import assad
except ImportError as exc:
   print(exc)
"""No module named asdasd"""
