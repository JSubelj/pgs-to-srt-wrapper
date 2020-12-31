FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y wget

RUN wget https://packages.microsoft.com/config/ubuntu/20.10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get update && apt-get install -y ffmpeg 
RUN apt-get install -y dotnet-sdk-5.0
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
RUN apt-get install -y libtesseract4 unzip curl
RUN mkdir -p /app/PgsToSrt
RUN LATEST_PGS_TO_SRT_VERSION=$(curl -s https://api.github.com/repos/Tentacule/PgsToSrt/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') && WITHOUT_V=$(echo $LATEST_PGS_TO_SRT_VERSION | sed 's/v//') && wget https://github.com/Tentacule/PgsToSrt/releases/download/$LATEST_PGS_TO_SRT_VERSION/PgsToSrt-$WITHOUT_V.zip && unzip PgsToSrt-$WITHOUT_V.zip -d /app/PgsToSrt
RUN mkdir /app/PgsToSrt/tessdata
RUN wget -O /app/PgsToSrt/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

COPY PgsToSrtWrapper/*.py /app/
COPY PgsToSrtWrapper/requirements.txt /app/requirements.txt
RUN python3.8 -m pip install -r /app/requirements.txt
# RUN python3.8 -m pip install pyinotify


ENV SKIP_DISCOVERY=FALSE
ENV SLEEPING_TIME_S=1
ENV PGSTOSRT_DLL=/app/PgsToSrt/PgsToSrt.dll
ENV DOTNET_EXECUTABLE=dotnet

VOLUME [ "/downloads" ]
CMD python3.8 /app/main.py
