import tensorflow as tf


def draw_gaussian_noise_power(batch_size, noise_power_spec):
    noise_power = tf.random.normal(
        shape=(batch_size,),
        mean=0.0,
        stddev=noise_power_spec,
    )
    return noise_power

def add_noise(image, noise_power_spec=30, fixed_noise=False, noise_input=False):
    if fixed_noise:
        noise_power = tf.constant(noise_power_spec, dtype=image.dtype)[None]
    else:
        noise_power = draw_gaussian_noise_power(
            batch_size=tf.shape(image)[0],
            noise_power_spec=noise_power_spec,
        )
    normal_noise = tf.random.normal(
        shape=tf.shape(image),
        mean=tf.cast(0.0, dtype=image.dtype),
        stddev=tf.cast(1.0, dtype=image.dtype),
        dtype=image.dtype,
    )
    noise_power_bdcast = noise_power[:, None, None, None]
    noise = normal_noise * noise_power_bdcast
    image_noisy = image + noise
    # this is to allow quick change in case we want to change the network's
    # input/output
    image_noisy.set_shape([None, None, None, image.shape[-1]])
    if noise_input:
        model_inputs = (image_noisy, noise_power[:, None])
    else:
        model_inputs = image_noisy
    model_outputs = image
    return model_inputs, model_outputs
