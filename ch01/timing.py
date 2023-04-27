#!/usr/bin/env python3

import time

start_time = time.time()
for i in range(5):
    time.sleep(1)

print("--- %.5f seconds ---" % (time.time() - start_time))
