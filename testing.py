import random
from unidecode import unidecode
import textwrap
import cv2
from datetime import datetime
import textwrap
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
import requests
import json
import inspect
import sys
import colorama
import discord
from discord import Intents
from colorama import Fore, Style
colorama.init()
import time

start_time = time.time()

user_name = 'mir1ow'
user_mensagem = 'olsda'
timer = 155
user_id = 1

class phone:

    """
    Todas as funções do Telefone Microondas (Nome sujeito a mudança)

    """
    
    def __init__(self, user_name, user_mensagem, timer, user_id):
    
        self.user_name = user_name
        self.user_mensagem = user_mensagem
        self.timer = timer
        self.user_id = user_id # Sem uso~
        self.current_date = datetime.now()
        
        
        
        # Configurações de Vídeo
        
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.frame_size = (1024, 576)
        self.fps = 5
        self.font = [cv2.FONT_HERSHEY_DUPLEX, cv2.FONT_HERSHEY_SIMPLEX]
        self.font_thickness = 2
        
        # Clips
        
        self.segment1 = r"user_timer.mp4"
        self.segment2 = r"assets/part_1.mp4"
        self.segment3 = r"output_vid.mp4"
        self.segment4 = r"assets/part_3.mp4"
        self.output_file = "combined_video.mp4"
    
    def phonewave_timer(self):
        """
        
        Imprimi o timer (input: tempo) na tela do celular (Tela: Em chamada)  
        
        """
       
        #------------------------ VIDEO SETTING
        
        video_writer = cv2.VideoWriter('user_timer.mp4', self.fourcc, self.fps, self.frame_size)
        image = cv2.imread("assets/part1.png")
        
        #------------------------ FONT SETTING
        
        text = f"{self.timer}#                "
        font_scale = 1.5
        
        #######################################
        
        for i in range(len(text)):
            # Create a copy of the original image for each frame
            frame = image.copy()

            # Add the current character to the frame
            cv2.putText(frame, text[:i+1], (780, 350), self.font[0], font_scale, (250, 253, 250), self.font_thickness, cv2.LINE_AA)

            # Write the frame to the video
            video_writer.write(frame)

        # Release the video writer and close the video file
        video_writer.release()
    
    def phone_dmail(self):
        """
         
        Imprimi a mesnagem (input: mensagem) na tela do celular (Tela: Enviando SMS)
        
        """
        
        #------------------------ VIDEO SETTING
        
        cap = cv2.VideoCapture('assets/part_2.mp4')
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))       
        out = cv2.VideoWriter('output.mp4', self.fourcc, cap.get(cv2.CAP_PROP_FPS), (self.frame_size[0], self.frame_size[1]))
        formatted_date = self.current_date.strftime("%d/%m/%Y")
        
        #------------------------ TEXT SETTING
        
        line_length = 26
        normalized_string = unidecode(self.user_mensagem)
        wrapped_lines = textwrap.wrap(normalized_string, width=line_length)
        formatted_text = "\n".join(wrapped_lines)
        text = f"""
    {formatted_date}
    {user_name}
{formatted_text}
        """
        user_msg_lines = text.split('\n')
        start_frame = 43  # Text time display~
        end_frame = 150  # Not really working but let keep it here~ lmao 
        
        ##############################
        
  
        for frame_idx in range(total_frames):
            # Read the frame
            ret, frame = cap.read()
            if not ret:
                break

            if start_frame <= frame_idx <= end_frame: # let leave this extra operator there. He's a survivor of a old code. 
                text_position = (290, 35)
                font_scale = 0.9
                text_color = (25, 27, 32) 
                for i, line in enumerate(user_msg_lines):
                    line_position = (text_position[0], text_position[1] + (i + 1) * 50)
                    cv2.putText(frame, line, line_position, self.font[1], font_scale, text_color, self.font_thickness, cv2.LINE_AA)

            out.write(frame)
            
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        #------------------------ AUDIO SETTING
        
        video = VideoFileClip("output.mp4")
        audio = AudioFileClip("assets/audio.m4a")
        video_with_audio = video.set_audio(audio)
        video_with_audio.write_videofile("output_vid.mp4")
        print("DMAIL VIDEO DONE")
        
    def combine_video_segments(self):
        """
        
        Combina os clip's 
        
        """
        clip1 = VideoFileClip(self.segment1)
        clip2 = VideoFileClip(self.segment2)
        clip3 = VideoFileClip(self.segment3)
        clip4 = VideoFileClip(self.segment4)

        final_clip = concatenate_videoclips([clip1, clip2, clip3, clip4])
        final_clip.write_videofile(self.output_file, codec='libx264', audio_codec="aac")

        print("Video segments combined successfully!")

