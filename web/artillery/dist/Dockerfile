FROM openjdk:8u181-jdk

RUN apt update -y && apt install wget -y

RUN find / -name "*.dtd" -type f -delete

RUN find / -name "*.xml" -type f -delete

RUN wget https://archive.apache.org/dist/tomcat/tomcat-10/v10.0.4/bin/apache-tomcat-10.0.4.tar.gz -O- | tar -xzv

RUN mv /apache-tomcat-10.0.4 /tomcat

RUN rm -rf /tomcat/webapps/*

COPY ./ROOT /tomcat/webapps/ROOT

COPY ./airbase.db /tomcat/bin

COPY ./request.xsd /tomcat/bin

COPY ./entrypoint.sh /tomcat/bin

RUN javac -cp "tomcat/lib/servlet-api.jar" tomcat/webapps/ROOT/WEB-INF/classes/Results.java

RUN javac -cp "tomcat/lib/servlet-api.jar" tomcat/webapps/ROOT/WEB-INF/classes/Flag.java

WORKDIR /tomcat/bin

RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh
