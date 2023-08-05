FROM fedora:33

RUN dnf -y update
RUN dnf -y install python3-pip python3-tox python3-wheel make git findutils
RUN dnf clean all

RUN git clone https://github.com/Iolaum/fcust.git /src

RUN useradd -ms /bin/bash user1
RUN useradd -ms /bin/bash user2
RUN groupadd family
RUN usermod -a -G family user1
RUN usermod -a -G family user2
RUN cd /src; pip install --upgrade pip; pip install .[dev] --use-feature=2020-resolver
