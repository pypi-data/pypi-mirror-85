"""
Name : VideoProcess.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-09 10:52
Desc:
"""

import os

import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.video_manager import VideoManager

from .FontWriter import write_text
from .Format import get_random_md5
from .Graphics import alpha_compose, add_border, erase_border

__all__ = ['extract_frames',
           'batch_resize',
           'video_attribute',
           'video_compose',
           'scene_frames',
           'video_clip',
           'video_caption',
           'video_border',
           'video_delete',
           'video_erase',
           'video_logo',
           'video_image',
           'video_jpg',
           'video_erase',
           'video_speed',
           'video_cut']


def extract_frames(path, threshold=30.0, batch_size=32):
    """
    提取视频关键帧
    :param path: the video path
    :param threshold: the threshold of two frames`s pixel diff
    :param batch_size: batch size
    :return: a list of [images]
    """
    key_frames = []
    try:
        video_capture = cv2.VideoCapture(path)
        success, frame = video_capture.read()
        height, width = frame.shape[:2]
        key_frames.append([frame[:, :, ::-1]])

        frame_diffs, prev_frame, idx = [], None, 0
        while success:
            curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            if curr_frame is not None and prev_frame is not None:
                diff = cv2.absdiff(curr_frame, prev_frame)
                diff_sum_mean = np.sum(diff) / (width * height)
                frame_diffs.append(diff_sum_mean)
                if diff_sum_mean > threshold:
                    if len(key_frames[-1]) < batch_size:
                        key_frames[-1].append(frame[:, :, ::-1])
                    else:
                        if len(key_frames) * batch_size > 128:
                            break
                        key_frames.append([frame[:, :, ::-1]])
            idx += 1
            prev_frame = curr_frame
            success, frame = video_capture.read()
        video_capture.release()
        return key_frames
    except:
        return []


def batch_resize(images, max_size=640):
    """
    批量缩放图像
    :param images: a list of numpy data
    :param max_size: max size of width, height
    :return: a list of numpy data
    """
    try:
        if len(images) > 0 and max(images[0].shape) > max_size:
            h, w, _ = images[0].shape
            r = max_size / max(w, h)
            images = [cv2.resize(image, (int(w * r), int(h * r))) for image in images]
        return images
    except:
        return []


def video_attribute(path):
    """
    视频合成
    :param path: video path
    :return:
    """
    try:
        clip = VideoFileClip(path)

        return dict(width=int(clip.w),
                    height=int(clip.h),
                    aspect_ratio=float(clip.aspect_ratio),
                    duration=float(clip.reader.infos['duration']),
                    video_found=bool(clip.reader.infos['video_found']),
                    video_fps=float(clip.reader.infos['video_fps']),
                    video_nframes=int(clip.reader.infos['video_nframes']),
                    audio_found=bool(clip.reader.infos['audio_found']))
    except:
        return None
    finally:
        clip.close()


def video_compose(paths):
    """
    视频合成
    :param paths: the list of video path
    :return:
    """
    try:
        clips = [VideoFileClip(path) for path in paths if os.path.exists(path)]
        if len(clips) == 0:
            return None

        fps = clips[0].fps
        video = concatenate_videoclips(clips)

        output_file = os.path.join(os.path.split(paths[0])[0], get_random_md5()) + '.mp4'
        video.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        video.close()
        return output_file
    except:
        return None


def scene_frames(path):
    """
    获取视频每个镜头所在的帧数
    :param path: the video path
    :return:
    """
    video_manager = VideoManager([path])
    scene_manager = SceneManager(StatsManager())
    scene_manager.add_detector(ContentDetector())
    start_time = video_manager.get_base_timecode()

    try:
        frame_nums = video_manager._frame_length
        video_manager.set_duration(start_time=start_time, end_time=start_time + frame_nums)
        video_manager.set_downscale_factor()
        video_manager.start()

        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(start_time)
        video_manager.release()
        return [scene[1].get_frames() - scene[0].get_frames() for scene in scene_list], frame_nums
    except:
        return None


