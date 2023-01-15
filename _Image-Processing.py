
#RGB Image #
class RGBImage:
    """
    This class creates a template of RBG color images with the following methods below:
    """

    def __init__(self, pixels):
        """
        This is a constructor that initializes an instance of an RGB image.
        It consists of the argument "pixels" which is a 3D list which is
        made up of a color channel, row and column.
        """
        self.pixels = pixels  # initialze the pixels list here

    def size(self):
        """
        This is a getter method that gives the size of an image as the number
        of rows and the number of columns.
        """
        for i in self.pixels:
            for j in i:
                return (len(i), len(j))

    def get_pixels(self):
        """
        This is a getter method that gives a deep copy of an image's pixel matrix
        """
        deep_copy_list = [[[l for l in y] for y in x] for x in self.pixels]
        return deep_copy_list

    def copy(self):
        """
        This method gives a copy of an RBGImage instance
        """
        return RGBImage(self.get_pixels())

    def get_pixel(self, row, col):
        """
        This is a getter method that returns the color of a pixel at a partical row and column.
        """
        if (isinstance(row, int))!= True and (isinstance(col, int)) != True:
            raise TypeError
        elif (0 <= row <= self.size()[0]) != True and (0 <= col <= self.size()[1]) !=True:
            raise ValueError
        else:
            return (self.pixels[0][row][col], self.pixels[1][row][col], self.pixels[2][row][col])


    def set_pixel(self, row, col, new_color):
        """
        This is a setter method that updates the color of a pixel
        at a particular location.
        """
        if (isinstance(row, int) and isinstance(col, int)) != True:
            raise TypeError
        if ((0 <= row <= self.size()[0]) and (0 <= col <= self.size()[1])) !=True:
            raise ValueError
        if new_color[0] >= 0:
            self.pixels[0][row][col] = new_color[0]
        if new_color[1] >= 0:
            self.pixels[1][row][col] = new_color[1]
        if new_color[2] >= 0:
            self.pixels[2][row][col] = new_color[2]


#Image Processing Methods #
class ImageProcessing:
    """
    This class processes images using the following methods below:
    """

    @staticmethod
    def negate(image):
        """
        This method gives you the negative image of an image.
        """
        processed_colors = image.get_pixels()
        return RGBImage(list(map(lambda x: list(map(lambda y: list(map(lambda z: 255 - z , y)), x)), processed_colors)))
    @staticmethod
    def tint(image, color):
        """
        This method tints a given image given a color.
        """
        processed_colors = image.get_pixels()
        first_channel = processed_colors[0]
        second_channel = processed_colors[1]
        third_channel = processed_colors[2]
        processed_colors[0] = list(map(lambda x: list(map(lambda y: (color[0] + y)//2, x)), first_channel))
        processed_colors[1] = list(map(lambda x: list(map(lambda y: (color[1] + y)//2, x)), second_channel))
        processed_colors[2] = list(map(lambda x: list(map(lambda y: (color[2] + y)//2, x)), third_channel))
        return RGBImage(processed_colors)

    @staticmethod
    def clear_channel(image, channel):
        """
        This method given a particular channel, clear it.
        """
        pixels = image.get_pixels()
        new_pixels = [[[0 for k in j] for j in pixels[i]] if i == channel else pixels[i] for i in range(len(pixels))]
        return RGBImage(new_pixels)

    @staticmethod
    def crop(image, tl_row, tl_col, target_size):
        """
        This method crops a given image.
        """
        pixels = image.get_pixels()
        red_channel = [i[tl_column:tl_column + target_size[1]] for i in pixels[0][tl_row:tl_row+target_size[0]]]
        blue_channel = [i[tl_column:tl_column + target_size[1]] for i in pixels[1][tl_row:tl_row+target_size[0]]]
        green_channel = [i[tl_column:tl_column + target_size[1]] for i in pixels[2][tl_row:tl_row+target_size[0]]]
        cropped_lst = [red_channel, blue_channel, green_channel]
        return RGBImage(cropped_lst)


    @staticmethod
    def chroma_key(chroma_image, background_image, color):
        """
        This method replaces all the pixels of a given color of an image with given color of a
        background image at that location.
        """
        if not isinstance(chroma_image, RGBImage) or not isinstance(background_image, RGBImage):
            raise TypeError
        if chroma_image.size() != background_image.size():
            raise ValueError
        count = 0
        for i in range(len(chroma_image.get_pixels()[0])):
            for j in range(len(chroma_image.get_pixels()[0][i])):
                if chroma_image.get_pixel(i, j) == color:
                    background_new_color = background_image.get_pixel(i, j)
                    chroma_image.set_pixel(i, j, background_new_color)
                    count += 1
        if count == 0:
            return chroma_image.copy()
        else:
            return RGBImage(chroma_image)

    # rotate_180 
    @staticmethod
    def rotate_180(image):
        """
        Rotates a picture by 180 degrees
        """
        pixels = image.get_pixels()
        pixels[0] = [i[::-1] for i in pixels[0]]
        pixels[1] = [i[::-1] for i in pixels[1]]
        pixels[2] = [i[::-1] for i in pixels[2]]
        pixels[0] = pixels[0][::-1]
        pixels[1] = pixels[1][::-1]
        pixels[2] = pixels[2][::-1]
        return RGBImage(pixels)

#Image KNN Classifier #
class ImageKNNClassifier:
    """
    This class predicts the label of a particular image using K-nearest-neighbors using the following methods:
    """

    def __init__(self, n_neighbors):
        """
        This constructor an instance of a ImageKNNClassifier.
        """
        self.n_neighbors = n_neighbors
        self.data = []

    def fit(self, data):
        """
        This method stores training data in a classifier instance to fit the classifier.
        """
        if len(data) <= self.n_neighbors:
            raise ValueError
        elif len(self.data) > 0:
            raise ValueError
        else:
            self.data = data


    @staticmethod
    def distance(image1, image2):
        """
        This method calculates the distance between two images.
        """
        if isinstance(image1, RGBImage) != True:
            raise TypeError
        if isinstance(image2, RGBImage) != True:
            raise TypeError
        if image1.size() != image1.size():
            raise ValueError
        flattened_list = [z for x in image1.get_pixels() for y in x for z in y]
        flattened_list_2 = [z for x in image2.get_pixels() for y in x for z in y]
        sum_list = [(flattened_list[i] - flattened_list_2[i])**2 for i in range(len(flattened_list))]
        total_value = sum(sum_list)
        final_answer = ((total_value)**(1/2))
        return final_answer

    @staticmethod
    def vote(candidates):
        """
        This method gives back the most popular label given a list of candidates.
        """
        longest = max(set(candidates), key = candidates.count)
        return longest

    def predict(self, image):
        """
        Using KNN, this method predicts the label of a particular image.
        """
        if len(self.data) == 0:
            raise ValueError
        new_dict = [{"label": i[1], "distance": self.distance(image, i[0])} for i in self.data]
        sort = sorted(new_dict, key = lambda i: i['distance'])[:self.n_neighbors]
        return self.vote([i["label"] for i in sort])