# -*- coding: utf-8 -*-



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This is untested and probably doesn't work
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



###########################################################################
#   Coqui TTS API
#
def get_tts_audio(text_in, config, args):

    """
    """
    from pathlib import Path
    import sys

    # ensure Coqui_tts is installed
    try:
        from TTS.utils.manage import ModelManager
    except:
        print("Error: Coqui TTS is not installed properly.  Try 'pip install TTS'")
        exit
    try:
       from TTS.utils.synthesizer import Synthesizer
    except:
        print("Error: Coqui TTS is not installed properly.  Try 'pip install TTS'")
        exit

    VOICE_in = config['preferred']['voice']
    LOCALE_in = config['preferred']['locale']
    AUDIO_FORMAT_in = config['preferred']['audio_format']
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format']


    text = "this is a test"
    


    # load model manager FIXME
        
    path = "/home/zymos/.local/lib/python3.8/site-packages/TTS/.models.json"

   #  path = Path(__file__).parent / "../.models.json"
    manager = ModelManager(path)

    model_path = None
    config_path = None
    speakers_file_path = None
    language_ids_file_path = None
    vocoder_path = None
    vocoder_config_path = None
    encoder_path = None
    encoder_config_path = None
    
    reference_wav=None
    capacitron_style_wav=None
    capacitron_style_text=None
    reference_speaker_idx=None
    save_spectogram=False
    use_cuda=False
    save_spectogram=False
    speaker_wav=None
    speaker_idx=None
    language_idx=None
    reference_speaker_idx=None

    model_name="tts_models/en/ljspeech/tacotron2-DDC"
    out_path="tts_output.wav"
    model_info_by_idx = None
    model_info_by_name = None
    vocoder_name = None

    # CASE2 #info : model info of pre-trained TTS models
    if model_info_by_idx:
        model_query = model_info_by_idx
        manager.model_info_by_idx(model_query)
        sys.exit()

    if model_info_by_name:
        model_query_full_name = model_info_by_name
        manager.model_info_by_full_name(model_query_full_name)
        sys.exit()

    # CASE3: load pre-trained model paths
    if model_name is not None and not model_path:
        model_path, config_path, model_item = manager.download_model(model_name)
        vocoder_name = model_item["default_vocoder"] if vocoder_name is None else vocoder_name

    if vocoder_name is not None and not vocoder_path:
        vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    # CASE4: set custom model paths
    if model_path is not None:
        model_path = model_path
        config_path = config_path
        speakers_file_path = speakers_file_path
        language_ids_file_path = language_ids_file_path

    if vocoder_path is not None:
        vocoder_path = vocoder_path
        vocoder_config_path = vocoder_config_path

    if encoder_path is not None:
        encoder_path = encoder_path
        encoder_config_path = encoder_config_path


#  https://github.com/coqui-ai/TTS/blob/dev/TTS/utils/synthesizer.py
   # load models
    synthesizer = Synthesizer(
      model_path,
      config_path,
      speakers_file_path,
      language_ids_file_path,
      vocoder_path,
      vocoder_config_path,
      encoder_path,
      encoder_config_path,
      use_cuda,
    )
   
   # kick it
    wav = synthesizer.tts(
        text,
        speaker_idx,
        language_idx,
        speaker_wav,
        reference_wav,
        capacitron_style_wav,
        capacitron_style_text,
        reference_speaker_name=reference_speaker_idx,
    )


    ###############
    # Debug stuff
    if DEBUG:
        print("-----------------------------------------------------------")
        print(" Using Coqui TTS application")
        print(VOICE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in)
        print("----------------------------TEXT---------------------------")
        print(text_in)
        print("----------------------------URL---------------------------")
        print(url)
        print("----------------------------------------------------------")
    

   # save the results
    print(" > Saving output to {}".format(out_path))
    synthesizer.save_wav(wav, out_path)