def video_clip(path, output_dir="", use_audio=True):
    """
    视频镜头分割
    :param path: the video path
    :param output_dir: output fold dir
    :param use_audio: use audio or not
    :return:
    """
    try:
        if not os.path.exists(path):
            return None
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        clip = VideoFileClip(path)
        frame_list, _ = scene_frames(path)

        output_files = []
        count, fps = 0, clip.fps
        for i, frame_num in enumerate(frame_list):
            file_name = os.path.join(output_dir, "%s_%s_%s.mp4" % (i + 1, count, count + frame_num))
            video = clip.subclip(count / fps, (count + frame_num) / fps)
            video.write_videofile(file_name, audio=use_audio, audio_codec="aac", threads=5)
            count = count + frame_num
            output_files.append(file_name)
        video.close()
        clip.close()
        return output_files
    except:
        return None


def video_caption(path, text, position, font_size, font_color, font_path, fps=None):
    """
    视频添加字幕
    :param path: the video path
    :param text: caption text
    :param position:
    :param font_size:
    :param font_color:
    :param font_path:
    :param fps:
    :return:
    """
    try:
        clip = VideoFileClip(path)
        frames = [write_text(frame, text, position, font_size, font_color, font_path) for frame in
                  clip.iter_frames()]
        num_frames = min(clip.reader.nframes, len(frames))
        fps = clip.fps if fps is None else fps
        audio = clip.audio.subclip(0 / fps, num_frames / fps) if clip.audio else None
        clip = ImageSequenceClip(frames, fps=fps)
        if audio is not None:
            clip.set_audio(audio)
            audio.close()

        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_border(path, border=[0, 0, 0, 0], color=(0, 0, 0)):
    """
    视频添加黑边
    :param path: the video path
    :param border: border list -> [up, down, left, right]
    :param color: color tuple -> (r, g, b)
    :return:
    """
    try:
        clip = VideoFileClip(path)
        frames = [add_border(frame, border, color) for frame in clip.iter_frames()]
        fps, num_frames = clip.fps, min(clip.reader.nframes, len(frames))

        if num_frames > 2000:
            frames = []
            for i, frame in enumerate(clip.iter_frames()):
                file_name = "%s.jpg" % i
                frame = add_border(frame, border, color)
                cv2.imwrite(file_name, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
                frames.append(file_name)
        else:
            frames = [add_border(frame, border, color) for frame in clip.iter_frames()]

        if clip.audio:
            clip = ImageSequenceClip(frames, fps=fps).set_audio(clip.audio)
        else:
            clip = ImageSequenceClip(frames, fps=fps)

        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_delete(path, border=[0, 0, 0, 0]):
    """
    视频裁剪边缘
    :param path:
    :param border: [up, down, left, right]
    :return:
    """

    def delete_border(image, border):
        if len(image.shape) < 3:
            return image

        height, width, _ = image.shape
        up, down, left, right = border
        if up < 0 or down < 0 or left < 0 or right < 0:
            return image
        if (height - down - up) % 2 == 1:
            down -= 1
        if (width - right - left) % 2 == 1:
            right -= 1
        new = image[up:height - down, left:width - right]
        return new.astype(np.uint8)

    try:
        clip = VideoFileClip(path)
        fps, num_frames = clip.fps, clip.reader.nframes
        if num_frames > 2000:
            frames = []
            for i, frame in enumerate(clip.iter_frames()):
                file_name = "%s.jpg" % i
                frame = delete_border(frame, border)
                cv2.imwrite(file_name, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
                frames.append(file_name)
        else:
            frames = [delete_border(frame, border) for frame in clip.iter_frames()]

        if clip.audio:
            clip = ImageSequenceClip(frames, fps=fps).set_audio(clip.audio)
        else:
            clip = ImageSequenceClip(frames, fps=fps)
        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_logo(path, src, x, y, start=0, end=-1):
    """
    视频添加LOGO
    :param path: the video path
    :param src: the logo image
    :param x: col
    :param y: row
    :param start: start frame
    :param end: end frame
    :return:
    """
    try:
        clip = VideoFileClip(path)
        if end == -1:
            end = clip.reader.nframes
        frames = []
        for i, frame in enumerate(clip.iter_frames()):
            if i in range(start, end + 1):
                frames.append(alpha_compose(frame, src, x, y))
            else:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA))

        fps, num_frames = clip.fps, min(clip.reader.nframes, len(frames))
        if clip.audio:
            clip = ImageSequenceClip(frames, fps=fps).set_audio(clip.audio)
        else:
            clip = ImageSequenceClip(frames, fps=fps)

        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_image(path, output_dir=""):
    """
    视频保存图片
    :param path: the video path
    :param output_dir: output fold dir
    :return:
    """
    try:
        if not os.path.exists(path):
            return None
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        clip = VideoFileClip(path, has_mask=True, audio=False)
        output_files = []
        for i, (frame, alpha) in enumerate(zip(clip.iter_frames(), clip.mask.iter_frames())):
            frame = np.dstack((frame, (alpha * 255).astype('uint8')))
            file_name = os.path.join(output_dir, "%s.png" % i)
            cv2.imwrite(file_name, cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGBA2BGRA))
            output_files.append(file_name)
        clip.close()
        return output_files
    except:
        return None


