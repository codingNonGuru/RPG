import os
import sys

sys.path.append(os.path.dirname(__file__) + '/..')

import client

client.Client.Get().Start()