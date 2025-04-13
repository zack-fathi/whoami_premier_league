############ Build stage ############
FROM eclipse-temurin:17-jdk-focal AS builder
WORKDIR /app

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN chmod +x mvnw && ./mvnw -B dependency:go-offline

COPY src ./src
RUN ./mvnw -B package -DskipTests   # should create target/whoami_premier_league-0.0.1-SNAPSHOT.jar

############ Runtime stage ##########
FROM eclipse-temurin:17-jre-focal
WORKDIR /app
RUN useradd -ms /bin/bash spring
USER spring

# Copy the built JAR and rename it
COPY --from=builder /app/target/whoami_premier_league-*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
