FROM nan42/eval:base

# should be passed from docker build CLI
ARG JAR_VERSION

RUN touch ${JAR_VERSION}".txt"


COPY runner ./experiments/runner/
COPY simulator/mobileCameras.rs ./experiments/simulator/mobileCameras.rs/
COPY simulator/trace ./experiments/simulator/trace
COPY simulator/runnable_jar/mobileCameras_${JAR_VERSION}.jar ./experiments/simulator/runnable_jar/mobileCameras.jar

WORKDIR ./experiments/runner/
ENTRYPOINT ["python3", "Main.py"]
