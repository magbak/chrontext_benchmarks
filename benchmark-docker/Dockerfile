FROM python:3.10.6-bullseye
RUN apt-get update && apt-get install nano
WORKDIR /scripts
COPY requirements.txt .
COPY chrontext-0.1.40-cp310-cp310-manylinux_2_31_x86_64.whl .
RUN python -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip install chrontext-0.1.40-cp310-cp310-manylinux_2_31_x86_64.whl
RUN mkdir output
COPY . .
ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]