def video_jpg(path, output_dir="", start=0, end=-1):
    """
    视频保存jpg图片
    :param path: the video path
    :param output_dir: output fold dir
    :param start: first frame to save
    :param end: last frame to save
    :return:
    """
    try:
        if not os.path.exists(path):
            return None
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        clip = VideoFileClip(path, has_mask=True, audio=False)
        fps, num_frames = clip.fps, clip.reader.nframes
        start = max(0, start)
        end = min(end, num_frames - 1) if end > -1 else num_frames - 1
        output_files = []
        for i, frame in enumerate(clip.iter_frames()):
            if i < start:
                continue
            elif start <= i <= end:
                file_name = os.path.join(output_dir, "%s.jpg" % i)
                cv2.imwrite(file_name, cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR))
                output_files.append(file_name)
            else:
                break
        clip.close()
        return output_files
    except:
        return None


def video_erase(path, border=[0, 0, 0, 0], color=(0, 0, 0), fps=None):
    """
    视频擦除边框
    :param path: the video path
    :param border: border list -> [up, down, left, right]
    :param color: color tuple -> (r, g, b)
    :param fps:
    :return:
    """
    try:
        clip = VideoFileClip(path)
        fps, num_frames = clip.fps if fps is None else fps, clip.reader.nframes
        if num_frames > 2000:
            frames = []
            for i, frame in enumerate(clip.iter_frames()):
                file_name = "%s.jpg" % i
                frame = erase_border(frame, border, color)
                cv2.imwrite(file_name, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
                frames.append(file_name)
        else:
            frames = [erase_border(frame, border, color) for frame in clip.iter_frames()]

        if clip.audio:
            clip = ImageSequenceClip(frames, fps=fps).set_audio(clip.audio)
        else:
            clip = ImageSequenceClip(frames, fps=fps)

        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_speed(path, fps):
    """
    视频变速
    :param path: the video path
    :param fps:
    :return:
    """
    try:
        if not os.path.exists(path):
            return None

        clip = VideoFileClip(path, has_mask=True)
        video_period = clip.duration
        clip = clip.speedx(final_duration=clip.fps / fps * video_period)

        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)
        clip.close()
        return output_file
    except:
        return None


def video_cut(path, start=0, end=-1):
    """
    视频裁掉片段
    :param path: the video path
    :param start: first frame to cut
    :param end: last frame to cut
    :return:
    """
    try:
        if not os.path.exists(path):
            return None

        clip = VideoFileClip(path, has_mask=True)
        fps, num_frames = clip.fps, clip.reader.nframes
        start = max(0, start)
        end = min(end, num_frames - 1) if end > -1 else num_frames - 1
        if end < start:
            return None
        video = []
        if start > 0:
            temp = clip.subclip(0 / fps, start / fps)
            video.append(temp)
        if end < num_frames - 1:
            temp = clip.subclip((end + 1) / fps, num_frames / fps)
            video.append(temp)

        if len(video) == 0:
            return None
        clip = concatenate_videoclips(video)
        output_file = os.path.join(os.path.split(path)[0], get_random_md5()) + '.mp4'
        clip.write_videofile(output_file, fps=fps, audio_codec="aac", threads=5)

        for v in video:
            v.close()

        temp.close()
        clip.close()
        return output_file
    except:
        return None
