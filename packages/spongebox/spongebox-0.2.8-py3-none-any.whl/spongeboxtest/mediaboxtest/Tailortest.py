import unittest
from spongebox.mediabox import Tailor

frgs = []
frgs.append(("001421", "010419"))
frgs.append(("000015", "000020"))
# Tailor("F:\\download\\20\\vedio.mp4").launch(frgs)
Tailor("F:\\download\\20\\vedio.mp4",output_dir="C:\\Users\\LuoJi\\Downloads").launch(frgs)