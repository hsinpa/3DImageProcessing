import matplotlib.pyplot as plt
import numpy as np


class ImageUtility:


    def sample_images(self, generator, z_dim, image_grid_rows=4, image_grid_columns=4):
        # Sample random noise
        z = np.random.normal(0, 1, (image_grid_rows * image_grid_columns, z_dim))

        # Generate images from random noise
        gen_imgs = generator.predict(z)

        # Rescale image pixel values to [0, 1]
        gen_imgs = 0.5 * gen_imgs + 0.5

        # Set image grid
        fig, axs = plt.subplots(image_grid_rows,
                                image_grid_columns,
                                figsize=(4, 4),
                                sharey=True,
                                sharex=True)

        cnt = 0
        for i in range(image_grid_rows):
            for j in range(image_grid_columns):
                # Output a grid of images
                axs[i, j].imshow(gen_imgs[cnt, :, :, 0])
                axs[i, j].axis('off')
                cnt += 1
        plt.show()