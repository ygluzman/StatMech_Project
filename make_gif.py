import imageio

images = []

for i in range(1,10000):
    if i%100 == 1:
        if i == 1:
            print("Converting generated images to gif",flush=True,end='')
        else:
            print(".",flush=True,end='')

    image_path = "./generated_images/polymer_" + str(i) + ".jpg" 
    # print(image_path)
    try:
        images.append(imageio.imread(image_path))
    except FileNotFoundError:
        break

print("")
print("Saving...")
imageio.mimsave('generated_gif.gif', images)
print("Done!")