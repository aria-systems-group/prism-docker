FROM ubuntu:18.04

# Update and install necessary tools (vim is just an option)
RUN apt-get -y update
RUN apt -y install make gcc g++ git wget vim
RUN apt -y install python
RUN apt -y install python3-pip

# Install Default JAVA for building prism
RUN apt -y install default-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# Install JAVA8 for building PPL
RUN apt -y install openjdk-8-jdk libgmp-dev m4
ENV JAVA8_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Build PPL Library with the option of java (for enabling java interface)
RUN wget http://www.bugseng.com/products/ppl/download/ftp/releases/1.2/ppl-1.2.tar.gz \
    && tar xfz ppl-1.2.tar.gz \
    && cd ppl-1.2 \
    && ./configure --enable-interfaces=java --with-java=$JAVA8_HOME \
    && make -j 4 \
    && make -j 4 install

# Build prism-game
RUN git clone https://github.com/prismmodelchecker/prism-games.git \
    && cd prism-games/prism \
    && make -j 4 PPL_DIR=/usr/local/lib

# BUild prism
RUN git clone https://github.com/prismmodelchecker/prism.git \
    && cd prism/prism \
    && make -j 4

# Link binary to local binaries so that we can call them from anywhere
RUN ln -s /prism-games/prism/bin/prism /usr/local/bin/prismgames
RUN ln -s /prism-games/prism/bin/xprism /usr/local/bin/xprismgames
RUN ln -s /prism/prism/bin/prism /usr/local/bin/prism
RUN ln -s /prism/prism/bin/xprism /usr/local/bin/xprism

# Set DISPLAY to make it work with XQuartz (Mac)
ENV DISPLAY=host.docker.internal:0

# Setting up ssh so that we can access from the local pc
RUN apt install  openssh-server sudo -y
RUN apt-get -y install net-tools
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 prism
RUN echo 'prism:prism' | chpasswd
RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]
ENTRYPOINT service ssh start && bash
