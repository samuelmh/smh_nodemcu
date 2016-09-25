#
# Author: Samuel M.H. <samuel.mh@gmail.com>
# Description:
#    Make-based utility to manage the project.
#    Idea taken from:
#     - http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

#
### MACROS
#

#Variables
# Local package to deploy
LIBRARY = 'smh_nodemcu'
# Path to the virtualenv directory.
VENVS_PATH = ~/projects/venvs


#Don't touch
PROJECT_PATH = $(abspath $(lastword $(MAKEFILE_LIST)/..))
VENV_PATH = $(VENVS_PATH)/$(LIBRARY)


#
### Autodocumenting thing, don't touch
#
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



#
### Install the project
#
install: ## Create a development environment (virtualenv).
	@echo "Create the environment in "$(VENV_PATH)
	@virtualenv -p /usr/bin/python2.7 $(VENV_PATH)
	@echo "Install requirements"
	@$(VENV_PATH)'/bin/pip' install -r $(PROJECT_PATH)'/deploy/requirements.txt'
	@echo "Create symbolic links"
	# Link to project
	@ln -s $(PROJECT_PATH) $(VENV_PATH)'/'
	# Link code to project library so it is in the PYTHONPATH
	@ln -s $(PROJECT_PATH)'/'$(LIBRARY) $(VENV_PATH)'/lib/python2.7/site-packages/'
	# Make the command nodemcu available
	@ln -s $(PROJECT_PATH)'/nodemcu.py' $(VENV_PATH)'/bin/nodemcu'
	@chmod +x $(VENV_PATH)'/bin/nodemcu'
	@echo "Done"



#
### Flash the board
#
flash-float-4mb: flash-float-4mb-v20160917  ## Flash the board with the latest custom firmware (float type)

flash-integer-4mb: flash-integer-4mb-v20160917  ## Flash the board with the lastest custom firmware (integer type)



flash-float-4mb-v20160917: ## Flash the board with the float firmware, version v20160917
	@python -m esptool --p /dev/ttyUSB0 write_flash 0x00000 bin/nodemcu_float_master_20160917-1140.bin 0x3fc000 bin/esp_init_data_default.bin -fm dio -fs 32m

flash-integer-4mb-v20160917: ## Flash the board with the integer firmware, version v20160917
	@python -m esptool --p /dev/ttyUSB0 write_flash 0x00000 bin/nodemcu_integer_master_20160917-1140.bin 0x3fc000 bin/esp_init_data_default.bin -fm dio -fs 32m
