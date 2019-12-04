PolySim is a software created for the Monte Carlo simulation of 2D polymers. The software supports two algorithms to accomplish this: reptation and pivot. These algorithms were taken from the following papers:

[1] F.T. Wall and and F. Mandel, J. Chem. Phys. 63, 4592 (1975).
[2] M. Lal, Mol. Phys. 17, 57 (1969).

To use PolySim, simply download the software and edit the bottom of "master_script.py":

"""
    #Define output directory:
    output_directory = "test_output"

    #Settings:
    move_type = 'reptation'
    n_moves = 100
    length_poly = 50
    lamellar = True
    temp = 50
    field_strength = 1
    n_sims = 5

    #Generate a gif? Takes 2-3 minutes more in execution
    generate_gif = False
"""

These variables will determine the nature of the simulation. Most are self explanatory:

"""
    move_type -- pivot or reptation
    n_moves -- number of moves in simulation
    length_poly -- number of monomers in the polymer
    generate_gif -- generate images of each step and make a gif at the end of execution (takes a while)
    lamellar -- boolean, lamellar field on or off
    temp -- temperature, only if lamellar is on
    field -- field strength, if lamellar is turned on
    output_directory -- where you would like to output the run
    n_sims -- how many simulations to run in total
"""

A folder will be created in the directory in which master_script.py is run (python master_script.py). The software will create $n_sims separate subfolders for each simulation, creating outputs (graphs and summary) in each folder. Observables are found by averaging the last $n_moves//2 points in a simulation. 

** 
Note that this means all simulations should be conducted over at least twice the number of moves it takes to converge.
** 

You can check for convergence by looking at the plots of end to end length and radius of gyration in the output file. You When running multiple simulations, the results of all simulations are averaged in order to provide error bars on calculated quantities.

If you wish to generate a gif, you will need the "imagemagick" shell command. If you have this, you can simply set generate_gif to "True", and the program will generate images in the "generated_images" output folder and will run a imagemagick shell command at the end of the simulation to create a gif. Take note to not generate gifs of simulations >~ 1000 images, as this will take quite a lot of time.

Have fun!

-Daniel, Yogev, Caini, Abhishek, and Peter


