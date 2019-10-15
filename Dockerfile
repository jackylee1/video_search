FROM base/archlinux:latest

WORKDIR /usr/src/app

COPY . .

RUN pacman -Syu --noconfirm \
    && pacman -S --noconfirm python python-pip gcc cmake make hdf5 gtk3 ffmpeg youtube-dl \
    && pacman -Scc --noconfirm \
    && pip install -e . \
    && youtube-dl -o video_search/assets/SAcpESN_Fk4/data/ddg.webm -f webm "https://www.youtube.com/watch?v=SAcpESN_Fk4" \
    && youtube-dl -o video_search/assets/ekb67icJRJ8/data/garv.webm -f webm "https://www.youtube.com/watch?v=ekb67icJRJ8" \
    && youtube-dl -o video_search/assets/HkuKHwetV6Q/data/naik.webm -f webm "https://www.youtube.com/watch?v=HkuKHwetV6Q" \
    && youtube-dl -o video_search/assets/b8UoC23jhPc/data/love_is_love.webm -f webm "https://www.youtube.com/watch?v=b8UoC23jhPc" \
    && python -m spacy download en \
    && python -m nltk.downloader punkt averaged_perceptron_tagger wordnet

CMD [ "searchui" ]
