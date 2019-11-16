#Import libraries
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import glob

#Import functions 
import imaging
from Pivot_algorithm import pivot
from radius_of_gyration import radius_gyration, radius_of_gyration
from lamilar import lamilar_test,generate_coblock_charges
from Reptation import reptation
from end_to_end import end_to_end
from initialization import init
import matplotlib.pyplot as plt
import shutil

img_number = 0
img_directory = "generated_images"

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
    move_numbers = np.linspace(0, array.shape[0], array.shape[0])
    plt.clf()
    plt.plot(move_numbers, array, 'o', markersize=0.5, color='black');
    plt.title(title)
    plt.savefig(output_directory + "/" + title + '.png')

def avg_std(array,n_points):
    last_points_array = array[-1:-n_points:-1]
    avg = np.mean(last_points_array)
    std_dev = last_points_array - avg
    std_dev = std_dev ** 2
    std_dev = np.mean(std_dev)
    std_dev = np.sqrt(std_dev)
    sem = std_dev/n_points
    return avg, std_dev, sem


def run(move_type,n_moves,length_poly,generate_gif=False,lamilar=False,temp=None,field=1,output_directory=None):
    """
    Runs a simulation with specified move type and number of moves

    Arguments:
    move_type -- pivot or reptation
    n_moves -- number of moves in simulation
    length_poly -- number of monomers in the polymer
    generate_gif -- generate images of each step and make a gif at the end of execution (takes a while)
    lamilar -- boolean, lamilar field on or off
    temp -- temperature, only if lamilar is on
    field -- field strength, if lamilar is turned on
    output_directory -- where you would like to output the run
    """

    if output_directory == None:
        print("Error! Output directory not specified. Exiting...")
        exit(1)

    #Check if move type is valid
    if move_type not in ['reptation','pivot']:
        print("Move type is not reptation or pivot... exiting")
        exit(1)

    if lamilar == True:
        if temp == None:
            print("Lamilar field requires a temperature. Please specify (temp = ...). Exiting...")
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
    end2ends = np.empty(0)

    if lamilar == True:
        charges = generate_coblock_charges(poly.shape[0])

    #Run algorithm:
    for i in range(0,n_moves+1):

        if lamilar == True:
            poly1 = poly

        if move_type == 'reptation':
            poly = reptation(poly)
        else: 
            poly = pivot(poly)

        #lamilar called with polymer1, polymer2, charges, temp, field=1
        if lamilar == True:
            poly2 = poly
            poly, energy = lamilar_test(poly1,poly2,charges,temp,field=field)

        #Calculate observables
        if lamilar != True:
            energy = 0

        gyradius = radius_of_gyration(poly)
        end2end = end_to_end(poly)

        #Append observables to array
        energies = np.append(energies,np.array([energy]))
        gyradii = np.append(gyradii,np.array([gyradius]))
        # print(gyradii)
        end2ends = np.append(end2ends,np.array([end2end]))
        # print(end2ends)

        #Save images only if requested
        if generate_gif == True:
            if lamilar == True:
                img = grid.plot_poly(poly,energy=energy,gyradius=np.round(gyradius,2),end2end=np.round(end2end,2),lamilar=True,charges=charges)
            else:
                img = grid.plot_poly(poly,energy=energy,gyradius=np.round(gyradius,2),end2end=np.round(end2end,2))
            save_img(img)


    #Debug
    # print(gyradii)
    # print(end2ends)

    #Generate plots of observables over the algorithm
    plot(energies,"Energy",output_directory)
    plot(gyradii,"Radius of Gyration",output_directory)
    plot(end2ends,"End to End Length",output_directory)

    #Calculate averages and standard deviations of observables from the last 500 moves
    #Edit later base off of observed equilibration time
    points_sampled = n_moves//2
    avg_energy, std_energy, sem_energy = avg_std(energies,points_sampled)
    avg_gyradius, std_gyradius, sem_gyradius = avg_std(gyradii,points_sampled)
    avg_end2end, std_end2end, sem_end2end = avg_std(end2ends,points_sampled)

    #Print mean and standard deviation to output file
    output_name = output_directory + "/output.txt"

    #Remove previous output if it exists
    try:
        os.remove(output_name)
    except FileNotFoundError:
        pass

    #Write to output file    
    with open(output_directory + "/output.txt", 'w+') as file:
        file.write("POLYSIM" + "\n")
        file.write("A Software by Abhishek, Daniel, Yogev, Peter, and Caini" + "\n")
        file.write("\n")

        file.write("SIMULATION ACHIEVED" + "\n")
        file.write("########################" + "\n")
        file.write("SETTINGS:" + "\n")
        file.write("Move type: " + move_type + "\n")
        file.write("Laminar field: ")
        if lamilar == True:
            file.write("ON" + "\n")
            file.write("Field Strength: " + str(field) + "\n")
        else:
            file.write("OFF" + "\n")

        file.write("Points Sampled: " + str(points_sampled) + "\n")
        file.write("########################" + "\n")
        file.write("Average energy: " + str(avg_energy) + "\n")
        file.write("Average radius of gyration: " + str(avg_gyradius) + "\n")
        file.write("Average end to end: " + str(avg_end2end) + "\n")
        file.write("########################" + "\n")
        file.write("Std deviation of energy: " + str(std_energy) + "\n")
        file.write("Std deviation of radius of gyration: " + str(std_gyradius) + "\n")
        file.write("Std deviation of end to end distance: " + str(std_end2end) + "\n")
        file.write("########################" + "\n")
        file.write("Std error of energy: " + str(sem_energy) + "\n")
        file.write("Std error of radius of gyration: " + str(sem_gyradius) + "\n")
        file.write("Std error of end to end distance: " + str(sem_end2end) + "\n")
        file.write("########################" + "\n")
        file.write("\n")

        file.write("NORMAL TERMINATION" + "\n")
        file.write("THANK YOU FOR USING OUR SOFTWARE" + "\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")

    #Generate gif with terminal command if requested
    #This will take a while if you have many images (~2-3 minutes for 1000 images)
    if generate_gif:
        print("Simualation done! Generating gif (this might take a while (2-3 minutes))...")
        make_gif(n_moves,output_directory)


def main():
    #Seed if you want
    # np.random.seed(34)

    ########################
    ###### IMPORTANT #######
    # USER MUST EDIT BELOW #
    ########################

    #Define output directory:
    output_directory = "pivot_laminar_1000"

    #Settings:
    move_type = 'pivot'
    n_moves = 1000
    length_poly = 250
    laminar = True
    temp = 10
    field_strength = 1

    #Generate a gif? Takes 2-3 minutes more on execution
    #Also takes a lot of time to generate images
    generate_gif = False

    #Note: Values in output are from sample of n_moves//2 points. Be sure to equilibrate at least over
    # twice the time it takes your system to equilibrate

    #####################
    # STOP EDITING HERE #
    #####################

    try:
        os.mkdir(output_directory)
    except FileExistsError:
        shutil.rmtree(output_directory)
        os.mkdir(output_directory)
        pass

    global img_directory
    img_directory = output_directory + "/generated_images"

    #run(move_type,n_moves,length_poly,generate_gif=False,lamilar=False,temp=None,field=1)
    run(move_type = move_type ,n_moves = n_moves, length_poly = length_poly, generate_gif = generate_gif, lamilar = laminar, temp = temp, field = field_strength, output_directory = output_directory)

if __name__ == "__main__":  
    main()





