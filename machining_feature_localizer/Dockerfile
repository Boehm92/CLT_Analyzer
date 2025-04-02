FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip setuptools && \
    apt-get update && \
    apt-get install -y build-essential cmake libglib2.0-0 libgl1-mesa-glx && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip install torch==2.0.0 && \
    pip install torch_geometric && \
    pip install torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cu117.html && \
    rm /usr/include/xlocale.h

COPY scripts/ /app/scripts/
ENV PYTHONPATH=/app/scripts

CMD ["python", "scripts/__main__.py"]
