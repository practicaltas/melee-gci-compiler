"""compile_ucf.py: compile NTSC and PAL gci files for UCF.
Usage: python compile_ucf.py"""

import os
commands = ["python melee_gci_compiler.py -o ucf0.84/ucf0.84ntsc.gci ucf0.84/ucf0.84ntsc.mgc",
			"python melee_gci_compiler.py -o ucf0.84/ucf0.84ntscfrozenstadium.gci ucf0.84/ucf0.84ntscfrozenstadium.mgc",
			"python melee_gci_compiler.py --pal -o ucf0.84/ucf0.84pal.gci ucf0.84/ucf0.84pal.mgc",
			"python melee_gci_compiler.py --pal -o ucf0.84/ucf0.84palfrozenstadium.gci ucf0.84/ucf0.84palfrozenstadium.mgc"]

for command in commands:
	os.system(command)
