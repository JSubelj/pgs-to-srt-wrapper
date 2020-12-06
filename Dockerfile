FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y wget

RUN wget https://packages.microsoft.com/config/ubuntu/20.10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get update && apt-get install -y ffmpeg 
RUN apt-get install -y dotnet-sdk-5.0
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
RUN apt-get install -y libtesseract4 unzip
RUN mkdir /app
RUN wget https://github.com/Tentacule/PgsToSrt/releases/download/v1.2.0/PgsToSrt-1.2.0.zip
RUN mkdir /app/PgsToSrt-1.2.0
RUN unzip PgsToSrt-1.2.0.zip -d /app/PgsToSrt-1.2.0
RUN mkdir /app/PgsToSrt-1.2.0/tessdata
RUN wget -O /app/PgsToSrt-1.2.0/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

COPY PgsToSrtWrapper/*.py /app/
COPY PgsToSrtWrapper/requirements.txt /app/requirements.txt
RUN python3.8 -m pip install -r /app/requirements.txt
# RUN python3.8 -m pip install pyinotify


ENV SKIP_DISCOVERY=FALSE
ENV SLEEPING_TIME_S=1
ENV PGSTOSRT_DLL=/app/PgsToSrt-1.2.0/PgsToSrt.dll
ENV DOTNET_EXECUTABLE=dotnet

VOLUME [ "/downloads" ]
CMD python3.8 /app/main.py
