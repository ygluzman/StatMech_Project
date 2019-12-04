#Import python libraries
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import shutil

#Import functions we made
import imaging
from Pivot_algorithm import pivot
from Reptation import reptation
from lamellar import lamellar_test, generate_coblock_charges
from misc import end_to_end, radius_of_gyration, init

#Global variables
img_number = 0
img_directory = "generated_images"

avg_energy = 0
avg_gyradius = 0
avg_gyradius_x = 0
avg_gyradius_y = 0
avg_end2end = 0
avg_end2end_x = 0
avg_end2end_y = 0

def save_img(img):
    """
    Saves image to "generated_images" directory
    Keeps track of how many images you have generated to label them differently
    """
    global img_number
    global img_directory
    img_number += 1
    img.save(img_directory + "/polymer_" + str(img_number) + ".jpg")
    
def make_gif(n_moves,output_directory):
    """
    Makes gif from images in 'generated_images' with imagemagick in command line
    You will need to first install imagemagick; see online for details
    """
    cmd = 'convert -resize 20% -delay 4 -loop 0 ' + img_directory + '/polymer_{1..' + str(n_moves+1) + '}.jpg ' + output_directory + '/generated_gif.gif'
    os.system(cmd)

def prepare_gif_process():
    """
    Creates some directories for gif generation and cleans up from the previous run
    """
    global img_directory
    try:
        os.mkdir(img_directory)
    except FileExistsError:
        #Clears all previous images
        for image in glob.glob(img_directory + "/*"):
            os.remove(image)
        pass

def plot(array,title,output_directory):
    """
    Makes a plot of the values of a 1D numpy array and saves with given title in output directory
    """
    move_numbers = np.linspace(0, array.shape[0], array.shape[0])
    plt.clf()
    plt.plot(move_numbers, array, 'o', markersize=0.5, color='black');
    plt.title(title)
    plt.savefig(output_directory + "/" + title + '.png')

def avg_std(array,n_points):
    """
    Takes avg, std. dev., and std. error of mean over the last n points
    """
    last_points_array = array[-1:-n_points:-1]
    avg = np.mean(last_points_array)
    std_dev = last_points_array - avg
    std_dev = std_dev ** 2
    std_dev = np.mean(std_dev)
    std_dev = np.sqrt(std_dev)
    sem = std_dev/np.sqrt(n_points)
    return avg, std_dev, sem