class Call_LLM:
    def __init__(self):
        self.call_llm = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")

    @staticmethod
    def format_prompt(message, history):
        prompt = "<s>"
        for user_prompt, bot_response in history:
            prompt += f"[INST] {user_prompt} [/INST]"
            prompt += f" {bot_response}</s> "
        prompt += f"[INST] {message} [/INST]"
        return prompt

    def generate(self, prompt, history, system_prompt, temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0):
        temperature = float(temperature)
        if temperature < 1e-2:
            temperature = 1e-2
        top_p = float(top_p)

        generate_kwargs = dict(
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True,
            seed=42,
        )

        formatted_prompt = self.format_prompt(f"{system_prompt}, {prompt}", history)
        response = self.call_llm.text_generation(formatted_prompt, **generate_kwargs)
        output = response

        return output

    def generate_story(self, user_name, user_mensagem, tempo):
        dias_v = tempo / 60
        dias = format(dias_v, '.2f')
        prompt = str(f"{user_name}(User): {user_mensagem}")
        history = [("Hello", "Hi, how can I assist you?")]
        system_prompt = f"""Responda somente em português:

        1. Responda sempre em terceira pessoa, como um narrador.
        2. A história criada deve estar dentro do Universo de Steins;Gate.
        3. É estritamente necessário que sua resposta esteja relacionada com o prompt (input) do usuário.
        4. A mensagem do usuário representa uma mensagem que foi enviada {dias} minutos no passado. Sua tarefa é narrar as consequências desta mensagem.

        Exemplo de resposta: 

        Nanao(User): 'Okabe é um cabeça de vento'

        Output:

        'Após se chatear pela mensagem recebida, Okabe decidiu abandonar o laboratório. A linha do tempo foi alterada drasticamente.'

        5. Você estará a cargo de decidir se as consequências serão positivas ou negativas, significativas ou triviais. Sempre relate o novo estado da linha do tempo.
        6. Não adicione observações e mantenha o escopo do texto dentro de 500 caracteres.
        7. A pessoa que receberá a mensagem no passado se chama Okabe, ela é fundadora do Future Gadget Lab - Member 001. Os membros do Laboratório são:
            Member 002 - Mayuri Shiina
            Member 003 - Itaru Hashida (AKA Daru, SuperHacker, DasH)
            Member 004 - Kurisu Makise (Neuroscientist from Viktor Chondria University - USA)
            Member 005 - Moeka Kiryu (SERN Agent in a parallel world line)
            Member 006 - Luka Urushibara (Androgynous guy)
            Member 007 - Faris NyanNyan (Rich girl who owns a Maid Café in Akihabara called MayQueen+Nyan²)
            Member 008 - Suzuha Amane (AKA John Titor, Daru's daughter)
            Member 009 - Maho Hiyajo (Neuroscientist from Viktor Chondria University - USA)
            Member 010 - Kagari Shiina (Mayuri's daughter from the future - Only present in the Alpha world line)
            Member 011 - Yuki Amane (Daru's wife, Suzuha's mother)

        Aqui está um resumo do plot da obra Steins;Gate:
        Rintarou Okabe, um autoproclamado cientista maluco, descobre acidentalmente uma forma de enviar mensagens para o passado usando um micro-ondas modificado chamado "PhoneWave". Ele e seus amigos, Mayuri e Daru, formam o "Laboratório Futurista" e começam a experimentar viagens no tempo.
        No entanto, eles logo se veem envolvidos em uma conspiração envolvendo uma organização chamada SERN, que também está pesquisando viagem no tempo. Okabe descobre que suas ações têm consequências drásticas e perigosas, levando a diferentes linhas do tempo e realidades alternativas.
        Conforme a trama se desenrola, Okabe tenta desesperadamente salvar seus amigos e impedir um futuro distópico. Ele se depara com dilemas éticos, sacrifícios e reviravoltas surpreendentes. A história explora temas como o efeito borboleta, manipulação do tempo e a luta do protagonista para encontrar uma linha do tempo ideal onde todos possam estar seguros.

        """

        output = self.generate(prompt, history, system_prompt)
        return output

phonewave = phone(user_name, user_mensagem, timer, user_id)
phonewave.phonewave_timer()
phonewave.phone_dmail()
phonewave.combine_video_segments()

end_time = time.time()
execution_time = end_time - start_time
print("Execution time: {:.2f} seconds".format(execution_time))
