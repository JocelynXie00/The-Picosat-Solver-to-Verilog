import os
'''
for i in range(1,33):
	instruction = "python3 solver.py ex4.v " + str(i) + " 00000000000000000000000010000000" 
	print(f"iteration {i}:")
	os.system(instruction)
'''
for i in range(32):

	instruction = "python3 solver.py stoplight2.v 17 " + format(i, "05b") 
	print("target state:", format(i, "05b") )
	os.system(instruction)

