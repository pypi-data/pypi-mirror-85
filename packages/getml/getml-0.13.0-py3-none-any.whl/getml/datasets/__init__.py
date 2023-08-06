"""
The :mod:`getml.datasets` module includes utilities to load datasets,
including methods to load and fetch popular reference datasets. It also
features some artificial data generators.
"""

from .samples_generator import _aggregate
from .samples_generator import make_categorical
from .samples_generator import make_discrete
from .samples_generator import make_numerical
from .samples_generator import make_same_units_categorical
from .samples_generator import make_same_units_numerical
from .samples_generator import make_snowflake

from .base import load_air_pollution
from .base import load_atherosclerosis
from .base import load_biodegradability
from .base import load_consumer_expenditures
from .base import load_interstate94
from .base import load_loans
from .base import load_occupancy
