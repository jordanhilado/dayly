FROM fedora:latest

# NOTE:
# the && : is a no-op action so the other lines can be swapped with ease (without removing the '\'` character)
RUN yum update -y \
    && \
    yum install \
    git -y \
    && \
   yum clean all \
   && :

ENV PATH /usr/local/bin:$PATH



COPY Dayly/ /repo

WORKDIR /repo

# TODO: decide where to put the pip3 install block
#       1. if the '-r Requirements is used it should be after the `COPY` and `WORKDIR`
#       2. if not it can be before
#
#       advantages of 2. is that after the code changes there is no need to rebuild the packages
RUN pip3 install \
    requests \
    flask_session \
    cs50 \
    && :
# TODO: when https://github.com/jordanhilado/Dayly/pull/8 is merged, use the following line instead of the explicit packages
#  -r Requirements.txt \

ENV FLASK_APP application.py

CMD python3 \
    -m flask \
    run \
    -h 0.0.0.0 \
    && :

# TODO: the '-h 0.0.0.0' allows flask to expose the website outside the container
#       
