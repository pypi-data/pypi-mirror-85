from .sound import get_voice
from .msn import crawl_data
from anews.common.utils import make_image_hd,create_loop
import textwrap
from moviepy.editor import *
import math,uuid,random
import traceback
from .texthelper import make_title,make_tag

def create_msn_news(url, title, root_path, font_path, logo_path,background_path, langCode, langName):
    arr_text, arr_img= crawl_data(url)
    if arr_text is None or len(arr_text)==0 or len(arr_img)==0:
        print("None data")
        return None, None, None, None, None,None
    final_path=None
    try:
        full_text= "".join(arr_text)
        full_text = full_text.strip()
        thumbnail_img = random.choice(arr_img)
        thumbnail_ok = make_title(title, full_text, make_image_hd(thumbnail_img, root_path),
                   font_path,88,langCode,root_path,logo_path)
        tags=make_tag(title,full_text,langCode)
        wrapper = textwrap.TextWrapper(width=5000)
        sumary_des=textwrap.shorten(text=full_text, width=300)

        arr_wrap_text=wrapper.wrap(text=full_text)
        arr_voice=[]
        for wrap_text in arr_wrap_text:
            path_voice = get_voice(wrap_text,root_path,langCode,langName)
            arr_voice.append(AudioFileClip(path_voice))
        full_audio = concatenate_audioclips(arr_voice)
        full_audio_duration=full_audio.duration
        time_per_img=math.ceil(full_audio_duration/len(arr_img))
        arr_img_comp=[]
        bg_path=create_loop(background_path,full_audio_duration,root_path)
        bg = VideoFileClip(bg_path)
        arr_img_comp.append(bg)
        start_t=0
        TIME_SUB_IMG=15
        for img in arr_img:
            arr_img_comp.append(
                ImageClip(make_image_hd(img, root_path)).set_start(start_t).set_duration(TIME_SUB_IMG).set_position((18, 15)))
            start_t+=TIME_SUB_IMG
            times_sub = math.floor(time_per_img-TIME_SUB_IMG/TIME_SUB_IMG)
            total_time_sub_tmp=0
            for i in range(times_sub):
                time_duration_tmp = TIME_SUB_IMG
                if i == times_sub-1:
                    time_duration_tmp=time_per_img-total_time_sub_tmp
                arr_img_comp.append(
                    ImageClip(make_image_hd(img, root_path,i%7)).set_start(start_t).set_duration(time_duration_tmp).set_position((18, 15)))
                total_time_sub_tmp+= time_duration_tmp
                start_t += time_duration_tmp
        # i=0
        # while start_t < full_audio_duration:
        #     arr_img_comp.append(arr_img_comp_tmp[i].set_start(start_t))
        #     start_t += time_per_img
        #     i = (i+1) % len(arr_img)
        final_path=f"{root_path}/final-up-{str(uuid.uuid4())}.avi"
        CompositeVideoClip(arr_img_comp).set_audio(full_audio).subclip(0, full_audio_duration).write_videofile(final_path, fps=24, codec='libx264')
        for item in arr_img_comp:
            item.close()
    except:
        print(traceback.format_exc())
        pass
    return final_path, thumbnail_ok, arr_img, full_text, sumary_des, tags








