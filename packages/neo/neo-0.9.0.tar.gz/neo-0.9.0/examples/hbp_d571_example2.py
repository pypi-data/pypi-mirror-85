import os
import matplotlib.pyplot as plt
import numpy as np
from quantities import Hz, mm, dimensionless
from neo.core import CircularRegionOfInterest
from neo.io import TiffIO
import elephant as el

data_path = os.path.expanduser("~/Data/WaveScalES/LENS/170110_mouse2_deep/t1")

# loading data
data = TiffIO(data_path, units=dimensionless, sampling_rate=25 * Hz, spatial_scale=0.05 * mm).read()
#data = TiffIO(data_path).read(units=dimensionless, sampling_rate=25 * Hz, spatial_scale=0.05 * mm)
images = data[0].segments[0].imagesequences[0]
images /= images.max()
plt.subplot(2, 2, 1)
plt.imshow(images[100], cmap='gray')
plt.title("Original image (frame 100)")
print(images.min(), images.max(), images.mean())  ###
# preprocessing
background = np.mean(images, axis=0)
print(background.min(), background.max(), background.mean())
preprocessed_images = images - background
print(preprocessed_images.min(), preprocessed_images.max(), preprocessed_images.mean(), preprocessed_images.shape, preprocessed_images.dtype)
np.save("preprocessed_images_orig.npy", preprocessed_images.magnitude)
plt.subplot(2, 2, 2)
plt.imshow(preprocessed_images[100], cmap='gray')
plt.title("Subtracted background (frame 100)")

# defining ROI and extracting signal
roi = CircularRegionOfInterest(x=50, y=50, radius=10)
circle = plt.Circle(roi.centre, roi.radius, color='b', fill=False)
ax = plt.gca()
ax.add_artist(circle)

central_signal = preprocessed_images.signal_from_region(roi)[0]
plt.subplot(2, 2, 3)
plt.plot(central_signal.times, central_signal, lw=0.8)
plt.title("Mean signal from ROI")
plt.xlabel("Time [s]")

# calculating power spectrum
freqs, psd = el.spectral.welch_psd(central_signal,
                                   fs=central_signal.sampling_rate,
freq_res=0.1 * Hz,
                                   overlap=0.8)
plt.subplot(2, 2, 4)
plt.plot(freqs, np.mean(psd, axis=0), lw=0.8)
plt.title("Average power spectrum")
plt.xlabel("frequency [Hz]")
plt.ylabel("Fourier signal")

plt.tight_layout()
plt.show()  # see Figure 2
