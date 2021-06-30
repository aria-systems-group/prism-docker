FROM ubuntu:18.04

RUN apt-get -y update
RUN apt -y install make gcc g++ default-jdk git wget vim
RUN apt -y install python

RUN git clone https://github.com/prismmodelchecker/prism-games.git
RUN export JAVA_HOME=`prism-games/prism/src/scripts/findjavac.sh | sed 's/\/bin\/javac//'`
RUN apt -y install openjdk-8-jdk libgmp-dev m4
RUN export JAVA8_HOME=`find /usr/lib/jvm -name 'java-8*'`
RUN wget http://www.bugseng.com/products/ppl/download/ftp/releases/1.2/ppl-1.2.tar.gz
RUN tar xfz ppl-1.2.tar.gz
RUN cd ppl-1.2 \
    && ./configure --enable-interfaces=java --with-java=$JAVA8_HOME \
    && make \
    && make install

RUN cd prism-games/prism \
    && make PPL_DIR=/usr/local/lib

RUN git clone https://github.com/prismmodelchecker/prism.git \
    && cd prism/prism \
    && make
RUN apt install  openssh-server sudo -y
RUN apt-get -y install net-tools
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 prism 
RUN echo 'prism:prism' | chpasswd
RUN service ssh start

EXPOSE 22


ENV DISPLAY=host.docker.internal:0
# RUN echo "export DISPLAY=host.docker.internal:0" >> ~/.bashrc \
    # && source ~/.bashrc

CMD ["/usr/sbin/sshd","-D"]

ENTRYPOINT service ssh start && bash
