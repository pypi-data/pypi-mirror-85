import numpy as np

def quaternionProduct(q1, q2):
    """quaternionProduct Computes the quaternion product. Element order is w,x,y,z
    where w is the real element.

    :param q1: An indexable 4-element container
    :param q2: An indexable 4-element container
    """

    w = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
    x = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
    y = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]
    z = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]

    return (w,x,y,z)


def quaternionProductNp(q1, q2):
    """quaternionProduct Computes the quaternion product using numpy methods.
    Element order is w,x,y,z where w is the real element.

    :param q1: An indexable 4-element container
    :param q2: An indexable 4-element container
    """

    real = q1[0] * q2[0] - \
        np.dot(q1[1:4], q2[1:4])
    imag = q1[0] * q2[1:4] + q1[1:4] * q2[0] + np.array(
        [q1[2] * q2[3]-q1[3] * q2[2], q1[3] * q2[1] - \
        q1[1] * q2[3], q1[1] * q2[2]-q1[2] * q2[1]])

    return np.array([real, imag[0], imag[1], imag[2]])
