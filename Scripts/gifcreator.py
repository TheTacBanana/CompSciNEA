import imageio

filenames = []

for i in range(6,500):
    filenames.append("GifFolder\\img{}.png".format(i))

with imageio.get_writer('GifFolder/final.gif', mode='I', duration = 0.0166666667) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)