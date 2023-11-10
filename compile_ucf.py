"""compile_ucf.py: compile NTSC and PAL gci files for UCF.
Usage: python compile_ucf.py"""

import datetime
import os

release_date = datetime.date.today().isoformat()

commands = ["python melee_gci_compiler.py -o ucf0.84/ucf0.84ntsc_" + release_date + ".gci ucf0.84/ucf0.84ntsc.mgc",
			"python melee_gci_compiler.py -o ucf0.84/ucf0.84ntscfrozenstadium_" + release_date + ".gci ucf0.84/ucf0.84ntscfrozenstadium.mgc",
			"python melee_gci_compiler.py --pal -o ucf0.84/ucf0.84pal_" + release_date + ".gci ucf0.84/ucf0.84pal.mgc",
			"python melee_gci_compiler.py --pal -o ucf0.84/ucf0.84palfrozenstadium_" + release_date + ".gci ucf0.84/ucf0.84palfrozenstadium.mgc"]

for command in commands:
	os.system(command)
