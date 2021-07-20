FROM nan42/eval:base

ARG JAR_VER="fd218e"

COPY runner ./experiments/runner/
COPY simulator/mobileCameras.rs ./experiments/simulator/mobileCameras.rs/
COPY simulator/trace ./experiments/simulator/trace
COPY simulator/runnable_jar/mobileCameras_${JAR_VER}.jar ./experiments/simulator/runnable_jar/mobileCameras.jar

WORKDIR ./experiments/runner/
ENTRYPOINT ["python3", "Main.py"]

