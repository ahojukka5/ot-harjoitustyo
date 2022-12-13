"""Saehaekkae is a program to help reduce user's energy bill.

In a variable-price electricity contract, the user can save on the total price
of energy by scheduling the use of electricity for favorable periods. Saehaekkae
tackles this problem basically from two different starting points.

1) by scheduling the use of the devices either automatically (for example with
   various wifi relays) or by receiving a message about the favorable usage time
   to a smart device

2) by understanding your own electricity consumption over time by visually
   looking at graphs and calculating certain key figures (how well did I manage
   to optimize?)
"""

# pylint: skip-file

# A very justified reason for using the pylint disable command is that this way
# the user can more easily import the functions of the package.

from record import Record
from database import Database
from utils import get_cheapest_hour
