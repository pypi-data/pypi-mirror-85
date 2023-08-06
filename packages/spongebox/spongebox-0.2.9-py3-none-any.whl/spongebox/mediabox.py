import os
from spongebox.timebox import stamp


class Tailor:
    def __init__(self, media_path, output_dir=None, suffix=None):
        self.media_path = media_path
        self.media_name = "".join(media_path.split("\\")[-1].split(".")[:-1])
        self.suffix = self.media_path.split(".")[-1] if suffix == None else suffix
        self.output_dir = "\\".join(media_path.split("\\")[:-1]) if output_dir == None else output_dir
        self.output = "{}\\{}_SUB.{}".format(self.output_dir, self.media_name, self.suffix)
        self.token = stamp()

    def cut(self, stamp: tuple, frag_idx: int, suffix=""):
        """
        :param stamp:(start_timestamp,end_timestamp) like ("000125","002334")
        :param frag_idx:idx for the cuted fragment,"0"
        :param suffix: 文件后缀，无需显示指定，一般从文件名获得
        :return:返回所截取片段的名称

        """
        start = str(stamp[0])
        end = str(stamp[1])
        start_timestamp = [int(start[i:i + 2]) for i in range(0, 5, 2)]
        end_timestamp = [int(end[i:i + 2]) for i in range(0, 5, 2)]
        print("fragment cut start:", start_timestamp, end_timestamp)

        suffix = self.media_path.split(".")[1] if suffix == "" else suffix
        # output_file = self.media_path.split(".")[0] + '_SUB' + str(frag_idx) + "." + suffix
        output_file = "{}\\{}_SUB{}.{}".format(self.output_dir, self.media_name, frag_idx, self.suffix)
        time_interval = end_timestamp[0] * 3600 + end_timestamp[1] * 60 + end_timestamp[2] - (
                start_timestamp[0] * 3600 + start_timestamp[1] * 60 + start_timestamp[2])
        cmd = "ffmpeg -ss {} -i {} -t {} -c:v copy -c:a copy {}".format(
            ":".join([start[i:i + 2] for i in range(0, 5, 2)]),
            self.media_path, time_interval,
            output_file)
        print(cmd)
        os.system(cmd)
        print("cut finished")
        return output_file.replace("\\", "\\\\")

    def concat(self, fragments):
        """
        :param fragments:["f:\\\\015203\download\\\\cnr_SUB0.mp4","f:\\\\download\\\\cnr_SUB1.mp4"]
        :return:
        """
        print("concat start:{}".format(fragments))
        media_list_path = "{}\\concat{}.txt".format(self.output_dir, self.token)
        concat_file_content = ["file " + input_file + "\n" for input_file in fragments]
        with open(media_list_path, mode="w") as f:
            f.writelines(concat_file_content)
        cmd = "ffmpeg -f concat -safe 0 -i {} -c copy {}".format(media_list_path, self.output)
        print(cmd)
        os.system(cmd)
        print("concat finished:{}".format(self.output))

    def launch(self, frag_stamp_list):
        def get_idx():
            i = 0
            while True:
                yield i
                i += 1

        fragments = list(map(self.cut, frag_stamp_list, get_idx()))
        if len(fragments) > 1:
            self.concat(fragments)
