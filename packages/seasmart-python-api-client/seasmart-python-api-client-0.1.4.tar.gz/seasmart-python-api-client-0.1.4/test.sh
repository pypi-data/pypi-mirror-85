#!/bin/bash
coverage run -m --source='.' pytest
coverage report --fail-under=72
