# This file is part of Sympathy for Data.
# Copyright (c) 2017, Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import numpy as np

from sympathy.api import node
from sympathy.api.exceptions import SyNodeError
from sympathy.api.nodeconfig import Port
from sympathy.api.nodeconfig import Ports
from sympathy.api.nodeconfig import Tag
from sympathy.api.nodeconfig import Tags

from sylib.imageprocessing.image import File as ImageFile
from sylib.machinelearning.abstract_nodes import SyML_abstract


class FeaturesToImages(node.Node):
    name = 'Features to Images'
    author = 'Mathias Broxvall'
    version = '0.1'
    icon = 'features_to_image.svg'
    description = 'Converts each row into a separate image in a list'
    nodeid = 'org.sysess.sympathy.machinelearning.features_to_images'
    tags = Tags(Tag.MachineLearning.IO)

    parameters = node.parameters()
    parameters.set_integer('channels', value=1, label='Channels',
                           description='Number of channels in image')
    parameters.set_integer(
        'width', value=8, label='Width',
        description='Width of image. If 0 then compute automatically '
        'assuming square input image')
    inputs = Ports([Port.Table('Dataset to be converted', name='X')])
    outputs = Ports([Port.Custom('[image]', 'Output images', name='out')])
    __doc__ = SyML_abstract.generate_docstring2(
        description, parameters, inputs, outputs)

    def execute(self, node_context):

        channels = node_context.parameters['channels'].value
        width = node_context.parameters['width'].value
        X_tbl = node_context.input['X']
        X_mat = X_tbl.to_matrix()
        X_arr = np.array(X_mat)

        out = node_context.output['out']
        rows = X_arr.shape[0]
        cols = X_arr.shape[1]
        if width <= 0:
            width = int(np.sqrt(cols // channels))
        height = (cols // channels) // width
        maxval = np.max(X_arr)
        for row in range(rows):
            im = X_arr[row, :].reshape(height, width, channels) / maxval
            im_f = ImageFile()
            im_f.set_image(im)
            out.append(im_f)


class ImagesToFeatures(node.Node):
    name = 'Images to Features'
    author = 'Mathias Broxvall'
    version = '0.1'
    icon = 'image_to_features.svg'
    description = 'Converts each image in a list into a row of features'
    nodeid = 'org.sysess.sympathy.machinelearning.images_to_features'
    tags = Tags(Tag.MachineLearning.IO)

    inputs = Ports([Port.Custom('[image]', 'Input images', name='in')])
    outputs = Ports([Port.Table('Dataset', name='X')])
    __doc__ = SyML_abstract.generate_docstring2(
        description, [], inputs, outputs)

    def execute(self, node_context):

        image_files = node_context.input['in']
        X_tbl = node_context.output['X']

        if len(image_files) == 0:
            return

        shape = image_files[0].get_image().shape
        width = shape[1]
        height = shape[0]
        if len(shape) > 2:
            channels = shape[2]
            images = [imf.get_image() for imf in image_files]
        else:
            channels = 1
            images = [imf.get_image().reshape((height, width, channels))
                      for imf in image_files]

        data = np.zeros((len(images), height*width*channels))
        for row, im in enumerate(images):
            data[row, :] = im.reshape(height*width*channels)

        if width*height*channels > 10000:
            raise SyNodeError("Too large input image to convert to features.")

        if channels > 1:
            fmt = "y{}_x{}_ch{}"
        else:
            fmt = "y{}_x{}"

        for y in range(height):
            for x in range(width):
                for ch in range(channels):
                    X_tbl.set_column_from_array(
                        fmt.format(y, x, ch),
                        data[:, y*width*channels + x*channels + ch])
