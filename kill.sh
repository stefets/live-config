#!/bin/bash

echo "Stoping mpg123..."
kill -9 $(pgrep mpg123) 2>/dev/null
echo "Stoping aplaymidi..."
kill -9 $(pgrep aplaymidi) 2>/dev/null