def run(move_type,n_moves,length_poly,generate_gif=False,lamellar=False,temp=None,field=1,output_directory=None):
    """
    Runs a simulation with specified move type and number of moves

    Arguments:
    move_type -- pivot or reptation
    n_moves -- number of moves in simulation
    length_poly -- number of monomers in the polymer
    generate_gif -- generate images of each step and make a gif at the end of execution (takes a while)
    lamellar -- boolean, lamellar field on or off
    temp -- temperature, only if lamellar is on
    field -- field strength, if lamellar is turned on
    output_directory -- where you would like to output the run
    """

    #Declaring global variables for multi-runs:
    global avg_energy
    global avg_gyradius
    global avg_gyradius_x
    global avg_gyradius_y
    global avg_end2end
    global avg_end2end_x
    global avg_end2end_y

    ######################
    ### Initialization ###
    ######################

    if output_directory == None:
        print("Error! Output directory not specified. Exiting...")
        exit(1)

    #Check if move type is valid
    if move_type not in ['reptation','pivot']:
        print("Move type is not reptation or pivot... exiting")
        exit(1)

    if lamellar == True:
        if temp == None:
            print("lamellar field requires a temperature. Please specify (temp = ...). Exiting...")
            exit(1)

    #Prepare gif process
    if generate_gif == True:
        prepare_gif_process()

    #Initialize polymer and grid
    poly = init(length_poly)

    if generate_gif == True:
        grid = imaging.grid(poly)

    #Initialize arrays to store energy, gyradius and end2end distance
    energies = np.empty(0)

    gyradii = np.empty(0)
    gyradii_x = np.empty(0)
    gyradii_y = np.empty(0)

    end2ends = np.empty(0)
    end2ends_x = np.empty(0)
    end2ends_y = np.empty(0)

    if lamellar == True:
        charges = generate_coblock_charges(poly.shape[0])


    ########################
    #### Run Simulation ####
    ########################

    #Run algorithm:
    for i in range(0,n_moves+1):

        #Write original polymer to memory if lamellar is on:
        if lamellar == True:
            poly1 = poly

        #Make a move:
        if move_type == 'reptation':
            poly = reptation(poly)
        else: 
            poly = pivot(poly)

        #If lamellar is on, compare energies of original and moved polymers:
        if lamellar == True:
            poly2 = poly
            poly, energy = lamellar_test(poly1,poly2,charges,temp,field=field)

        #Calculate observables
        if lamellar != True:
            energy = 0

        gyradius,gyradius_x,gyradius_y = radius_of_gyration(poly)
        end2end,end2end_x,end2end_y = end_to_end(poly)

        #Append observables to arrays
        energies = np.append(energies,np.array([energy]))

        gyradii = np.append(gyradii,np.array([gyradius]))
        gyradii_x = np.append(gyradii_x,np.array([gyradius_x]))
        gyradii_y = np.append(gyradii_y,np.array([gyradius_y]))

        end2ends = np.append(end2ends,np.array([end2end]))
        end2ends_x = np.append(end2ends_x,np.array([end2end_x]))
        end2ends_y = np.append(end2ends_y,np.array([end2end_y]))

        #Save images for gif upon request
        if generate_gif == True:
            if lamellar == True:
                img = grid.plot_poly(poly,energy=energy,gyradius=np.round(gyradius,2),end2end=np.round(end2end,2),lamellar=True,charges=charges)
            else:
                img = grid.plot_poly(poly,energy=energy,gyradius=np.round(gyradius,2),end2end=np.round(end2end,2))
            save_img(img)

    #########################################
    #### Plot and Calculate Observables  ####
    #########################################

    #Generate plots of observables over the algorithm
    plot(energies,"Energy",output_directory)

    plot(gyradii,"Radius of Gyration",output_directory)
    plot(gyradii_x,"Radius of Gyration x",output_directory)
    plot(gyradii_y,"Radius of Gyration y",output_directory)

    plot(end2ends,"End to End Length",output_directory)
    plot(end2ends_x,"End to End Length x",output_directory)
    plot(end2ends_y,"End to End Length y",output_directory)

    #Calculate avg, std. dev., and sem of observables over the last n/2 points
    points_sampled = n_moves//2
    avg_energy, std_energy, sem_energy = avg_std(energies,points_sampled)

    avg_gyradius, std_gyradius, sem_gyradius = avg_std(gyradii,points_sampled)
    avg_gyradius_x, std_gyradius_x, sem_gyradius_x = avg_std(gyradii_x,points_sampled)
    avg_gyradius_y, std_gyradius_y, sem_gyradius_y = avg_std(gyradii_y,points_sampled)

    avg_end2end, std_end2end, sem_end2end = avg_std(end2ends,points_sampled)
    avg_end2end_x, std_end2end_x, sem_end2end_x = avg_std(end2ends_x,points_sampled)
    avg_end2end_y, std_end2end_y, sem_end2end_y = avg_std(end2ends_y,points_sampled)

    ###########################
    #### Write Output File ####
    ###########################

    output_name = output_directory + "/output.txt"

    #Remove previous output if it exists
    try:
        os.remove(output_name)
    except FileNotFoundError:
        pass

    #Write output file:    
    with open(output_directory + "/output.txt", 'w+') as file:
        file.write("POLYSIM" + "\n")
        file.write("A Software by Abhishek, Daniel, Yogev, Peter, and Caini" + "\n")
        file.write("\n")

        file.write("SIMULATION ACHIEVED" + "\n")
        file.write("########################" + "\n")
        file.write("SETTINGS:" + "\n")
        file.write("Move type: " + move_type + "\n")
        file.write("Lamellar field: ")
        if lamellar == True:
            file.write("ON" + "\n")
            file.write("Field Strength: " + str(field) + "\n")
        else:
            file.write("OFF" + "\n")
        if lamellar == True:
            file.write("Temperature: " + str(temp) + "\n")

        file.write("Length of Polymer: " + str(length_poly) + "\n")
        file.write("Moves in Simualation: " + str(n_moves) + "\n")
        file.write("Points Sampled: " + str(points_sampled) + "\n")

        file.write("########################" + "\n")
        file.write("Average energy: " + str(avg_energy) + "\n")
        file.write("\n")
        file.write("Average radius of gyration: " + str(avg_gyradius) + "\n")
        file.write("Average radius of gyration x: " + str(avg_gyradius_x) + "\n")
        file.write("Average radius of gyration y: " + str(avg_gyradius_y) + "\n")
        file.write("\n")
        file.write("Average end to end: " + str(avg_end2end) + "\n")
        file.write("Average end to end x: " + str(avg_end2end_x) + "\n")
        file.write("Average end to end y: " + str(avg_end2end_y) + "\n")

        file.write("########################" + "\n")
        file.write("Std deviation of energy: " + str(std_energy) + "\n")
        file.write("\n")
        file.write("Std deviation of radius of gyration: " + str(std_gyradius) + "\n")
        file.write("Std deviation of radius of gyration x: " + str(std_gyradius_x) + "\n")
        file.write("Std deviation of radius of gyration y: " + str(std_gyradius_y) + "\n")
        file.write("\n")
        file.write("Std deviation of end to end distance: " + str(std_end2end) + "\n")
        file.write("Std deviation of end to end distance x: " + str(std_end2end_x) + "\n")
        file.write("Std deviation of end to end distance y: " + str(std_end2end_y) + "\n")

        file.write("########################" + "\n")
        file.write("Std error of energy: " + str(sem_energy) + "\n")
        file.write("\n")

        file.write("Std error of radius of gyration: " + str(sem_gyradius) + "\n")
        file.write("Std error of radius of gyration x: " + str(sem_gyradius_x) + "\n")
        file.write("Std error of radius of gyration y: " + str(sem_gyradius_y) + "\n")

        file.write("\n")
        file.write("Std error of end to end distance: " + str(sem_end2end) + "\n")
        file.write("Std error of end to end distance x: " + str(sem_end2end_x) + "\n")
        file.write("Std error of end to end distance y: " + str(sem_end2end_y) + "\n")
        file.write("########################" + "\n")
        file.write("\n")

        file.write("NORMAL TERMINATION" + "\n")
        file.write("THANK YOU FOR USING OUR SOFTWARE" + "\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")

    #######################
    #### Generate Gif  ####
    #######################

    if generate_gif:
        print("Simualation done! Generating gif (this might take a while (2-3 minutes))...")
        make_gif(n_moves,output_directory)

def multi_run(n_sims,move_type,n_moves,length_poly,generate_gif=False,lamellar=False,temp=None,field=1,output_directory=None):
    """
    Calls n_sims runs with variables specified in main, then groups results into summary text files.
    See "run" function for more details.
    """
    
    #Global variables to get from sims:
    energies = np.empty(0)
    gyradii = np.empty(0)
    gyradii_x = np.empty(0)
    gyradii_y = np.empty(0)
    end2ends = np.empty(0)
    end2ends_x = np.empty(0)
    end2ends_y = np.empty(0)

    global avg_energy
    global avg_gyradius
    global avg_gyradius_x
    global avg_gyradius_y
    global avg_end2end
    global avg_end2end_x
    global avg_end2end_y

    for i in range(1,n_sims+1):
        run_directory = output_directory + '/sim_' + str(i)
        os.mkdir(run_directory)

        run(move_type = move_type ,n_moves = n_moves, length_poly = length_poly, generate_gif = generate_gif, lamellar = lamellar,
         temp = temp, field = field, output_directory = run_directory)
        
        #Append outputs to arrays
        energies = np.append(energies,np.array([avg_energy]))
        gyradii = np.append(gyradii,np.array([avg_gyradius]))
        gyradii_x = np.append(gyradii_x,np.array([avg_gyradius_x]))
        gyradii_y = np.append(gyradii_y,np.array([avg_gyradius_y]))
        end2ends = np.append(end2ends,np.array([avg_end2end]))
        end2ends_x = np.append(end2ends_x,np.array([avg_end2end_x]))
        end2ends_y = np.append(end2ends_y,np.array([avg_end2end_y]))

    avg_energy, std_energy, sem_energy = avg_std(energies,len(energies))
    avg_gyradius, std_gyradius, sem_gyradius = avg_std(gyradii,len(energies))
    avg_gyradius_x, std_gyradius_x, sem_gyradius_x = avg_std(gyradii_x,len(energies))
    avg_gyradius_y, std_gyradius_y, sem_gyradius_y = avg_std(gyradii_y,len(energies))
    avg_end2end, std_end2end, sem_end2end = avg_std(end2ends,len(energies))
    avg_end2end_x, std_end2end_x, sem_end2end_x = avg_std(end2ends_x,len(energies))
    avg_end2end_y, std_end2end_y, sem_end2end_y = avg_std(end2ends_y,len(energies))

    with open(output_directory + "/output.txt", 'w+') as file:
        file.write("POLYSIM" + "\n")
        file.write("A Software by Abhishek, Daniel, Yogev, Peter, and Caini" + "\n")
        file.write("\n")

        file.write(str(n_sims) + " SIMULATIONS ACHIEVED" + "\n")
        file.write("SETTINGS:" + "\n")
        file.write("########################" + "\n")
        file.write("Move type: " + move_type + "\n")
        file.write("Lamellar field: ")
        if lamellar == True:
            file.write("ON" + "\n")
            file.write("Field Strength: " + str(field) + "\n")
        else:
            file.write("OFF" + "\n")
        if lamellar == True:
            file.write("Temperature: " + str(temp) + "\n")

        file.write("Length of Polymer: " + str(length_poly) + "\n")

        file.write("Moves in Each Simualation: " + str(n_moves) + "\n")
        file.write("Points Sampled in Each Simulation: " + str(len(energies)) + "\n")
        file.write("\n")

        file.write("Average values over " + str(n_sims) + " simulations" + ":\n")
        file.write("########################" + "\n")
        file.write("Average energy: " + str(avg_energy) + "\n")
        file.write("\n")
        file.write("Average radius of gyration: " + str(avg_gyradius) + "\n")
        file.write("Average radius of gyration x: " + str(avg_gyradius_x) + "\n")
        file.write("Average radius of gyration y: " + str(avg_gyradius_y) + "\n")
        file.write("\n")
        file.write("Average end to end: " + str(avg_end2end) + "\n")
        file.write("Average end to end x: " + str(avg_end2end_x) + "\n")
        file.write("Average end to end y: " + str(avg_end2end_y) + "\n")

        file.write("\n")
        file.write("Standard error over " + str(n_sims) + " simulations" + ":\n")
        file.write("########################" + "\n")
        file.write("Std error of energy: " + str(sem_energy) + "\n")
        file.write("\n")

        file.write("Std error of radius of gyration: " + str(sem_gyradius) + "\n")
        file.write("Std error of radius of gyration x: " + str(sem_gyradius_x) + "\n")
        file.write("Std error of radius of gyration y: " + str(sem_gyradius_y) + "\n")

        file.write("\n")
        file.write("Std error of end to end distance: " + str(sem_end2end) + "\n")
        file.write("Std error of end to end distance x: " + str(sem_end2end_x) + "\n")
        file.write("Std error of end to end distance y: " + str(sem_end2end_y) + "\n")
        file.write("########################" + "\n")
        file.write("\n")

        file.write("NORMAL TERMINATION" + "\n")
        file.write("THANK YOU FOR USING OUR SOFTWARE!" + "\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")

def main():
    """
    Runs a simulation with user-specified settings below
    Values in output are taken over the last n_moves//2 points, so be sure to equilibrate at least
    over twice the time it takes your system to equilibrate
    """

    ########################
    ###### IMPORTANT #######
    # USER MUST EDIT BELOW #
    ########################

    #Define output directory:
    output_directory = "test_output"

    #Settings:
    move_type = 'pivot'
    n_moves = 100
    length_poly = 10000
    lamellar = False
    temp = 50
    field_strength = 1
    n_sims = 5

    #Generate a gif? Takes 2-3 minutes more in execution
    generate_gif = False

    #####################
    # STOP EDITING HERE #
    #####################

    #Remove previous directory of the same name if it exists
    try:
        os.mkdir(output_directory)
    except FileExistsError:
        shutil.rmtree(output_directory)
        os.mkdir(output_directory)
        pass

    #Set output directory for images
    global img_directory
    img_directory = output_directory + "/generated_images"

    #Execute the run
    multi_run(n_sims = n_sims, move_type = move_type ,n_moves = n_moves, length_poly = length_poly, generate_gif = generate_gif, lamellar = lamellar,
         temp = temp, field = field_strength, output_directory = output_directory)


if __name__ == "__main__":  
    main()





